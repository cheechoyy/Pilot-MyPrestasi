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

# --- DATA MOCK TEMPATAN (Kemas kini Semua Negeri di Malaysia) ---
STATE_CENTERS = {
    "Semua Negeri": {"lat": 4.2105, "lon": 101.9758, "zoom": 6},
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
    # Jana data rawak doktor mengikut format jadual yang diminta
    random.seed(hash(clinic_name)) # Supaya data tak berubah-ubah bila refresh
    doctors = []
    names = ["Dr. Farhana", "Dr. Ah Meng", "Dr. Sarah", "Dr. David", "Dr. Ali", "Dr. Muthu", "Dr. Siti", "Dr. Chong", "Dr. Ramesh", "Dr. Aisyah"]
    
    for _ in range(random.randint(4, 8)):
        score = random.randint(60, 99)
        if score >= 85: status = "Cemerlang"
        elif score >= 75: status = "Baik"
        elif score >= 65: status = "Sederhana"
        else: status = "Perlu Perhatian"
        
        doctors.append({
            "Nama Pegawai": f"{random.choice(names)} ({random.randint(100,999)})",
            "Jabatan": "Pesakit Luar",
            "Skor Semasa": score,
            "Status": status
        })
    return pd.DataFrame(doctors)


def show_admin_dashboard():
    # --- 1. CSS KHAS UNTUK TEMA DASHBOARD MODEN ---
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

    # --- 2. DATA CARTA ---
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
        st.markdown('<div style="text-align:center; padding:10px;"><h2 style="color:#4318FF; font-weight:800; margin:0;">MyPrestasi</h2><p style="color:gray; font-size:12px;">Admin Portal</p></div>', unsafe_allow_html=True)
        st.divider()
        
        if st.button("🏠 Papan Pemuka", width="stretch", type="primary" if st.session_state["selected_view"] == "Dashboard Utama" else "secondary"):
            st.session_state["selected_view"] = "Dashboard Utama"
            st.session_state["selected_doctor"] = None
            st.session_state["selected_klinik"] = None
            st.rerun()
            
        st.write("")
        st.markdown("<p style='font-size:13px; font-weight:bold; color:#a3aed1; margin-bottom:10px;'>📊 STATISTIK KESELURUHAN</p>", unsafe_allow_html=True)
        
        st.markdown("""
            <div class="sidebar-kpi">
                <div class="sidebar-icon" style="background:#E2E8FF; color:#4318FF;">🏥</div>
                <div class="sidebar-text"><h3>21</h3><p>Fasiliti Aktif</p></div>
            </div>
            <div class="sidebar-kpi">
                <div class="sidebar-icon" style="background:#E6F8F3; color:#05CD99;">👨‍⚕️</div>
                <div class="sidebar-text"><h3>394</h3><p>Jumlah Kakitangan</p></div>
            </div>
            <div class="sidebar-kpi">
                <div class="sidebar-icon" style="background:#FFF2E5; color:#FF9F43;">📈</div>
                <div class="sidebar-text"><h3>82%</h3><p>Purata Prestasi</p></div>
            </div>
            <div class="sidebar-kpi">
                <div class="sidebar-icon" style="background:#FEECEF; color:#EE5D50;">✅</div>
                <div class="sidebar-text"><h3>1,250</h3><p>Penilaian Selesai</p></div>
            </div>
        """, unsafe_allow_html=True)

        st.write("")
        st.markdown("<p style='font-size:13px; font-weight:bold; color:#a3aed1; margin-bottom:10px;'>⚙️ MENU PENTADBIRAN</p>", unsafe_allow_html=True)
        
        if st.button("⚙️ Tetapan", width="stretch", key="btn_tetapan"):
            st.toast("Halaman Tetapan dibuka.")
        if st.button("📄 Laporan", width="stretch", key="btn_laporan"):
            st.toast("Halaman Laporan dibuka.")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        if st.session_state["selected_view"] != "Dashboard Utama" or st.session_state["selected_doctor"]:
            if st.button("⬅️ Kembali ke Dashboard", width="stretch"):
                st.session_state["selected_doctor"] = None
                st.session_state["selected_view"] = "Dashboard Utama"
                st.rerun()
        
        if st.button("🚪 Log Keluar", type="primary", width="stretch"):
            st.session_state.clear()
            st.rerun()

    # --- 4. PENGHALAAN (ROUTING) KANDUNGAN ---
    view = st.session_state["selected_view"]

    if view == "CTS":
        st.title("⚕️ Modul Cardiothoracic Surgery (CTS)")
        st.markdown("Sila pilih sub-modul penilaian di bawah:")
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
        # Inisialisasi State Tambahan untuk Sub-Menu FMS jika belum ada
        if "sub_menu_fms" not in st.session_state:
            st.session_state["sub_menu_fms"] = "Clinical Excellence"
            
        st.title("🩺 Modul Family Medicine Specialist (FMS)")
        st.markdown("Sila pilih sub-modul penilaian di bawah:")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            # Tambah key="fms_clin" elak ralat duplicate
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

        # Memanggil paparan klinikal dengan parameter khas untuk FMS
        if st.session_state["sub_menu_fms"] == "Clinical Excellence": show_clinical_page(module_type="FMS")
        elif st.session_state["sub_menu_fms"] == "Operational": show_operational_page()
        elif st.session_state["sub_menu_fms"] == "Interpersonal Excellence": show_interpersonal_page()

    elif st.session_state["selected_doctor"]:
        col_prof, col_prog = st.columns([1, 1])
        with col_prof:
            st.title(f"🔍 Profil: {st.session_state['selected_doctor']}")
            st.caption("Jabatan: Kecemasan | ID: HPU-9921 | Penilaian Terakhir: 15 Jan 2026")
        with col_prog:
            st.write("")
            st.progress(0.75, text="Kemajuan Borang Penilaian: 75%")
        st.info("Gunakan butang 'Papan Pemuka' di menu untuk kembali.")

    # --- DASHBOARD UTAMA ---
    else:
        st.markdown("<h2 style='color:#2b3674; margin-bottom: 0;'>Papan Pemuka Utama</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color:#a3aed1; margin-top: 0; margin-bottom: 20px;'>Sila pilih modul atau teliti pemantauan fasiliti.</p>", unsafe_allow_html=True)

        # -- BUTANG MODUL ATAS --
        col_m1, col_m2, col_m3, col_m4 = st.columns(4, gap="medium")
        with col_m1:
            if st.button("⚕️ Modul CTS", use_container_width=True, key="btn_top_cts"):
                st.session_state["selected_view"] = "CTS"
                st.session_state["selected_doctor"] = None
                st.rerun()
        with col_m2:
            if st.button("🩺 Modul FMS", use_container_width=True, key="btn_top_fms"):
                st.session_state["selected_view"] = "FMS"
                st.session_state["selected_doctor"] = None
                st.rerun()
        with col_m3:
            st.button("🔒 Modul Seterusnya (Soon)", use_container_width=True, disabled=True, key="btn_top_soon1")
        with col_m4:
            st.button("🔒 Modul Seterusnya (Soon)", use_container_width=True, disabled=True, key="btn_top_soon2")

        st.write("---")

        # -- PILIHAN NEGERI (DINAMIK) --
        col_opt, _ = st.columns([1, 3])
        with col_opt:
            senarai_negeri = list(STATE_CENTERS.keys())
            if "pilihan_negeri" not in st.session_state:
                st.session_state["pilihan_negeri"] = "Semua Negeri"
            
            negeri_dipilih = st.selectbox(
                "Tapis Lokasi:", 
                senarai_negeri, 
                index=senarai_negeri.index(st.session_state["pilihan_negeri"]),
                label_visibility="collapsed"
            )
            
            if negeri_dipilih != st.session_state["pilihan_negeri"]:
                st.session_state["pilihan_negeri"] = negeri_dipilih
                st.session_state["selected_klinik"] = None
                st.rerun()

        # -- BARIS 1: PETA & CARTA BULATAN --
        row1_col1, row1_col2 = st.columns([2, 1], gap="large")

        with row1_col1:
            st.markdown("<div class='section-title'>📍 Peta Taburan Fasiliti</div>", unsafe_allow_html=True)
            
            # Peta dinamik mengikut negeri
            pusat_peta = STATE_CENTERS[negeri_dipilih]
            
            if negeri_dipilih == "Semua Negeri":
                klinik_dipaparkan = MOCK_KLINIK
            else:
                klinik_dipaparkan = [k for k in MOCK_KLINIK if k["state"] == negeri_dipilih]

            m = folium.Map(location=[pusat_peta["lat"], pusat_peta["lon"]], zoom_start=pusat_peta["zoom"])
            
            for k in klinik_dipaparkan:
                folium.Marker([k["lat"], k["lon"]], tooltip=k["name"]).add_to(m)
            
            out = st_folium(m, width="100%", height=320, key=f"map_{negeri_dipilih}")

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

        with row1_col2:
            st.markdown("<div class='section-title'>🧭 Kategori Modul Penilaian</div>", unsafe_allow_html=True)
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

        # -- BARIS 2: SENARAI STAF & LOG (Matriks Dibuang) --
        st.write("")
        row2_col1, row2_col2 = st.columns([2, 1], gap="large")

        with row2_col1:
            st.markdown("<div class='section-title'>📋 Senarai Kakitangan Penilaian</div>", unsafe_allow_html=True)
            if st.session_state.get("selected_klinik"):
                st.markdown(f"Lokasi: <span style='color:#05CD99; font-weight:bold;'>{st.session_state['selected_klinik']}</span>", unsafe_allow_html=True)
                df_docs = st.session_state["doctor_list"]
                
                event_df = st.dataframe(
                    df_docs, use_container_width=True, height=250, hide_index=True,
                    on_select="rerun", selection_mode="single-row"
                )
                if event_df.selection.rows:
                    idx = event_df.selection.rows[0]
                    st.session_state["selected_doctor"] = df_docs.iloc[idx]["Nama Pegawai"]
                    st.rerun()
            else:
                st.info("Sila pilih lokasi (pin) pada Peta Fasiliti di atas untuk memaparkan senarai kakitangan.")

        with row2_col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #4318FF 0%, #865CFF 100%); padding: 25px 20px; border-radius: 15px; color: white; height: 100%; min-height: 250px; box-shadow: 0 10px 20px rgba(67, 24, 255, 0.2);">
                <h3 style="margin:0; font-size: 36px; font-weight: bold; color:white;">124</h3>
                <p style="margin:0 0 20px 0; font-size: 14px; opacity: 0.9;">Penilaian bulan ini</p>
                <div style="font-size: 12px; line-height: 1.8; border-top: 1px solid rgba(255,255,255,0.2); padding-top: 15px;">
                    <p style="margin:0;">• <b>09:45 AM</b>: Skor Dr. Raju disah.</p>
                    <p style="margin:0;">• <b>08:20 AM</b>: Sijil CPD dimuat naik.</p>
                    <p style="margin:0;">• <b>Semalam</b>: Laporan bulanan dijana.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- FOOTER GLOBAL KEKAL ---
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
            Hak Cipta Terpelihara © 2026 MyPrestasi HPU | Fasiliti Kesihatan Negara
        </div>
    """, unsafe_allow_html=True)

# =====================================================================
# --- PORTAL DOKTOR (STAFF) ---
# =====================================================================
def show_staff_dashboard():
    if "staff_view" not in st.session_state:
        st.session_state["staff_view"] = "Dashboard"

    with st.sidebar:
        st.markdown('<div class="user-avatar" style="background-color: #2ecc71;">👨‍⚕️</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'><b>Dr. Portal</b><br>Pegawai Perubatan</p>", unsafe_allow_html=True)
        st.divider()
        
        st.write("**Menu Utama**")
        if st.button("🏠 Dashboard", width="stretch"):
            st.session_state["staff_view"] = "Dashboard"
            st.rerun()
            
        if st.button("📊 My Performance", width="stretch"):
            st.session_state["staff_view"] = "My Performance"
            st.rerun()
        
        st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
        
        if st.button("🚪 Log Keluar", type="primary", width="stretch"): 
            st.session_state.clear()
            st.rerun()

    if st.session_state["staff_view"] == "My Performance":
        st.title("📊 Prestasi Saya (My Performance)")
        st.markdown("<p style='color: #666; font-size: 1.1rem; margin-top: -15px;'>Ringkasan penilaian dan pencapaian kemahiran anda.</p>", unsafe_allow_html=True)
        st.write("")

        col1, col2 = st.columns(2, gap="large")
        with col1:
            with st.container(border=True):
                st.subheader("⭐ Ringkasan Skor")
                st.metric(label="Clinical Excellence", value="85%", delta="Naik 2%")
                st.metric(label="Operational Output", value="92%", delta="Naik 5%")
                st.metric(label="Interpersonal Rating", value="Tinggi", delta="Kekal")
        
        with col2:
            with st.container(border=True):
                st.subheader("📈 Kemajuan CUSUM")
                st.info("Berdasarkan 20 prosedur terakhir, kemahiran anda konsisten dan stabil.")
                st.progress(85, text="Konsistensi Pemerhatian Prosedur (85%)")
                st.write("---")
                st.caption("Pematuhan Polisi & Protokol")
                st.progress(95, text="Kadar Pematuhan (95%)")

    else:
        st.title("🩺 Dashboard Pegawai Perubatan")
        st.markdown("<p style='color: #666; font-size: 1.1rem; margin-top: -15px;'>Ringkasan Tugasan, Jadual & Analisis Harian</p>", unsafe_allow_html=True)
        st.write("")

        col_cal, col_msg = st.columns([1, 1], gap="large")

        with col_cal:
            with st.container(border=True):
                st.markdown("#### 📅 Jadual Hari Ini")
                st.caption(f"Tarikh Semasa: {date.today().strftime('%d %B %Y')}")
                st.info("**10:30 - 11:30 AM** | 🛏️ Grand Rounds (Wad Umum)")
                st.success("**13:30 - 13:45 PM** | 🩺 Pemeriksaan Pesakit Baru (Klinik)")
                st.warning("**14:00 - 14:30 PM** | 💉 Prosedur LMP (Bilik Rawatan)")

        with col_msg:
            with st.container(border=True):
                st.markdown("#### 💬 Mesej & Notifikasi")
                st.caption("Peti masuk utama anda")
                st.markdown("""
                **🏥 Makmal Hospital Utama** <span style='color:gray; font-size:0.8em; float:right;'>14:03</span><br>
                <small>Keputusan makmal pesakit A telah sedia untuk disemak.</small>
                <hr style="margin:0.5em 0;">
                **👩‍🔬 Dr. Siti Nurhaliza** <span style='color:gray; font-size:0.8em; float:right;'>13:27</span><br>
                <small>Rujukan pesakit X dilampirkan. Boleh kita bincang sebentar?</small>
                <hr style="margin:0.5em 0;">
                **👨‍⚕️ Dr. Ahmad Kamil** <span style='color:gray; font-size:0.8em; float:right;'>08:12</span><br>
                <small>RE: Pertukaran syif hujung minggu ini. Saya setuju.</small>
                """, unsafe_allow_html=True)

        st.write("")

        with st.container(border=True):
            st.markdown("#### 📈 Analisis Klinikal")
            col_chart, col_metrics = st.columns([1.5, 1], gap="large")
            
            with col_chart:
                df_chart = pd.DataFrame({
                    "Jabatan": ["ICU", "Med/Surg", "ED", "Wad Kanak-Kanak"],
                    "Kes Selesai": [12, 10, 6, 8],
                    "Kes Aktif": [6, 4, 2, 3]
                })
                fig = px.bar(
                    df_chart, x="Jabatan", y=["Kes Selesai", "Kes Aktif"], 
                    barmode="stack", color_discrete_sequence=["#2ea78e", "#e0e0e0"] 
                )
                fig.update_layout(margin=dict(t=20, l=0, r=0, b=0), height=300, legend_title_text="Status Kes")
                st.plotly_chart(fig, use_container_width=True)

            with col_metrics:
                m1, m2 = st.columns(2)
                with m1:
                    with st.container(border=True):
                        st.markdown("**Inpatient LOS**")
                        st.metric("ICU", "3.4 Hari")
                        st.metric("Med/Surg", "2.2 Hari")
                with m2:
                    with st.container(border=True):
                        st.markdown("**Risk & Quality**")
                        st.metric("Sepsis Score", "3")
                        st.metric("Readmissions", "4")
                
                m3, m4 = st.columns(2)
                with m3:
                    with st.container(border=True):
                        st.markdown("**Kehadiran**")
                        st.metric("Hadir", "94%")
                with m4:
                    with st.container(border=True):
                        st.markdown("**Prosedur**")
                        st.metric("Selesai", "18/20")
                        
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
            Hak Cipta Terpelihara © 2026 MyPrestasi HPU | Fasiliti Kesihatan Negara
        </div>
    """, unsafe_allow_html=True)