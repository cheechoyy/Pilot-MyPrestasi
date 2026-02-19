import streamlit as st

def show_operational_page():
    st.title("⚙️ Modul Penilaian: Operational Excellence")
    st.markdown("Halaman pemantauan produktiviti dan inovasi pegawai perubatan.")
    st.divider()

    with st.container(border=True):
        # Ambil senarai doktor dari sesi (jika ada)
        if st.session_state.get("doctor_list") is not None:
            doc_list = st.session_state["doctor_list"]["Nama Pegawai"].tolist()
        else:
            doc_list = ["Sila pilih klinik di Dashboard utama dahulu"]
            
        selected_doc_eval = st.selectbox("Pilih Pegawai Perubatan:", doc_list, key="op_select")
        st.write(f"Sesi Penilaian: **{selected_doc_eval}**")
        st.write("---")

        # Tab untuk Kategori Operational
        tab1, tab2 = st.tabs(["⏱️ Productivity & Efficiency", "💡 Innovation & Problem Solving"])

        with tab1:
            st.subheader("1. Produktiviti & Kecekapan")
            st.number_input("Purata Kes Harian Dirawat", min_value=0, value=45, step=1)
            st.slider("Skor Kecekapan Pengurusan Masa", 0, 100, 80, key="prod_slider")
            st.button("Simpan Skor Produktiviti", type="primary")
            
        with tab2:
            st.subheader("2. Inovasi & Penyelesaian Masalah")
            st.radio("Penglibatan Projek Inovasi (QA/QI)?", ["Tiada", "Ahli", "Ketua Projek"])
            st.text_area("Contoh Penyelesaian Masalah", key="inov_kom")
            st.button("Simpan Skor Inovasi", type="primary")