# Full Technical Script — UPC Collision Deep-Dive as 15-Minute Presentation Copy
*Continuous spoken script, full technical depth, timed to run ~15 minutes read aloud at a measured pace (~140-150 wpm). Read straight through.*

---

**[0:00]**

"Before I get into the plan, I want to spend real time on one specific thing I found in the product master data, because it's the clearest example of the kind of problem this pilot is actually exposed to, and because the fix tells you something about how I want to run data quality for the rest of this engagement, not just this one case.

Northbridge IT sent over the product catalog and described it as clean. I want to walk you through why it wasn't, using one exact example, because 'the data had issues' isn't a useful sentence to anyone in this room and I don't want to give you one.

**[1:00]**

Here's what happened. In the sample extract, sixty-three SKUs, I found five groups where two or three different SKU numbers share the exact same UPC — the same twelve-digit barcode. Four of those five groups are the same story, and it's a boring story: Northbridge reissues a SKU number at some point, a new number goes live, and the old one never gets deactivated. Both rows carry the same barcode, same description, same supplier, same cost, same price — the only difference is the SKU number and the word 'legacy' tacked onto the description. That's routine. Any retailer running SAP IS-Retail for a few years accumulates this.

**[2:15]**

The fifth group is the one I want you to actually hear the detail on, because it's not routine, and treating it like the other four would have been a real mistake. UPC 182084873288 appears on three rows. SKU 100056, 'Burrito Bean 8-pack.' SKU 100063, 'Burrito Bean 8-pack, legacy' — that's the same reissue pattern as the other four, fine. But SKU 100057 is 'Waffles Buttermilk 10-count' — a completely different product — carrying that exact same barcode. Different supplier code, VENDOR_007 instead of VENDOR_022. Different cost. Different retail price. The only field where it matches the Burrito Bean rows is the UPC itself. That's not a reissue. That's a keying error — someone typed the wrong barcode onto that row, or copy-pasted from an adjacent line, and nothing in Northbridge's data entry process validates UPC uniqueness at the point of entry. That last part is the actual root cause, not the specific typo.

**[3:45]**

Now, here's why that distinction matters mechanically, not just as a curiosity. The dedup rule that was already documented for this project says: when SKUs share a UPC, the primary record is whichever has the lower SKU number. That rule is correct for four of my five groups. Applied blindly to the fifth, it would have designated SKU 100056 as primary and treated both 100057 and 100063 as its duplicates — which means Waffles Buttermilk's entire sales and stock history would get silently folded into Burrito Bean's identity on ingest. Two products with nothing in common except a data entry mistake would end up sharing one corrupted demand history, and there is nothing in that process that would flag it as wrong, because structurally it looks identical to the four legitimate cases sitting right next to it in the same file.

**[5:15]**

So the fix I built splits the rule on one additional signal: does the description match, allowing for a 'legacy' suffix. Same UPC, matching description — auto-resolve to the lower SKU, mark the other inactive, no human touches it. Same UPC, non-matching description — stop. Hard-flag it, no auto-merge, a person makes the call. That's what let the two genuine Burrito Bean rows resolve automatically while pulling Waffles out cleanly before anything downstream ever saw a corrupted number.

**[6:30]**

I want to be straight with you about the tradeoffs in that fix, because I don't think a data quality rule is trustworthy until someone has stress-tested it out loud, and I'd rather do that here than have you find the gap later.

The advantages are real: it's cheap to implement, it's one string comparison, no new tooling. It scales — this sample is sixty-three SKUs, the full pilot catalog is thousands, and this rule handles the routine ninety percent automatically instead of queueing all of it for manual review. And critically, it fails safe. When the heuristic can't tell what it's looking at, it doesn't guess. It stops and asks a person.

**[8:00]**

But it is a heuristic, not a proof, and it has two honest failure directions. The first is a false negative: if a real, legitimate reissue also happened to reword the description — not just adding 'legacy,' but changing the wording itself — my exact-match comparison would treat that as a mismatch and kick a perfectly safe case to manual review. That's not dangerous, it's just noise, extra manual load I'd rather not create. The second is more serious: could two genuinely different products end up with matching descriptions on a shared UPC by coincidence, and get auto-merged anyway? At sixty-three rows, I don't see it happen. At full catalog scale, I can't rule it out from this sample alone. I don't have a clean engineering answer that makes that risk zero. What I have is a forcing function — the under-two-percent unresolved-conflict bar on the Go, No-Go criteria isn't just a gate at the end, it's the reason I'm asking Raj for a fresh extract to re-run this logic against, rather than building it once and assuming it holds.

**[9:45]**

I also want to walk you through what I didn't do, because I considered four other approaches to this and rejected three of them, and the reasoning matters more than the conclusion.

The first alternative was simplest: leave the original rule exactly as written, auto-merge every UPC duplicate to the lower SKU with no exception. That's the fastest option and it's exactly the rule that would have corrupted Waffles into Burrito Bean. I'm not doing that.

The second alternative was to stop trusting UPC entirely and use SKU number as the sole identity key, sidestepping the collision risk completely. That avoids this specific failure, but it stops solving the actual underlying problem — the four legitimate reissue pairs are still two different SKU numbers pointing at one physical product, so you'd trade a risk of a wrong merge for a guarantee of a double-count, which is the first problem in my triage document, not a fix for it.

**[11:15]**

The third alternative was to send every single duplicate-UPC pair to manual review, no automation at all. That's the safest option on paper — zero risk of a bad automated merge — but it doesn't scale. At full catalog volume, that's hundreds of routine legacy reissues landing in front of a buyer every week, and the realistic outcome of that isn't careful review, it's fatigue — someone starts rubber-stamping obviously-safe pairs without really checking, which quietly reintroduces the exact risk the manual step was supposed to prevent. And operationally, it doesn't fit the Week 7 pipeline date.

The fourth alternative was to hand the whole problem back to Northbridge — tell IT to clean the master data before we ingest it, since it is, after all, their data. That's fair in principle, but nobody on the Northbridge side caught this before I did, there's no dedicated data steward visible in this process, and waiting on that would blow the seven-week plan entirely. My job is to make this deployment work in the environment you actually have, not the one I'd prefer you had — so that becomes a parallel ask to your data engineering team, not a blocking dependency before I can move forward.

**[13:00]**

Last thing, and I want to say this slowly because it's the actual reason this is worth fifteen minutes of a steering committee's time instead of a footnote in an appendix.

If the original rule had shipped as written, here is exactly what happens. Waffles Buttermilk's sales and stock history merges into Burrito Bean's SKU on ingest. From that point forward, RELEX is forecasting Burrito Bean demand off a blended curve built from two products with completely different seasonality and sell-through — a frozen breakfast item and a frozen entrée. The replenishment number it produces looks completely reasonable. Nobody can eyeball it and know it's wrong, because it isn't obviously wrong, it's just built on the wrong history.

**[14:00]**

Meanwhile Waffles, as an identity in the system, has effectively disappeared — its sales history got absorbed into another SKU — so RELEX has nothing to base a reorder recommendation on. It either stops recommending the item or recommends close to zero, and shelves go empty on a product that was selling fine before we touched it.

Here is the part that makes this genuinely dangerous rather than just an annoying bug: this doesn't fail loudly. There's no error, no rejected file — the pack-size problem I flag separately gets caught because SAP rejects the order file outright when it sees bad data. This one doesn't get that safety net. The pipeline runs clean and produces a confidently wrong number. Which means the realistic point this gets discovered isn't this week while I'm building the ingestion pipeline — it's Week 11, in the parallel run, when a store manager or someone on Diana's team notices Waffles isn't reordering and Burrito Bean's numbers look strange. That is the single worst moment for a foundational data problem to surface: right as we're supposed to be building confidence for the Go, No-Go call, not unwinding a silent data corruption issue from five weeks earlier.

**[15:00]**

That gap — a pipeline that visibly breaks versus a pipeline that runs clean and quietly lies to you — is why this one row got a hard stop instead of an automated guess. And it's the standard I want applied to every data quality decision in this pilot, not just this one."
