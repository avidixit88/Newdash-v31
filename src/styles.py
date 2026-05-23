CSS = """
<style>
:root{
  --bg:#070b14;--panel:rgba(14,22,36,.78);--line:rgba(164,183,219,.16);
  --text:#edf4ff;--muted:#9aa8c1;--gold:#d8b86c;--gold2:#b9954c;--cyan:#63d7ff;
}
html,body,[data-testid="stAppViewContainer"]{
  background:
    radial-gradient(circle at 18% -8%,rgba(75,108,255,.14),transparent 29%),
    radial-gradient(circle at 82% -6%,rgba(216,184,108,.11),transparent 26%),
    linear-gradient(180deg,#070b14 0%,#0a1020 46%,#070a12 100%);
  color:var(--text);
}
[data-testid="stHeader"]{background:rgba(8,13,24,0)}
[data-testid="stToolbar"]{display:none}
.block-container{padding-top:1.35rem;padding-bottom:4rem;max-width:1480px}

/* Premium hero: refined signal-room marquee. */
.hero-clean{
  position:relative;display:flex;align-items:center;justify-content:center;
  max-width:1080px;min-height:118px;margin:0 auto 20px auto;
  border-radius:30px;padding:26px 230px 26px 230px;
  background:
    radial-gradient(circle at 18% 0%,rgba(216,184,108,.20),transparent 34%),
    radial-gradient(circle at 82% 8%,rgba(99,215,255,.12),transparent 36%),
    linear-gradient(135deg,rgba(18,29,48,.92),rgba(8,13,24,.96) 52%,rgba(14,23,38,.90));
  box-shadow:
    0 34px 90px rgba(0,0,0,.42),
    inset 0 1px 0 rgba(255,255,255,.10),
    inset 0 -1px 0 rgba(216,184,108,.16);
  overflow:hidden;
}
.hero-clean:before{
  content:"";position:absolute;inset:0;border-radius:30px;padding:1px;
  background:linear-gradient(120deg,rgba(216,184,108,.72),rgba(99,215,255,.14) 42%,rgba(216,184,108,.44));
  -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);
  -webkit-mask-composite:xor;mask-composite:exclude;pointer-events:none;
}
.hero-clean:after{
  content:"";position:absolute;left:18%;right:18%;bottom:0;height:1px;
  background:linear-gradient(90deg,transparent,rgba(216,184,108,.72),rgba(99,215,255,.38),transparent);
  pointer-events:none;
}
.hero-inner{position:relative;z-index:2;text-align:center}
.hero-kicker{
  display:inline-flex;align-items:center;justify-content:center;margin-bottom:8px;
  color:#d8b86c;font-size:.70rem;font-weight:900;letter-spacing:.22em;text-transform:uppercase;
}
.hero-title{
  position:relative;z-index:2;font-size:2.56rem;line-height:1.02;font-weight:900;letter-spacing:-.055em;
  color:#fff;text-align:center;text-shadow:0 18px 38px rgba(0,0,0,.50);
  white-space:nowrap;
}
.hero-accent{
  width:124px;height:3px;border-radius:99px;margin:14px auto 0 auto;
  background:linear-gradient(90deg,transparent,rgba(216,184,108,.95),rgba(99,215,255,.56),transparent);
  box-shadow:0 0 22px rgba(216,184,108,.24);
}
.buildwell-emblem{
  position:absolute;right:28px;top:50%;transform:translateY(-50%);
  width:164px;max-width:18vw;height:auto;z-index:2;
  filter:drop-shadow(0 18px 30px rgba(0,0,0,.46));border:0!important;background:transparent!important;
}

.metric-card{border:1px solid var(--line);background:linear-gradient(180deg,rgba(20,31,51,.82),rgba(12,19,33,.72));border-radius:22px;padding:20px;min-height:112px;box-shadow:0 16px 44px rgba(0,0,0,.23)}
.metric-label{color:var(--muted);text-transform:uppercase;letter-spacing:.12em;font-size:.72rem;font-weight:800}.metric-value{color:#fff;font-size:2.2rem;font-weight:800;letter-spacing:-.04em;margin-top:8px}.metric-note{color:#aab6cc;font-size:.87rem;margin-top:7px;line-height:1.35}
.section-title{margin-top:34px;margin-bottom:16px;font-size:1.28rem;font-weight:850;letter-spacing:-.025em;color:#fff}.section-subtitle{display:none}
.lane-card{border:1px solid var(--line);background:rgba(14,22,36,.62);border-radius:18px;padding:16px;min-height:92px}.lane-title{color:#fff;font-weight:850;font-size:1rem}.lane-metrics{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px}.lane-metrics span{border:1px solid rgba(216,184,108,.18);background:rgba(216,184,108,.055);color:#f2deaa;border-radius:999px;padding:5px 9px;font-size:.76rem}
.signal{border-left:3px solid rgba(99,215,255,.85);background:rgba(99,215,255,.055);border-radius:14px;padding:12px 14px;margin-bottom:10px;color:#dceaff}.signal strong{color:#fff}.caption{display:none}


/* Premium flexible lane picker */
.scan-selector-shell{
  max-width:980px;margin:0 auto 26px auto;text-align:center;border:1px solid rgba(164,183,219,.15);
  border-radius:28px;padding:22px 26px 24px 26px;background:
    radial-gradient(circle at 18% 0%,rgba(99,215,255,.12),transparent 36%),
    radial-gradient(circle at 82% 8%,rgba(216,184,108,.12),transparent 34%),
    linear-gradient(135deg,rgba(15,25,44,.86),rgba(8,13,24,.74));
  box-shadow:0 24px 70px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.08);
}
.scan-selector-kicker{color:#d8b86c;font-size:.66rem;font-weight:900;letter-spacing:.25em;text-transform:uppercase;margin-bottom:7px}
.scan-selector-title{color:#fff;font-size:1.28rem;font-weight:900;letter-spacing:-.035em}
.scan-selector-note{max-width:760px;margin:10px auto 0 auto;color:#a7b4ca;font-size:.93rem;line-height:1.45}
.lane-card-zone{max-width:1180px;margin:0 auto 18px auto;padding:0 10px}.lane-card-zone [data-testid="column"]{padding:0 .35rem!important}
.lane-choice-card{position:relative;min-height:178px;border-radius:18px;padding:22px 24px 20px 24px;overflow:hidden;border:1px solid rgba(164,183,219,.16);background:linear-gradient(145deg,rgba(16,25,45,.86),rgba(7,12,23,.88));box-shadow:0 22px 58px rgba(0,0,0,.24), inset 0 1px 0 rgba(255,255,255,.06);transition:transform .18s ease,border-color .18s ease,box-shadow .18s ease}.lane-choice-card:before{content:"";position:absolute;inset:0;opacity:.45;pointer-events:none}.lane-choice-card.selected{transform:translateY(-1px);box-shadow:0 26px 64px rgba(0,0,0,.30), inset 0 1px 0 rgba(255,255,255,.09)}.lane-choice-card.unselected{opacity:.72}.lane-choice-card.unselected .lane-choice-check{background:rgba(12,19,33,.62)!important;color:#a7b4ca!important;border-color:rgba(164,183,219,.20)!important}.lane-choice-topline{display:flex;align-items:center;justify-content:space-between;margin-bottom:22px}.lane-choice-icon{width:42px;height:42px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-weight:950;letter-spacing:-.04em;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.08);box-shadow:0 10px 24px rgba(0,0,0,.24)}.lane-choice-check{width:36px;height:36px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1rem;font-weight:950;color:#07101e;background:linear-gradient(135deg,#f0d989,#bd984a);border:1px solid rgba(255,230,165,.34);box-shadow:0 10px 26px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.34)}.lane-choice-title{color:#fff;font-size:1.15rem;font-weight:900;letter-spacing:-.03em;line-height:1.15;white-space:normal}.lane-choice-subtitle{color:#bdc8db;font-size:.91rem;line-height:1.35;margin-top:10px}.lane-choice-note{color:#9aa8c1;font-size:.88rem;line-height:1.35;margin-top:4px}.lane-violet{border-color:rgba(160,101,255,.55)}.lane-violet:before{background:radial-gradient(circle at 5% 0%,rgba(160,101,255,.44),transparent 45%)}.lane-violet .lane-choice-icon{color:#caa7ff;box-shadow:0 0 24px rgba(160,101,255,.18)}.lane-blue{border-color:rgba(60,140,255,.58)}.lane-blue:before{background:radial-gradient(circle at 10% 0%,rgba(60,140,255,.44),transparent 45%)}.lane-blue .lane-choice-icon{color:#8cc0ff;box-shadow:0 0 24px rgba(60,140,255,.18)}.lane-green{border-color:rgba(65,207,130,.55)}.lane-green:before{background:radial-gradient(circle at 10% 0%,rgba(65,207,130,.34),transparent 45%)}.lane-green .lane-choice-icon{color:#7cf0ad;box-shadow:0 0 24px rgba(65,207,130,.18)}.lane-gold{border-color:rgba(216,184,108,.62)}.lane-gold:before{background:radial-gradient(circle at 10% 0%,rgba(216,184,108,.32),transparent 45%)}.lane-gold .lane-choice-icon{color:#f0d989;box-shadow:0 0 24px rgba(216,184,108,.18)}
.st-key-lane_toggle_0 button,.st-key-lane_toggle_1 button,.st-key-lane_toggle_2 button,.st-key-lane_toggle_3 button{margin-top:-54px!important;height:54px!important;opacity:0!important;border-radius:18px!important}.st-key-lane_toggle_0,.st-key-lane_toggle_1,.st-key-lane_toggle_2,.st-key-lane_toggle_3{margin-bottom:0!important}.selection-row-wrap{max-width:1180px;margin:4px auto 0 auto}.lane-selection-summary{min-height:56px;border-radius:18px;border:1px solid rgba(164,183,219,.16);background:linear-gradient(135deg,rgba(15,25,44,.78),rgba(8,13,24,.72));display:flex;align-items:center;gap:14px;padding:12px 18px;color:#aebbd0;box-shadow:inset 0 1px 0 rgba(255,255,255,.06)}.lane-selection-summary strong{color:#fff;font-size:1rem;white-space:nowrap}.summary-dot{width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,#8665ff,#4e39bc);color:white;font-weight:950;box-shadow:0 10px 24px rgba(0,0,0,.25)}.st-key-lane_clear_all button{min-height:56px!important;border-radius:16px!important;border:1px solid rgba(255,89,89,.40)!important;background:rgba(255,72,72,.06)!important;color:#ff9a9a!important;font-weight:850!important}.st-key-lane_clear_all button:hover{background:rgba(255,72,72,.10)!important;border-color:rgba(255,120,120,.55)!important;color:#ffc0c0!important}.scan-selector-caption{width:fit-content;max-width:880px;margin:18px auto 22px auto;padding:10px 16px;border-radius:999px;border:1px solid rgba(99,215,255,.18);background:rgba(99,215,255,.06);color:#d7edff;font-size:.84rem;text-align:center;box-shadow:inset 0 1px 0 rgba(255,255,255,.05)}

/* Centered premium action */
.run-button-zone{display:flex;justify-content:center;align-items:center;width:100%;margin:2px auto 34px auto;text-align:center}
.st-key-run_analysis{display:flex!important;justify-content:center!important;align-items:center!important;width:100%!important;margin:0 auto 34px auto!important;text-align:center!important}
.st-key-run_analysis div[data-testid="stButton"]{display:flex!important;justify-content:center!important;width:100%!important;margin:0 auto!important}
.st-key-run_analysis button, div[data-testid="stButton"] button[kind="secondary"]{
  width:190px!important;max-width:190px!important;border-radius:999px!important;min-height:50px!important;
  border:1px solid rgba(216,184,108,.62)!important;
  background:linear-gradient(135deg,rgba(238,211,142,.98),rgba(184,146,67,.98))!important;
  color:#07101e!important;font-weight:900!important;letter-spacing:.01em;
  box-shadow:0 18px 42px rgba(0,0,0,.36), inset 0 1px 0 rgba(255,255,255,.34)!important;
}
.st-key-run_analysis button:hover{border-color:rgba(255,230,165,.92)!important;transform:translateY(-1px);box-shadow:0 22px 52px rgba(0,0,0,.44), inset 0 1px 0 rgba(255,255,255,.40)!important}
.stPlotlyChart{border-radius:22px;overflow:hidden;border:1px solid rgba(164,183,219,.10);background:rgba(7,12,22,.18)}

/* Dark select/dropdown cleanup */
div[data-baseweb="select"]>div, div[data-baseweb="select"] div, div[data-baseweb="input"]>div, input, textarea{
  background-color:rgba(12,19,33,.96)!important;border-color:rgba(164,183,219,.22)!important;color:#edf4ff!important;
}
div[data-baseweb="select"]>div{border-radius:14px!important;box-shadow:none!important}
div[data-baseweb="select"] span, div[data-baseweb="select"] svg, div[data-baseweb="input"] input{color:#edf4ff!important;fill:#edf4ff!important}
div[data-baseweb="popover"], div[data-baseweb="menu"], ul[role="listbox"], div[role="listbox"]{
  background:#0d1526!important;color:#edf4ff!important;border:1px solid rgba(164,183,219,.22)!important;
}
li[role="option"], div[role="option"]{background:#0d1526!important;color:#edf4ff!important}
li[role="option"]:hover, div[role="option"]:hover{background:rgba(99,215,255,.10)!important}
[data-testid="stSelectbox"], [data-testid="stMultiSelect"]{color:#edf4ff!important}

/* Expander cleanup: remove white header bars across Streamlit versions. */
div[data-testid="stExpander"]{border:1px solid rgba(164,183,219,.16)!important;border-radius:16px!important;background:rgba(10,16,28,.42)!important;overflow:hidden!important;box-shadow:none!important}
div[data-testid="stExpander"] details{background:rgba(10,16,28,.42)!important;color:#edf4ff!important}
div[data-testid="stExpander"] details > summary,
div[data-testid="stExpander"] summary,
div[data-testid="stExpander"] summary:hover,
div[data-testid="stExpander"] [data-testid="stExpanderToggleIcon"]{
  background:linear-gradient(90deg,rgba(17,27,46,.98),rgba(12,19,33,.96))!important;color:#edf4ff!important;border-bottom:1px solid rgba(164,183,219,.12)!important;
}
div[data-testid="stExpander"] summary *, div[data-testid="stExpander"] svg{color:#edf4ff!important;fill:#edf4ff!important}
div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p{color:#edf4ff!important}

/* Native dataframe fallback styling */
div[data-testid="stDataFrame"], div[data-testid="stDataFrame"] div{background:rgba(10,16,28,.78)!important;color:#edf4ff!important;border-color:rgba(164,183,219,.16)!important}
div[data-testid="stDataFrame"] *{color:#edf4ff!important}
.dark-table-wrap{overflow:auto;border:1px solid var(--line);border-radius:18px;background:rgba(10,16,28,.78);box-shadow:0 16px 42px rgba(0,0,0,.18);margin-bottom:14px}.dark-data-table{border-collapse:separate;border-spacing:0;width:100%;font-size:.82rem;color:#edf4ff}.dark-data-table thead th{position:sticky;top:0;background:#111b2e;color:#fff;text-align:left;padding:10px 12px;border-bottom:1px solid rgba(164,183,219,.22);white-space:nowrap;z-index:2}.dark-data-table tbody td{padding:9px 12px;border-bottom:1px solid rgba(164,183,219,.10);color:#dce7f7;vertical-align:top;max-width:360px}.dark-data-table tbody tr:nth-child(even){background:rgba(255,255,255,.025)}.dark-data-table tbody tr:hover{background:rgba(99,215,255,.06)}

@media(max-width:900px){
  .hero-clean{min-height:126px;padding:20px 22px;justify-content:center;flex-direction:column;gap:12px}
  .hero-title{font-size:2.08rem;white-space:normal}.buildwell-emblem{position:relative;right:auto;top:auto;transform:none;width:146px;max-width:56vw}.hero-kicker{font-size:.64rem}
}

/* v2.12 BuildWell correction: reliable lane controls, centered summary, no redundant caption. */
.lane-card-zone{max-width:1220px;margin:0 auto 12px auto;padding:0 10px}.lane-card-zone [data-testid="column"]{padding:0 .45rem!important}.lane-choice-card{min-height:184px;margin-bottom:12px}.lane-choice-card.unselected{opacity:.86}.lane-choice-card.unselected .lane-choice-check{background:rgba(12,19,33,.72)!important;color:#a7b4ca!important;border-color:rgba(164,183,219,.28)!important}.lane-choice-title{font-size:1.12rem}.lane-choice-subtitle,.lane-choice-note{overflow:visible;white-space:normal}.st-key-lane_toggle_0 button,.st-key-lane_toggle_1 button,.st-key-lane_toggle_2 button,.st-key-lane_toggle_3 button{margin-top:0!important;height:44px!important;opacity:1!important;border-radius:999px!important;border:1px solid rgba(164,183,219,.20)!important;background:linear-gradient(135deg,rgba(20,32,52,.92),rgba(9,15,27,.90))!important;color:#edf4ff!important;font-weight:850!important;box-shadow:inset 0 1px 0 rgba(255,255,255,.08)!important}.st-key-lane_toggle_0 button:hover,.st-key-lane_toggle_1 button:hover,.st-key-lane_toggle_2 button:hover,.st-key-lane_toggle_3 button:hover{border-color:rgba(216,184,108,.52)!important;background:linear-gradient(135deg,rgba(26,40,64,.94),rgba(12,20,35,.94))!important;transform:translateY(-1px)}.selection-row-wrap{display:none!important}.selection-center-wrap{max-width:960px;margin:22px auto 18px auto;text-align:center}.lane-selection-summary.centered{min-height:54px;border-radius:18px;border:1px solid rgba(164,183,219,.16);background:linear-gradient(135deg,rgba(15,25,44,.80),rgba(8,13,24,.72));display:inline-flex;align-items:center;justify-content:center;gap:14px;padding:12px 20px;color:#aebbd0;box-shadow:inset 0 1px 0 rgba(255,255,255,.06);max-width:900px}.lane-selection-summary.centered strong{color:#fff;font-size:1rem;white-space:nowrap}.st-key-lane_select_all button,.st-key-lane_clear_all button{min-height:44px!important;border-radius:999px!important;font-weight:850!important;background:rgba(12,19,33,.72)!important;color:#dce7f7!important;border:1px solid rgba(164,183,219,.20)!important;box-shadow:inset 0 1px 0 rgba(255,255,255,.06)!important}.st-key-lane_select_all button:hover{border-color:rgba(99,215,255,.42)!important;color:#eff8ff!important;background:rgba(99,215,255,.08)!important}.st-key-lane_clear_all button{border-color:rgba(255,95,95,.30)!important;color:#ffb0b0!important}.st-key-lane_clear_all button:hover{background:rgba(255,72,72,.10)!important;border-color:rgba(255,120,120,.55)!important;color:#ffd0d0!important}.scan-selector-caption{display:none!important}.run-button-zone{margin:12px auto 34px auto}.st-key-run_analysis button{width:220px!important;max-width:220px!important;min-height:54px!important;border-radius:999px!important;border:1px solid rgba(216,184,108,.62)!important;background:linear-gradient(135deg,rgba(238,211,142,.98),rgba(184,146,67,.98))!important;color:#07101e!important;font-weight:900!important;box-shadow:0 18px 42px rgba(0,0,0,.36), inset 0 1px 0 rgba(255,255,255,.34)!important}
@media(max-width:900px){.lane-card-zone{padding:0 2px}.lane-choice-card{min-height:160px}.lane-selection-summary.centered{display:flex;width:100%;font-size:.86rem;align-items:flex-start;text-align:left}.selection-center-wrap{padding:0 8px}.st-key-lane_select_all button,.st-key-lane_clear_all button{margin-top:6px!important}}

/* v2.13 BuildWell refinement: centered compact lane buttons, centered summary, stronger primary CTA. */
.lane-card-zone{
  max-width:1220px!important;
  margin:0 auto 18px auto!important;
  padding:0 10px!important;
}
.lane-card-zone [data-testid="column"]{
  padding:0 .55rem!important;
}
.lane-choice-card{
  min-height:184px!important;
  margin-bottom:12px!important;
}
.st-key-lane_toggle_0,
.st-key-lane_toggle_1,
.st-key-lane_toggle_2,
.st-key-lane_toggle_3{
  display:flex!important;
  justify-content:center!important;
  align-items:center!important;
  width:100%!important;
  margin:0 auto!important;
}
.st-key-lane_toggle_0 div[data-testid="stButton"],
.st-key-lane_toggle_1 div[data-testid="stButton"],
.st-key-lane_toggle_2 div[data-testid="stButton"],
.st-key-lane_toggle_3 div[data-testid="stButton"]{
  display:flex!important;
  justify-content:center!important;
  width:100%!important;
}
.st-key-lane_toggle_0 button,
.st-key-lane_toggle_1 button,
.st-key-lane_toggle_2 button,
.st-key-lane_toggle_3 button{
  width:144px!important;
  max-width:144px!important;
  min-width:144px!important;
  height:38px!important;
  min-height:38px!important;
  margin:0 auto!important;
  border-radius:999px!important;
  border:1px solid rgba(216,184,108,.34)!important;
  background:linear-gradient(135deg,rgba(18,29,48,.92),rgba(8,14,26,.92))!important;
  color:#f1dc9b!important;
  font-size:.84rem!important;
  font-weight:850!important;
  letter-spacing:.005em!important;
  box-shadow:0 10px 26px rgba(0,0,0,.22), inset 0 1px 0 rgba(255,255,255,.07)!important;
}
.st-key-lane_toggle_0 button:hover,
.st-key-lane_toggle_1 button:hover,
.st-key-lane_toggle_2 button:hover,
.st-key-lane_toggle_3 button:hover{
  border-color:rgba(240,217,137,.70)!important;
  background:linear-gradient(135deg,rgba(28,42,66,.96),rgba(12,20,34,.96))!important;
  color:#ffe9aa!important;
  transform:translateY(-1px);
  box-shadow:0 14px 32px rgba(0,0,0,.30), inset 0 1px 0 rgba(255,255,255,.10)!important;
}
.selection-center-wrap{
  display:flex!important;
  justify-content:center!important;
  align-items:center!important;
  max-width:980px!important;
  margin:36px auto 22px auto!important;
  padding:0 12px!important;
  text-align:center!important;
}
.lane-selection-summary.centered{
  display:inline-flex!important;
  justify-content:center!important;
  align-items:center!important;
  width:auto!important;
  max-width:900px!important;
  min-height:54px!important;
  margin:0 auto!important;
  padding:12px 22px!important;
  text-align:center!important;
}
.st-key-lane_select_all,
.st-key-lane_clear_all{
  display:none!important;
}
.run-button-zone{
  display:flex!important;
  justify-content:center!important;
  align-items:center!important;
  width:100%!important;
  margin:28px auto 40px auto!important;
  text-align:center!important;
}
.st-key-run_analysis{
  display:flex!important;
  justify-content:center!important;
  align-items:center!important;
  width:100%!important;
  margin:0 auto!important;
}
.st-key-run_analysis div[data-testid="stButton"]{
  display:flex!important;
  justify-content:center!important;
  align-items:center!important;
  width:100%!important;
}
.st-key-run_analysis button{
  width:292px!important;
  max-width:292px!important;
  min-height:62px!important;
  border-radius:999px!important;
  border:1px solid rgba(255,226,151,.86)!important;
  background:
    radial-gradient(circle at 28% 15%,rgba(255,255,255,.30),transparent 24%),
    linear-gradient(135deg,#f2d98a 0%,#d0a84e 48%,#946b24 100%)!important;
  color:#06101f!important;
  font-size:1.02rem!important;
  font-weight:950!important;
  letter-spacing:.005em!important;
  box-shadow:0 0 0 1px rgba(216,184,108,.18),0 20px 48px rgba(216,184,108,.22),0 24px 58px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,255,255,.45)!important;
}
.st-key-run_analysis button:hover{
  transform:translateY(-2px)!important;
  border-color:rgba(255,239,188,1)!important;
  box-shadow:0 0 0 1px rgba(216,184,108,.25),0 24px 62px rgba(216,184,108,.30),0 28px 68px rgba(0,0,0,.50),inset 0 1px 0 rgba(255,255,255,.55)!important;
}
.st-key-run_analysis button:disabled{
  opacity:.45!important;
  filter:saturate(.62)!important;
  cursor:not-allowed!important;
}
@media(max-width:900px){
  .st-key-lane_toggle_0 button,
  .st-key-lane_toggle_1 button,
  .st-key-lane_toggle_2 button,
  .st-key-lane_toggle_3 button{width:136px!important;max-width:136px!important;min-width:136px!important;height:36px!important;min-height:36px!important;font-size:.80rem!important}
  .selection-center-wrap{margin:24px auto 18px auto!important;padding:0 8px!important}
  .lane-selection-summary.centered{width:100%!important;display:flex!important;text-align:left!important;justify-content:flex-start!important}
  .st-key-run_analysis button{width:260px!important;max-width:260px!important;min-height:58px!important}
}


/* v2.16 BuildWell lane selector correction: CSS stays inside style tag, subtle controls, centered status, premium CTA. */
.lane-card-zone{
  max-width:1230px!important;
  margin:0 auto 12px auto!important;
  padding:0 8px!important;
}
.lane-card-zone [data-testid="column"]{
  padding-left:.55rem!important;
  padding-right:.55rem!important;
}
.lane-choice-card{
  min-height:174px!important;
  padding:22px 24px 20px 24px!important;
  border-radius:20px!important;
  margin-bottom:12px!important;
  background:
    radial-gradient(circle at 12% 0%,rgba(255,255,255,.055),transparent 30%),
    linear-gradient(145deg,rgba(13,23,42,.88),rgba(6,11,21,.94))!important;
  box-shadow:0 22px 54px rgba(0,0,0,.24), inset 0 1px 0 rgba(255,255,255,.065)!important;
}
.lane-choice-card.selected{
  opacity:1!important;
  transform:none!important;
}
.lane-choice-card.unselected{
  opacity:.80!important;
}
.lane-choice-topline{
  margin-bottom:24px!important;
}
.lane-choice-icon{
  width:38px!important;
  height:38px!important;
  border-radius:13px!important;
  background:linear-gradient(135deg,rgba(255,255,255,.07),rgba(255,255,255,.025))!important;
  border:1px solid rgba(255,255,255,.08)!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.07),0 9px 22px rgba(0,0,0,.21)!important;
  font-size:.80rem!important;
}
.lane-choice-check{
  width:auto!important;
  min-width:32px!important;
  height:26px!important;
  padding:0 9px!important;
  border-radius:999px!important;
  font-size:.70rem!important;
  font-weight:900!important;
  letter-spacing:.08em!important;
  color:#08111f!important;
  background:linear-gradient(135deg,rgba(238,215,148,.98),rgba(180,141,57,.98))!important;
  border:1px solid rgba(255,231,164,.30)!important;
  box-shadow:0 8px 18px rgba(0,0,0,.25), inset 0 1px 0 rgba(255,255,255,.34)!important;
}
.lane-choice-card.unselected .lane-choice-check{
  background:rgba(8,14,27,.48)!important;
  border:1px solid rgba(164,183,219,.17)!important;
  color:#79869e!important;
  box-shadow:inset 0 1px 0 rgba(255,255,255,.045)!important;
}
.lane-choice-title{
  font-size:1.10rem!important;
}
.lane-choice-subtitle{
  font-size:.89rem!important;
}
.lane-choice-note{
  font-size:.86rem!important;
}
.st-key-lane_toggle_0,
.st-key-lane_toggle_1,
.st-key-lane_toggle_2,
.st-key-lane_toggle_3{
  display:flex!important;
  justify-content:center!important;
  align-items:center!important;
  width:100%!important;
  margin:0 auto 0 auto!important;
  text-align:center!important;
}
.st-key-lane_toggle_0 div[data-testid="stButton"],
.st-key-lane_toggle_1 div[data-testid="stButton"],
.st-key-lane_toggle_2 div[data-testid="stButton"],
.st-key-lane_toggle_3 div[data-testid="stButton"]{
  display:flex!important;
  justify-content:center!important;
  width:100%!important;
}
.st-key-lane_toggle_0 button,
.st-key-lane_toggle_1 button,
.st-key-lane_toggle_2 button,
.st-key-lane_toggle_3 button{
  width:96px!important;
  max-width:96px!important;
  min-width:96px!important;
  height:28px!important;
  min-height:28px!important;
  padding:0 10px!important;
  margin:0 auto!important;
  border-radius:999px!important;
  border:1px solid rgba(216,184,108,.32)!important;
  background:linear-gradient(135deg,rgba(17,28,47,.78),rgba(7,13,24,.88))!important;
  color:#efd996!important;
  font-size:.70rem!important;
  line-height:1!important;
  font-weight:850!important;
  letter-spacing:.01em!important;
  box-shadow:0 7px 17px rgba(0,0,0,.20), inset 0 1px 0 rgba(255,255,255,.06)!important;
}
.st-key-lane_toggle_0 button:hover,
.st-key-lane_toggle_1 button:hover,
.st-key-lane_toggle_2 button:hover,
.st-key-lane_toggle_3 button:hover{
  border-color:rgba(240,217,137,.58)!important;
  background:linear-gradient(135deg,rgba(28,41,64,.92),rgba(10,17,31,.94))!important;
  color:#fff1bb!important;
  transform:translateY(-1px)!important;
}
.selection-center-wrap{
  width:100%!important;
  margin:32px auto 26px auto!important;
  padding:0!important;
  text-align:center!important;
  display:flex!important;
  justify-content:center!important;
  align-items:center!important;
}
.lane-selection-summary.centered{
  width:fit-content!important;
  max-width:min(850px,88vw)!important;
  min-height:50px!important;
  margin:0 auto!important;
  padding:11px 20px!important;
  display:inline-flex!important;
  justify-content:center!important;
  align-items:center!important;
  gap:13px!important;
  border-radius:999px!important;
  background:linear-gradient(135deg,rgba(15,25,44,.76),rgba(8,13,24,.70))!important;
  border:1px solid rgba(164,183,219,.18)!important;
  box-shadow:0 14px 34px rgba(0,0,0,.20), inset 0 1px 0 rgba(255,255,255,.06)!important;
  text-align:center!important;
}
.lane-selection-summary.centered span:last-child{
  white-space:normal!important;
}
.summary-dot{
  width:25px!important;
  height:25px!important;
  min-width:25px!important;
  background:linear-gradient(135deg,#6f58d9,#4731a7)!important;
  box-shadow:0 8px 20px rgba(0,0,0,.22), inset 0 1px 0 rgba(255,255,255,.18)!important;
}
.run-button-zone{
  display:flex!important;
  justify-content:center!important;
  align-items:center!important;
  width:100%!important;
  margin:26px auto 48px auto!important;
  text-align:center!important;
}
.st-key-run_analysis,
.st-key-run_analysis div[data-testid="stButton"]{
  display:flex!important;
  justify-content:center!important;
  align-items:center!important;
  width:100%!important;
}
.st-key-run_analysis button{
  width:330px!important;
  max-width:330px!important;
  min-height:66px!important;
  border-radius:999px!important;
  border:1px solid rgba(255,229,157,.88)!important;
  background:
    radial-gradient(circle at 30% 18%,rgba(255,255,255,.30),transparent 25%),
    linear-gradient(135deg,#f7dc8b 0%,#d0a34a 48%,#95691f 100%)!important;
  color:#06101f!important;
  font-size:1.04rem!important;
  font-weight:950!important;
  letter-spacing:.005em!important;
  box-shadow:0 0 0 1px rgba(216,184,108,.20),0 18px 44px rgba(216,184,108,.24),0 26px 62px rgba(0,0,0,.48),inset 0 1px 0 rgba(255,255,255,.50)!important;
}
.st-key-run_analysis button:hover{
  transform:translateY(-1px)!important;
  border-color:rgba(255,239,184,.98)!important;
  box-shadow:0 0 0 1px rgba(216,184,108,.28),0 22px 56px rgba(216,184,108,.30),0 30px 68px rgba(0,0,0,.52),inset 0 1px 0 rgba(255,255,255,.58)!important;
}
@media(max-width:900px){
  .lane-choice-card{min-height:156px!important}
  .st-key-lane_toggle_0 button,.st-key-lane_toggle_1 button,.st-key-lane_toggle_2 button,.st-key-lane_toggle_3 button{width:90px!important;min-width:90px!important;height:28px!important;font-size:.68rem!important}
  .lane-selection-summary.centered{max-width:92vw!important;align-items:flex-start!important;text-align:left!important;border-radius:18px!important}
  .st-key-run_analysis button{width:286px!important;max-width:286px!important;min-height:60px!important}
}

</style>
"""
