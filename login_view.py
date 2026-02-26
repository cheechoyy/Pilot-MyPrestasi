import streamlit as st

def show_login_page():
    # 1. CSS KHAS: Gaya Serasi dengan Main Dashboard (Moden & Bersih)
    st.markdown("""
        <style>
        /* Latar belakang keseluruhan disamakan dengan Main Dashboard (#f4f7fe) */
        [data-testid="stAppViewContainer"] {
            background-color: #f4f7fe;
        }

        /* GAYA PANEL KIRI (INFO SISTEM) - Konsep Kad Terapung */
        .gov-panel { 
            background-color: #ffffff;
            padding: 40px 45px; 
            border-radius: 16px; /* Bucu membulat sama seperti kad dashboard */
            border: 1px solid #f0f2f6;
            box-shadow: 0 4px 15px rgba(0,0,0,0.03); /* Bayang-bayang lembut */
            height: 100%;
        }
        .gov-logo { width: 90px; margin-bottom: 25px; }
        .gov-title { font-size: 2.2rem; font-weight: 900; color: #1E3A8A; line-height: 1.2; font-family: Arial, sans-serif; text-transform: uppercase; margin-bottom: 10px; }
        .gov-subtitle { font-size: 1.05rem; font-weight: 500; color: #a3aed1; margin-bottom: 30px; border-bottom: 1px solid #f0f2f6; padding-bottom: 20px;}
        
        /* Senarai Ciri-ciri */
        .gov-list { list-style-type: none; padding: 0; margin: 0 0 40px 0; }
        .gov-list li { font-size: 0.95rem; color: #2b3674; font-weight: 600; margin-bottom: 15px; display: flex; align-items: center; }
        
        /* Ikon 'Tick' dikemaskini guna warna biru terang (#4318FF) */
        .gov-list li::before { 
            content: "✓"; 
            color: #4318FF; 
            font-weight: bold; 
            margin-right: 15px; 
            font-size: 1rem; 
            background: #E2E8FF; 
            border-radius: 50%; 
            width: 26px; 
            height: 26px; 
            display: inline-flex; 
            justify-content: center; 
            align-items: center;
        }

        /* Kotak Amaran Keselamatan Diperhalusi */
        .security-notice { 
            background-color: #FFF0F0; 
            border: 1px solid #FFD6D6;
            padding: 15px 20px; 
            font-size: 0.85rem; 
            color: #D32F2F; 
            border-radius: 12px;
            line-height: 1.5;
        }
        .security-notice strong { color: #B71C1C; display: block; margin-bottom: 5px; font-size: 0.9rem;}

        /* GAYA PANEL KANAN (KAD LOG MASUK) - Konsep Kad Terapung */
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) { 
            background-color: #ffffff; 
            border-radius: 16px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.03); 
            padding: 40px 35px !important; 
            border: 1px solid #f0f2f6;
        }
        
        /* Gaya Kotak Input */
        div.stTextInput > div > div > input { 
            border-radius: 12px; 
            padding: 12px 15px; 
            border: 1px solid #e2e8f0; 
            background-color: #f8f9fa;
            color: #2b3674;
        }
        div.stTextInput > div > div > input:focus { border-color: #4318FF; box-shadow: 0 0 0 1px #4318FF; }
        
        /* Tombol LOGIN - Diselaraskan dengan warna butang Dashboard (#4318FF) */
        div.stButton > button[kind="primary"] { 
            background-color: #4318FF !important; 
            color: white !important;
            border-radius: 12px !important; 
            height: 50px; 
            font-weight: 800 !important; 
            font-size: 1.05rem !important; 
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
        }
        div.stButton > button[kind="primary"]:hover { 
            background-color: #3311DB !important; 
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(67,24,255,0.2); 
        }

        /* Butang SSO (Secondary) */
        div.stButton > button[kind="secondary"] {
            border-radius: 12px !important;
            height: 50px;
            font-weight: 700 !important;
            color: #2b3674 !important;
            border: 1px solid #e2e8f0 !important;
        }

        /* Toggle Admin/Staff */
        div.row-widget.stRadio > div { flex-direction: row; gap: 20px; background-color: #f4f7fe; padding: 10px 15px; border-radius: 12px; border: none; }

        /* Footer */
        .login-footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; padding: 15px; color: #a3aed1; font-size: 0.8rem; background-color: transparent; font-weight: 500; z-index: 100;}
        </style>
    """, unsafe_allow_html=True)

    # 2. Susun Atur (Layout)
    st.write("<br>", unsafe_allow_html=True) # Jarak dari atas
    col_info, col_form = st.columns([1.2, 1], gap="large")

    # --- PANEL KIRI: INFO SISTEM ---
    with col_info:
        html_kiri = (
            '<div class="gov-panel">'
            '<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Coat_of_arms_of_Malaysia.svg/800px-Coat_of_arms_of_Malaysia.svg.png" class="gov-logo" alt="Jata Negara">'
            '<div class="gov-title">MyPrestasi</div>'
            '<div class="gov-subtitle">Portal Pemantauan Prestasi & Penilaian Fasiliti Kesihatan</div>'
            '<ul class="gov-list">'
            '<li>Modul Analitik Data & Pelaporan (CUSUM)</li>'
            '<li>Pengurusan Penjadualan Atas Talian</li>'
            '<li>Penilaian Petunjuk Prestasi Utama (KPI) Fasiliti</li>'
            '<li>Penyimpanan Log Pegawai & Kakitangan</li>'
            '</ul>'
            '<div class="security-notice">'
            '<strong>AMARAN KESELAMATAN</strong>'
            'Penggunaan sistem ini adalah terhad kepada pengguna yang sah sahaja. Sebarang capaian tanpa kebenaran adalah satu kesalahan di bawah Akta Jenayah Komputer 1997.'
            '</div>'
            '</div>'
        )
        st.markdown(html_kiri, unsafe_allow_html=True)

    # --- PANEL KANAN: FORM LOGIN ---
    with col_form:
        st.markdown('<h2 style="color:#1E3A8A; margin-top:0px; margin-bottom: 25px; font-weight:800; text-align: center;">LOG MASUK PENGGUNA</h2>', unsafe_allow_html=True)
        
        role = st.radio("Peranan:", ["Admin", "Staff"], horizontal=True, label_visibility="collapsed")
        
        st.write("") 
        user = st.text_input("ID Pengguna / E-mel", placeholder="contoh@moh.gov.my")
        pwd = st.text_input("Kata Laluan", type="password", placeholder="••••••••")
        
        c1, c2 = st.columns(2)
        with c1: 
            st.checkbox("Ingat Saya")
        with c2: 
            st.markdown("<div style='text-align: right; padding-top: 8px;'><a href='#' style='text-decoration:none; font-size:13px; color:#4318FF; font-weight:700;'>LUPA KATA LALUAN?</a></div>", unsafe_allow_html=True)

        st.write("") 
        
        if st.button("LOG MASUK", use_container_width=True, type="primary"):
            if pwd == "123": 
                st.session_state["logged_in"] = True
                st.session_state["role"] = role
                st.rerun()
            else:
                st.error("Ralat: Kata laluan tidak sah.")
        
        st.write("") 
        st.button("Log Masuk via MyIdentity (SSO)", use_container_width=True, icon="🔐")

    # 3. Footer
    html_footer = '<div class="login-footer">Hak Cipta Terpelihara © 2026 Kementerian Kesihatan Malaysia (KKM).<br>Sistem ini dipantau secara berterusan. Paparan terbaik menggunakan Google Chrome resolusi 1920x1080.</div>'
    st.markdown(html_footer, unsafe_allow_html=True)