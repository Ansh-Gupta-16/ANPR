import streamlit as st
import requests
import time

# ── Page config ─────────────────────────────────────────────
st.set_page_config(
    page_title="ALPR — Number Plate Recognition",
    page_icon="🚗",
    layout="wide",
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
/* ── Base ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0d1117;
    color: #e6edf3;
}

/* ── Header ── */
.alpr-header {
    background: linear-gradient(135deg, #1a2332 0%, #0d1117 100%);
    border: 1px solid #21262d;
    border-radius: 12px;
    padding: 28px 32px;
    margin-bottom: 24px;
}
.alpr-header h1 {
    font-size: 2rem;
    font-weight: 700;
    color: #f0f6fc;
    margin: 0;
    letter-spacing: -0.5px;
}
.alpr-header p {
    color: #8b949e;
    font-size: 0.95rem;
    margin: 6px 0 0 0;
}

/* ── Config box ── */
.config-box {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 20px 24px;
    margin-bottom: 20px;
}
.config-box label {
    font-size: 0.8rem;
    color: #8b949e;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* ── Metric cards ── */
.metric-row { display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }
.metric-card {
    flex: 1; min-width: 130px;
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 16px 18px;
    text-align: center;
}
.metric-card .val {
    font-size: 1.7rem;
    font-weight: 700;
    color: #58a6ff;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1;
}
.metric-card .lbl {
    font-size: 0.75rem;
    color: #8b949e;
    margin-top: 5px;
    font-weight: 500;
}

/* ── Type badge ── */
.type-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    margin-bottom: 6px;
}
.badge-white    { background:#2d333b; color:#e6edf3; border:1px solid #444c56; }
.badge-yellow   { background:#2d2a1f; color:#e3b341; border:1px solid #5a4c1a; }
.badge-green    { background:#1a2d1e; color:#3fb950; border:1px solid #1f4428; }
.badge-red      { background:#2d1a1a; color:#f85149; border:1px solid #4d1f1f; }
.badge-black    { background:#1a1a1f; color:#b0b8c4; border:1px solid #333; }
.badge-unknown  { background:#21262d; color:#8b949e; border:1px solid #30363d; }

/* ── Plate card ── */
.plate-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 10px;
    transition: border-color 0.2s;
}
.plate-card:hover { border-color: #58a6ff44; }
.plate-number {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.35rem;
    font-weight: 600;
    color: #f0f6fc;
    letter-spacing: 2px;
    margin-bottom: 6px;
}
.plate-meta { font-size: 0.82rem; color: #8b949e; }
.plate-meta span { margin-right: 16px; }

/* ── Confidence bar ── */
.conf-bar-wrap {
    background: #21262d;
    border-radius: 4px;
    height: 6px;
    margin-top: 10px;
    overflow: hidden;
}
.conf-bar {
    height: 6px;
    border-radius: 4px;
    background: linear-gradient(90deg, #1f6feb, #58a6ff);
    transition: width 0.6s ease;
}

/* ── Section title ── */
.section-title {
    font-size: 0.78rem;
    font-weight: 600;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 20px 0 10px 0;
    border-bottom: 1px solid #21262d;
    padding-bottom: 8px;
}

/* ── State pill ── */
.state-pill {
    display:inline-block;
    background: #1f2d3d;
    border: 1px solid #1f6feb44;
    border-radius: 6px;
    padding: 5px 12px;
    font-size: 0.82rem;
    color: #79c0ff;
    font-weight: 500;
    margin: 4px 4px 4px 0;
}

/* ── Type distribution bar ── */
.dist-row { display:flex; align-items:center; margin-bottom:8px; gap:10px; }
.dist-label { font-size:0.82rem; color:#8b949e; width:170px; flex-shrink:0; }
.dist-track {
    flex:1; background:#21262d; border-radius:4px; height:8px; overflow:hidden;
}
.dist-fill { height:8px; border-radius:4px; }

/* ── Button overrides ── */
.stButton > button {
    background: #238636 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    width: 100%;
    transition: background 0.2s !important;
}
.stButton > button:hover { background: #2ea043 !important; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border: 2px dashed #30363d !important;
    border-radius: 10px !important;
    background: #161b22 !important;
    padding: 20px !important;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: #58a6ff !important; }

/* ── Streamlit element cleanup ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; }
</style>
""", unsafe_allow_html=True)


# ── State codes helper ───────────────────────────────────────
STATE_CODES = {
    'AP': 'Andhra Pradesh', 'AR': 'Arunachal Pradesh', 'AS': 'Assam',
    'BR': 'Bihar', 'CG': 'Chhattisgarh', 'GA': 'Goa', 'GJ': 'Gujarat',
    'HR': 'Haryana', 'HP': 'Himachal Pradesh', 'JH': 'Jharkhand',
    'KA': 'Karnataka', 'KL': 'Kerala', 'MP': 'Madhya Pradesh',
    'MH': 'Maharashtra', 'MN': 'Manipur', 'ML': 'Meghalaya',
    'MZ': 'Mizoram', 'NL': 'Nagaland', 'OD': 'Odisha', 'OR': 'Odisha',
    'PB': 'Punjab', 'RJ': 'Rajasthan', 'SK': 'Sikkim', 'TN': 'Tamil Nadu',
    'TS': 'Telangana', 'TR': 'Tripura', 'UP': 'Uttar Pradesh',
    'UK': 'Uttarakhand', 'WB': 'West Bengal', 'DL': 'Delhi',
    'AN': 'Andaman and Nicobar', 'CH': 'Chandigarh', 'DD': 'Daman and Diu',
    'DN': 'Dadra and Nagar Haveli', 'JK': 'Jammu and Kashmir',
    'LA': 'Ladakh', 'LD': 'Lakshadweep', 'PY': 'Puducherry',
    'BH': 'Bharat Series',
}

TYPE_STYLES = {
    "Private (White)":     ("badge-white",   "#b0b8c4", "🚗"),
    "Commercial (Yellow)": ("badge-yellow",  "#e3b341", "🚛"),
    "Electric (Green)":    ("badge-green",   "#3fb950", "⚡"),
    "Government (Red)":    ("badge-red",     "#f85149", "🏛️"),
    "Army (Black)":        ("badge-black",   "#6e7681", "🪖"),
    "Unknown":             ("badge-unknown", "#8b949e", "❓"),
}


def type_badge(vehicle_type: str) -> str:
    badge_cls, _, icon = TYPE_STYLES.get(vehicle_type, ("badge-unknown", "#8b949e", "❓"))
    return f'<span class="type-badge {badge_cls}">{icon} {vehicle_type}</span>'


def conf_color(conf: float) -> str:
    if conf >= 0.85:  return "#3fb950"
    if conf >= 0.65:  return "#e3b341"
    return "#f85149"


# ── Header ──────────────────────────────────────────────────
st.markdown("""
<div class="alpr-header">
  <h1>🚗 ALPR — License Plate Recognition</h1>
  <p>Upload a traffic video · Detect Indian number plates · Classify vehicle types</p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar : API config ─────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    api_url = st.text_input(
        "Backend URL (ngrok)",
        placeholder="https://xxxx-xx-xxx-xxx.ngrok-free.app",
        help="Paste the ngrok URL printed by the Colab backend."
    )
    st.caption("Start the Colab backend first, then paste the URL above.")
    st.markdown("---")
    st.markdown("**Supported formats:** MP4, MOV, AVI")
    st.markdown("**Max recommended size:** 200 MB")

# ── Main layout ──────────────────────────────────────────────
col_upload, col_results = st.columns([1, 1], gap="large")

with col_upload:
    st.markdown('<div class="section-title">Upload Video</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Drag & drop or click to browse",
        type=["mp4", "mov", "avi"],
        label_visibility="collapsed",
    )

    if uploaded_file:
        st.video(uploaded_file)
        file_size = len(uploaded_file.getvalue()) / (1024 * 1024)
        st.markdown(
            f'<div class="metric-row">'
            f'<div class="metric-card"><div class="val">{file_size:.1f}</div><div class="lbl">Size (MB)</div></div>'
            f'<div class="metric-card"><div class="val">{uploaded_file.type.split("/")[-1].upper()}</div><div class="lbl">Format</div></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        if not api_url:
            st.warning("⚠️ Enter the backend URL in the sidebar before processing.")
        else:
            if st.button("🚀 Start Recognition"):
                with st.spinner("Sending video to backend…"):
                    try:
                        endpoint = api_url.rstrip("/") + "/anpr"
                        files    = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        t0       = time.time()
                        response = requests.post(endpoint, files=files, timeout=300)
                        elapsed  = time.time() - t0

                        if response.status_code == 200:
                            st.session_state["result"]  = response.json()
                            st.session_state["elapsed"] = elapsed
                            st.success(f"✅ Done in {elapsed:.1f}s")
                        else:
                            detail = ""
                            try:
                                detail = response.json().get("message", "")
                            except Exception:
                                pass
                            st.error(f"❌ Backend error {response.status_code}: {detail or response.text[:200]}")

                    except requests.exceptions.ConnectionError:
                        st.error("❌ Could not reach the backend. Is the Colab server running? Is the URL correct?")
                    except requests.exceptions.Timeout:
                        st.error("❌ Request timed out (>5 min). Try a shorter video.")
                    except Exception as exc:
                        st.error(f"❌ Unexpected error: {exc}")
    else:
        st.info("Upload a video file to begin.")


# ── Results panel ────────────────────────────────────────────
with col_results:
    st.markdown('<div class="section-title">Detection Results</div>', unsafe_allow_html=True)

    if "result" not in st.session_state:
        st.markdown(
            '<div style="color:#8b949e;font-size:0.9rem;padding:40px 0;text-align:center;">'
            'Results will appear here after processing.</div>',
            unsafe_allow_html=True,
        )
    else:
        result  = st.session_state["result"]
        summary = result.get("processing_summary", {})
        plates  = result.get("detected_plates", [])
        elapsed = st.session_state.get("elapsed", 0)

        # ── Summary metrics ──────────────────────────────────
        total_f   = summary.get("total_frames", "—")
        proc_f    = summary.get("frames_processed", "—")
        raw_det   = summary.get("raw_detections", "—")
        unique_p  = summary.get("unique_plates", len(plates))

        st.markdown(
            f'<div class="metric-row">'
            f'<div class="metric-card"><div class="val">{unique_p}</div><div class="lbl">Plates Found</div></div>'
            f'<div class="metric-card"><div class="val">{raw_det}</div><div class="lbl">Raw Detections</div></div>'
            f'<div class="metric-card"><div class="val">{proc_f}</div><div class="lbl">Frames Scanned</div></div>'
            f'<div class="metric-card"><div class="val">{elapsed:.0f}s</div><div class="lbl">Process Time</div></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # ── Vehicle type distribution ────────────────────────
        type_counts = summary.get("vehicle_type_counts", {})
        if not type_counts and plates:
            for p in plates:
                vt = p.get("vehicle_type", "Unknown")
                type_counts[vt] = type_counts.get(vt, 0) + 1

        if type_counts:
            st.markdown('<div class="section-title">Vehicle Type Breakdown</div>', unsafe_allow_html=True)
            max_count = max(type_counts.values()) if type_counts else 1
            type_html = ""
            for vtype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
                _, fill_color, icon = TYPE_STYLES.get(vtype, ("badge-unknown", "#8b949e", "❓"))
                pct = int(count / max_count * 100)
                type_html += (
                    f'<div class="dist-row">'
                    f'<div class="dist-label">{icon} {vtype}</div>'
                    f'<div class="dist-track"><div class="dist-fill" style="width:{pct}%;background:{fill_color};"></div></div>'
                    f'<div style="font-size:0.85rem;color:#e6edf3;font-weight:600;width:28px;text-align:right;">{count}</div>'
                    f'</div>'
                )
            st.markdown(type_html, unsafe_allow_html=True)

        # ── Plate list ───────────────────────────────────────
        if plates:
            st.markdown('<div class="section-title">Detected Plates</div>', unsafe_allow_html=True)

            for plate in plates:
                text      = plate.get("plate", "—")
                conf      = plate.get("confidence", 0)
                vtype     = plate.get("vehicle_type", "Unknown")
                frame_num = plate.get("frame_number", "—")
                timestamp = plate.get("timestamp", None)
                info      = plate.get("info", {})

                state_name = info.get("state_name", "") if info else ""
                rto_code   = info.get("rto_code", "")   if info else ""

                ts_str = f"{timestamp:.1f}s" if timestamp is not None else f"frame {frame_num}"
                conf_pct = int(conf * 100)
                cc = conf_color(conf)

                state_pill = (
                    f'<span class="state-pill">📍 {state_name}</span>'
                    if state_name and state_name != "Unknown" else ""
                )
                rto_pill = (
                    f'<span class="state-pill">RTO {rto_code}</span>'
                    if rto_code else ""
                )

                card = f"""
<div class="plate-card">
  <div class="plate-number">{text}</div>
  {type_badge(vtype)}
  <div class="plate-meta">
    <span>⏱ {ts_str}</span>
    <span style="color:{cc}">● {conf_pct}% confidence</span>
  </div>
  <div class="conf-bar-wrap">
    <div class="conf-bar" style="width:{conf_pct}%;background:linear-gradient(90deg,{cc}88,{cc});"></div>
  </div>
  <div style="margin-top:10px;">{state_pill}{rto_pill}</div>
</div>"""
                st.markdown(card, unsafe_allow_html=True)

        elif result.get("status") == "success":
            st.warning("⚠️ No valid plates were detected in this video. Try a clearer / higher-resolution video.")