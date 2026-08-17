# Final 15-Minute Presentation Script — Northbridge Recovery Plan
*The one script to actually deliver from at the Week 6 steering committee walkthrough (Sarah, Marcus, Diana, Tom). Target 14:00, leaves buffer before the 45-min open discussion. Consolidated from the longer rehearsal drafts — this is the trimmed, delivery-ready version.*

**Pacing:** 6 slides, ~15 minutes = 2.5 min/slide average, but don't spread evenly. Slides 3 and 4 (the integration decision and the plan) are where you earn credibility — slow down there. Slides 1 and 6 should move fast.

Spoken lines are in blockquotes. Everything else is a delivery note — don't say it out loud.

---

## Slide 1 — Title (0:00–0:20)

> "Thanks everyone for making time. I'm going to walk through where we stand at Week 5, the two integration decisions I need your sign-off on today, the 7-week plan to Go-Live, what I need from each of you, and how we'll know at Week 12 whether this worked. Fifteen minutes, then I want the rest of the hour to be yours."

Sets the contract up front. Don't linger — this slide's only job is to tell them what's coming.

---

## Slide 2 — Where We Stand at Week 5 (0:20–2:30, ~2 min)

> "Starting with the honest read. The foundation is solid — kickoff's complete, data feed contents are agreed, store master data is done, all 25 tablets are provisioned, and the product catalog issue that's been sitting in the email thread is now root-caused, not just flagged.
>
> "Two things that were open when I took this over — how Northbridge data lands in RELEX, and how RELEX orders land back in SAP — were never actually finalized. I'm closing both today, pending your sign-off, and I'll walk through the recommendation on the next slide.
>
> "SSO has three open items with your security team. We have a working session scheduled this week. It's not a blocker today — it becomes one if it slips past Week 7, because that starts squeezing the testing window before Go-Live.
>
> "No change to pilot scope: 25 stores, Iowa and Missouri, Fresh Produce, Bakery, Dairy, Frozen."

**Say this precision line deliberately, don't wait to be asked:**
> "I want to be precise about what 'on track' means here — it's on track *if* two things land on schedule that are outside my control: the mTLS certificate, four-to-six week lead time with no buffer against the Week 9 test window, and SSO closing this week rather than slipping again. Those are the two items I'm watching hardest, which is why I'm asking for a 90-minute session this week instead of letting it drift."

This is the line that shows you're neither sugarcoating nor catastrophizing — exactly what the brief says they're testing. It also pre-empts the "your internal doc says At Risk" question before anyone has to ask it.

---

## Slide 3 — Data Integration Plan: Recommendation (2:30–5:30, ~3 min)

Technical spine of the deck. Slow down. Marcus owns SAP and Snowflake — this slide is really addressed to him.

> "Two decisions, one recommendation each — and I'll tell you what I rejected and why, because the 'why not' matters as much as the 'why.'
>
> "**Data in.** I'm recommending read-only access to NB_RETAIL_CORE in Snowflake — one integration point covers sales, deliveries, stock movements, and product catalog. Raj has already offered this access, and it avoids the six-to-eight-week new-API approval process the alternative would trigger. I looked at SFTP-per-feed direct from SAP CAR and IS-Retail — six separate integration points for no material benefit over the Snowflake route. Rejected.
>
> "**Orders out.** I'm recommending we reuse the existing SFTP order channel — a flat-file drop into `Z_ORD_INBOUND_PROC`. This is four-year-old production infrastructure you already run for vendor PO confirmations, so it's proven, not new. The alternative was SAP IDoc — that needs roughly six weeks of Basis work plus two weeks of ABAP dev, and that capacity doesn't exist until January because of the S/4 program. That's a hard no for a Week 12 Go-Live.
>
> "One limitation I want flagged, not hidden: for the pilot, orders carry `ORDER_TYPE = REGULAR`. Not the ideal long-term tag — it's a fast-follow ask to Raj's team, not a blocker to Go-Live.
>
> "The theme across both: we're reusing infrastructure you already operate today. That's what makes a seven-week timeline credible instead of aspirational."

---

## Slide 4 — 7-Week Plan to Go-Live (5:30–8:30, ~3 min)

Don't read the table row by row — narrate the shape of it, land on the three weeks that matter.

> "Week by week, named owners, real dependencies. I won't read every row, but three weeks matter most.
>
> "**Week 7** — SSO goes live end-to-end, and the UPC dedup rule gets built into the ingestion pipeline. Both gated on today's sign-off.
>
> "**Week 9** — first end-to-end test order: a real RELEX proposal, through the SFTP file, accepted by SAP, for a single pilot store. First time we prove the whole chain, not just each piece.
>
> "**Week 11** — parallel run: store managers review RELEX proposals alongside their manual ordering, no cutover yet. Has to be clean before I recommend Go-Live in Week 12.
>
> "Every week has a named owner, and it's never just 'FDE' — it's FDE plus whoever on your side needs to be in the room. I'm not asking for a blank check, I'm asking for specific people at specific weeks."

**Why single-store-first, not all 25 at once** (say only if asked, otherwise skip — it's in your back pocket): the SAP reject log shows one bad line takes down the *entire file*, and files batch by store. Testing on one store first means a bad line costs one store's order while the pack-size/ORDER_TYPE issues get shaken out — not all 25 at once.

---

## Slide 5 — What We Need From Northbridge (8:30–11:00, ~2.5 min)

Make direct eye contact with whoever owns each ask as you say it.

> "Six asks, each with an owner and a date — not a general risk list.
>
> "Two are due *this week*, from Sarah: sign-off on the integration approach I just walked through, and the decision to accept `ORDER_TYPE = REGULAR` for the pilot.
>
> "The one I'd flag hardest: the mTLS client certificate request, filed with Lisa's security team, four-to-six week lead time, needed by Week 10. That clock needs to start now — it's the one item on this slide that isn't in any of our control once it's filed, so the ask is to file it today, not to compress the lead time."

If there's time, name the rest quickly: Marcus on the Azure AD / Workday `store_id` claim question, Lisa's team on the cert, Tom and Diana on tablet install and the shared-device model.

---

## Slide 6 — Go / No-Go Criteria (11:00–13:00, ~2 min)

> "Five criteria, all measurable, all agreed today rather than argued about in Week 12.
>
> "Ninety-five percent or higher SAP order acceptance across all 25 stores. Under two percent unresolved product master conflicts after dedup, checked against a fresh extract. Twenty of twenty-five store managers signing off the tablet workflow is usable in daily operation. SSO live for every store and category manager with correct per-store scoping. Zero P1 data-quality incidents during the Week 11 parallel run.
>
> "Next checkpoint is Week 8, same format, same audience — so nobody's surprised in Week 12."

---

## Close (13:00–14:00)

> "That's the plan: two decisions closed today, a seven-week path with named owners, specific asks with dates, and criteria we'll all agree meant success or didn't. I'd rather spend the rest of this hour in the details you care about than rush through slides — happy to go wherever you want to start."

Stop talking. Let the silence sit for a beat before anyone jumps in — don't fill it.

---

## Pocket prep — have this cold, don't present it unprompted

The Technical Triage Document is internal-only. A sharp technical question from Marcus (or either RELEX interviewer) will pull on it — see [Interview_QA_Prep.md](Interview_QA_Prep.md) for the full Q&A version.

1. **UPC identity** — 8/63 nulls, 11/63 duplicate-UPC rows across 5 groups, all still `Active_Flag=Y`. One group (`182084873288`) is two genuinely different products sharing a UPC — auto-resolve can't touch it, needs a manual flag. Fix ships Monday, re-checked against a fresh extract vs. the <2% Go/No-Go bar.
2. **Category free text** — 16 raw strings for 4 departments (casing/whitespace, not typos) — breaks department-level dashboards on exact-match ingest. Canonicalization map in the pipeline; unmapped values flagged, not guessed.
3. **Frozen pack-size gaps** — 4/13 Frozen SKUs have blank `Pack_Size`. SAP rejects the *entire order file* on one bad line, and files batch multiple stores — one missing value can take down every store's order that day. Emitter hard-blocks, doesn't default; confirming with Raj/Marcus whether files can be split per-store to contain the blast radius.
4. **Honest status call: At Risk** — specifically because of two schedule dependencies outside your control (mTLS lead time colliding with the Week 9–11 test window; SSO already a week behind, Lisa hard to schedule). Everything else has a known, executable fix. If asked why the deck says "on track" and the triage doc says "At Risk": the deck states the condition under which "on track" holds.
5. **The Slack ask to Data Eng**, verbatim if asked: UPC dedup pairing session Monday; category canonicalization before Week 8 staging; order-emitter hard-block validation before the Week 9 live test.

**If time runs short, cut in this order:** (1) Slide 6 — drop straight to the five numbers, no framing; (2) Slide 4 — skip the single-store-first rationale unless asked; (3) Slide 5 — name only the mTLS ask, list the rest without elaboration; (4) Slide 3 — drop to one sentence per recommendation, keep both "why not" lines intact (they're what a technical stakeholder is most likely to probe).
