import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Concrete Mix Design | IS 10262",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
html, body, [class*="css"] { font-family: Arial, sans-serif; }

.stApp { background-color: #f5f7fa; }

section[data-testid="stSidebar"] {
    background-color: #1a2f4a;
}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stNumberInput label,
section[data-testid="stSidebar"] .stCheckbox label,
section[data-testid="stSidebar"] .stSlider label {
    color: #f0c060 !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
}

section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] div,
section[data-testid="stSidebar"] div[data-baseweb="select"] span,
section[data-testid="stSidebar"] div[data-baseweb="select"] input,
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] * {
    color: #ffffff !important;
    background-color: #243d5c !important;
}

section[data-testid="stSidebar"] div[data-baseweb="select"] svg {
    fill: #f0c060 !important;
}

section[data-testid="stSidebar"] input[type="number"],
section[data-testid="stSidebar"] input {
    color: #ffffff !important;
    background-color: #243d5c !important;
    border: 1px solid #4a7aa0 !important;
    border-radius: 5px !important;
}

section[data-testid="stSidebar"] .stCheckbox span {
    color: #ffffff !important;
}

section[data-testid="stSidebar"] .stSlider div,
section[data-testid="stSidebar"] .stSlider span {
    color: #f0c060 !important;
}

ul[data-testid="stSelectboxVirtualDropdown"] li,
div[data-baseweb="popover"] li,
div[data-baseweb="menu"] li,
div[role="listbox"] div,
div[role="option"] {
    color: #1a2f4a !important;
    background-color: #ffffff !important;
    font-size: 0.9rem !important;
}
div[role="option"]:hover {
    background-color: #e8f0fe !important;
    color: #1a2f4a !important;
}

section[data-testid="stSidebar"] hr {
    border-color: #4a7aa0;
}

.stButton > button {
    background-color: #e8a020 !important;
    color: #0a1628 !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 6px !important;
    width: 100% !important;
    padding: 0.6rem !important;
}
.stButton > button:hover {
    background-color: #c07010 !important;
    color: #ffffff !important;
}

.section-header {
    font-size: 0.75rem;
    color: #0a1628;
    background-color: #e8a020;
    padding: 5px 12px;
    border-radius: 4px;
    letter-spacing: 0.1em;
    margin: 14px 0 8px 0;
    display: inline-block;
    font-weight: 700;
}

.main-title {
    font-size: 2rem; color: #1a2f4a;
    font-weight: 700; margin-bottom: 0;
}
.main-sub {
    font-size: 0.9rem; color: #4a7aa0;
    text-transform: uppercase; margin-bottom: 1.5rem; font-weight: 500;
}

div[data-testid="metric-container"] {
    background-color: #1a2f4a;
    border: 2px solid #e8a020;
    border-radius: 10px;
    padding: 16px 20px;
}
div[data-testid="metric-container"] label {
    color: #f0c060 !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
}

.ratio-card {
    background-color: #1a2f4a;
    border: 2px solid #4a7aa0;
    border-top: 4px solid #e8a020;
    border-radius: 8px;
    padding: 16px 20px;
    text-align: center;
}
.ratio-label {
    font-size: 0.72rem; color: #f0c060;
    letter-spacing: 0.1em; text-transform: uppercase; font-weight: 700;
}
.ratio-value {
    font-size: 1.4rem; color: #ffffff;
    margin-top: 8px; font-weight: 700;
}

.result-box {
    background-color: #1a2f4a;
    border: 1px solid #4a7aa0;
    border-left: 5px solid #e8a020;
    border-radius: 8px;
    padding: 20px 24px;
    font-family: monospace;
    font-size: 0.9rem;
    color: #e0eaf5;
    line-height: 2.0;
    white-space: pre-wrap;
}

h4 {
    color: #1a2f4a !important;
    font-weight: 700 !important;
    border-bottom: 2px solid #e8a020;
    padding-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)

STD_DEVIATION = {"M10":3.5,"M15":4.0,"M20":4.0,"M25":4.0,"M30":5.0,"M35":5.0,"M40":5.0,"M45":5.0,"M50":5.0}
MAX_WC = {"M10":0.60,"M15":0.60,"M20":0.55,"M25":0.50,"M30":0.50,"M35":0.45,"M40":0.45,"M45":0.40,"M50":0.40}
WATER_CONTENT = {
    "Very Low  (0-25 mm)":172,"Low       (25-50 mm)":180,
    "Medium    (50-100 mm)":186,"High      (100-150 mm)":195,"Very High (150 mm+)":202
}
CA_FRACTION = {
    "Zone I":  {0.40:0.71,0.45:0.69,0.50:0.66,0.55:0.64,0.60:0.62},
    "Zone II": {0.40:0.69,0.45:0.67,0.50:0.64,0.55:0.62,0.60:0.60},
    "Zone III":{0.40:0.67,0.45:0.65,0.50:0.62,0.55:0.60,0.60:0.58},
    "Zone IV": {0.40:0.65,0.45:0.63,0.50:0.60,0.55:0.58,0.60:0.56},
}
MIN_CEMENT = {"Mild":300,"Moderate":300,"Severe":320,"Very Severe":340,"Extreme":360}

def interpolate_ca(zone, wc):
    tbl = CA_FRACTION[zone]
    keys = sorted(tbl.keys())
    if wc <= keys[0]: return tbl[keys[0]]
    if wc >= keys[-1]: return tbl[keys[-1]]
    for i in range(len(keys)-1):
        k1, k2 = keys[i], keys[i+1]
        if k1 <= wc <= k2:
            return tbl[k1] + (wc-k1)/(k2-k1)*(tbl[k2]-tbl[k1])
    return tbl[keys[-1]]

def calculate_mix(grade,exposure,sg_c,sg_fa,sg_ca,abs_fa,abs_ca,zone,slump,msa_str,use_adm,water_red,use_fly,fa_pct,sg_fly):
    fck = int(grade[1:])
    steps = []
    S = STD_DEVIATION[grade]
    fck_t = fck + 1.65 * S
    steps.append(("STEP 1 - Target Mean Compressive Strength",
        f"fck = {fck} MPa  |  S = {S} MPa\nf'ck = {fck} + {1.65*S:.2f} = {fck_t:.2f} MPa"))
    wc_calc = round(12.25 / (1.115 ** fck_t), 3)
    wc_max = MAX_WC[grade]
    wc = min(wc_calc, wc_max)
    steps.append(("STEP 2 - Water-Cement Ratio",
        f"Computed W/C = {wc_calc:.3f}\nMax W/C (IS 456) = {wc_max}\nAdopted W/C = {wc:.3f}"))
    water_base = WATER_CONTENT[slump]
    msa_corr = {"10mm":3,"16mm":1.5,"20mm":0,"25mm":-1.5,"40mm":-6}
    water_msa = water_base * (1 + msa_corr.get(msa_str,0)/100)
    water_final = water_msa * (1 - water_red/100) if use_adm else water_msa
    steps.append(("STEP 3 - Water Content",
        f"Base = {water_base} lt/m3\nAfter MSA correction = {water_msa:.1f} lt/m3\nAdopted = {water_final:.1f} lt/m3"))
    cement_raw = water_final / wc
    flyash_mass = cement_raw * (fa_pct/100) if use_fly else 0
    cement_final = cement_raw - flyash_mass
    if not use_fly: sg_fly = 2.2
    min_c = MIN_CEMENT[exposure]
    adopted_cement = max(cement_final, min_c)
    warn = f"Adopted = {adopted_cement:.1f} kg/m3" + (" (min cement applied)" if cement_final < min_c else " (OK)")
    steps.append(("STEP 4 - Cement Content",
        f"Cement = {water_final:.1f}/{wc} = {cement_raw:.1f} kg/m3\n"
        + (f"Fly Ash = {flyash_mass:.1f} kg/m3\n" if use_fly else "") + warn))
    vol_water = water_final/1000
    vol_cement = adopted_cement/(sg_c*1000)
    vol_flyash = flyash_mass/(sg_fly*1000) if use_fly else 0
    air = 0.02
    vol_agg = 1 - vol_water - vol_cement - vol_flyash - air
    ca_frac = interpolate_ca(zone, wc)
    if msa_str == "10mm": ca_frac -= 0.10
    elif msa_str == "40mm": ca_frac += 0.05
    ca_frac = max(0.30, min(ca_frac, 0.90))
    vol_ca = vol_agg * ca_frac
    vol_fa_agg = vol_agg * (1 - ca_frac)
    mass_ca = vol_ca * sg_ca * 1000
    mass_fa = vol_fa_agg * sg_fa * 1000
    steps.append(("STEP 5 - Aggregate Volumes",
        f"Total Agg. Vol = {vol_agg:.4f} m3\nCA Fraction = {ca_frac:.3f}\n"
        f"Coarse Agg = {mass_ca:.1f} kg/m3\nFine Agg = {mass_fa:.1f} kg/m3"))
    r_fa = round(mass_fa/adopted_cement, 2)
    r_ca = round(mass_ca/adopted_cement, 2)
    r_w  = round(water_final/adopted_cement, 2)
    steps.append(("STEP 6 - Final Mix Proportions",
        f"Cement : Fine Agg : Coarse Agg : Water\n1 : {r_fa} : {r_ca} : {r_w}\nDesign complete - IS 10262 : 2019"))
    return {"fck_t":fck_t,"wc":wc,"water":water_final,"cement":adopted_cement,
            "flyash":flyash_mass,"fa":mass_fa,"ca":mass_ca,
            "vol_cement":vol_cement,"vol_flyash":vol_flyash,
            "vol_fa":vol_fa_agg,"vol_ca":vol_ca,"vol_water":vol_water,
            "r_fa":r_fa,"r_ca":r_ca,"r_w":r_w,"use_fly":use_fly,"steps":steps}

st.markdown('<div class="main-title">CONCRETE MIX DESIGN</div>', unsafe_allow_html=True)
st.markdown('<div class="main-sub">IS 10262 : 2019 | IS 456 : 2000 | Absolute Volume Method</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Design Inputs")
    st.markdown('<div class="section-header">1. GRADE & EXPOSURE</div>', unsafe_allow_html=True)
    grade    = st.selectbox("Grade of Concrete", ["M10","M15","M20","M25","M30","M35","M40","M45","M50"], index=3)
    exposure = st.selectbox("Exposure Condition", ["Mild","Moderate","Severe","Very Severe","Extreme"])
    st.markdown('<div class="section-header">2. CEMENT</div>', unsafe_allow_html=True)
    cement_type = st.selectbox("Type of Cement", ["OPC 33","OPC 43","OPC 53","PPC","PSC","SRC"], index=2)
    sg_c = st.number_input("Sp. Gravity of Cement", value=3.15, step=0.01, format="%.2f")
    st.markdown('<div class="section-header">3. AGGREGATE</div>', unsafe_allow_html=True)
    msa_str = st.selectbox("Max Size of Aggregate", ["10mm","16mm","20mm","25mm","40mm"], index=2)
    zone    = st.selectbox("Fine Aggregate Zone (IS 383)", ["Zone I","Zone II","Zone III","Zone IV"], index=1)
    sg_fa   = st.number_input("Sp. Gravity - Fine Agg.", value=2.65, step=0.01, format="%.2f")
    sg_ca   = st.number_input("Sp. Gravity - Coarse Agg.", value=2.70, step=0.01, format="%.2f")
    abs_fa  = st.number_input("Water Absorption - FA (%)", value=1.0, step=0.1, format="%.1f")
    abs_ca  = st.number_input("Water Absorption - CA (%)", value=0.5, step=0.1, format="%.1f")
    st.markdown('<div class="section-header">4. WORKABILITY</div>', unsafe_allow_html=True)
    slump = st.selectbox("Required Workability", list(WATER_CONTENT.keys()), index=2)
    st.markdown('<div class="section-header">5. ADMIXTURES</div>', unsafe_allow_html=True)
    use_adm = st.checkbox("Use Plasticizer / Superplasticizer")
    water_red = st.slider("Water Reduction (%)", 5, 35, 20) if use_adm else 0.0
    use_fly = st.checkbox("Use Fly Ash (IS 1344)")
    fa_pct = 0.0
    sg_fly = 2.20
    if use_fly:
        fa_pct = st.slider("Fly Ash Replacement (%)", 5, 35, 20)
        sg_fly = st.number_input("Sp. Gravity - Fly Ash", value=2.20, step=0.01, format="%.2f")
    st.markdown("---")
    calc = st.button("CALCULATE MIX DESIGN")

if calc:
    res = calculate_mix(grade,exposure,sg_c,sg_fa,sg_ca,
                        abs_fa/100,abs_ca/100,zone,slump,msa_str,
                        use_adm,water_red,use_fly,fa_pct,sg_fly)
    st.markdown("#### Key Design Parameters")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("W/C Ratio",      f"{res['wc']:.3f}")
    c2.metric("Water Content",  f"{res['water']:.1f} lt/m3")
    c3.metric("Cement Content", f"{res['cement']:.1f} kg/m3")
    c4.metric("Target f'ck",    f"{res['fck_t']:.2f} MPa")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Mix Proportion - Cement : FA : CA : Water")
    r1,r2,r3,r4 = st.columns(4)
    for col,label,val,color in [
        (r1,"CEMENT","1.000","#f0c060"),
        (r2,"FINE AGGREGATE",str(res['r_fa']),"#7dd8f8"),
        (r3,"COARSE AGGREGATE",str(res['r_ca']),"#6ee7b7"),
        (r4,"WATER",str(res['r_w']),"#fca5a5"),
    ]:
        col.markdown(f'<div class="ratio-card"><div class="ratio-label">{label}</div><div class="ratio-value" style="color:{color}">{val}</div></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Quantity per m3 of Concrete")
    rows = [{"Material":"Cement","Quantity (kg/m3)":round(res['cement'],2),"Volume (m3)":round(res['vol_cement'],4),"Ratio":1.000}]
    if res['use_fly']:
        rows.append({"Material":"Fly Ash","Quantity (kg/m3)":round(res['flyash'],2),"Volume (m3)":round(res['vol_flyash'],4),"Ratio":round(res['flyash']/res['cement'],3)})
    rows += [
        {"Material":"Fine Aggregate","Quantity (kg/m3)":round(res['fa'],2),"Volume (m3)":round(res['vol_fa'],4),"Ratio":res['r_fa']},
        {"Material":"Coarse Aggregate","Quantity (kg/m3)":round(res['ca'],2),"Volume (m3)":round(res['vol_ca'],4),"Ratio":res['r_ca']},
        {"Material":"Water","Quantity (kg/m3)":round(res['water'],2),"Volume (m3)":round(res['vol_water'],4),"Ratio":res['r_w']},
    ]
    total_kg  = sum(r["Quantity (kg/m3)"] for r in rows)
    total_vol = sum(r["Volume (m3)"] for r in rows)
    rows.append({"Material":"TOTAL","Quantity (kg/m3)":round(total_kg,2),"Volume (m3)":round(total_vol,4),"Ratio":"—"})
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Design Steps - IS 10262 : 2019")
    for title, body in res['steps']:
        with st.expander(f"{title}"):
            st.code(body, language=None)
    st.success("Mix design completed successfully as per IS 10262 : 2019 & IS 456 : 2000")
else:
    st.info("Fill in the inputs on the left panel and click CALCULATE MIX DESIGN to get results.")
    st.markdown("""<div class="result-box">IS 10262 : 2019 - DESIGN PROCEDURE

  Step 1  ->  Target Mean Compressive Strength
  Step 2  ->  Selection of Water-Cement Ratio
  Step 3  ->  Selection of Water Content
  Step 4  ->  Calculation of Cement Content
  Step 5  ->  Proportion of Volume of CA and FA
  Step 6  ->  Mix Proportions for Trial Mix

  Supports:
    - M10 to M50 grades
    - Mild to Extreme exposure conditions
    - Chemical admixtures (plasticizer)
    - Mineral admixtures (fly ash, IS 1344)
    - All fine aggregate zones (IS 383)
    - MSA: 10mm, 16mm, 20mm, 25mm, 40mm</div>""", unsafe_allow_html=True)
