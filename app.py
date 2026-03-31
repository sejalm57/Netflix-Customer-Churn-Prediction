import streamlit as st
import pickle
from streamlit_option_menu import option_menu
import base64

st.set_page_config(page_title="Netflix Churn", layout="wide")

# ---------- FUNCTION ----------
def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_img = get_base64("kk.jpg")   

# ---------- CSS ----------
st.markdown(f"""
<style>
.stApp {{
background-image: url("data:image/jpg;base64,{bg_img}");
background-size: cover;
background-position: center;
background-repeat: no-repeat;
background-attachment: fixed;
background-color: rgba(0,0,0,0.2);
background-blend-mode: darken;
}}

.title {{
color: red;
font-size: 65px;
text-align: center;
font-weight: bold;
text-shadow: 0px 0px 20px red;
letter-spacing: 2px;
}}

.subtitle {{
color: white;
font-size: 22px;
text-align: center;
}}

.stButton>button {{
background-color: red;
color: white;
border-radius: 12px;
font-size: 18px;
padding: 10px 20px;
transition: 0.3s;
}}

.stButton>button:hover {{
transform: scale(1.05);
background-color: darkred;
}}

.card {{
background-color: rgba(0,0,0,0.4);
backdrop-filter: blur(6px);
padding:20px;
border-radius:15px;
}}

label, .stMarkdown {{
color: white !important;
}}
</style>
""", unsafe_allow_html=True)

# ---------- NAVBAR ----------
selected = option_menu(
    menu_title=None,
    options=["Home","Prediction","Model Info","About"],
    orientation="horizontal"
)

# ---------- HOME ----------
if selected == "Home":

    # Hero Section
    st.markdown('<p class="title">🎬 NETFLIX CHURN PREDICTION</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Predict customer behavior before they leave 🚀</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Problem + Objective
    st.markdown("""
    <div class="card">
    <h3 style="color:red;">📊 Problem Statement</h3>
    <p>
    Streaming platforms face customer churn due to low engagement and inactivity, leading to revenue loss.
    Identifying such users in advance helps improve retention strategies.
    </p>

    <h3 style="color:red;">🎯 Objective</h3>
    <p>
    Build a machine learning system to predict whether a customer will churn or stay based on behavior patterns.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Features + Business Impact
    st.markdown("""
    <div class="card">
    <h3 style="color:red;">🚀 Key Features</h3>
    <p>
    Provides real-time churn prediction with an easy-to-use interface. It analyzes user behavior such as watch time and login activity to deliver fast and accurate results.
    </p>

    <h3 style="color:red;">💡 Business Impact</h3>
    <p>
    Helps businesses identify at-risk customers and take proactive steps to retain them, improving customer satisfaction and overall revenue.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # How it Works
    st.markdown("""
    <div class="card">
    <h3 style="color:red;">⚙️ How It Works</h3>
    <p>
    The system collects user inputs, processes the data, and applies a trained machine learning model to predict whether the customer will churn or stay.
    </p>
    </div>
    """, unsafe_allow_html=True)

# ---------- PREDICTION ----------
elif selected == "Prediction":

    import pandas as pd

    st.markdown('<p class="title">🎯 Churn Prediction</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Fill details to check churn</p>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("🎂 Age", 18, 80, 18)
    with col2:
        gender = st.selectbox("👤 Gender", ["Male", "Female","Other"])
    with col3:
        watch = st.number_input("📺 Monthly Watch Hours", 0, 200, 40)

    col4, col5, col6 = st.columns(3)

    with col4:
        login = st.number_input("📅 Last Login Days", 0, 60, 5)
    with col5:
        profiles = st.number_input("👥 Profiles", 1, 5, 2)
    with col6:
        subscription = st.selectbox("💳 Subscription", ["Basic", "Standard", "Premium"])

    try:
        model = pickle.load(open("decision_tree_model.pkl", "rb"))
        model_columns = pickle.load(open("model_columns.pkl", "rb"))
    except:
        st.error("Model files not found")
        st.stop()

    if st.button("🔍 Predict Churn"):

        gender_map = {"Other": 2,"Female": 0,"Male": 1}
        subscription_map = {"Basic": 0, "Standard": 1, "Premium": 2}

        input_data = pd.DataFrame([{
            "age": age,
            "gender": gender_map[gender],
            "subscription_type": subscription_map[subscription],
            "watch_hours": watch,
            "monthly_fee": 15,
            "last_login_days": login,
            "region": 0,
            "device": 0,
            "payment_method": 0,
            "number_of_profiles": profiles,
            "avg_watch_time_per_day": 2,
            "favorite_genre": 0
        }])

        input_data = input_data.reindex(columns=model_columns, fill_value=0)

        prediction = model.predict(input_data)

        if prediction[0] == 1:
            st.markdown("""
            <div style="background: linear-gradient(45deg, red, darkred);
            padding:30px; border-radius:20px; text-align:center;">
            <h2 style="color:white;">❌ Customer Will Churn</h2>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(45deg, green, darkgreen);
            padding:30px; border-radius:20px; text-align:center;">
            <h2 style="color:white;">✅ Customer Will Stay</h2>
            </div>
            """, unsafe_allow_html=True)

# ---------- MODEL INFO ----------
elif selected == "Model Info":

    import pandas as pd

    st.markdown('<p class="title">📊 Model Info</p>', unsafe_allow_html=True)

    df = pd.read_csv("netflix_customer_churn.csv")
    st.dataframe(df.head(10))

# ---------- ABOUT ----------
elif selected == "About":

    st.markdown('<p class="title">👤 About</p>', unsafe_allow_html=True)
    st.write("")

    st.markdown("""
    <div style="
    background-color: rgba(0,0,0,0.4);
    backdrop-filter: blur(6px);
    padding:20px;
    border-radius:15px;
    text-align:center;
    ">

    <h3 style="color:red;">🛠️ Tools & Technologies</h3>

    <ul style="color:white; list-style-type:none; font-size:16px;">
        <li>Python</li>
        <li>Pandas</li>
        <li>NumPy</li>
        <li>Scikit-learn</li>
        <li>Decision Tree Algorithm</li>
        <li>Streamlit</li>
    </ul>

    <h3 style="color:red;">👩‍💻 Developed By</h3>

    <p style="color:white; font-size:18px;">
    Sejal <br>
    Ridhi
    </p>

    <p style="color:white; font-size:15px;">
    This project demonstrates a real-world application of machine learning 
    for predicting customer churn and improving business decisions.
    </p>

    <p style="color:gray; font-size:14px;">
    © 2026 Netflix Churn Project
    </p>

    </div>
    """, unsafe_allow_html=True)