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
        ["📈 Google Ads Quality Check", "🏪 GMB AI Review Replier", "🔍 Website Audit (Soon)"]
    )
    
    active_client = st.sidebar.selectbox("🎯 Target Business:", ["My Business", "Friend's Business"])

    # ==========================================
    # MODULE 1: GOOGLE ADS QUALITY CHECK
    # ==========================================
    if app_mode == "📈 Google Ads Quality Check":
        st.title(f"🚀 Google Ads Optimizer > {active_client}")
        st.write("We scan your ad performance numbers to stop wasted spend and find real buyers.")
        st.write("---")

        st.subheader("📊 Step 1: Drag the sliders to match your business numbers")
        col1, col2, col3 = st.columns(3)
        with col1:
            spend = st.slider("💰 Total Money Spent This Week ($)", min_value=10, max_value=1000, value=200, step=10)
        with col2:
            raw_leads = st.slider("📞 Total Phone Calls / Contacts Received", min_value=1, max_value=50, value=10)
        with col3:
            qualified_leads = st.slider("⭐️ How many of them were Real Buyers?", min_value=0, max_value=50, value=4)

        st.write("---")

        if st.button("🔍 Run My Smart AI Audit"):
            cost_per_buyer = spend / qualified_leads if qualified_leads > 0 else spend
            waste_percentage = ((raw_leads - qualified_leads) / raw_leads) * 100 if raw_leads > 0 else 0
            
            st.subheader("📈 Step 2: Read Your Core Performance Report")
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric(label="💵 Cost for One Real Buyer", value=f"${cost_per_buyer:.2f}")
            with m2:
                st.metric(label="🚦 Total Ad Traffic Health", value="Good Control" if waste_percentage < 50 else "Action Required")
            with m3:
                st.metric(label="💸 Estimated Budget Wasted", value=f"{waste_percentage:.0f}%", delta=f"{'-' if waste_percentage < 50 else '+'} Alert")

            st.write("---")
            st.subheader("🛡️ Step 3: Your Instant 3-Step Action Plan")

            if waste_percentage > 50:
                st.error("⚠️ **AD SPEND WARNING**: More than half of your budget is going to people who aren't buying anything. Your money is leaking!")
            else:
                st.success("✅ **EXCELLENT BUDGET EFFICIENCY**: Your ads are targeted well and your money is well protected!")

            st.info("👉 **Action 1: Block Non-Buyers** — Add 'free', 'cheap', and 'DIY' as negative keywords in your ad panel so casual browsers don't click your link.")
            st.info("👉 **Action 2: Upgrade Your Intake Form** — Add a quick question to your website form asking for their timeline or project type to naturally pre-qualify customers.")
            st.info("👉 **Action 3: Monitor Daily Limits** — Check your daily spending caps every morning to prevent unexpected spikes during off-peak hours.")

    # ==========================================
    # MODULE 2: GMB AI REVIEW REPLIER (UNLOCKED!)
    # ==========================================
    elif app_mode == "🏪 GMB AI Review Replier":
        st.title(f"🏪 GMB AI Review Assistant > {active_client}")
        st.write("Write perfect, professional replies to customer reviews to rank higher on Google Maps.")
        st.write("---")
        
        # Step 1: Input Review Information
        st.subheader("📝 Step 1: Paste Your Customer's Review Below")
        review_text = st.text_area(
            "What did the customer write?",
            value="Great service! They arrived on time, fixed the problem quickly, and were very polite. Highly recommend!"
        )
        
        # Step 2: Select Review Rating
        st.subheader("⭐ Step 2: Select Star Rating")
        star_rating = st.selectbox("How many stars did they give?", ["⭐⭐⭐⭐⭐ (5 Stars)", "⭐⭐⭐⭐ (4 Stars)", "⭐⭐⭐ (3 Stars)", "⭐⭐ (2 Stars)", "⭐ (1 Star)"])
        
        st.write("---")
        
        # Step 3: Trigger Smart Response Generation
        if st.button("✨ Generate My Smart Reply"):
            st.subheader("🤖 Step 3: Copy Your Custom AI Reply Template")
            
            # Smart Local Response Generator Rules based on Star Ratings
            if "5 Stars" in star_rating or "4 Stars" in star_rating:
                st.success("🎉 **POSITIVE REVIEW DETECTED**: Here is a keyword-optimized reply to boost your local SEO.")
                
                # Custom templates tailored to business types
                if active_client == "My Business":
                    reply_output = f"Thank you so much for the wonderful {star_rating[0:5]} review! We take pride in delivering top-notch professional service to our local community. We truly appreciate your support and look forward to helping you again next time!"
                else:
                    reply_output = f"Wow, thank you for the fantastic {star_rating[0:5]} rating! Our team is dedicated to providing an amazing customer experience. We are thrilled to hear you had a great experience, and we look forward to your next visit!"
                    
            elif "3 Stars" in star_rating:
                st.warning("⚠️ **NEUTRAL REVIEW DETECTED**: Professional template to address feedback gracefully.")
                reply_output = "Thank you for sharing your valuable feedback with us. We always strive to provide the best experience possible, and we would appreciate the opportunity to learn how we can earn those extra stars next time. Please reach out to our team directly so we can make things right."
                
            else:
                st.error("🚨 **NEGATIVE REVIEW ALERT**: High-priority polite template to handle complaints safely.")
                reply_output = "Hello. We are deeply sorry to hear that your experience did not meet your expectations. We take customer satisfaction very seriously and want to investigate this issue immediately. Please contact our manager directly at our main office so we can resolve this matter for you as quickly as possible."
                
            # Render the final reply box for easy copy-pasting
            st.info(f"📋 **Draft Response Ready for Copying:**")
            st.code(reply_output, language="text")
            st.write("💡 *Tip: Copy this text and paste it right into your real Google Business Profile dashboard response section!*")

    # ==========================================
    # MODULE 3: FUTURE EXPANSION SLOT
    # ==========================================
    elif app_mode == "🔍 Website Audit (Soon)":
        st.title("🔍 Local SEO Explorer")
        st.info("Coming soon in Phase 3: Simple maps checker and site page optimization logs.")
