import streamlit as st
import plotly.express as px
import pandas as pd
import folium
import random
from streamlit_folium import st_folium
from datetime import date

from interpersonal_view import show_interpersonal_page
from clinical_view import show_clinical_page
from operational_view import show_operational_page

# --- MOCK LOCAL DATA (Updated for All States in Malaysia) ---
STATE_CENTERS = {
    "All States": {"lat": 4.2105, "lon": 101.9758, "zoom": 6},
    "Johor": {"lat": 2.0301, "lon": 103.3185, "zoom": 8},
    "Kedah": {"lat": 6.1184, "lon": 100.3685, "zoom": 9},
    "Kelantan": {"lat": 5.3117, "lon": 102.2125, "zoom": 8},
    "Kuala Lumpur": {"lat": 3.1390, "lon": 101.6869, "zoom": 11},
    "Labuan": {"lat": 5.2831, "lon": 115.2308, "zoom": 11},
    "Melaka": {"lat": 2.2008, "lon": 102.2501, "zoom": 10},
    "Negeri Sembilan": {"lat": 2.7258, "lon": 101.9424, "zoom": 9},
    "Pahang": {"lat": 3.8126, "lon": 103.3256, "zoom": 8},
    "Perak": {"lat": 4.5921, "lon": 101.0901, "zoom": 8},
    "Perlis": {"lat": 6.4449, "lon": 100.2048, "zoom": 10},
    "Pulau Pinang": {"lat": 5.4141, "lon": 100.3288, "zoom": 10},
    "Putrajaya": {"lat": 2.9264, "lon": 101.6964, "zoom": 12},
    "Sabah": {"lat": 5.3853, "lon": 116.8953, "zoom": 7},
    "Sarawak": {"lat": 2.5000, "lon": 113.0000, "zoom": 6},
    "Selangor": {"lat": 3.0738, "lon": 101.5183, "zoom": 9},
    "Terengganu": {"lat": 4.9081, "lon": 103.0044, "zoom": 8}
}

MOCK_KLINIK = [
    # Selangor & KL
    {"name": "KK Seksyen 7 Shah Alam", "lat": 3.0738, "lon": 101.5183, "state": "Selangor"},
    {"name": "Hospital Tengku Ampuan Rahimah", "lat": 3.0401, "lon": 101.4449, "state": "Selangor"},
    {"name": "Hospital Serdang", "lat": 2.9760, "lon": 101.7180, "state": "Selangor"},
    {"name": "KK Kajang", "lat": 2.9935, "lon": 101.7876, "state": "Selangor"},
    {"name": "Hospital Kuala Lumpur (HKL)", "lat": 3.1706, "lon": 101.7011, "state": "Kuala Lumpur"},
    {"name": "KK Jinjang", "lat": 3.2100, "lon": 101.6588, "state": "Kuala Lumpur"},
    # Johor
    {"name": "Hospital Sultanah Aminah", "lat": 1.4585, "lon": 103.7460, "state": "Johor"},
    {"name": "KK Mahmoodiah", "lat": 1.4550, "lon": 103.7400, "state": "Johor"},
    # Perak & Penang
    {"name": "Hospital Raja Permaisuri Bainun", "lat": 4.6033, "lon": 101.0905, "state": "Perak"},
    {"name": "Hospital Pulau Pinang", "lat": 5.4172, "lon": 100.3117, "state": "Pulau Pinang"},
    # Melaka & Negeri Sembilan
    {"name": "Hospital Melaka", "lat": 2.2223, "lon": 102.2592, "state": "Melaka"},
    {"name": "Hospital Tuanku Ja'afar", "lat": 2.7106, "lon": 101.9463, "state": "Negeri Sembilan"},
    # Pantai Timur
    {"name": "Hospital Tengku Ampuan Afzan", "lat": 3.8055, "lon": 103.3235, "state": "Pahang"},
    {"name": "Hospital Sultanah Nur Zahirah", "lat": 5.3250, "lon": 103.1504, "state": "Terengganu"},
    {"name": "Hospital Raja Perempuan Zainab II", "lat": 6.1246, "lon": 102.2458, "state": "Kelantan"},
    # Utara
    {"name": "Hospital Sultanah Bahiyah", "lat": 6.1498, "lon": 100.4068, "state": "Kedah"},
    {"name": "Hospital Tuanku Fauziah", "lat": 6.4414, "lon": 100.1916, "state": "Perlis"},
    # Borneo & WP
    {"name": "Hospital Queen Elizabeth", "lat": 5.9759, "lon": 116.0716, "state": "Sabah"},
    {"name": "Hospital Umum Sarawak", "lat": 1.5323, "lon": 110.3409, "state": "Sarawak"},
    {"name": "Hospital Putrajaya", "lat": 2.9293, "lon": 101.6742, "state": "Putrajaya"},
    {"name": "Hospital Labuan", "lat": 5.2830, "lon": 115.2494, "state": "Labuan"}
]

def generate_mock_doctors(clinic_name):
    # Generate random doctor data based on requested table format
    random.seed(hash(clinic_name)) 
    doctors = []
    names = ["Dr. Farhana", "Dr. Ah Meng", "Dr. Sarah", "Dr. David", "Dr. Ali", "Dr. Muthu", "Dr. Siti", "Dr. Chong", "Dr. Ramesh", "Dr. Aisyah"]
    
    for _ in range(random.randint(4, 8)):
        score = random.randint(60, 99)
        if score >= 85: status = "Outstanding"
        elif score >= 75: status = "Good"
        elif score >= 65: status = "Competent"
        else: status = "Needs Attention"
        
        doctors.append({
            "Officer Name": f"{random.choice(names)} ({random.randint(100,999)})",
            "Department": "Outpatient",
            "Current Score": score,
            "Status": status
        })
    return pd.DataFrame(doctors)


def show_admin_dashboard():
    # --- 1. SPECIAL CSS FOR MODERN DASHBOARD THEME ---
    st.markdown("""
        <style>
        .stApp { background-color: #f4f7fe; }
        
        div[data-testid="stVerticalBlock"] > div > div > div[data-testid="stVerticalBlock"] {
            background-color: white; border-radius: 15px; padding: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.02); border: 1px solid #f0f2f6;
        }
        
        .section-title { font-size: 16px; font-weight: bold; color: #2b3674; margin-bottom: 15px; }
        
        .sidebar-kpi {
            background: white; padding: 12px; border-radius: 12px; 
            border: 1px solid #f0f2f6; display: flex; align-items: center; 
            margin-bottom: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);
        }
        .sidebar-icon {
            width: 40px; height: 40px; border-radius: 50%; display: flex; 
            justify-content: center; align-items: center; font-size: 18px; margin-right: 12px;
        }
        .sidebar-text h3 { margin: 0; font-size: 18px; font-weight: 700; color: #2b3674; line-height: 1.1; }
        .sidebar-text p { margin: 0; font-size: 11px; color: #a3aed1; font-weight: 600; }
        </style>
    """, unsafe_allow_html=True)

    # --- 2. CHART DATA ---
    data_nav = {
        "labels": ["HPU", "Clinical<br>Excellence", "Operational", "Interpersonal<br>Excellence", "Skills", "Knowledge &<br>Capacity", "Policies &<br>Protocols", "Documentation", "Productivity &<br>Efficiency", "Innovation &<br>Problem Solving", "Patient<br>Experience", "Emotional<br>Intelligence", "Teamwork &<br>Collaboration", "Mentorship"],
        "parents": ["", "HPU", "HPU", "HPU", "Clinical<br>Excellence", "Clinical<br>Excellence", "Clinical<br>Excellence", "Clinical<br>Excellence", "Operational", "Operational", "Interpersonal<br>Excellence", "Interpersonal<br>Excellence", "Interpersonal<br>Excellence", "Interpersonal<br>Excellence"],
        "colors": ["Base", "Clinical", "Operational", "Interpersonal"] + ["Clinical"]*4 + ["Operational"]*2 + ["Interpersonal"]*4
    }
    color_map = {"Base": "#ffffff", "Clinical": "#4318FF", "Operational": "#39B8FF", "Interpersonal": "#05CD99"}

    if "sub_menu_cts" not in st.session_state:
        st.session_state["sub_menu_cts"] = "Clinical Excellence"
    if "selected_klinik" not in st.session_state:
        st.session_state["selected_klinik"] = None

    # --- 3. SIDEBAR ---
    with st.sidebar:
        # Custom Sidebar Header dengan Logo Jata Negara & Jarak Teks yang Dirapatkan
        st.markdown(
            """
            <div style="text-align:center; margin-top: -30px;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Coat_of_arms_of_Malaysia.svg/800px-Coat_of_arms_of_Malaysia.svg.png" width="75" style="margin-bottom: 0px;">
                <h2 style="color:#1E3A8A; font-weight:900; margin: 0px; padding: 0px; line-height: 1;">MyPrestasi</h2>
                <p style="color:#888; font-size:12px; margin: 0px; padding: 0px; margin-top: 2px;">Admin Portal</p>
                <hr style="margin-top: 15px; margin-bottom: 15px; border: 0; border-top: 1px solid #e6e6e6;">
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.markdown("<p style='font-size:13px; font-weight:bold; color:#a3aed1; margin-bottom:10px;'>📊 OVERALL STATISTICS</p>", unsafe_allow_html=True)
        
        # --- BASE64 ICONS ---
        ICON_HOSPITAL = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAACXBIWXMAAAsTAAALEwEAmpwYAAADY0lEQVR4nO3WPUyTQRgH8KrRxOhg4uDg4uLkZFyYbHjbu7cmUlpNxWCqqbFLBZWAQFAoGmqUL8Mkg4uOEicHB2N0se97tTZVsCioFWgQ0Wrl7QcW6N/cRVBUolDKR+w/eZKmvfb5tc/dpTrd/xKvJG33mUx3fbJ8X9Hrd+hWSnpstg0KIedVSuNhl2si7HJNqpQmGSHn/Xv2rF9W3KPCwr2M0nB3SYn2xeNB6upVUWOXLuF5aanGKI0okkSWHKZI0jaV0tu+ffsSI7W1AqVdvoyQ4zhCDge0K1fEcyM1NeBrmCx38ffkHHbLZlunGo1ljBDttdM5nmhtFZDBigo8LirCQGenKP54qKJCvMbXvDpxIq0SkmCEnILbvTYnuEcGw24my93BAwfGPl+8KJp/unABwZIS9LhcSITDmE5qaAih06cRtNkQbWgQa2NNTXh68KDmo/SlajQWLBrsgV6/hVHa6aM0OXTmTCbV3o54Swv6nE74zWa8v3MHyGTwp3x8+BB+qxW9Dgfi38c+fPZsxmcyJRVKbzGDYWtWOK/ReEgl5HOv3Z6absD33BOLBf0eDyZiMfwtE5qGcEcH/MXFiFRWgX9BrbkZ/Q7HOKM05iXkGHS6NfOCKUbjTp/J5A2YzfGo2z0zom67Hc/4IQiFMN/E+/rQ7XTiWWkpZrZIYyMCVmucyXKAFRbu+vsvVlCwkVHqYZTGB8rLJ5Pt7WKTv3GdFON819WFzNQUFpxMRmyJx2Yz+p1OsVU4NFJZOckoTaiEXHug12/+M06SilRK3/ccPpzk99jMOK1WvKipwdfRUSxW0tEo+pua4LdYMFJd/eOastuTTJajXkmyzcIxk+mef//++Idz58TiL/yiPXoUwSNHEAsEkKvEAgHRg/fiPXlvbuAWbvqx5wwG8HEm29rwtqxM3GORGzcwlU4j15lKpxG5eVOM/W15uTBwCzfNAn6sr4ev2CLur+TgIJY648PD6K2uhmouxmhd3e9ARumHjio3ljsdVW5hmQ2UpOYgIZtqW64v+IMVg2FWLTTcwC3c9NtJzhaY+v5vJlvgnPdgHvgPyQNTyw389bQqP9XPwLlqSYDTkNQ8Kw9cFSNe8Ydkrih5oC4PXH6gskh.png" 
        ICON_STAFF = "data:image/png;base64,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" 
        ICON_CHART = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAACXBIWXMAAAsTAAALEwEAmpwYAAABwklEQVR4nO2VP0vDQBjGTxRXBRdFd3HwM4j9AG5ZbO9N61DURQTvrooljuLg4tTe0VaoSwdFB4dgJ8GtH0CnguIgjrpaefsHamyosUmawj1wJLxJuF+e90leQrRGWKCYAMUbzkWipI3S/uFWOft5/XjbsOvV6AEaFWsyWRD3m+XsF0JGCjCu2CJIXgPJr5KFzOn2hfURKmAiL2Kg2BppkDHnNVOyNJXsDY+dWqqYyYYCaFSMcVDcopK/tB2qdUDpeWaGSn6JNXTQ+SyV7ChQOLO4N0slv8OF5wiFcF2gzyD5CWaPhK1EXsSariluoYs/LrZB8Z7AAECx1V6ZMrpaGiiAq1pvL0CxV2emTGdLw1Y6J6bwNwCSP8TzfMGZKerW0jCULIhlKvkTVezsV6h9yhT8d9RRKdZBsneQPDUIQD8hEI64zuoLuGJZE1TyY3QOHSQBC7wAQml3HrMGit2YxZ3poOE8AcZzB3PNr1Qx0Ws0RcJBKvmSHxuCh9B7zqAfgLaHDTXgXzd0a/3AgH5lCjzWQ28ZaMD6YJmCYQDaAdZ7ggTpCPgBOAwQ0IB1DdiSBlQasKoB7ZEHBJdRN4w6GRV9A4g3/DjDTM9MAAAAAElFTkSuQmCC" 
        ICON_CHECK = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAACXBIWXMAAAsTAAALEwEAmpwYAAAEkUlEQVR4nN2YX0xbdRTHr/9988UHk71ojIkmxhdfjC8kZmNt7700urCYGTs392R0S9R1cUJKNJsRnNAIlNL7r7ARZAtbdM7R+/v1Mhg6oAwMuE7+yPgrf0ub9rZIgWN+rHEwgd62txg9yTe5uffhfO75nd85v/OjqP+zXXXmPi+76E+UGnMzlphRxNNBxNMhLDJjXolt9XAmG3IZXtpRKJvN9qDHZTyERXZMkczqr+iD2HTvKVgY+Bpi41UQm3BCcLAUpntPg997bLG5xhzGAj0lc4b3FFvOw1mF8zgNOVhghn++cCAc6D8DEKgBCNQmVXCwDDoaLREsMpOyK9eQFTiZNx3FIqtO932hCQo20Zy/GBR3nooFpkBXOCyyFa11+yLRMUfacJDQ4kQ1tNXvj3hF9hwA9YAukSNw8Wk+YzhIaHlWgp++fTOCBJMt85wTWVWPyMH9kZx0guI2qzJvZNKCa2jIfwhLzFAmOQdJNP9bCZAd3tCQ/2jKgDJnOHzj/IFwtuAgId+ldyIyZ/wwZUBS5+6WkuwChoe/AcTTC6S+aobzuEwvkHKgtc5Bhmqp2xfyVBte0b68gqngFj66uBNwEKiFgZaPl5FIn9EMSHrrVO+prMCM/F79z81yuwS87rxezYBYZEZJP9UbrrHtKzjInQDcZd/wPjJSTvIwpBkQCXSQNH694SycdU0HeSv84q/8+1t8RgAPZ4xrj6DABMipJBtwFs4Kxd99DktzNRs6i8wZlzQDKu68wdCQfUfgIFALpFNhiZ3RDiiZb8z5v9wROEgcxxTJfFsT3BW74TEkMj0TN4u2db6ZI9gGruT7zeGIZvpOAxaYAU0tDwu0o/OiJUoSdyvnzTftcKK+EAKTQkaRu7dJxMSBlq5ICoh4kxod23oHK132tVJBHFvrC2DhPshUIrcxD6tA5umwBkA6FJvYGrDnViUcFu8CWjgrHF8XyVQjt17EJxboYPIl5tmyjsa31e3qoK+vHA4J9yCt9QVQ11ycVuTW4MaroOOiRcWCqTQpoM/58iNIZEvI33RfPhLVCmlJE65Pfj9GGgPxSXxTWk127n5C5kyxpT84zZG0pAi3MisBEugoctC7NINtWG43e/5O+8mV7Zz0rMvJVHKOaLy7CBSJRVS6dtWZ++q1s6+HV+e3d+rrK4fSH1KDI2fN6+fywxnPyV6J9U32fLaq3XGtJpFZB4tsf8ajZ1O18bWWs2+EV+fcusGtztfC9br9YY9zbx6lh2GRbR1uPxnXC3DUV7iCJaZbl8GdmMex+zks0iqZZTOF+3PSRZZWbeL2vEjpaZini9ovvBVJtmEgydJ2XrJEEE8XU3obGQvJUg+0fJT2MDXUdjxONl3WruEUJ/MkuQkY7SxMOR/HumzLSKBnFdH0FJVN+9Gx92ksMlMj7QXLWuFGOj5dQQIzg52GZ7MKtwGSZ/q7L78bXpra+tYrPi1Az5UjKhKYwabqPc9QO2nk5I1FtgLxdMyvHFsMDZWtDT9E5Jm8I9+8AlOpiDmPU/+WIQe9C/FsiVdi75DJjIg8k3dpHwL+S/YX14zjyU25G48AAAAASUVORK5CYII=" 

        st.markdown(f"""
            <div class="sidebar-kpi">
                <div class="sidebar-icon" style="background:#E2E8FF;"><img src="{ICON_HOSPITAL}" width="26" height="26"></div>
                <div class="sidebar-text"><h3>21</h3><p>Active Facilities</p></div>
            </div>
            <div class="sidebar-kpi">
                <div class="sidebar-icon" style="background:#E6F8F3;"><img src="{ICON_STAFF}" width="26" height="26"></div>
                <div class="sidebar-text"><h3>394</h3><p>Total Staff</p></div>
            </div>
            <div class="sidebar-kpi">
                <div class="sidebar-icon" style="background:#FFF2E5;"><img src="{ICON_CHART}" width="26" height="26"></div>
                <div class="sidebar-text"><h3>82%</h3><p>Average Performance</p></div>
            </div>
            <div class="sidebar-kpi">
                <div class="sidebar-icon" style="background:#FEECEF;"><img src="{ICON_CHECK}" width="26" height="26"></div>
                <div class="sidebar-text"><h3>1,250</h3><p>Evaluations Completed</p></div>
            </div>
        """, unsafe_allow_html=True)

        st.write("")
        st.markdown("<p style='font-size:13px; font-weight:bold; color:#a3aed1; margin-bottom:10px;'>⚙️ ADMINISTRATION MENU</p>", unsafe_allow_html=True)
        
        if st.button("Settings", icon=":material/settings:", width="stretch", key="btn_tetapan"):
            st.toast("Settings page opened.")
        if st.button("Reports", icon=":material/description:", width="stretch", key="btn_laporan"):
            st.toast("Reports page opened.")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        if st.session_state["selected_view"] != "Main Dashboard" or st.session_state["selected_doctor"]:
            if st.button("Back to Dashboard", icon=":material/arrow_back:", width="stretch"):
                st.session_state["selected_doctor"] = None
                st.session_state["selected_klinik"] = None 
                st.session_state["selected_view"] = "Main Dashboard"
                st.rerun()
        
        if st.button("Logout", icon=":material/logout:", type="primary", width="stretch"):
            st.session_state.clear()
            st.rerun()

    # --- 4. ROUTING EXECUTION ---
    view = st.session_state["selected_view"]

    # --- CSS GLOBAL UNTUK SEMUA BUTANG MENU DI DALAM SUB-MODUL ---
    if view in ["CTS", "FMS"]:
        st.markdown("""
        <style>
        /* Mensasarkan butang-butang menu (di dalam kolum/stHorizontalBlock) */
        div[data-testid="stHorizontalBlock"] div.stButton > button {
            height: 75px !important;
            border-radius: 12px !important;
            border: 1px solid #f0f2f6 !important;
            box-shadow: 0 4px 10px rgba(0,0,0,0.03) !important;
            transition: all 0.3s ease !important;
            background-color: #ffffff !important;
        }
        
        div[data-testid="stHorizontalBlock"] div.stButton > button:hover {
            border-color: #4318FF !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 15px rgba(67,24,255,0.1) !important;
        }

        /* ====================================================
           KOD UNTUK MEMBESARKAN & MENEBALKAN TEKS BUTANG MENU
           ==================================================== */
        div[data-testid="stHorizontalBlock"] div.stButton > button p {
            font-size: 18px !important; /* Saiz dibesarkan */
            font-weight: 800 !important; /* Tulisan ditebalkan (Bold) */
            color: #2b3674 !important; /* Warna biru gelap tema */
            margin: 0 !important;
        }

        /* Gaya untuk butang yang sedang AKTIF (Primary) */
        div[data-testid="stHorizontalBlock"] div.stButton > button[kind="primary"] {
            background-color: #E2E8FF !important; /* Latar biru cair elegan */
            border: 2px solid #4318FF !important; /* Bingkai biru terang */
        }
        
        div[data-testid="stHorizontalBlock"] div.stButton > button[kind="primary"] p {
            color: #4318FF !important; /* Warna teks biru terang untuk butang aktif */
        }
        </style>
        """, unsafe_allow_html=True)

    if view == "CTS":
        st.title("⚕️ Cardiothoracic Surgery (CTS) Module")
        st.markdown("Please select an evaluation sub-module below:")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🩺 Clinical Excellence", use_container_width=True, type="primary" if st.session_state["sub_menu_cts"] == "Clinical Excellence" else "secondary"):
                st.session_state["sub_menu_cts"] = "Clinical Excellence"
                st.rerun()
        with c2:
            if st.button("⚙️ Operational", use_container_width=True, type="primary" if st.session_state["sub_menu_cts"] == "Operational" else "secondary"):
                st.session_state["sub_menu_cts"] = "Operational"
                st.rerun()
        with c3:
            if st.button("🤝 Interpersonal Excellence", use_container_width=True, type="primary" if st.session_state["sub_menu_cts"] == "Interpersonal Excellence" else "secondary"):
                st.session_state["sub_menu_cts"] = "Interpersonal Excellence"
                st.rerun()
        st.divider()

        if st.session_state["sub_menu_cts"] == "Clinical Excellence": show_clinical_page(module_type="CTS")
        elif st.session_state["sub_menu_cts"] == "Operational": show_operational_page()
        elif st.session_state["sub_menu_cts"] == "Interpersonal Excellence": show_interpersonal_page()

    elif view == "FMS":
        if "sub_menu_fms" not in st.session_state:
            st.session_state["sub_menu_fms"] = "Clinical Excellence"
            
        st.title("🩺 Family Medicine Specialist (FMS) Module")
        st.markdown("Please select an evaluation sub-module below:")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("🩺 Clinical Excellence", use_container_width=True, type="primary" if st.session_state["sub_menu_fms"] == "Clinical Excellence" else "secondary", key="fms_clin"):
                st.session_state["sub_menu_fms"] = "Clinical Excellence"
                st.rerun()
        with c2:
            if st.button("⚙️ Operational", use_container_width=True, type="primary" if st.session_state["sub_menu_fms"] == "Operational" else "secondary", key="fms_op"):
                st.session_state["sub_menu_fms"] = "Operational"
                st.rerun()
        with c3:
            if st.button("🤝 Interpersonal Excellence", use_container_width=True, type="primary" if st.session_state["sub_menu_fms"] == "Interpersonal Excellence" else "secondary", key="fms_int"):
                st.session_state["sub_menu_fms"] = "Interpersonal Excellence"
                st.rerun()
        st.divider()

        if st.session_state["sub_menu_fms"] == "Clinical Excellence": show_clinical_page(module_type="FMS")
        elif st.session_state["sub_menu_fms"] == "Operational": show_operational_page()
        elif st.session_state["sub_menu_fms"] == "Interpersonal Excellence": show_interpersonal_page()

    elif st.session_state["selected_doctor"]:
        col_prof, col_prog = st.columns([1, 1])
        with col_prof:
            st.title(f"🔍 Profile: {st.session_state['selected_doctor']}")
            st.caption("Department: Emergency | ID: HPU-9921 | Last Evaluation: Jan 15, 2026")
        with col_prog:
            st.write("")
            st.progress(0.75, text="Evaluation Form Progress: 75%")
        st.info("Use the 'Back to Dashboard' button in the menu to return.")

    # --- MAIN DASHBOARD ---
    else:
        # 1. Tajuk Main Dashboard diperbesarkan dan dirapatkan mengikut lakaran
        st.markdown("<h1 style='color:#1E3A8A; font-weight:900; font-size: 3.2rem; margin-top: -20px; margin-bottom: 0px;'>Main Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color:#a3aed1; font-size: 1.2rem; margin-top: 5px; margin-bottom: 30px;'>Please select a module or monitor facilities.</p>", unsafe_allow_html=True)

        # -- BASE64 ICONS UNTUK BUTANG MODUL --
        # Kita menggunakan ikon yang SAMA TEPAT dengan panel KPI kiri
        ICON_HOSPITAL = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAACXBIWXMAAAsTAAALEwEAmpwYAAADY0lEQVR4nO3WPUyTQRgH8KrRxOhg4uDg4uLkZFyYbHjbu7cmUlpNxWCqqbFLBZWAQFAoGmqUL8Mkg4uOEicHB2N0se97tTZVsCioFWgQ0Wrl7QcW6N/cRVBUolDKR+w/eZKmvfb5tc/dpTrd/xKvJG33mUx3fbJ8X9Hrd+hWSnpstg0KIedVSuNhl2si7HJNqpQmGSHn/Xv2rF9W3KPCwr2M0nB3SYn2xeNB6upVUWOXLuF5aanGKI0okkSWHKZI0jaV0tu+ffsSI7W1AqVdvoyQ4zhCDge0K1fEcyM1NeBrmCx38ffkHHbLZlunGo1ljBDttdM5nmhtFZDBigo8LirCQGenKP54qKJCvMbXvDpxIq0SkmCEnILbvTYnuEcGw24my93BAwfGPl+8KJp/unABwZIS9LhcSITDmE5qaAih06cRtNkQbWgQa2NNTXh68KDmo/SlajQWLBrsgV6/hVHa6aM0OXTmTCbV3o54Swv6nE74zWa8v3MHyGTwp3x8+BB+qxW9Dgfi38c+fPZsxmcyJRVKbzGDYWtWOK/ReEgl5HOv3Z6absD33BOLBf0eDyZiMfwtE5qGcEcH/MXFiFRWgX9BrbkZ/Q7HOKM05iXkGHS6NfOCKUbjTp/J5A2YzfGo2z0zom67Hc/4IQiFMN/E+/rQ7XTiWWkpZrZIYyMCVmucyXKAFRbu+vsvVlCwkVHqYZTGB8rLJ5Pt7WKTv3GdFON819WFzNQUFpxMRmyJx2Yz+p1OsVU4NFJZOckoTaiEXHug12/+M06SilRK3/ccPpzk99jMOK1WvKipwdfRUSxW0tEo+pua4LdYMFJd/eOastuTTJajXkmyzcIxk+mef//++Idz58TiL/yiPXoUwSNHEAsEkKvEAgHRg/fiPXlvbuAWbvqx5wwG8HEm29rwtqxM3GORGzcwlU4j15lKpxG5eVOM/W15uTBwCzfNAn6sr4ev2CLur+TgIJY648PD6K2uhmouxmhd3e9ARumHjio3ljsdVW5hmQ2UpOYgIZtqW64v+IMVg2FWLTTcwC3c9NtJzhaY+v5vJlvgnPdgHvgPyQNTyw389bQqP9XPwLlqSYDTkNQ8Kw9cFSNe8Ydkrih5oC4PXH6gskh.png" 
        ICON_STAFF = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAACXBIWXMAAAsTAAALEwEAmpwYAAAG1ElEQVR4nN3We1BT2R0HcKbd3c5sd7p/dPtP/+rf/tVZEru2ldpuEhKQJKhh64hbdiuxi0uRl+R5bxKCKKDICCQ3Dx4moEJkXVkIUbdACAQkuquy7mIB91VktFUCSRAffDv3Dmx9gCQBdaZn5juTnJzc88nvnntOYmL+X5pcGPtHVTKrSSVmTyhErLsKEfuOKnntoFLIjnuhMFKy5jV1MttFbPpN4PD7b8/V7kqAfXcS7FlJMKZzoU5mB1TJbO0LwUmlsS8rxewLJdvWzzTsTkJjtvCJ2LI2gti0NqAUxubQP+a5ApViFlH0zm+DjdmL4xrnY83go1Cyzq8SsybLszboLBr+GRPBu1mt5Nw1qrh3rCT/kkHBTSNJ8kerhiMla15RitlT9C19Gq5xPvX5iTCpeGgp3/Jg6OTfMdGjhn+wEJPndPinMxf2YmHIQvA7KzL5P1kVoFz05nqt5K3J5WDWDD4O7dqAel0ivvtUhuCFokUzfV6PtqqtIRPB/2hVgAoRK6MkNS70NBy1k4eS9DjYipJwu1+7JG4hU4OFsOmTQmaCP06peSWludyfrqCCLEX5u394QEMasoWoy0xkUvthAigpD6Xb41CSFgcrKcD1buWyuIcz3qXAJ1V/nrEQ8b4mieTH0VVQzJLSFTR/EA9dyjrot/4Oxdt+j33b18OYyYfHko6Boztx2rQ9bNjkgBaB8/Pvz+vRXLZpulLBTYsKKBPH8nQp6yZ1krfgs2UsOmHLIQmutueEhfuPV4PGfWI07BP9UPErrbthIfmeqID0nqYQs2cUYhb85woXnbRWl4B/95HL4uiHx7ZXiEFHLoZdWtQVJjLgGx41TOr4W1EBDfI/rdFvWzejELGWnNio4mLap3+kb+EW+ge0GDudj9PUdtRoE3D1jBYYszH5R93f0FX3HvPQGJTce1EBq+WcXLsu6f7TgBYNH7f6NUw1nIZUmAk+DEoOqhUcmIl4NB9Mge9EPmauWH7A0bl5rgL1+kRmjzQoObPRVVD59oZanWCKnmwpoOPAZoy68nGyIgVu+y7MDtc8Alkq967WgVJxmVtvIfjfxETbKHV8q0HBwbRv8TXYa9+B7vr3Qal4CF0xh4VbCP3DvXbpfYrgUVED6bPTpOb56X1rMaDHvgNWjYCZLBLcArCuMHGOUsaXxaykmcl4R19D+r3FgFaNAI7yd6IGHi/bQlc/uCJgpYL7a0odH5roUT0BtBcL8aWLiBr4RTsBCykYj1lpMyp4UqtWwGwbDwP7j0rRZng3auDHh1ODFMFXxqxGoy9YoxXgxMHNzElAx3FwCyyaBFQrOZgbORI2jh5Lf8eiETgpaezLqwYc7chFV00as/HSp0hXbRrTRxF8BC5TYQOnLxvpE8S/IpAw/+Qvk+RtezYRrnNitfPWIZVkrteejjFX3iPptaXDpElijrBwgV92aOjqnYkKtpE89apY3W4UqZwhaYVvRm4fQ9HJGyhr8sFICtFZk4Yrp7KYdNa8x/SVW+ywlWzFg9H6ZXEPRuphKxZNVyk4iRHjRAXOX4lVHaN/LR8IFZ+6iVLn5CMpO3EJhgPZMBCJTKoP5OCA4zLzmeFgDrqOZACjT1mLo0fQWf8BLISgM5rKvSFWOb/LMg/dexwWTspax2EiBHBZdiA4ZHoCR69Rl3kHzCQfVAHn9YiBYmX7xzsrL9yJBlc6H/pB6j+eDas2Aaet6Zi6aIT/ooF5Tff1N2UzYyLHKVrXbiZcwf1tt7BSIMZsuDtcg0FHHuqLhEzo13Tfwv4XMTBZ5bRkmYbuR4xqvw294xuQ9i+grPXBqN6Iyc+rllyDtz+rYtauzOz9Vkb1n8it7N1CUr5XlwcSrm/J5n9FBNM1jUJuHkBx8xBs3utouxpES0cLjh9KZf5OPY67O1yLY+Xb0NLxETP2SN917G265N9D9d3OM/buIsnOl5YEihTtQaGiDeEkWdWOrMoe6I5+jtbhANwT+F+uz+F4w37Y96fgWlcxc1vpXOvcC9s+CZoaSpkxD3+n9asA9EcvBmTmPq/s8MDPY1bS5BXuXxRQ3u+ps1/Pdj82kfuhfNLThYbKD5kNnI69KhOtnu4lx9PXMpy5NktfO4fqfCMqHNk09IrM7P2M+vTr2aUmcq8wxrPXZmVm73kp5Yv8fM439hYUHbsY6H5GODddyQlg77FLgTyjJyciXAHle30P1TftHJ15Zjj3fJwjMyig+qYyK/p/FjYwt7rnL/sdQ/5njXPPp6T58lRelSc1bKDM3H+2cfDGc8G5JwB6LrnZ64oA6B13joSeG7B9JASZyft92MB8gyeUV+3Bc04wbOCLbP8FL4tuIiE74GsAAAAASUVORK5CYII=" 
        ICON_MODUL_LOCK = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

        # 2. CSS Khas - Memastikan ia menumpukan pada susunan st.columns yang PERTAMA di Main Dashboard
        st.markdown(f"""
        <style>
        /* TARGET TEPAT KEPADA BUTANG STREAMLIT SAHAJA */
        section[data-testid="stMain"] div[data-testid="stHorizontalBlock"]:first-of-type div.stButton > button {{
            height: 90px !important; 
            border-radius: 12px !important;
            background-color: white !important; 
            border: 1px solid #f0f2f6 !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.02) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important; /* Teks berada di tengah */
            transition: all 0.3s ease !important;
        }}

        /* Kesan Hover */
        section[data-testid="stMain"] div[data-testid="stHorizontalBlock"]:first-of-type div.stButton > button:hover {{
            border-color: #4318FF !important;
            box-shadow: 0 6px 15px rgba(67,24,255,0.1) !important;
            transform: translateY(-3px) !important;
        }}

        /* ====================================================
           KOD BARU: MEMBESARKAN & MENEBALKAN TEKS DALAM BUTANG 
           ==================================================== */
        section[data-testid="stMain"] div[data-testid="stHorizontalBlock"]:first-of-type div.stButton > button p {{
            margin: 0 !important;
            padding: 0 !important;
            font-size: 20px !important; /* SAIZ FONT DIBESARKAN */
            font-weight: 800 !important; /* TULISAN DITEBALKAN (BOLD) */
            color: #2b3674 !important; /* WARNA BIRU GELAP TEMA */
        }}

        /* Butang 1 (CTS): Ikon Hospital + Latar Biru Cair */
        section[data-testid="stMain"] div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="column"]:nth-child(1) div.stButton > button {{
            background: 
                url('{ICON_HOSPITAL}') no-repeat 20px center / 28px,
                radial-gradient(circle 24px at 34px 50%, #E2E8FF 99%, transparent 100%),
                white !important;
            padding-left: 50px !important; /* Menolak teks ke kanan sikit supaya tak langgar ikon */
        }}

        /* Butang 2 (FMS): Ikon Staff + Latar Hijau Cair */
        section[data-testid="stMain"] div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="column"]:nth-child(2) div.stButton > button {{
             background: 
                url('{ICON_STAFF}') no-repeat 20px center / 28px,
                radial-gradient(circle 24px at 34px 50%, #E6F8F3 99%, transparent 100%),
                white !important;
             padding-left: 50px !important;
        }}

        /* Butang 3 & 4 (Dikunci): Ikon Lock + Latar Kelabu */
        section[data-testid="stMain"] div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="column"]:nth-child(n+3) div.stButton > button {{
            background: 
                url('{ICON_MODUL_LOCK}') no-repeat 24px center / 20px,
                radial-gradient(circle 24px at 34px 50%, #f0f2f6 99%, transparent 100%),
                #fbfbfb !important;
            padding-left: 50px !important;
        }}
        
        /* Warna teks dikelabukan untuk butang yang belum siap (Soon) */
        section[data-testid="stMain"] div[data-testid="stHorizontalBlock"]:first-of-type div[data-testid="column"]:nth-child(n+3) div.stButton > button p {{
            color: #a3aed1 !important;
        }}
        </style>
        """, unsafe_allow_html=True)

        col_m1, col_m2, col_m3, col_m4 = st.columns(4, gap="medium")
        with col_m1:
            if st.button("CTS Module", use_container_width=True, key="btn_top_cts"):
                st.session_state["selected_view"] = "CTS"
                st.session_state["selected_doctor"] = None
                st.rerun()
        with col_m2:
            if st.button("FMS Module", use_container_width=True, key="btn_top_fms"):
                st.session_state["selected_view"] = "FMS"
                st.session_state["selected_doctor"] = None
                st.rerun()
        with col_m3:
            st.button("Unavailable", use_container_width=True, disabled=True, key="btn_top_soon1")
        with col_m4:
            st.button("Unavailable", use_container_width=True, disabled=True, key="btn_top_soon2")

        st.write("---")

        # -- BARIS 1: PETA, CARTA BAR, & CARTA PIE --
        st.write("")

        # 1. Marker & CSS Khusus untuk membingkaikan KESELURUHAN KOLUM
        st.markdown('<div class="chart-row-marker"></div>', unsafe_allow_html=True)
        st.markdown("""
        <style>
        /* Mensasarkan kolum tepat selepas marker untuk dijadikan 'kad' putih */
        div.element-container:has(.chart-row-marker) + div[data-testid="stHorizontalBlock"] > div[data-testid="column"] > div[data-testid="stVerticalBlock"] {
            background-color: white !important;
            border-radius: 16px !important;
            box-shadow: 0 6px 15px rgba(0,0,0,0.04) !important;
            padding: 20px !important;
            border: 1px solid #f0f2f6 !important;
            height: 100% !important;
        }
        
        /* Membulatkan bucu peta Folium supaya sepadan dengan kad */
        div.element-container:has(.chart-row-marker) + div[data-testid="stHorizontalBlock"] iframe {
            border-radius: 10px !important;
            border: 1px solid #e6e6e6 !important;
        }
        </style>
        """, unsafe_allow_html=True)

        title_style = "font-size: 16px; font-weight: 800; color: #2b3674; margin-bottom: 15px; display: flex; align-items: center; gap: 8px;"

        col_map, col_bar, col_pie = st.columns([1.2, 1, 1], gap="large")

        # --- LAYOUT 1: PETA (KIRI) ---
        with col_map:
            st.markdown(f"<div style='{title_style}'>📍 Facility Map</div>", unsafe_allow_html=True)
            
            # Pastikan state wujud sebelum peta dipaparkan
            if "pilihan_negeri" not in st.session_state:
                st.session_state["pilihan_negeri"] = "All States"

            pusat_peta = STATE_CENTERS[st.session_state["pilihan_negeri"]]
            if st.session_state["pilihan_negeri"] == "All States":
                klinik_dipaparkan = MOCK_KLINIK
            else:
                klinik_dipaparkan = [k for k in MOCK_KLINIK if k["state"] == st.session_state["pilihan_negeri"]]

            m = folium.Map(location=[pusat_peta["lat"], pusat_peta["lon"]], zoom_start=pusat_peta["zoom"])
            for k in klinik_dipaparkan:
                folium.Marker([k["lat"], k["lon"]], tooltip=k["name"]).add_to(m)
            
            out = st_folium(m, width="100%", height=280, key=f"map_{st.session_state['pilihan_negeri']}")

            if out and out.get("last_object_clicked"):
                lat = out["last_object_clicked"]["lat"]
                lon = out["last_object_clicked"]["lng"]
                for k in klinik_dipaparkan:
                    if abs(k["lat"] - lat) < 0.01 and abs(k["lon"] - lon) < 0.01:
                        if st.session_state.get("selected_klinik") != k["name"]:
                            st.session_state["selected_klinik"] = k["name"]
                            st.session_state["doctor_list"] = generate_mock_doctors(k["name"])
                            st.rerun()
                        break
            
            # -- FILTER NEGERI DIPINDAHKAN KE SINI (BAWAH PETA) --
            st.write("") # Beri sedikit jarak ruang
            senarai_negeri = list(STATE_CENTERS.keys())
            negeri_dipilih = st.selectbox(
                "Pilih Negeri:", 
                senarai_negeri, 
                index=senarai_negeri.index(st.session_state["pilihan_negeri"]),
                label_visibility="collapsed" 
            )
            
            if negeri_dipilih != st.session_state["pilihan_negeri"]:
                st.session_state["pilihan_negeri"] = negeri_dipilih
                
                # --- LOGIK BAHARU: AUTO-PAPAR JADUAL BILA NEGERI DIPILIH ---
                if negeri_dipilih != "All States":
                    # Cari senarai klinik dalam negeri yang dipilih
                    klinik_negeri = [k["name"] for k in MOCK_KLINIK if k["state"] == negeri_dipilih]
                    if klinik_negeri:
                        # Pilih klinik pertama secara automatik dan jana senarai staf
                        st.session_state["selected_klinik"] = klinik_negeri[0]
                        st.session_state["doctor_list"] = generate_mock_doctors(klinik_negeri[0])
                else:
                    # Jika kembali ke "All States", kosongkan jadual
                    st.session_state["selected_klinik"] = None
                    
                st.rerun()

        # --- LAYOUT 2: CARTA BAR (TENGAH) ---
        with col_bar:
            st.markdown(f"<div style='{title_style}'>📊 Evaluations by Module</div>", unsafe_allow_html=True)
            
            df_bar = pd.DataFrame({
                "Module": ["CTS", "FMS", "Pediatrics", "O&G"],
                "Count": [120, 95, 60, 45]
            })
            fig_bar = px.bar(
                df_bar, x="Module", y="Count", color="Module", text="Count",
                color_discrete_sequence=["#4318FF", "#39B8FF", "#05CD99", "#f1c40f"]
            )
            fig_bar.update_traces(textposition='outside', marker_line_width=0, opacity=0.9) 
            fig_bar.update_layout(
                height=280,
                margin=dict(l=0, r=0, t=15, b=0), 
                showlegend=False,
                xaxis_title=None,
                yaxis_title=None,
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False), 
                yaxis=dict(showgrid=False, showticklabels=False)
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

        # --- LAYOUT 3: CARTA PIE / DONUT (KANAN) ---
        with col_pie:
            st.markdown(f"<div style='{title_style}'>🍩 Competency Breakdown</div>", unsafe_allow_html=True)
            
            df_pie = pd.DataFrame({
                "Status": ["Outstanding", "Good", "Competent", "Needs Attention"],
                "Value": [25, 45, 20, 10]
            })
            fig_pie = px.pie(
                df_pie, names="Status", values="Value", hole=0.6, 
                color_discrete_sequence=["#05CD99", "#39B8FF", "#f1c40f", "#FF4B4B"]
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent', marker=dict(line=dict(color='#ffffff', width=2))) 
            fig_pie.update_layout(
                height=280,
                margin=dict(l=0, r=0, t=10, b=0),
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                annotations=[dict(text='Status', x=0.5, y=0.5, font_size=14, showarrow=False, font_weight='bold', font_color='#a3aed1')] 
            )
            st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})

        st.write("---")

        # -- BARIS 2: SENARAI STAF (Penuh) --
        st.markdown("<div class='section-title'>📋 Staff Evaluation List</div>", unsafe_allow_html=True)
        if st.session_state.get("selected_klinik"):
            st.markdown(f"Location: <span style='color:#05CD99; font-weight:bold;'>{st.session_state['selected_klinik']}</span>", unsafe_allow_html=True)
            df_docs = st.session_state["doctor_list"]
            
            event_df = st.dataframe(
                df_docs, use_container_width=True, height=250, hide_index=True,
                on_select="rerun", selection_mode="single-row"
            )
            if event_df.selection.rows:
                idx = event_df.selection.rows[0]
                st.session_state["selected_doctor"] = df_docs.iloc[idx]["Officer Name"]
                st.rerun()
        else:
            st.info("Please select a location (pin) on the Facility Map above to display the staff list.")

        st.write("---")

        # -- BARIS 3: CARTA BULATAN & KAD LOG (Bersebelahan) --
        row3_col1, row3_col2 = st.columns([1, 1], gap="large")

        with row3_col1:
            st.markdown("<div class='section-title'>🧭 Evaluation Module Categories</div>", unsafe_allow_html=True)
            fig = px.sunburst(pd.DataFrame(data_nav), names='labels', parents='parents', color='colors', color_discrete_map=color_map)
            fig.update_traces(insidetextorientation='tangential', textinfo='label', textfont_size=11)
            fig.update_layout(margin=dict(t=0, l=0, r=0, b=0), height=320, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            
            event = st.plotly_chart(fig, use_container_width=True, on_select="rerun")
            if event and "selection" in event and event["selection"]["points"]:
                label_raw = event["selection"]["points"][0]["label"]
                st.session_state["selected_view"] = "CTS" 
                if "Clinical" in label_raw: st.session_state["sub_menu_cts"] = "Clinical Excellence"
                elif "Operational" in label_raw: st.session_state["sub_menu_cts"] = "Operational"
                elif "Interpersonal" in label_raw: st.session_state["sub_menu_cts"] = "Interpersonal Excellence"
                st.rerun()

        with row3_col2:
            st.markdown("<div class='section-title'>📈 Monthly Activity</div>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4318FF 0%, #865CFF 100%); padding: 25px 20px; border-radius: 15px; color: white; height: 100%; min-height: 290px; box-shadow: 0 10px 20px rgba(67, 24, 255, 0.2); display: flex; flex-direction: column; justify-content: center;">
                <h3 style="margin:0; font-size: 48px; font-weight: bold; color:white;">124</h3>
                <p style="margin:0 0 20px 0; font-size: 16px; opacity: 0.9;">Evaluations this month</p>
                <div style="font-size: 14px; line-height: 2; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 15px;">
                    <p style="margin:0;">• <b>09:45 AM</b>: Dr. Raju's score verified.</p>
                    <p style="margin:0;">• <b>08:20 AM</b>: CPD Certificate uploaded.</p>
                    <p style="margin:0;">• <b>Yesterday</b>: Monthly report generated.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- GLOBAL FIXED FOOTER ---
    st.markdown("""
        <style>
        .custom-footer {
            position: fixed; left: 0; bottom: 0; width: 100%;
            background-color: #f8f9fa; color: #6c757d; text-align: center;
            padding: 12px 0; font-size: 0.9rem; font-weight: 500;
            border-top: 1px solid #e9ecef; z-index: 999;
        }
        .block-container { padding-bottom: 70px !important; }
        </style>
        <div class="custom-footer">
            Copyright © 2026 MyPrestasi HPU | National Health Facility
        </div>
    """, unsafe_allow_html=True)