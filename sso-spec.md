# Northbridge Grocers — RELEX SSO Integration Spec (DRAFT)

**Author:** Lisa Okonkwo, Northbridge IT Security & Identity
**Co-author:** Alex Brennan, RELEX FDE
**Status:** DRAFT v0.3 — partially reviewed, NOT signed off
**Last touched:** Week 3

---

## 1. Scope

This document covers identity and access management for the RELEX Store Operations deployment at Northbridge.

Three flows are in scope:
1. **End user SSO** — store managers and category managers sign into the RELEX tablet app and web console
2. **Service-to-service auth** — RELEX backend reads from Northbridge Snowflake / writes to SAP
3. **Admin access** — RELEX implementation team SSH / VPN into Northbridge environment (probably not in scope, see open items)

---

## 2. End user SSO

### 2.1 Identity provider

Northbridge identity is centralized in **Azure AD** (tenant ID: `northbridge.onmicrosoft.com`). All Northbridge employees have an Azure AD account.

### 2.2 Protocol

**Proposed:** OpenID Connect (OIDC) authorization code flow with PKCE for the mobile app, standard authorization code flow for the web console.

**[LISA — comment Week 3]: Why OIDC? Our standard for third-party SaaS at Northbridge is SAML 2.0. We have ~40 SAML integrations live with Azure AD today, and OIDC is approved only for our own internal apps. Need a strong justification or we use SAML.**

### 2.3 User provisioning

- Just-in-time provisioning on first login
- User identifier: Azure AD `oid` (object ID)
- Email and display name read from token claims

### 2.4 Group / role mapping

RELEX defines three application roles:

| RELEX role | Who | What they can do |
|-----------|-----|------------------|
| `store_user` | Store manager, dept manager | Place orders for their own store(s) |
| `category_user` | Category manager | View dashboards across all stores in their categories |
| `admin` | Northbridge IT, RELEX FDE | Configure system |

Proposed group mapping:

| Azure AD group | RELEX role | Scope |
|----------------|-----------|-------|
| `NB_All_Store_Managers` | `store_user` | **ALL stores** |
| `NB_Category_Mgmt` | `category_user` | All categories |
| `NB_RELEX_Admin` (to be created) | `admin` | n/a |

**[LISA — comment Week 3]: This violates our least-privilege policy. A store manager at store 142 should NOT be able to see or place orders for store 197. We need per-store scoping. Probably means we need to create one AD group per store, or pass a `store_id` claim in the token. Recommend the claim approach. Marcus needs to weigh in on whether AD can emit a custom claim from HR data.**

**[ALEX — reply Week 3]: Agree on the scoping issue. The custom claim approach is cleaner. Need to confirm whether Azure AD can pull a `store_id` from Northbridge's HRIS (Workday) and emit it as a token claim. If not we'll need a different approach — maybe RELEX maintains its own user→store mapping table and we sync from HR feed.**

### 2.5 Token claims (proposed)

```json
{
  "iss": "https://login.microsoftonline.com/<tenant>/v2.0",
  "aud": "<relex-client-id>",
  "sub": "<azure-ad-oid>",
  "oid": "<azure-ad-oid>",
  "email": "user@northbridge.com",
  "name": "User Name",
  "groups": ["<group-oid-1>", "<group-oid-2>"],
  "store_id": "142"  // TBD — see open items
}
```

### 2.6 Session

- Access token: 1 hour
- Refresh token: 8 hours (one workday)
- Re-auth required at start of each shift

**[LISA — Week 3]: Refresh token of 8h is fine for desktop. For the shared tablet at the store — multiple users in a day — we probably want shorter. What does the device sharing model look like? One tablet per store, multiple users? Or one tablet per user?**

**[ALEX — reply]: One tablet per department per store. So tablet 142-PROD belongs to "produce department at store 142", and is used by whoever's on shift. Could be the dept manager, could be an associate. We assumed PIN-based user switching on the tablet with full re-auth every 4h. Need to confirm with Tom and Diana.**

---

## 3. Service-to-service auth

### 3.1 RELEX → Snowflake (data reads)

**Proposed:** OAuth client credentials grant. RELEX gets a `client_id` / `client_secret`, exchanges for an access token, uses it to query Snowflake.

**[LISA — Week 3]: We don't issue OAuth client credentials to external vendors. Our standard is certificate-based authentication (mutual TLS). RELEX would need to present a client cert issued by Northbridge's internal CA. We can issue it after a security review. Lead time 4-6 weeks.**

**[ALEX — comment]: Lisa — RELEX SaaS doesn't typically do mTLS to customer environments, we use OAuth. Worth a conversation about whether you can make an exception here, or whether we need a different integration pattern (e.g. read via your data exchange platform rather than direct Snowflake).**

### 3.2 RELEX → SAP (order outbound)

**Not yet designed.** Depends on whether we go via:
- (a) flat-file SFTP into `Z_ORD_INBOUND_PROC` — uses SFTP credentials, simple
- (b) inbound IDoc — uses SAP service user + RFC connection over TCP/3300

See `04_SAP_Order_Sample.md` for context. Auth mechanism follows the integration mechanism choice.

### 3.3 Snowflake → RELEX (data push, alternative model)

Not in current design. If we ever want Northbridge to push data to RELEX rather than RELEX pulling, we'd use a Snowflake → S3 unload + RELEX-side ingestion. Out of scope for v1.

---

## 4. Open items (blocking)

1. **OIDC vs SAML decision** — need to align with Lisa's policy
2. **Per-store scoping mechanism** — group-per-store OR custom claim from HR. Needs Marcus + Lisa decision.
3. **Snowflake auth** — OAuth client credentials vs. mTLS. Needs Lisa decision OR alternative integration design.
4. **Tablet shared-device model** — PIN switching, session length, what re-auth looks like at shift change.
5. **HRIS integration** — if we go custom claim, can Azure AD pull `store_id` from Workday? Probably needs Marcus.

## 5. Open items (non-blocking)

1. Logout flow — single logout on all RELEX clients when AD session ends? Or app-level only?
2. MFA — Northbridge requires MFA on web. Inherit from Azure AD ✓. On tablet shared device — what's the policy?
3. Audit — RELEX should ship login events to Northbridge's SIEM (Splunk). Format TBD.

---

## 6. Status

This is **DRAFT v0.3**, not approved. Lisa was out Week 3 (family leave). She's back Week 5. We need a 90-minute working session with Lisa and Marcus to close items 1-5 above and get this signed off.

The kickoff plan had SSO done by end of Week 4. We are behind. Not catastrophically — but it's a critical path item, and if it slips past Week 7 it starts squeezing the testing window before Go-Live.
