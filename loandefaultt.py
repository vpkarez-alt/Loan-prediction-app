import streamlit as st
import pandas as pd
import pickle

# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="Loan Default Prediction - Bank Standard",
    page_icon="₦💰",  # Naira symbol + money bag
    layout="wide"
)


# =========================
# Custom CSS Styling
# =========================
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #b0c4de, #8da3b8);
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h3, h4, h2, h5, h6, label {
        color: #004080 !important;
    }
    .stNumberInput input, .stSelectbox div, .stSlider, textarea, input[type="text"], input[type="number"] {
        background-color: rgba(255, 255, 255, 0.8) !important;
        color: #003366 !important;
        font-weight: bold;
        border-radius: 8px;
    }
    .stButton>button {
        background-color: #004080;
        color: white;
        border-radius: 8px;
        font-size: 16px;
        padding: 8px 20px;
        transition: 0.3s;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0066cc;
        color: #f2f2f2;
    }
    .success-box {
        background-color: rgba(212, 237, 218, 0.95);
        border-left: 6px solid #28a745;
        padding: 15px;
        border-radius: 5px;
        color: #1a3d1a;
    }
    .error-box {
        background-color: rgba(248, 215, 218, 0.95);
        border-left: 6px solid #dc3545;
        padding: 15px;
        border-radius: 5px;
        color: #4a1a1a;
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# Load Model
# =========================
with open('loandefault.pkl', 'rb') as f:
    model = pickle.load(f)

# =========================
# App Header
# =========================
st.markdown("<h1>💰₦ Loan Default Prediction</h1>", unsafe_allow_html=True)
st.markdown("### Professional Banking Standard - Predict a Customer's Loan Repayment Likelihood")

# =========================
# Loan Information
# =========================
st.markdown("#### 💳 Loan Information")
col1, col2, col3 = st.columns(3)
with col1:
    loan_number = st.number_input(
        "Number of Loans Taken",
        min_value=1,
        max_value=60,
        value=20,
        step=1
    )
    bank_account_type = st.selectbox("Bank Account Type", ["Savings", "Current", "Other"])

with col2:
    loan_amount = st.number_input(
        "Loan Amount (₦)",
        min_value=5000,
        max_value=1_000_000,
        value=50_000,
        step=1000
    )
    bank_name_clients = st.selectbox(
        "Bank Name",
        [
            "Access Bank", "Diamond Bank", "EcoBank", "FCMB", "Fidelity Bank", "First Bank", "GT Bank",
            "Heritage Bank", "Keystone Bank", "Skye Bank", "Stanbic IBTC", "Standard Chartered",
            "Sterling Bank", "UBA", "Union Bank", "Unity Bank", "Wema Bank", "Zenith Bank"
        ]
    )

with col3:
    loan_total_due = st.number_input(
        "Total Loan Due (₦)",
        min_value=5000,
        max_value=1_000_000,
        value=50_000,
        step=1000
    )

# =========================
# Employment & Education
# =========================
st.markdown("#### 👔 Employment & Education")
col4, col5 = st.columns(2)
with col4:
    employment_status_clients = st.selectbox(
        "Employment Status",
        ["Contract", "Permanent", "Retired", "Self-Employed", "Student", "Unemployed"]
    )
with col5:
    level_of_education_clients = st.selectbox(
        "Level of Education",
        ["None", "Primary", "Secondary", "Graduate", "Post-Graduate"]
    )

# =========================
# Credit & Repayment Behavior
# =========================
st.markdown("#### 📊 Credit & Repayment Behavior")
col6, col7, col8 = st.columns(3)
with col6:
    on_time_ratio = st.slider("On-time Repayment Ratio (0-1)", 0.0, 1.0, 0.5)
with col7:
    avg_loan_term_days = st.number_input(
        "Average Loan Term (days)",
        min_value=10,
        max_value=100,
        value=60,
        step=1
    )
with col8:
    credit_score = st.number_input(
        "Credit Score (0-100)",
        min_value=0,
        max_value=100,
        value=50,
        step=1
    )

# =========================
# Personal Information
# =========================
st.markdown("#### 👤 Personal Information")
col9, col10, col11 = st.columns([1,1,1])
with col9:
    age = st.slider("Age", 18, 100, 50)
with col10:
    state = st.selectbox(
        "State of Residence",
        [
            "Abia", "Abuja Federal Capital Territory", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue",
            "Borno", "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "Gombe", "Imo", "Jigawa", "Kaduna", "Kano",
            "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos", "Nassarawa", "Niger", "Ogun", "Ondo", "Osun", "Outside Nigeria",
            "Oyo", "Plateau", "Rivers", "Sokoto", "Taraba", "Zamfara"
        ]
    )
with col11:
    st.write("")

# =========================
# Prediction Button
# =========================
st.markdown("---")
if st.button("🔍 Predict Loan Default Risk"):
    customer_data = {
        "loan_number": [loan_number],
        "loan_amount": [loan_amount],
        "loan_total_due": [loan_total_due],
        "bank_account_type": [bank_account_type],
        "bank_name_clients": [bank_name_clients],
        "employment_status_clients": [employment_status_clients],
        "level_of_education_clients": [level_of_education_clients],
        "on_time_ratio": [on_time_ratio],
        "avg_loan_term_days": [avg_loan_term_days],
        "credit_score": [credit_score],
        "age": [age],
        "state": [state]
    }
    customer_data["loan_to_due_ratio"] = customer_data["loan_amount"][0] / customer_data["loan_total_due"][0]
    input_df = pd.DataFrame(customer_data)

    prediction = model.predict(input_df)[0]

    if prediction:  # True means loan will be repaid
        st.markdown('<div class="success-box">✅ <b>Likely to Repay:</b> This customer is predicted to repay the loan on time.</div>', unsafe_allow_html=True)
    else:  # False means default
        st.markdown('<div class="error-box">⚠️ <b>Likely to Default:</b> This customer may fail to repay the loan.</div>', unsafe_allow_html=True)







