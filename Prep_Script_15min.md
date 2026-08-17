# 15-Minute Presentation Script — Northbridge Recovery Plan
*Rehearsal script for the Week 6 steering committee walkthrough (Sarah, Marcus, Diana, Tom). Target: 14:00–15:00 total, leaves buffer before the 45-min open discussion.*

Pacing note: this is a 6-slide deck for a 15-min slot — that's 2.5 min/slide average. Don't spread evenly; the integration decision (Slide 3) and the plan (Slide 4) are where you earn credibility. Slide 1 and 6 should be fast.

---

## Slide 1 — Title (0:00–0:20)

> "Thanks everyone for making time. I'm going to walk through where we stand at Week 5, the two integration decisions I need your sign-off on today, the 7-week plan to Go-Live, what I need from each of you, and how we'll know at Week 12 whether this worked. Fifteen minutes, then I want the rest of the hour to be yours."

Sets the contract: they know what's coming and that you're leaving room for discussion. Don't linger here.

---

## Slide 2 — Where We Stand at Week 5 (0:20–2:20, ~2 min)

> "Starting with the honest read. The foundation is solid — kickoff's complete, data feed contents are agreed, store master data is done, all 25 tablets are provisioned, and the product catalog issue that's been sitting in the email thread is now root-caused, not just flagged.
>
> "Two things that were open when I took this over — how Northbridge data lands in RELEX, and how RELEX orders land back in SAP — were never actually finalized. I'm closing both today, pending your sign-off, and I'll walk through the recommendation on the next slide.
>
> "SSO has three open items with your security team. We have a working session scheduled this week. It is not a blocker today — it becomes one if it slips past Week 7, because that starts squeezing the testing window before Go-Live.
>
> "No change to pilot scope: 25 stores, Iowa and Missouri, Fresh Produce, Bakery, Dairy, Frozen.
>
> "Bottom line: on track for Week 12, with two decisions closing this week that need your sign-off today."

**Watch this tension**: your internal triage doc calls the project "At Risk" (mTLS lead time + SSO schedule risk), while this slide says "on track." That's not a contradiction if you frame it right — say it once, deliberately, don't wait to be caught:

> "I want to be precise about what 'on track' means here — it's on track *if* two things land on schedule that are outside my control: the mTLS certificate, which has a 4-to-6-week lead time with no buffer against the Week 9 test window, and SSO closing this week rather than slipping again. Those are the two items I'm watching hardest, and they're the reason I'm asking for a 90-minute session this week instead of letting it drift."

This is the line that shows you're not sugarcoating and not catastrophizing — exactly what the brief says they're testing.

---

## Slide 3 — Data Integration Plan: Recommendation (2:20–5:20, ~3 min)

This is the technical spine of the deck. Slow down here.

> "Two decisions, one recommendation each, and I'll tell you what I rejected and why, because the 'why not' is as important as the 'why.'
>
> "**Data in.** I'm recommending read-only access to NB_RETAIL_CORE in Snowflake. One integration point covers sales, deliveries, stock movements, and product catalog. Raj has already offered this access, and it avoids the 6-to-8-week new-API approval process that the alternative would trigger. I looked at SFTP-per-feed direct from SAP CAR and IS-Retail — that's six separate integration points for no material benefit over the Snowflake route. Rejected.
>
> "**Orders out.** I'm recommending we reuse the existing SFTP order channel — a flat-file drop into Z_ORD_INBOUND_PROC. This is four-year-old production infrastructure you already run for vendor PO confirmations, so it's proven, not new. The alternative was SAP IDoc, WHSORD03 — that needs about six weeks of Basis work plus two weeks of ABAP dev, and Marcus's team doesn't have that capacity until January. That's a hard no for a Week 12 Go-Live.
>
> "One limitation I want flagged, not hidden: for the pilot, orders will carry ORDER_TYPE = REGULAR. It's not the ideal long-term tag, and it's a fast-follow ask to Raj's team, not a blocker to Go-Live.
>
> "The theme across both: we're reusing infrastructure you already operate today. That's what makes a 7-week timeline credible instead of aspirational."

Marcus owns SAP and Snowflake — this slide is really addressed to him. Make eye contact there when you say "reused infrastructure."

---

## Slide 4 — 7-Week Plan to Go-Live (5:20–8:20, ~3 min)

Don't read the table row by row — narrate the shape of it and land on the three weeks that matter.

> "Week by week, named owners, real dependencies. I won't read every row, but three weeks matter most.
>
> "**Week 7**: SSO goes live end-to-end, and the UPC dedup rule gets built into the ingestion pipeline — that's gated on this week's sign-off.
>
> "**Week 9**: first end-to-end test order — a real RELEX proposal, through the SFTP file, accepted by SAP, for a single pilot store. That's the first time we prove the whole chain works, not just each piece.
>
> "**Week 11**: parallel run — store managers review RELEX proposals alongside their manual ordering, no cutover yet. That has to be clean before I recommend Go-Live in Week 12.
>
> "Every week has a named owner — you'll notice it's never just 'FDE,' it's FDE plus whoever on your side needs to be in the room. That's deliberate; I'm not asking for a blank check, I'm asking for specific people at specific weeks."

---

## Slide 5 — What We Need From Northbridge (8:20–10:50, ~2.5 min)

> "Six asks, each with an owner and a date — not a general risk list.
>
> "Two are due *this week*, from Sarah: sign-off on the integration approach I just walked through, and the decision to accept ORDER_TYPE = REGULAR for the pilot.
>
> "The one I'd flag hardest: the mTLS client certificate request, filed with Lisa's security team, four-to-six week lead time, needed by Week 10. That clock needs to start now — it's not compressible, and it's the one item on this slide that isn't in any of our control once it's filed."

This is the moment to make direct eye contact with whoever owns each ask — Sarah for sign-off, Marcus for the Azure AD / Workday claim question, Lisa's team (via Marcus if Lisa isn't in the room) for the cert, Tom and Diana for the tablet model.

---

## Slide 6 — Go / No-Go Criteria (10:50–13:00, ~2 min)

> "Five criteria, all measurable, all agreed today rather than argued about in Week 12.
>
> "Ninety-five percent or higher SAP order acceptance rate across all 25 stores. Under 2% unresolved product master conflicts after dedup, checked against a fresh extract. Twenty of 25 store managers signing off that the tablet workflow is usable in daily operation. SSO live for every store and category manager with correct per-store scoping. And zero P1 data-quality incidents during the Week 11 parallel run.
>
> "Next checkpoint is Week 8, same format, same audience — so nobody's surprised in Week 12."

---

## Close (13:00–14:00)

> "That's the plan: two decisions closed today, a 7-week path with named owners, specific asks with dates, and criteria we'll all agree meant success or didn't. I'd rather spend the rest of this hour in the details you care about than rush through slides — happy to go wherever you want to start."

Stop talking. Let silence sit for a beat before anyone jumps in — don't fill it.

---

## Pocket prep — triage doc, for the 45-min discussion (not presented, but be ready)

The Technical Triage Document is internal-only — don't volunteer it unprompted, but Marcus or a sharp technical question will pull on it:

1. **UPC identity**: 8/63 nulls, 11/63 duplicate-UPC rows across 5 groups, all still `Active_Flag=Y`. One group (`182084873288`) is two genuinely different products sharing a UPC — the auto-resolve rule can't touch it, it needs manual flag. Fix ships Monday, re-checked against a fresh extract vs. the <2% Go/No-Go bar.
2. **Category free text**: 16 raw strings for 4 departments (casing/whitespace, not typos) — breaks department-level dashboards if ingested as exact-match. Canonicalization map in the pipeline, unmapped values flagged not guessed.
3. **Frozen pack-size gaps**: 4/13 Frozen SKUs have blank `Pack_Size`. SAP rejects the *entire order file* on one bad line, and files batch multiple stores — so one missing value can take down every store's order that day. Emitter will hard-block, not default, and you're confirming with Raj/Marcus whether files can be split per-store to contain the blast radius.
4. **Honest status call**: At Risk, specifically because of two schedule dependencies outside your control — mTLS cert lead time (Week 9–11 landing window collides with first live test) and SSO (already a week behind, Lisa hard to schedule). Everything else — the two integration decisions, the data-quality issues — has a known, executable fix. If asked "why does the deck say on track and the triage doc say at risk," that's your answer: the deck states the condition under which "on track" holds.

If someone asks for the Slack message you'd send Data Eng, you have it verbatim in the triage doc — UPC dedup pairing Monday, category canonicalization before Week 8 staging, order-emitter hard-block validation before Week 9.
