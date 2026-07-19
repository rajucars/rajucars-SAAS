import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="LocalGrow AI - Simplified Dashboard", layout="wide")

# 2. Easy Access Sidebar Gate
PASSWORD_INPUT = st.sidebar.text_input("🔑 Enter Secret Access Key", type="password")
CORRECT_PASSWORD = "GrowYourBusiness2026"

if PASSWORD_INPUT != CORRECT_PASSWORD:
    st.sidebar.warning("🔒 App Locked. Please type your password.")
    st.title("🛡️ Welcome to LocalGrow AI")
    st.info("Type your secret password in the left sidebar to unlock your business tools!")
else:
    st.sidebar.success("🔓 App Unlocked!")
    
    # Simple Visual Navigation Icons
    st.sidebar.title("🎛️ App Menu")
    app_mode = st.sidebar.radio(
        "Choose Your Tool:",
        ["📈 Google Ads Quality Check", "🏪 Google Business Profile (Soon)", "🔍 Website Audit (Soon)"]
    )
    
    active_client = st.sidebar.selectbox("🎯 Target Business:", ["My Business", "Friend's Business"])

    # ==========================================
    # DESIGNED MODULE: GOOGLE ADS QUALITY CHECK
    # ==========================================
    if app_mode == "📈 Google Ads Quality Check":
        st.title(f"🚀 Google Ads Optimizer > {active_client}")
        st.write("We scan your ad performance numbers to stop wasted spend and find real buyers.")
        st.write("---")

        # Step 1: Simple Slider Inputs
        st.subheader("📊 Step 1: Drag the sliders to match your business numbers")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            spend = st.slider("💰 Total Money Spent This Week ($)", min_value=10, max_value=1000, value=200, step=10)
        with col2:
            raw_leads = st.slider("📞 Total Phone Calls / Contacts Received", min_value=1, max_value=50, value=10)
        with col3:
            qualified_leads = st.slider("⭐️ How many of them were Real Buyers?", min_value=0, max_value=50, value=4)

        st.write("---")

        # Step 2: The Visual Audit Trigger
        if st.button("🔍 Run My Smart AI Audit"):
            
            # Simple Math Backend
            cost_per_buyer = spend / qualified_leads if qualified_leads > 0 else spend
            waste_percentage = ((raw_leads - qualified_leads) / raw_leads) * 100 if raw_leads > 0 else 0
            
            st.subheader("📈 Step 2: Read Your Core Performance Report")
            
            # Large, clean visual summary metrics
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric(label="💵 Cost for One Real Buyer", value=f"${cost_per_buyer:.2f}")
            with m2:
                st.metric(label="🚦 Total Ad Traffic Health", value="Good Control" if waste_percentage < 50 else "Action Required")
            with m3:
                st.metric(label="💸 Estimated Budget Wasted", value=f"{waste_percentage:.0f}%", delta=f"{'-' if waste_percentage < 50 else '+'} Alert")

            st.write("---")
            st.subheader("🛡️ Step 3: Your Instant 3-Step Action Plan")

            # Clean Color-Coded Optimization Flags
            if waste_percentage > 50:
                st.error("⚠️ **AD SPEND WARNING**: More than half of your budget is going to people who aren't buying anything. Your money is leaking!")
            else:
                st.success("✅ **EXCELLENT BUDGET EFFICIENCY**: Your ads are targeted well and your money is well protected!")

            st.info("👉 **Action 1: Block Non-Buyers** — Add 'free', 'cheap', and 'DIY' as negative keywords in your ad panel so casual browsers don't click your link.")
            st.info("👉 **Action 2: Upgrade Your Intake Form** — Add a quick question to your website form asking for their timeline or project type to naturally pre-qualify customers.")
            st.info("👉 **Action 3: Monitor Daily Limits** — Check your daily spending caps every morning to prevent unexpected spikes during off-peak hours.")

    # Simple Placeholders for Next Phases
    elif app_mode == "🏪 Google Business Profile (Soon)":
        st.title("🏪 Google Business Profile Tools")
        st.info("Coming soon in Phase 2: Automated review replies and visual local posts organizer.")
    elif app_mode == "🔍 Website Audit (Soon)":
        st.title("🔍 Local SEO Explorer")
        st.info("Coming soon in Phase 3: Simple maps checker and site page optimization logs.")
