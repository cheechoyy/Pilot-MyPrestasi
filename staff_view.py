import streamlit as st
import pandas as pd
from datetime import date
import plotly.express as px

# --- IMPORT FUNGSI DARI FAIL MODUL ---
# Kita kekalkan operational dan interpersonal buat masa ini
from operational_view import show_operational_page
from interpersonal_view import show_interpersonal_page

# =====================================================================
# --- FUNGSI BORANG KLINIKAL KHAS UNTUK STAF ---
# =====================================================================
def show_staff_clinical_update():
    st.markdown("<h2 style='color:#2b3674;'>🩺 Kemas Kini Data: Clinical Excellence</h2>", unsafe_allow_html=True)
    st.info("Sila masukkan rekod prosedur, aktiviti CPD, dan audit dokumentasi anda. Data ini akan dihantar kepada HOD untuk pengesahan.")

    # 1. Identiti Statik (Auto-detect siapa yang login)
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #2ecc71; margin-bottom: 20px;'>
            <strong>Nama Pegawai:</strong> Dr. Portal (Log Masuk Semasa)<br>
            <strong>Jabatan:</strong> Pesakit Luar
        </div>
    """, unsafe_allow_html=True)

    # 2. Tabs untuk kategori pengisian berbeza
    tab1, tab2, tab3, tab4 = st.tabs(["🛠️ Log Prosedur (Skills)", "📚 Tuntutan CPD (Knowledge)", "📝 Audit Dokumentasi", "📜 Deklarasi Polisi"])

    # --- TAB 1: KEMAHIRAN (LOG PROSEDUR) ---
    with tab1:
        st.markdown("### Tambah Log Prosedur Klinikal")
        with st.form("form_skills", clear_on_submit=True):
            c1, c2 = st.columns(2)
            tarikh = c1.date_input("Tarikh Prosedur")
            jenis = c2.selectbox("Jenis Prosedur", ["Intubation", "Central Line Insertion", "Chest Tube", "Appendectomy", "Lain-lain"])
            
            c3, c4 = st.columns(2)
            komplikasi = c3.radio("Adakah terdapat komplikasi?", ["Tidak", "Ya"], horizontal=True)
            peranan = c4.selectbox("Peranan Anda", ["Primary Surgeon / Operator", "First Assistant", "Observer"])
            
            nota = st.text_area("Catatan Tambahan / Pembelajaran (Pilihan)")
            
            submitted = st.form_submit_button("Hantar Log Prosedur", type="primary", use_container_width=True)
            if submitted:
                st.success("✅ Log prosedur berjaya dihantar dan menanti pengesahan HOD.")

    # --- TAB 2: PENGETAHUAN (CPD) ---
    with tab2:
        st.markdown("### Tuntutan Mata CPD / CME")
        with st.form("form_cpd", clear_on_submit=True):
            tajuk = st.text_input("Tajuk Program / Kursus")
            
            # Senarai penuh berdasarkan borang log CPD standard
            senarai_kategori_cpd = [
                "A1 - SCIENTIFIC MEETINGS/CONGRESS",
                "A2 - WORKSHOPS/COURSES/SKILL COURSES INCLUDING ATLS/CCRISP/CPR...",
                "B1A - HOSPITAL/DEPARTMENT CME",
                "B1B - SMALL GROUP DISCUSSION/CASE CONFERENCE",
                "B1C - PARTICIPATION IN INTER-DEPARTMENT CLINICAL MEETING / EPI REVIEW",
                "B1D - JOURNAL CLUB MEETING",
                "B1E - FORMAL GRAND WARD ROUND",
                "B1F - EXTERNAL CME LECTURE/ TOPIC SEMINAR",
                "B2A - MORBIDITY AND MORTALITY REVIEWS",
                "B2B - AUDIT MEETINGS",
                "B2C - PARTICIPATION IN ACCREDITATION EXERCISE",
                "B2D - PARTICIPATION IN QUALITY ASSURANCE (QA) ACTIVITIES",
                "C1 - SCHOLARLY ACTIVITIES/TRAINING/PRESENTATION",
                "C2 - SCHOLARLY ACTIVITIES/RESEARCH/PUBLICATION",
                "DA - ONLINE CME MODULES (PER MODULE)",
                "DB - SELF-STUDY (RELEVANT BOOKS, PUBLICATIONS, PODCASTS ETC.)",
                "DC - EXTERNAL LECTURE/ TOPIC SEMINAR (PER HOUR)",
                "E - PROFESSIONAL DEVELOPMENT"
            ]
            kategori = st.selectbox("Kategori CPD", senarai_kategori_cpd)
            
            c1, c2, c3 = st.columns(3)
            mula = c1.date_input("Tarikh Mula")
            tamat = c2.date_input("Tarikh Tamat")
            mata = c3.number_input("Mata CPD Dituntut", min_value=0, step=1)
            
            sijil = st.file_uploader("Muat Naik Sijil/Bukti (PDF/JPG)", type=['pdf', 'jpg', 'png'])
            
            sub_cpd = st.form_submit_button("Hantar Tuntutan CPD", type="primary", use_container_width=True)
            if sub_cpd:
                if tajuk == "":
                    st.error("Sila masukkan tajuk program.")
                else:
                    st.success(f"✅ Tuntutan sebanyak {mata} mata CPD untuk '{tajuk}' telah dihantar ke sistem HPU.")

    # --- TAB 3: DOKUMENTASI ---
    with tab3:
        st.markdown("### Laporan Audit Dokumentasi Kendiri (Bulanan)")
        with st.form("form_doc"):
            bulan = st.selectbox("Bulan Laporan", ["Januari", "Februari", "Mac", "April"])
            
            st.write("Berdasarkan semakan rawak 10 fail pesakit anda bulan ini:")
            c1, c2 = st.columns(2)
            jum_kes = c1.number_input("Jumlah Fail Disemak", value=10, min_value=1)
            siap_24j = c2.number_input("Fail dengan Ringkasan Discaj (Discharge Summary) disiapkan < 24 jam", value=0, min_value=0, max_value=100)
            
            sub_doc = st.form_submit_button("Hantar Laporan Audit", type="primary", use_container_width=True)
            if sub_doc:
                if jum_kes > 0:
                    peratus = (siap_24j / jum_kes) * 100
                    st.success(f"✅ Audit dihantar! Pematuhan dokumentasi anda: **{peratus:.1f}%**")

    # --- TAB 4: POLISI & PROTOKOL ---
    with tab4:
        st.markdown("### Deklarasi & Pematuhan SOP")
        st.info("Sila baca dan sahkan pematuhan anda terhadap polisi terkini fasiliti. Pengesahan ini akan direkodkan sebagai bukti pematuhan (compliance).")
        
        with st.container(border=True):
            p1 = st.checkbox("Saya telah membaca dan memahami **Garis Panduan Kawalan Infeksi 2026**.")
            p2 = st.checkbox("Saya telah mengemas kini **Sijil BLS/ALS** tahunan saya dan melampirkan salinan kepada Unit Latihan.")
            p3 = st.checkbox("Saya akur dengan **Polisi Kerahsiaan Pesakit (PDPA)** terkini fasiliti.")
            
        if st.button("Sahkan Deklarasi", type="primary", use_container_width=True):
            if p1 and p2 and p3:
                st.success("✅ Deklarasi pematuhan anda telah direkodkan ke dalam pangkalan data.")
            else:
                st.error("Sila tanda (tick) pada semua kotak untuk mengesahkan deklarasi anda.")

# =====================================================================
# --- FUNGSI BORANG OPERATIONAL KHAS UNTUK STAF ---
# =====================================================================
def show_staff_operational_update():
    st.markdown("<h2 style='color:#2b3674;'>⚙️ Kemas Kini Data: Operational Excellence</h2>", unsafe_allow_html=True)
    st.info("Sila masukkan rekod produktiviti harian dan laporan inovasi anda.")

    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #39B8FF; margin-bottom: 20px;'>
            <strong>Nama Pegawai:</strong> Dr. Portal (Log Masuk Semasa)<br>
            <strong>Jabatan:</strong> Pesakit Luar
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["⏱️ Productivity & Efficiency", "💡 Innovation & Problem Solving"])

    with tab1:
        st.markdown("### Log Produktiviti & Kecekapan")
        with st.form("form_ops_prod", clear_on_submit=True):
            tarikh_kerja = st.date_input("Tarikh Semakan")
            c1, c2 = st.columns(2)
            pesakit_dilihat = c1.number_input("Jumlah Pesakit Dilihat Hari Ini", min_value=0, step=1)
            discaj_dibuat = c2.number_input("Jumlah Discaj Diuruskan", min_value=0, step=1)
            masa_rata = st.number_input("Purata Masa Konsultasi (Minit)", min_value=0, step=1)
            
            if st.form_submit_button("Hantar Log Produktiviti", type="primary", use_container_width=True):
                st.success("✅ Data produktiviti berjaya direkodkan.")

    with tab2:
        st.markdown("### Cadangan Inovasi & Penyelesaian Masalah")
        with st.form("form_ops_innov", clear_on_submit=True):
            isu = st.text_input("Isu/Masalah Operasi yang Dikenal Pasti")
            solusi = st.text_area("Cadangan Solusi / Inovasi yang Dilaksanakan")
            
            if st.form_submit_button("Hantar Cadangan Inovasi", type="primary", use_container_width=True):
                if isu == "":
                    st.error("Sila masukkan isu/masalah.")
                else:
                    st.success("✅ Idea inovasi anda telah dihantar ke sistem untuk penilaian.")

# =====================================================================
# --- FUNGSI BORANG INTERPERSONAL KHAS UNTUK STAF ---
# =====================================================================
def show_staff_interpersonal_update():
    st.markdown("<h2 style='color:#2b3674;'>🤝 Kemas Kini Data: Interpersonal Excellence</h2>", unsafe_allow_html=True)
    st.info("Sila rekodkan maklum balas pesakit, pengurusan emosi, kerja berpasukan, dan sesi mentorship.")

    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #05CD99; margin-bottom: 20px;'>
            <strong>Nama Pegawai:</strong> Dr. Portal (Log Masuk Semasa)<br>
            <strong>Jabatan:</strong> Pesakit Luar
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["😊 Patient Experience", "🧠 Emotional Intel.", "👥 Teamwork", "🎓 Mentorship"])

    with tab1:
        st.markdown("### Maklum Balas Pesakit")
        with st.form("form_int_px", clear_on_submit=True):
            c1, c2 = st.columns(2)
            pujian = c1.number_input("Bilangan Pujian/Penghargaan Diterima", min_value=0, step=1)
            aduan = c2.number_input("Bilangan Aduan/Teguran Diterima", min_value=0, step=1)
            catatan = st.text_area("Ringkasan Maklum Balas Pesakit / Tindakan Diambil")
            
            if st.form_submit_button("Simpan Rekod Patient Experience", type="primary", use_container_width=True):
                st.success("✅ Rekod pengalaman pesakit dikemaskini.")
                
    with tab2:
        st.markdown("### Kecerdasan Emosi (Self-Reflection)")
        with st.form("form_int_ei", clear_on_submit=True):
            refleksi = st.text_area("Refleksi Pengurusan Tekanan & Emosi Kendiri")
            tindakan = st.text_input("Langkah Penambahbaikan (Cth: Sesi Kaunseling, Riadah)")
            
            if st.form_submit_button("Simpan Rekod Emotional Intel", type="primary", use_container_width=True):
                st.success("✅ Log refleksi kecerdasan emosi berjaya direkodkan.")

    with tab3:
        st.markdown("### Kerja Berpasukan & Kolaborasi (MDT)")
        with st.form("form_int_team", clear_on_submit=True):
            projek = st.text_input("Nama Aktiviti / Kes Mesyuarat (MDT)")
            peranan = st.text_input("Peranan Anda dalam Pasukan")
            jabatan_terlibat = st.multiselect("Jabatan Terlibat", ["Pakar Perubatan", "Pakar Bedah", "Farmasi", "Dietetik", "Fisioterapi", "Lain-lain"])
            
            if st.form_submit_button("Simpan Rekod Teamwork", type="primary", use_container_width=True):
                if not jabatan_terlibat:
                    st.error("Sila pilih sekurang-kurangnya satu jabatan.")
                else:
                    st.success("✅ Data kerjasama pasukan berjaya direkodkan.")

    with tab4:
        st.markdown("### Sesi Mentorship")
        with st.form("form_int_mentor", clear_on_submit=True):
            peranan_m = st.radio("Peranan Anda:", ["Sebagai Mentor (Mendidik)", "Sebagai Mentee (Belajar)"], horizontal=True)
            nama_rakan = st.text_input("Nama Rakan (Mentor/Mentee)")
            tarikh_sesi = st.date_input("Tarikh Sesi")
            topik = st.text_area("Topik Perbincangan / Kemahiran Diajar")
            
            if st.form_submit_button("Simpan Log Mentorship", type="primary", use_container_width=True):
                st.success("✅ Log sesi mentorship telah disimpan.")

# =====================================================================
# --- DASHBOARD UTAMA STAF ---
# =====================================================================
def show_staff_dashboard():
    if "staff_view" not in st.session_state:
        st.session_state["staff_view"] = "Dashboard"

    # --- SIDEBAR KHAS UNTUK STAF ---
    with st.sidebar:
        st.markdown('<div class="user-avatar" style="background-color: #2ecc71; width: 60px; height: 60px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 30px; margin: 0 auto;">👨‍⚕️</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'><b>Dr. Portal</b><br>Pegawai Perubatan</p>", unsafe_allow_html=True)
        st.divider()
        
        st.write("**Menu Utama**")
        if st.button("🏠 Dashboard", width="stretch", type="primary" if st.session_state["staff_view"] == "Dashboard" else "secondary"):
            st.session_state["staff_view"] = "Dashboard"
            st.rerun()
            
        if st.button("📊 My Performance", width="stretch", type="primary" if st.session_state["staff_view"] == "My Performance" else "secondary"):
            st.session_state["staff_view"] = "My Performance"
            st.rerun()
            
        st.write("")
        st.write("**Kemas Kini Data Kendiri**")
        if st.button("🩺 Clinical Excellence", width="stretch", type="primary" if st.session_state["staff_view"] == "Clinical" else "secondary"):
            st.session_state["staff_view"] = "Clinical"
            st.rerun()
            
        if st.button("⚙️ Operational", width="stretch", type="primary" if st.session_state["staff_view"] == "Operational" else "secondary"):
            st.session_state["staff_view"] = "Operational"
            st.rerun()
            
        if st.button("🤝 Interpersonal", width="stretch", type="primary" if st.session_state["staff_view"] == "Interpersonal" else "secondary"):
            st.session_state["staff_view"] = "Interpersonal"
            st.rerun()
        
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        
        if st.button("🚪 Log Keluar", type="primary", width="stretch"): 
            st.session_state.clear()
            st.rerun()

    # --- KANDUNGAN: MY PERFORMANCE ---
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

    # --- KANDUNGAN: MODUL PENGISIAN DATA STAF ---
    elif st.session_state["staff_view"] == "Clinical":
        show_staff_clinical_update()

    elif st.session_state["staff_view"] == "Operational":
        show_staff_operational_update()

    elif st.session_state["staff_view"] == "Interpersonal":
        show_staff_interpersonal_update()

    # --- KANDUNGAN: DASHBOARD UTAMA STAF ---
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