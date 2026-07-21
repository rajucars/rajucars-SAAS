import hashlib
import hmac
import random
import time
from datetime import date, datetime, timedelta

import pandas as pd
import streamlit as st


# ---------------------------------------------------------------------------
# LocalGrow AI - Streamlit MVP
# Safe MVP for Google Ads, Google Business Profile, website audit,
# content planning, and corrective-action dashboards.
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="LocalGrow AI - Growth Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)


DEMO_SALT = "localgrow-ai-streamlit-mvp"
DEMO_PASSWORD = "ChangeMe2026!"


def hash_password(password: str, salt: str = DEMO_SALT) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        120_000,
    ).hex()


DEFAULT_USERS = {
    "admin@rajucars.com": {
        "name": "Raju Cars Admin",
        "role": "Owner",
        "password_hash": hash_password(DEMO_PASSWORD),
    },
    "manager@rajucars.com": {
        "name": "Store Manager",
        "role": "Manager",
        "password_hash": hash_password(DEMO_PASSWORD),
    },
}


BUSINESS_PROFILES = {
    "Raju Cars - Authorized 3M Car Care": {
        "business_name": "Raju Cars",
        "display_name": "Raju Cars - Authorized 3M Car Care",
        "base_location": "Sholinganallur / OMR-ECR Link Road",
        "support_email": "management@rajucars.com",
        "phone": "7904506926",
        "services": [
            "3M Ceramic Coating",
            "3M Paint Protection Film",
            "3M Sunfilm",
            "Paint correction",
            "Interior protection",
        ],
        "locations": [
            "Sholinganallur",
            "OMR",
            "ECR",
            "Akkarai",
            "Navalur",
            "Medavakkam",
            "Perumbakkam",
            "Siruseri",
            "Thiruvanmiyur",
            "Adyar",
            "Velachery",
        ],
        "competitors": [
            "3M Tiruvanmiyur",
            "3M Thuraipakkam",
            "Detailing Mafia",
            "Turtle Wax",
            "CarSpark",
        ],
    },
    "Friend's Premium Bakery": {
        "business_name": "Friend's Premium Bakery",
        "display_name": "Friend's Premium Bakery",
        "base_location": "Adyar",
        "support_email": "orders@premiumbakery.com",
        "phone": "9000000000",
        "services": [
            "Birthday cakes",
            "Sourdough bread",
            "Dessert boxes",
            "Corporate gifting",
        ],
        "locations": [
            "Adyar",
            "Besant Nagar",
            "Mylapore",
            "RA Puram",
            "Velachery",
            "T-Nagar",
            "Kotturpuram",
            "Alwarpet",
            "Mandaveli",
            "Guindy",
        ],
        "competitors": [
            "The Adyar Cake Studio",
            "Chennai Crust Company",
            "Bespoke Bakes OMR",
        ],
    },
}


GOOGLE_ADS_API_VERSION = "v24"
GOOGLE_ADS_SECRET_KEYS = {
    "developer_token": "GOOGLE_ADS_DEVELOPER_TOKEN",
    "client_id": "GOOGLE_ADS_CLIENT_ID",
    "client_secret": "GOOGLE_ADS_CLIENT_SECRET",
    "refresh_token": "GOOGLE_ADS_REFRESH_TOKEN",
    "customer_id": "GOOGLE_ADS_CUSTOMER_ID",
    "login_customer_id": "GOOGLE_ADS_LOGIN_CUSTOMER_ID",
}


st.markdown(
    """
    <style>
    :root {
        --lg-blue: #1d4ed8;
        --lg-ink: #0f172a;
        --lg-muted: #64748b;
        --lg-line: #e2e8f0;
        --lg-soft: #f8fafc;
        --lg-green: #15803d;
        --lg-amber: #b45309;
        --lg-red: #b91c1c;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    [data-testid="stSidebar"] {
        background: #0f172a;
    }

    [data-testid="stSidebar"] * {
        color: #e5e7eb;
    }

    .app-title {
        font-size: 1.85rem;
        font-weight: 800;
        color: var(--lg-ink);
        margin: 0 0 .25rem;
    }

    .app-subtitle {
        color: var(--lg-muted);
        font-size: .98rem;
        margin-bottom: 1rem;
    }

    .panel {
        border: 1px solid var(--lg-line);
        border-radius: 8px;
        padding: 1rem;
        background: #ffffff;
    }

    .small-label {
        font-size: .78rem;
        text-transform: uppercase;
        letter-spacing: .04em;
        color: var(--lg-muted);
        font-weight: 700;
    }

    .risk-high {
        color: var(--lg-red);
        font-weight: 700;
    }

    .risk-medium {
        color: var(--lg-amber);
        font-weight: 700;
    }

    .risk-low {
        color: var(--lg-green);
        font-weight: 700;
    }

    .security-note {
        border-left: 4px solid var(--lg-blue);
        background: #eff6ff;
        padding: .75rem .9rem;
        border-radius: 6px;
        color: #1e3a8a;
        font-size: .9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def init_state() -> None:
    defaults = {
        "authenticated": False,
        "pending_user": None,
        "user": None,
        "auth_step": "login",
        "two_factor_code": None,
        "two_factor_expiry": 0,
        "reset_email": None,
        "reset_code": None,
        "reset_expiry": 0,
        "session_password_overrides": {},
        "login_events": [],
        "review_replies": {},
        "content_status": {},
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_users() -> dict:
    users = DEFAULT_USERS.copy()
    for email, password_hash in st.session_state.session_password_overrides.items():
        if email in users:
            users[email] = {**users[email], "password_hash": password_hash}
    return users


def add_login_event(event: str, email: str, status: str) -> None:
    st.session_state.login_events.insert(
        0,
        {
            "Time": datetime.now().strftime("%d-%b-%Y %I:%M %p"),
            "Event": event,
            "User": email,
            "Status": status,
        },
    )
    st.session_state.login_events = st.session_state.login_events[:20]


def verify_password(email: str, password: str) -> bool:
    user = get_users().get(email.lower().strip())
    if not user:
        return False
    entered_hash = hash_password(password)
    return hmac.compare_digest(entered_hash, user["password_hash"])


def generate_otp() -> str:
    return str(random.randint(100000, 999999))


def login_screen() -> None:
    st.markdown('<div class="app-title">LocalGrow AI</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-subtitle">Streamlit MVP for Google Ads, Google Business Profile, website audits, content planning and corrective actions.</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.05, 1])
    with left:
        st.subheader("Secure sign in")
        st.caption("Demo users: admin@rajucars.com and manager@rajucars.com")

        email = st.text_input("Email address", value="admin@rajucars.com")
        password = st.text_input("Password", type="password")

        col_a, col_b = st.columns([1, 1])
        with col_a:
            sign_in = st.button("Sign in", type="primary", use_container_width=True)
        with col_b:
            forgot = st.button("Forgot password", use_container_width=True)

        if forgot:
            st.session_state.auth_step = "forgot"
            st.rerun()

        if sign_in:
            clean_email = email.lower().strip()
            if verify_password(clean_email, password):
                st.session_state.pending_user = clean_email
                st.session_state.two_factor_code = generate_otp()
                st.session_state.two_factor_expiry = time.time() + 300
                st.session_state.auth_step = "two_factor"
                add_login_event("Password accepted", clean_email, "2FA pending")
                st.rerun()
            else:
                add_login_event("Password rejected", clean_email, "Failed")
                st.error("Invalid email or password.")

        st.markdown(
            """
            <div class="security-note">
            For quick MVP testing, the temporary password is ChangeMe2026!.
            In production, store users in Supabase/Firebase/Postgres, send OTP by email/SMS,
            and remove all demo credentials from GitHub.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.subheader("MVP modules")
        st.write("1. Google Ads quality dashboard")
        st.write("2. Google Business Profile review reply approval")
        st.write("3. GMB health and profile upkeep audit")
        st.write("4. Website audit and correction tracker")
        st.write("5. Daily content posting planner")
        st.write("6. Owner-friendly corrective action dashboard")


def two_factor_screen() -> None:
    email = st.session_state.pending_user
    st.markdown('<div class="app-title">Two-step verification</div>', unsafe_allow_html=True)
    st.write(f"Enter the 6-digit code for {email}.")

    if time.time() > st.session_state.two_factor_expiry:
        st.warning("The verification code expired. Please sign in again.")
        if st.button("Back to sign in"):
            st.session_state.auth_step = "login"
            st.session_state.pending_user = None
            st.rerun()
        return

    st.info(f"Demo MVP code: {st.session_state.two_factor_code}")
    code = st.text_input("Verification code", max_chars=6)

    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button("Verify and open dashboard", type="primary", use_container_width=True):
            if code.strip() == st.session_state.two_factor_code:
                user = get_users()[email]
                st.session_state.authenticated = True
                st.session_state.user = {
                    "email": email,
                    "name": user["name"],
                    "role": user["role"],
                }
                st.session_state.auth_step = "dashboard"
                add_login_event("Two-step verification", email, "Success")
                st.rerun()
            else:
                add_login_event("Two-step verification", email, "Failed")
                st.error("Incorrect verification code.")
    with col_b:
        if st.button("Cancel", use_container_width=True):
            st.session_state.auth_step = "login"
            st.session_state.pending_user = None
            st.rerun()


def forgot_password_screen() -> None:
    st.markdown('<div class="app-title">Forgot password recovery</div>', unsafe_allow_html=True)

    if st.session_state.reset_email is None:
        email = st.text_input("Registered email address", value="admin@rajucars.com")
        col_a, col_b = st.columns([1, 1])
        with col_a:
            if st.button("Send recovery code", type="primary", use_container_width=True):
                clean_email = email.lower().strip()
                if clean_email in get_users():
                    st.session_state.reset_email = clean_email
                    st.session_state.reset_code = generate_otp()
                    st.session_state.reset_expiry = time.time() + 300
                    add_login_event("Password reset requested", clean_email, "Code generated")
                    st.rerun()
                else:
                    st.error("No user found for this email.")
        with col_b:
            if st.button("Back to login", use_container_width=True):
                st.session_state.auth_step = "login"
                st.rerun()
        return

    email = st.session_state.reset_email
    if time.time() > st.session_state.reset_expiry:
        st.warning("The recovery code expired.")
        if st.button("Start again"):
            clear_reset()
            st.rerun()
        return

    st.info(f"Demo MVP recovery code: {st.session_state.reset_code}")
    code = st.text_input("Recovery code", max_chars=6)
    new_password = st.text_input("New password", type="password")
    confirm_password = st.text_input("Confirm new password", type="password")

    col_a, col_b = st.columns([1, 1])
    with col_a:
        if st.button("Reset password", type="primary", use_container_width=True):
            if code.strip() != st.session_state.reset_code:
                st.error("Incorrect recovery code.")
            elif len(new_password) < 10:
                st.error("Use at least 10 characters.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                st.session_state.session_password_overrides[email] = hash_password(new_password)
                add_login_event("Password reset completed", email, "Success")
                clear_reset()
                st.session_state.auth_step = "login"
                st.success("Password reset for this session. You can sign in now.")
    with col_b:
        if st.button("Cancel recovery", use_container_width=True):
            clear_reset()
            st.session_state.auth_step = "login"
            st.rerun()


def clear_reset() -> None:
    st.session_state.reset_email = None
    st.session_state.reset_code = None
    st.session_state.reset_expiry = 0


def create_ads_data(profile_name: str) -> pd.DataFrame:
    if "Raju Cars" in profile_name:
        rows = [
            ["3M PPF Sholinganallur", "Google Search", "3M Paint Protection Film", "Sholinganallur", 15300, 31, 7, 1800, "Action Required"],
            ["Ceramic Coating OMR", "Google Search", "3M Ceramic Coating", "OMR", 12650, 24, 6, 1700, "Good Control"],
            ["Sunfilm Leads Chennai", "Google Search", "3M Sunfilm", "ECR", 8400, 20, 2, 1500, "Action Required"],
            ["Brand Store Calls", "Maps Ads", "Paint correction", "Akkarai", 4200, 11, 5, 1600, "Strong"],
            ["Interior Protection", "Performance Max", "Interior protection", "Navalur", 6100, 14, 3, 1600, "Watch"],
        ]
    else:
        rows = [
            ["Birthday Cake Adyar", "Google Search", "Birthday cakes", "Adyar", 8200, 29, 8, 900, "Good Control"],
            ["Sourdough Near Me", "Google Search", "Sourdough bread", "Besant Nagar", 5600, 16, 5, 850, "Good Control"],
            ["Dessert Gift Box", "Performance Max", "Dessert boxes", "Velachery", 4900, 18, 3, 850, "Watch"],
        ]

    df = pd.DataFrame(
        rows,
        columns=[
            "Campaign",
            "Channel",
            "Service",
            "Location",
            "Spend",
            "Raw Leads",
            "Verified Buyers",
            "Goal CPA",
            "Status",
        ],
    )
    df["Cost Per Buyer"] = df.apply(
        lambda row: row["Spend"] / row["Verified Buyers"]
        if row["Verified Buyers"] > 0
        else row["Spend"],
        axis=1,
    )
    df["Waste %"] = df.apply(
        lambda row: ((row["Raw Leads"] - row["Verified Buyers"]) / row["Raw Leads"]) * 100
        if row["Raw Leads"] > 0
        else 0,
        axis=1,
    )
    df["Corrective Action"] = df.apply(ad_action, axis=1)
    return df


def ad_action(row: pd.Series) -> str:
    if row["Verified Buyers"] == 0:
        return "Pause high-spend keywords until conversion tracking is verified."
    if row["Cost Per Buyer"] > row["Goal CPA"] * 1.25:
        return "Review search terms, add exact negative keywords and improve landing page qualification."
    if row["Waste %"] > 70:
        return "Tighten match types and add buyer-intent questions before form submission."
    if row["Status"] == "Watch":
        return "Monitor for 3 days and move budget only after buyer conversion improves."
    return "Maintain budget and test one controlled improvement."


def create_review_data(profile_name: str) -> pd.DataFrame:
    if "Raju Cars" in profile_name:
        rows = [
            [
                "Arun",
                5,
                "3M Sunfilm",
                "Very professional team. Competitive price and clean work.",
                "Pending Approval",
                "Sanjay",
            ],
            [
                "Karthik",
                5,
                "3M PPF",
                "Door pads were removed carefully and the PPF finish looks seamless.",
                "Pending Approval",
                "Hari",
            ],
            [
                "Meena",
                1,
                "Ceramic Coating",
                "Delivery update was delayed and I had to call multiple times.",
                "Needs Owner Review",
                "Manager",
            ],
        ]
    else:
        rows = [
            [
                "Priya",
                5,
                "Birthday cakes",
                "Cake design was exactly as promised and tasted fresh.",
                "Pending Approval",
                "Baker",
            ],
            [
                "Rahul",
                2,
                "Sourdough bread",
                "Pickup timing was confusing and staff did not update me.",
                "Needs Owner Review",
                "Manager",
            ],
        ]

    return pd.DataFrame(
        rows,
        columns=["Customer", "Rating", "Service", "Review", "Status", "Owner"],
    )


def generate_review_reply(row: pd.Series, profile: dict) -> str:
    customer = row["Customer"]
    service = row["Service"]
    business = profile["business_name"]
    email = profile["support_email"]

    if row["Rating"] >= 4:
        return (
            f"Hi {customer}, thank you for sharing your experience with {business}. "
            f"We are glad our team could support you with {service} and deliver the finish you expected. "
            "Your feedback means a lot to the team, and we look forward to helping you again."
        )

    return (
        f"Hello {customer}, thank you for bringing this to our attention. "
        f"We are sorry that your {service} experience did not meet the standard we aim to deliver. "
        f"Please email us at {email} with your booking details so our management team can review it and resolve the matter directly."
    )


def create_gmb_audit_data(profile_name: str) -> pd.DataFrame:
    rows = [
        ["Business name, address and phone", "Healthy", "Low", "Verify weekly NAP consistency across GBP, website and directories.", "Manager"],
        ["Review response time", "Attention", "High", "Reply to all pending reviews within 24 hours after owner approval.", "Sales Lead"],
        ["Photo freshness", "Attention", "Medium", "Upload 3 genuine recent work photos with correct service caption.", "Floor Lead"],
        ["Service list accuracy", "Healthy", "Low", "Confirm active services and remove discontinued items.", "Admin"],
        ["Google posts", "Action Required", "High", "Publish one useful customer-problem update today.", "Marketing"],
    ]
    if "Bakery" in profile_name:
        rows[2][3] = "Upload fresh product photos from this week's orders."
        rows[4][3] = "Publish one fresh menu or order deadline update today."
    return pd.DataFrame(rows, columns=["Audit Item", "Status", "Priority", "Corrective Action", "Owner"])


def create_website_audit_data(profile_name: str) -> pd.DataFrame:
    if "Raju Cars" in profile_name:
        rows = [
            ["Home page", 82, "Good", "Add clearer CTA for Sholinganallur 3M services.", "Marketing"],
            ["3M PPF page", 68, "Action Required", "Add process photos, warranty clarity and FAQ for price comparison buyers.", "Admin"],
            ["Ceramic coating page", 74, "Watch", "Improve before/after proof and maintenance explanation.", "Marketing"],
            ["Contact page", 91, "Healthy", "Keep phone, map and WhatsApp working.", "Admin"],
        ]
    else:
        rows = [
            ["Home page", 86, "Good", "Add today's featured cakes above the fold.", "Marketing"],
            ["Birthday cakes", 71, "Watch", "Add design gallery and order lead-time FAQ.", "Admin"],
            ["Sourdough page", 64, "Action Required", "Explain bake schedule, ingredients and pickup timing.", "Manager"],
        ]
    return pd.DataFrame(rows, columns=["Page", "Score", "Status", "Corrective Action", "Owner"])


def create_content_data(profile_name: str) -> pd.DataFrame:
    if "Raju Cars" in profile_name:
        rows = [
            ["Today", "Google Business Profile", "PPF door handle edge protection", "Pending Approval", "Hari", "Book inspection"],
            ["Tomorrow", "Instagram", "Sunfilm first 48 hours care tips", "Draft Ready", "Sanjay", "WhatsApp enquiry"],
            ["This Week", "LinkedIn", "Why price-only coating comparison fails", "Needs Rewrite", "Marketing", "Read article"],
            ["This Week", "Website Update", "3M PPF seamless installation process", "Pending Photos", "Floor Lead", "Call Raju Cars"],
        ]
    else:
        rows = [
            ["Today", "Google Business Profile", "Fresh sourdough batch timing", "Pending Approval", "Baker", "Pre-order now"],
            ["Tomorrow", "Instagram", "Birthday cake design checklist", "Draft Ready", "Marketing", "DM to order"],
            ["This Week", "Website Update", "Cake order lead-time FAQ", "Needs Rewrite", "Admin", "Order enquiry"],
        ]
    return pd.DataFrame(rows, columns=["Due", "Platform", "Topic", "Status", "Owner", "CTA"])


def currency(value: float) -> str:
    return f"Rs. {value:,.0f}"


def filter_dataframe(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    result = df.copy()
    for column, selected in filters.items():
        if column in result.columns and selected != "All":
            result = result[result[column] == selected]
    return result


def read_secret(name: str) -> str:
    try:
        value = st.secrets.get(name, "")
    except Exception:
        value = ""
    return str(value).strip() if value is not None else ""


def normalize_customer_id(value: str) -> str:
    return "".join(ch for ch in str(value) if ch.isdigit())


def get_google_ads_settings() -> dict:
    settings = {
        key: read_secret(secret_name)
        for key, secret_name in GOOGLE_ADS_SECRET_KEYS.items()
    }
    settings["customer_id"] = normalize_customer_id(settings["customer_id"])
    settings["login_customer_id"] = normalize_customer_id(settings["login_customer_id"])
    settings["api_version"] = read_secret("GOOGLE_ADS_API_VERSION") or GOOGLE_ADS_API_VERSION
    return settings


def missing_google_ads_settings(settings: dict) -> list[str]:
    required = ["developer_token", "client_id", "client_secret", "refresh_token", "customer_id"]
    return [GOOGLE_ADS_SECRET_KEYS[key] for key in required if not settings.get(key)]


def google_ads_config_table(settings: dict) -> pd.DataFrame:
    rows = []
    labels = {
        "developer_token": "Developer token",
        "client_id": "OAuth client ID",
        "client_secret": "OAuth client secret",
        "refresh_token": "OAuth refresh token",
        "customer_id": "Client customer ID",
        "login_customer_id": "Manager login customer ID",
    }
    for key, label in labels.items():
        required = key != "login_customer_id"
        value = settings.get(key, "")
        rows.append(
            {
                "Setting": label,
                "Secret name": GOOGLE_ADS_SECRET_KEYS[key],
                "Required": "Yes" if required else "Only for MCC access",
                "Status": "Configured" if value else "Missing",
            }
        )
    return pd.DataFrame(rows)


def load_google_ads_client(settings: dict):
    try:
        from google.ads.googleads.client import GoogleAdsClient
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Google Ads Python library is not installed. Add google-ads to requirements.txt and redeploy Streamlit."
        ) from exc

    config = {
        "developer_token": settings["developer_token"],
        "client_id": settings["client_id"],
        "client_secret": settings["client_secret"],
        "refresh_token": settings["refresh_token"],
        "use_proto_plus": True,
    }
    if settings.get("login_customer_id"):
        config["login_customer_id"] = settings["login_customer_id"]

    return GoogleAdsClient.load_from_dict(config, version=settings["api_version"])


def resolve_google_ads_dates(date_range) -> tuple[str, str]:
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        end_date = date.today()
        start_date = end_date - timedelta(days=7)
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")


def live_google_ads_action(row: pd.Series, goal_cpa: float) -> str:
    conversions = float(row["Conversions"])
    cost = float(row["Cost"])
    clicks = int(row["Clicks"])
    if cost > 0 and conversions == 0:
        return "Check conversion tracking, search terms and landing page before increasing budget."
    if conversions > 0 and goal_cpa > 0 and row["Cost / Conversion"] > goal_cpa:
        return "Reduce waste: inspect search terms, refine match types and improve buyer qualification."
    if clicks > 0 and conversions / clicks < 0.03:
        return "Improve lead quality: add clearer offer, proof, price range and qualifying questions."
    return "Maintain controlled budget and test one improvement at a time."


def fetch_google_ads_campaign_metrics(settings: dict, date_range, goal_cpa: float) -> pd.DataFrame:
    client = load_google_ads_client(settings)
    customer_id = settings["customer_id"]
    start_date, end_date = resolve_google_ads_dates(date_range)

    query = f"""
        SELECT
          campaign.id,
          campaign.name,
          campaign.status,
          campaign.advertising_channel_type,
          metrics.impressions,
          metrics.clicks,
          metrics.cost_micros,
          metrics.conversions,
          metrics.all_conversions
        FROM campaign
        WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY metrics.cost_micros DESC
        LIMIT 50
    """

    service = client.get_service("GoogleAdsService")
    rows = []
    response = service.search_stream(customer_id=customer_id, query=query)

    for batch in response:
        for row in batch.results:
            cost = float(row.metrics.cost_micros or 0) / 1_000_000
            conversions = float(row.metrics.conversions or 0)
            cost_per_conversion = cost / conversions if conversions else 0
            status = getattr(row.campaign.status, "name", str(row.campaign.status))
            channel = getattr(
                row.campaign.advertising_channel_type,
                "name",
                str(row.campaign.advertising_channel_type),
            )
            rows.append(
                {
                    "Campaign ID": row.campaign.id,
                    "Campaign": row.campaign.name,
                    "Channel": status_clean(channel),
                    "Status": status_clean(status),
                    "Impressions": int(row.metrics.impressions or 0),
                    "Clicks": int(row.metrics.clicks or 0),
                    "Cost": cost,
                    "Conversions": conversions,
                    "All Conversions": float(row.metrics.all_conversions or 0),
                    "Cost / Conversion": cost_per_conversion,
                }
            )

    df = pd.DataFrame(rows)
    if df.empty:
        return pd.DataFrame(
            columns=[
                "Campaign ID",
                "Campaign",
                "Channel",
                "Status",
                "Impressions",
                "Clicks",
                "Cost",
                "Conversions",
                "All Conversions",
                "Cost / Conversion",
                "Suggested Action",
            ]
        )

    df["Suggested Action"] = df.apply(lambda row: live_google_ads_action(row, goal_cpa), axis=1)
    return df


def status_clean(value: str) -> str:
    return str(value).replace("_", " ").title()


def render_sidebar() -> tuple[str, dict, str]:
    st.sidebar.title("LocalGrow AI")
    user = st.session_state.user
    st.sidebar.caption(f"{user['name']} | {user['role']}")

    profile_name = st.sidebar.selectbox("Business account", list(BUSINESS_PROFILES.keys()))
    profile = BUSINESS_PROFILES[profile_name]

    st.sidebar.divider()
    menu = st.sidebar.radio(
        "Workspace",
        [
            "Owner Dashboard",
            "Google Ads",
            "GMB Reviews",
            "GMB Audit",
            "Website Audit",
            "Content Planner",
            "Corrective Actions",
            "Security",
        ],
    )

    st.sidebar.divider()
    st.sidebar.subheader("Global filters")
    date_range = st.sidebar.date_input(
        "Report date range",
        value=(date.today() - timedelta(days=7), date.today()),
    )
    location = st.sidebar.selectbox("Location", ["All"] + profile["locations"])
    service = st.sidebar.selectbox("Service", ["All"] + profile["services"])
    priority = st.sidebar.selectbox("Priority", ["All", "High", "Medium", "Low"])
    owner = st.sidebar.selectbox(
        "Owner",
        ["All", "Admin", "Manager", "Marketing", "Sales Lead", "Floor Lead", "Sanjay", "Hari"],
    )

    if st.sidebar.button("Sign out", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.pending_user = None
        st.session_state.auth_step = "login"
        st.rerun()

    filters = {
        "date_range": date_range,
        "Location": location,
        "Service": service,
        "Priority": priority,
        "Owner": owner,
    }
    return profile_name, filters, menu


def render_header(profile: dict, filters: dict) -> None:
    st.markdown(f'<div class="app-title">{profile["display_name"]}</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="app-subtitle">Base: {profile["base_location"]} | Support: {profile["support_email"]} | Phone: {profile["phone"]}</div>',
        unsafe_allow_html=True,
    )

    date_range = filters["date_range"]
    if isinstance(date_range, tuple) and len(date_range) == 2:
        range_text = f"{date_range[0].strftime('%d-%b-%Y')} to {date_range[1].strftime('%d-%b-%Y')}"
    else:
        range_text = "Custom period"

    cols = st.columns(4)
    cols[0].caption("Date filter")
    cols[0].write(range_text)
    cols[1].caption("Location")
    cols[1].write(filters["Location"])
    cols[2].caption("Service")
    cols[2].write(filters["Service"])
    cols[3].caption("Priority")
    cols[3].write(filters["Priority"])
    st.divider()


def render_owner_dashboard(profile_name: str, profile: dict, filters: dict) -> None:
    ads = filter_dataframe(create_ads_data(profile_name), {"Location": filters["Location"], "Service": filters["Service"]})
    reviews = create_review_data(profile_name)
    gmb = filter_dataframe(create_gmb_audit_data(profile_name), {"Priority": filters["Priority"], "Owner": filters["Owner"]})
    website = filter_dataframe(create_website_audit_data(profile_name), {"Owner": filters["Owner"]})
    content = filter_dataframe(create_content_data(profile_name), {"Owner": filters["Owner"]})

    total_spend = ads["Spend"].sum()
    verified_buyers = ads["Verified Buyers"].sum()
    cost_per_buyer = total_spend / verified_buyers if verified_buyers else 0
    pending_reviews = len(reviews[reviews["Status"] != "Approved"])
    high_priority = len(gmb[gmb["Priority"] == "High"]) + len(website[website["Status"] == "Action Required"])

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Ad Spend", currency(total_spend), "Manual MVP data")
    k2.metric("Cost Per Verified Buyer", currency(cost_per_buyer), "Quality over raw leads")
    k3.metric("Pending Review Replies", pending_reviews, "Approval required")
    k4.metric("High Priority Actions", high_priority, "Fix first")

    st.subheader("Today first corrections")
    actions = build_corrective_actions(profile_name)
    actions = filter_dataframe(actions, {"Priority": filters["Priority"], "Owner": filters["Owner"]})
    st.dataframe(
        actions.head(8),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Impact": st.column_config.ProgressColumn("Impact", min_value=0, max_value=100),
        },
    )

    col_a, col_b = st.columns([1.1, 1])
    with col_a:
        st.subheader("Google Ads quality snapshot")
        st.dataframe(
            ads[["Campaign", "Spend", "Raw Leads", "Verified Buyers", "Cost Per Buyer", "Waste %", "Status"]],
            use_container_width=True,
            hide_index=True,
            column_config={
                "Spend": st.column_config.NumberColumn("Spend", format="Rs. %d"),
                "Cost Per Buyer": st.column_config.NumberColumn("Cost Per Buyer", format="Rs. %d"),
                "Waste %": st.column_config.ProgressColumn("Waste %", min_value=0, max_value=100),
            },
        )
    with col_b:
        st.subheader("Content and profile upkeep")
        st.dataframe(content, use_container_width=True, hide_index=True)


def render_google_ads_connection_panel(filters: dict) -> None:
    st.subheader("Direct Google Ads API connection")
    st.caption("Read-only live reporting. Keep manual/sample mode until Google credentials are configured.")

    settings = get_google_ads_settings()
    status_df = google_ads_config_table(settings)
    st.dataframe(status_df, use_container_width=True, hide_index=True)

    with st.expander("Streamlit Secrets format"):
        st.write("Paste these values in Streamlit Cloud under App Settings > Secrets. Do not paste real secrets into GitHub.")
        st.code(
            """
GOOGLE_ADS_DEVELOPER_TOKEN = "your-developer-token"
GOOGLE_ADS_CLIENT_ID = "your-oauth-client-id"
GOOGLE_ADS_CLIENT_SECRET = "your-oauth-client-secret"
GOOGLE_ADS_REFRESH_TOKEN = "your-refresh-token"
GOOGLE_ADS_CUSTOMER_ID = "1234567890"

# Optional, only when accessing client accounts through an MCC manager account.
GOOGLE_ADS_LOGIN_CUSTOMER_ID = "0987654321"

# Keep v24 for Google Ads API v24.x client library support.
GOOGLE_ADS_API_VERSION = "v24"
            """.strip(),
            language="toml",
        )
        st.write(
            "Customer IDs should be numbers only, without hyphens. The customer account must have conversion tracking "
            "configured if you want cost-per-conversion and corrective actions to be meaningful."
        )

    missing = missing_google_ads_settings(settings)
    if missing:
        st.warning("Google Ads API is not connected yet. Missing secrets: " + ", ".join(missing))
        st.info("You can continue using the manual audit below until these values are added.")
        return

    goal_cpa = st.number_input(
        "Target cost per conversion for live report",
        min_value=1,
        value=1800,
        step=100,
        help="Used only for SaaS corrective-action suggestions. Google will return account-currency cost.",
    )

    if st.button("Fetch live Google Ads campaign metrics", type="primary"):
        with st.spinner("Connecting to Google Ads API and reading campaign performance..."):
            try:
                live_df = fetch_google_ads_campaign_metrics(settings, filters["date_range"], goal_cpa)
            except Exception as exc:
                st.error("Could not fetch Google Ads data.")
                st.caption(f"{exc.__class__.__name__}: {exc}")
                st.info(
                    "Check developer token approval, OAuth refresh token, customer ID, MCC login customer ID and account permissions."
                )
                return

        if live_df.empty:
            st.info("Connected, but no campaign rows were returned for this date range.")
            return

        st.success("Live Google Ads data loaded.")
        st.dataframe(
            live_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Cost": st.column_config.NumberColumn("Cost", format="%.2f"),
                "Conversions": st.column_config.NumberColumn("Conversions", format="%.2f"),
                "All Conversions": st.column_config.NumberColumn("All Conversions", format="%.2f"),
                "Cost / Conversion": st.column_config.NumberColumn("Cost / Conversion", format="%.2f"),
            },
        )


def render_google_ads(profile_name: str, filters: dict) -> None:
    render_google_ads_connection_panel(filters)
    st.divider()

    st.subheader("Google Ads performance and budget waste check")
    st.caption("Manual/sample fallback for demo, onboarding and accounts that are not connected yet.")
    ads = filter_dataframe(create_ads_data(profile_name), {"Location": filters["Location"], "Service": filters["Service"]})

    st.dataframe(
        ads,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Spend": st.column_config.NumberColumn("Spend", format="Rs. %d"),
            "Goal CPA": st.column_config.NumberColumn("Goal CPA", format="Rs. %d"),
            "Cost Per Buyer": st.column_config.NumberColumn("Cost Per Buyer", format="Rs. %d"),
            "Waste %": st.column_config.ProgressColumn("Waste %", min_value=0, max_value=100),
        },
    )

    st.subheader("Manual smart audit")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        spend = st.number_input("Spend this week", min_value=0, value=15000, step=500)
    with c2:
        raw_leads = st.number_input("Raw calls or leads", min_value=1, value=25, step=1)
    with c3:
        verified_buyers = st.number_input("Verified buyers", min_value=0, value=5, step=1)
    with c4:
        goal_cpa = st.number_input("Goal cost per buyer", min_value=1, value=1800, step=100)

    if st.button("Run ad quality audit", type="primary"):
        actual_cpa = spend / verified_buyers if verified_buyers else spend
        waste = ((raw_leads - verified_buyers) / raw_leads) * 100
        m1, m2, m3 = st.columns(3)
        m1.metric("Actual cost per buyer", currency(actual_cpa))
        m2.metric("Estimated wasted traffic", f"{waste:.0f}%")
        m3.metric("Status", "Good Control" if actual_cpa <= goal_cpa and waste < 50 else "Action Required")

        if verified_buyers == 0:
            st.error("Corrective action: stop scaling spend until conversion tracking and lead quality are verified.")
        elif actual_cpa > goal_cpa:
            st.warning("Corrective action: check search terms, add exact negative keywords carefully, improve form qualification and landing page proof.")
        else:
            st.success("Maintain budget and test one controlled improvement at a time.")


def render_gmb_reviews(profile_name: str, profile: dict) -> None:
    st.subheader("GMB review reply approval queue")
    st.caption("MVP rule: draft only. No automatic posting without human approval.")
    reviews = create_review_data(profile_name)

    for idx, row in reviews.iterrows():
        with st.expander(f"{row['Customer']} | {row['Rating']} star | {row['Service']} | {row['Status']}", expanded=idx == 0):
            st.write(row["Review"])
            key = f"{profile_name}-{idx}"
            default_reply = st.session_state.review_replies.get(key, generate_review_reply(row, profile))
            reply = st.text_area("Draft reply", value=default_reply, key=f"reply-{key}", height=130)
            st.session_state.review_replies[key] = reply

            c1, c2, c3 = st.columns([1, 1, 2])
            with c1:
                if st.button("Approve draft", key=f"approve-{key}", use_container_width=True):
                    st.success("Approved in MVP queue. Connect GBP API later for controlled publishing.")
            with c2:
                if st.button("Needs edit", key=f"edit-{key}", use_container_width=True):
                    st.warning("Marked for edit.")
            with c3:
                st.caption("Safe rule: reply to real review content, avoid keyword stuffing, avoid false locations and avoid automatic publishing.")


def render_gmb_audit(profile_name: str, filters: dict) -> None:
    st.subheader("Google Business Profile audit")
    audit = filter_dataframe(create_gmb_audit_data(profile_name), {"Priority": filters["Priority"], "Owner": filters["Owner"]})
    st.dataframe(audit, use_container_width=True, hide_index=True)

    st.subheader("Weekly profile upkeep checklist")
    checks = [
        "Verify business name, address and phone consistency",
        "Reply to pending reviews after approval",
        "Upload genuine recent photos",
        "Publish one useful local business update",
        "Check service list and appointment links",
        "Record competitor movements from public information only",
    ]
    for item in checks:
        st.checkbox(item)


def render_website_audit(profile_name: str, filters: dict) -> None:
    st.subheader("Website audit and corrections")
    website = filter_dataframe(create_website_audit_data(profile_name), {"Owner": filters["Owner"]})
    st.dataframe(
        website,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100),
        },
    )

    st.subheader("Manual page audit input")
    c1, c2, c3 = st.columns(3)
    with c1:
        page_url = st.text_input("Page URL", value="https://www.rajucars.com/")
    with c2:
        page_goal = st.selectbox("Page goal", ["Lead enquiry", "Phone call", "WhatsApp", "Booking", "Information"])
    with c3:
        mobile_score = st.slider("Mobile usability score", 0, 100, 75)

    proof = st.slider("Trust proof strength", 0, 100, 60)
    cta = st.slider("CTA clarity", 0, 100, 55)
    technical = st.slider("Technical health", 0, 100, 70)

    if st.button("Run website correction check", type="primary"):
        total = round((mobile_score * 0.35) + (proof * 0.25) + (cta * 0.25) + (technical * 0.15))
        st.metric("Page readiness score", f"{total}/100")
        if total < 70:
            st.warning(f"Corrective action for {page_goal}: improve CTA clarity, proof, load speed and FAQ before sending more paid traffic to {page_url}.")
        else:
            st.success("Page can receive controlled traffic. Continue monitoring calls, form quality and buyer conversion.")


def render_content_planner(profile_name: str, filters: dict) -> None:
    st.subheader("Daily content posting planner")
    content = filter_dataframe(create_content_data(profile_name), {"Owner": filters["Owner"]})
    st.dataframe(content, use_container_width=True, hide_index=True)

    st.subheader("Create a safe content draft")
    profile = BUSINESS_PROFILES[profile_name]
    c1, c2, c3 = st.columns(3)
    with c1:
        platform = st.selectbox("Platform", ["Google Business Profile", "Instagram", "LinkedIn", "Website Update", "WhatsApp"])
    with c2:
        service = st.selectbox("Service", profile["services"])
    with c3:
        tone = st.selectbox("Tone", ["Helpful", "Authority", "Offer", "Customer confusion"])

    customer_problem = st.text_area(
        "Customer problem",
        value="Many customers compare only price and miss the difference in inspection, prep work and installation quality.",
    )
    insight = st.text_area(
        "Technical insight",
        value="Final result depends on surface preparation, product selection, installation method and curing discipline.",
    )

    if st.button("Generate content draft", type="primary"):
        draft = (
            f"{customer_problem}\n\n"
            f"For {service}, the visible result is not only the product name. {insight}\n\n"
            f"At {profile['business_name']}, our team focuses on explaining the process clearly before the customer decides. "
            f"For booking or inspection, contact {profile['phone']}."
        )
        if platform == "Google Business Profile":
            draft += "\n\nLocal note: available for customers around our service area."
        if tone == "Offer":
            draft += "\n\nAsk for the current package before booking. Terms depend on vehicle size and condition."
        st.code(draft, language="text")


def build_corrective_actions(profile_name: str) -> pd.DataFrame:
    ads = create_ads_data(profile_name)
    gmb = create_gmb_audit_data(profile_name)
    website = create_website_audit_data(profile_name)
    content = create_content_data(profile_name)

    rows = []
    for _, row in ads.iterrows():
        if row["Status"] in ["Action Required", "Watch"]:
            rows.append(
                [
                    "Google Ads",
                    row["Campaign"],
                    "High" if row["Status"] == "Action Required" else "Medium",
                    row["Corrective Action"],
                    "Marketing",
                    85 if row["Status"] == "Action Required" else 55,
                    "Today" if row["Status"] == "Action Required" else "3 days",
                ]
            )

    for _, row in gmb.iterrows():
        if row["Status"] != "Healthy":
            rows.append(
                [
                    "GMB Audit",
                    row["Audit Item"],
                    row["Priority"],
                    row["Corrective Action"],
                    row["Owner"],
                    80 if row["Priority"] == "High" else 55,
                    "Today" if row["Priority"] == "High" else "This week",
                ]
            )

    for _, row in website.iterrows():
        if row["Status"] in ["Action Required", "Watch"]:
            rows.append(
                [
                    "Website Audit",
                    row["Page"],
                    "High" if row["Status"] == "Action Required" else "Medium",
                    row["Corrective Action"],
                    row["Owner"],
                    75 if row["Status"] == "Action Required" else 50,
                    "This week",
                ]
            )

    for _, row in content.iterrows():
        if row["Status"] in ["Needs Rewrite", "Pending Photos", "Pending Approval"]:
            rows.append(
                [
                    "Content",
                    row["Topic"],
                    "Medium",
                    f"Move {row['Platform']} item from {row['Status']} to approved/published.",
                    row["Owner"],
                    45,
                    row["Due"],
                ]
            )

    return pd.DataFrame(
        rows,
        columns=["Module", "Item", "Priority", "Corrective Action", "Owner", "Impact", "Due"],
    )


def render_corrective_actions(profile_name: str, filters: dict) -> None:
    st.subheader("Corrective action control center")
    actions = build_corrective_actions(profile_name)
    actions = filter_dataframe(actions, {"Priority": filters["Priority"], "Owner": filters["Owner"]})
    st.dataframe(
        actions,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Impact": st.column_config.ProgressColumn("Impact", min_value=0, max_value=100),
        },
    )

    st.subheader("Owner decision note")
    action = st.selectbox("Select action for management note", actions["Item"].tolist() if not actions.empty else ["No pending action"])
    decision = st.text_area("Decision / instruction", value="Call customer leads same day, update status before closing business.")
    if st.button("Save management note", type="primary"):
        st.success(f"Saved note for: {action}")
        st.caption(decision)


def render_security() -> None:
    st.subheader("Security and user access")
    users = []
    for email, user in get_users().items():
        users.append({"Email": email, "Name": user["name"], "Role": user["role"], "Status": "Active"})
    st.dataframe(pd.DataFrame(users), use_container_width=True, hide_index=True)

    st.subheader("Login activity")
    if st.session_state.login_events:
        st.dataframe(pd.DataFrame(st.session_state.login_events), use_container_width=True, hide_index=True)
    else:
        st.info("No login events recorded in this session.")

    st.subheader("Production authentication checklist")
    checklist = [
        "Move users from code to database",
        "Hash passwords with per-user salts",
        "Send real email/SMS OTP",
        "Add forgot-password email link expiry",
        "Add role-based page permissions",
        "Add audit logs for every approval and API push",
    ]
    for item in checklist:
        st.checkbox(item)


def dashboard() -> None:
    profile_name, filters, menu = render_sidebar()
    profile = BUSINESS_PROFILES[profile_name]
    render_header(profile, filters)

    if menu == "Owner Dashboard":
        render_owner_dashboard(profile_name, profile, filters)
    elif menu == "Google Ads":
        render_google_ads(profile_name, filters)
    elif menu == "GMB Reviews":
        render_gmb_reviews(profile_name, profile)
    elif menu == "GMB Audit":
        render_gmb_audit(profile_name, filters)
    elif menu == "Website Audit":
        render_website_audit(profile_name, filters)
    elif menu == "Content Planner":
        render_content_planner(profile_name, filters)
    elif menu == "Corrective Actions":
        render_corrective_actions(profile_name, filters)
    elif menu == "Security":
        render_security()

    st.divider()
    st.caption(
        "MVP status: Google Ads API supports live read-only reporting after Streamlit Secrets are configured. GMB API, email OTP and database remain backend-phase items."
    )


def main() -> None:
    init_state()
    if not st.session_state.authenticated:
        if st.session_state.auth_step == "two_factor":
            two_factor_screen()
        elif st.session_state.auth_step == "forgot":
            forgot_password_screen()
        else:
            login_screen()
    else:
        dashboard()


if __name__ == "__main__":
    main()
