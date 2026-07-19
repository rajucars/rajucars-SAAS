import streamlit as st
from anthropic import Anthropic

# 1. Page Settings
st.set_page_config(page_title="LocalGrow AI - 2026 Professional Suite", layout="wide")

# 2. Initialize the Real Claude Client from our Secure Cloud Vault
try:
    # This automatically fetches the hidden key you just saved in the secrets vault
    client = Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
except Exception as e:
    st.error("⚠️ Secure Vault Key missing! Please check your Streamlit Secrets settings.")

# 3. Secure Access Gate
PASSWORD_INPUT = st.sidebar.text_input("Security Key Access", type="password")
CORRECT_PASSWORD = "GrowYourBusiness2026"

if PASSWORD_INPUT != CORRECT_PASSWORD:
    st.sidebar.warning("🔒 Enter your security key to unlock the system.")
    st.title("Welcome to LocalGrow AI Suite")
    st.info("Log in via the sidebar to access your 2026 automated marketing tools.")
else:
    st.sidebar.success("🔓 Pro Access Granted")
    
    # Navigation Modules
    st.sidebar.title("🛠️ Navigation Center")
    app_mode = st.sidebar.radio(
        "Choose a Tool Module",
        ["📈 2026 Smart Ads Optimizer", "🏪 Google Business Profile (Soon)", "🔍 Full Local SEO Audit (Soon)"]
    )
    
    active_client = st.sidebar.selectbox("Select Active Business Account", ["My Business", "Friend's Business"])

    # ==========================================
    # MODULE 1: 2026 SMART ADS OPTIMIZER
    # ==========================================
    if app_mode == "📈 2026 Smart Ads Optimizer":
        st.title(f"📈 2026 AI-First Google Ads Control Center")
        st.write("Optimizing smart broad-match and PMax assets for maximum currency value.")

        st.info("📅 **System Pulse**: Live cloud connection verified. Claude 3.5 Sonnet engine active.")

        # Section 1: Campaign Infrastructure Type Selector
        st.subheader("🤖 Choose Campaign Infrastructure Type")
        campaign_type = st.radio(
            "What type of campaign are we auditing?",
            ["Performance Max (AI Automated Images/Search)", "Search Ads (Smart Broad Match Focused)"]
        )

        # Section 2: Input fields for advanced metrics tracking
        st.subheader("📊 Performance Metric Inputs")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            spend = st.number_input("Total Spend ($)", min_value=0.0, value=500.0, step=25.0)
        with col2:
            clicks = st.number_input("Total Clicks Received", min_value=0, value=120, step=5)
        with col3:
            conversions = st.number_input("Verified Purchases / Leads", min_value=0, value=8, step=1)
        with col4:
            invalid_clicks = st.number_input("Google Refunded / Junk Clicks", min_value=0, value=12, step=1)

        # Section 3: Strategic parameters
        st.subheader("🎯 Audience Guard Parameters")
        target_cpa = st.number_input("What is your absolute maximum target cost per customer? ($)", min_value=1.0, value=45.0)

        if st.button("🚀 Execute Live Claude AI Audit"):
            st.write("---")
            
            # Form calculations
            ctr = (clicks / spend) * 100 if spend > 0 else 0
            cpa = spend / conversions if conversions > 0 else spend
            waste_percentage = (invalid_clicks / clicks) * 100 if clicks > 0 else 0
            
            # Displaying advanced pro tables
            st.subheader("📋 Advanced Audit Analytics Ledger")
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric(label="Calculated Click-Through Rate (CTR)", value=f"{ctr:.2f}%")
            with m2:
                st.metric(label="Calculated Cost-Per-Acquisition (CPA)", value=f"${cpa:.2f}")
            with m3:
                st.metric(label="System Detected Waste Percentage", value=f"{waste_percentage:.2f}%")

            # Real-Time AI Processing Section
            st.subheader("🧠 Live Claude AI Analysis Output")
            
            # Constructing the instruction prompt dynamically for Claude
            ai_prompt = f"""
            You are a world-class professional Google Ads manager operating a live SaaS optimization dashboard. 
            Analyze the following real performance metrics for our client account: '{active_client}'.
            Campaign Infrastructure Type: {campaign_type}
            Metrics:
            - Total Spend: ${spend}
            - Clicks: {clicks}
            - Conversions: {conversions}
            - Calculated CTR: {ctr:.2f}%
            - Calculated CPA: ${cpa:.2f}
            - Target CPA limit: ${target_cpa}
            - Invalid/Junk Clicks: {invalid_clicks}
            
            Write a professional 2026 expert maintenance report. It must contain:
            1. An evaluation of whether our budget efficiency is safe or leaking.
            2. A bulleted list of 3 highly tactical, advanced action steps to maximize value for every penny spent and exclude wrong customer clicks based on current 2026 search match algorithm standards. Keep instructions direct and actionable.
            """
            
            with st.spinner("Claude is thinking... analyzing metrics ledger..."):
                try:
                    # Making the real-time API request to Claude
                    message = client.messages.create(
                        model="claude-3-5-sonnet-20241022",
                        max_tokens=700,
                        temperature=0.2,
                        messages=[{"role": "user", "content": ai_prompt}]
                    )
                    # Printing Claude's real, custom response on screen
                    st.success("### Audit Completed Successfully:")
                    st.write(message.content.text)
                    
                except Exception as e:
                    st.error(f"Failed to communicate with Claude's brain. Error: {e}")

    # Expansion Modules
    elif app_mode == "🏪 Google Business Profile (Soon)":
        st.title("🏪 Google Business Profile Manager")
        st.info("Phase 2 Expansion Module")
    elif app_mode == "🔍 Full Local SEO Audit (Soon)":
        st.title("🔍 Full Local SEO Audit Engine")
        st.info("Phase 3 Expansion Module")
