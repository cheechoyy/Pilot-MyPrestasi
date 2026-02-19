import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

def show_interpersonal_page():
    st.title("🤝 Modul Penilaian: Interpersonal Excellence")
    st.markdown("Halaman penilaian bagi pengalaman pesakit (PSQ-18), kerjasama pasukan, dan kepimpinan.")
    st.divider()

    with st.container(border=True):
        # Ambil senarai doktor dari sesi
        if st.session_state.get("doctor_list") is not None:
            doc_list = st.session_state["doctor_list"]["Nama Pegawai"].tolist()
        else:
            doc_list = ["Sila pilih klinik di Dashboard utama dahulu"]
            
        selected_doc_eval = st.selectbox("Pilih Pegawai Perubatan:", doc_list)
        st.write(f"Sesi Penilaian: **{selected_doc_eval}**")
        st.write("---")

        # --- VISUALISASI: RADAR CHART PRESTASI INTERPERSONAL ---
        if selected_doc_eval != "Sila pilih klinik di Dashboard utama dahulu":
            st.subheader("📊 Profil Kemahiran Insaniah")
            
            # Simulasi data untuk Radar Chart (Boleh ditarik dari DB pada masa depan)
            categories = ['Pengalaman Pesakit', 'Kecerdasan Emosi', 'Kerjasama Pasukan', 
                          'Mentorship', 'Komunikasi']
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=[85, 90, 78, 92, 88], # Skor simulasi
                theta=categories,
                fill='toself',
                name='Skor Semasa',
                line_color='#2ecc71' # Warna hijau mengikut butang sidebar
            ))

            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                showlegend=False,
                height=350,
                margin=dict(t=30, b=30, l=30, r=30)
            )
            st.plotly_chart(fig, width="stretch")

        # --- TAB PENILAIAN ---
        tab1, tab2, tab3, tab4 = st.tabs([
            "😊 Patient Experience", "🧠 Emotional Intelligence", 
            "👥 Teamwork", "🎓 Mentorship"
        ])

        with tab1:
            st.subheader("1. Pengalaman Pesakit (PSQ-18)")
            st.info("Berdasarkan borang maklum balas pesakit yang dikumpulkan secara bulanan.")
            st.slider("Skor Purata Kepuasan Pesakit", 0, 100, 88, key="psq_slider")
            st.text_area("Komen Utama Pesakit", placeholder="Contoh: Doktor sangat ramah dan mendengar penjelasan...")
            st.button("Simpan Skor PSQ-18", type="primary")

        with tab2:
            st.subheader("2. Kecerdasan Emosi (EI)")
            
            if selected_doc_eval != "Sila pilih klinik di Dashboard utama dahulu":
                st.markdown("**Pecahan Komponen Kecerdasan Emosi**")
                # Jana data simulasi komponen EI
                np.random.seed(hash(selected_doc_eval) % (2**32 - 1))
                ei_data = {
                    "Komponen": ["Self-Awareness", "Emotional Regulation", "Social Skills", "Empathy"],
                    "Skor": [np.random.randint(75, 95) for _ in range(4)]
                }
                df_ei = pd.DataFrame(ei_data)
                
                # Visualisasi Bar Mendatar (Horizontal Bar)
                fig_ei = px.bar(df_ei, x="Skor", y="Komponen", orientation='h', 
                                color="Skor", color_continuous_scale='Greens',
                                text_auto=True)
                fig_ei.update_layout(height=280, margin=dict(t=10, b=10, l=0, r=0), 
                                   showlegend=False, coloraxis_showscale=False)
                st.plotly_chart(fig_ei, width="stretch")

            st.divider()
            st.slider("Kesedaran Diri & Pengurusan Emosi", 0, 100, 85)
            st.slider("Empati terhadap Rakan Setugas", 0, 100, 80)
            st.button("Simpan Skor EI", type="primary")

        with tab3:
            st.subheader("3. Kerjasama & Kolaborasi Pasukan")
            
            if selected_doc_eval != "Sila pilih klinik di Dashboard utama dahulu":
                st.markdown("**Analisis Maklum Balas 360°**")
                # Data simulasi maklum balas dari pelbagai peringkat
                roles = ["Rakan Setugas (Peers)", "Staf Sokongan/Nurse", "Pegawai Atasan"]
                feedback_scores = [np.random.randint(80, 98) for _ in range(3)]
                
                fig_team = go.Figure(data=[
                    go.Bar(x=roles, y=feedback_scores, marker_color='#27ae60', text=feedback_scores, textposition='auto')
                ])
                fig_team.update_layout(title="Purata Skor Penilaian Rakan Setugas", 
                                     height=300, margin=dict(t=50, b=20, l=0, r=0))
                fig_team.update_yaxes(range=[0, 100])
                st.plotly_chart(fig_team, width="stretch")

            st.divider()
            st.radio("Tahap Sumbangan dalam Pasukan", ["Pasif", "Aktif", "Sangat Proaktif", "Ketua Pasukan"])
            st.multiselect("Kualiti Kerjasama Utama", ["Boleh Dipercayai", "Komunikator Baik", "Penyelesai Konflik", "Fleksibel"], default=["Boleh Dipercayai"])
            st.button("Simpan Skor Teamwork", type="primary")

        with tab4:
            st.subheader("4. Mentorship & Bimbingan")
            st.number_input("Bilangan Kakitangan Dibimbing (Mentees)", min_value=0, value=2)
            st.slider("Skor Keberkesanan Mentorship", 0, 100, 90)
            st.button("Simpan Skor Mentorship", type="primary")