import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def show_operational_page():
    st.title("⚙️ Operational Evaluation")
    st.markdown("Monitoring system for productivity, clinic flow, and operational efficiency.")
    st.divider()

    # ==========================================================
    # PART 1: CSS INJECTION (KEMBALIKAN SAIZ BUTANG ASAL)
    # ==========================================================
    st.markdown("""
    <style>
        /* Card styling */
        .eval-card {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            margin-bottom: 10px;
            border: 1px solid #f0f2f6;
        }
        
        /* Metric values */
        .metric-value { font-size: 24px; font-weight: 700; color: #4318FF; line-height: 1.2; }
        .metric-label { font-size: 11px; color: #A3AED0; text-transform: uppercase; font-weight: bold;}
        .metric-trend-up { font-size: 11px; color: #05CD99; font-weight: bold; }
        .metric-trend-down { font-size: 11px; color: #FF4B4B; font-weight: bold; }

        /* Target top navigation buttons - SAIZ DIKEMBALIKAN KEPADA ASAL SUPAYA TIDAK BENYEK */
        div[data-testid="stHorizontalBlock"] div.stButton > button {
            height: 100px !important; /* Dikembalikan kepada 100px */
            width: 100% !important;
            border-radius: 15px !important; /* Bucu bulat seperti asal */
            background-color: white !important;
            border: 1px solid #f0f2f6 !important;
            box-shadow: 0px 2px 4px rgba(0,0,0,0.05) !important;
            transition: all 0.3s ease !important;
            font-weight: bold !important;
            font-size: 16px !important;
            padding: 10px !important;
        }
        
        /* Hover effect */
        div[data-testid="stHorizontalBlock"] div.stButton > button:hover {
            border-color: #39B8FF !important;
            color: #39B8FF !important;
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
        
        # Susun dropdown bersebelahan
        col_negeri, col_pegawai = st.columns(2)
        
        with col_negeri:
            senarai_negeri = ["Semua Negeri"] + list(mock_state_officers.keys())
            pilihan_negeri = st.selectbox("Pilih Negeri:", options=senarai_negeri, index=0, key="op_state_sel")
            
        with col_pegawai:
            if pilihan_negeri == "Semua Negeri":
                doc_list = []
                for officers in mock_state_officers.values():
                    doc_list.extend(officers)
            else:
                doc_list = mock_state_officers.get(pilihan_negeri, [])
                
            selected_doc_eval = st.selectbox("Select Medical Officer:", options=doc_list, key="op_doc_sel")
            
        if not selected_doc_eval:
            st.warning("Tiada pegawai dijumpai.")
            st.stop()

        st.write(f"Evaluation Session: **{selected_doc_eval}**")
        st.write("---")

        # ==========================================================
        # PART 2: BUTTON NAVIGATION LOGIC
        # ==========================================================
        if 'active_tab_ops' not in st.session_state:
            st.session_state['active_tab_ops'] = "Productivity"

        c1, c2 = st.columns(2)
        with c1:
            is_act = st.session_state['active_tab_ops'] == "Productivity"
            if st.button("🚀\nProductivity & Efficiency", key="btn_prod", type="primary" if is_act else "secondary", use_container_width=True):
                st.session_state['active_tab_ops'] = "Productivity"
                st.rerun()
        with c2:
            is_act = st.session_state['active_tab_ops'] == "Innovation"
            if st.button("💡\nInnovation & Problem Solving", key="btn_inno", type="primary" if is_act else "secondary", use_container_width=True):
                st.session_state['active_tab_ops'] = "Innovation"
                st.rerun()

        st.write("") # Sedikit ruang sebelum paparan kandungan

        # ==========================================================
        # PART 3: CONDITIONAL CONTENT
        # ==========================================================
        
        # ---------------------------------------------------------
        # TAB 1: PRODUCTIVITY & EFFICIENCY
        # ---------------------------------------------------------
        if st.session_state['active_tab_ops'] == "Productivity":
            st.subheader("1. Productivity & Efficiency Metrics")
            
            # Top Metrics Row
            st.markdown("<div class='eval-card'>", unsafe_allow_html=True)
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                st.markdown("<div class='metric-label'>Avg Patients/Day</div>", unsafe_allow_html=True)
                st.markdown("<div class='metric-value'>42</div>", unsafe_allow_html=True)
                st.markdown("<div class='metric-trend-up'>↑ +5 vs last month</div>", unsafe_allow_html=True)
            with col_m2:
                st.markdown("<div class='metric-label'>Avg Consult Time</div>", unsafe_allow_html=True)
                st.markdown("<div class='metric-value'>12 min</div>", unsafe_allow_html=True)
                st.markdown("<div class='metric-trend-up'>Optimal Range</div>", unsafe_allow_html=True)
            with col_m3:
                st.markdown("<div class='metric-label'>Punctuality Rate</div>", unsafe_allow_html=True)
                st.markdown("<div class='metric-value'>95%</div>", unsafe_allow_html=True)
                st.markdown("<div class='metric-trend-up'>Target: >90%</div>", unsafe_allow_html=True)
            with col_m4:
                st.markdown("<div class='metric-label'>Sick Leaves Taken</div>", unsafe_allow_html=True)
                st.markdown("<div class='metric-value'>2 Days</div>", unsafe_allow_html=True)
                st.markdown("<div class='metric-trend-down'>YTD 2026</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            # Chart & Assessment Row
            col_chart, col_assess = st.columns([1.5, 1])
            
            with col_chart:
                st.markdown("##### 📊 Patient Clearance Trend (Last 7 Days)")
                # Mock Data for area chart
                df_trend = pd.DataFrame({
                    "Date": pd.date_range(start="2026-02-20", periods=7).strftime("%d %b"),
                    "Patients Cleared": [38, 42, 45, 30, 48, 40, 50]
                })
                fig = px.area(df_trend, x="Date", y="Patients Cleared", markers=True, color_discrete_sequence=['#39B8FF'])
                fig.update_layout(height=280, margin=dict(l=0, r=0, t=10, b=0)) 
                st.plotly_chart(fig, use_container_width=True)

            with col_assess:
                st.markdown("##### 🎯 Supervisor Evaluation")
                st.slider("Time Management & Punctuality", 0, 100, 85, key="op_s1")
                st.slider("Patient Flow Handling (Clinic/Ward)", 0, 100, 80, key="op_s2")
                st.slider("Resource Utilization", 0, 100, 75, key="op_s3")
                st.write("")
                st.button("💾 Save Productivity Score", type="primary", use_container_width=True)

        # ---------------------------------------------------------
        # TAB 2: INNOVATION & PROBLEM SOLVING
        # ---------------------------------------------------------
        elif st.session_state['active_tab_ops'] == "Innovation":
            st.subheader("2. Innovation & Problem Solving")
            st.info("Evaluate the officer's ability to handle crises, propose system improvements, and execute operational tasks efficiently.")

            col_in1, col_in2 = st.columns([1, 1])

            with col_in1:
                st.markdown("<div class='eval-card'>", unsafe_allow_html=True)
                st.markdown("##### Continuous Quality Improvement (CQI)")
                st.write("Does the officer actively participate in or lead CQI / Lean Healthcare projects?")
                
                cqi_status = st.radio("Involvement Status:", ["Lead/Initiator", "Active Member", "Passive Participant", "None"], index=1)
                
                if cqi_status in ["Lead/Initiator", "Active Member"]:
                    st.text_input("Project Name / Description:")
                    st.slider("Impact of the Project", 0, 100, 85, key="cqi_impact")
                
                st.write("---")
                st.markdown("##### Crisis Management")
                st.slider("Ability to handle Code Blue / Emergency Ward Flow", 0, 100, 88, key="crisis_1")
                st.slider("Conflict resolution (with patients or staff)", 0, 100, 80, key="crisis_2")
                st.markdown("</div>", unsafe_allow_html=True)

            with col_in2:
                st.markdown("<div class='eval-card'>", unsafe_allow_html=True)
                st.markdown("##### Radar Assessment")
                
                # Mock Data for Operational Radar
                df_op_radar = pd.DataFrame(dict(
                    r=[85, 90, 75, 88, 85],
                    theta=['Crisis Response', 'Team Delegation', 'Proactive Thinking', 'System Compliance', 'Crisis Response']
                ))
                fig_op_radar = px.line_polar(df_op_radar, r='r', theta='theta', line_close=True)
                fig_op_radar.update_traces(fill='toself', fillcolor='rgba(57, 184, 255, 0.4)', line_color='#39B8FF')
                fig_op_radar.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    showlegend=False,
                    height=280, 
                    margin=dict(t=20, b=20, l=20, r=20)
                )
                st.plotly_chart(fig_op_radar, use_container_width=True)
                
                st.text_area("HOD Comments on Innovation:")
                st.button("💾 Save Innovation Score", type="primary", use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)