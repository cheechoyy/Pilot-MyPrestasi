import streamlit as st
import plotly.express as px
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import date
from utils import DATA_KLINIK, generate_doctors

from interpersonal_view import show_interpersonal_page
from clinical_view import show_clinical_page
from operational_view import show_operational_page

def show_admin_dashboard():
    # 1. Data Carta Navigasi
    data_nav = {
        "labels": ["HPU", "Clinical<br>Excellence", "Operational", "Interpersonal<br>Excellence", "Skills", "Knowledge &<br>Capacity", "Policies &<br>Protocols", "Documentation", "Productivity &<br>Efficiency", "Innovation &<br>Problem Solving", "Patient<br>Experience", "Emotional<br>Intelligence", "Teamwork &<br>Collaboration", "Mentorship"],
        "parents": ["", "HPU", "HPU", "HPU", "Clinical<br>Excellence", "Clinical<br>Excellence", "Clinical<br>Excellence", "Clinical<br>Excellence", "Operational", "Operational", "Interpersonal<br>Excellence", "Interpersonal<br>Excellence", "Interpersonal<br>Excellence", "Interpersonal<br>Excellence"],
        "colors": ["Base", "Clinical", "Operational", "Interpersonal"] + ["Clinical"]*4 + ["Operational"]*2 + ["Interpersonal"]*4
    }
    color_map = {"Base": "#ffffff", "Clinical": "#f1c40f", "Operational": "#9b59b6", "Interpersonal": "#2ecc71"}

    clinical_views = ["Clinical Excellence", "Skills", "Knowledge & Capacity", "Policies & Protocols", "Documentation"]
    operational_views = ["Operational", "Productivity & Efficiency", "Innovation & Problem Solving"]
    interpersonal_views = ["Interpersonal Excellence", "Patient Experience", "Emotional Intelligence", "Teamwork & Collaboration", "Mentorship"]

    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown('<div class="user-avatar">👤</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'><b>Admin HPU</b></p>", unsafe_allow_html=True)
        st.divider()
        
        st.write("**Navigasi Pintas Modul**")
        if st.button("🔴 Clinical Excellence", width="stretch"):
            st.session_state["selected_view"] = "Clinical Excellence"
            st.session_state["selected_doctor"] = None
            st.rerun()
        if st.button("🟣 Operational Excellence", width="stretch"):
            st.session_state["selected_view"] = "Operational"
            st.session_state["selected_doctor"] = None
            st.rerun()
        if st.button("🟢 Interpersonal Excellence", width="stretch"):
            st.session_state["selected_view"] = "Interpersonal Excellence"
            st.session_state["selected_doctor"] = None
            st.rerun()
        
        # Penambahan ruang kosong untuk menolak butang ke bawah
        st.markdown("<br><br><br><br>", unsafe_allow_html=True)
        
        if st.session_state["selected_view"] != "Dashboard Utama" or st.session_state["selected_doctor"]:
            if st.button("⬅️ Kembali ke Dashboard", width="stretch"):
                st.session_state["selected_doctor"] = None
                st.session_state["selected_view"] = "Dashboard Utama"
                st.rerun()
        
        # Butang Log Keluar kini berada di posisi lebih bawah
        if st.button("🚪 Log Keluar", type="primary", width="stretch"):
            st.session_state.clear()
            st.rerun()

    # --- PENGHALAAN (ROUTING) ---
    view = st.session_state["selected_view"]

    if view in clinical_views:
        show_clinical_page()
    elif view in operational_views:
        show_operational_page()
    elif view in interpersonal_views:
        show_interpersonal_page()
    elif st.session_state["selected_doctor"]:
        st.title(f"🔍 Profil Individu: {st.session_state['selected_doctor']}")
        st.info("Gunakan butang 'Kembali ke Dashboard' di sidebar untuk menukar data.")
    else:
        # --- DASHBOARD UTAMA ---
        st.title("📊 DASHBOARD MYPRESTASI")
        st.markdown("<p style='color: #666; font-size: 1.1rem; margin-top: -15px;'>Pemantauan Fasiliti Kesihatan Negeri Selangor</p>", unsafe_allow_html=True)

        m1, m2, m3 = st.columns(3)
        with m1:
            with st.container(border=True): st.metric("Clinical Performance", "80%", "Sasaran: 80%")
        with m2:
            with st.container(border=True): st.metric("Operational Output", "1,240", "Target: >100")
        with m3:
            with st.container(border=True): st.metric("Interpersonal Rating", "High", "PSQ18")
        
        st.write("")

        col_chart, col_map, col_list = st.columns([1.3, 1.6, 1.1], gap="medium")

        with col_chart:
            with st.container(border=True):
                st.markdown("#### 🧭 Navigasi Modul")
                fig = px.sunburst(pd.DataFrame(data_nav), names='labels', parents='parents', color='colors', color_discrete_map=color_map)
                fig.update_traces(insidetextorientation='tangential', textinfo='label')
                fig.update_layout(margin=dict(t=10, l=0, r=0, b=10), height=380)
                
                event = st.plotly_chart(fig, use_container_width=True, on_select="rerun")
                if event and "selection" in event and event["selection"]["points"]:
                    label_raw = event["selection"]["points"][0]["label"]
                    st.session_state["selected_view"] = label_raw.replace("<br>", " ")
                    st.rerun()

        with col_map:
            with st.container(border=True):
                st.markdown("#### 📍 Peta Fasiliti")
                m = folium.Map(location=[3.0738, 101.5183], zoom_start=10)
                for k in DATA_KLINIK:
                    folium.Marker([k["lat"], k["lon"]], tooltip=k["name"]).add_to(m)
                
                out = st_folium(m, width="100%", height=380, key="admin_map")

                if out and out.get("last_object_clicked"):
                    lat = out["last_object_clicked"]["lat"]
                    lon = out["last_object_clicked"]["lng"]
                    
                    # Nilai 0.001 telah ditukar kepada 0.01 supaya klik lebih mudah dikesan
                    for k in DATA_KLINIK:
                        if abs(k["lat"] - lat) < 0.01 and abs(k["lon"] - lon) < 0.01:
                            # Halang skrin daripada loading tanpa henti (infinite loop)
                            if st.session_state.get("selected_klinik") != k["name"]:
                                st.session_state["selected_klinik"] = k["name"]
                                st.session_state["doctor_list"] = generate_doctors(k["name"])
                                st.rerun()
                            break

        with col_list:
            with st.container(border=True):
                st.markdown("#### 📋 Senarai Kakitangan")
                if st.session_state["selected_klinik"]:
                    st.success(f"{st.session_state['selected_klinik']}")
                    df_docs = st.session_state["doctor_list"]
                    
                    event_df = st.dataframe(
                        df_docs, 
                        use_container_width=True, 
                        height=280, 
                        hide_index=True,
                        on_select="rerun", 
                        selection_mode="single-row"
                    )
                    
                    if event_df.selection.rows:
                        idx = event_df.selection.rows[0]
                        st.session_state["selected_doctor"] = df_docs.iloc[idx]["Nama Pegawai"]
                        st.rerun()
                else:
                    st.info("Sila klik lokasi pada peta.")

    # --- PENAMBAHAN FOOTER GLOBAL ---
    st.markdown("""
        <style>
        .custom-footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f8f9fa;
            color: #6c757d;
            text-align: center;
            padding: 12px 0;
            font-size: 0.9rem;
            font-weight: 500;
            border-top: 1px solid #e9ecef;
            z-index: 999;
        }
        .block-container {
            padding-bottom: 70px !important; /* Elak kandungan tertutup oleh footer */
        }
        </style>
        <div class="custom-footer">
            Hak Cipta Terpelihara © 2026 MyPrestasi HPU | Fasiliti Kesihatan Negeri Selangor
        </div>
    """, unsafe_allow_html=True)


# --- PORTAL DOKTOR (STAFF) ---
# --- PORTAL DOKTOR (STAFF) ---
def show_staff_dashboard():
    # 1. Tetapkan state paparan lalai jika belum wujud
    if "staff_view" not in st.session_state:
        st.session_state["staff_view"] = "Dashboard"

    with st.sidebar:
        st.markdown('<div class="user-avatar" style="background-color: #2ecc71;">👨‍⚕️</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'><b>Dr. Portal</b><br>Pegawai Perubatan</p>", unsafe_allow_html=True)
        st.divider()
        
        # --- BUTANG NAVIGASI DOKTOR ---
        st.write("**Menu Utama**")
        if st.button("🏠 Dashboard", width="stretch"):
            st.session_state["staff_view"] = "Dashboard"
            st.rerun()
            
        if st.button("📊 My Performance", width="stretch"):
            st.session_state["staff_view"] = "My Performance"
            st.rerun()
        
        # Penambahan ruang kosong untuk tolak butang ke bawah
        st.markdown("<br><br><br><br><br>", unsafe_allow_html=True)
        
        if st.button("🚪 Log Keluar", type="primary", width="stretch"): 
            st.session_state.clear()
            st.rerun()

    # --- PENGHALAAN (ROUTING) HALAMAN DOKTOR ---
    if st.session_state["staff_view"] == "My Performance":
        # HALAMAN BAHARU: MY PERFORMANCE
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
        # HALAMAN LALAI: DASHBOARD ASAL DOKTOR
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
                        
    # --- FOOTER GLOBAL KEKAL ---
    st.markdown("""
        <style>
        .custom-footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f8f9fa;
            color: #6c757d;
            text-align: center;
            padding: 12px 0;
            font-size: 0.9rem;
            font-weight: 500;
            border-top: 1px solid #e9ecef;
            z-index: 999;
        }
        .block-container {
            padding-bottom: 70px !important;
        }
        </style>
        <div class="custom-footer">
            Hak Cipta Terpelihara © 2026 MyPrestasi HPU | Fasiliti Kesihatan Negeri Selangor
        </div>
    """, unsafe_allow_html=True)
    # --- PENAMBAHAN FOOTER GLOBAL (Sama Seperti Admin) ---
    st.markdown("""
        <style>
        .custom-footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f8f9fa;
            color: #6c757d;
            text-align: center;
            padding: 12px 0;
            font-size: 0.9rem;
            font-weight: 500;
            border-top: 1px solid #e9ecef;
            z-index: 999;
        }
        .block-container {
            padding-bottom: 70px !important;
        }
        </style>
        <div class="custom-footer">
            Hak Cipta Terpelihara © 2026 MyPrestasi HPU | Fasiliti Kesihatan Negeri Selangor
        </div>
    """, unsafe_allow_html=True)