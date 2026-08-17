# Technical Triage: Northbridge Grocers Pilot
**RELEX internal only, Week 5/6 handover**

## 1. Three specific technical problems

### Problem 1: Product master identity is broken, not just "dirty"
12.7% of SKUs (8/63) have a null UPC, and 17.5% (11/63) share a UPC with another SKU across 5 duplicate groups. Every single one of those rows, legacy and current, is still `Active_Flag = Y`; nothing has ever been deactivated. If we ingest as-is, RELEX will double-count stock and sales for the same physical product under two SKU numbers.

One group is worse than a simple legacy reissue: UPC `182084873288` is shared by three SKUs, and two of them are genuinely different products, "Burrito Bean 8pk" and "Waffles Buttermilk 10ct," not a renamed duplicate. The stated resolution rule ("primary = lower SKU number when there are duplicates") assumes duplicates are the same item under two numbers. This case breaks that assumption; auto-resolving it would silently merge two different products' sales history.

**Fix:** Monday: dedup script that (a) flags null UPCs for buyer review, (b) auto-resolves matching-description "(legacy)" pairs to the lower SKU and marks the superseded one inactive, (c) hard-flags same-UPC-different-description conflicts (the Burrito/Waffles case) for manual resolution, no auto-merge. Push to staging, ask Raj for a fresh extract to re-check counts against the Go/No-Go bar of <2% unresolved conflicts.

### Problem 2: Category isn't a controlled vocabulary, it's free text
16 distinct raw `Category` strings across 63 SKUs, for what the SOW scopes to exactly 4 departments. Casing and whitespace collide freely: "Fresh Produce," "Fresh produce " (trailing space), "FRESH PRODUCE," "fresh produce," and "Produce" are all live values for one department. Same pattern in Bakery (4 variants), Dairy (3), Frozen (4).

If ingestion groups by exact string match, which is the default behavior for most category-based forecasting, department-level views and store manager dashboards will silently fragment. That's not a cosmetic issue; those 4 departments are the entire pilot scope.

**Fix:** A canonicalization map (trim + case-fold + synonym table) inside the ingestion pipeline, before anything downstream reads `Category`, not a reporting-layer patch. Unmapped values get flagged into a 5th bucket for manual review rather than silently dropped or auto-guessed.

### Problem 3: Frozen pack-size gaps will get orders rejected at SAP, not just RELEX
4 of 13 Frozen SKUs (31%) have a blank `Pack_Size`. Zero blanks anywhere else in the sample; this is concentrated entirely in Frozen. It's the exact risk the prior FDE flagged in the Week 4 handover notes ("pack-size handling for case-pack quantities is different for Frozen, need to validate the model handles it"), now confirmed against real data.

Per the SAP order sample, `QUANTITY` must be greater than 0 and a multiple of the SKU's case-pack size, and if any line fails validation the entire file is rejected, not just that line. The file format allows multiple stores batched into one file. So with `Pack_Size` null, RELEX can't compute a valid case-pack multiple, and a missing Pack_Size on one Frozen SKU at one store can knock out that day's order file for every store in it.

**Fix:** Get Pack_Size for these 4 SKUs from Raj this week, ahead of the Week 9 first live order test. Add a pre-send validation step in the order emitter that **blocks** (not defaults) any line missing Pack_Size, and confirm with Raj/Marcus whether files can be split per-store so one bad Frozen line doesn't take down unrelated stores' orders.

## 2. Ask to RELEX Data Engineering, this week

> Hey team, triaging the Northbridge product master before we build the ingestion pipeline, need help on 3 things this week:
>
> 1. **UPC dedup rule.** I've got 5 duplicate UPC groups in the sample (11/63 rows), plus 8 nulls. Most are legacy SKU reissues (same description, safe to auto-resolve to lowest SKU), but one is two *different* products sharing a UPC, that one needs a manual-review flag, not an auto-merge. Can someone pair with me Monday to get the dedup + flagging logic into the ingestion staging job? I'll have the resolution rules written up by then.
> 2. **Category canonicalization.** Raw `Category` has 16 variants for 4 departments (casing/whitespace mess, not typos). Need a normalization step ahead of anything that groups by department; this blocks accurate store-manager dashboards. Priority: before Week 8 staging pipeline goes live.
> 3. **Order-emitter validation.** For Week 8's per-store order file emitter: can we build it to hard-block (not default) any line missing `Pack_Size`, since SAP rejects the whole file on one bad line? Want this in place before the Week 9 live test so we're not debugging a full-file rejection against a real store.
>
> None of these are blockers today, but all three hit the critical path by Weeks 8 to 9. Flagging now so it's not a Week 8 surprise.

## 3. Honest status call: **At Risk**

At Risk with two specific named things that could blow up Week 12:

1. **mTLS cert lead time has no buffer.** Filed Week 5, a 4 to 6 week lead time from Lisa's security team lands anywhere from Week 9 to Week 11, the same window as the first live order test and the parallel run. If it lands late, it doesn't just delay a task, it collides with testing itself.
2. **SSO is already behind the original plan** (it was due end of Week 4) and depends on Lisa, who's been hard to schedule all along. A slip past Week 7 starts squeezing the testing window before Go-Live.

Everything else, the two integration decisions, the data-quality issues above, is real work but has a known, executable fix. The two items above depend on a third party's calendar and a fixed lead time we can't compress. That's the actual risk to Week 12, not the data mess.
