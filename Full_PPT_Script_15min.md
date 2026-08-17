# Full Presentation Script — Why / Why Not / Worst Case, Every Slide
*Full precision version. Grounded in the kickoff memo, email thread, SAP order sample, and SSO spec — every "why not" and "worst case" below traces to a specific line in those documents, not a generic risk. Read at normal pace this runs ~25-30 min; trim before the live 15-min slot (cut suggestions marked [TRIM] at the end).*

---

## Slide 1 — Title

"Thanks everyone for making time. I'm going to walk through where we stand at Week 5, the two integration decisions I need your sign-off on today, the seven-week plan to Go-Live, what I need from each of you, and how we'll know at Week 12 whether this worked."

---

## Slide 2 — Where We Stand

**What / status.** "Foundation is solid — kickoff complete, data feed contents agreed, store master data done, twenty-five tablets provisioned. Two decisions that were never actually finalized close today: how data lands in RELEX, how orders land back in SAP."

**Why 'on track' is the honest call, precisely.** "I'm calling this on track, not green. On track *if* two things outside my control land on schedule — I'll name them on the asks slide. That's a deliberate distinction, not hedging."

**The product catalog — why, why not, worst case, in full.**

*What happened:* "Northbridge IT called the catalog clean. Raj's own email says otherwise — a 2022 vendor consolidation merged two parallel SKU numbering systems in a hurry, there's an eighteen-month-old open ticket on it, DATA-3041, and it's never been closed. In the sample, that shows up as five UPC-duplicate groups. Four are routine reissues. The fifth — UPC 182084873288 — has two Burrito Bean rows plus one completely unrelated product, Waffles Buttermilk, sharing that barcode by what's clearly a keying error, not a reissue."

*Why this fix (description-match split):* "Raj's own documented convention is 'primary equals lower SKU number when there are duplicates' — that's the existing rule, and it assumes every collision is the same item under two numbers. My fix keeps that rule for the ninety percent case but adds one check first: does the description actually match. Matches — auto-resolve, no human touches it. Doesn't match — hard stop, flagged for manual review."

*Why not the alternatives:* "I considered three other paths. Leave Raj's rule exactly as documented, no exception — that's the rule that would have merged Waffles into Burrito Bean, so no. Drop UPC as an identity signal entirely, key off SKU number alone — that avoids this specific collision but stops solving the double-count problem the four legitimate reissues create, since Raj confirms both old and new SKUs are still marked active with no plan to retire them. Send every duplicate to manual review, no automation — safest on paper, but DATA-3041 has been open eighteen months already, which tells you how a fully-manual queue performs against Northbridge's actual bandwidth. None of those beat the split rule."

*Worst case:* "If it ships as Raj's original rule, Waffles' sales history silently merges into Burrito Bean's. No error, no rejected file — Problem Three, the Frozen pack-size gaps, gets caught because SAP rejects the file outright on bad data. This doesn't get that safety net. It runs clean and produces a confidently wrong forecast. Realistic discovery point: Week 11, in the parallel run, exactly when we're supposed to be building confidence for the Go, No-Go call."

**SSO status line.** "SSO has three open items with your security team, working session scheduled this week — not a blocker today, becomes one past Week 7. No change to pilot scope."

---

## Slide 3 — Data Integration Plan

### Data in

**Recommendation:** "Read-only access to NB_RETAIL_CORE in Snowflake — one integration point covers sales, deliveries, stock movements, and product catalog."

**Why:** "Raj offered this directly — his email is explicit that Northbridge's change-management process for a new API out of SAP CAR requires architecture board approval, six to eight weeks, and he'd rather not stand up a new one just for us. Snowflake mirrors CAR already and bypasses that process entirely."

**Why not the alternative — SFTP-per-feed:** "The kickoff memo shows the original plan was six separate feeds — sales, deliveries, stock movements, catalog, store master, price and promo — each its own format, schedule, and mechanism. As of Week 4, three of those six were marked NOT STARTED. Raj's own note in the memo flags that daily SFTP for sales might not scale to five hundred stores with hourly transactions. Six integration points instead of one, for no material benefit — that's the read."

**Worst case if we'd gone the SFTP-per-feed route:** "Three of six feeds unbuilt with seven weeks left, each one a separate failure point, each on its own schedule — so a delay on any single feed among six independently threatens the pipeline, instead of one integration point with one thing to validate. And even on Snowflake, I'm not treating this as risk-free: the plan explicitly validates schema and freshness in Week 6, because if the Snowflake mirror lags CAR by hours, RELEX builds replenishment proposals on stale sales data — that's a live worst case, not a hypothetical, which is exactly why freshness validation is a named Week 6 milestone, not an assumption."

### Orders out

**Recommendation:** "The existing SFTP order channel — flat file into Z_ORD_INBOUND_PROC."

**Why:** "This is Marcus's own proposal, not mine — his email lays out three options when the IDoc route stalled: wrap orders as a flat file onto the existing vendor-PO SFTP channel, push Go-Live back four weeks, or bring in an outside IDoc specialist for two weeks. His email also confirms this file gets picked up by the same job used for vendor PO confirmations today, running four years in production."

**Why not IDoc, the SAP-blessed route:** "It needs a logical system defined in BD54, a partner profile in WE20, an RFC destination in SM59, a firewall opening on port 3300, a new service user, and Marcus's own estimate is six weeks of a SAP Basis consultant plus two weeks of an ABAP developer — 'none currently available due to the S/4 migration program,' his words. That's not a preference, it's a hard capacity wall Marcus flagged to Sarah back in February, before this project was even greenlit."

**Worst case — and this is the one I want to be precise about:** "The flat-file job was built for vendor PO confirmations, not AI-generated store orders. None of its three ORDER_TYPE values — REGULAR, PROMO, EMERGENCY — cleanly describes what we're sending, so pilot orders get tagged REGULAR as a workaround. Two concrete consequences. First, the actual reject log from last week shows this validation is strict and unforgiving — a SKU not found in the material master, a quantity that isn't a multiple of the case-pack size, a vendor not authorized for that store — any one of those rejects the *entire file*, and files batch multiple stores. One bad line from an unresolved data issue — the Frozen pack-size gaps, for instance — takes down every store's order in that file for that day. Second, tagging everything REGULAR means Northbridge's own systems can't distinguish a RELEX-generated order from a human buyer's PO in their own reporting — if something goes wrong, nobody can filter 'which of today's orders came from RELEX' without cross-referencing separately. That's the real cost of the REGULAR workaround, and it's why it's on the asks slide as a decision Raj and Marcus need to actively accept, not something I quietly assumed."

---

## Slide 4 — 7-Week Plan

**Why this sequence, specifically the shape of it — single store first, then scale, then parallel run before cutover.** "Week 9 is one store, not twenty-five. Week 10 expands to all twenty-five. Week 11 is a parallel run — managers see RELEX proposals next to their existing manual process, nobody's live yet. Week 12 is the only week real orders replace manual ones."

**Why not compress it — go straight to all 25 stores at Week 9, or skip the parallel run and cut over right after the Week 9 test:** "Given what the SAP reject log actually shows — one bad line rejects the whole file, and files batch by store — testing on one store first means a bad line only costs one store's order while we shake out the ORDER_TYPE and pack-size issues, not all twenty-five at once in week one. And skipping the parallel run removes the one checkpoint where a store manager catches a bad proposal before it becomes a real order in front of a real customer. Diana's already brought regional VPs through Cedar Rapids to see this system — those are the same people deciding on Phase 2 rollout. A visibly wrong live order in front of that audience costs more than two extra weeks of parallel running."

**Worst case if the sequence gets compressed — realistically, by an mTLS or SSO slip eating into weeks 9 through 11.** "Sarah went to the board on this in March — her own email says she's put 'real budget and real political capital' behind it. If the schedule slips, the choice isn't neutral: either push Go-Live, which reads as this pilot underperforming right as Phase 2 decisions are being shaped, or hold the date and compress the parallel run, which means going live having validated the full chain against exactly one store instead of twenty-five, with whatever data issues haven't fully surfaced yet. That's how you get an empty-shelf problem in front of the exact store manager — Mike at Cedar Rapids, who already flagged connectivity concerns on the tablet — that Tom has to explain."

---

## Slide 5 — What We Need From Northbridge

**mTLS — why, why not, worst case.**

*Why this is the ask, specifically:* "The Snowflake role Raj offered answers *what* data we read. It doesn't answer *how* we authenticate to it. Lisa's spec is explicit: Northbridge doesn't issue OAuth client credentials to external vendors, their standard for service-to-service auth is a client certificate off their internal CA, four-to-six week lead time, and it only starts after a security review."

*Why not push back and negotiate OAuth, which the previous FDE actually tried:* "The spec shows that conversation already happened — Alex asked Lisa directly whether an exception was possible or whether a different integration pattern made more sense. No resolution is recorded, and Lisa's language elsewhere in the doc reads as policy, not preference. Relitigating a fixed security standard costs calendar time we don't have; the better use of that time is managing the lead time, which is exactly what filing it Week 5 does."

*Worst case:* "Filed Week 5, four-to-six weeks lands anywhere from Week 9 to Week 11 — the same window as the single-store live test and the parallel run. If it lands late, RELEX literally cannot authenticate to read Northbridge data during the weeks it needs to run those two milestones. That's not a delay you can resource your way out of. It's a fixed external lead time colliding with the two events that most need to happen on schedule."

**SSO — why, why not, worst case.**

*Why this needs a dedicated working session, not just 'please hurry':* "The kickoff plan had SSO done by end of Week 4 — already a week behind by the time I started. The reason isn't generic slowness. Lisa was out on family leave in Week 3, a design went around without her — OIDC, and a group mapping giving every store manager access to every store — and when she came back she rejected three separate pieces of it at once: OIDC against Northbridge's SAML standard for third-party SaaS, the all-store access against least-privilege policy, and OAuth client credentials against the mTLS requirement. That's not one open item, it's a design that needs to be substantively redone with the actual policy owner in the room, which is why the ask is ninety focused minutes with Lisa and Marcus, not a status nudge."

*Why not proceed with the already-drafted design to save time:* "It doesn't meet Northbridge's own policy as Lisa stated it. Pushing it through either gets rejected again, or gets approved on paper and ships a real access-control gap — every store manager able to see and place orders for all twenty-five stores — that surfaces the moment Tom or Diana's team notices it in the parallel run, or worse, in a security audit after Go-Live."

*Worst case:* "The spec's own language is that a slip past Week 7 'starts squeezing the testing window before Go-Live.' And per-store scoping isn't fully closed even once the working session happens — it still depends on Marcus confirming whether Azure AD can pull a store_id claim from Workday, which is why that's its own line item on this slide, not folded into 'SSO working session' as if one meeting resolves it."

---

## Slide 6 — Go / No-Go Criteria

**Why these five, specifically:** "Each one maps to a failure mode I've already diagnosed, not a generic KPI. Ninety-five percent SAP order acceptance tests whether the order emitter and the ORDER_TYPE workaround actually hold up at volume, not just in one test order. Under two percent unresolved product master conflicts is the exact bar the UPC and category fixes get re-checked against on a fresh extract. Twenty of twenty-five managers signing off usability is the adoption side — Diana's world, and it's the same workflow Tom's already fielding real questions about, like Mike at Cedar Rapids and tablet connectivity. SSO live with correct per-store scoping is Lisa's least-privilege requirement, made measurable. Zero P1 incidents during the parallel run is the real-world safety net before anyone commits to live orders."

**Why not softer criteria:** "The slide itself says it — no 'system feels ready' language, on purpose. Sarah has board exposure on this, Diana wants a win in front of the CEO, regional VPs have already seen a demo. That's exactly the kind of pressure that turns a Go-Live decision into a political call instead of a technical one if the bar isn't numeric and agreed in advance. This protects the decision — and it protects me, so I'm not making a judgment call alone in Week 12 with no pre-agreed reference point."

**Why not stricter criteria — 100% acceptance, 25 of 25 managers, zero conflicts:** "Unrealistic for a first live rollout at this complexity in seven weeks. Set the bar there and one of two things happens: it gets quietly waived when missed, which defeats the point of having a hard bar, or a real Go-Live gets blocked over noise-level issues instead of substantive ones. Ninety-five, two, twenty-of-twenty-five are calibrated to catch real problems without punishing expected first-rollout friction."

**Worst case — two directions worth naming out loud.** "First: these numbers are only meaningful if they run against the full twenty-five stores and the full catalog, not a curated subset. If order acceptance hits ninety-five percent because problem SKUs got quietly excluded from the test rather than fixed, the number passes and the actual risk — one bad line taking down a real store's orders — ships anyway. Second, if the criteria genuinely aren't met at Week 12, the answer isn't automatically 'go live anyway' or 'cancel the project' — it can be a partial Go, live for the stores or departments that clear the bar, held back where they don't. I'd rather have that conversation now, as a real option, than have it improvised in the room in Week 12."

---

## [TRIM] — cuts to get back to 15 minutes

If reading this straight through runs long, cut in this order — least load-bearing first:
1. Slide 6: drop the "why not stricter criteria" paragraph — the "why not softer" one carries the point.
2. Slide 4: shorten the worst-case paragraph to the first two sentences; drop the Mike/Cedar Rapids callback.
3. Slide 3: on Data In, drop the Snowflake-freshness worst-case aside; keep the SFTP-per-feed rejection.
4. Slide 5, mTLS: cut the "why not push back and negotiate OAuth" paragraph — keep why + worst case only.
5. Slide 2: if still over time, compress the UPC "why not the alternatives" to one sentence naming all three and the one-line reason all three lose to the split rule.

Slide 3's Orders Out worst case and Slide 2's UPC worst case are the two paragraphs to protect at all costs — they're the ones a technical stakeholder is most likely to probe, and they're the ones with the sharpest concrete grounding.
