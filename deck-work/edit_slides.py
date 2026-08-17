from lxml import etree

NS = {
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
}
A = NS['a']; P = NS['p']

def load(path):
    parser = etree.XMLParser(remove_blank_text=False)
    return etree.parse(path, parser)

def save(tree, path):
    tree.write(path, xml_declaration=True, encoding='UTF-8', standalone=True)

def sp_by_idx(root, idx=None, ph_type=None):
    for sp in root.iter(f'{{{P}}}sp'):
        ph = sp.find(f'.//{{{P}}}nvSpPr/{{{P}}}nvPr/{{{P}}}ph')
        if ph is None:
            continue
        if idx is not None and ph.get('idx') != str(idx):
            continue
        if ph_type is not None and ph.get('type') != ph_type:
            continue
        return sp
    return None

def sp_all_with_idx(root, idx):
    out = []
    for sp in root.iter(f'{{{P}}}sp'):
        ph = sp.find(f'.//{{{P}}}nvSpPr/{{{P}}}nvPr/{{{P}}}ph')
        if ph is not None and ph.get('idx') == str(idx):
            out.append(sp)
    return out

def set_single_run_text(sp, new_text):
    txBody = sp.find(f'{{{P}}}txBody')
    t = txBody.find(f'.//{{{A}}}t')
    t.text = new_text

def replace_content_paragraphs(sp, heading=None, bullets=None, bullet_lvl=1, heading_bold=True):
    txBody = sp.find(f'{{{P}}}txBody')
    for p in txBody.findall(f'{{{A}}}p'):
        txBody.remove(p)
    if heading:
        p = etree.SubElement(txBody, f'{{{A}}}p')
        pPr = etree.SubElement(p, f'{{{A}}}pPr')
        pPr.set('marL', '0'); pPr.set('indent', '0')
        etree.SubElement(pPr, f'{{{A}}}buNone')
        r = etree.SubElement(p, f'{{{A}}}r')
        rPr = etree.SubElement(r, f'{{{A}}}rPr')
        rPr.set('lang', 'en-US'); rPr.set('noProof', '0'); rPr.set('dirty', '0')
        if heading_bold:
            rPr.set('b', '1')
        t = etree.SubElement(r, f'{{{A}}}t')
        t.text = heading
    if bullets:
        for text in bullets:
            p = etree.SubElement(txBody, f'{{{A}}}p')
            pPr = etree.SubElement(p, f'{{{A}}}pPr')
            pPr.set('lvl', str(bullet_lvl))
            r = etree.SubElement(p, f'{{{A}}}r')
            rPr = etree.SubElement(r, f'{{{A}}}rPr')
            rPr.set('lang', 'en-US'); rPr.set('noProof', '0'); rPr.set('dirty', '0')
            t = etree.SubElement(r, f'{{{A}}}t')
            t.text = text

# ---------------------------------------------------------------------------
# Slide 29 — Cover
# ---------------------------------------------------------------------------
t29 = load('ppt/slides/slide29.xml')
r29 = t29.getroot()

sp = sp_by_idx(r29, idx=10)
txBody = sp.find(f'{{{P}}}txBody')
runs = txBody.findall(f'.//{{{A}}}r')
runs[0].find(f'{{{A}}}t').text = 'RELEX Store Operations'
runs[1].find(f'{{{A}}}t').text = 'Recovery Plan — Northbridge Grocers'

sp = sp_by_idx(r29, idx=11)
set_single_run_text(sp, 'Week 6 Steering Committee — Data Integration, SSO, and the Path to Go-Live')

sp = sp_by_idx(r29, idx=12)
set_single_run_text(sp, 'Forward Deployed Engineer, RELEX  |  Week 6  |  St. Louis, MO')

save(t29, 'ppt/slides/slide29.xml')
print('slide29 done')

# ---------------------------------------------------------------------------
# Slide 30 — Where We Stand at Week 5 (Basic body)
# ---------------------------------------------------------------------------
t30 = load('ppt/slides/slide30.xml')
r30 = t30.getroot()

sp = sp_by_idx(r30, ph_type='title')
set_single_run_text(sp, 'Where We Stand at Week 5')

sp = sp_by_idx(r30, idx=15)
set_single_run_text(sp, 'On track for Week 12 — two decisions closed this week, need your sign-off today')

sp = sp_by_idx(r30, idx=1)
replace_content_paragraphs(sp, heading=None, bullets=[
    'Foundation is solid: kickoff complete, data feed contents agreed, store master data done, 25 tablets provisioned, product catalog issue root-caused',
    'Two decisions that were never actually finalized — how data lands in RELEX, how orders land back in SAP — are closed this week, pending your approval today',
    'SSO has three open items with Northbridge IT Security; a working session is scheduled this week — not yet a blocker, becomes one if it slips past Week 7',
    'No change to pilot scope: 25 stores, Iowa / Missouri, Fresh Produce, Bakery, Dairy, Frozen',
])

save(t30, 'ppt/slides/slide30.xml')
print('slide30 done')

# ---------------------------------------------------------------------------
# Slide 31 — Data Integration Plan (2 columns)
# ---------------------------------------------------------------------------
t31 = load('ppt/slides/slide31.xml')
r31 = t31.getroot()

sp = sp_by_idx(r31, ph_type='title')
set_single_run_text(sp, 'Data Integration Plan: Recommendation')

sp = sp_by_idx(r31, idx=15)
set_single_run_text(sp, 'Both directions reuse infrastructure Northbridge already runs today')

cols = sp_all_with_idx(r31, 4294967295)
# Column 1 = Data In
replace_content_paragraphs(cols[0], heading='Data In — Snowflake Read Access', bullets=[
    'Read-only access to NB_RETAIL_CORE — covers sales, deliveries, stock movements, and product catalog in one integration',
    'Avoids the 6–8 week new-API approval process; Raj has already offered read-only access',
    'Rejected for pilot: SFTP-per-feed direct from SAP CAR / IS-Retail — six integration points instead of one, no material benefit',
])
# Column 2 = Orders Out
replace_content_paragraphs(cols[1], heading='Orders Out — Existing SFTP Order Channel', bullets=[
    'Flat-file drop into Z_ORD_INBOUND_PROC — 4-year-old production infrastructure already used for vendor PO confirmations',
    'Rejected for pilot: SAP IDoc (WHSORD03) — needs ~6 weeks basis + 2 weeks ABAP dev Marcus’s team doesn’t have until January',
    'Known limitation, flagged not hidden: orders tagged ORDER_TYPE=REGULAR for pilot; a proper order-type value is a fast-follow ask to Raj’s team',
])

save(t31, 'ppt/slides/slide31.xml')
print('slide31 done')

# ---------------------------------------------------------------------------
# Slide 34 — Go / No-Go Criteria (Key features)
# ---------------------------------------------------------------------------
t34 = load('ppt/slides/slide34.xml')
r34 = t34.getroot()

sp = sp_by_idx(r34, ph_type='title')
set_single_run_text(sp, 'Go / No-Go Criteria for Week 12')

sp = sp_by_idx(r34, idx=15)
set_single_run_text(sp, 'Every criterion is measurable — no “system feels ready” language')

sp = sp_by_idx(r34, idx=24)
set_single_run_text(sp, 'Measurable, Pre-Agreed Criteria')

sp = sp_by_idx(r34, idx=23)
set_single_run_text(sp, '≥95%')
sp = sp_by_idx(r34, idx=25)
set_single_run_text(sp, 'SAP order acceptance rate across all 25 pilot stores')

sp = sp_by_idx(r34, idx=26)
set_single_run_text(sp, '<2%')
sp = sp_by_idx(r34, idx=27)
set_single_run_text(sp, 'Unresolved product master conflicts after dedup, on a fresh extract')

sp = sp_by_idx(r34, idx=28)
set_single_run_text(sp, '20 / 25')
sp = sp_by_idx(r34, idx=29)
set_single_run_text(sp, 'Store managers signing off tablet workflow as usable in daily operation')

sp = sp_by_idx(r34, idx=4294967295)
replace_content_paragraphs(sp, heading=None, bullets=[
    'SSO live for all store managers and category managers, with correct per-store access scoping',
    'Zero P1 data-quality incidents during the Week 11 parallel run',
    'Next status checkpoint: Week 8, same format, same audience',
])

save(t34, 'ppt/slides/slide34.xml')
print('slide34 done')
