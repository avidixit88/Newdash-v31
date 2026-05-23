import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from .config import PHASE_ORDER, TODAY
from .analytics import split_multi_rows

CHART_CONFIG = {"displayModeBar": False}


def _to_scalar(value):
    """Return a chart-safe scalar for pandas groupby/plotly labels.

    ClinicalTrials.gov fields can arrive as lists/dicts after normalization.
    Plotly can display strings, but pandas groupby cannot hash dict/list values.
    """
    if isinstance(value, (list, tuple, set)):
        cleaned = [str(v).strip() for v in value if str(v).strip()]
        return ", ".join(cleaned) if cleaned else "Not specified"
    if isinstance(value, dict):
        return ", ".join(f"{k}: {v}" for k, v in value.items()) if value else "Not specified"
    if pd.isna(value):
        return "Not specified"
    return value


def _chart_df(df: pd.DataFrame) -> pd.DataFrame:
    """Sanitize a dataframe before chart aggregations.

    This is intentionally broad because the dashboard is fed by live registry
    records, and one malformed nested field should not crash the executive UI.
    """
    if df is None or df.empty:
        return pd.DataFrame() if df is None else df.copy()
    d = df.copy()
    for col in d.columns:
        if d[col].dtype == "object":
            d[col] = d[col].map(_to_scalar)
    for col in ["enrollment", "site_count", "lane_relevance_score"]:
        if col in d.columns:
            d[col] = pd.to_numeric(d[col], errors="coerce").fillna(0)
    for col in ["nct_id", "target_lane", "status_group", "status", "phase", "sponsor", "modality_class", "adc_relevance", "line_of_therapy"]:
        if col in d.columns:
            d[col] = d[col].astype(str).replace({"nan": "Not specified", "None": "Not specified", "": "Not specified"})
    return d

def _empty_chart(message: str, height: int = 340) -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(text=message, x=0.5, y=0.5, showarrow=False, font={"color": "#eaf2ff", "size": 14})
    return chart_layout(fig, height, legend="none")


def chart_layout(fig: go.Figure, height: int = 410, legend: str = "bottom") -> go.Figure:
    """Apply the Signal Room chart theme.

    Legends are intentionally placed outside the plotting/title area wherever
    possible because the prior build let horizontal legends collide with chart
    titles. Bottom legends use extra bottom margin; right legends are used for
    dense timelines where a bottom legend would eat too much vertical space.
    """
    legend_cfg = {
        "font": {"color": "#ffffff", "size": 13},
        "title": {"font": {"color": "#ffffff", "size": 13}},
        "bgcolor": "rgba(8,13,24,.84)",
        "bordercolor": "rgba(190,205,235,.34)",
        "borderwidth": 1,
    }
    margin = {"l": 10, "r": 10, "t": 78, "b": 156}
    if legend == "right":
        legend_cfg.update({"orientation": "v", "yanchor": "top", "y": 1, "xanchor": "left", "x": 1.02})
        margin = {"l": 10, "r": 180, "t": 78, "b": 36}
    elif legend == "bottom_roomy":
        legend_cfg.update({"orientation": "h", "yanchor": "top", "y": -0.34, "xanchor": "center", "x": 0.5})
        margin = {"l": 10, "r": 10, "t": 78, "b": 188}
    elif legend == "none":
        legend_cfg.update({"visible": False})
        margin = {"l": 10, "r": 10, "t": 78, "b": 40}
    else:
        legend_cfg.update({"orientation": "h", "yanchor": "top", "y": -0.42, "xanchor": "center", "x": 0.5})

    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#eef5ff", "family": "Inter, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif"},
        margin=margin,
        legend=legend_cfg,
        title={"font": {"color": "#ffffff", "size": 18}, "x": 0.01, "xanchor": "left"},
        xaxis={"gridcolor": "rgba(164,183,219,.14)", "zerolinecolor": "rgba(164,183,219,.22)", "tickfont": {"color": "#e6eefc", "size": 12}, "title": {"font": {"color": "#f4f8ff"}}},
        yaxis={"gridcolor": "rgba(164,183,219,.14)", "zerolinecolor": "rgba(164,183,219,.22)", "tickfont": {"color": "#e6eefc", "size": 12}, "title": {"font": {"color": "#f4f8ff"}}},
    )
    return fig

def active_phase_chart(active_df: pd.DataFrame) -> go.Figure:
    active_df = _chart_df(active_df)
    if active_df.empty:
        return _empty_chart("No active/near-active studies available for phase chart.", 430)
    phase_df = active_df.groupby(["target_lane", "phase"], as_index=False).agg(trials=("nct_id", "count"), enrollment=("enrollment", "sum"))
    fig = px.bar(phase_df, x="phase", y="trials", color="target_lane", hover_data=["enrollment"], category_orders={"phase": PHASE_ORDER}, title="Active / Near-Active Trials by Phase")
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Studies")
    return chart_layout(fig, 430)


def country_charts(df: pd.DataFrame) -> tuple[go.Figure, go.Figure, pd.DataFrame]:
    df = _chart_df(df)
    country_rows = split_multi_rows(df, "countries", "country")
    country_counts = country_rows.groupby("country", as_index=False).agg(trials=("nct_id", "count"), enrollment=("enrollment", "sum"), sites=("site_count", "sum")).sort_values("trials", ascending=False).head(18)
    fig_country = px.bar(country_counts.sort_values("trials"), x="trials", y="country", orientation="h", hover_data=["enrollment", "sites"], title="Active Trials by Country")
    fig_country.update_xaxes(title="Studies")
    fig_country.update_yaxes(title="")
    geo_lane = country_rows.groupby(["target_lane", "country"], as_index=False).agg(trials=("nct_id", "count"))
    geo_pivot = geo_lane.pivot_table(index="country", columns="target_lane", values="trials", aggfunc="sum", fill_value=0) if not geo_lane.empty else pd.DataFrame()
    fig_heat = px.imshow(geo_pivot, text_auto=True, aspect="auto", title="Country × Lane Density") if not geo_pivot.empty else go.Figure()
    return chart_layout(fig_country, 470, legend="none"), chart_layout(fig_heat, 470, legend="none"), country_counts


def enrollment_charts(df: pd.DataFrame) -> tuple[go.Figure, go.Figure]:
    """Enrollment views with more context than blunt totals.

    ClinicalTrials.gov enrollment is a listed study target/actual count, not
    disease prevalence. This version keeps the high-level charts readable but
    encodes more useful context: active/planned/completed status, phase, ADC
    relevance, and patient-population hints.
    """
    df = _chart_df(df)
    if df.empty:
        return _empty_chart("No enrollment data available.", 430), _empty_chart("No enrollment data available.", 430)

    for col in ["status_group", "enrollment_type", "target_lane", "indication_hint", "modality_class", "adc_relevance", "phase"]:
        if col not in df.columns:
            df[col] = "Not specified"

    enroll_lane = (
        df.groupby(["target_lane", "status_group", "phase", "adc_relevance"], as_index=False)
        .agg(enrollment=("enrollment", "sum"), trials=("nct_id", "count"), sites=("site_count", "sum"))
        .sort_values(["target_lane", "enrollment"], ascending=[True, False])
    )
    fig_lane = px.bar(
        enroll_lane,
        x="target_lane",
        y="enrollment",
        color="status_group",
        hover_data=["trials", "sites", "phase", "adc_relevance"],
        title="Listed Enrollment by Lane, Status, Phase, and ADC Relevance",
    )
    fig_lane.update_xaxes(title="")
    fig_lane.update_yaxes(title="Listed patients")

    enroll_ind = (
        df.groupby(["indication_hint", "target_lane", "phase", "adc_relevance", "status_group"], as_index=False)
        .agg(enrollment=("enrollment", "sum"), trials=("nct_id", "count"), sites=("site_count", "sum"))
        .sort_values("enrollment", ascending=False)
        .head(30)
    )
    enroll_ind["population_label"] = enroll_ind["indication_hint"].astype(str).str.slice(0, 38) + " · " + enroll_ind["target_lane"].astype(str).str.slice(0, 12)
    fig_ind = px.bar(
        enroll_ind.sort_values("enrollment"),
        x="enrollment",
        y="population_label",
        color="adc_relevance",
        orientation="h",
        hover_data=["trials", "sites", "phase", "status_group", "target_lane"],
        title="Listed Enrollment by Patient Population, Lane, Phase, and ADC Relevance",
    )
    fig_ind.update_xaxes(title="Listed patients")
    fig_ind.update_yaxes(title="")
    return chart_layout(fig_lane, 500, legend="right"), chart_layout(fig_ind, 620, legend="right")


def enrollment_detail_tables(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return executive-detail enrollment tables for the Streamlit UI.

    These tables are intentionally separate from the charts because the user
    asked for more data points, not just prettier aggregation.
    """
    d = _chart_df(df)
    if d.empty:
        return pd.DataFrame(), pd.DataFrame()
    for col in ["target_lane", "status_group", "phase", "adc_relevance", "indication_hint", "line_of_therapy", "prior_therapy_context", "enrollment_type", "sponsor"]:
        if col not in d.columns:
            d[col] = "Not specified"
    if "site_count" not in d.columns:
        d["site_count"] = 0

    lane_detail = (
        d.groupby(["target_lane", "status_group", "phase", "adc_relevance", "enrollment_type"], as_index=False)
        .agg(
            trials=("nct_id", "count"),
            listed_enrollment=("enrollment", "sum"),
            median_enrollment=("enrollment", "median"),
            sites=("site_count", "sum"),
            sponsors=("sponsor", pd.Series.nunique),
        )
        .sort_values(["target_lane", "listed_enrollment"], ascending=[True, False])
    )

    population_detail = (
        d.groupby(["indication_hint", "target_lane", "line_of_therapy", "prior_therapy_context", "adc_relevance"], as_index=False)
        .agg(
            trials=("nct_id", "count"),
            listed_enrollment=("enrollment", "sum"),
            median_enrollment=("enrollment", "median"),
            sites=("site_count", "sum"),
            sponsors=("sponsor", pd.Series.nunique),
        )
        .sort_values("listed_enrollment", ascending=False)
        .head(40)
    )
    return lane_detail, population_detail


def combo_chart(df: pd.DataFrame) -> go.Figure:
    df = _chart_df(df)
    if df.empty:
        return _empty_chart("No combination data available.", 430)
    combo_df = df.groupby(["target_lane", "combo_category"], as_index=False).agg(
        trials=("nct_id", "count"), enrollment=("enrollment", "sum")
    )
    fig = px.bar(
        combo_df, x="target_lane", y="trials", color="combo_category",
        hover_data=["enrollment"], title="Combination Strategy by Lane"
    )
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Studies")
    return chart_layout(fig, 455)


def combo_class_chart(df: pd.DataFrame) -> go.Figure:
    df = _chart_df(df)
    rows = []
    for _, r in df.iterrows():
        classes = [c.strip() for c in str(r.get("combo_classes", "")).split(",") if c.strip() and c.strip() not in {"No partner class detected", "No lane-specific class detected"}]
        if not classes:
            classes = ["No partner class detected"]
        for cls in classes:
            rows.append({"target_lane": r.get("target_lane"), "combo_class": cls, "nct_id": r.get("nct_id"), "enrollment": r.get("enrollment", 0)})
    d = pd.DataFrame(rows)
    combo_df = d.groupby(["combo_class", "target_lane"], as_index=False).agg(trials=("nct_id", "count"), enrollment=("enrollment", "sum")) if not d.empty else pd.DataFrame(columns=["combo_class", "target_lane", "trials", "enrollment"])
    fig = px.bar(
        combo_df, x="trials", y="combo_class", color="target_lane", orientation="h",
        hover_data=["enrollment"], title="Detected Partner Classes"
    )
    fig.update_xaxes(title="Studies")
    fig.update_yaxes(title="")
    return chart_layout(fig, 560, legend="right")


def combo_confidence_chart(df: pd.DataFrame) -> go.Figure:
    df = _chart_df(df)
    if df.empty:
        return _empty_chart("No combination confidence data available.", 390)
    conf = df.groupby(["combo_confidence", "target_lane"], as_index=False).agg(trials=("nct_id", "count"))
    fig = px.bar(conf, x="combo_confidence", y="trials", color="target_lane", title="Combination Extraction Confidence")
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Studies")
    return chart_layout(fig, 390)


def forward_start_chart(planned_start_df: pd.DataFrame) -> go.Figure:
    d = _chart_df(planned_start_df)
    if d.empty:
        return _empty_chart("No planned-start records found in the current registry pull.", 430)
    d["event_label"] = d["target_lane"] + " · " + d["sponsor"].str.slice(0, 22) + " · " + d["nct_id"]
    fig = px.scatter(d, x="start_date", y="event_label", size="enrollment", color="target_lane", hover_data=["title", "status", "phase", "indication_hint", "combo_category"], title="Forward Starts: Trials Expected to Begin")
    fig.update_yaxes(title="", autorange="reversed")
    fig.update_xaxes(title="Planned / estimated start date")
    return chart_layout(fig, max(430, min(820, 120 + len(d) * 24)))


def forward_completion_chart(expected_completion_df: pd.DataFrame) -> go.Figure:
    d = _chart_df(expected_completion_df)
    if d.empty:
        return _empty_chart("No expected-completion records found in the current registry pull.", 430)
    d["event_label"] = d["target_lane"] + " · " + d["sponsor"].str.slice(0, 22) + " · " + d["nct_id"]
    fig = px.scatter(d, x="primary_completion_date", y="event_label", size="enrollment", color="phase", hover_data=["title", "status", "target_lane", "indication_hint", "combo_category"], title="Forward Completions: Primary Completion Windows")
    fig.update_yaxes(title="", autorange="reversed")
    fig.update_xaxes(title="Primary completion date")
    return chart_layout(fig, max(430, min(820, 120 + len(d) * 24)))


def sponsor_chart(df: pd.DataFrame) -> go.Figure:
    """Top sponsors, filtered to ADC-relevant records.

    The earlier chart counted every registry record in the broad lane scan.
    For Michael, this should emphasize the ADC competitive landscape, so we
    keep ADC-confirmed/watch records and the two core oncology lanes.
    """
    df = _chart_df(df)
    if df.empty:
        return _empty_chart("No sponsor data available.", 430)
    active_statuses = {"Active / Recruiting", "Active / Not Recruiting"}
    core = df[
        (df.get("target_lane", "").isin(["B7-H4 / VTCN1", "CDH6"]))
        & (df.get("status_group", "").isin(active_statuses))
        & (
            df.get("adc_relevance", "").astype(str).str.contains("ADC", case=False, na=False)
            | df.get("modality_class", "").astype(str).str.contains("ADC", case=False, na=False)
        )
    ].copy()
    if core.empty:
        return _empty_chart("No active ADC-focused sponsor records captured for B7-H4/CDH6 in this scan.", 430)
    sponsor_counts = (
        core.groupby(["sponsor", "target_lane", "status_group", "phase", "adc_relevance"], as_index=False)
        .agg(trials=("nct_id", "count"), enrollment=("enrollment", "sum"), sites=("site_count", "sum"))
        .sort_values("trials", ascending=False)
        .head(25)
    )
    fig = px.bar(
        sponsor_counts.sort_values("trials"),
        x="trials",
        y="sponsor",
        color="target_lane",
        orientation="h",
        hover_data=["status_group", "phase", "adc_relevance", "enrollment", "sites"],
        title="Top Active ADC-Focused Sponsors by Trial Count",
    )
    fig.update_yaxes(title="")
    fig.update_xaxes(title="ADC-relevant studies")
    return chart_layout(fig, 560, legend="right")


def timeline_chart(df: pd.DataFrame) -> go.Figure:
    df = _chart_df(df)
    # This development-window chart is intentionally focused only on the two
    # core oncology ADC lanes Michael asked to monitor: B7-H4 and CDH6.
    # Alzheimer's/ApoE4 and bone/Siglec-15 remain in other dashboard sections
    # as side-channel registry watch lanes, but they do not belong in this
    # oncology development-window view.
    core_lanes = ["B7-H4 / VTCN1", "CDH6"]
    d = df[df["target_lane"].isin(core_lanes)].copy()
    if d.empty:
        return chart_layout(go.Figure(), 420, legend="none")
    d["_future_weight"] = d["primary_completion_date"].fillna(d["completion_date"]).fillna(d["timeline_finish"])
    d = d.sort_values(["target_lane", "_future_weight", "timeline_start", "sponsor"])
    show_df = d.groupby("target_lane", group_keys=False).head(28).copy()
    show_df = show_df.sort_values(["target_lane", "timeline_start", "sponsor"]).head(60)
    show_df["label"] = show_df["target_lane"].str.slice(0, 18) + " · " + show_df["sponsor"].str.slice(0, 20) + " · " + show_df["nct_id"]
    fig = px.timeline(
        show_df,
        x_start="timeline_start",
        x_end="timeline_finish",
        y="label",
        color="modality_class",
        hover_data=["title", "sponsor", "target_lane", "status", "phase", "modality_class", "adc_relevance", "line_of_therapy", "enrollment", "countries", "combo_category", "conditions", "interventions"],
        title="Trial Development Windows: B7-H4 + CDH6 Core Oncology Lanes",
    )
    fig.update_yaxes(autorange="reversed", title="")
    fig.update_xaxes(title="")
    return chart_layout(fig, max(560, min(1040, 90 + len(show_df) * 24)), legend="right")


def modality_chart(df: pd.DataFrame) -> go.Figure:
    df = _chart_df(df)
    if df.empty:
        return _empty_chart("No modality data available.", 430)
    d = df.groupby(["target_lane", "modality_class"], as_index=False).agg(
        trials=("nct_id", "count"), enrollment=("enrollment", "sum")
    )
    fig = px.bar(
        d, x="target_lane", y="trials", color="modality_class",
        hover_data=["enrollment"], title="ADC vs Non-ADC Modality by Lane"
    )
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Studies")
    return chart_layout(fig, 455, legend="right")


def adc_relevance_chart(df: pd.DataFrame) -> go.Figure:
    df = _chart_df(df)
    if df.empty:
        return _empty_chart("No ADC relevance data available.", 430)
    d = df.groupby(["target_lane", "adc_relevance"], as_index=False).agg(
        trials=("nct_id", "count"), enrollment=("enrollment", "sum")
    )
    fig = px.bar(
        d, x="trials", y="target_lane", color="adc_relevance", orientation="h",
        hover_data=["enrollment"], title="ADC Relevance Audit"
    )
    fig.update_xaxes(title="Studies")
    fig.update_yaxes(title="")
    return chart_layout(fig, 430, legend="right")

def line_of_therapy_chart(df: pd.DataFrame) -> go.Figure:
    d = df.copy()
    # Keep explicit unknowns because LOT is not a universal structured registry field.
    g = d.groupby(["target_lane", "line_of_therapy"], as_index=False).agg(
        trials=("nct_id", "count"), enrollment=("enrollment", "sum")
    )
    order = ["1L / frontline", "2L", "3L", "4L+ / heavily pretreated", "Relapsed / refractory"]
    fig = px.bar(
        g,
        x="target_lane",
        y="trials",
        color="line_of_therapy",
        hover_data=["enrollment"],
        category_orders={"line_of_therapy": order},
        title="Line-of-Therapy Signals by Target Lane",
    )
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Studies")
    return chart_layout(fig, 455)

def lane_relevance_chart(df: pd.DataFrame) -> go.Figure:
    df = _chart_df(df)
    if df.empty:
        return _empty_chart("No lane relevance data available.", 430)
    d = df.groupby(["target_lane", "lane_relevance_label"], as_index=False).agg(
        trials=("nct_id", "count"), enrollment=("enrollment", "sum")
    )
    order = ["High relevance to NextCure lane", "Moderate relevance to NextCure lane", "Contextual / monitor only", "Low relevance / weak lane match"]
    fig = px.bar(
        d, x="target_lane", y="trials", color="lane_relevance_label",
        hover_data=["enrollment"], category_orders={"lane_relevance_label": order},
        title="Target-Lane Relevance, Not Generic Oncology Activity"
    )
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Studies")
    return chart_layout(fig, 430)


def target_specific_signal_chart(df: pd.DataFrame) -> go.Figure:
    rows = []
    for _, r in df.iterrows():
        classes = [c.strip() for c in str(r.get("combo_classes", "")).split(",") if c.strip()]
        classes = [c for c in classes if c not in {"No partner class detected", "No lane-specific class detected"}]
        if not classes:
            classes = ["No target-specific class detected"]
        for cls in classes:
            rows.append({"target_lane": r.get("target_lane"), "signal_class": cls, "nct_id": r.get("nct_id"), "enrollment": r.get("enrollment", 0), "score": r.get("lane_relevance_score", 0)})
    d = pd.DataFrame(rows)
    if d.empty:
        return chart_layout(go.Figure(), 430)
    g = d.groupby(["target_lane", "signal_class"], as_index=False).agg(trials=("nct_id", "count"), enrollment=("enrollment", "sum"), avg_relevance=("score", "mean"))
    fig = px.bar(
        g, x="trials", y="signal_class", color="target_lane", orientation="h",
        hover_data=["enrollment", "avg_relevance"],
        title="Target-Specific Therapy / Biology Signals"
    )
    fig.update_xaxes(title="Studies")
    fig.update_yaxes(title="")
    return chart_layout(fig, max(460, min(800, 170 + len(g) * 24)), legend="right")


def partner_landscape_chart(df: pd.DataFrame) -> go.Figure:
    """Lane-aware partner/regimen landscape.

    Unlike the named-agent chart, this keeps B7-H4/CDH6 records visible even
    when the trial is ADC monotherapy or the registry does not name a combo
    partner. This prevents the graph from falsely implying the lane has no
    captured activity.
    """
    col = "partner_landscape_bucket" if "partner_landscape_bucket" in df.columns else "combo_classes"
    d = _split_signal_rows(df, col, "partner_bucket", exclude=set())
    if d.empty:
        fig = go.Figure()
        fig.add_annotation(text="No partner/regimen buckets available in the normalized dataset.", x=0.5, y=0.5, showarrow=False, font={"color": "#eaf2ff", "size": 14})
        return chart_layout(fig, 340, legend="none")
    # Replace technical fallbacks with executive-readable buckets.
    d["partner_bucket"] = d["partner_bucket"].replace({
        "No partner class detected": "No named partner / monotherapy or not stated",
        "No lane-specific class detected": "No named partner / monotherapy or not stated",
    })
    g = d.groupby(["target_lane", "partner_bucket"], as_index=False).agg(
        trials=("nct_id", "count"), enrollment=("enrollment", "sum")
    )
    order = [
        "ADC monotherapy / no partner listed",
        "No named partner / modality unclear",
        "IO / checkpoint",
        "Chemo / platinum / taxane",
        "PARP / DNA damage",
        "Anti-VEGF / angiogenesis",
        "HER2 / EGFR / targeted pathway",
        "ADC / multi-ADC strategy",
        "Endocrine / hormonal",
        "Neuro / Alzheimer biologic",
        "Biomarker / genetics",
        "Bone / rare disease therapy",
        "Device / diagnostic / non-drug",
        "Non-oncology lane signal",
    ]
    fig = px.bar(
        g,
        x="trials",
        y="target_lane",
        color="partner_bucket",
        orientation="h",
        hover_data=["enrollment"],
        category_orders={"partner_bucket": order},
        title="Lane Partner / Regimen Landscape",
    )
    fig.update_xaxes(title="Studies")
    fig.update_yaxes(title="")
    return chart_layout(fig, 470, legend="right")


def strategic_signal_stack_chart(df: pd.DataFrame) -> go.Figure:
    col = "strategic_signal_stack" if "strategic_signal_stack" in df.columns else "biology_signals"
    d = _split_signal_rows(
        df,
        col,
        "strategic_signal",
        exclude={"No strategic signal detected beyond registry capture", "No target biology signal beyond lane match"},
    )
    if d.empty:
        fig = go.Figure()
        fig.add_annotation(text="No target-specific strategic signals detected beyond lane capture.", x=0.5, y=0.5, showarrow=False, font={"color": "#eaf2ff", "size": 14})
        return chart_layout(fig, 340, legend="none")
    g = d.groupby(["strategic_signal", "target_lane"], as_index=False).agg(
        trials=("nct_id", "count"), enrollment=("enrollment", "sum")
    )
    fig = px.bar(
        g,
        x="trials",
        y="strategic_signal",
        color="target_lane",
        orientation="h",
        hover_data=["enrollment"],
        title="Expanded Target Biology + Trial-Design Signals",
    )
    fig.update_xaxes(title="Studies")
    fig.update_yaxes(title="")
    return chart_layout(fig, max(500, min(900, 170 + 30 * g["strategic_signal"].nunique())), legend="right")


def status_overview_chart(df: pd.DataFrame) -> go.Figure:
    """Executive status mix across all captured records."""
    from .config import STATUS_GROUP_ORDER
    df = _chart_df(df)
    if df.empty or "status_group" not in df.columns:
        return _empty_chart("No trial status data available.", 430)
    d = df.groupby(["status_group"], as_index=False).agg(
        trials=("nct_id", "count"), enrollment=("enrollment", "sum"), sites=("site_count", "sum")
    )
    fig = px.bar(
        d,
        x="status_group",
        y="trials",
        hover_data=["enrollment", "sites"],
        category_orders={"status_group": STATUS_GROUP_ORDER},
        title="Trial Status Mix: Active, Planned, Completed, Terminated",
    )
    fig.update_xaxes(title="", tickangle=-20)
    fig.update_yaxes(title="Studies")
    return chart_layout(fig, 430, legend="none")


def status_by_lane_chart(df: pd.DataFrame) -> go.Figure:
    """Status distribution by NextCure-relevant lane."""
    from .config import STATUS_GROUP_ORDER
    df = _chart_df(df)
    if df.empty:
        return _empty_chart("No status-by-lane data available.", 430)
    d = df.groupby(["target_lane", "status_group"], as_index=False).agg(
        trials=("nct_id", "count"), enrollment=("enrollment", "sum")
    )
    fig = px.bar(
        d,
        x="target_lane",
        y="trials",
        color="status_group",
        hover_data=["enrollment"],
        category_orders={"status_group": STATUS_GROUP_ORDER},
        title="Status by Target Lane",
    )
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Studies")
    return chart_layout(fig, 455, legend="right")


def status_by_modality_chart(df: pd.DataFrame) -> go.Figure:
    """Development status by ADC relevance with lane context.

    This chart now answers a more useful executive question: within each target
    lane, how much active/planned/completed/discontinued development is ADC-
    confirmed, ADC-watch, or non-ADC?
    """
    from .config import STATUS_GROUP_ORDER
    df = _chart_df(df)
    if df.empty:
        return _empty_chart("No status-by-modality data available.", 430)
    for col in ["adc_relevance", "status_group", "target_lane", "modality_class", "phase"]:
        if col not in df.columns:
            df[col] = "Not specified"
    d = df.groupby(["target_lane", "adc_relevance", "status_group", "phase", "modality_class"], as_index=False).agg(
        trials=("nct_id", "count"), enrollment=("enrollment", "sum"), sites=("site_count", "sum")
    )
    d["lane_modality"] = d["target_lane"].astype(str) + " · " + d["adc_relevance"].astype(str)
    fig = px.bar(
        d.sort_values(["target_lane", "adc_relevance"]),
        x="trials",
        y="lane_modality",
        color="status_group",
        orientation="h",
        hover_data=["phase", "modality_class", "enrollment", "sites"],
        category_orders={"status_group": STATUS_GROUP_ORDER},
        title="Development Status by Lane and ADC Relevance",
    )
    fig.update_xaxes(title="Studies")
    fig.update_yaxes(title="")
    return chart_layout(fig, max(560, min(900, 190 + 38 * max(1, d["lane_modality"].nunique()))), legend="right")


def status_modality_detail_table(df: pd.DataFrame) -> pd.DataFrame:
    """Detailed status/modality table for active, planned, completed, and discontinued buckets."""
    d = _chart_df(df)
    if d.empty:
        return pd.DataFrame()
    for col in ["target_lane", "adc_relevance", "modality_class", "status_group", "status", "phase", "sponsor"]:
        if col not in d.columns:
            d[col] = "Not specified"
    return (
        d.groupby(["target_lane", "adc_relevance", "modality_class", "status_group", "phase"], as_index=False)
        .agg(
            trials=("nct_id", "count"),
            listed_enrollment=("enrollment", "sum"),
            sites=("site_count", "sum"),
            sponsors=("sponsor", pd.Series.nunique),
        )
        .sort_values(["target_lane", "adc_relevance", "trials"], ascending=[True, True, False])
    )


def terminated_watchlist_chart(df: pd.DataFrame) -> go.Figure:
    """Terminated/withdrawn/suspended records, useful as a risk/competition audit."""
    df = _chart_df(df)
    if df.empty or "status_group" not in df.columns:
        return _empty_chart("No terminated/withdrawn/suspended data available.", 340)
    d = df[df["status_group"] == "Terminated / Withdrawn / Suspended"].copy()
    if d.empty:
        return chart_layout(go.Figure(), 340, legend="none")
    d["event_date"] = d["last_update"].fillna(d["completion_date"]).fillna(d["primary_completion_date"]).fillna(d["start_date"])
    d["label"] = d["target_lane"].str.slice(0, 18) + " · " + d["sponsor"].str.slice(0, 22) + " · " + d["nct_id"]
    d = d.sort_values(["event_date", "target_lane"], ascending=[False, True]).head(30)
    fig = px.scatter(
        d,
        x="event_date",
        y="label",
        color="status",
        size="enrollment",
        hover_data=["title", "target_lane", "phase", "modality_class", "adc_relevance", "conditions", "interventions"],
        title="Terminated / Withdrawn / Suspended Watchlist",
    )
    fig.update_xaxes(title="Most relevant registry date available")
    fig.update_yaxes(title="", autorange="reversed")
    return chart_layout(fig, max(400, min(780, 120 + len(d) * 24)), legend="right")

# --- v2.0 overrides / enhanced intelligence charts ---

def _split_signal_rows(df: pd.DataFrame, source_col: str, value_name: str, exclude: set[str] | None = None) -> pd.DataFrame:
    df = _chart_df(df)
    exclude = exclude or set()
    rows = []
    for _, r in df.iterrows():
        vals = [v.strip() for v in str(r.get(source_col, "")).split(",") if v.strip()]
        vals = [v for v in vals if v not in exclude]
        if not vals:
            continue
        for v in vals:
            rows.append({
                "target_lane": r.get("target_lane"),
                value_name: v,
                "nct_id": r.get("nct_id"),
                "enrollment": r.get("enrollment", 0),
                "sponsor": r.get("sponsor"),
                "phase": r.get("phase"),
                "status": r.get("status"),
            })
    return pd.DataFrame(rows)


def line_of_therapy_chart(df: pd.DataFrame) -> go.Figure:
    d = _chart_df(df)
    if d.empty:
        return _empty_chart("No line-of-therapy data available.", 430)
    g = d.groupby(["target_lane", "line_of_therapy"], as_index=False).agg(
        trials=("nct_id", "count"), enrollment=("enrollment", "sum")
    )
    order = [
        "1L / frontline", "2L", "3L", "4L+ / heavily pretreated", "Relapsed / refractory",
        "Multiple LOT signals: 1L / frontline, Relapsed / refractory",
        "Multiple LOT signals: 2L, Relapsed / refractory",
        "Multiple LOT signals: 3L, Relapsed / refractory",
        "Multiple LOT signals: 4L+ / heavily pretreated, Relapsed / refractory",
        "Line not specified in registry text",
    ]
    fig = px.bar(
        g,
        x="trials",
        y="target_lane",
        color="line_of_therapy",
        orientation="h",
        hover_data=["enrollment"],
        category_orders={"line_of_therapy": order},
        title="Line-of-Therapy Signals by Target Lane",
    )
    fig.update_xaxes(title="Studies")
    fig.update_yaxes(title="")
    return chart_layout(fig, 470, legend="right")


def prior_therapy_context_chart(df: pd.DataFrame) -> go.Figure:
    d = _split_signal_rows(
        df,
        "prior_therapy_context",
        "prior_context",
        exclude={"Prior-therapy context not specified"},
    )
    if d.empty:
        fig = go.Figure()
        fig.add_annotation(text="No explicit prior-therapy context detected in available registry text.", x=0.5, y=0.5, showarrow=False, font={"color": "#eaf2ff", "size": 14})
        return chart_layout(fig, 340, legend="none")
    g = d.groupby(["prior_context", "target_lane"], as_index=False).agg(
        trials=("nct_id", "count"), enrollment=("enrollment", "sum")
    )
    fig = px.bar(
        g,
        x="trials",
        y="prior_context",
        color="target_lane",
        orientation="h",
        hover_data=["enrollment"],
        title="Prior-Therapy / Patient-Setting Context",
    )
    fig.update_xaxes(title="Studies")
    fig.update_yaxes(title="")
    return chart_layout(fig, max(430, min(760, 160 + 32 * g["prior_context"].nunique())), legend="right")


def biology_signal_chart(df: pd.DataFrame) -> go.Figure:
    d = _split_signal_rows(
        df,
        "biology_signals",
        "biology_signal",
        exclude={"No target biology signal beyond lane match"},
    )
    if d.empty:
        fig = go.Figure()
        fig.add_annotation(text="No lane-specific biology signals detected beyond the target query match.", x=0.5, y=0.5, showarrow=False, font={"color": "#eaf2ff", "size": 14})
        return chart_layout(fig, 340, legend="none")
    g = d.groupby(["biology_signal", "target_lane"], as_index=False).agg(
        trials=("nct_id", "count"), enrollment=("enrollment", "sum")
    )
    fig = px.bar(
        g,
        x="trials",
        y="biology_signal",
        color="target_lane",
        orientation="h",
        hover_data=["enrollment"],
        title="Target-Specific Biology / Patient-Selection Signals",
    )
    fig.update_xaxes(title="Studies")
    fig.update_yaxes(title="")
    return chart_layout(fig, max(455, min(820, 170 + 32 * g["biology_signal"].nunique())), legend="right")


def partner_agent_chart(df: pd.DataFrame) -> go.Figure:
    """Named agents and explicit target/asset terms by lane.

    v2.1 keeps B7-H4/CDH6 visible by adding lane target/asset terms when no
    external partner is named. This makes the chart honest: it separates
    true partner agents from target/asset evidence without dropping the lane.
    """
    rows = []
    for _, r in df.iterrows():
        lane = r.get("target_lane")
        vals = [v.strip() for v in str(r.get("combo_agents", "")).split(",") if v.strip()]
        vals = [v for v in vals if v != "No named partner agent detected"]
        if not vals:
            if lane == "B7-H4 / VTCN1":
                vals = ["B7-H4 / VTCN1 target or asset signal"]
            elif lane == "CDH6":
                vals = ["CDH6 target or asset signal"]
            elif lane == "Alzheimer's / ApoE4":
                vals = ["ApoE4 / Alzheimer biology signal"]
            elif lane == "Bone / Siglec-15":
                vals = ["Bone / Siglec-15 biology signal"]
            else:
                vals = ["No named partner listed"]
        for v in vals:
            rows.append({
                "target_lane": lane,
                "partner_agent": v,
                "nct_id": r.get("nct_id"),
                "enrollment": r.get("enrollment", 0),
                "sponsor": r.get("sponsor"),
                "phase": r.get("phase"),
                "status": r.get("status"),
            })
    d = pd.DataFrame(rows)
    if d.empty:
        fig = go.Figure()
        fig.add_annotation(text="No partner, asset, or target terms detected in available registry text.", x=0.5, y=0.5, showarrow=False, font={"color": "#eaf2ff", "size": 14})
        return chart_layout(fig, 340, legend="none")
    g = d.groupby(["partner_agent", "target_lane"], as_index=False).agg(
        trials=("nct_id", "count"), enrollment=("enrollment", "sum")
    ).sort_values(["trials", "target_lane"], ascending=[False, True]).head(30)
    fig = px.bar(
        g,
        x="trials",
        y="partner_agent",
        color="target_lane",
        orientation="h",
        hover_data=["enrollment"],
        title="Detected Partner Agents + Target/Asset Signals",
    )
    fig.update_xaxes(title="Studies")
    fig.update_yaxes(title="")
    return chart_layout(fig, max(460, min(900, 160 + 27 * g["partner_agent"].nunique())), legend="right")

def planned_trial_mix_chart(df: pd.DataFrame) -> go.Figure:
    d = df[df.get("is_planned", False)].copy()
    if d.empty:
        fig = go.Figure()
        fig.add_annotation(text="No planned / not-yet-recruiting records captured in the current scan.", x=0.5, y=0.5, showarrow=False, font={"color": "#eaf2ff", "size": 14})
        return chart_layout(fig, 340, legend="none")
    g = d.groupby(["target_lane", "status"], as_index=False).agg(
        trials=("nct_id", "count"), enrollment=("enrollment", "sum")
    )
    fig = px.bar(
        g,
        x="target_lane",
        y="trials",
        color="status",
        hover_data=["enrollment"],
        title="Planned / Not-Yet-Recruiting Records by Lane",
    )
    fig.update_xaxes(title="")
    fig.update_yaxes(title="Studies")
    return chart_layout(fig, 390, legend="right")


def forward_start_chart(planned_start_df: pd.DataFrame) -> go.Figure:
    d = _chart_df(planned_start_df)
    if d.empty:
        return _empty_chart("No planned-start records found in the current registry pull.", 430)
    if d.empty:
        return chart_layout(go.Figure(), 340, legend="none")
    d["event_label"] = d["target_lane"] + " · " + d["sponsor"].str.slice(0, 22) + " · " + d["nct_id"]
    d["start_display"] = d["start_date"].dt.strftime("%b %d, %Y")
    fig = px.scatter(
        d,
        x="start_date",
        y="event_label",
        size="enrollment",
        color="target_lane",
        custom_data=["start_display", "title", "status", "phase", "indication_hint", "modality_class", "line_of_therapy"],
        title="Forward Starts: Trials Expected to Begin",
    )
    fig.update_traces(
        hovertemplate="<b>%{customdata[1]}</b><br>Start: %{customdata[0]}<br>Status: %{customdata[2]}<br>Phase: %{customdata[3]}<br>Indication: %{customdata[4]}<br>Modality: %{customdata[5]}<br>LOT: %{customdata[6]}<extra></extra>"
    )
    fig.update_yaxes(title="", autorange="reversed")
    fig.update_xaxes(title="Planned / estimated start date", tickformat="%b %Y")
    return chart_layout(fig, max(460, min(860, 160 + len(d) * 24)), legend="right")


def forward_completion_chart(expected_completion_df: pd.DataFrame) -> go.Figure:
    d = _chart_df(expected_completion_df)
    if d.empty:
        return _empty_chart("No expected-completion records found in the current registry pull.", 430)
    if d.empty:
        return chart_layout(go.Figure(), 340, legend="none")
    d["event_label"] = d["target_lane"] + " · " + d["sponsor"].str.slice(0, 22) + " · " + d["nct_id"]
    d["completion_display"] = d["primary_completion_date"].dt.strftime("%b %d, %Y")
    fig = px.scatter(
        d,
        x="primary_completion_date",
        y="event_label",
        size="enrollment",
        color="phase",
        custom_data=["completion_display", "title", "status", "target_lane", "indication_hint", "combo_category", "line_of_therapy"],
        title="Forward Completions: Primary Completion Windows",
    )
    fig.update_traces(
        hovertemplate="<b>%{customdata[1]}</b><br>Primary completion: %{customdata[0]}<br>Status: %{customdata[2]}<br>Lane: %{customdata[3]}<br>Indication: %{customdata[4]}<br>Therapy context: %{customdata[5]}<br>LOT: %{customdata[6]}<extra></extra>"
    )
    fig.update_yaxes(title="", autorange="reversed")
    fig.update_xaxes(title="Primary completion date", tickformat="%b %Y")
    # Keep the legend below the plotting area. In the two-column catalyst
    # layout a right-side legend can sit on top of the date markers.
    return chart_layout(fig, max(560, min(940, 230 + len(d) * 24)), legend="bottom_roomy")
