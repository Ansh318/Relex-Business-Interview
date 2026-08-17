# Deep-Dive Script — UPC Collision (SKU 100056/100057/100063)
*For the 45-min discussion. This is the single technical point most likely to get pulled on hard — it's the one place your resolution rule almost breaks. Know it cold.*

---

## 1. What happened

> "Let me walk through the specific case, because it's the one that changed how I wrote the resolution rule.
>
> "In the product master sample, UPC `182084873288` appears on three separate rows: SKU 100056 'Burrito Bean 8pk,' SKU 100057 'Waffles Buttermilk 10ct,' and SKU 100063 'Burrito Bean 8pk (legacy).' Same 12-digit UPC, typed into three different rows.
>
> "Two of those three are obviously the same item — 100056 and 100063 match on description, supplier code, cost, and price; the only difference is the SKU number and the word '(legacy)' in the description. That's Northbridge reissuing a SKU number at some point and never deactivating the old one — I see the identical pattern four other times in the sample, it's a routine occurrence.
>
> "But the third row, Waffles, doesn't match on *anything else*. Different product, different supplier — VENDOR_007 instead of VENDOR_022 — different cost, different price. The only thing it shares with the other two is that one field. That's not a reissue, that's a keying error: someone typed, copy-pasted, or pulled a stale UPC onto the wrong row, and there's nothing in Northbridge's data entry process that validates UPC uniqueness at the point of entry. That last part is the actual root cause — worth saying explicitly if IT asks 'how does this even happen.'"

---

## 2. Why the current approach

> "The dedup rule I inherited was simple: primary equals the lower SKU number when duplicates share a UPC. That rule works for four of my five duplicate groups. It fails on this one, because it assumes every UPC collision means 'same item, two numbers' — and here that assumption is false for one of the three rows.
>
> "So I split the rule into two paths on one signal: does the description match. If SKU A and SKU B share a UPC *and* their descriptions match (allowing for a '(legacy)' suffix), auto-resolve to the lower SKU, mark the other inactive. If they share a UPC but the descriptions *don't* match, don't touch it — hard-flag it for a human. That's what let the two clean Burrito Bean rows resolve automatically while pulling Waffles out for manual review instead of getting silently merged into Burrito Bean's identity."

---

## 3. Pros and cons of this approach

**Pros:**
> "It's cheap to build — one string comparison, no new tooling. It scales past this 63-row sample to the full catalog without more manual load, because the 90% case, the routine reissue, still auto-resolves. And it fails *safe* — when the heuristic can't tell, it stops and asks a human instead of guessing."

**Cons — say these before you're asked, it shows you've stress-tested your own fix:**
> "It's a heuristic, not a proof. It only catches mismatches the way this sample happens to present them — a clean product-name difference. Two honest risks I'd want to validate against a fuller extract:
>
> "One — false negative risk: if a real reissue *also* changed the description slightly, not just adding '(legacy)' but rewording it, exact-match description comparison would treat it as a mismatch and kick a genuinely safe case to manual review. That's not dangerous, just noisy — more manual load than necessary. I'd watch the flagged-for-review volume on the first fresh extract; if it's high, that's the signal to loosen the match to fuzzy comparison.
>
> "Two, the more serious direction — false positive risk: could two genuinely different products end up with *matching* descriptions on a shared UPC by coincidence, and auto-merge anyway? Unlikely at 63 rows, more plausible at full catalog scale. I don't have a hard fix for that in the sample data, I have a mitigation: the <2% unresolved-conflict bar isn't just a gate, it's a forcing function to get Raj to re-run this against a live extract before Week 8, not just trust the logic once and move on."

---

## 4. Alternatives considered

Have four in your pocket — you don't need to present all of them unprompted, but if Marcus asks "why not just X," you want an answer ready, not a stall.

1. **Keep the original rule as-is — auto-merge every UPC duplicate to the lower SKU, no exception.**
   *Rejected.* Fastest to ship, zero manual load — and it's exactly the rule that would've silently merged Waffles into Burrito Bean. This is the rule I found, not the rule I'm proposing.

2. **Ignore UPC entirely, use SKU as the sole identity key.**
   *Rejected.* Sidesteps the collision risk completely, but it doesn't solve the actual problem — the four legitimate reissue pairs are still two different SKU numbers pointing at one physical product. You'd just trade "risk of wrong merge" for "guaranteed double-count," which is the exact failure the triage doc opens with.

3. **No auto-resolution at all — every duplicate UPC goes to manual review, always.**
   *Rejected for this timeline, not wrong in principle.* Safest option, zero risk of a bad merge. But it doesn't scale — this sample is 63 SKUs; the pilot catalog is thousands. Full manual review of every routine legacy reissue blows the Week 7 pipeline date, and it invites the failure mode where a buyer reviewing hundreds of obviously-safe pairs starts rubber-stamping and stops actually checking — which quietly reintroduces the exact risk you built the process to avoid.

4. **Push the cleanup back to Northbridge — "fix your master data before we ingest."**
   *Rejected as the sole path, kept as a parallel ask.* Technically fair, it is their data. But nobody on their side caught this before I did, there's no dedicated data steward in evidence, and waiting on them blows the 7-week plan. The FDE's job is to make the deployment work inside the client's actual environment, not the one you wish they had — so this becomes the Data Eng ask and the buyer-review flag in the fix, not a blocking dependency on Northbridge fixing their process first.

---

## 5. Worst-case scenario if this goes unaddressed

This is the part to deliver slowly — it's the "why should I care" payoff.

> "If the original rule ships as-is, here's exactly what happens, not in the abstract. Waffles Buttermilk's sales and stock history gets merged into Burrito Bean's SKU on ingest. From that point on, RELEX is forecasting 'Burrito Bean' demand off a blended curve of two products with completely different seasonality and velocity — a frozen breakfast item and a frozen entrée. The replenishment proposal for Burrito Bean is now wrong in a way nobody can eyeball and catch, because the number looks perfectly reasonable, it's just built on the wrong history.
>
> "Meanwhile Waffles, as an identity, has effectively vanished — its sales history is gone, absorbed into another SKU — so RELEX has nothing to base a reorder recommendation on. It either stops recommending Waffles or recommends near-zero. Shelves go empty on an item stores were selling fine before the pilot touched it.
>
> "Here's the part that makes this worse than a normal bug: **the pipeline doesn't fail.** No error, no rejected file, no red flag anywhere in the system — Problem 3's SAP validation catches bad pack-size data because SAP rejects the file outright. This doesn't get that safety net. It runs clean and produces confidently wrong numbers. So the realistic discovery point isn't Week 7 when I'm building the pipeline, it's Week 11, in the parallel run, when a store manager or Diana's category team notices Waffles isn't reordering and Burrito Bean's numbers look strange — right as we're supposed to be building confidence for the Week 12 Go/No-Go call, not debugging a silent data corruption issue from five weeks earlier.
>
> "That gap — broken pipeline versus pipeline that runs clean and lies to you — is exactly why this one row got a hard-block instead of a heuristic guess."
