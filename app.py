import streamlit as st

# 1. Professional Software Page Configuration
st.set_page_config(page_title="LocalGrow AI - Lead Quality Suite", layout="wide")

# 2. Strict Security Access Gate
PASSWORD_INPUT = st.sidebar.text_input("Security Key Access", type="password")
CORRECT_PASSWORD = "GrowYourBusiness2026"

if PASSWORD_INPUT != CORRECT_PASSWORD:
    st.sidebar.warning("🔒 Enter your security key to unlock the system.")
    st.title("Welcome to LocalGrow AI Suite")
    st.info("Log in via the sidebar to access your 2026 automated marketing tools.")
else:
    st.sidebar.success("🔓 Pro Access Granted")
    
    # 3. User-Friendly Navigation Sidebar
    st.sidebar.title("🛠️ Navigation Center")
    app_mode = st.sidebar.radio(
        "Choose a Tool Module",
        ["📈 High-Quality Lead Optimizer", "🏪 Google Business Profile (Soon)", "🔍 Full Local SEO Audit (Soon)"]
    )
    
    active_client = st.sidebar.selectbox("Select Active Business Account", ["My Business", "Friend's Business"])

    # ==========================================
    # MODULE 1: HIGH-QUALITY LEAD OPTIMIZER
    # ==========================================
    if app_mode == "📈 High-Quality Lead Optimizer":
        st.title(f"🎯 High-Quality Lead Optimization Engine")
        st.write("Filter out junk traffic and maximize your value for money on every click.")

        # Real-time System Update Alert Box
        st.info("💡 **Developer Safe-Mode Active**: Running on local simulation engine. No paid API credits required to test!")

        # Layout Section 1: Campaign Strategy Context
        st.subheader("📋 Step 1: Define Your Premium Target Audience")
        target_notes = st.text_input(
            "What type of customer brings you the most profit?",
            value="We want premium clients who pay full price. Avoid people looking for free, cheap, or DIY options."
        )

        # Layout Section 2: User-Friendly Metric Sliders
        st.subheader("📊 Step 2: Input Your Live Performance Numbers")
        col1, col2 = st.columns(2)
        with col1:
            spend = st.number_input("Total Money Spent ($)", min_value=1.0, value=300.0, step=25.0)
            raw_leads = st.number_input("Total Leads Received (Form Fills / Phone Calls)", min_value=1.0, value=15.0, step=1.0)
        with col2:
            qualified_leads = st.number_input("Highly Qualified Leads (Real Buyers Who Answered)", min_value=0.0, value=4.0, step=1.0)
            target_lead_cost = st.number_input("What is your goal cost per qualified customer? ($)", min_value=1.0, value=50.0)

        # Layout Section 3: The Audit Trigger Button
        if st.button("🚀 Run Lead Quality Optimization Audit"):
            st.write("---")
            
            # Smart Local Math Formulas
            conversion_rate = (raw_leads / spend) * 100
            cost_per_raw_lead = spend / raw_leads
            cost_per_qualified_lead = spend / qualified_leads if qualified_leads > 0 else spend
            quality_score = (qualified_leads / raw_leads) * 100 if raw_leads > 0 else 0
            
            # Displaying the clean User Dashboard Performance Metrics Table
            st.subheader("📋 Advanced Quality Ledger Metrics")
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.metric(label="Raw Lead Cost", value=f"${cost_per_raw_lead:.2f}")
            with m2:
                st.metric(label="Real Qualified Cost", value=f"${cost_per_qualified_lead:.2f}")
            with m3:
                st.metric(label="Lead Quality Score", value=f"{quality_score:.2f}%")
            with m4:
                st.metric(label="Budget Waste Estimation", value=f"{100 - quality_score:.2f}%", delta=f"-5% vs last week")

            # Local Simulated Expert Advice Output (Completely Free)
            st.subheader("🛡️ Professional Budget Protection Strategy")
            
            if cost_per_qualified_lead > target_lead_cost:
                st.error(f"⚠️ **BUDGET LEAK DETECTED**: Your real qualified customer cost (${cost_per_qualified_lead:.2f}) is higher than your target (${target_lead_cost:.2f}). You are paying too much for unqualified lookers.")
            else:
                st.success("✅ **MAXIMUM VALUE EFFICIENCY**: Your strategy is attracting premium buyers at a great price. Scale up!")

            st.success("### 📜 2026 Action Plan to Secure Your Money:")
            st.write(f"🛑 **1. Stop Intent Bleeding**: Based on your strategy notes (*'{target_notes}'*), add negative keywords like `['free', 'cheap', 'price list', 'DIY']` to block low-budget traffic immediately.")
            st.write("📋 **2. Upgrade the Lead Capture Forms**: Your lead quality is sitting at a level where adding 1 or 2 mandatory qualifying questions to your business forms (like 'What is your budget size?') will naturally screen out wrong customers before you pay for the click.")
            st.write("🎯 **3. Adjust Google Bidding**: Shift your campaign bid settings from 'Maximize Clicks' to 'Maximize Conversions' to instruct Google's algorithm to hunt for quality over pure volume.")

    # Expansion Modules Placeholders
    elif app_mode == "🏪 Google Business Profile (Soon)":
        st.title("🏪 Google Business Profile Manager")
        st.info("Phase 2 Expansion Module: Auto-Review Reply Integration.")
    elif app_mode == "🔍 Full Local SEO Audit (Soon)":
        st.title("🔍 Full Local SEO Audit Engine")
        st.info("Phase 3 Expansion Module: Citation Tracking.")
