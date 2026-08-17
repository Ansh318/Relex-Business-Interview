# SAP IS-Retail — Store Order Sample (Northbridge)

The Northbridge buyers today key store orders directly into SAP via transaction MEPO (purchase order). When done in bulk, the orders flow into SAP through two mechanisms, depending on the source:

1. **For vendor-confirmed PO updates**: a flat file dropped on an SFTP folder, picked up every 15 minutes by a custom ABAP job (`Z_ORD_INBOUND_PROC`).
2. **For automated replenishment from their existing forecasting tool**: an inbound IDoc of type `WHSORD03` posted to SAP's RFC endpoint.

Either mechanism, in principle, can be used to land RELEX-generated orders into SAP.

---

## Sample 1 — Flat file format (SFTP `/sap/inbound/store_orders/`)

Filename convention: `STOREORDER_<STORE>_<YYYYMMDD>_<HHMMSS>.dat`

Pipe-delimited. No header row. Each line is one order line. Multiple stores in one file allowed (group by `STORE_ID`). Order itself is identified by the `ORDER_REF` column — same `ORDER_REF` = same PO.

```
H|142|20251124|083015|VENDOR_007|20251126|REGULAR
L|142|20251124|083015|VENDOR_007|100005|24|CS|REGULAR
L|142|20251124|083015|VENDOR_007|100002|12|CS|REGULAR
L|142|20251124|083015|VENDOR_007|100043|6|CS|REGULAR
L|142|20251124|083015|VENDOR_007|100051|18|EA|PROMO
H|142|20251124|083117|VENDOR_011|20251126|REGULAR
L|142|20251124|083117|VENDOR_011|100007|12|CS|REGULAR
L|142|20251124|083117|VENDOR_011|100012|24|CS|REGULAR
T|142|20251124|083117|6
```

Column layout:

| Record Type | Position | Field | Notes |
|-------------|----------|-------|-------|
| H (header) | 1 | RECORD_TYPE | H / L / T |
|  | 2 | STORE_ID | 3 digits |
|  | 3 | ORDER_DATE | YYYYMMDD |
|  | 4 | ORDER_TIME | HHMMSS |
|  | 5 | SUPPLIER_CODE |  |
|  | 6 | DELIVERY_DATE | YYYYMMDD |
|  | 7 | ORDER_TYPE | REGULAR / PROMO / EMERGENCY |
| L (line) | 1 | RECORD_TYPE |  |
|  | 2 | STORE_ID |  |
|  | 3 | ORDER_DATE |  |
|  | 4 | ORDER_TIME |  |
|  | 5 | SUPPLIER_CODE |  |
|  | 6 | SKU | matches SAP MM_MATNR |
|  | 7 | QUANTITY |  |
|  | 8 | UOM | CS = case, EA = each, KG / LB for variable weight |
|  | 9 | LINE_TYPE | REGULAR / PROMO |
| T (trailer) | 1 | RECORD_TYPE |  |
|  | 2 | STORE_ID |  |
|  | 3 | ORDER_DATE |  |
|  | 4 | ORDER_TIME |  |
|  | 5 | LINE_COUNT |  |

Validation rules (enforced by `Z_ORD_INBOUND_PROC`):

- `STORE_ID` must exist in SAP table T001L (storage locations)
- `SUPPLIER_CODE` must exist in LFA1 (vendor master) AND be active for this store
- `SKU` must exist in MARA AND be active in EKKO (purchasing) for this `SUPPLIER_CODE`
- `UOM` must match one of the units configured for the SKU in MARM
- `QUANTITY` must be > 0 AND a multiple of the SKU's PCB (case-pack quantity, table MARC field MEINS)
- If `ORDER_TYPE = EMERGENCY`, delivery date must be < 48h from order date

If any line fails validation: **entire file is rejected**. Rejected files move to `/sap/inbound/store_orders/rejected/` with a `.err` file alongside containing the error log.

### Real-world reject sample (from last week)

`STOREORDER_142_20251119_073402.dat.err`:

```
[2025-11-19 07:34:18] Z_ORD_INBOUND_PROC v3.2.1
[2025-11-19 07:34:18] Processing file STOREORDER_142_20251119_073402.dat
[2025-11-19 07:34:18] 1 header, 8 lines, 1 trailer found
[2025-11-19 07:34:19] Line 2: ERROR E_MARA_NOT_FOUND - SKU 100107 not found in material master
[2025-11-19 07:34:19] Line 5: ERROR E_QTY_NOT_MULTIPLE_PCB - SKU 100024 qty 7, PCB 6, mod 1
[2025-11-19 07:34:19] Line 7: ERROR E_VENDOR_NOT_AUTHORIZED - SKU 100051 supplier VENDOR_018 not in source list for store 142
[2025-11-19 07:34:19] File rejected. 3 errors.
[2025-11-19 07:34:19] Move to /sap/inbound/store_orders/rejected/
```

---

## Sample 2 — Inbound IDoc WHSORD03

This is the SAP-blessed mechanism. RELEX would emit an IDoc payload, posted via tRFC to Northbridge's SAP gateway. SAP processes it via standard `IDOC_INPUT_WHSORD` function module.

Example payload (segments simplified):

```xml
<WHSORD03>
  <EDI_DC40>
    <DOCNUM>0000000123456</DOCNUM>
    <DIRECT>2</DIRECT>
    <IDOCTYP>WHSORD03</IDOCTYP>
    <MESTYP>WHSORD</MESTYP>
    <SNDPRT>LS</SNDPRT>
    <SNDPRN>RELEX_STORE_OPS</SNDPRN>
    <RCVPRT>LS</RCVPRT>
    <RCVPRN>SAPPRD</RCVPRN>
  </EDI_DC40>
  <E1WHSOH>
    <BSART>NB</BSART>
    <LIFNR>VENDOR_007</LIFNR>
    <WERKS>142</WERKS>
    <BEDAT>20251124</BEDAT>
    <EINDT>20251126</EINDT>
    <E1WHSOI>
      <EBELP>00010</EBELP>
      <MATNR>100005</MATNR>
      <MENGE>24</MENGE>
      <MEINS>CS</MEINS>
      <NETPR>14.86</NETPR>
    </E1WHSOI>
    <E1WHSOI>
      <EBELP>00020</EBELP>
      <MATNR>100002</MATNR>
      <MENGE>12</MENGE>
      <MEINS>CS</MEINS>
    </E1WHSOI>
  </E1WHSOH>
</WHSORD03>
```

To make this work, Northbridge SAP team needs to:

1. Define a logical system `RELEX_STORE_OPS` in transaction `BD54`
2. Configure a partner profile in `WE20` for the inbound flow
3. Set up an RFC destination from RELEX to their SAP gateway in `SM59`
4. Open firewall on port 3300 (SAP gateway) from RELEX's outbound IP range
5. Provision a service user (type Communication) in SU01 with role `Z_RELEX_INBOUND`
6. Allocate ABAP developer time to configure the IDoc processing and handle errors

**Effort estimate from Marcus's team**: ~6 weeks of a SAP basis consultant + 2 weeks of an ABAP developer. None currently available due to the S/4 migration program.

---

## Notes from previous FDE

> The flat-file route is uglier but it's a known-good path. Every vendor at Northbridge already uses it to confirm POs back into SAP. The IDoc route is "the right way" but requires SAP capacity Northbridge does not currently have.
>
> If we used the flat-file path, RELEX would emit the pipe-delimited file, drop it via SFTP, and the existing `Z_ORD_INBOUND_PROC` job would pick it up. We'd be reusing infrastructure that's been running for 4 years.
>
> Open question: the existing job assumes the source is a vendor PO confirmation, not a store-originated order. The `ORDER_TYPE` field has values REGULAR / PROMO / EMERGENCY — none of them map cleanly to "automated AI-generated store replenishment". Need to check with Raj whether a new ORDER_TYPE value can be added or whether REGULAR will fly.
