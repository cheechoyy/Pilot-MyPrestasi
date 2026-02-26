import streamlit as st

def show_login_page():
    # 1. CSS KHAS
    st.markdown("""
        <style>
        /* Mengubah warna butang primary (LOGIN) */
        div.stButton > button[kind="primary"] {
            background-color: #6a9cff;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 24px;
            font-weight: bold;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        div.stButton > button[kind="primary"]:hover {
            background-color: #5888ed;
        }
        
        /* Panel Kiri (Biru Gradien) */
        .blue-panel {
            background: linear-gradient(135deg, #026DB4 0%, #0093E9 100%);
            padding: 50px 40px;
            border-radius: 20px;
            color: white;
            height: 100%;
            min-height: 550px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        .blue-panel h1 {
            color: white;
            font-size: 2.5rem;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 40px;
        }
        
        /* Gaya Senarai (List) Meniru Gambar Rujukan Kedua */
        .feature-list {
            list-style-type: none;
            padding: 0;
            margin: 0;
        }
        .feature-list li {
            margin-bottom: 20px;
            font-size: 1.05rem;
            display: flex;
            align-items: center;
            font-weight: 500;
        }
        .feature-list li span.icon {
            margin-right: 15px;
            background: rgba(255, 255, 255, 0.15);
            border-radius: 50%;
            display: inline-flex;
            width: 32px;
            height: 32px;
            justify-content: center;
            align-items: center;
            font-size: 0.9rem;
        }
        
        /* Footer Kekal */
        .login-footer {
            position: fixed; left: 0; bottom: 0; width: 100%;
            background-color: #f8f9fa; color: #888;
            text-align: center; padding: 15px 0; font-size: 0.8rem;
            border-top: 1px solid #eee; z-index: 100;
        }
        .main .block-container { padding-bottom: 80px; }
        
        /* Menjadikan st.radio nampak lebih seperti toggle melintang */
        div.row-widget.stRadio > div {
            flex-direction: row;
            gap: 20px;
            background-color: #f8f9fa;
            padding: 10px 15px;
            border-radius: 10px;
            border: 1px solid #eee;
        }
        </style>
    """, unsafe_allow_html=True)

    col_info, col_form = st.columns([1.2, 1], gap="large")

    with col_info:
        # Kod HTML senarai ciri-ciri tanpa kotak/berita
        st.markdown(
            '<div class="blue-panel">'
            '<h1>MyPrestasi<br>Medical Portal</h1>'
            '<ul class="feature-list">'
            '<li><span class="icon">📊</span> Data Analytics</li>'
            '<li><span class="icon">📅</span> Online Scheduling</li>'
            '<li><span class="icon">📋</span> Resulting</li>'
            '<li><span class="icon">📈</span> KPI</li>'
            '<li><span class="icon">📝</span> Log</li>'
            '<li><span class="icon">🔍</span> CUSUM</li>'
            '</ul>'
            '</div>', 
            unsafe_allow_html=True
        )

    with col_form:
        # BORANG LOG MASUK
        c_logo, _ = st.columns([1, 2])
        with c_logo:
            st.image("logo1.png", use_container_width=True) 
            
        st.markdown('<h2 style="color:#1E293B; margin-top:10px; margin-bottom: 20px;">Login</h2>', unsafe_allow_html=True)
        
        # Ditukar kepada radio button melintang untuk mimic "Admin | Staff" toggle
        role = st.radio("Please select role:", ["Admin", "Staff"], horizontal=True, label_visibility="collapsed")
        
        st.write("") # Ruang kosong
        user = st.text_input("Email", placeholder="ymaiel@mail.com")
        pwd = st.text_input("Password", type="password", placeholder="••••••••")
        
        c1, c2 = st.columns(2)
        with c1: 
            st.checkbox("Save User")
        with c2: 
            st.markdown("<div style='text-align: right; padding-top: 8px;'><a href='#' style='text-decoration:none; font-size:14px; color:#6a9cff; font-weight:bold;'>FORGET PASSWORD?</a></div>", unsafe_allow_html=True)

        st.write("") 
        
        # Logik asal dikekalkan
        if st.button("LOGIN", use_container_width=True, type="primary"):
            if pwd == "123": 
                st.session_state["logged_in"] = True
                st.session_state["role"] = role
                st.rerun()
            else:
                st.error("Incorrect password.")
        
        st.write("") 
        st.button("Sign in with Google", use_container_width=True, icon="🌐")
        st.markdown("<center style='margin-top:15px; font-size: 0.9rem;'>Don't have an account? <b style='color:#6a9cff;'>Sign up</b></center>", unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <div class="login-footer">
            Copyright © 2026 MyPrestasi HPU | Selangor State Health Unit
        </div>
    """, unsafe_allow_html=True)