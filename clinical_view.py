import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def show_clinical_page():
    st.title("⚕️ Modul Penilaian: Clinical Excellence")
    st.markdown("Halaman khusus untuk penilaian klinikal pegawai perubatan.")
    st.divider()

    # ==========================================================
    # BAHAGIAN 1: MASUKKAN CSS DI SINI
    # ==========================================================
    st.markdown("""
    <style>
        /* Target hanya butang di dalam navigasi kad ini */
        div[data-testid="stHorizontalBlock"] div.stButton > button {
            height: 100px !important;
            width: 100% !important;
            border-radius: 15px !important;
            background-color: white !important;
            border: 1px solid #f0f2f6 !important;
            box-shadow: 0px 2px 4px rgba(0,0,0,0.05) !important;
            transition: all 0.3s ease !important;
            padding: 10px !important;
            font-weight: bold !important;
        }

        /* Kesan apabila butang dihalakan tetikus (Hover) */
        div[data-testid="stHorizontalBlock"] div.stButton > button:hover {
            border-color: #FF4B4B !important;
            color: #FF4B4B !important;
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
            
        selected_doc_eval = st.selectbox("Pilih Pegawai Perubatan:", doc_list)
        st.write(f"Sesi Penilaian: **{selected_doc_eval}**")
        st.write("---")

        # ==========================================================
        # BAHAGIAN 2: LOGIK NAVIGASI BUTANG (GANTI st.tabs)
        # ==========================================================
        if 'active_tab_clinical' not in st.session_state:
            st.session_state['active_tab_clinical'] = "Skills"

        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            is_active = st.session_state['active_tab_clinical'] == "Skills"
            if st.button("🛠️\nSkills", key="btn_skills", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state['active_tab_clinical'] = "Skills"
                st.rerun()
                
        with col2:
            is_active = st.session_state['active_tab_clinical'] == "Knowledge"
            if st.button("🧠\nKnowledge", key="btn_know", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state['active_tab_clinical'] = "Knowledge"
                st.rerun()
                
        with col3:
            is_active = st.session_state['active_tab_clinical'] == "Documentation"
            if st.button("📝\nDoc.", key="btn_doc", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state['active_tab_clinical'] = "Documentation"
                st.rerun()
                
        with col4:
            is_active = st.session_state['active_tab_clinical'] == "Policies"
            if st.button("📜\nPolicies", key="btn_pol", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state['active_tab_clinical'] = "Policies"
                st.rerun()

        st.write("") # Ruang kosong

        # ==========================================================
        # BAHAGIAN 3: KANDUNGAN BERDASARKAN BUTANG (GANTI with tabX)
        # ==========================================================
        
        # --- TAB 1: SKILLS ---
        if st.session_state['active_tab_clinical'] == "Skills":
            st.subheader("1. Kemahiran Klinikal (Skills)")
            if selected_doc_eval != "Sila pilih klinik di Dashboard utama dahulu":
                st.markdown("**Analisis Prestasi CUSUM: Prosedur LIMA-LAD**")
                st.caption("Memantau lengkung pembelajaran (learning curve) berdasarkan 20 kes LIMA-LAD terakhir.")
                
                with st.container(border=True):
                    np.random.seed(hash(selected_doc_eval) % (2**32 - 1))
                    procedures = np.arange(1, 21)
                    learning_curve_scores = 88 - 15 * np.exp(-procedures / 6)
                    noise = np.random.normal(0, 3, 20)
                    actual_scores = learning_curve_scores + noise
                    target_score = 80
                    cusum_values = np.cumsum(actual_scores - target_score)
                    df_cusum = pd.DataFrame({"Prosedur": procedures, "Nilai CUSUM": cusum_values})
                    
                    fig = px.line(df_cusum, x="Prosedur", y="Nilai CUSUM", markers=True,
                                 labels={"Prosedur": "Bilangan Prosedur LIMA-LAD", "Nilai CUSUM": "Variasi CUSUM"})
                    fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Baseline KPI (80)")
                    fig.update_traces(line_color="#00a0dc")
                    fig.update_layout(margin=dict(t=20, l=0, r=0, b=0), height=320)
                    st.plotly_chart(fig, use_container_width=True)
            
            st.write("") 
            st.slider("Skor Pemerhatian Prosedur Baharu", 0, 100, 85, key="skill_slider")
            st.text_area("Komen Kemahiran", key="skill_kom")
            st.button("Simpan Skor Skills", type="primary")

        # --- TAB 2: KNOWLEDGE ---
        elif st.session_state['active_tab_clinical'] == "Knowledge":
            st.subheader("2. Pengetahuan & Kapasiti (CME/CPD)")
            
            # Tetapkan nilai default supaya tidak ralat "Undefined"
            cpd_score = 0
            cpd_target = 40

            # 1. BAHAGIAN PENAPIS (Filters)
            with st.container(border=True):
                col_f1, col_f2, col_f3 = st.columns(3)
                with col_f1: st.selectbox("📅 Tahun", ["2026", "2025"], key="f_year")
                with col_f2: st.selectbox("🗓️ Bulan", ["Semua", "Januari", "Februari"], key="f_month")
                with col_f3: st.text_input("🔍 Subjek/Topik", placeholder="Cari topik...", key="f_sub")

            # 2. DUA GAUGE CHARTS
            if selected_doc_eval != "Sila pilih klinik di Dashboard utama dahulu":
                # Jana data simulasi (Hanya jika doktor dipilih)
                np.random.seed(hash(selected_doc_eval) % (2**32 - 1))
                cpd_score = np.random.randint(20, 55)
                
                col_gauge1, col_gauge2 = st.columns(2)
                with col_gauge1:
                    fig_ind = go.Figure(go.Indicator(
                        mode = "gauge+number", value = cpd_score,
                        title = {'text': "Skor Anda (%)", 'font': {'size': 16}},
                        gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#2ecc71"}}
                    ))
                    fig_ind.update_layout(height=260, margin=dict(t=40, b=10, l=30, r=30))
                    st.plotly_chart(fig_ind, use_container_width=True)

                with col_gauge2:
                    score_peer = 72 
                    fig_peer = go.Figure(go.Indicator(
                        mode = "gauge+number", value = score_peer,
                        title = {'text': "Purata Rakan Setugas", 'font': {'size': 16}},
                        gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#3498db"}}
                    ))
                    fig_peer.update_layout(height=260, margin=dict(t=40, b=10, l=30, r=30))
                    st.plotly_chart(fig_peer, use_container_width=True)

                st.divider()

                # 3. JADUAL LOG SEJARAH
                st.markdown("#### 📜 Log Aktiviti & Markah Pembelajaran")
                history_df = pd.DataFrame({
                    "Date": ["20/02/2026", "12/02/2026", "05/01/2026"],
                    "Category": ["CME", "Workshop", "Online Quiz"],
                    "Topic": ["Trauma Management", "LIMA-LAD Technique", "Medical Ethics"],
                    "Marks": [85, 92, 78]
                })
                st.dataframe(history_df, use_container_width=True, hide_index=True)

            # 4. BORANG INPUT (Diperkemaskan)
            st.write("")
            with st.expander("➕ Tambah Rekod / Simpan Skor Baharu"):
                st.info("Pilih cara kemasukan: 1) Masuk Sendiri atau 2) Imbas QR CME")
                c1, c2 = st.columns(2)
                with c1: st.date_input("Tarikh Aktiviti", key="in_date")
                with c2: st.selectbox("Kategori", ["CME", "Workshop", "Exam"], key="in_cat")
                st.text_input("Topik Pembelajaran", key="in_topic")
                markah_input = st.slider("Markah Diperolehi", 0, 100, 80, key="know_slider_new")
                
                if st.button("Simpan Rekod Knowledge", type="primary", key="btn_save_k"):
                    st.success("Rekod berjaya disimpan!")
                    # Sekarang cpd_score & cpd_target sudah selamat digunakan
                    if cpd_score >= cpd_target:
                        st.success("✅ Sasaran Mata CPD Tahunan Dicapai!")
                    else:
                        st.warning(f"⚠️ Memerlukan {cpd_target - cpd_score} mata lagi.")

            # PADAM/BUANG baris slider dan button lama yang berada di bawah st.divider() asal (baris 187-189 dalam gambar)

            st.divider()
            st.slider("Kemas Kini Skor Ujian / CPD Points Baharu", 0, 100, 90, key="know_slider")
            st.button("Simpan Skor Knowledge", type="primary")

        # --- TAB 3: DOCUMENTATION ---
        elif st.session_state['active_tab_clinical'] == "Documentation":
            st.subheader("3. Dokumentasi")
            st.number_input("Purata Masa Siap Nota (Jam)", min_value=0.0, value=2.5, step=0.5)
            st.button("Simpan Skor Dokumentasi", type="primary")

        # --- TAB 4: POLICIES ---
        elif st.session_state['active_tab_clinical'] == "Policies":
            st.subheader("4. Pematuhan Polisi & Protokol")
            st.slider("Kadar Pematuhan SOP (%)", 0, 100, 95, key="pol_slider")
            st.button("Simpan Skor Polisi", type="primary")