# Northbridge Grocers — Kickoff Memo
**Author:** Alex Brennan (FDE, left RELEX in Week 4)
**Date:** Week 0 kickoff recap
**Status:** Final

## Project at a glance

Northbridge Grocers is rolling out RELEX Store Operations to 25 pilot stores in the Midwest cluster (Iowa + Missouri). Pilot lasts 12 weeks. Then 6 weeks of stabilization, then Go / No-Go for the full 500-store fleet.

Sponsor: Sarah Chen, COO. Strong sponsor, has done a Walmart stint, knows replenishment is a real lever. Wants this to work.

Key deliverable from RELEX side: a working tablet experience for 25 store managers by end of Week 12, with order proposals generated daily and orders flowing back into SAP.

## Stakeholders

| Name | Role | Notes |
|------|------|-------|
| Sarah Chen | COO | Sponsor. Pragmatic. Wants weekly status, 1 page max. Doesn't read tech detail. |
| Marcus Reilly | VP IT Infra | Owns SAP, Snowflake, Azure AD. Overstretched. Just took on a S/4 migration program in parallel. Will be hard to get cycles from. |
| Diana Park | VP Category Mgmt | Champion on the business side. Pushed for RELEX. Expects to look good in front of the CEO. |
| Tom Bradley | Pilot Coordinator | Daily contact. Ex-store manager, knows the field. Good at unblocking operational stuff. |
| Raj Patel | Data Engineer (Northbridge) | Reports to Marcus. The one actually doing the data work. Solid. |
| Lisa Okonkwo | Identity / Security (Northbridge) | Azure AD owner. We need her for SSO. Hard to schedule. |

## Scope (from signed SOW)

- 25 pilot stores in IA / MO
- Departments in scope: **Fresh produce, Bakery, Dairy, Frozen**. Grocery is OUT for the pilot.
- Data flows: sales, deliveries, stock movements, product catalog, store master, prices
- Daily order generation, sent back to SAP IS-Retail
- SSO via Northbridge Azure AD
- Mobile app on Zebra TC52 handhelds (already deployed in stores, Android 11)

## What we've done in Week 0 to 4

1. **Kickoff workshop** — Week 1, on-site at Northbridge HQ in St. Louis. 2 days. Went well.
2. **Data spec signed off** — Week 2. We agreed on 6 data feeds (see below). Raj is owner.
3. **SSO design discussion** — Week 3. Lisa was in 30 min then dropped. We agreed in principle on OIDC via Azure AD. Open items remaining.
4. **Sample data delivered** — Week 4. Raj sent first extracts of product master + sales. Quality is OK-ish, see notes below.
5. **Tablet provisioning** — Week 4. Tom got 25 Zebra TC52s flashed and ready. Pending app install + SSO config.

## Data feeds agreed

| Feed | Source | Frequency | Mechanism | Status |
|------|--------|-----------|-----------|--------|
| Sales | SAP CAR | Daily, T+1 | TBD (Raj wants SFTP, we'd prefer API) | NOT STARTED |
| Deliveries | SAP IS-Retail | Daily | SFTP | Sample delivered |
| Stock movements | SAP IS-Retail | Daily | SFTP | NOT STARTED |
| Product catalog | SAP MDG | Weekly + delta | SFTP | Sample delivered, see issues |
| Store master | SAP IS-Retail | Monthly | SFTP | Done |
| Price / promo | SAP CAR | Daily | SFTP | NOT STARTED |

**Order outbound** (RELEX → SAP): we agreed it would go back via IDoc into SAP IS-Retail. Format: WHSORD03. Raj needs to set up the inbound IDoc channel on their side. NOT STARTED.

## Open items

- **SSO**: still need to clarify token claims with Lisa. Group mapping for store-level access control unclear.
- **Product catalog quality**: sample had ~10% rows with missing or duplicate UPCs. Raj says it's a known issue, they're "working on it".
- **IDoc inbound config** on Northbridge side: not scoped in detail yet, Marcus said "should be fine, we do this all the time"
- **Sales feed mechanism**: Raj wants daily SFTP, but for 500 stores with hourly sales this might not scale. To revisit.
- **Frozen department**: pack-size handling for case-pack quantities is different from other departments. Need to validate forecasting model handles it.
- **Tablet rollout**: 25 devices ready, but no plan yet for who installs the app in stores. Tom said he'd handle.

## Risks (my call as of Week 4)

- **Marcus's bandwidth**. He owns SAP. He's running a S/4 migration in parallel. Every SAP-side ask will take longer than estimated.
- **Lisa's availability** on SSO. Hard to get.
- **Product master quality**. We can build around it short-term but it will bite us at scale.

Overall I think this is on track. Sarah is happy, Diana is happy, the teams are engaged. The data work is behind where I'd like it to be but we have buffer.

## Handover notes for whoever takes over

Sorry to leave at this point. If I had another month I'd:

1. Push harder on the sales feed — pick a mechanism, build the ingestion, get the first end-to-end flow working even if it's ugly.
2. Get Lisa in a room for 90 min and close the SSO design.
3. Run the product master extract through a quality check and bring the issues to Raj with a clear ask.
4. Start designing the order outbound IDoc — this is the single piece nobody is owning right now and it WILL be on the critical path.

Good luck.

— Alex
