# Northbridge Grocers — Recent Email Thread
*(Reverse chronological — most recent at top. Excerpts only, irrelevant signatures removed.)*

---

**From:** Sarah Chen <s.chen@northbridge.com>
**To:** Alex Brennan <a.brennan@relex.com>
**Cc:** Marcus Reilly, Diana Park, Tom Bradley
**Date:** End of Week 4, Friday 5:47 PM
**Subject:** RE: Quick check-in

Alex,

Heard from Diana you're moving on. Sorry to see you go, you were doing a good job.

I'll need to meet whoever takes this over within the first week. Northbridge has put real budget and real political capital behind this — I went to the board on it in March. I need to know that Go-Live in Week 12 is still real.

Tom mentioned the data work is "ongoing". I'd like a concrete view of what "ongoing" means.

Let's plan a steering committee Monday Week 6, 10am CT. Marcus, Diana, Tom and me. Bring something honest.

Sarah

---

**From:** Marcus Reilly <m.reilly@northbridge.com>
**To:** Alex Brennan
**Date:** End of Week 4, Thursday 9:14 PM
**Subject:** RE: SAP inbound IDoc — need your config

Alex,

Got your note. I'll be candid — I don't have a developer available for the IDoc work until mid-January at the earliest. The S/4 program is eating all my SAP capacity. I flagged this risk to Sarah back in February but the project was greenlit anyway.

A few options I can think of:
1. You build something on your side that wraps the IDoc as a flat file and drops it on the existing store ordering SFTP that our buyers use. Our SAP picks that up anyway, every 15 min. It's how vendors send PO confirmations today.
2. We push back Go-Live by 4 weeks
3. RELEX brings a SAP IDoc specialist who can work alongside Raj for 2 weeks

I'm not the decision maker on this, Sarah is. But I'd like your read before we go to her.

Also — Lisa is back from leave Monday, she's blocking time with you for SSO. She's not happy that we agreed OIDC without looping her in fully. Heads up.

— Marcus

---

**From:** Diana Park <d.park@northbridge.com>
**To:** Alex Brennan
**Date:** Week 4, Wednesday 3:22 PM
**Subject:** Store demo at Cedar Rapids

Alex,

I'm going to Cedar Rapids next Tuesday with two of our regional VPs to show them what RELEX will look like. They've heard a lot about it, want to see the tablet in action.

Can you set up a working demo on a TC52 for me? Even a fake data demo is fine, I just need them to see and touch it. I'll handle the narrative.

This matters. The regional VPs are the ones who'll decide if their stores get rolled out in phase 2. I need them on side now, before any data hiccups.

Thanks
Diana

---

**From:** Raj Patel <r.patel@northbridge.com>
**To:** Alex Brennan
**Date:** Week 4, Wednesday 10:48 AM
**Subject:** RE: product master extract — questions

Alex,

Yes the duplicates are a known issue. We had a vendor consolidation in 2022 and two parallel SKU numbering systems got merged in a hurry. We have an internal ticket open to clean it (DATA-3041) but it's been open 18 months.

For your purposes — the "primary" UPC is the one with the lower SKU number when there are duplicates. That's the convention buyers use. Not documented anywhere but everyone here knows it.

Re: sales feed mechanism — SFTP is what we do for everything else. I'd really rather not stand up a new API integration just for RELEX. We have a strict change management process for new APIs out of CAR, it requires architecture board approval, 6-8 weeks.

But — there's a Snowflake instance that mirrors CAR. If you can read from Snowflake instead, we can grant you a read-only role and bypass the whole API approval thing. I should have mentioned that earlier. Sorry.

— Raj

---

**From:** Tom Bradley <t.bradley@northbridge.com>
**To:** Alex Brennan
**Date:** Week 3, Friday 6:01 PM
**Subject:** Tablet question from Cedar Rapids store manager

Alex,

Quick one — Mike at Cedar Rapids #142 asked me today if RELEX will replace the order he places at 4am for the bread vendor. He places that one directly to the bakery supplier, not through our central system. He's worried RELEX will mess with it.

Short answer is no right? Direct-to-vendor orders aren't in scope, only orders going through SAP central are. Can you confirm so I can tell him.

Also — he wants to know if the tablet works offline. The back of his store has terrible cell reception.

Tom

---

**From:** Lisa Okonkwo <l.okonkwo@northbridge.com>
**To:** Marcus Reilly
**Cc:** Alex Brennan
**Date:** Week 3, Tuesday 11:23 AM
**Subject:** RELEX SSO — concerns

Marcus,

Got the design Alex sent. A few things:

1. OIDC is fine in principle but our standard for third party SaaS is SAML 2.0. Why are we doing OIDC here?
2. The proposed group mapping has every store manager getting access to every store's data. That violates our least-privilege policy. Each store manager should only see their own store.
3. Service account for system-to-system: I see RELEX wants client credentials grant. We don't issue those to external vendors. We issue certificate-based auth.

I'm out the rest of this week (family). Back Monday Week 5. Let's redo this properly when I'm back.

Lisa

---

**From:** Alex Brennan <a.brennan@relex.com>
**To:** Sarah Chen, Marcus Reilly, Diana Park
**Cc:** Tom Bradley
**Date:** Week 2, Monday 8:15 AM
**Subject:** Week 2 update — all green

Hi all,

Quick update. Things are moving well:
- Data spec signed off Friday
- Tablet provisioning kicked off, devices arrive Wednesday
- SSO design draft circulated, low complexity, we should be done by end of week 3
- Workshop next week with category managers on order acceptance UX

No blockers. I'll send a more detailed status Friday.

Alex
