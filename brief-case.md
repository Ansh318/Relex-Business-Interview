# RELEX Store Operations — Forward Deployed Engineer Case

## 1. The role you are stepping into

You are joining RELEX as a Forward Deployed Engineer (FDE) on the Store Operations team. Our software helps grocery retailers automate replenishment and store ordering across thousands of stores. Your job is to make the software actually work in the client's environment — not in a demo, in production.

A FDE at RELEX sits at the intersection of three worlds:

- The client's IT and operations teams, who have constraints, legacy systems and politics you cannot ignore.
- RELEX product, engineering and data science, who build the platform but don't know your client.
- The store managers and category managers who will use the tool every day and judge whether it is worth keeping.

You are accountable for one thing: that the deployment lands on time, with clean data flowing in and clean orders flowing out, and with the client's teams trusting the system enough to use it.

## 2. The case

### 2.1 Client context

You are taking over an active deployment for **Northbridge Grocers** (fictional name).

- ~500 stores across the US Midwest and South
- ~$20B annual revenue
- Conventional supermarket format, strong fresh / grocery / frozen / dairy mix
- ERP backbone: **SAP IS-Retail** (on-premise, S/4HANA migration ongoing but not relevant for this scope)
- POS data centralized in **SAP CAR** (Customer Activity Repository)
- Data platform: **Snowflake**, fed by SAP through a daily batch and a near-real-time stream
- Identity: **Azure AD** with SSO for all internal apps

The signed scope is the **RELEX Store Operations module** on 25 pilot stores, with a 12-week implementation window, followed by a 6-week stabilization period before a Go / No-Go for scale-up to the full 500-store fleet.

You are taking over at the **start of Week 5**. The previous FDE has left the company. The kickoff was 4 weeks ago. Go-live is planned for **Week 12**. You have 7 weeks left.

### 2.2 What the system needs to do

The RELEX Store Operations module needs two things to work:

**Data in.** We ingest from Northbridge:

- Sales (POS transactions, per store, per SKU, per day, with quantity, price, promo flag)
- Deliveries (what physically arrived in the store, per store, per SKU, per day)
- Stock movements (receipts, transfers, adjustments, waste / shrink, returns)
- Product catalog (master data: SKU, UPC, description, category hierarchy, pack size, supplier, ordering parameters)
- Store master (store ID, format, address, opening hours, departments)
- Price and promotion calendar

**Orders out.** Once the AI generates a replenishment proposal, the order needs to flow back into the client's existing systems — meaning, into SAP IS-Retail in a format SAP can process as if it had been keyed in by a store associate. The proposal needs to reach SAP, get validated, and be sent to the warehouse without anyone re-keying anything.

How exactly to ingest the data, and how exactly to send the order back — that's part of what you have to figure out.

### 2.3 What you have inherited

You have access to the following materials (provided separately):

- **`01_Kickoff_Memo.md`** — the kickoff summary your predecessor wrote at week 0. Read it critically.
- **`02_Email_Thread.md`** — a thread of recent emails between the previous FDE, Northbridge IT, Category, and the COO sponsor. There are signals in it.
- **`03_Sample_Master_Data.csv`** — an extract of the product catalog Northbridge IT sent over. They say it's "clean". Verify.
- **`04_SAP_Order_Sample.txt`** — a sample of how store orders currently look in SAP IS-Retail. This is the format your output has to match (or be transformed into).
- **`05_SSO_Spec.md`** — the SSO / identity spec that Northbridge IT wrote up. Partial, somewhat inconsistent.
- **`06_Client_Architecture_Diagram.svg`** — Northbridge's current data architecture, as understood by the previous FDE. Use it. Improve it if needed.

### 2.4 Your mission and deliverables

You have **5 business days** to prepare two deliverables.

#### Deliverable 1 — Recovery Plan presentation (client-facing)

A **6-slide PowerPoint deck** that you will present to the Northbridge steering committee at the start of Week 6. Audience:

- **Sarah Chen** — COO, executive sponsor of the project, your economic buyer
- **Marcus Reilly** — VP IT Infrastructure, owns SAP and Snowflake
- **Diana Park** — VP Category Management, owns the user adoption side
- **Tom Bradley** — Pilot coordinator, day-to-day Northbridge contact

The slides must cover:

- **Where we stand at Week 5** — your honest read on what's done, what's at risk, what's blocked. Don't sugarcoat. Don't catastrophize either.
- **The data integration plan** — your concrete proposal on how Northbridge data lands in RELEX and how RELEX orders land back in SAP. You may propose more than one option but you must recommend one.
- **The 7-week plan to Go-Live** — week by week, with named owners and dependencies.
- **What you need from Northbridge** — decisions, accesses, people, by when. Be specific.
- **The Go / No-Go criteria** — what does success look like at Go-Live, measurable and pre-agreed.

A template deck is provided (`RELEX_Store_Operations_Template.pptx`). Use it. The slides above are guidance, not a strict mandate — if you want to add or remove a slide, justify it.

#### Deliverable 2 — Technical Triage Document (internal)

A **1-page document** for RELEX-internal use only. Three things in it:

- **Three specific technical problems** you have identified in the materials provided, with your diagnosis of each and how you would solve them. Be precise. "The data is messy" is not a problem statement. "The UPC column in master data has 14% nulls and 3% duplicates with conflicting descriptions, which will break our SKU-level forecasting unless we resolve it" is.
- **What you would ask of the RELEX Data Engineering team this week**, phrased as you would actually send it on Slack — with the context they need to prioritize it.
- **Your honest call on the project's status**: On track, At risk, or Pivot needed. With your reasoning. If you say "at risk", say what specifically risks blowing up Go-Live.

### 2.5 What we are evaluating

We are not looking for a polished consulting deck. We are looking for a FDE.

Specifically:

- **Can you read a messy situation fast?** A real implementation never comes with clean specs. You should be able to find the signals in the noise.
- **Are you concrete?** "We will improve data quality" is not a plan. "I'll write a Python script Monday morning to dedupe the UPC column, push it to staging, and ask Marcus for a fresh extract by Wednesday" is.
- **Do you make calls under uncertainty?** You don't have full information. Neither does anyone in real life. Take a position, own your assumptions, and say what you'd do to validate them.
- **Do you handle the client well?** The COO is not your friend, the IT VP is overworked, the Category VP wants this to succeed but doesn't speak tech. Each one needs a different message.
- **Do you know when to push back?** If something in the inherited setup looks wrong, say it. Diplomatically. But say it.

### 2.6 Logistics

- Time: 5 business days from receipt of this brief
- Submission: send both deliverables (PPTX + PDF or MD for the triage doc) to your hiring contact
- Live discussion: 60-minute session, where you'll present the deck (15 min) and discuss freely with two RELEX team members (45 min)
- Language: English

### 2.7 Not in scope

Don't waste cycles on these — they are not what we are testing:

- ROI quantification or business case sizing (assume the business case is already approved)
- Detailed financial modeling
- Slide design polish (the template handles that)
- A full deployment Gantt for the 500-store rollout (just the 25-store pilot)
- Resolving the SAP S/4HANA migration roadmap

Focus on the 7 weeks ahead of you.

Good luck.
