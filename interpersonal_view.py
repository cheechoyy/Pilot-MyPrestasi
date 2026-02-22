import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

def show_interpersonal_page():
    st.title("🤝 Modul Penilaian: Interpersonal Excellence")
    st.markdown("Halaman penilaian bagi pengalaman pesakit (PSQ-18), kerjasama pasukan, dan kepimpinan.")
    st.divider()

    # --- 1. CSS KHUSUS (Tema Hijau Interpersonal) ---
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

        /* Gaya untuk butang yang sedang AKTIF - Hijau */
        div[data-testid="stHorizontalBlock"] div.stButton > button[kind="primary"] {
            background-color: #f0fff4 !important;
            border: 2px solid #27ae60 !important; 
            color: #27ae60 !important;
            box-shadow: 0px 4px 10px rgba(39, 174, 96, 0.1) !important;
        }

        div[data-testid="stHorizontalBlock"] div.stButton > button:hover {
            border-color: #27ae60 !important;
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
            
        selected_doc_eval = st.selectbox("Pilih Pegawai Perubatan:", doc_list, key="inter_select")
        st.write(f"Sesi Penilaian: **{selected_doc_eval}**")
        st.write("---")

        # --- VISUALISASI: RADAR CHART (Kekal di atas) ---
        if selected_doc_eval != "Sila pilih klinik di Dashboard utama dahulu":
            st.subheader("📊 Profil Kemahiran Insaniah")
            categories = ['Pengalaman Pesakit', 'Kecerdasan Emosi', 'Kerjasama Pasukan', 'Mentorship', 'Komunikasi']
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=[85, 90, 78, 92, 88], 
                theta=categories,
                fill='toself',
                name='Skor Semasa',
                line_color='#27ae60'
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=False,
                height=350,
                margin=dict(t=30, b=30, l=30, r=30)
            )
            st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # --- 2. LOGIK NAVIGASI KAD (4 Kategori) ---
        if 'active_tab_inter' not in st.session_state:
            st.session_state['active_tab_inter'] = "Patient"

        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            is_active = st.session_state['active_tab_inter'] == "Patient"
            if st.button("😊\nPatient Experience", key="btn_patient", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state['active_tab_inter'] = "Patient"
                st.rerun()
                
        with col2:
            is_active = st.session_state['active_tab_inter'] == "EI"
            if st.button("🧠\nEmotional Intel.", key="btn_ei", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state['active_tab_inter'] = "EI"
                st.rerun()
                
        with col3:
            is_active = st.session_state['active_tab_inter'] == "Teamwork"
            if st.button("👥\nTeamwork", key="btn_team", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state['active_tab_inter'] = "Teamwork"
                st.rerun()
                
        with col4:
            is_active = st.session_state['active_tab_inter'] == "Mentorship"
            if st.button("🎓\nMentorship", key="btn_mentor", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state['active_tab_inter'] = "Mentorship"
                st.rerun()

        st.write("") 

        # --- 3. KANDUNGAN BERSYARAT ---
        
        # KATEGORI 1: PATIENT EXPERIENCE
        if st.session_state['active_tab_inter'] == "Patient":
            st.subheader("1. Pengalaman Pesakit (PSQ-18)")
            st.info("Berdasarkan borang maklum balas pesakit yang dikumpulkan secara bulanan.")
            st.slider("Skor Purata Kepuasan Pesakit", 0, 100, 88, key="psq_slider")
            st.text_area("Komen Utama Pesakit", placeholder="Contoh: Doktor sangat ramah...", key="psq_kom")
            st.button("Simpan Skor PSQ-18", type="primary", key="save_psq")

        # KATEGORI 2: EMOTIONAL INTELLIGENCE
        elif st.session_state['active_tab_inter'] == "EI":
            st.subheader("2. Kecerdasan Emosi (EI)")
            if selected_doc_eval != "Sila pilih klinik di Dashboard utama dahulu":
                st.markdown("**Pecahan Komponen Kecerdasan Emosi**")
                np.random.seed(hash(selected_doc_eval) % (2**32 - 1))
                ei_data = {
                    "Komponen": ["Self-Awareness", "Emotional Regulation", "Social Skills", "Empathy"],
                    "Skor": [np.random.randint(75, 95) for _ in range(4)]
                }
                df_ei = pd.DataFrame(ei_data)
                fig_ei = px.bar(df_ei, x="Skor", y="Komponen", orientation='h', 
                                color="Skor", color_continuous_scale='Greens', text_auto=True)
                fig_ei.update_layout(height=280, margin=dict(t=10, b=10, l=0, r=0), 
                                     showlegend=False, coloraxis_showscale=False)
                st.plotly_chart(fig_ei, use_container_width=True)

            st.divider()
            st.slider("Kesedaran Diri & Pengurusan Emosi", 0, 100, 85, key="ei_slider1")
            st.slider("Empati terhadap Rakan Setugas", 0, 100, 80, key="ei_slider2")
            st.button("Simpan Skor EI", type="primary", key="save_ei")

        # KATEGORI 3: TEAMWORK
        elif st.session_state['active_tab_inter'] == "Teamwork":
            st.subheader("3. Kerjasama & Kolaborasi Pasukan")
            if selected_doc_eval != "Sila pilih klinik di Dashboard utama dahulu":
                st.markdown("**Analisis Maklum Balas 360°**")
                roles = ["Rakan Setugas (Peers)", "Staf Sokongan/Nurse", "Pegawai Atasan"]
                feedback_scores = [np.random.randint(80, 98) for _ in range(3)]
                fig_team = go.Figure(data=[
                    go.Bar(x=roles, y=feedback_scores, marker_color='#27ae60', text=feedback_scores, textposition='auto')
                ])
                fig_team.update_layout(title="Purata Skor Penilaian Rakan Setugas", height=300, margin=dict(t=50, b=20, l=0, r=0))
                fig_team.update_yaxes(range=[0, 100])
                st.plotly_chart(fig_team, use_container_width=True)

            st.divider()
            st.radio("Tahap Sumbangan dalam Pasukan", ["Pasif", "Aktif", "Sangat Proaktif", "Ketua Pasukan"], key="team_radio")
            st.multiselect("Kualiti Kerjasama Utama", ["Boleh Dipercayai", "Komunikator Baik", "Penyelesai Konflik", "Fleksibel"], default=["Boleh Dipercayai"], key="team_multi")
            st.button("Simpan Skor Teamwork", type="primary", key="save_team")

        # KATEGORI 4: MENTORSHIP
        elif st.session_state['active_tab_inter'] == "Mentorship":
            st.subheader("4. Mentorship & Bimbingan")
            st.number_input("Bilangan Kakitangan Dibimbing (Mentees)", min_value=0, value=2, key="mentor_num")
            st.slider("Skor Keberkesanan Mentorship", 0, 100, 90, key="mentor_slider")
            st.button("Simpan Skor Mentorship", type="primary", key="save_mentor")