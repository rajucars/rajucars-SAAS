import streamlit as st

# 1. Page Configuration (Makes it look like a clean professional software)
st.set_page_config(page_title="LocalGrow AI - All-in-One Dashboard", layout="wide")

# 2. Strict Security Access Control
PASSWORD_INPUT = st.sidebar.text_input("Security Key Access", type="password")
CORRECT_PASSWORD = "GrowYourBusiness2026" # Change this to your private password

if PASSWORD_INPUT != CORRECT_PASSWORD:
    st.sidebar.warning("🔒 Enter your security key to unlock the system.")
    st.title("Welcome to LocalGrow AI")
    st.info("Please enter your admin credentials in the sidebar to access your client accounts.")
else:
    st.sidebar.success("🔓 System Authenticated")
    
    # 3. Sidebar Navigation Center
    st.sidebar.title("🛠️ Navigation Center")
    app_mode = st.sidebar.radio(
        "Choose a Tool Module",
        ["📈 Google Ads Optimizer", "🏪 Google Business Profile (Soon)", "🔍 Full Local SEO Audit (Soon)"]
    )
    
    # 4. Client Selector (You and your friend)
    st.sidebar.title("👥 Active Client Accounts")
    active_client = st.sidebar.selectbox("Select Account", ["My Business", "Friend's Business"])

    # ==========================================
    # MODULE 1: GOOGLE ADS OPTIMIZER (ACTIVE)
    # ==========================================
    if app_mode == "📈 Google Ads Optimizer":
        st.title(f"📈 Google Ads Engine > {active_client}")
        st.write("Input current ad performance data to receive immediate maintenance tasks.")
        
        # Grid layout for simple data input
        col1, col2, col3 = st.columns(3)
        with col1:
            spend = st.number_input("Total Spend ($)", min_value=0.0, value=250.0, step=10.0)
        with col2:
            clicks = st.number_input("Total Clicks", min_value=0, value=75, step=1)
        with col3:
            conversions = st.number_input("Total Conversions", min_value=0, value=4, step=1)
            
        if st.button("🚀 Analyze with Claude AI"):
            st.write("---")
            # Calculate basic formulas instantly
            ctr = (clicks / spend) * 100 if spend > 0 else 0
            cpa = spend / conversions if conversions > 0 else spend
            
            st.subheader("📊 Performance Summary Table")
            st.metric(label="Calculated Click-Through Rate (CTR)", value=f"{ctr:.2f}%")
            st.metric(label="Cost Per Conversion (CPA)", value=f"${cpa:.2f}")
            
            # Artificial intelligence recommendations placeholder
            st.subheader("🤖 Claude AI Optimization Action Tasks")
            st.success("### Priority Action Checklist:")
            st.write("🟩 **Task 1**: Look through search terms from yesterday. Mark search queries containing 'cheap' or 'free' as negative keywords.")
            st.write("🟩 **Task 2**: Your CTR looks slightly low. Instruct Claude to write three new ad headlines focusing on your 5-star customer reviews.")
            st.write("🟩 **Task 3**: If your conversion count drops lower this week, shift 15% of this budget into your best-performing ad asset group.")

    # ==========================================
    # MODULE 2 & 3: EXPANSION SLOTS (PLACEHOLDERS)
    # ==========================================
    elif app_mode == "🏪 Google Business Profile (Soon)":
        st.title("🏪 Google Business Profile Management")
        st.info("Phase 2 Expansion Module: This section will handle automated review replies and local post generation.")
        
    elif app_mode == "🔍 Full Local SEO Audit (Soon)":
        st.title("🔍 Full Local SEO Audit Engine")
        st.info("Phase 3 Expansion Module: This section will scan site health, local citations, and maps tracking.")
