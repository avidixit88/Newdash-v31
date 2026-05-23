# NextCure Signal Room v2.5 UI Cleanup

## v2.5 UI cleanup
- Simplified header to only show NextCure Signal Room.
- Centered the Run Analysis button.
- Removed idle bubble, footer/source clutter, and explanatory subtitles under section titles.
- Reordered sections by executive usefulness.
- Added dark HTML table renderer for evidence/detail tables.
- Darkened select/dropdown styling.
- Moved expected-primary-completion legends below the chart and formatted dates without timestamps.

Run with:
```bash
streamlit run app.py
```

# NextCure Signal Room v2.2

Backend-ready Streamlit rebuild focused on Michael’s actual target lanes:

- B7-H4 / VTCN1
- CDH6
- Alzheimer's / ApoE4
- Bone / Siglec-15

## What changed in v2.2

- Expanded line-of-therapy extraction beyond simple 1L/2L/3L labels.
- Added prior-therapy / patient-setting context: platinum-resistant, prior platinum, taxane, PARP/DDR, VEGF/bevacizumab, checkpoint/IO, and prior ADC exposure.
- Removed the combination extraction confidence chart from the UI because it was not executive-useful.
- Expanded target-specific biology and patient-selection signals.
- Added named partner-agent / biology-term chart.
- Added a planned/not-yet-recruiting registry mix chart and auditable planned-trials table.
- Cleaned forward catalyst date formatting so hover labels and axes do not show `00:00:00`.
- Moved dense legends to the right side of charts where they were crowding titles or dates.
- Preserved the one-button executive flow: `Run Analysis`.
- Preserved backend-ready structure: ingestion, normalization, analytics, charts, UI, config, tests.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Architecture

- `app.py` — Streamlit interface
- `src/clinicaltrials_client.py` — ClinicalTrials.gov API ingestion boundary
- `src/normalization.py` — registry parsing, target-lane classification, phase cleanup, modality classification, therapy-signal extraction
- `src/analytics.py` — analysis bundle and rules-based signal feed
- `src/charts.py` — Plotly visual layer
- `src/ui.py` — reusable Streamlit UI components
- `src/config.py` — lane presets, aliases, classifiers, strategy rules
- `tests/` — sanity checks

Streamlit is the interface, not the brain. These layers can later move behind FastAPI/Postgres without rethinking the product logic.

## Interpretation notes

- **B7-H4 and CDH6** are treated as core oncology/ADC target lanes.
- **Alzheimer's/ApoE4 and Bone/Siglec-15** remain side-channel registry watch lanes and are intentionally excluded from the oncology ADC timeline.
- Line-of-therapy and prior-therapy context are derived from registry text because ClinicalTrials.gov does not provide them as universal structured fields.
- Planned trials are shown two ways: all planned/not-yet-recruiting records, and dated future-start events when the registry provides a future start date.


## v2.2 tightening pass
- Added lane-aware partner/regimen landscape so B7-H4/CDH6 records remain visible even when no named combo partner is listed.
- Added expanded target biology + trial-design signal stack for B7-H4, CDH6, ApoE4/Alzheimer's, and bone/Siglec-15 lanes.
- Kept named partner agents separate from target/asset signals to avoid implying monotherapy records have external partners.
- Preserved backend-ready separation between ingestion, normalization, analytics, charts, and Streamlit UI.


## v2.2 Stability Patch

- Fixed `classify_status_group()` so it always returns a scalar string, not a tuple/dict.
- Added chart dataframe sanitization before groupby operations to prevent pandas hash/type errors from nested registry fields.
- Added empty-state fallbacks for status, modality, sponsor, enrollment, combination, timeline, and catalyst charts.
- Re-ran normalization tests and chart smoke tests across status-heavy charts.

## v2.3 update
- Replaced deprecated `use_container_width` calls with Streamlit `width` arguments.
- Filtered Top Sponsors to ADC-focused B7-H4/CDH6 records.
- Expanded enrollment views by lane/status/enrollment type and patient population/modality.
- Reworked status-by-modality into status by ADC relevance.
- Removed the redundant planned/not-yet-recruiting records-by-lane chart.

## v2.4 Active ADC Robustness Pass

- Top ADC sponsor chart now filters to active B7-H4/CDH6 ADC-confirmed or ADC-watch records only.
- Enrollment section now includes richer chart grouping by lane, status, phase, ADC relevance, and patient population.
- Added enrollment detail tables for lane/status/phase/ADC relevance and patient population/line-of-therapy/prior-treatment context.
- Status by ADC/non-ADC modality now breaks down by lane, ADC relevance, modality class, status, phase, sponsor count, enrollment, and sites.
- Removed the duplicate status-by-modality chart from the top status section and moved the robust version into the ADC modality section where it belongs.
