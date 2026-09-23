import streamlit as st
import pandas as pd
import plotly.express as px

from modules.pdf_processor import extract_text_from_pdf
from modules.paper_metadata import extract_metadata
from modules.topic_model import detect_topics
from modules.method_detector import detect_methods
from modules.similarity import compare_papers
from modules.gap_detector import (
    detect_gap_signals,
    compare_gap_signals
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="GAPNOVA | Research Intelligence",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# GAPNOVA 2.0 — FUTURISTIC AI THEME
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       GLOBAL BACKGROUND
       ===================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 5% 5%,
                rgba(124, 58, 237, 0.18),
                transparent 25%
            ),
            radial-gradient(
                circle at 95% 10%,
                rgba(34, 211, 238, 0.12),
                transparent 25%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(168, 85, 247, 0.10),
                transparent 30%
            ),
            #070910;
    }


    /* =====================================================
       ANIMATED BACKGROUND GLOW
       ===================================================== */

    .stApp::before {
        content: "";

        position: fixed;

        width: 450px;
        height: 450px;

        top: 15%;
        right: 5%;

        background:
            radial-gradient(
                circle,
                rgba(124, 58, 237, 0.08),
                transparent 70%
            );

        filter: blur(30px);

        animation:
            novaFloat 8s ease-in-out infinite alternate;

        pointer-events: none;

        z-index: 0;
    }


    @keyframes novaFloat {

        from {
            transform:
                translate(0px, 0px);
        }

        to {
            transform:
                translate(-80px, 50px);
        }

    }


    /* =====================================================
       MAIN CONTENT
       ===================================================== */

    .block-container {

        max-width: 1250px;

        padding-top: 2.5rem;

        padding-bottom: 3rem;

    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #10121c 0%,
                #080a11 100%
            );

        border-right:
            1px solid
            rgba(139, 92, 246, 0.20);

    }


    section[data-testid="stSidebar"] > div {

        padding-top: 1.5rem;

    }


    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {

        color: #f5f3ff;

    }


    section[data-testid="stSidebar"] label {

        color:
            #b8b9c8 !important;

    }


    /* =====================================================
       MAIN TITLE
       ===================================================== */

    .main-title {

        font-size: 58px;

        font-weight: 900;

        letter-spacing: -3px;

        line-height: 1;

        margin-bottom: 8px;

        background:
            linear-gradient(
                90deg,
                #ffffff 0%,
                #c4b5fd 35%,
                #a78bfa 65%,
                #67e8f9 100%
            );

        -webkit-background-clip: text;

        -webkit-text-fill-color: transparent;

        filter:
            drop-shadow(
                0 0 20px
                rgba(139, 92, 246, 0.18)
            );

    }


    .subtitle {

        font-size: 16px;

        color:
            #8f94aa;

        margin-bottom:
            20px;

    }


    /* =====================================================
       LIVE STATUS
       ===================================================== */

    .live-status {

        display:
            inline-flex;

        align-items:
            center;

        gap:
            8px;

        padding:
            7px 13px;

        border-radius:
            30px;

        background:
            rgba(34, 197, 94, 0.08);

        border:
            1px solid
            rgba(34, 197, 94, 0.25);

        color:
            #86efac;

        font-size:
            12px;

        font-weight:
            700;

        letter-spacing:
            1px;

        margin-bottom:
            22px;

    }


    .live-dot {

        width:
            8px;

        height:
            8px;

        background:
            #4ade80;

        border-radius:
            50%;

        box-shadow:
            0 0 10px
            rgba(74, 222, 128, 0.9);

        animation:
            pulseLive 1.5s infinite;

    }


    @keyframes pulseLive {

        0% {
            opacity: 1;
            transform: scale(1);
        }

        50% {
            opacity: 0.45;
            transform: scale(0.75);
        }

        100% {
            opacity: 1;
            transform: scale(1);
        }

    }


    /* =====================================================
       HERO CARD
       ===================================================== */

    .hero-card {

        position:
            relative;

        padding:
            27px 30px;

        margin:
            5px 0 35px;

        border-radius:
            22px;

        background:
            linear-gradient(
                135deg,
                rgba(124, 58, 237, 0.16),
                rgba(34, 211, 238, 0.07)
            );

        border:
            1px solid
            rgba(139, 92, 246, 0.28);

        box-shadow:
            0 15px 45px
            rgba(0, 0, 0, 0.25);

        overflow:
            hidden;

    }


    .hero-card::after {

        content:
            "";

        position:
            absolute;

        width:
            220px;

        height:
            220px;

        right:
            -70px;

        top:
            -100px;

        border-radius:
            50%;

        background:
            radial-gradient(
                circle,
                rgba(103, 232, 249, 0.18),
                transparent 70%
            );

    }


    .hero-title {

        font-size:
            22px;

        font-weight:
            750;

        color:
            #ffffff;

        margin-bottom:
            8px;

    }


    .hero-text {

        color:
            #a5a8bb;

        font-size:
            14px;

        max-width:
            800px;

        line-height:
            1.7;

    }


    /* =====================================================
       ANALYSIS ENGINE STATUS
       ===================================================== */

    .engine-status {

        margin-top:
            24px;

        padding:
            18px 22px;

        border-radius:
            16px;

        background:
            linear-gradient(
                135deg,
                rgba(18, 20, 31, 0.90),
                rgba(12, 14, 24, 0.90)
            );

        border:
            1px solid
            rgba(139, 92, 246, 0.22);

        box-shadow:
            0 10px 30px
            rgba(0, 0, 0, 0.18);

    }


    .engine-label {

        color:
            #8f94aa;

        font-size:
            11px;

        letter-spacing:
            1.5px;

        text-transform:
            uppercase;

        margin-bottom:
            8px;

    }


    .engine-active {

        color:
            #86efac;

        font-size:
            14px;

        font-weight:
            700;

        display:
            flex;

        align-items:
            center;

        gap:
            8px;

    }


    .engine-dot {

        width:
            8px;

        height:
            8px;

        border-radius:
            50%;

        background:
            #4ade80;

        box-shadow:
            0 0 10px
            rgba(74, 222, 128, 0.8);

        animation:
            pulseLive 1.5s infinite;

    }


    /* =====================================================
       SECTION TITLES
       ===================================================== */

    .section-title {

        font-size:
            30px;

        font-weight:
            800;

        color:
            #f8f7ff;

        margin-top:
            10px;

        margin-bottom:
            22px;

    }


    h1,
    h2,
    h3 {

        color:
            #f8f7ff !important;

    }


    h4 {

        color:
            #d9d7e8 !important;

    }


    /* =====================================================
       METRIC CARDS
       ===================================================== */

    div[data-testid="stMetric"] {

        background:
            linear-gradient(
                145deg,
                rgba(22, 24, 38, 0.96),
                rgba(10, 12, 20, 0.96)
            );

        border:
            1px solid
            rgba(139, 92, 246, 0.22);

        border-radius:
            20px;

        padding:
            22px;

        min-height:
            125px;

        box-shadow:
            0 12px 35px
            rgba(0, 0, 0, 0.25);

        transition:
            all 0.25s ease;

    }


    div[data-testid="stMetric"]:hover {

        transform:
            translateY(-6px);

        border-color:
            rgba(103, 232, 249, 0.45);

        box-shadow:
            0 15px 40px
            rgba(124, 58, 237, 0.18);

    }


    div[data-testid="stMetricLabel"] {

        color:
            #8f94aa !important;

        font-size:
            13px !important;

    }


    div[data-testid="stMetricValue"] {

        color:
            #ffffff !important;

        font-size:
            36px !important;

        font-weight:
            800 !important;

    }


    /* =====================================================
       BUTTONS
       ===================================================== */

    .stButton > button {

        border:
            1px solid
            rgba(167, 139, 250, 0.45);

        border-radius:
            13px;

        background:
            linear-gradient(
                135deg,
                #6d28d9,
                #8b5cf6
            );

        color:
            #ffffff;

        font-weight:
            700;

        min-height:
            44px;

        box-shadow:
            0 8px 25px
            rgba(124, 58, 237, 0.25);

        transition:
            all 0.2s ease;

    }


    .stButton > button:hover {

        transform:
            translateY(-3px);

        box-shadow:
            0 12px 32px
            rgba(124, 58, 237, 0.45);

        border-color:
            #c4b5fd;

    }


    /* =====================================================
       FILE UPLOADER
       ===================================================== */

    section[data-testid="stFileUploader"] {

        background:
            rgba(18, 20, 31, 0.75);

        border:
            1px dashed
            rgba(139, 92, 246, 0.38);

        border-radius:
            16px;

    }


    section[data-testid="stFileUploader"]:hover {

        border-color:
            rgba(34, 211, 238, 0.55);

    }


    /* =====================================================
       RESEARCH BRIEF
       ===================================================== */

    div[data-testid="stAlert"] {

        background:
            linear-gradient(
                135deg,
                rgba(76, 29, 149, 0.22),
                rgba(8, 145, 178, 0.12)
            );

        border:
            1px solid
            rgba(103, 232, 249, 0.20);

        border-radius:
            18px;

        box-shadow:
            0 10px 30px
            rgba(0, 0, 0, 0.18);

    }


    /* =====================================================
       GAP CARDS
       ===================================================== */

    .gap-card {

        background:
            linear-gradient(
                145deg,
                rgba(23, 25, 39, 0.96),
                rgba(10, 12, 20, 0.96)
            );

        padding:
            23px;

        border-radius:
            19px;

        border:
            1px solid
            rgba(139, 92, 246, 0.20);

        margin-bottom:
            18px;

        box-shadow:
            0 10px 30px
            rgba(0, 0, 0, 0.20);

        transition:
            all 0.25s ease;

    }


    .gap-card:hover {

        transform:
            translateY(-4px);

        border-color:
            rgba(34, 211, 238, 0.42);

    }


    /* =====================================================
       DATAFRAMES
       ===================================================== */

    div[data-testid="stDataFrame"] {

        border-radius:
            16px;

        overflow:
            hidden;

        border:
            1px solid
            rgba(139, 92, 246, 0.20);

    }


    /* =====================================================
       EXPANDERS
       ===================================================== */

    details {

        background:
            rgba(18, 20, 31, 0.70);

        border:
            1px solid
            rgba(139, 92, 246, 0.18);

        border-radius:
            14px;

    }


    details summary {

        color:
            #d8d5e8 !important;

    }


    /* =====================================================
       DIVIDERS
       ===================================================== */

    hr {

        border:
            none !important;

        border-top:
            1px solid
            rgba(139, 92, 246, 0.15)
            !important;

        margin:
            30px 0 !important;

    }


    /* =====================================================
       FOOTER
       ===================================================== */

    .footer {

        text-align:
            center;

        color:
            #666b80;

        font-size:
            12px;

        padding:
            35px 0 10px;

    }


    /* =====================================================
       SCROLLBAR
       ===================================================== */

    ::-webkit-scrollbar {

        width:
            7px;

    }


    ::-webkit-scrollbar-track {

        background:
            #070910;

    }


    ::-webkit-scrollbar-thumb {

        background:
            linear-gradient(
                #6d28d9,
                #0891b2
            );

        border-radius:
            10px;

    }


    ::-webkit-scrollbar-thumb:hover {

        background:
            #a78bfa;

    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "papers" not in st.session_state:
    st.session_state.papers = []

if "gap_signals" not in st.session_state:
    st.session_state.gap_signals = []

if "opportunities" not in st.session_state:
    st.session_state.opportunities = []

if "similarity_results" not in st.session_state:
    st.session_state.similarity_results = []


# =========================================================
# SIDEBAR BRANDING
# =========================================================

st.sidebar.markdown(
    """
    <div style="
        font-size:28px;
        font-weight:900;
        background:
            linear-gradient(
                90deg,
                #ffffff,
                #c4b5fd,
                #67e8f9
            );
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
        margin-bottom:4px;
    ">
        GAPNOVA
    </div>

    <div style="
        font-size:11px;
        color:#74788b;
        letter-spacing:1.5px;
        margin-bottom:28px;
    ">
        RESEARCH INTELLIGENCE
    </div>
    """,
    unsafe_allow_html=True
)


st.sidebar.markdown(
    """
    <div style="
        font-size:11px;
        color:#777b8e;
        text-transform:uppercase;
        letter-spacing:1.4px;
        margin-bottom:8px;
    ">
        Navigation
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# NAVIGATION
# =========================================================

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Literature Explorer",
        "Research Landscape",
        "Gap Finder",
        "Research Opportunities"
    ],
    label_visibility="collapsed"
)


# =========================================================
# PAPER UPLOAD SECTION
# =========================================================

st.sidebar.markdown(
    """
    <div style="
        font-size:11px;
        color:#777b8e;
        text-transform:uppercase;
        letter-spacing:1.4px;
        margin-top:28px;
        margin-bottom:8px;
    ">
        Research Papers
    </div>
    """,
    unsafe_allow_html=True
)


uploaded_files = st.sidebar.file_uploader(
    "Upload Research Papers",
    type=["pdf"],
    accept_multiple_files=True
)


# =========================================================
# ANALYZE BUTTON
# =========================================================

if uploaded_files:

    if st.sidebar.button(
        "⚡ Analyze Papers",
        use_container_width=True
    ):

        papers = []

        with st.spinner(
            "GAPNOVA AI engine is analyzing your literature..."
        ):

            for uploaded_file in uploaded_files:

                # -----------------------------------------
                # PDF TEXT EXTRACTION
                # -----------------------------------------

                text = extract_text_from_pdf(
                    uploaded_file
                )


                # -----------------------------------------
                # METADATA
                # -----------------------------------------

                metadata = extract_metadata(
                    text
                )


                # -----------------------------------------
                # TOPICS
                # -----------------------------------------

                topics = detect_topics(
                    text,
                    metadata["keywords"]
                )


                # -----------------------------------------
                # METHODS
                # -----------------------------------------

                methods = detect_methods(
                    text
                )


                # -----------------------------------------
                # PAPER OBJECT
                # -----------------------------------------

                paper = {

                    "title":
                        metadata["title"],

                    "authors":
                        metadata["authors"],

                    "abstract":
                        metadata["abstract"],

                    "keywords":
                        metadata["keywords"],

                    "topics":
                        topics,

                    "methods":
                        methods,

                    "text":
                        text

                }


                papers.append(
                    paper
                )


            # =============================================
            # STORE PAPERS
            # =============================================

            st.session_state.papers = papers


            # =============================================
            # SIMILARITY
            # =============================================

            if len(papers) >= 2:

                st.session_state.similarity_results = (
                    compare_papers(
                        papers
                    )
                )

            else:

                st.session_state.similarity_results = []


            # =============================================
            # GAP SIGNALS
            # =============================================

            st.session_state.gap_signals = (
                detect_gap_signals(
                    papers
                )
            )


            # =============================================
            # OPPORTUNITIES
            # =============================================

            st.session_state.opportunities = (
                compare_gap_signals(
                    st.session_state.gap_signals
                )
            )


        st.success(
            f"✓ {len(papers)} research paper(s) analyzed successfully!"
        )


# =========================================================
# MAIN HEADER
# =========================================================

st.markdown(
    '<div class="main-title">GAPNOVA</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Research Intelligence · '
    'Discover What Research Hasn’t Yet Answered.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# LIVE AI STATUS
# =========================================================

st.markdown(
    """
    <div class="live-status">
        <span class="live-dot"></span>
        GAPNOVA AI ENGINE · LIVE
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HERO CARD
# =========================================================

st.markdown("## 🔬 Research Intelligence Engine")

st.markdown(
    "GAPNOVA analyzes research literature, maps topics and methodologies, "
    "identifies evidence-based gap signals, and surfaces potential research directions."
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    st.markdown(
        '<div class="section-title">'
        'Research Intelligence'
        '</div>',
        unsafe_allow_html=True
    )


    papers = st.session_state.papers


    # -----------------------------------------------------
    # COUNTS
    # -----------------------------------------------------

    total_topics = len(
        set(
            topic
            for paper in papers
            for topic in paper["topics"]
        )
    )


    total_methods = len(
        set(
            method
            for paper in papers
            for method in paper["methods"]
        )
    )


    total_gaps = len(
        st.session_state.gap_signals
    )


    total_opportunities = len(
        st.session_state.opportunities
    )


    # -----------------------------------------------------
    # METRICS
    # -----------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "📄 Papers",
            len(papers)
        )


    with col2:

        st.metric(
            "🧠 Topics",
            total_topics
        )


    with col3:

        st.metric(
            "🔎 Gap Signals",
            total_gaps
        )


    with col4:

        st.metric(
            "💡 Opportunities",
            total_opportunities
        )


    st.divider()


    # =====================================================
    # RESEARCH BRIEF
    # =====================================================

    if papers:

        st.markdown(
            '<div class="section-title">'
            'Research Brief'
            '</div>',
            unsafe_allow_html=True
        )


        st.info(
            f"GAPNOVA analyzed {len(papers)} research papers "
            f"covering {total_topics} research topics and "
            f"{total_methods} identified methodologies. "
            f"The system detected {total_gaps} potential gap "
            f"signals and generated {total_opportunities} "
            f"possible research directions."
        )


        # -------------------------------------------------
        # ENGINE STATUS
        # -------------------------------------------------

        st.markdown("#### ⚡ ANALYSIS ENGINE")

        st.success("● Literature analysis pipeline active")


# =========================================================
# LITERATURE EXPLORER
# =========================================================

elif page == "Literature Explorer":

    st.markdown(
        '<div class="section-title">'
        '📚 Literature Explorer'
        '</div>',
        unsafe_allow_html=True
    )


    papers = st.session_state.papers


    if not papers:

        st.info(
            "Upload research papers to explore the literature."
        )


    else:

        for i, paper in enumerate(
            papers,
            1
        ):

            st.markdown(
                '<div class="gap-card">',
                unsafe_allow_html=True
            )


            st.subheader(
                f"Paper {i}: {paper['title']}"
            )


            st.write(
                f"**Authors:** "
                f"{paper['authors']}"
            )


            st.write(
                f"**Topics:** "
                f"{', '.join(paper['topics'])}"
            )


            st.write(
                f"**Methods:** "
                f"{', '.join(paper['methods'])}"
            )


            with st.expander(
                "📖 View Abstract"
            ):

                st.write(
                    paper["abstract"]
                )


            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


# =========================================================
# RESEARCH LANDSCAPE
# =========================================================

elif page == "Research Landscape":

    st.markdown(
        '<div class="section-title">'
        '🌐 Research Landscape'
        '</div>',
        unsafe_allow_html=True
    )


    papers = st.session_state.papers


    if not papers:

        st.info(
            "Upload research papers to generate "
            "the research landscape."
        )


    else:

        # =================================================
        # TOPIC DISTRIBUTION
        # =================================================

        st.subheader(
            "📊 Topic Distribution"
        )


        topic_counts = {}


        for paper in papers:

            for topic in paper["topics"]:

                topic_counts[topic] = (
                    topic_counts.get(
                        topic,
                        0
                    ) + 1
                )


        topic_df = pd.DataFrame(
            list(
                topic_counts.items()
            ),
            columns=[
                "Topic",
                "Papers"
            ]
        )


        topic_df = topic_df.sort_values(
            "Papers",
            ascending=False
        ).head(15)


        fig_topics = px.bar(
            topic_df,
            x="Papers",
            y="Topic",
            orientation="h",
            title="Most Common Research Topics",
            template="plotly_dark"
        )


        fig_topics.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#d9d7e8"
            )
        )


        st.plotly_chart(
            fig_topics,
            use_container_width=True
        )


        # =================================================
        # METHOD DISTRIBUTION
        # =================================================

        st.subheader(
            "🧪 Method Distribution"
        )


        method_counts = {}


        for paper in papers:

            for method in paper["methods"]:

                method_counts[method] = (
                    method_counts.get(
                        method,
                        0
                    ) + 1
                )


        method_df = pd.DataFrame(
            list(
                method_counts.items()
            ),
            columns=[
                "Method",
                "Papers"
            ]
        )


        method_df = method_df.sort_values(
            "Papers",
            ascending=False
        )


        fig_methods = px.bar(
            method_df,
            x="Method",
            y="Papers",
            title="Research Method Distribution",
            template="plotly_dark"
        )


        fig_methods.update_layout(
            xaxis_tickangle=-45,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#d9d7e8"
            )
        )


        st.plotly_chart(
            fig_methods,
            use_container_width=True
        )


        # =================================================
        # SHARED RESEARCH AREAS
        # =================================================

        if len(papers) >= 2:

            st.subheader(
                "🔗 Shared Research Areas"
            )


            common_topics = set(
                papers[0]["topics"]
            ).intersection(
                set(
                    papers[1]["topics"]
                )
            )


            if common_topics:

                for topic in sorted(
                    common_topics
                ):

                    st.write(
                        f"• {topic}"
                    )

            else:

                st.info(
                    "No shared topics detected "
                    "between the analyzed papers."
                )


        # =================================================
        # PAPER-SPECIFIC AREAS
        # =================================================

        st.subheader(
            "📌 Paper-Specific Research Areas"
        )


        for i, paper in enumerate(
            papers,
            1
        ):

            st.write(
                f"**Paper {i}:** "
                f"{paper['title']}"
            )


            st.write(
                ", ".join(
                    paper["topics"]
                )
            )


        # =================================================
        # RESEARCH GAP MATRIX
        # =================================================

        st.divider()


        st.subheader(
            "🔬 Research Gap Matrix"
        )


        st.write(
            "GAPNOVA organizes research areas using "
            "evidence from the analyzed literature."
        )


        matrix_rows = []


        all_topics = set()


        for paper in papers:

            all_topics.update(
                paper["topics"]
            )


        for topic in sorted(
            all_topics
        ):

            paper_presence = []


            for paper in papers:

                if topic in paper["topics"]:

                    paper_presence.append(
                        "✓"
                    )

                else:

                    paper_presence.append(
                        "—"
                    )


            if all(
                topic in paper["topics"]
                for paper in papers
            ):

                signal = (
                    "Shared across analyzed papers"
                )

            else:

                signal = (
                    "Paper-specific area"
                )


            matrix_row = {
                "Research Area": topic
            }


            for i, presence in enumerate(
                paper_presence,
                1
            ):

                matrix_row[
                    f"Paper {i}"
                ] = presence


            matrix_row[
                "GAPNOVA Signal"
            ] = signal


            matrix_rows.append(
                matrix_row
            )


        matrix_df = pd.DataFrame(
            matrix_rows
        )


        st.dataframe(
            matrix_df,
            use_container_width=True,
            hide_index=True
        )


        # =================================================
        # EVIDENCE-BASED GAP SIGNALS
        # =================================================

        st.subheader(
            "🎯 Evidence-Based Gap Signals"
        )


        gap_matrix_rows = []


        for gap in (
            st.session_state.gap_signals[:10]
        ):

            gap_matrix_rows.append({

                "Type":
                    gap["type"],

                "Strength":
                    gap["strength"],

                "Supporting Paper":
                    gap["paper"],

                "Evidence":
                    gap["evidence"]

            })


        if gap_matrix_rows:

            gap_matrix_df = pd.DataFrame(
                gap_matrix_rows
            )


            st.dataframe(
                gap_matrix_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No gap signals detected."
            )


# =========================================================
# GAP FINDER
# =========================================================

elif page == "Gap Finder":

    st.markdown(
        '<div class="section-title">'
        '🎯 Top Gap Finder'
        '</div>',
        unsafe_allow_html=True
    )


    gap_signals = (
        st.session_state.gap_signals
    )


    if not gap_signals:

        st.info(
            "Analyze research papers to detect "
            "potential gap signals."
        )


    else:

        high_count = sum(
            1
            for gap in gap_signals
            if gap["strength"] == "High"
        )


        medium_count = sum(
            1
            for gap in gap_signals
            if gap["strength"] == "Medium"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Total Gap Signals",
                len(gap_signals)
            )


        with col2:

            st.metric(
                "High Strength",
                high_count
            )


        with col3:

            st.metric(
                "Medium Strength",
                medium_count
            )


        st.divider()


        # Show strongest six signals
        display_gaps = gap_signals[:6]


        for i, gap in enumerate(
            display_gaps,
            1
        ):

            st.markdown(
                '<div class="gap-card">',
                unsafe_allow_html=True
            )


            st.subheader(
                f"{i}. {gap['type']}"
            )


            st.write(
                f"**Strength:** "
                f"{gap['strength']}"
            )


            st.write(
                f"**Supporting Paper:** "
                f"{gap['paper']}"
            )


            st.write(
                f"**Evidence:** "
                f"{gap['evidence']}"
            )


            st.write(
                f"**Detected Signal:** "
                f"`{gap['keyword']}`"
            )


            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


# =========================================================
# RESEARCH OPPORTUNITIES
# =========================================================

elif page == "Research Opportunities":

    st.markdown(
        '<div class="section-title">'
        '💡 Research Opportunities'
        '</div>',
        unsafe_allow_html=True
    )


    opportunities = (
        st.session_state.opportunities
    )


    if not opportunities:

        st.info(
            "Analyze research papers to generate "
            "possible research directions."
        )


    else:

        st.metric(
            "Potential Research Directions",
            len(opportunities)
        )


        st.divider()


        for i, opportunity in enumerate(
            opportunities,
            1
        ):

            st.markdown(
                '<div class="gap-card">',
                unsafe_allow_html=True
            )


            st.subheader(
                f"{i}. {opportunity['title']}"
            )


            st.write(
                f"**Category:** "
                f"{opportunity['gap_type']}"
            )


            st.write(
                opportunity["description"]
            )


            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">'
    'GAPNOVA · AI-Based Research Gap Detection · '
    'Research Intelligence Platform'
    '</div>',
    unsafe_allow_html=True
)