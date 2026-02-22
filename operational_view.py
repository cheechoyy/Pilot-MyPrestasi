import streamlit as st

def show_operational_page():
    st.title("⚙️ Modul Penilaian: Operational Excellence")
    st.markdown("Halaman pemantauan produktiviti dan inovasi pegawai perubatan.")
    st.divider()

    # --- 1. CSS KHUSUS (Sama seperti Clinical untuk keseragaman) ---
    st.markdown("""
    <style>
        div[data-testid="stHorizontalBlock"] div.stButton > button {
            height: 90px !important;
            width: 100% !important;
            border-radius: 12px !important;
            background-color: #ffffff !important;
            border: 1px solid #e0e0e0 !important;
            color: #31333F !important;
            box-shadow: 0px 2px 5px rgba(0,0,0,0.05) !important;
            transition: all 0.2s ease-in-out !important;
            font-size: 14px !important;
            line-height: 1.2 !important;
            font-weight: bold !important;
        }

        /* Gaya untuk butang yang sedang AKTIF */
        div[data-testid="stHorizontalBlock"] div.stButton > button[kind="primary"] {
            background-color: #f0f7ff !important;
            border: 2px solid #6c5ce7 !important; /* Warna ungu mengikut tema Operational */
            color: #6c5ce7 !important;
            box-shadow: 0px 4px 10px rgba(108, 92, 231, 0.1) !important;
        }

        div[data-testid="stHorizontalBlock"] div.stButton > button:hover {
            border-color: #6c5ce7 !important;
            transform: translateY(-2px);
        }
    </style>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        # Ambil senarai doktor dari sesi
        if st.session_state.get("doctor_list") is not None:
            doc_list = st.session_state["doctor_list"]["Nama Pegawai"].tolist()
        else:
            doc_list = ["Sila pilih klinik di Dashboard utama dahulu"]
            
        selected_doc_eval = st.selectbox("Pilih Pegawai Perubatan:", doc_list, key="op_select")
        st.write(f"Sesi Penilaian: **{selected_doc_eval}**")
        st.write("---")

        # --- 2. LOGIK NAVIGASI KAD (2 Kategori) ---
        if 'active_tab_op' not in st.session_state:
            st.session_state['active_tab_op'] = "Productivity"

        # Kita gunakan 2 kolum sahaja supaya butang nampak besar dan jelas
        col1, col2 = st.columns(2)
        
        with col1:
            is_active = st.session_state['active_tab_op'] == "Productivity"
            if st.button("⏱️\nProductivity & Efficiency", key="btn_prod", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state['active_tab_op'] = "Productivity"
                st.rerun()
                
        with col2:
            is_active = st.session_state['active_tab_op'] == "Innovation"
            if st.button("💡\nInnovation & Problem Solving", key="btn_inov", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state['active_tab_op'] = "Innovation"
                st.rerun()

        st.write("") # Ruang kosong

        # --- 3. KANDUNGAN BERSYARAT ---
        
        # KATEGORI 1: PRODUCTIVITY
        if st.session_state['active_tab_op'] == "Productivity":
            st.subheader("1. Produktiviti & Kecekapan")
            
            # Input data objektif
            st.number_input("Purata Kes Harian Dirawat", min_value=0, value=45, step=1)
            
            # --- IDEA BAHARU: Metrik Kecekapan ---
            with st.container(border=True):
                st.markdown("#### ⏱️ Metrik Kecekapan")
                c1, c2 = st.columns(2)
                with c1:
                    st.slider("Kesesuaian Penggunaan Sumber (Resource)", 0, 100, 85, help="Kecekapan penggunaan ubat/lab")
                with c2:
                    st.slider("Pusing Ganti Kes (TAT)", 0, 100, 90, help="Kepatuhan masa standard rawatan")
                
                st.button("Simpan Skor Produktiviti", type="primary", key="save_prod_new")
            
        # KATEGORI 2: INNOVATION
        # KATEGORI 2: INNOVATION
        elif st.session_state['active_tab_op'] == "Innovation":
            st.subheader("2. Inovasi & Penyelesaian Masalah")
            
            # --- IDEA BAHARU: Pencapaian Inovatif ---
            with st.container(border=True):
                st.markdown("#### 💡 Pencapaian Inovatif")
                st.radio("Penglibatan Projek Inovasi (QA/QI/KIK)", ["Tiada", "Ahli", "Ketua Projek"], horizontal=True)
                st.multiselect("Sumbangan Dokumentasi", ["Update SOP", "Protocol Baru", "Flowchart Baru"], default=[])
                st.text_area("Huraian Ringkas Inovasi", placeholder="Contoh: Mempercepatkan proses pendaftaran di ED sebanyak 10% melalui sistem QR.")
                
                st.button("Simpan Skor Inovasi", type="primary", key="save_inov_new")
                
            # --- RINGKASAN SKOR AKHIR (WEIGHTAGE) ---
        st.write("---")
        st.subheader("🎯 Keputusan Operational Keseluruhan")
        
        # Simulasi pengiraan (Ambil daripada session_state yang kita set di Admin)
        w_p = st.session_state.get("w_prod", 70) / 100
        w_i = st.session_state.get("w_inov", 30) / 100
        
        # Contoh skor (Dalam sistem sebenar, tarik dari database)
        final_score = (85 * w_p) + (60 * w_i)
        
        col_res1, col_res2 = st.columns([2, 1])
        with col_res1:
            st.info(f"**Markah Akhir Operational: {final_score:.1f}%**")
            st.caption(f"Formula: (Productivity × {w_p}) + (Innovation × {w_i})")
        with col_res2:
            if final_score >= 80:
                st.success("✨ Cemerlang")
            else:
                st.warning("📈 Perlukan Peningkatan")