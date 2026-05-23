import datetime as dt
import html
import base64
from pathlib import Path
import pandas as pd
import streamlit as st
from .config import APP_VERSION, TARGET_LANES, LANE_DISPLAY_NAMES, LANE_CAPTIONS
from .analytics import split_multi_rows


def render_sidebar():
    with st.sidebar:
        st.markdown("### BuildWell Control Notes")
        st.caption(f"{APP_VERSION}. Executive-facing flow remains one button only.")
        st.markdown("**Preset lanes**")
        for lane in TARGET_LANES:
            st.caption(f"• {lane}")
        st.caption("Architecture: UI → analytics service → ingestion client → normalization layer. Later the same layers can move behind FastAPI/Postgres without rebuilding the Streamlit UI.")


def _emblem_data_uri() -> str:
    asset = Path(__file__).resolve().parents[1] / "assets" / "buildwell_emblem.png"
    if not asset.exists():
        return ""
    encoded = base64.b64encode(asset.read_bytes()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def render_hero():
    emblem = _emblem_data_uri()
    emblem_html = f'<img class="buildwell-emblem" src="{emblem}" alt="Built by BuildWell" />' if emblem else ""
    st.markdown(f"""
    <div class="hero-clean">
        <div class="hero-inner">
            <div class="hero-kicker">Clinical Intelligence Console</div>
            <div class="hero-title">NextCure Signal Room</div>
            <div class="hero-accent"></div>
        </div>
        {emblem_html}
    </div>
    """, unsafe_allow_html=True)



def render_lane_selector() -> list[str]:
    """Premium first-screen selector for choosing one, several, or all clinical lanes."""
    lane_options = list(TARGET_LANES.keys())
    if "scan_lanes" not in st.session_state:
        st.session_state.scan_lanes = lane_options.copy()

    current = st.session_state.get("scan_lanes", lane_options.copy())
    if not isinstance(current, list):
        current = lane_options.copy()
    current = [lane for lane in current if lane in lane_options]
    st.session_state.scan_lanes = current

    lane_meta = {
        "B7-H4 / VTCN1": {"title": "B7-H4 (ADC)", "subtitle": "Antibody-Drug Conjugate", "note": "Target intelligence", "icon": "Y", "tone": "violet"},
        "CDH6": {"title": "CDH6 (ADC)", "subtitle": "Antibody-Drug Conjugate", "note": "Ovarian-relevant intelligence", "icon": "C6", "tone": "blue"},
        "Alzheimer's / ApoE4": {"title": "Alzheimer's / ApoE4", "subtitle": "Neurodegeneration", "note": "Biomarker intelligence", "icon": "A4", "tone": "green"},
        "Bone / Siglec-15": {"title": "Bone / Siglec-15", "subtitle": "Bone Biology & Oncology", "note": "Registry intelligence", "icon": "B", "tone": "gold"},
    }

    st.markdown(
        '<div class="scan-selector-shell">'
        '<div class="scan-selector-kicker">Analysis Scope</div>'
        '<div class="scan-selector-title">Choose the intelligence lanes</div>'
        '<div class="scan-selector-note">Select one or more lanes to include in the analysis. Run all four lanes, focus on one lane, or combine the exact lanes needed for the discussion.</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="lane-card-zone">', unsafe_allow_html=True)
    cols = st.columns(4, gap="medium")
    for idx, lane in enumerate(lane_options):
        meta = lane_meta[lane]
        selected = lane in st.session_state.scan_lanes
        state_class = "selected" if selected else "unselected"
        with cols[idx]:
            check = "IN" if selected else ""
            card_html = f"""
                <div class="lane-choice-card lane-{meta['tone']} {state_class}">
                    <div class="lane-choice-topline">
                        <div class="lane-choice-icon">{html.escape(meta['icon'])}</div>
                        <div class="lane-choice-check">{check}</div>
                    </div>
                    <div class="lane-choice-title">{html.escape(meta['title'])}</div>
                    <div class="lane-choice-subtitle">{html.escape(meta['subtitle'])}</div>
                    <div class="lane-choice-note">{html.escape(meta['note'])}</div>
                </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            toggle_label = "Remove" if selected else "Include"
            if st.button(toggle_label, key=f"lane_toggle_{idx}", use_container_width=True):
                updated = list(st.session_state.scan_lanes)
                if selected:
                    updated = [item for item in updated if item != lane]
                else:
                    updated.append(lane)
                st.session_state.scan_lanes = [item for item in lane_options if item in updated]
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    selected_lanes = st.session_state.scan_lanes
    count = len(selected_lanes)
    plural = "s" if count != 1 else ""
    summary_label = f"{count} lane{plural} selected" if count else "No lanes selected"
    if count == len(lane_options):
        caption = "Comprehensive executive scan across CDH6, B7-H4, Alzheimer's/ApoE4, and Bone/Siglec-15."
    elif count:
        caption = "Selected lens: " + " • ".join(LANE_DISPLAY_NAMES.get(lane, lane) for lane in selected_lanes)
    else:
        caption = "Choose at least one lane to run the analysis."

    st.markdown('<div class="selection-center-wrap">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="lane-selection-summary centered"><span class="summary-dot">✓</span><strong>{html.escape(summary_label)}</strong><span>{html.escape(caption)}</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)
    return selected_lanes

def render_idle_panel():
    # Intentionally blank for the cleaned executive UI. The centered Run Analysis
    # button is the only power-on affordance.
    return None


def metric_card(label: str, value: str, note: str = ""):
    note_html = f'<div class="metric-note">{html.escape(str(note))}</div>' if note else ""
    st.markdown(f"""
    <div class="metric-card"><div class="metric-label">{html.escape(str(label))}</div><div class="metric-value">{html.escape(str(value))}</div>{note_html}</div>
    """, unsafe_allow_html=True)


def section(title: str, subtitle: str = ""):
    st.markdown(f'<div class="section-title">{html.escape(str(title))}</div>', unsafe_allow_html=True)
    # Clean-up pass: do not render explanatory subtitles under every heading.
    return None


def render_snapshot(bundle: dict):
    df, active_df, planned_df = bundle["df"], bundle["active_df"], bundle["planned_df"]
    countries = split_multi_rows(df, "countries", "country")["country"].nunique() if not df.empty else 0
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: metric_card("Trials Captured", f"{len(df):,}")
    with c2: metric_card("Active / Near-Active", f"{len(active_df):,}")
    with c3: metric_card("Planned", f"{len(planned_df):,}")
    with c4: metric_card("Patients Planned", f"{int(df['enrollment'].sum()):,}")
    with c5: metric_card("Countries", f"{countries:,}")


def render_lane_cards(bundle: dict):
    df = bundle["df"]
    cols = st.columns(4)
    for idx, lane in enumerate(bundle["lane_names"]):
        lane_df = df[df["target_lane"] == lane]
        active_lane = lane_df[lane_df["is_active"]]
        enroll = int(lane_df["enrollment"].sum()) if not lane_df.empty else 0
        with cols[idx]:
            st.markdown(
                f'<div class="lane-card"><div class="lane-title">{html.escape(str(lane))}</div>'
                f'<div class="lane-metrics"><span>{len(lane_df)} studies</span><span>{len(active_lane)} active</span><span>{enroll:,} patients</span></div></div>',
                unsafe_allow_html=True,
            )


def render_signal_feed(signals: list[tuple[str, str]]):
    for title, body in signals:
        st.markdown(f'<div class="signal"><strong>{html.escape(str(title))}</strong><br>{html.escape(str(body))}</div>', unsafe_allow_html=True)


def render_dark_table(df: pd.DataFrame, height: int | None = None):
    """Render a dataframe as a dark, scrollable HTML table.

    Native Streamlit dataframes can show up with white interiors on some Cloud
    theme/version combinations. This renderer keeps the executive aesthetic
    consistent for evidence/detail tables.
    """
    if df is None or df.empty:
        st.caption("No records available for this section.")
        return
    d = df.copy()
    # Convert datetimes safely for display.
    for col in d.columns:
        if pd.api.types.is_datetime64_any_dtype(d[col]):
            d[col] = d[col].dt.strftime("%b %d, %Y").fillna("Date not listed")
    d = d.fillna("Not specified")
    max_h = height or 420
    table_html = d.to_html(index=False, escape=True, classes="dark-data-table")
    st.markdown(f'<div class="dark-table-wrap" style="max-height:{max_h}px;">{table_html}</div>', unsafe_allow_html=True)


def render_footer():
    # Footer/source clutter intentionally removed in v2.5 UI cleanup.
    return None
