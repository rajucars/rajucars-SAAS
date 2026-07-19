import streamlit as st
import random

# 1. Page Configuration
st.set_page_config(page_title="LocalGrow AI - 2026 SERP Suite", layout="wide")

# 2. Secure Gate Login
PASSWORD_INPUT = st.sidebar.text_input("🔑 Enter Secret Access Key", type="password")
CORRECT_PASSWORD = "GrowYourBusiness2026"

if PASSWORD_INPUT != CORRECT_PASSWORD:
    st.sidebar.warning("🔒 App Locked. Please type your password.")
    st.title("🛡️ Welcome to LocalGrow AI")
    st.info("Type your secret password in the left sidebar to unlock your business tools!")
else:
    st.sidebar.success("🔓 App Unlocked!")
    
    # Navigation
    st.sidebar.title("🎛️ App Menu")
    app_mode = st.sidebar.radio(
        "Choose Your Tool:",
        ["🏪 Advanced Dynamic AI Review Engine", "📈 Google Ads Quality Check", "🔍 Website Audit (Soon)"]
    )
    
    active_client = st.sidebar.selectbox("🎯 Target Business:", ["My Business", "Friend's Business"])

    # Core lists of neighborhoods within 25KM radius
    if active_client == "My Business":
        biz_name = "Raju Cars Detailing"
        base_location = "Injambakkam"
        service_focus = "ceramic coating and car scratch removal"
        support_channel = "management@rajucars.com"
        # 25KM radius areas for car business
        all_neighborhoods = ["Thiruvanmiyur", "Sholinganallur", "ECR Road", "Palavakkam", "Neelankarai", "OMR Corridor", "Perungudi", "Kottivakkam", "Akkarai", "Uthandi"]
    else:
        biz_name = "Friend's Premium Bakery"
        base_location = "Adyar"
        service_focus = "custom birthday cakes and sourdough bread"
        support_channel = "orders@premiumbakery.com"
        # 25KM radius areas for bakery business
        all_neighborhoods = ["Besant Nagar", "Mylapore", "Gandhi Nagar", "RA Puram", "Velachery", "T-Nagar", "Kotturpuram", "Alwarpet", "Mandaveli", "Guindy"]

    # ==========================================
    # MODULE: ADVANCED DYNAMIC AI REVIEW ENGINE
    # ==========================================
    if app_mode == "🏪 Advanced Dynamic AI Review Engine":
        st.title("🏪 2026 Real-Time Dynamic Maps SEO Engine")
        st.write("Every click randomly shuffles service roads and areas to stay natural and look human.")
        st.write("---")

        st.subheader("📋 Step 1: Real-Time Review Input Ledger")
        col_name, col_stars = st.columns(2)
        with col_name:
            customer_name = st.text_input("👤 Customer Name:", value="Alex Harrison")
        with col_stars:
            star_rating = st.selectbox("⭐ Review Rating Star Level:", ["⭐⭐⭐⭐⭐ (5-Star Appreciative)", "⭐ (1-Star Complaint)"])

        review_content = st.text_area(
            "💬 Paste the exact text left by the customer:",
            value="Absolutely blown away by the service. They were completely on time and did an amazing job on my vehicle. Will tell all my friends." if "5-Star" in star_rating else "Terrible experience. The communication was bad, they missed my time window, and the quality was poor."
        )

        st.write("---")

        if st.button("⚡ Process Real-Time AI Response"):
            st.subheader("🧠 Step 2: Generated Natural Review Response")
            
            # --- THE GRAY-HAT SHUFFLER LOGIC ---
            # Randomly pick 2 different neighborhoods from our 25KM list every single click
            shuffled_areas = random.sample(all_neighborhoods, 2)
            area_one = shuffled_areas[0]
            area_two = shuffled_areas[1]

            # Randomly switch up the friendly sign-offs to look natural
            good_closings = ["Appreciate you trustin us!", "Thanks for choosing us!", "See you next time buddy", "Glad we could help out!"]
            chosen_closing = random.choice(good_closings)

            if "5-Star" in star_rating:
                st.success("🔥 **DYNAMIC APPRECIATION ENGINE LINKED** — Strategy: Proud customer + randomized 25KM locations.")
                
                # Conversational template with randomized locations and informal lowercase style
                simulated_response = (
                    f"Hi {customer_name}! thanks so much for the awesome words, it honestly makes our whole crew super proud to read this. "
                    f"We love helping out neighbors with premium {service_focus} all across the {base_location} area, and we frequently drive out to clients in nearby spots like {area_one} and {area_two} too. "
                    f"hearing that you want to recommend {biz_name} to your friends is the biggest win we could ask for. {chosen_closing}"
                )
            else:
                st.error("🛡️ **DIPLOMATIC COMPLAINT DAMAGE CONTROL ACTIVE** — Strategy: Move offline + keep brand safe.")
                
                simulated_response = (
                    f"Hello {customer_name}. The management team at {biz_name} takes all operational feedback very seriously. "
                    f"We maintain strict standards for our {service_focus} solutions throughout the {base_location} region, including our surrounding service delivery sectors like {area_one} and {area_two}. "
                    f"We sincerely apologize that your experience did not align with our usual high quality. We want to take full control of this issue and fix it immediately. "
                    f"Please contact our coordinator directly at {support_channel} so we can gather your details and resolve this matter offline."
                )

            st.info("📋 **Live Output (SEO Crawl & SERP Safe Version):**")
            st.code(simulated_response, language="text")
            st.caption("✨ *Notice: Click the button again to see the target neighborhoods and sign-offs change completely at random!*")

    # ==========================================
    # MODULE: GOOGLE ADS QUALITY CHECK
    # ==========================================
    elif app_mode == "📈 Google Ads Quality Check":
        st.title(f"🚀 Google Ads Optimizer > {active_client}")
        st.write("We scan your ad performance numbers to stop wasted spend and find real buyers.")
        st.write("---")

        st.subheader("📊 Drag the sliders to match your business numbers")
        col1, col2, col3 = st.columns(3)
        with col1:
            spend = st.slider("💰 Total Money Spent This Week ($)", min_value=10, max_value=1000, value=200, step=10)
        with col2:
            raw_leads = st.slider("📞 Total Phone Calls / Contacts Received", min_value=1, max_value=50, value=10)
        with col3:
            qualified_leads = st.slider("⭐️ How many of them were Real Buyers?", min_value=0, max_value=50, value=4)

        if st.button("🔍 Run My Smart AI Audit"):
            cost_per_buyer = spend / qualified_leads if qualified_leads > 0 else spend
            waste_percentage = ((raw_leads - qualified_leads) / raw_leads) * 100 if raw_leads > 0 else 0
            
            st.subheader("📈 Core Performance Report")
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric(label="💵 Cost for One Real Buyer", value=f"${cost_per_buyer:.2f}")
            with m2:
                st.metric(label="🚦 Total Ad Traffic Health", value="Good Control" if waste_percentage < 50 else "Action Required")
            with m3:
                st.metric(label="💸 Estimated Budget Wasted", value=f"{waste_percentage:.0f}%")

    # Module 3 Placeholder
    elif app_mode == "🔍 Website Audit (Soon)":
        st.title("🔍 Local SEO Explorer")
        st.info("Coming soon in Phase 3.")
