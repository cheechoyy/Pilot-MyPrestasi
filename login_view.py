import streamlit as st

def show_login_page():
    # 1. SPECIAL CSS: Consistent with Main Dashboard Theme (Modern & Clean)
    st.markdown("""
        <style>
        /* Import Google Font (Inter) for a modern, sleek look */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap');

        /* Overall background matched to Main Dashboard (#f4f7fe) */
        [data-testid="stAppViewContainer"] {
            background-color: #f4f7fe;
            font-family: 'Inter', sans-serif;
        }

        /* LEFT PANEL STYLE (SYSTEM INFO) - Floating Card Concept */
        .gov-panel { 
            background-color: #ffffff;
            padding: 40px 45px; 
            border-radius: 16px; 
            border: 1px solid #f0f2f6;
            box-shadow: 0 4px 15px rgba(0,0,0,0.03); 
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
        
        /* Logo Container - Ditarik naik ke atas */
        .logo-container {
            display: flex;
            align-items: center;
            gap: 20px; 
            margin-top: -35px; 
            margin-bottom: 25px;
        }
        
        /* MODERN STYLING FOR 'MYPRESTASI' TITLE */
        .gov-title { 
            font-size: 2.4rem; 
            font-weight: 900; 
            color: #1E3A8A; 
            line-height: 1.1; 
            font-family: 'Inter', sans-serif; 
            letter-spacing: -1px; 
            text-transform: uppercase; 
            margin-bottom: 8px; 
        }
        
        .gov-subtitle { 
            font-size: 1rem; 
            font-weight: 500; 
            color: #8fa0c9; 
            margin-bottom: 30px; 
            border-bottom: 1px solid #f0f2f6; 
            padding-bottom: 20px;
            font-family: 'Inter', sans-serif;
        }
        
        /* Features List */
        .gov-list { list-style-type: none; padding: 0; margin: 0 0 30px 0; font-family: 'Inter', sans-serif;}
        .gov-list li { font-size: 0.95rem; color: #2b3674; font-weight: 600; margin-bottom: 15px; display: flex; align-items: center; }
        
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

        /* Refined Security Warning Box */
        .security-notice { 
            background-color: #FFF0F0; 
            border: 1px solid #FFD6D6;
            padding: 15px 20px; 
            font-size: 0.85rem; 
            color: #D32F2F; 
            border-radius: 12px;
            line-height: 1.5;
            font-family: 'Inter', sans-serif;
            margin-bottom: 20px;
        }
        .security-notice strong { color: #B71C1C; display: block; margin-bottom: 5px; font-size: 0.9rem;}

        /* Quick Links Section */
        .quick-links {
            border-top: 1px solid #f0f2f6;
            padding-top: 20px;
            font-size: 0.9rem;
            color: #2b3674;
            font-weight: 500;
        }
        .quick-links a {
            color: #4318FF;
            text-decoration: none;
            font-weight: 600;
            margin-right: 15px;
        }
        .quick-links a:hover { text-decoration: underline; }

        /* RIGHT PANEL STYLE (LOGIN CARD) */
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) { 
            background-color: #ffffff; 
            border-radius: 16px; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.03); 
            padding: 40px 35px !important; 
            border: 1px solid #f0f2f6;
        }
        
        /* Input Box Style */
        div.stTextInput > div > div > input { 
            border-radius: 12px; 
            padding: 12px 15px; 
            border: 1px solid #e2e8f0; 
            background-color: #f8f9fa;
            color: #2b3674;
            font-family: 'Inter', sans-serif;
        }
        div.stTextInput > div > div > input:focus { border-color: #4318FF; box-shadow: 0 0 0 1px #4318FF; }
        
        /* --- GAYA BAHARU: TOGGLE ADMIN/STAFF DIPANJANGKAN --- */
        div[role="radiogroup"] {
            background-color: #f1f5f9; 
            padding: 6px;
            border-radius: 12px;
            display: flex;
            width: 280px; /* Diberikan lebar tetap supaya panjang dan tidak sempit */
            gap: 4px;
        }
        div[role="radiogroup"] > label {
            flex: 1; 
            justify-content: center;
            padding: 10px 5px; /* Padding dikurangkan */
            border-radius: 8px;
            cursor: pointer;
            margin: 0;
            transition: all 0.2s ease;
            white-space: nowrap; /* CRITICAL: Elak perkataan Admin turun baris baru */
        }
        /* Sembunyikan bulatan radio */
        div[role="radiogroup"] > label > div:first-child {
            display: none;
        }
        /* Teks dalam butang (Tidak Aktif) */
        div[role="radiogroup"] > label > div:last-child p {
            color: #64748b;
            font-weight: 600;
            font-size: 0.95rem;
            margin: 0;
            font-family: 'Inter', sans-serif;
            white-space: nowrap; /* CRITICAL */
        }
        /* Teks & Latar Belakang (Apabila Ditekan/Aktif) */
        div[role="radiogroup"] > label:has(input:checked) {
            background-color: #ffffff;
            box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        }
        div[role="radiogroup"] > label:has(input:checked) > div:last-child p {
            color: #4318FF; 
        }
        /* ------------------------------------------------------------------------ */

        /* LOGIN Button */
        div.stButton > button[kind="primary"] { 
            background-color: #4318FF !important; 
            color: white !important;
            border-radius: 12px !important; 
            height: 50px; 
            font-weight: 800 !important; 
            font-size: 1.05rem !important; 
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            font-family: 'Inter', sans-serif;
        }
        div.stButton > button[kind="primary"]:hover { 
            background-color: #3311DB !important; 
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(67,24,255,0.2); 
        }

        /* SSO Button */
        div.stButton > button[kind="secondary"] {
            border-radius: 12px !important;
            height: 50px;
            font-weight: 700 !important;
            color: #2b3674 !important;
            border: 1px solid #e2e8f0 !important;
            font-family: 'Inter', sans-serif;
        }

        /* Helpdesk Box */
        .helpdesk-box {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px dashed #e2e8f0;
            text-align: center;
            font-size: 0.85rem;
            color: #8fa0c9;
            line-height: 1.6;
            font-family: 'Inter', sans-serif;
        }
        .helpdesk-box b { color: #2b3674; }

        /* Footer */
        .login-footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; padding: 15px; color: #a3aed1; font-size: 0.8rem; background-color: transparent; font-weight: 500; z-index: 100; font-family: 'Inter', sans-serif;}
        </style>
    """, unsafe_allow_html=True)

    # 2. Layout
    st.write("<br>", unsafe_allow_html=True) 
    col_info, col_form = st.columns([1.2, 1], gap="large")

    # --- LEFT PANEL: SYSTEM INFO ---
    with col_info:
        html_left = (
            '<div class="gov-panel">'
            '<div>' 
            '<div class="logo-container">'
            # KKM LOGO (Stable direct link + Fixed Size & Multiply Blend)
            '<img src="https://sebenarnya.my/wp-content/uploads/2017/06/Logo-KKM-e1518677887552.jpg" style="height: 65px; width: auto; mix-blend-mode: multiply;" alt="KKM Logo">'
            
            # KAMI SEDIA MEMBANTU LOGO (Stable direct link + Fixed Size & Multiply Blend)
            '<img src="https://imgv2-2-f.scribdassets.com/img/document/738030853/original/08c4aa6b37/1?v=1" style="height: 85px; width: auto; mix-blend-mode: multiply;" alt="Kami Sedia Membantu Logo">'
            '</div>'
            
            '<div class="gov-title">MYPRESTASI</div>'
            '<div class="gov-subtitle">Health Facility Performance Monitoring & Evaluation Portal</div>'
            '<ul class="gov-list">'
            '<li>Data Analytics & Reporting Module (CUSUM)</li>'
            '<li>Online Scheduling Management</li>'
            '<li>Facility Key Performance Indicator (KPI) Evaluation</li>'
            '<li>Officer & Staff Log Storage</li>'
            '</ul>'
            '<div class="security-notice">'
            '<strong>SECURITY WARNING</strong>'
            'Access to this system is restricted to authorized users only. Any unauthorized access is an offense under the Computer Crimes Act 1997.'
            '</div>'
            '</div>'
            
            '<div class="quick-links">'
            '📚 <a href="#" target="_blank">User Manual (PDF)</a> | ❓ <a href="#" target="_blank">System FAQ</a>'
            '</div>'
            
            '</div>'
        )
        st.markdown(html_left, unsafe_allow_html=True)

    # --- RIGHT PANEL: LOGIN FORM ---
    with col_form:
        st.markdown('<h2 style="color:#1E3A8A; margin-top:0px; margin-bottom: 25px; font-weight:900; font-family: \'Inter\', sans-serif; font-size: 2rem; letter-spacing: -0.5px; text-transform: uppercase; text-align: left;">USER LOGIN</h2>', unsafe_allow_html=True)
        
        role = st.radio("Role:", ["Admin", "Staff"], horizontal=True, label_visibility="collapsed")
        
        st.write("") 
        user = st.text_input("User ID / Email", placeholder="example@moh.gov.my")
        pwd = st.text_input("Password", type="password", placeholder="••••••••")
        
        c1, c2 = st.columns(2)
        with c1: 
            st.checkbox("Remember Me")
        with c2: 
            st.markdown("<div style='text-align: right; padding-top: 8px;'><a href='#' style='text-decoration:none; font-size:13px; color:#4318FF; font-weight:700; font-family: \'Inter\', sans-serif;'>FORGOT PASSWORD?</a></div>", unsafe_allow_html=True)

        st.write("") 
        
        if st.button("LOGIN", use_container_width=True, type="primary"):
            if pwd == "123": 
                st.session_state["logged_in"] = True
                st.session_state["role"] = role
                st.rerun()
            else:
                st.error("Error: Invalid password.")
        
        st.write("") 
        st.button("Login via MyIdentity (SSO)", use_container_width=True, icon="🔐")

        st.markdown("""
            <div class="helpdesk-box">
                Having trouble logging in?<br>
                Contact MOH Helpdesk: <b>1-800-88-xxxx</b> or email <b>helpdesk@moh.gov.my</b><br>
                (Operating Hours: Mon - Fri, 8:00 AM - 5:00 PM)
            </div>
        """, unsafe_allow_html=True)

    # 3. Footer
    html_footer = '<div class="login-footer">Copyright © 2026 Ministry of Health Malaysia (MOH).<br>This system is continuously monitored. Best viewed using Google Chrome at 1920x1080 resolution.</div>'
    st.markdown(html_footer, unsafe_allow_html=True)