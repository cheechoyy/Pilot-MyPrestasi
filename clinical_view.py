import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def show_clinical_page():
    st.title("⚕️ Modul Penilaian: Clinical Excellence")
    st.markdown("Halaman khusus untuk penilaian klinikal pegawai perubatan.")
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

        tab1, tab2, tab3, tab4 = st.tabs(["🛠️ Skills", "🧠 Knowledge", "📝 Documentation", "📜 Policies"])

        with tab1:
            st.subheader("1. Kemahiran Klinikal (Skills)")
            
            # ==========================================
            # FUNGSI BAHARU: GRAF CUSUM PRESTASI DOKTOR
            # ==========================================
            if selected_doc_eval != "Sila pilih klinik di Dashboard utama dahulu":
                # Perhatikan jarak (indent) ke dalam di bawah ini
                st.markdown("**Analisis Prestasi CUSUM: Prosedur LIMA-LAD**")
                st.caption("Memantau lengkung pembelajaran (learning curve) berdasarkan 20 kes LIMA-LAD terakhir.")
                
                with st.container(border=True):
                    # 1. Jana data simulasi CUSUM berdasarkan nama doktor (supaya unik)
                    np.random.seed(hash(selected_doc_eval) % (2**32 - 1))
                    procedures = np.arange(1, 21) # 20 prosedur lepas
                    
                    # ==================================================
                    # PERUBAHAN MATEMATIK DI SINI (Logik LIMA-LAD Eksponen)
                    # ==================================================
                    learning_curve_scores = 88 - 15 * np.exp(-procedures / 6)
                    noise = np.random.normal(0, 3, 20)
                    actual_scores = learning_curve_scores + noise
                    target_score = 80
                    
                    # Formula CUSUM: Jumlah kumulatif (Skor Sebenar - Skor Sasaran)
                    cusum_values = np.cumsum(actual_scores - target_score)
                    
                    df_cusum = pd.DataFrame({
                        "Prosedur": procedures,
                        "Nilai CUSUM": cusum_values
                    })
                    
                    # 2. Bina Plotly Line Chart
                    fig = px.line(
                        df_cusum, 
                        x="Prosedur", 
                        y="Nilai CUSUM", 
                        markers=True,
                        labels={"Prosedur": "Bilangan Prosedur LIMA-LAD", "Nilai CUSUM": "Variasi CUSUM"}
                    )
                    
                    # Tambah garisan merah (Baseline 0)
                    fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Baseline KPI (80)")
                    
                    # Kemaskini warna dan margin
                    fig.update_traces(line_color="#00a0dc")
                    fig.update_layout(margin=dict(t=20, l=0, r=0, b=0), height=320)
                    
                    # Paparkan Graf (Guna width="stretch" untuk hilangkan amaran kuning)
                    st.plotly_chart(fig, width="stretch")
            
            st.write("") # Ruang kosong
            # ==========================================
            
            # Borang penilaian asal dikekalkan
            st.slider("Skor Pemerhatian Prosedur Baharu", 0, 100, 85, key="skill_slider")
            st.text_area("Komen Kemahiran", key="skill_kom")
            st.button("Simpan Skor Skills", type="primary")
            
        with tab2:
            st.subheader("2. Pengetahuan & Kapasiti")
            
            # PENAMBAHAN VISUALISASI KNOWLEDGE
            if selected_doc_eval != "Sila pilih klinik di Dashboard utama dahulu":
                st.markdown("**Status Pembelajaran & Mata CPD**")
                
                # Jana data simulasi berdasarkan nama doktor
                np.random.seed(hash(selected_doc_eval) % (2**32 - 1))
                cpd_score = np.random.randint(20, 55) # Mata CPD semasa
                cpd_target = 40 # Sasaran tahunan
                
                col_gauge, col_details = st.columns([1, 1])
                
                with col_gauge:
                    # 1. Gauge Chart untuk Mata CPD
                    fig_gauge = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = cpd_score,
                        title = {'text': "Kemajuan CPD (Tahun Ini)", 'font': {'size': 18}},
                        gauge = {
                            'axis': {'range': [None, 60], 'tickwidth': 1},
                            'bar': {'color': "#f1c40f"}, # Warna kuning tema Clinical
                            'steps': [
                                {'range': [0, 40], 'color': "#eeeeee"},
                                {'range': [40, 60], 'color': "#d4edda"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': cpd_target
                            }
                        }
                    ))
                    fig_gauge.update_layout(height=280, margin=dict(t=50, b=0, l=20, r=20))
                    st.plotly_chart(fig_gauge, width="stretch")

                with col_details:
                    # 2. Pecahan Kategori Pengetahuan
                    st.write("**Pecahan Aktiviti Pengetahuan:**")
                    st.info(f"""
                    * 📚 **CME/Workshop:** {np.random.randint(10, 25)} Mata
                    * 📝 **Clinical Audit:** {np.random.randint(5, 15)} Mata
                    * 🔬 **Research/Journal:** {np.random.randint(0, 10)} Mata
                    """)
                    
                    if cpd_score >= cpd_target:
                        st.success("✅ Sasaran Mata CPD Tahunan Dicapai!")
                    else:
                        st.warning(f"⚠️ Memerlukan {cpd_target - cpd_score} mata lagi untuk sasaran.")

            st.divider()
            # Borang Input Asal Kekal Di Sini
            st.slider("Kemas Kini Skor Ujian / CPD Points Baharu", 0, 100, 90, key="know_slider")
            st.button("Simpan Skor Knowledge", type="primary")
            
        with tab3:
            st.subheader("3. Dokumentasi")
            st.number_input("Purata Masa Siap Nota (Jam)", min_value=0.0, value=2.5, step=0.5)
            st.button("Simpan Skor Dokumentasi", type="primary")
            
        with tab4:
            st.subheader("4. Pematuhan Polisi & Protokol")
            st.slider("Kadar Pematuhan SOP (%)", 0, 100, 95, key="pol_slider")
            st.button("Simpan Skor Polisi", type="primary")