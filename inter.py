import streamlit as st
import plotly.express as px
import pandas as pd

# 1. Konfigurasi Halaman Utama
st.set_page_config(page_title="HPU Performance System", layout="wide")

# 2. CSS Custom untuk UI Modul dan Login
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    .login-title { font-size: 3rem; font-weight: 700; color: #31333F; }
    .user-avatar { 
        width: 80px; height: 80px; background-color: #bdc3c7; 
        border-radius: 50%; display: flex; align-items: center; 
        justify-content: center; font-size: 40px; margin: auto; color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Pengurusan Sesi (Session State)
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["role"] = None
if "selected_view" not in st.session_state:
    st.session_state["selected_view"] = "Dashboard Utama"

# --- FUNGSI HALAMAN LOGIN (Split Screen) ---
def login_page():
    col_img, col_form = st.columns([1.5, 1], gap="large")
    with col_img:
        st.image("https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?q=80&w=2053", use_container_width=True)
    with col_form:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<div class="login-title">Selamat Datang</div>', unsafe_allow_html=True)
        with st.form("login_form"):
            role = st.selectbox("Log masuk sebagai:", ["Admin", "Staff (Doctor)"])
            user = st.text_input("Username")
            pwd = st.text_input("Password", type="password")
            if st.form_submit_button("Log Masuk", use_container_width=True):
                if pwd == "123": # Password simulasi
                    st.session_state["logged_in"] = True
                    st.session_state["role"] = role
                    st.rerun()
                else:
                    st.error("Password salah.")

# --- DATA CARTA NAVIGASI ---
data_nav = {
    "labels": [
        "HPU", "Clinical<br>Excellence", "Operational", "Interpersonal<br>Excellence",
        "Skills", "Knowledge &<br>Capacity", "Policies &<br>Protocols", "Documentation",
        "Productivity &<br>Efficiency", "Innovation &<br>Problem Solving",
        "Patient<br>Experience", "Emotional<br>Intelligence", "Teamwork &<br>Collaboration", "Mentorship"
    ],
    "parents": [
        "", "HPU", "HPU", "HPU",
        "Clinical<br>Excellence", "Clinical<br>Excellence", "Clinical<br>Excellence", "Clinical<br>Excellence",
        "Operational", "Operational",
        "Interpersonal<br>Excellence", "Interpersonal<br>Excellence", "Interpersonal<br>Excellence", "Interpersonal<br>Excellence"
    ],
    "colors": ["Base", "Clinical", "Operational", "Interpersonal"] + ["Clinical"]*4 + ["Operational"]*2 + ["Interpersonal"]*4
}
color_map = {"Base": "#ffffff", "Clinical": "#f1c40f", "Operational": "#9b59b6", "Interpersonal": "#2ecc71"}

# --- LOGIK UTAMA ---
if not st.session_state["logged_in"]:
    login_page()
else:
    # --- SIDEBAR NAVIGASI (Hanya jika Login) ---
    with st.sidebar:
        st.markdown('<div class="user-avatar">👤</div>', unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center;'><b>{st.session_state['role']} HPU</b></p>", unsafe_allow_html=True)
        st.write("---")
        
        if st.session_state["role"] == "Admin":
            st.write("**Navigasi Interaktif**")
            fig = px.sunburst(pd.DataFrame(data_nav), names='labels', parents='parents', color='colors', color_discrete_map=color_map)
            fig.update_traces(insidetextorientation='tangential', textinfo='label')
            fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=300)
            
            # Navigasi Klik
            event = st.plotly_chart(fig, use_container_width=True, on_select="rerun")
            if event and "selection" in event and event["selection"]["points"]:
                st.session_state["selected_view"] = event["selection"]["points"][0]["label"].replace("<br>", " ")

    # --- HALAMAN UTAMA ---
    view = st.session_state["selected_view"]
    
    # Header Dashboard
    c_title, c_logout = st.columns([5, 1])
    with c_title:
        st.title(f"Modul: {view if st.session_state['role'] == 'Admin' else 'Staff Home'}")
    with c_logout:
        if st.button("Log Keluar"):
            st.session_state.clear()
            st.rerun()
    st.divider()

    # Logik Paparan Ikut Peranan
    if st.session_state["role"] == "Staff (Doctor)":
        st.info("👋 Selamat datang, Doktor. Halaman anda sedang disediakan (Blank Page).")
    else:
        # Paparan Admin Berdasarkan Klik Carta
        if view == "Clinical Excellence":
            st.header("Kecemerlangan Klinikal")
            st.info("1) Skills | 2) Knowledge | 3) Policies | 4) Documentation")
        elif view == "Skills":
            st.subheader("Borang Penilaian: Skills")
            st.slider("Skor Kompetensi Teknikal", 0, 100, 80)
        elif view == "Operational":
            st.header("Operational Excellence")
            st.success("Produktiviti & Inovasi")
        elif "Dashboard Utama" in view or "HPU" in view:
            st.subheader("Ringkasan Prestasi Keseluruhan")
            m1, m2, m3 = st.columns(3)
            m1.metric("Clinical", "80%", "Sasaran: 80%")
            m2.metric("Operational", "1,240", "Target: >100")
            m3.metric("Interpersonal", "High", "PSQ18")
            st.info("Sila klik segmen carta di sidebar untuk modul spesifik.")