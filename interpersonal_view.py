import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

def show_interpersonal_page():
    st.title("🤝 Interpersonal Excellence")
    st.markdown("Evaluation page for patient experience (PSQ-18), teamwork, and leadership.")
    st.divider()

    # --- 1. SPECIAL CSS (Interpersonal Green Theme + Compact Fit 1 Page) ---
    st.markdown("""
    <style>
        /* Kurangkan jarak antara widget */
        [data-testid="stVerticalBlock"] {
            gap: 0.3rem !important;
        }

        /* Card-style Buttons Navigation */
        div[data-testid="stHorizontalBlock"] div.stButton > button {
            height: 100px !important; /* Saiz padat tetapi jelas */
            width: 100% !important;
            border-radius: 12px !important;
            background-color: #ffffff !important;
            border: 1px solid #e0e0e0 !important;
            color: #31333F !important;
            box-shadow: 0px 2px 5px rgba(0,0,0,0.02) !important;
            transition: all 0.2s ease-in-out !important;
            font-size: 15px !important;
            line-height: 1.2 !important;
            font-weight: bold !important;
        }

        /* Style for ACTIVE button - Green */
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
        # =========================================================================
        # LOGIK BAHARU: PILIH NEGERI -> MUNCUL PEGAWAI (Data Mockup Dinamik)
        # =========================================================================
        mock_state_officers = {
            "Johor": ["Dr. Ali (998)", "Dr. Muthu (104)", "Dr. Siti (205)"],
            "Kedah": ["Dr. Hassan (112)", "Dr. Zikri (113)"],
            "Kelantan": ["Dr. Amir (221)", "Dr. Sofea (222)"],
            "Kuala Lumpur": ["Dr. Farhana (553)", "Dr. David (201)"],
            "Labuan": ["Dr. John (331)"],
            "Melaka": ["Dr. Ramesh (405)", "Dr. Kumar (406)"],
            "Negeri Sembilan": ["Dr. Aina (501)", "Dr. Danial (502)"],
            "Pahang": ["Dr. Fazura (601)", "Dr. Kamal (602)"],
            "Perak": ["Dr. Chong (302)", "Dr. Wei (303)"],
            "Perlis": ["Dr. Azim (701)"],
            "Pulau Pinang": ["Dr. Lim (801)", "Dr. Sarah (802)"],
            "Putrajaya": ["Dr. Aisyah (102)", "Dr. Badrul (902)"],
            "Sabah": ["Dr. Bernard (712)", "Dr. Michael (881)"],
            "Sarawak": ["Dr. Wong (901)", "Dr. Lina (922)"],
            "Selangor": ["Dr. Kassim (123)", "Dr. Nabila (124)"],
            "Terengganu": ["Dr. Osman (234)", "Dr. Liyana (235)"]
        }
        
        # Susun dropdown bersebelahan untuk jimat ruang
        col_negeri, col_pegawai = st.columns(2)
        
        with col_negeri:
            senarai_negeri = ["Semua Negeri"] + list(mock_state_officers.keys())
            pilihan_negeri = st.selectbox("Pilih Negeri:", options=senarai_negeri, index=0, key="int_state_sel")
            
        with col_pegawai:
            if pilihan_negeri == "Semua Negeri":
                # Gabungkan semua doktor
                doc_list = []
                for officers in mock_state_officers.values():
                    doc_list.extend(officers)
            else:
                # Tapis doktor mengikut negeri
                doc_list = mock_state_officers.get(pilihan_negeri, [])
                
            selected_doc_eval = st.selectbox("Select Medical Officer:", options=doc_list, key="int_doc_sel")
            
        if not selected_doc_eval:
            st.warning("Tiada pegawai dijumpai.")
            st.stop()

        st.write(f"Evaluation Session: **{selected_doc_eval}**")
        st.write("") # Dibuang garisan pemisah untuk jimat ruang

        # --- VISUALIZATION: RADAR CHART (Ketinggian Dikecilkan) ---
        st.markdown("#### 📊 Soft Skills Profile")
        categories = ['Patient Experience', 'Emotional Intelligence', 'Teamwork', 'Mentorship', 'Communication']
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=[85, 90, 78, 92, 88], 
            theta=categories,
            fill='toself',
            name='Current Score',
            line_color='#27ae60'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            height=280, # Dikurangkan dari 350px kepada 280px
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig, use_container_width=True)

        st.write("") # Dibuang garisan pemisah untuk jimat ruang

        # --- 2. CARD NAVIGATION LOGIC (4 Categories) ---
        if 'active_tab_inter' not in st.session_state:
            st.session_state['active_tab_inter'] = "Patient"

        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            is_active = st.session_state['active_tab_inter'] == "Patient"
            if st.button("😊\nPatient Exp.", key="btn_patient", type="primary" if is_active else "secondary", use_container_width=True):
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

        # --- 3. CONDITIONAL CONTENT ---
        
        # CATEGORY 1: PATIENT EXPERIENCE
        if st.session_state['active_tab_inter'] == "Patient":
            st.subheader("1. Patient Experience (PSQ-18)")
            st.info("Based on patient feedback forms collected monthly.")
            st.slider("Average Patient Satisfaction Score", 0, 100, 88, key="psq_slider")
            st.text_area("Key Patient Comments", placeholder="Example: The doctor was very friendly...", key="psq_kom")
            st.button("Save PSQ-18 Score", type="primary", key="save_psq")

        # CATEGORY 2: EMOTIONAL INTELLIGENCE
        elif st.session_state['active_tab_inter'] == "EI":
            st.subheader("2. Emotional Intelligence (EI)")
            st.markdown("**Emotional Intelligence Component Breakdown**")
            
            np.random.seed(hash(selected_doc_eval) % (2**32 - 1))
            ei_data = {
                "Component": ["Self-Awareness", "Emotional Regulation", "Social Skills", "Empathy"],
                "Score": [np.random.randint(75, 95) for _ in range(4)]
            }
            df_ei = pd.DataFrame(ei_data)
            fig_ei = px.bar(df_ei, x="Score", y="Component", orientation='h', 
                            color="Score", color_continuous_scale='Greens', text_auto=True)
            # Ketinggian dikurangkan untuk muat halaman
            fig_ei.update_layout(height=200, margin=dict(t=10, b=10, l=0, r=0), 
                                 showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig_ei, use_container_width=True)

            st.slider("Self-Awareness & Emotional Management", 0, 100, 85, key="ei_slider1")
            st.slider("Empathy towards Colleagues", 0, 100, 80, key="ei_slider2")
            st.button("Save EI Score", type="primary", key="save_ei")

        # CATEGORY 3: TEAMWORK
        elif st.session_state['active_tab_inter'] == "Teamwork":
            st.subheader("3. Teamwork & Collaboration")
            
            # --- SUB-MENU UNTUK ADMIN VIEW ---
            teamwork_view = st.radio(
                "Select View:", 
                ["360° Feedback Analysis", "Teamwork Contribution Log"], 
                horizontal=True,
                label_visibility="collapsed"
            )
            
            # ==========================================
            # PAPARAN 1: 360 FEEDBACK (ASAL)
            # ==========================================
            if teamwork_view == "360° Feedback Analysis":
                st.markdown("**360° Feedback Analysis**")
                roles = ["Peers", "Support Staff/Nurses", "Supervisors"]
                np.random.seed(hash(selected_doc_eval) % (2**32 - 1))
                feedback_scores = [np.random.randint(80, 98) for _ in range(3)]
                
                fig_team = go.Figure(data=[
                    go.Bar(x=roles, y=feedback_scores, marker_color='#27ae60', text=feedback_scores, textposition='auto')
                ])
                fig_team.update_layout(height=220, margin=dict(t=20, b=20, l=0, r=0))
                fig_team.update_yaxes(range=[0, 100])
                st.plotly_chart(fig_team, use_container_width=True)

                st.radio("Level of Team Contribution", ["Passive", "Active", "Highly Proactive", "Team Leader"], key="team_radio", horizontal=True)
                st.multiselect("Key Collaboration Qualities", ["Reliable", "Good Communicator", "Conflict Resolver", "Flexible"], default=["Reliable"], key="team_multi")
                st.button("Save Teamwork Score", type="primary", key="save_team")

            # ==========================================
            # PAPARAN 2: CONTRIBUTION LOG
            # ==========================================
            elif teamwork_view == "Teamwork Contribution Log":
                st.markdown("**Teamwork Contribution Log**")
                st.caption("Visualizing support and assistance provided to colleagues over time.")
                
                if 'teamwork_filter' not in st.session_state:
                    st.session_state['teamwork_filter'] = 'Month'
                    
                col_f1, col_f2, col_f3, _ = st.columns([1.5, 1.5, 1.5, 5])
                
                if col_f1.button("Year", type="primary" if st.session_state['teamwork_filter'] == 'Year' else "secondary", use_container_width=True):
                    st.session_state['teamwork_filter'] = 'Year'
                    st.rerun()
                if col_f2.button("Month", type="primary" if st.session_state['teamwork_filter'] == 'Month' else "secondary", use_container_width=True):
                    st.session_state['teamwork_filter'] = 'Month'
                    st.rerun()
                if col_f3.button("Week", type="primary" if st.session_state['teamwork_filter'] == 'Week' else "secondary", use_container_width=True):
                    st.session_state['teamwork_filter'] = 'Week'
                    st.rerun()
                
                np.random.seed(hash(selected_doc_eval + st.session_state['teamwork_filter']) % (2**32 - 1))
                
                if st.session_state['teamwork_filter'] == 'Week':
                    dates = pd.date_range(start="2026-02-20", end="2026-02-26", freq='D')
                    num_dots = np.random.randint(3, 6)
                elif st.session_state['teamwork_filter'] == 'Month':
                    dates = pd.date_range(start="2026-02-01", end="2026-02-28", freq='2D')
                    num_dots = np.random.randint(8, 15)
                else: 
                    dates = pd.date_range(start="2025-03-01", end="2026-02-28", freq='10D')
                    num_dots = np.random.randint(20, 30)
                    
                selected_dates = np.random.choice(dates, num_dots, replace=False)
                categories = ["General Clinical", "Procedural", "Consultation"]
                
                df_contrib = pd.DataFrame({
                    "Date": selected_dates,
                    "Category": np.random.choice(categories, num_dots),
                    "Points": np.random.choice([5, 10, 15, 20], num_dots) 
                }).sort_values("Date")
                
                col_chart, col_breakdown = st.columns([3, 1], gap="large")
                
                with col_chart:
                    fig_scatter = px.scatter(
                        df_contrib, x="Date", y="Points", color="Category",
                        size="Points", hover_data=["Category"],
                        color_discrete_map={"General Clinical": "#2ecc71", "Procedural": "#f1c40f", "Consultation": "#3498db"}
                    )
                    fig_scatter.update_layout(
                        height=240, margin=dict(l=0, r=0, t=10, b=0),
                        yaxis_title="Points per Event", xaxis_title=None,
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                    )
                    fig_scatter.update_xaxes(showline=True, linewidth=2, linecolor='black')
                    st.plotly_chart(fig_scatter, use_container_width=True)
                    
                with col_breakdown:
                    st.markdown("<div style='font-weight:bold; margin-bottom:10px; text-align:center;'>Point Breakdown</div>", unsafe_allow_html=True)
                    
                    pts_gen = df_contrib[df_contrib['Category'] == 'General Clinical']['Points'].sum()
                    pts_proc = df_contrib[df_contrib['Category'] == 'Procedural']['Points'].sum()
                    pts_cons = df_contrib[df_contrib['Category'] == 'Consultation']['Points'].sum()
                    
                    st.markdown(f"""
                    <div style="background-color: #f8f9fa; border-left: 4px solid #2ecc71; padding: 8px; border-radius: 4px; margin-bottom: 8px; display:flex; justify-content:space-between;">
                        <span style="font-size:11px;">General</span> <b style="font-size:13px;">{pts_gen} <span style="font-size:9px; color:gray;">/ 100</span></b>
                    </div>
                    <div style="background-color: #f8f9fa; border-left: 4px solid #f1c40f; padding: 8px; border-radius: 4px; margin-bottom: 8px; display:flex; justify-content:space-between;">
                        <span style="font-size:11px;">Procedure</span> <b style="font-size:13px;">{pts_proc} <span style="font-size:9px; color:gray;">/ 100</span></b>
                    </div>
                    <div style="background-color: #f8f9fa; border-left: 4px solid #3498db; padding: 8px; border-radius: 4px; display:flex; justify-content:space-between;">
                        <span style="font-size:11px;">Consult</span> <b style="font-size:13px;">{pts_cons} <span style="font-size:9px; color:gray;">/ 100</span></b>
                    </div>
                    """, unsafe_allow_html=True)

        # CATEGORY 4: MENTORSHIP
        elif st.session_state['active_tab_inter'] == "Mentorship":
            st.subheader("4. Mentorship & Guidance")
            st.number_input("Number of Staff Mentored (Mentees)", min_value=0, value=2, key="mentor_num")
            st.slider("Mentorship Effectiveness Score", 0, 100, 90, key="mentor_slider")
            st.button("Save Mentorship Score", type="primary", key="save_mentor")