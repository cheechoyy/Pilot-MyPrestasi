import streamlit as st

def show_login_page():
    col_form, col_img = st.columns([1, 1.2], gap="large")

    with col_form:
        # Kod Baharu
        st.image("logo1.png", width=550)
        #st.markdown('<p class="medstar-blue">🌀 MyPRESTASI</p>', unsafe_allow_html=True)
        
        st.markdown('<p class="login-title">Welcome back</p>', unsafe_allow_html=True)
        st.write("Welcome back! Please enter your details.")
        
        role = st.selectbox("Role", ["Admin", "Staff (Doctor)"])
        user = st.text_input("Email / Username", placeholder="Enter your email")
        pwd = st.text_input("Password", type="password", placeholder="••••••••")
        
        c1, c2 = st.columns(2)
        with c1: st.checkbox("Remember for 30 days")
        with c2: st.markdown("[Forgot password](https://google.com)")

        if st.button("Sign in", use_container_width=True, type="primary"):
            if pwd == "123": 
                st.session_state["logged_in"] = True
                st.session_state["role"] = role
                st.rerun()
            else:
                st.error("Incorrect password.")
        
        st.button("Sign in with Google", use_container_width=True, icon="🌐")
        st.markdown("<center>Don't have an account? <b>Sign up</b></center>", unsafe_allow_html=True)

    with col_img:
        st.image("https://images.unsplash.com/photo-1551076805-e1869033e561?q=80&w=2070&auto=format&fit=crop", use_container_width=True)
        # Gantikan Baris 32-37 dengan ini:
        st.markdown("""
            <style>
            .testimonial-box {
                background: rgba(255, 255, 255, 0.95);
                padding: 25px;
                border-radius: 12px;
                border-left: 5px solid #00a0dc;
                box-shadow: 0 8px 20px rgba(0,0,0,0.15);
                margin-top: -100px; /* Menaikkan kotak ke atas gambar */
                margin-left: 20px;
                margin-right: 20px;
                position: relative;
                z-index: 10;
            }
            .quote-text {
                font-style: italic;
                font-size: 1.05rem;
                color: #333;
                line-height: 1.5;
                margin-bottom: 10px;
            }
            .quote-author {
                font-weight: bold;
                color: #004a99;
                font-size: 0.95rem;
            }
            </style>
            
            <div class="testimonial-box">
                <p class="quote-text">"Data yang telus membolehkan kita menambah baik sistem kesihatan secara berterusan. MyPrestasi adalah kunci kepada transformasi ini.."</p>
                <p class="quote-author">Dr. Mohd Azlan<br>
                <span style='font-weight:normal; color:#666; font-size:0.85rem;'>Attending physician, FMS Clinic</span></p>
            </div>
        """, unsafe_allow_html=True)

        # Tambah di akhir fail login_view.py
    st.write("---")
    col_info, col_empty = st.columns([1, 1])
    
    with col_info:
        st.markdown("""
            <div style="padding: 10px 0;">
                <h4 style="color: #004a99; margin-bottom: 5px;">🆘 Pusat Bantuan IT</h4>
                <p style="color: #666; font-size: 0.9rem;">
                    Menghadapi masalah log masuk? Hubungi pentadbir sistem di:<br>
                    📧 <b>support.hpu@selangor.gov.my</b> | 📞 <b>Ext: 4040</b>
                </p>
            </div>
        """, unsafe_allow_html=True)

    # Footer Kekal di Bawah Skrin
    st.markdown("""
        <style>
        .login-footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #f8f9fa;
            color: #888;
            text-align: center;
            padding: 15px 0;
            font-size: 0.8rem;
            border-top: 1px solid #eee;
        }
        </style>
        <div class="login-footer">
            Hak Cipta Terpelihara © 2026 MyPrestasi HPU | Unit Kesihatan Negeri Selangor
        </div>
    """, unsafe_allow_html=True)