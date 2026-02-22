import streamlit as st
from login_view import show_login_page
from admin_view import show_admin_dashboard, show_staff_dashboard


# 1. Konfigurasi Halaman
st.set_page_config(page_title="MyPrestasi HPU", layout="wide")
# --- Tambah di sini (Baris 8) ---
def apply_saas_theme():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
        
        /* Kad Metrik SaaS */
        [data-testid="stMetric"] {
            background-color: #ffffff;
            border: 1px solid #eef2f6;
            padding: 15px 20px;
            border-radius: 12px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.02);
        }
        
        /* Butang Moden */
        .stButton > button {
            border-radius: 10px !important;
            font-weight: 600 !important;
            border: 1px solid #e2e8f0 !important;
        }
        </style>
    """, unsafe_allow_html=True)
# 2. CSS Global
st.markdown("""
    <style>
    .block-container { padding-top: 4rem !important; max-width: 95% !important; }
    .stApp { background-color: white; }
    .medstar-blue { 
        color: #00a0dc !important; font-weight: 900 !important; font-size: 6rem !important; 
        line-height: 1.2 !important; letter-spacing: -2px !important; margin-top: -20px !important; margin-bottom: 20px !important;
        display: block !important;
    }
    .login-title { font-size: 2.5rem !important; font-weight: 700 !important; color: #333 !important; margin-top: 0px !important; }
    .stTextInput input, .stSelectbox div[data-baseweb="select"] { font-size: 1.1rem !important; height: 3.5rem !important; border-radius: 8px !important; }
    .stTextInput label, .stSelectbox label { font-size: 1.2rem !important; font-weight: 600 !important; margin-bottom: 5px !important; }
    .testimonial-box { background-color: rgba(255, 255, 255, 0.9); padding: 40px; border-radius: 15px; position: absolute; bottom: 10%; left: 5%; right: 5%; border-left: 10px solid #00a0dc; box-shadow: 0 15px 35px rgba(0,0,0,0.1); }
    .user-avatar { width: 90px; height: 90px; background-color: #bdc3c7; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 45px; margin: auto; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 3. Pengurusan Sesi (Session State)
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "role" not in st.session_state:
    st.session_state["role"] = None
if "selected_view" not in st.session_state:
    st.session_state["selected_view"] = "Dashboard Utama"
if "selected_klinik" not in st.session_state:
    st.session_state["selected_klinik"] = None 
if "doctor_list" not in st.session_state:
    st.session_state["doctor_list"] = None 
if "selected_doctor" not in st.session_state:
    st.session_state["selected_doctor"] = None

apply_saas_theme()

# --- EXECUTION ROUTING ---
if not st.session_state["logged_in"]:
    show_login_page()
else:
    if st.session_state["role"] == "Admin":
        show_admin_dashboard()
    else:
        show_staff_dashboard()