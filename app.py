import streamlit as st
from src.styles import CSS
from src.analytics import run_clinical_analysis, build_signal_feed
from src import charts
from src.ui import (
    render_sidebar,
    render_hero,
    render_lane_selector,
    render_snapshot,
    render_lane_cards,
    section,
    render_signal_feed,
    render_footer,
    render_dark_table,
)

st.set_page_config(page_title="NextCure Signal Room", page_icon="🧬", layout="wide", initial_sidebar_state="collapsed")
st.markdown(CSS, unsafe_allow_html=True)
render_sidebar()

if "scan_ran" not in st.session_state:
    st.session_state.scan_ran = False

render_hero()
selected_lanes = render_lane_selector()

# Centered, clean power-on action.
st.markdown('<div class="run-button-zone">', unsafe_allow_html=True)
run_scan = st.button("▶  Run Intelligence Scan", key="run_analysis", disabled=not selected_lanes)
st.markdown('</div>', unsafe_allow_html=True)
if run_scan:
    st.session_state.scan_ran = True

if not st.session_state.scan_ran:
    st.stop()

progress = st.progress(0)
status_box = st.empty()
status_box.caption("Initializing clinical registry scan…")
progress.progress(20)
lane_status = "all four lanes" if len(selected_lanes) == 4 else ", ".join(selected_lanes)
status_box.caption(f"Filtering {lane_status} registry lane selection…")
progress.progress(45)
bundle = run_clinical_analysis(selected_lanes)
progress.progress(75)
status_box.caption("Building executive clinical views…")
progress.progress(100)
status_box.empty()
progress.empty()

df = bundle["df"]
active_df = bundle["active_df"]
planned_start_df = bundle["planned_start_df"]
expected_completion_df = bundle["expected_completion_df"]

# 1. Immediate orientation.
section("Executive Snapshot")
render_snapshot(bundle)

# 2. Highest priority: what is alive, what is inactive, and where NextCure lanes sit.
section("Recruitment & Development Status")
st1, st2 = st.columns([.95, 1.05])
with st1:
    st.plotly_chart(charts.status_overview_chart(df), width="stretch", config=charts.CHART_CONFIG)
with st2:
    st.plotly_chart(charts.status_by_lane_chart(df), width="stretch", config=charts.CHART_CONFIG)
term_df = df[df["status_group"] == "Terminated / Withdrawn / Suspended"]
with st.expander("Terminated / withdrawn / suspended study watchlist", expanded=not term_df.empty):
    if term_df.empty:
        st.caption("No terminated, withdrawn, or suspended records were captured in the current preset scan.")
    else:
        st.plotly_chart(charts.terminated_watchlist_chart(df), width="stretch", config=charts.CHART_CONFIG)
        render_dark_table(term_df[["nct_id", "target_lane", "sponsor", "status", "phase", "modality_class", "adc_relevance", "title", "conditions", "interventions", "last_update", "url"]].sort_values(["target_lane", "sponsor"]), height=360)

# 3. Development window early, with a lane-aware title when the scan is focused.
development_window_title = "Four-Lane Trial Development Window" if len(selected_lanes) == 4 else f"{bundle['scan_scope']} Trial Development Window"
section(development_window_title)
st.plotly_chart(charts.timeline_chart(df), width="stretch", config=charts.CHART_CONFIG)

# 4. Forward-looking calendar: what starts and what may read out.
section("Forward-Looking Catalyst Calendar")
fc1, fc2 = st.columns([1, 1])
with fc1:
    st.markdown("#### Planned Trial Starts")
    if planned_start_df.empty:
        st.info("No future start dates found in the current scan.")
    else:
        st.plotly_chart(charts.forward_start_chart(planned_start_df), width="stretch", config=charts.CHART_CONFIG)
with fc2:
    st.markdown("#### Expected Primary Completions")
    if expected_completion_df.empty:
        st.info("No future primary completion dates found in the current scan.")
    else:
        st.plotly_chart(charts.forward_completion_chart(expected_completion_df), width="stretch", config=charts.CHART_CONFIG)
with st.expander("Planned / not-yet-recruiting registry records", expanded=False):
    planned_table = bundle["planned_df"].copy()
    if planned_table.empty:
        st.caption("No planned or not-yet-recruiting records were captured in this scan.")
    else:
        for dc in ["start_date", "primary_completion_date", "completion_date", "last_update"]:
            if dc in planned_table:
                planned_table[dc] = planned_table[dc].dt.strftime("%b %d, %Y").fillna("Date not listed")
        render_dark_table(planned_table[["nct_id", "target_lane", "sponsor", "status", "phase", "start_date", "primary_completion_date", "completion_date", "title", "url"]].sort_values(["target_lane", "start_date"]), height=360)

# 5. Competitive ADC sponsor view.
section("Active ADC-Focused Sponsor / Competitor Activity")
st.plotly_chart(charts.sponsor_chart(df), width="stretch", config=charts.CHART_CONFIG)

# 6. Patient scale and who is being studied.
section("Patient Population & Enrollment")
e1, e2 = st.columns([1, 1])
fig_enroll_lane, fig_enroll_ind = charts.enrollment_charts(df)
with e1:
    st.plotly_chart(fig_enroll_lane, width="stretch", config=charts.CHART_CONFIG)
with e2:
    st.plotly_chart(fig_enroll_ind, width="stretch", config=charts.CHART_CONFIG)
lane_enroll_detail, pop_enroll_detail = charts.enrollment_detail_tables(df)
with st.expander("Enrollment detail: lane, phase, status, and ADC relevance", expanded=False):
    render_dark_table(lane_enroll_detail, height=360)
with st.expander("Enrollment detail: patient population, line of therapy, and prior-treatment context", expanded=False):
    render_dark_table(pop_enroll_detail, height=420)

# 7. Modality/status detail because ADC vs non-ADC is strategically important.
section("ADC vs Non-ADC Modality")
mod1, mod2 = st.columns([1, 1])
with mod1:
    st.plotly_chart(charts.modality_chart(df), width="stretch", config=charts.CHART_CONFIG)
with mod2:
    st.plotly_chart(charts.adc_relevance_chart(df), width="stretch", config=charts.CHART_CONFIG)
st.plotly_chart(charts.status_by_modality_chart(df), width="stretch", config=charts.CHART_CONFIG)
status_modality_detail = charts.status_modality_detail_table(df)
with st.expander("Status × modality detail by lane, phase, sponsors, enrollment, and sites", expanded=False):
    render_dark_table(status_modality_detail, height=420)

# 8. Therapy, partner, and biology interpretation after the operational views.
section("Target-Relevant Therapy Intelligence")
tr1, tr2 = st.columns([1, 1])
with tr1:
    st.plotly_chart(charts.lane_relevance_chart(df), width="stretch", config=charts.CHART_CONFIG)
with tr2:
    st.plotly_chart(charts.target_specific_signal_chart(df), width="stretch", config=charts.CHART_CONFIG)
cmb1, cmb2 = st.columns([1, 1])
with cmb1:
    st.plotly_chart(charts.combo_chart(df), width="stretch", config=charts.CHART_CONFIG)
with cmb2:
    st.plotly_chart(charts.combo_class_chart(df), width="stretch", config=charts.CHART_CONFIG)
st.plotly_chart(charts.partner_landscape_chart(df), width="stretch", config=charts.CHART_CONFIG)
st.plotly_chart(charts.partner_agent_chart(df), width="stretch", config=charts.CHART_CONFIG)
st.plotly_chart(charts.strategic_signal_stack_chart(df), width="stretch", config=charts.CHART_CONFIG)
st.plotly_chart(charts.biology_signal_chart(df), width="stretch", config=charts.CHART_CONFIG)
with st.expander("Target-relevant evidence highlights", expanded=False):
    highlight_cols = ["nct_id", "target_lane", "adc_relevance", "modality_class", "lane_relevance_score", "lane_relevance_label", "sponsor", "phase", "status", "status_group", "indication_hint", "combo_classes", "combo_agents", "partner_landscape_bucket", "strategic_signal_stack", "biology_signals", "line_of_therapy", "prior_therapy_context", "line_of_therapy_evidence", "lane_specific_readout", "url"]
    render_dark_table(df[highlight_cols].sort_values(["lane_relevance_score", "target_lane"], ascending=[False, True]).head(30), height=460)

# 9. Line of therapy detail.
section("Line of Therapy")
lot1, lot2 = st.columns([1, 1])
with lot1:
    st.plotly_chart(charts.line_of_therapy_chart(df), width="stretch", config=charts.CHART_CONFIG)
with lot2:
    st.plotly_chart(charts.prior_therapy_context_chart(df), width="stretch", config=charts.CHART_CONFIG)

# 10. Supporting trial structure: phase, lane snapshot, geography.
section("Active Trials by Phase")
if active_df.empty:
    st.info("No active phase data found for the current scan.")
else:
    st.plotly_chart(charts.active_phase_chart(active_df), width="stretch", config=charts.CHART_CONFIG)

section("Lane Snapshot")
render_lane_cards(bundle)

section("Geographic Trial Footprint")
g1, g2 = st.columns([1.05, .95])
fig_country, fig_geo_heat, _country_counts = charts.country_charts(active_df if not active_df.empty else df)
with g1:
    st.plotly_chart(fig_country, width="stretch", config=charts.CHART_CONFIG)
with g2:
    st.plotly_chart(fig_geo_heat, width="stretch", config=charts.CHART_CONFIG)

# 11. Trust layer and raw evidence last.
section("Signal Feed")
render_signal_feed(build_signal_feed(bundle))

section("Evidence Table")
cols = ["nct_id", "target_lane", "adc_relevance", "modality_class", "lane_relevance_score", "lane_relevance_label", "title", "sponsor", "status", "status_group", "phase", "study_type", "enrollment", "enrollment_type", "start_date", "primary_completion_date", "completion_date", "countries", "site_count", "indication_hint", "combo_category", "combo_classes", "combo_agents", "partner_landscape_bucket", "strategic_signal_stack", "biology_signals", "line_of_therapy", "prior_therapy_context", "line_of_therapy_evidence", "combo_evidence", "lane_specific_readout", "conditions", "interventions", "url"]
display_df = df[cols].sort_values(["target_lane", "sponsor", "phase"]).reset_index(drop=True).copy()
for dc in ["start_date", "primary_completion_date", "completion_date"]:
    display_df[dc] = display_df[dc].dt.strftime("%b %d, %Y").fillna("Date not listed")
render_dark_table(display_df, height=620)
render_footer()
