# Interview Q&A Prep — Northbridge Recovery Plan
*For the 45-minute open discussion (and any mid-presentation interruptions) with two RELEX team members. Organized by who's likely asking and what they're actually testing. Answers are short on purpose — say the first two sentences, then stop and let them pull the thread if they want more.*

---

## How to use this doc

You won't get asked all of these. Skim it once end to end the night before, then use it as a lookup, not a script to memorize. If a question surprises you and isn't here, fall back to the pattern every answer below follows: **name the fact → say your call → say why → name the risk you're not fully sure about.** That pattern is what's actually being graded, not perfect recall.

If you truly don't know something, say so and say what you'd do to find out. "I don't know, I'd check with Raj" is a better answer than a guess dressed up as confidence.

---

## A. Sarah Chen (COO) — status, risk, board narrative

**"Is Week 12 still real?"**
> On track, conditionally — if two things outside my control land on schedule: the mTLS cert (4–6 week lead time, filed this week) and SSO closing this week instead of slipping again. Those are the two items I'm watching hardest. Everything inside my control — the two integration decisions, the data-quality fixes — has a known, executable path.

**"Tom said the data work is 'ongoing.' What does that actually mean?"**
> It means three specific things, not a vague status. Product catalog: root-caused, fix ships Monday. Sales/deliveries/stock/catalog ingestion: recommending one Snowflake read instead of six separate SFTP feeds, cuts the integration surface from six failure points to one. Order flow back to SAP: recommending we reuse the 4-year-old vendor-PO SFTP channel rather than wait on IDoc, which needs SAP capacity Marcus doesn't have until January.

**"Why should I trust 'on track' when your internal document says 'At Risk'?"** *(only answer if they've clearly seen or been told about the triage doc)*
> They're not contradictory, they're answering different questions. "On track" states the condition — the two external dependencies land on time. "At Risk" is the internal call because those two dependencies are outside my control and have zero schedule buffer. I'd rather tell you the condition than round it up to green.

**"What do you need from me specifically, today?"**
> Two sign-offs: the Snowflake-in / SFTP-out integration approach, and accepting that pilot orders carry `ORDER_TYPE = REGULAR` as an interim tag — not ideal, but not a blocker, and it's a fast-follow ask to Data Eng, not something I'm quietly hiding.

**"What happens if mTLS or SSO slips?"**
> Be honest, don't catastrophize: it doesn't kill the pilot, but it compresses the parallel-run window, which is the one checkpoint where a store manager catches a bad proposal before it becomes a real order. If it slips past Week 7, I'd rather have the conversation about trimming to fewer pilot stores at Week 12 than silently defend an unrealistic date.

---

## B. Marcus Reilly (VP IT) — technical, SAP, Snowflake, capacity

**"Why Snowflake instead of the six feeds we already agreed to?"**
> Raj offered it directly — new APIs out of CAR need architecture board approval, 6–8 weeks, and Snowflake already mirrors CAR read-only. One integration point instead of six, and three of the six original feeds were still NOT STARTED as of Week 4.

**"Why not just push through the IDoc route — it's the 'right way'?"**
> Your own estimate is 6 weeks of Basis plus 2 weeks of ABAP dev, and none of that capacity exists until January because of the S/4 program. That's not a preference, it's a hard capacity wall you flagged to Sarah in February. Choosing it anyway would mean choosing to miss Week 12.

**"The flat-file job was built for vendor PO confirmations. Are you comfortable running AI-generated store orders through it?"**
> Mostly yes, with one flagged limitation: none of the existing `ORDER_TYPE` values (REGULAR/PROMO/EMERGENCY) cleanly describe an AI-generated replenishment order, so pilot orders get tagged REGULAR as a workaround. That means Northbridge can't filter "which of today's orders came from RELEX" without cross-referencing separately — that's on the asks slide as a decision you and Raj need to actively accept, not something I assumed.

**"What happens when a bad line hits that file?"**
> Per your own reject log, the entire file is rejected, not just the bad line — and files batch multiple stores. That's exactly why the plan tests one store in Week 9 before scaling to 25 in Week 10: a bad line costs one store's order, not all 25, while we shake out the pack-size and ORDER_TYPE issues.

**"Can Azure AD pull a `store_id` claim from Workday?"**
> Don't know yet — that's explicitly on the asks slide as a decision that needs you specifically, because it determines whether we do per-store scoping via custom claim or fall back to one AD group per store, which is uglier to maintain at 500-store scale.

**"Why do you think the previous FDE didn't get this done?"**
> Careful here — don't throw Alex under the bus. *"I think two things: the two integration decisions sat undecided for four weeks with no forcing function, and Lisa's family leave meant a design went out without the actual policy owner in the room. Neither is a competence problem, it's a sequencing problem — which is why I closed both decisions in week one instead of letting them drift again."*

---

## C. Diana Park (VP Category) — adoption, usability, the Cedar Rapids demo

**"Will this actually be ready for store managers to use by Week 12?"**
> Yes, with a checkpoint you'll see directly: Week 11 is a parallel run where 25 managers see RELEX proposals next to their existing manual process before anything goes live. Go/No-Go includes 20 of 25 managers actually signing off that the workflow is usable — that's your world, and it's measurable, not a vibe check.

**"The regional VPs saw a demo at Cedar Rapids. What happens if real data looks different from what they saw?"**
> That's exactly the risk the parallel run in Week 11 exists to catch before it reaches a real customer or a regional VP again. I'd rather find a bad proposal in front of a store manager in Week 11 than in front of the same VPs in Phase 2 planning.

**"Why is Grocery out of scope for the pilot?"**
> That's signed SOW scope, not my call to relitigate — Fresh Produce, Bakery, Dairy, Frozen only. I'd flag it if I thought it undermined the pilot's validity, but four departments with real seasonality and pack-size variation (Frozen especially) is a reasonable test of the model before scaling to the full catalog.

**"What do I tell my regional VPs about timing for Phase 2?"**
> Nothing concrete yet — Phase 2 scope and timeline is explicitly a Week 12 Go/No-Go decision, not something to promise ahead of the criteria being met. I'd rather you tell them "we have five measurable criteria and we'll know in 7 weeks" than a date that might move.

---

## D. Tom Bradley (pilot coordinator) — field/store-level questions

**"Mike at Cedar Rapids asked if RELEX will replace his 4am direct-to-vendor bread order."**
> No — confirmed out of scope. Only orders that flow through SAP central are touched by RELEX; direct-to-vendor relationships are untouched. Good to close that loop with him explicitly so it doesn't turn into a trust issue later.

**"Does the tablet work offline? Mike says reception is bad in the back of his store."**
> Not addressed yet in what I've inherited — genuinely open. I'd flag this as a question for the mobile app spec, not guess an answer. If asked to commit: *"I'll get a concrete answer from RELEX product on offline caching behavior this week and get back to Tom before Week 9's single-store test, since that's the first real-world usage."*

**"Who's installing the app on the 25 tablets?"**
> Per the kickoff memo, that was Tom's own commitment in Week 4 — worth confirming it's still on track rather than assuming, since it's a dependency for the Week 9 single-store test.

---

## E. Technical deep-dive (either RELEX interviewer, likely to go here)

These map directly to the Technical Triage Document and the UPC deep-dive script — see [Deep_Dive_UPC_Collision.md](Deep_Dive_UPC_Collision.md) for the full version if you need to go deeper live.

**"Walk me through the UPC collision case."**
> UPC `182084873288` sits on three rows — two are a routine SKU reissue (same description, safe to auto-merge), the third is a genuinely different product (Waffles) sharing the barcode by keying error. The inherited rule ("primary = lower SKU number") would've silently merged Waffles' sales history into Burrito Bean's. My fix adds one check before the merge: does the description match. Match → auto-resolve. No match → hard-flag for a human, no auto-merge.

**"What's the actual failure mode if you'd shipped the original rule?"**
> It doesn't fail loudly — that's the dangerous part. No rejected file, no error. RELEX forecasts Burrito Bean off a blended demand curve from two unrelated products, the number looks plausible, and Waffles quietly stops getting reordered. Realistic discovery point is Week 11, in the parallel run — the worst possible week for a silent data bug to surface.

**"Isn't your fix just a heuristic? What if it's wrong?"**
> Yes, honestly — two named failure directions. False negative: a legitimate reissue with a reworded (not just "(legacy)"-suffixed) description gets kicked to manual review unnecessarily — noisy, not dangerous. False positive, the more serious one: two different products could coincidentally share a matching description on a shared UPC and get auto-merged — unlikely at 63 rows, can't rule it out at full catalog scale. The <2% unresolved-conflict Go/No-Go bar is the forcing function to re-test this against a fresh extract, not just trust it once.

**"Why not send every duplicate to manual review — safest option?"**
> Considered and rejected for this timeline. DATA-3041, Northbridge's own dedup ticket, has been open 18 months — that tells you how a fully-manual queue performs against their actual bandwidth. At full catalog scale it also invites reviewer fatigue: rubber-stamping obviously-safe pairs, which quietly reintroduces the exact risk the manual step exists to prevent.

**"Why is Frozen a bigger risk than the other three departments?"**
> 4 of 13 Frozen SKUs (31%) have a blank Pack_Size — zero blanks anywhere else in the sample. SAP requires quantity to be a multiple of case-pack size and rejects the whole file, not just the bad line, if it isn't. One missing Frozen value can take down every store's order in that file for the day. Fix: order emitter hard-blocks (not defaults) any line missing Pack_Size, and I'm confirming with Raj/Marcus whether files can be split per-store to contain the blast radius.

**"Category field — why does free text matter?"**
> 16 raw strings for what's scoped as 4 departments — casing/whitespace collisions, not typos ("Fresh Produce" vs "FRESH PRODUCE " vs "Produce"). If ingestion groups by exact string match, department dashboards silently fragment — and those 4 departments are the entire pilot scope. Fix is a canonicalization map inside the pipeline, unmapped values flagged for review, not silently dropped or guessed.

**"What exactly would you Slack the Data Eng team this week?"**
> Verbatim, it's in the triage doc: pair Monday on the UPC dedup + flag logic; category canonicalization before the Week 8 staging pipeline; order-emitter hard-block on missing Pack_Size before the Week 9 live test. All three hit critical path by Weeks 8–9, none are blockers today — flagging now so they're not a Week 8 surprise.

---

## F. Pushback / "why not X" — devil's advocate on the plan itself

**"Why not just push Go-Live back 4 weeks — Marcus already offered that as an option?"**
> I could recommend that, and I'd say so directly if I thought the plan couldn't hold. I don't think it's necessary yet — the two blocking decisions are closeable this week, and the two real risks (mTLS lead time, SSO) are schedule risks I can manage by filing/escalating now, not scope problems that need more time to solve. I'd rather ask for the date change in Week 8 if the risk materializes than burn political capital asking for it preemptively.

**"Isn't 'At Risk' just covering yourself?"**
> No — it's specific and falsifiable. I named two exact things (mTLS lead time landing in the Week 9–11 test window, SSO already a week behind a hard-to-schedule stakeholder) rather than a general hedge. If neither materializes, this becomes "on track" with no asterisk by Week 8.

**"You're recommending reusing a 4-year-old vendor-PO job for AI-generated orders. Isn't that a hack?"**
> It's a pragmatic interim step, not the end state — I'd frame it as "proven infrastructure with one known limitation I'm flagging," not a hack I'm hiding. The alternative (IDoc) is objectively cleaner but doesn't exist as an option given Marcus's stated capacity. Shipping the right thing in January instead of the workable thing in Week 12 isn't actually the safer choice here.

**"Why trust Raj's Snowflake offer over the originally signed data spec?"**
> Because it was Raj's own email, unprompted, explaining that the API route requires 6–8 week architecture board approval he'd rather avoid — I'd validate schema and freshness against the original 6-feed spec in Week 6 before fully committing, which is already a named milestone, not an assumption I'm skipping.

---

## G. Scope & edge-case gotchas — things not spelled out in the deck, likely to get pulled on

| If asked about... | Say |
|---|---|
| **500-store scale-up** | Out of scope for this case by design — the brief explicitly says don't build the full-fleet Gantt. I'd flag one directional risk if pushed: per-store AD group scoping (vs. a claims-based approach) gets unwieldy at 500 stores, which is part of why I'm pushing for the custom-claim design now while it's cheap to decide. |
| **S/4HANA migration overlap** | Also explicitly out of scope. The one place it matters: it's *why* Marcus has no SAP Basis/ABAP capacity for IDoc work, which is directly why I'm recommending the flat-file route. I wouldn't try to resolve the migration roadmap itself. |
| **Sales feed frequency at scale (Raj's SFTP-won't-scale note)** | Real concern in the kickoff memo, mitigated by the Snowflake recommendation — Snowflake reads bypass the daily-SFTP bottleneck entirely, so it's less urgent than it was at Week 4, but I'd still validate query latency during Week 6 freshness testing. |
| **ROI / business case** | Explicitly out of scope per the brief — assume it's already approved. Don't volunteer a business case; redirect to the technical/operational plan if pushed. |
| **What if Diana and Marcus disagree on priority?** | Name it directly rather than dodge: *"Diana needs adoption confidence, Marcus needs SAP capacity respected — those aren't actually in conflict here, since the plan doesn't ask Marcus for capacity he doesn't have. If a real conflict came up, I'd surface it to Sarah rather than quietly pick a side."* |

---

## H. FDE role / judgment / behavioral

**"Why RELEX, why this role?"**
> Personalize honestly — the case brief's own framing is a good anchor: an FDE sits at the intersection of client politics, product/eng, and end users, and is accountable for the software actually working in production, not in a demo. That intersection — technical judgment plus stakeholder management under real constraints — is the part of the job worth naming specifically, not "I like solving problems."

**"Tell me about a technical judgment call you made under uncertainty."** *(use the UPC case as your worked example if you don't have a stronger real one)*
> The UPC split-rule is a good real example from this exercise: incomplete information (a 63-row sample, not the full catalog), a real decision under time pressure (Monday ship date), and an explicit tradeoff I can defend (fails safe over fails silent, with a named residual risk I'm still watching).

**"How do you decide what to escalate vs. handle yourself?"**
> Escalate anything that needs a decision only the client can make (mTLS acceptance, ORDER_TYPE=REGULAR tradeoff, Snowflake vs SFTP sign-off) or a resource only they control (Marcus's SAP capacity, Lisa's calendar). Handle anything inside RELEX's control myself — the dedup logic, the canonicalization map, the emitter validation — and only escalate those if I'm blocked.

**"What's the one thing in this plan you're least confident about?"**
> Be honest, not falsely modest: the false-positive risk in the UPC fix (two different products coincidentally sharing a matching description) is the one I can't fully rule out from a 63-row sample — that's why it's tied to a hard Go/No-Go gate and a fresh-extract re-check, not something I'm asserting is solved.

**"If you had one more week, what would you do differently?"**
> Get the mTLS request filed even earlier — Week 5 filing already has zero buffer against the Week 9 test, so a week earlier removes the single tightest dependency on the whole plan. Second choice: push for the 90-minute SSO working session with Lisa in week one instead of "this week," since her calendar is the hardest constraint in the whole plan.

---

## I. Meta — about the case itself, if asked

**"How did you approach this in the time you had?"**
> Read the kickoff memo and email thread first for signal, not just content — who said what, what got walked back, what's still open. Verified the "clean" master data myself rather than trusting the label. Built the recovery plan around two decisions that were actually blocking (data in, orders out), not a generic status update, because those were the two things nobody had actually closed.

**"What surprised you most in the materials?"**
> A good honest answer, pick one and be specific: Raj's Snowflake offer buried in an email reply, not the main plan — that one line changes the whole data-in recommendation. Or: how much of the "SSO is basically done" read from Week 3 was actually three separate policy rejections waiting to happen once Lisa was back in the room.
