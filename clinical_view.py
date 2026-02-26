import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ADD module_type PARAMETER
def show_clinical_page(module_type="CTS"):
    st.title(f"⚕️ Evaluation Module: Clinical Excellence ({module_type})")
    st.markdown("Dedicated page for clinical evaluation of medical officers.")
    st.divider()

    # ==========================================================
    # PART 1: CSS INJECTION
    # ==========================================================
    st.markdown("""
    <style>
        /* Target only buttons inside this specific card navigation */
        div[data-testid="stHorizontalBlock"] div.stButton > button {
            height: 100px !important;
            width: 100% !important;
            border-radius: 15px !important;
            background-color: white !important;
            border: 1px solid #f0f2f6 !important;
            box-shadow: 0px 2px 4px rgba(0,0,0,0.05) !important;
            transition: all 0.3s ease !important;
            padding: 10px !important;
            font-weight: bold !important;
        }

        /* Hover effect */
        div[data-testid="stHorizontalBlock"] div.stButton > button:hover {
            border-color: #FF4B4B !important;
            color: #FF4B4B !important;
            transform: translateY(-2px);
        }
    </style>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        # Retrieve doctor list from session
        if st.session_state.get("doctor_list") is not None:
            # Check if data is dataframe or list
            if isinstance(st.session_state["doctor_list"], pd.DataFrame):
                # Using the English column name as defined in main/admin view
                doc_list = st.session_state["doctor_list"]["Officer Name"].tolist()
            else:
                doc_list = st.session_state["doctor_list"]
        else:
            doc_list = ["Please select a clinic on the main Dashboard first"]
            
        selected_doc_eval = st.selectbox("Select Medical Officer:", doc_list, key=f"doc_sel_{module_type}")
        st.write(f"Evaluation Session: **{selected_doc_eval}**")
        st.write("---")

        # ==========================================================
        # PART 2: BUTTON NAVIGATION LOGIC
        # ==========================================================
        if 'active_tab_clinical' not in st.session_state:
            st.session_state['active_tab_clinical'] = "Skills"

        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            is_active = st.session_state['active_tab_clinical'] == "Skills"
            if st.button("🛠️\nSkills", key=f"btn_sk_{module_type}", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state['active_tab_clinical'] = "Skills"
                st.rerun()
                
        with col2:
            is_active = st.session_state['active_tab_clinical'] == "Knowledge"
            if st.button("🧠\nKnowledge", key=f"btn_kn_{module_type}", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state['active_tab_clinical'] = "Knowledge"
                st.rerun()
                
        with col3:
            is_active = st.session_state['active_tab_clinical'] == "Documentation"
            if st.button("📝\nDoc.", key=f"btn_dc_{module_type}", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state['active_tab_clinical'] = "Documentation"
                st.rerun()
                
        with col4:
            is_active = st.session_state['active_tab_clinical'] == "Policies"
            if st.button("📜\nPolicies", key=f"btn_pl_{module_type}", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state['active_tab_clinical'] = "Policies"
                st.rerun()

        st.write("") # Empty space

        # ==========================================================
        # PART 3: CONDITIONAL CONTENT
        # ==========================================================
        
        # --- TAB 1: SKILLS ---
        if st.session_state['active_tab_clinical'] == "Skills":
            st.subheader("1. Clinical Skills")
            
            if selected_doc_eval != "Please select a clinic on the main Dashboard first":
                with st.container(border=True):
                    
                    # CTS CHART LOGIC (CONTINUOUS CUSUM - LIMA LAD)
                    if module_type == "CTS":
                        st.markdown("**CUSUM Performance Analysis: LIMA-LAD Procedure (Continuous)**")
                        st.caption("Monitoring the learning curve based on the last 20 LIMA-LAD cases.")
                        
                        np.random.seed(hash(selected_doc_eval) % (2**32 - 1))
                        procedures = np.arange(1, 21)
                        learning_curve_scores = 88 - 15 * np.exp(-procedures / 6)
                        noise = np.random.normal(0, 3, 20)
                        actual_scores = learning_curve_scores + noise
                        target_score = 80
                        cusum_values = np.cumsum(actual_scores - target_score)
                        df_cusum = pd.DataFrame({"Procedure": procedures, "CUSUM Value": cusum_values})
                        
                        fig = px.line(df_cusum, x="Procedure", y="CUSUM Value", markers=True,
                                      labels={"Procedure": "Number of LIMA-LAD Procedures", "CUSUM Value": "CUSUM Variation"})
                        fig.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Baseline KPI (80)")
                        fig.update_traces(line_color="#00a0dc")
                        fig.update_layout(margin=dict(t=20, l=0, r=0, b=0), height=320)
                        st.plotly_chart(fig, use_container_width=True)

                    # FMS CHART LOGIC (BINARY CUSUM)
                    elif module_type == "FMS":
                        st.markdown("**CUSUM Performance Analysis: Primary Clinical (Binary)**")
                        st.caption("Monitoring success/complication rate for the last 20 procedure cases (1=Success, 0=Complication).")
                        
                        np.random.seed(hash(selected_doc_eval) % (2**32 - 1))
                        procedures = np.arange(1, 21)
                        
                        # Generate Binary data: 85% success(1), 15% fail(0)
                        outcomes = np.random.choice([1, 0], size=20, p=[0.85, 0.15])
                        
                        # Binary CUSUM Calculation
                        cusum_values = np.zeros(20)
                        current_cusum = 0
                        for i, outcome in enumerate(outcomes):
                            if outcome == 0: # Complication/Fail (+1 penalty)
                                current_cusum += 1
                            else: # Success (-0.2 reward)
                                current_cusum = max(0, current_cusum - 0.2) 
                            cusum_values[i] = current_cusum

                        df_cusum = pd.DataFrame({
                            "Procedure": procedures,
                            "CUSUM Value": cusum_values,
                            "Status": ["Complication (0)" if x == 0 else "Success (1)" for x in outcomes]
                        })

                        fig = px.line(df_cusum, x="Procedure", y="CUSUM Value", markers=True,
                                      labels={"Procedure": "Number of Procedures/Cases", "CUSUM Value": "CUSUM Score (Must be < 3)"},
                                      hover_data=["Status"])
                        
                        # Binary Warning Lines
                        fig.add_hline(y=3, line_dash="dash", line_color="orange", annotation_text="Warning Limit")
                        fig.add_hline(y=4, line_dash="solid", line_color="red", annotation_text="Action Limit (Stop)")
                        
                        fig.update_traces(line_color="#865CFF")
                        fig.update_layout(margin=dict(t=20, l=0, r=0, b=0), height=320, yaxis_range=[-0.5, 5])
                        st.plotly_chart(fig, use_container_width=True)
            
            st.write("") 
            st.slider("New Procedure Observation Score", 0, 100, 85, key=f"skill_slider_{module_type}")
            st.text_area("Skill Comments", key=f"skill_kom_{module_type}")
            st.button("Save Skills Score", type="primary", key=f"btn_save_sk_{module_type}")

        # --- TAB 2: KNOWLEDGE ---
        elif st.session_state['active_tab_clinical'] == "Knowledge":
            st.subheader("2. Knowledge & Capacity (CME/CPD)")
            
            cpd_score = 0
            cpd_target = 40

            # 1. FILTER SECTION
            with st.container(border=True):
                col_f1, col_f2, col_f3 = st.columns(3)
                with col_f1: st.selectbox("📅 Year", ["2026", "2025"], key=f"f_year_{module_type}")
                with col_f2: st.selectbox("🗓️ Month", ["All", "January", "February"], key=f"f_month_{module_type}")
                with col_f3: st.text_input("🔍 Subject/Topic", placeholder="Search topic...", key=f"f_sub_{module_type}")

            # 2. TWO GAUGE CHARTS 
            if selected_doc_eval != "Please select a clinic on the main Dashboard first":
                np.random.seed(hash(selected_doc_eval) % (2**32 - 1))
                cpd_score = np.random.randint(50, 95) 
                
                # Scale status logic
                if cpd_score >= 85:
                    status_text = "🌟 Outstanding"
                    status_color = "#2ecc71"
                elif cpd_score >= 75:
                    status_text = "👍 Good"
                    status_color = "#9acd32"
                elif cpd_score >= 65:
                    status_text = "✅ Competent"
                    status_color = "#ffa500"
                else:
                    status_text = "⚠️ Improvement Required"
                    status_color = "#ff4b4b"

                col_gauge1, col_gauge2 = st.columns(2)
                with col_gauge1:
                    fig_ind = go.Figure(go.Indicator(
                        mode = "gauge+number", value = cpd_score,
                        title = {'text': "Your Clinical Score (%)", 'font': {'size': 16}},
                        gauge = {
                            'axis': {'range': [0, 100]},
                            'bar': {'color': "#2c3e50", 'thickness': 0.15}, 
                            'steps': [
                                {'range': [0, 65], 'color': "#ff4b4b"},    
                                {'range': [65, 75], 'color': "#ffa500"},   
                                {'range': [75, 85], 'color': "#9acd32"},   
                                {'range': [85, 100], 'color': "#2ecc71"}   
                            ]
                        }
                    ))
                    fig_ind.update_layout(height=260, margin=dict(t=40, b=10, l=30, r=30))
                    st.plotly_chart(fig_ind, use_container_width=True)
                    st.markdown(f"<center>Current Level: <b style='color:{status_color}; font-size:18px;'>{status_text}</b></center>", unsafe_allow_html=True)

                with col_gauge2:
                    score_peer = 72 
                    fig_peer = go.Figure(go.Indicator(
                        mode = "gauge+number", value = score_peer,
                        title = {'text': "Peer Average (%)", 'font': {'size': 16}},
                        gauge = {
                            'axis': {'range': [0, 100]}, 
                            'bar': {'color': "#2c3e50", 'thickness': 0.15},
                            'steps': [
                                {'range': [0, 65], 'color': "rgba(255, 75, 75, 0.3)"},
                                {'range': [65, 75], 'color': "rgba(255, 165, 0, 0.3)"},
                                {'range': [75, 85], 'color': "rgba(154, 205, 50, 0.3)"},
                                {'range': [85, 100], 'color': "rgba(46, 204, 113, 0.3)"}
                            ]
                        }
                    ))
                    fig_peer.update_layout(height=260, margin=dict(t=40, b=10, l=30, r=30))
                    st.plotly_chart(fig_peer, use_container_width=True)
                    st.markdown("<center>Status: <b style='color:#ffa500; font-size:18px;'>✅ Competent</b></center>", unsafe_allow_html=True)

                st.divider()

                # 3. HISTORY LOG TABLE
                st.markdown("#### 📜 Activity Log & Learning Marks")
                history_df = pd.DataFrame({
                    "Date": ["20/02/2026", "12/02/2026", "05/01/2026"],
                    "Category": ["CME", "Workshop", "Online Quiz"],
                    "Topic": ["Trauma Management", "LIMA-LAD Technique", "Medical Ethics"],
                    "Marks": [85, 92, 78]
                })
                st.dataframe(history_df, use_container_width=True, hide_index=True)

            # 4. INPUT FORM
            st.write("")
            with st.expander("➕ Add Record / Save New Score"):
                st.info("Choose entry method: 1) Manual Entry or 2) Scan CME QR")
                c1, c2 = st.columns(2)
                with c1: st.date_input("Activity Date", key=f"in_date_{module_type}")
                with c2: st.selectbox("Category", ["CME", "Workshop", "Exam"], key=f"in_cat_{module_type}")
                st.text_input("Learning Topic", key=f"in_topic_{module_type}")
                markah_input = st.slider("Marks Obtained", 0, 100, 80, key=f"know_slider_new_{module_type}")
                
                if st.button("Save Knowledge Record", type="primary", key=f"btn_save_k_{module_type}"):
                    st.success("Record successfully saved!")
                    if cpd_score >= cpd_target:
                        st.success("✅ Annual CPD Point Target Achieved!")
                    else:
                        st.warning(f"⚠️ Needs {cpd_target - cpd_score} more points.")

            st.divider()
            st.slider("Update Test Score / New CPD Points", 0, 100, 90, key=f"know_slider_{module_type}")
            st.button("Save Knowledge Score", type="primary", key=f"btn_save_k_bottom_{module_type}")

        # --- TAB 3: DOCUMENTATION ---
        elif st.session_state['active_tab_clinical'] == "Documentation":
            st.subheader("3. Clinical Documentation Monitoring (HOD View)")
            st.write("Real-time update for patient notes entry timeliness.")
            st.write("")
            
            # --- OVERALL METRICS ---
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Entries", "1,247", "+12 Today")
            c2.metric("On-time (%)", "85%", "-2% Last Mth", delta_color="inverse") 
            c3.metric("Avg Completion Time", "1h 10m", "Less than 1 hr from target")
            c4.metric("Dept Ranking", "1 / 25", "Unchanged")
            
            st.markdown("---")
            
            # --- TIMELINESS CHART ---
            st.markdown("#### Timeliness Patient Entry Review")
            st.write("**Target:** < 4 Hours (Metric) | ≥ 90% (Score)")
            
            # Simulated data for horizontal bar chart
            df_timeliness = pd.DataFrame({
                "Category": ["On-time", "Delayed", "Overdue"],
                "Percentage": [85, 10, 5],
                "Y_Axis": ["Overall Records", "Overall Records", "Overall Records"] 
            })
            
            # Building Horizontal Stacked Bar Chart
            fig_time = px.bar(
                df_timeliness, 
                y="Y_Axis",  
                x="Percentage", 
                color="Category", 
                orientation='h',
                color_discrete_map={"On-time": "#2ecc71", "Delayed": "#f1c40f", "Overdue": "#e74c3c"},
                text="Percentage"
            )
            
            fig_time.update_traces(texttemplate='%{text}%', textposition='inside', insidetextanchor='middle')
            fig_time.update_layout(
                barmode='stack', 
                yaxis_title=None, 
                xaxis_title="Percentage (%)",
                height=180, 
                margin=dict(l=0, r=0, t=10, b=0),
                showlegend=True
            )
            st.plotly_chart(fig_time, use_container_width=True)
            
            st.markdown("---")
            
            # --- HOD ATTENTION LIST ---
            st.markdown("#### ⚠️ HOD Attention List: Delayed Entry")
            
            # Simulated overdue table data
            df_delayed = pd.DataFrame({
                "Doctor": ["Dr. Ahmad", "Dr. Siti Fazura", "Dr. Chong Wei"],
                "Count": [3, 2, 1],
                "Delay (Avg)": ["5.5 Hours", "4.5 Hours", "8.0 Hours"],
                "Reason": ["Shortage of staff in ward", "Red Zone emergency case", "System login delayed"]
            })
            
            st.dataframe(df_delayed, use_container_width=True, hide_index=True)
            
            # Action Button
            c_btn1, c_btn2 = st.columns([1, 3])
            with c_btn1:
                if st.button("🔔 Send 'Reminder'", type="primary", use_container_width=True, key=f"btn_remind_{module_type}"):
                    st.toast("Automated reminder sent to the relevant staff's email!", icon="✅")

        # --- TAB 4: POLICIES ---
        elif st.session_state['active_tab_clinical'] == "Policies":
            st.subheader("4. Policy & Protocol Compliance")
            st.slider("SOP Compliance Rate (%)", 0, 100, 95, key=f"pol_slider_{module_type}")
            st.button("Save Policy Score", type="primary", key=f"btn_save_pol_{module_type}")