import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from pathlib import Path
import joblib
import textwrap


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Recovery AI",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
MODEL_PATH = PROJECT_ROOT / "ml" / "recovery_model.pkl"
STRATEGY_FILE = DATA_DIR / "strategy_analysis.csv"

API_URL = "http://127.0.0.1:8000/predict"


# ============================================================
# REQUIRED CSV COLUMNS
# ============================================================

REQUIRED_COLUMNS = [
    "transaction_id",
    "customer_id",
    "amount",
    "payment_method",
    "failure_reason",
    "customer_lifetime_value",
    "successful_payments",
    "failed_payments",
    "previous_recovery_rate",
    "hour_of_day",
    "days_since_last_payment",
    "subscription_status",
    "checkout_abandoned",
    "retry_count",
    "recovered",
]


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(textwrap.dedent(
    """
    <style>

    /* ======================================================
       GLOBAL
       ====================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 0%,
                rgba(124, 58, 237, 0.075),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(168, 85, 247, 0.045),
                transparent 30%
            ),
            #080b14;
        color: #f8fafc;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    /* ======================================================
       SIDEBAR
       ====================================================== */

    [data-testid="stSidebar"] {
        background: #0d111c;
        border-right: 1px solid rgba(255,255,255,0.07);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: #f8fafc !important;
    }

    .brand {
        padding: 10px 0 25px 0;
    }

    .brand-title {
        font-size: 25px;
        font-weight: 900;
        letter-spacing: -1px;
        color: #ffffff;
    }

    .brand-title span {
        color: #a855f7;
    }

    .brand-subtitle {
        color: #94a3b8;
        font-size: 12px;
        margin-top: 4px;
    }

    .sidebar-status {
        margin-top: 25px;
        padding: 12px 14px;
        border-radius: 14px;
        background: rgba(34,197,94,0.08);
        border: 1px solid rgba(34,197,94,0.20);
        color: #86efac;
        font-size: 12px;
        font-weight: 700;
    }

    /* ======================================================
       HERO
       ====================================================== */

    .hero {
        padding: 58px 60px;
        margin: 5px 0 40px 0;
        border-radius: 28px;
        background: linear-gradient(135deg, #2a2035 0%, #1b1721 52%, #121116 100%);
        color: white;
        box-shadow:
            0 25px 80px rgba(168,85,247,0.12);
        position: relative;
        overflow: hidden;
    }

    .hero::before {
        content: "";
        position: absolute;
        width: 420px;
        height: 420px;
        right: -130px;
        top: -190px;
        border-radius: 50%;
        background: rgba(255,255,255,0.10);
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 220px;
        height: 220px;
        right: 140px;
        bottom: -150px;
        border-radius: 50%;
        background: rgba(255,255,255,0.06);
    }

    .hero-content {
        position: relative;
        z-index: 2;
    }

    .hero-kicker {
        font-size: 13px;
        font-weight: 900;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        margin-bottom: 18px;
        opacity: 0.90;
    }

    .hero-title {
        font-size: 54px;
        line-height: 1.03;
        font-weight: 900;
        letter-spacing: -2.5px;
        margin-bottom: 22px;
    }

    .hero-title span {
        color: #eadcff;
    }

    .hero-text {
        max-width: 780px;
        font-size: 18px;
        line-height: 1.65;
        opacity: 0.92;
        margin-bottom: 28px;
    }

    .hero-pills {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }

    .pill {
        display: inline-block;
        padding: 9px 15px;
        border-radius: 999px;
        background: rgba(255,255,255,0.13);
        border: 1px solid rgba(255,255,255,0.20);
        font-size: 12px;
        font-weight: 800;
        backdrop-filter: blur(10px);
    }

    .hero-visual {
        position: absolute;
        right: 42px;
        top: 50%;
        transform: translateY(-50%);
        width: 285px;
        padding: 22px;
        border-radius: 22px;
        background: rgba(12, 10, 16, 0.72);
        border: 1px solid rgba(255,255,255,0.10);
        box-shadow: 0 20px 55px rgba(0,0,0,0.25);
        backdrop-filter: blur(18px);
    }

    .visual-head {
        color: rgba(255,255,255,0.65);
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.5px;
    }

    .visual-head span {
        float: right;
        color: #86efac;
        letter-spacing: 0.5px;
    }

    .visual-value {
        margin-top: 14px;
        font-size: 34px;
        font-weight: 900;
        letter-spacing: -1.5px;
    }

    .visual-caption {
        color: rgba(255,255,255,0.58);
        font-size: 11px;
        margin-top: 2px;
    }

    .visual-bars {
        height: 74px;
        display: flex;
        align-items: end;
        gap: 8px;
        margin: 22px 0 14px;
    }

    .visual-bars i {
        display: block;
        flex: 1;
        border-radius: 7px 7px 2px 2px;
        background: linear-gradient(to top, #7c3aed, #c084fc);
        opacity: 0.85;
    }

    .visual-bars i:nth-child(1) { height: 30%; }
    .visual-bars i:nth-child(2) { height: 42%; }
    .visual-bars i:nth-child(3) { height: 36%; }
    .visual-bars i:nth-child(4) { height: 58%; }
    .visual-bars i:nth-child(5) { height: 52%; }
    .visual-bars i:nth-child(6) { height: 78%; }
    .visual-bars i:nth-child(7) { height: 92%; }

    .visual-footer {
        padding-top: 12px;
        border-top: 1px solid rgba(255,255,255,0.08);
        color: rgba(255,255,255,0.68);
        font-size: 11px;
    }

    .visual-footer b {
        float: right;
        color: #c084fc;
        font-size: 14px;
    }

    /* ======================================================
       SECTION HEADERS
       ====================================================== */

    .section-kicker {
        color: #a855f7;
        font-size: 12px;
        font-weight: 900;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }

    .section-title {
        font-size: 28px;
        font-weight: 850;
        letter-spacing: -1px;
        color: #f8fafc;
        margin-bottom: 5px;
    }

    .section-description {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 25px;
    }

    /* ======================================================
       METRIC CARDS
       ====================================================== */

    .metric-card {
        background: linear-gradient(
            145deg,
            rgba(20,27,43,0.96),
            rgba(13,17,28,0.96)
        );
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 20px;
        min-height: 125px;
        box-shadow: 0 12px 35px rgba(0,0,0,0.18);
    }

    .metric-label {
        color: #94a3b8;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .metric-value {
        color: #f8fafc;
        font-size: 29px;
        font-weight: 900;
        letter-spacing: -1px;
    }

    .metric-small {
        color: #64748b;
        font-size: 11px;
        margin-top: 7px;
    }

    /* ======================================================
       CARDS
       ====================================================== */

    .glass-card {
        background: rgba(15,23,42,0.72);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 18px;
    }

    .feature-card {
        background: linear-gradient(
            145deg,
            rgba(124,58,237,0.12),
            rgba(168,85,247,0.035)
        );
        border: 1px solid rgba(168,85,247,0.18);
        border-radius: 18px;
        padding: 22px;
        min-height: 150px;
    }

    .feature-icon {
        font-size: 27px;
        margin-bottom: 10px;
    }

    .feature-title {
        font-size: 16px;
        font-weight: 850;
        color: #f8fafc;
        margin-bottom: 8px;
    }

    .feature-text {
        color: #94a3b8;
        font-size: 13px;
        line-height: 1.55;
    }

    /* ======================================================
       UPLOAD AREA
       ====================================================== */

    [data-testid="stFileUploader"] {
        background: rgba(15,23,42,0.75);
        border: 1px dashed rgba(168,85,247,0.45);
        border-radius: 18px;
        padding: 8px;
    }

    /* ======================================================
       BUTTONS
       ====================================================== */

    .stButton > button {
        border-radius: 12px;
        font-weight: 800;
        min-height: 45px;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 10px 25px rgba(124,58,237,0.20);
    }

    /* ======================================================
       ALERTS
       ====================================================== */

    div[data-testid="stAlert"] {
        border-radius: 14px;
    }

    /* ======================================================
       TABLE
       ====================================================== */

    [data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
    }

    /* ======================================================
       FOOTER
       ====================================================== */

    .footer {
        text-align: center;
        color: #475569;
        font-size: 12px;
        padding: 30px 0 10px 0;
    }

    @media (max-width: 900px) {

        .hero {
            padding: 35px 28px;
        }

        .hero-title {
            font-size: 38px;
        }

        .hero-text {
            font-size: 16px;
        }

        .hero-visual {
            position: relative;
            right: auto;
            top: auto;
            transform: none;
            width: auto;
            margin-top: 26px;
        }

    }

    </style>
    """),
    unsafe_allow_html=True
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def format_crore(value):
    return f"₹{value / 10_000_000:.2f} Cr"


def validate_csv(df):

    return [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]


def analyze_uploaded_data(df):

    try:

        model = joblib.load(MODEL_PATH)

        feature_columns = [
            "amount",
            "payment_method",
            "failure_reason",
            "customer_lifetime_value",
            "successful_payments",
            "failed_payments",
            "previous_recovery_rate",
            "hour_of_day",
            "days_since_last_payment",
            "subscription_status",
            "checkout_abandoned",
            "retry_count",
        ]

        features = df[feature_columns].copy()

        probabilities = model.predict_proba(
            features
        )[:, 1]

        result = df.copy()

        result["recovery_probability"] = probabilities

        result["expected_recovery"] = (
            result["amount"]
            * result["recovery_probability"]
        )

        # ----------------------------------------------------
        # PRIORITY
        # ----------------------------------------------------

        def calculate_priority(probability):

            if probability >= 0.70:
                return "HIGH"

            elif probability >= 0.40:
                return "MEDIUM"

            return "LOW"

        result["priority"] = (
            result["recovery_probability"]
            .apply(calculate_priority)
        )

        # ----------------------------------------------------
        # STRATEGY
        # ----------------------------------------------------

        def determine_strategy(row):

            probability = row["recovery_probability"]

            if row["recovered"] == 1:
                return "NO_ACTION"

            if (
                row["checkout_abandoned"] == 1
                and probability >= 0.40
            ):
                return "SEND_PAYMENT_LINK"

            if (
                probability >= 0.75
                and row["retry_count"] < 3
            ):
                return "RETRY_PAYMENT"

            if probability >= 0.40:
                return "RETRY_LATER"

            return "ESCALATE"

        result["recommended_strategy"] = (
            result.apply(
                determine_strategy,
                axis=1
            )
        )

        # ----------------------------------------------------
        # GUARDRAILS
        # ----------------------------------------------------

        def apply_guardrail(row):

            probability = row["recovery_probability"]

            if row["recovered"] == 1:

                return pd.Series(
                    [
                        False,
                        "NO_ACTION",
                        "SAFE",
                        "Transaction has already been recovered",
                    ]
                )

            if row["retry_count"] >= 3:

                return pd.Series(
                    [
                        False,
                        "ESCALATE",
                        "HIGH",
                        "Maximum retry threshold reached",
                    ]
                )

            if probability < 0.30:

                return pd.Series(
                    [
                        False,
                        "NO_ACTION",
                        "LOW",
                        "Recovery probability is too low",
                    ]
                )

            if (
                row["recommended_strategy"]
                == "RETRY_PAYMENT"
            ):

                return pd.Series(
                    [
                        True,
                        "RETRY_PAYMENT",
                        "MEDIUM",
                        "High recovery probability and retry limit not exceeded",
                    ]
                )

            if (
                row["recommended_strategy"]
                == "SEND_PAYMENT_LINK"
            ):

                return pd.Series(
                    [
                        True,
                        "SEND_PAYMENT_LINK",
                        "LOW",
                        "Payment link recovery is considered low risk",
                    ]
                )

            if (
                row["recommended_strategy"]
                == "RETRY_LATER"
            ):

                return pd.Series(
                    [
                        True,
                        "RETRY_LATER",
                        "LOW",
                        "Recovery opportunity can be revisited later",
                    ]
                )

            return pd.Series(
                [
                    True,
                    "ESCALATE",
                    "HIGH",
                    "Manual intervention recommended",
                ]
            )

        guardrail_results = result.apply(
            apply_guardrail,
            axis=1
        )

        guardrail_results.columns = [
            "action_allowed",
            "final_action",
            "risk_level",
            "guardrail_reason",
        ]

        result = pd.concat(
            [
                result,
                guardrail_results,
            ],
            axis=1
        )

        return result

    except Exception as e:

        st.error(
            f"Could not analyze uploaded data: {e}"
        )

        return None


def predict_transaction(transaction):

    try:

        response = requests.post(
            API_URL,
            json=transaction,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    except requests.exceptions.ConnectionError:

        st.error(
            "Could not connect to FastAPI. "
            "Run: uvicorn api.main:app --reload"
        )

        return None

    except requests.exceptions.RequestException as e:

        st.error(
            f"Prediction API error: {e}"
        )

        return None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html(textwrap.dedent(
        """
        <div class="brand">
            <div class="brand-title">
                💜 Recovery <span>AI</span>
            </div>

            <div class="brand-subtitle">
                Revenue Recovery Intelligence
            </div>
        </div>
        """),
        
    )

    st.markdown("### Navigation")

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Transaction Analysis",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")

    st.html(textwrap.dedent(
        """
        <div class="sidebar-status">
            🟢 ML ENGINE READY
        </div>
        """),
        
    )

    st.caption(
        "AI-powered recovery decisions with bounded actions and safety guardrails."
    )


# ============================================================
# HERO
# ============================================================

st.html(textwrap.dedent(
    """
    <div class="hero">
        <div class="hero-content">

            <div class="hero-kicker">
                ⚡ AI REVENUE RECOVERY PLATFORM
            </div>

            <div class="hero-title">
                Find revenue that's slipping away.<br>
                <span>Win it back.</span>
            </div>

            <div class="hero-text">
                Detect failed payments, estimate recovery probability,
                choose the right intervention, and execute bounded
                recovery workflows with safety guardrails.
            </div>

            <div class="hero-pills">
                <span class="pill">🧠 ML-powered</span>
                <span class="pill">🛡️ Guardrail protected</span>
                <span class="pill">📊 Revenue intelligence</span>
                <span class="pill">⚡ Real-time decisions</span>
            </div>

            <div class="hero-visual">
                <div class="visual-head">RECOVERY SIGNAL <span>● LIVE</span></div>
                <div class="visual-value">₹2.4L</div>
                <div class="visual-caption">expected recoverable revenue</div>
                <div class="visual-bars">
                    <i></i><i></i><i></i><i></i><i></i><i></i><i></i>
                </div>
                <div class="visual-footer">82% recovery confidence <b>↗</b></div>
            </div>

        </div>
    </div>
    """),
    
)


# ============================================================
# DASHBOARD PAGE
# ============================================================

if page == "Dashboard":

    st.html(textwrap.dedent(
        """
        <div class="section-kicker">
            REVENUE INTELLIGENCE
        </div>

        <div class="section-title">
            Recovery command center
        </div>

        <div class="section-description">
            Detect revenue at risk, diagnose failed payments,
            prioritize recovery opportunities, and execute
            bounded recovery workflows.
        </div>
        """),
        
    )

    # ========================================================
    # UPLOAD DATA
    # ========================================================

    st.html(textwrap.dedent(
        """
        <div class="glass-card">

        <div class="section-title">
            📂 Analyze payment data
        </div>

        <div class="section-description">
            Upload failed-payment transactions and let the ML
            engine generate fresh recovery decisions.
        </div>

        </div>
        """),
        
    )

    uploaded_file = st.file_uploader(
        "Upload transaction CSV",
        type=["csv"],
        help="CSV must contain the required transaction columns.",
    )

    if uploaded_file is not None:

        try:

            uploaded_df = pd.read_csv(
                uploaded_file
            )

            missing_columns = validate_csv(
                uploaded_df
            )

            if missing_columns:

                st.error(
                    "Your CSV is missing required columns."
                )

                with st.expander(
                    "View missing columns"
                ):

                    st.write(
                        missing_columns
                    )

            else:

                st.success(
                    f"✓ Dataset loaded successfully — "
                    f"{len(uploaded_df):,} transactions"
                )

                if st.button(
                    "🚀 Analyze Uploaded Dataset",
                    type="primary",
                    use_container_width=True,
                ):

                    with st.spinner(
                        "Running ML recovery analysis..."
                    ):

                        analyzed_df = (
                            analyze_uploaded_data(
                                uploaded_df
                            )
                        )

                    if analyzed_df is not None:

                        st.session_state[
                            "uploaded_analysis"
                        ] = analyzed_df

                        st.success(
                            "Analysis complete."
                        )

                        st.rerun()

        except Exception as e:

            st.error(
                f"Could not read the uploaded CSV: {e}"
            )

    # ========================================================
    # ACTIVE DATASET
    # ========================================================

    active_df = None

    if "uploaded_analysis" in st.session_state:

        active_df = st.session_state[
            "uploaded_analysis"
        ]

        st.info(
            "🟢 Showing results from your uploaded dataset."
        )

    elif STRATEGY_FILE.exists():

        active_df = pd.read_csv(
            STRATEGY_FILE
        )

        st.caption(
            "🔵 Showing the project's demo dataset."
        )

    # ========================================================
    # DASHBOARD
    # ========================================================

    if active_df is not None:

        total_transactions = len(
            active_df
        )

        revenue_at_risk = active_df[
            "amount"
        ].sum()

        expected_recovery = active_df[
            "expected_recovery"
        ].sum()

        high_priority = (
            active_df["priority"]
            == "HIGH"
        ).sum()

        recovery_rate = 0

        if revenue_at_risk > 0:

            recovery_rate = (
                expected_recovery
                / revenue_at_risk
                * 100
            )

        # ====================================================
        # KPI CARDS
        # ====================================================

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.html(textwrap.dedent(
                f"""
                <div class="metric-card">
                    <div class="metric-label">
                        REVENUE AT RISK
                    </div>
                    <div class="metric-value">
                        {format_crore(revenue_at_risk)}
                    </div>
                    <div class="metric-small">
                        Failed payment value
                    </div>
                </div>
                """),
                
            )

        with col2:

            st.html(textwrap.dedent(
                f"""
                <div class="metric-card">
                    <div class="metric-label">
                        EXPECTED RECOVERY
                    </div>
                    <div class="metric-value">
                        {format_crore(expected_recovery)}
                    </div>
                    <div class="metric-small">
                        ML-estimated recoverable value
                    </div>
                </div>
                """),
                
            )

        with col3:

            st.html(textwrap.dedent(
                f"""
                <div class="metric-card">
                    <div class="metric-label">
                        TRANSACTIONS
                    </div>
                    <div class="metric-value">
                        {total_transactions:,}
                    </div>
                    <div class="metric-small">
                        Transactions analyzed
                    </div>
                </div>
                """),
                
            )

        with col4:

            st.html(textwrap.dedent(
                f"""
                <div class="metric-card">
                    <div class="metric-label">
                        HIGH PRIORITY
                    </div>
                    <div class="metric-value">
                        {high_priority:,}
                    </div>
                    <div class="metric-small">
                        Immediate opportunities
                    </div>
                </div>
                """),
                
            )

        st.write("")

        # ====================================================
        # RECOVERY RATE
        # ====================================================

        st.html(textwrap.dedent(
            f"""
            <div class="glass-card">

                <div class="section-kicker">
                    RECOVERY POTENTIAL
                </div>

                <div class="section-title">
                    {recovery_rate:.1f}% of at-risk revenue
                    is currently recoverable
                </div>

                <div class="section-description">
                    Based on the ML model's transaction-level
                    recovery probabilities.
                </div>

            </div>
            """),
            
        )

        # ====================================================
        # FEATURE CARDS
        # ====================================================

        f1, f2, f3 = st.columns(3)

        with f1:

            st.html(textwrap.dedent(
                """
                <div class="feature-card">
                    <div class="feature-icon">🧠</div>
                    <div class="feature-title">
                        ML Recovery Scoring
                    </div>
                    <div class="feature-text">
                        Every failed payment receives a
                        recovery probability based on customer,
                        payment and failure signals.
                    </div>
                </div>
                """),
                
            )

        with f2:

            st.html(textwrap.dedent(
                """
                <div class="feature-card">
                    <div class="feature-icon">🎯</div>
                    <div class="feature-title">
                        Intelligent Intervention
                    </div>
                    <div class="feature-text">
                        The system recommends retry, payment
                        link, retry later, no action or escalation.
                    </div>
                </div>
                """),
                
            )

        with f3:

            st.html(textwrap.dedent(
                """
                <div class="feature-card">
                    <div class="feature-icon">🛡️</div>
                    <div class="feature-title">
                        Safety Guardrails
                    </div>
                    <div class="feature-text">
                        Retry limits, low-probability blocking
                        and escalation rules prevent unsafe
                        recovery actions.
                    </div>
                </div>
                """),
                
            )

        st.write("")

        # ====================================================
        # CHARTS
        # ====================================================

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                "🎯 Priority distribution"
            )

            priority_counts = (
                active_df[
                    "priority"
                ]
                .value_counts()
                .reset_index()
            )

            priority_counts.columns = [
                "priority",
                "count",
            ]

            fig_priority = px.bar(
                priority_counts,
                x="priority",
                y="count",
                text="count",
                title="Transactions by recovery priority",
            )

            fig_priority.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(
                    l=20,
                    r=20,
                    t=50,
                    b=20,
                ),
            )

            st.plotly_chart(
                fig_priority,
                use_container_width=True,
            )

        with col2:

            st.subheader(
                "🧠 Strategy distribution"
            )

            strategy_column = (
                "recommended_strategy"
                if "recommended_strategy"
                in active_df.columns
                else "strategy"
            )

            strategy_counts = (
                active_df[
                    strategy_column
                ]
                .value_counts()
                .reset_index()
            )

            strategy_counts.columns = [
                "strategy",
                "count",
            ]

            fig_strategy = px.bar(
                strategy_counts,
                x="strategy",
                y="count",
                text="count",
                title="Recommended recovery strategies",
            )

            fig_strategy.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(
                    l=20,
                    r=20,
                    t=50,
                    b=20,
                ),
            )

            st.plotly_chart(
                fig_strategy,
                use_container_width=True,
            )

        # ====================================================
        # EXPECTED RECOVERY
        # ====================================================

        st.subheader(
            "💰 Expected recovery by strategy"
        )

        strategy_revenue = (
            active_df
            .groupby(strategy_column)[
                "expected_recovery"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
            .reset_index()
        )

        fig_revenue = px.bar(
            strategy_revenue,
            x=strategy_column,
            y="expected_recovery",
            text_auto=".2s",
            title="Potential revenue recovery",
        )

        fig_revenue.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )

        st.plotly_chart(
            fig_revenue,
            use_container_width=True,
        )

        # ====================================================
        # RECOVERY PROBABILITY
        # ====================================================

        st.subheader(
            "📈 Recovery probability distribution"
        )

        fig_probability = px.histogram(
            active_df,
            x="recovery_probability",
            nbins=20,
            title="ML recovery probability distribution",
        )

        fig_probability.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )

        st.plotly_chart(
            fig_probability,
            use_container_width=True,
        )

        # ====================================================
        # TOP OPPORTUNITIES
        # ====================================================

        st.subheader(
            "🔥 Top recovery opportunities"
        )

        top_opportunities = (
            active_df
            .sort_values(
                "expected_recovery",
                ascending=False,
            )
            .head(10)
            .copy()
        )

        table_columns = [
            "transaction_id",
            "amount",
            "recovery_probability",
            "expected_recovery",
            "priority",
            strategy_column,
        ]

        table_df = top_opportunities[
            table_columns
        ].copy()

        table_df["amount"] = (
            table_df["amount"]
            .apply(
                lambda x:
                f"₹{x:,.2f}"
            )
        )

        table_df[
            "recovery_probability"
        ] = (
            table_df[
                "recovery_probability"
            ]
            .apply(
                lambda x:
                f"{x * 100:.2f}%"
            )
        )

        table_df[
            "expected_recovery"
        ] = (
            table_df[
                "expected_recovery"
            ]
            .apply(
                lambda x:
                f"₹{x:,.2f}"
            )
        )

        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True,
        )

        # ====================================================
        # EXPORT
        # ====================================================

        st.subheader(
            "📥 Export recovery decisions"
        )

        csv_data = (
            active_df
            .to_csv(index=False)
            .encode("utf-8")
        )

        st.download_button(
            label="Download Recovery Analysis CSV",
            data=csv_data,
            file_name="recovery_decisions.csv",
            mime="text/csv",
            use_container_width=True,
        )

    else:

        st.html(textwrap.dedent(
            """
            <div class="glass-card">

                <div class="section-title">
                    👋 Your recovery dashboard is ready
                </div>

                <div class="section-description">
                    Upload a transaction CSV above to generate
                    ML-powered recovery decisions.
                </div>

            </div>
            """),
            
        )


# ============================================================
# INDIVIDUAL TRANSACTION PAGE
# ============================================================

elif page == "Transaction Analysis":

    st.html(textwrap.dedent(
        """
        <div class="section-kicker">
            REAL-TIME DECISION ENGINE
        </div>

        <div class="section-title">
            Analyze one failed payment
        </div>

        <div class="section-description">
            Enter transaction signals and let the ML API
            recommend the safest recovery action.
        </div>
        """),
        
    )

    with st.form(
        "transaction_form"
    ):

        st.subheader(
            "Transaction details"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            transaction_id = st.text_input(
                "Transaction ID",
                value="TEST_001",
            )

            amount = st.number_input(
                "Transaction Amount (₹)",
                min_value=100.0,
                value=20000.0,
                step=500.0,
            )

            payment_method = st.selectbox(
                "Payment Method",
                [
                    "card",
                    "upi",
                    "netbanking",
                    "wallet",
                ],
            )

            failure_reason = st.selectbox(
                "Failure Reason",
                [
                    "network_error",
                    "insufficient_funds",
                    "bank_declined",
                    "timeout",
                    "authentication_failed",
                    "unknown",
                ],
            )

        with col2:

            customer_lifetime_value = (
                st.number_input(
                    "Customer Lifetime Value (₹)",
                    min_value=0.0,
                    value=80000.0,
                    step=5000.0,
                )
            )

            successful_payments = (
                st.number_input(
                    "Successful Payments",
                    min_value=0,
                    value=20,
                )
            )

            failed_payments = (
                st.number_input(
                    "Failed Payments",
                    min_value=0,
                    value=3,
                )
            )

            previous_recovery_rate = (
                st.slider(
                    "Previous Recovery Rate",
                    0.0,
                    1.0,
                    0.65,
                )
            )

        with col3:

            hour_of_day = st.slider(
                "Hour of Day",
                0,
                23,
                14,
            )

            days_since_last_payment = (
                st.number_input(
                    "Days Since Last Payment",
                    min_value=0,
                    value=5,
                )
            )

            subscription_status = (
                st.selectbox(
                    "Subscription Status",
                    [
                        "active",
                        "paused",
                        "cancelled",
                        "expired",
                    ],
                )
            )

            checkout_abandoned = (
                st.selectbox(
                    "Checkout Abandoned",
                    [0, 1],
                )
            )

            retry_count = (
                st.number_input(
                    "Retry Count",
                    min_value=0,
                    max_value=10,
                    value=0,
                )
            )

            recovered = (
                st.selectbox(
                    "Already Recovered",
                    [0, 1],
                )
            )

        submitted = st.form_submit_button(
            "🚀 Analyze Recovery Opportunity",
            type="primary",
            use_container_width=True,
        )

    # ========================================================
    # API PREDICTION
    # ========================================================

    if submitted:

        transaction = {

            "transaction_id": transaction_id,

            "amount": amount,

            "payment_method": payment_method,

            "failure_reason": failure_reason,

            "customer_lifetime_value":
                customer_lifetime_value,

            "successful_payments":
                successful_payments,

            "failed_payments":
                failed_payments,

            "previous_recovery_rate":
                previous_recovery_rate,

            "hour_of_day":
                hour_of_day,

            "days_since_last_payment":
                days_since_last_payment,

            "subscription_status":
                subscription_status,

            "checkout_abandoned":
                checkout_abandoned,

            "retry_count":
                retry_count,

            "recovered":
                recovered,
        }

        with st.spinner(
            "Running AI recovery analysis..."
        ):

            result = predict_transaction(
                transaction
            )

        if result is not None:

            st.session_state[
                "prediction"
            ] = result

    # ========================================================
    # DISPLAY PREDICTION
    # ========================================================

    if "prediction" in st.session_state:

        result = st.session_state[
            "prediction"
        ]

        st.divider()

        st.html(textwrap.dedent(
            """
            <div class="section-kicker">
                AI DECISION
            </div>

            <div class="section-title">
                Recovery recommendation
            </div>
            """),
            
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            probability = result[
                "recovery_probability"
            ]

            st.metric(
                "Recovery Probability",
                f"{probability:.2f}%",
            )

        with col2:

            st.metric(
                "Expected Recovery",
                f"₹{result['expected_recovery']:,.2f}",
            )

        with col3:

            st.metric(
                "Priority",
                result["priority"],
            )

        st.write("")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Recommended Strategy",
                result[
                    "recommended_strategy"
                ],
            )

        with col2:

            st.metric(
                "Final Action",
                result[
                    "final_action"
                ],
            )

        with col3:

            st.metric(
                "Risk Level",
                result[
                    "risk_level"
                ],
            )

        st.write("")

        # ====================================================
        # EXPLANATION
        # ====================================================

        st.subheader(
            "🧠 Why this action?"
        )

        st.info(
            result.get(
                "strategy_reason",
                "The ML engine selected this strategy based on the transaction signals.",
            )
        )

        # ====================================================
        # GUARDRAIL
        # ====================================================

        st.subheader(
            "🛡️ Safety guardrail"
        )

        if result["action_allowed"]:

            st.success(
                "✓ ACTION ALLOWED\n\n"
                + result[
                    "guardrail_reason"
                ]
            )

        else:

            st.error(
                "✕ ACTION BLOCKED\n\n"
                + result[
                    "guardrail_reason"
                ]
            )

        # ====================================================
        # DECISION SUMMARY
        # ====================================================

        st.html(textwrap.dedent(
            f"""
            <div class="glass-card">

                <div class="section-kicker">
                    DECISION SUMMARY
                </div>

                <div class="section-title">
                    {result["final_action"]}
                </div>

                <div class="section-description">
                    The system estimates a
                    <b>{probability:.2f}%</b>
                    recovery probability and recommends
                    <b>{result["final_action"]}</b>
                    with
                    <b>{result["risk_level"]}</b>
                    risk.
                </div>

            </div>
            """),
            
        )


# ============================================================
# FOOTER
# ============================================================

st.html(textwrap.dedent(
    """
    <div class="footer">
        💜 Recovery AI · ML-powered revenue recovery ·
        Bounded actions · Safety-first decisions
    </div>
    """),
    
)