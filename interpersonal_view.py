import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import plotly.express as px

def show_interpersonal_page():
    st.title("🤝 Evaluation Module: Interpersonal Excellence")
    st.markdown("Evaluation page for patient experience (PSQ-18), teamwork, and leadership.")
    st.divider()

    # --- 1. SPECIAL CSS (Interpersonal Green Theme) ---
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
        # Retrieve doctor list from session
        if st.session_state.get("doctor_list") is not None:
            # Check if dataframe or list
            if isinstance(st.session_state["doctor_list"], pd.DataFrame):
                 # Try to get the correct column name dynamically
                 try:
                     doc_list = st.session_state["doctor_list"]["Officer Name"].tolist()
                 except KeyError:
                      # Fallback if the column is named differently
                      col_name = st.session_state["doctor_list"].columns[0]
                      doc_list = st.session_state["doctor_list"][col_name].tolist()
            else:
                 doc_list = st.session_state["doctor_list"]
        else:
            doc_list = ["Please select a clinic on the main Dashboard first"]
            
        selected_doc_eval = st.selectbox("Select Medical Officer:", doc_list, key="inter_select")
        st.write(f"Evaluation Session: **{selected_doc_eval}**")
        st.write("---")

        # --- VISUALIZATION: RADAR CHART (Stays on top) ---
        if selected_doc_eval != "Please select a clinic on the main Dashboard first":
            st.subheader("📊 Soft Skills Profile")
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
                height=350,
                margin=dict(t=30, b=30, l=30, r=30)
            )
            st.plotly_chart(fig, use_container_width=True)

        st.divider()

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
            if selected_doc_eval != "Please select a clinic on the main Dashboard first":
                st.markdown("**Emotional Intelligence Component Breakdown**")
                np.random.seed(hash(selected_doc_eval) % (2**32 - 1))
                ei_data = {
                    "Component": ["Self-Awareness", "Emotional Regulation", "Social Skills", "Empathy"],
                    "Score": [np.random.randint(75, 95) for _ in range(4)]
                }
                df_ei = pd.DataFrame(ei_data)
                fig_ei = px.bar(df_ei, x="Score", y="Component", orientation='h', 
                                color="Score", color_continuous_scale='Greens', text_auto=True)
                fig_ei.update_layout(height=280, margin=dict(t=10, b=10, l=0, r=0), 
                                     showlegend=False, coloraxis_showscale=False)
                st.plotly_chart(fig_ei, use_container_width=True)

            st.divider()
            st.slider("Self-Awareness & Emotional Management", 0, 100, 85, key="ei_slider1")
            st.slider("Empathy towards Colleagues", 0, 100, 80, key="ei_slider2")
            st.button("Save EI Score", type="primary", key="save_ei")

        # CATEGORY 3: TEAMWORK
        elif st.session_state['active_tab_inter'] == "Teamwork":
            st.subheader("3. Teamwork & Collaboration")
            
            if selected_doc_eval != "Please select a clinic on the main Dashboard first":
                # --- SUB-MENU UNTUK ADMIN VIEW ---
                teamwork_view = st.radio(
                    "Select View:", 
                    ["360° Feedback Analysis", "Teamwork Contribution Log"], 
                    horizontal=True,
                    label_visibility="collapsed"
                )
                st.write("---")
                
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
                    fig_team.update_layout(title="Average Colleague Evaluation Score", height=300, margin=dict(t=50, b=20, l=0, r=0))
                    fig_team.update_yaxes(range=[0, 100])
                    st.plotly_chart(fig_team, use_container_width=True)

                    st.divider()
                    st.radio("Level of Team Contribution", ["Passive", "Active", "Highly Proactive", "Team Leader"], key="team_radio")
                    st.multiselect("Key Collaboration Qualities", ["Reliable", "Good Communicator", "Conflict Resolver", "Flexible"], default=["Reliable"], key="team_multi")
                    st.button("Save Teamwork Score", type="primary", key="save_team")

                # ==========================================
                # PAPARAN 2: CONTRIBUTION LOG (BERDASARKAN LAKARAN)
                # ==========================================
                elif teamwork_view == "Teamwork Contribution Log":
                    st.markdown("**Teamwork Contribution Log**")
                    st.caption("Visualizing support and assistance provided to colleagues over time.")
                    
                    # 1. INIT STATE UNTUK FILTER MASA
                    if 'teamwork_filter' not in st.session_state:
                        st.session_state['teamwork_filter'] = 'Month'
                        
                    # 2. BUTANG FILTER INTERAKTIF
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
                    
                    # 3. JANA DATA BERDASARKAN FILTER (Titik akan berubah bila klik)
                    # Guna hash pada kombinasi nama + filter supaya logik simulasi berbeza untuk setiap tempoh
                    np.random.seed(hash(selected_doc_eval + st.session_state['teamwork_filter']) % (2**32 - 1))
                    
                    if st.session_state['teamwork_filter'] == 'Week':
                        dates = pd.date_range(start="2026-02-20", end="2026-02-26", freq='D')
                        num_dots = np.random.randint(3, 6) # Sedikit titik dalam seminggu
                    elif st.session_state['teamwork_filter'] == 'Month':
                        dates = pd.date_range(start="2026-02-01", end="2026-02-28", freq='2D')
                        num_dots = np.random.randint(8, 15) # Sederhana dalam sebulan
                    else: # Year
                        dates = pd.date_range(start="2025-03-01", end="2026-02-28", freq='10D')
                        num_dots = np.random.randint(20, 30) # Banyak titik dalam setahun
                        
                    selected_dates = np.random.choice(dates, num_dots, replace=False)
                    categories = ["General Clinical", "Procedural", "Consultation"]
                    
                    # Kita naikkan saiz mata (Points) supaya bila dicampur jadi besar (contoh: 10, 15, 20)
                    df_contrib = pd.DataFrame({
                        "Date": selected_dates,
                        "Category": np.random.choice(categories, num_dots),
                        "Points": np.random.choice([5, 10, 15, 20], num_dots) 
                    })
                    df_contrib = df_contrib.sort_values("Date")
                    
                    # Susun Atur: Carta di kiri, Kotak Pecahan di kanan
                    col_chart, col_breakdown = st.columns([3, 1], gap="large")
                    
                    with col_chart:
                        # Bina Scatter Plot
                        fig_scatter = px.scatter(
                            df_contrib, 
                            x="Date", 
                            y="Points", 
                            color="Category",
                            size="Points", # Titik lebih besar untuk skor tinggi
                            hover_data=["Category"],
                            color_discrete_map={
                                "General Clinical": "#2ecc71", 
                                "Procedural": "#f1c40f",       
                                "Consultation": "#3498db"      
                            }
                        )
                        fig_scatter.update_layout(
                            height=300, 
                            margin=dict(l=0, r=0, t=30, b=0),
                            yaxis_title="Points per Event",
                            xaxis_title=f"Timeline ({st.session_state['teamwork_filter']})",
                            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                        )
                        fig_scatter.update_xaxes(showline=True, linewidth=2, linecolor='black')
                        st.plotly_chart(fig_scatter, use_container_width=True)
                        
                    with col_breakdown:
                        # Kotak Pecahan Point skala besar (Contoh: XX / 100)
                        st.markdown("<div style='font-weight:bold; margin-bottom:10px; text-align:center;'>Point Breakdown</div>", unsafe_allow_html=True)
                        
                        # Kiraan dari simulasi
                        pts_gen = df_contrib[df_contrib['Category'] == 'General Clinical']['Points'].sum()
                        pts_proc = df_contrib[df_contrib['Category'] == 'Procedural']['Points'].sum()
                        pts_cons = df_contrib[df_contrib['Category'] == 'Consultation']['Points'].sum()
                        
                        # Kad Metrik dengan sasaran / 100
                        st.markdown(f"""
                        <div style="background-color: #f8f9fa; border-left: 5px solid #2ecc71; padding: 10px; border-radius: 5px; margin-bottom: 10px; display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:13px;">General Support</span> <b style="font-size:16px;">{pts_gen} <span style="font-size:10px; color:gray;">/ 100</span></b>
                        </div>
                        <div style="background-color: #f8f9fa; border-left: 5px solid #f1c40f; padding: 10px; border-radius: 5px; margin-bottom: 10px; display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:13px;">Procedural Asst.</span> <b style="font-size:16px;">{pts_proc} <span style="font-size:10px; color:gray;">/ 100</span></b>
                        </div>
                        <div style="background-color: #f8f9fa; border-left: 5px solid #3498db; padding: 10px; border-radius: 5px; display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:13px;">Consultation</span> <b style="font-size:16px;">{pts_cons} <span style="font-size:10px; color:gray;">/ 100</span></b>
                        </div>
                        <div style="margin-top:15px; text-align:center;">
                            <p style="font-size:11px; color:#888;">Target KPI points set per category</p>
                        </div>
                        """, unsafe_allow_html=True)


        # CATEGORY 4: MENTORSHIP
        elif st.session_state['active_tab_inter'] == "Mentorship":
            st.subheader("4. Mentorship & Guidance")
            st.number_input("Number of Staff Mentored (Mentees)", min_value=0, value=2, key="mentor_num")
            st.slider("Mentorship Effectiveness Score", 0, 100, 90, key="mentor_slider")
            st.button("Save Mentorship Score", type="primary", key="save_mentor")