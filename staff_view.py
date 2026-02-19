import streamlit as st

def show_staff_dashboard():
    st.title("Portal Doktor")
    st.divider()
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info("👋 Selamat datang, Doktor.")
        st.warning("Halaman ini sedang dalam penyelenggaraan (Blank Page).")
        st.write("Sila hubungi admin untuk kemaskini KPI.")
    
    with col2:
        st.image("https://images.unsplash.com/photo-1622902046580-2b47f47f5471?q=80&w=2000", caption="Work in Progress")