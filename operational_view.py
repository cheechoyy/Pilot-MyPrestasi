import streamlit as st

def show_operational_page():
    st.title("⚙️ Evaluation Module: Operational Excellence")
    st.markdown("Monitoring page for medical officer productivity and innovation.")
    st.divider()

    # --- 1. SPECIAL CSS (Same as Clinical for consistency) ---
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

        /* Style for ACTIVE button */
        div[data-testid="stHorizontalBlock"] div.stButton > button[kind="primary"] {
            background-color: #f0f7ff !important;
            border: 2px solid #6c5ce7 !important; /* Purple color for Operational theme */
            color: #6c5ce7 !important;
            box-shadow: 0px 4px 10px rgba(108, 92, 231, 0.1) !important;
        }

        div[data-testid="stHorizontalBlock"] div.stButton > button:hover {
            border-color: #6c5ce7 !important;
            transform: translateY(-2px);
        }
    </style>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        # Retrieve doctor list from session
        if st.session_state.get("doctor_list") is not None:
            # Added a failsafe to match English column names
            try:
                doc_list = st.session_state["doctor_list"]["Officer Name"].tolist()
            except KeyError:
                col_name = st.session_state["doctor_list"].columns[0]
                doc_list = st.session_state["doctor_list"][col_name].tolist()
        else:
            doc_list = ["Please select a clinic on the main Dashboard first"]
            
        selected_doc_eval = st.selectbox("Select Medical Officer:", doc_list, key="op_select")
        st.write(f"Evaluation Session: **{selected_doc_eval}**")
        st.write("---")

        # --- 2. CARD NAVIGATION LOGIC (2 Categories) ---
        if 'active_tab_op' not in st.session_state:
            st.session_state['active_tab_op'] = "Productivity"

        # Using 2 columns to make buttons large and clear
        col1, col2 = st.columns(2)
        
        with col1:
            is_active = st.session_state['active_tab_op'] == "Productivity"
            if st.button("⏱️\nProductivity & Efficiency", key="btn_prod", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state['active_tab_op'] = "Productivity"
                st.rerun()
                
        with col2:
            is_active = st.session_state['active_tab_op'] == "Innovation"
            if st.button("💡\nInnovation & Problem Solving", key="btn_inov", type="primary" if is_active else "secondary", use_container_width=True):
                st.session_state['active_tab_op'] = "Innovation"
                st.rerun()

        st.write("") # Empty space

        # --- 3. CONDITIONAL CONTENT ---
        
        # CATEGORY 1: PRODUCTIVITY
        if st.session_state['active_tab_op'] == "Productivity":
            st.subheader("1. Productivity & Efficiency")
            
            # Objective data input
            st.number_input("Average Daily Cases Treated", min_value=0, value=45, step=1)
            
            # --- NEW IDEA: Efficiency Metrics ---
            with st.container(border=True):
                st.markdown("#### ⏱️ Efficiency Metrics")
                c1, c2 = st.columns(2)
                with c1:
                    st.slider("Appropriateness of Resource Utilization", 0, 100, 85, help="Efficiency in medication/lab usage")
                with c2:
                    st.slider("Case Turnaround Time (TAT)", 0, 100, 90, help="Compliance with standard treatment time")
                
                st.button("Save Productivity Score", type="primary", key="save_prod_new")
            
        # CATEGORY 2: INNOVATION
        elif st.session_state['active_tab_op'] == "Innovation":
            st.subheader("2. Innovation & Problem Solving")
            
            # --- NEW IDEA: Innovative Achievements ---
            with st.container(border=True):
                st.markdown("#### 💡 Innovative Achievements")
                st.radio("Innovation Project Involvement (QA/QI/KIK)", ["None", "Member", "Project Leader"], horizontal=True)
                st.multiselect("Documentation Contribution", ["Update SOP", "New Protocol", "New Flowchart"], default=[])
                st.text_area("Brief Description of Innovation", placeholder="Example: Accelerated ED registration process by 10% via QR system.")
                
                st.button("Save Innovation Score", type="primary", key="save_inov_new")
                
        # --- OVERALL SCORE SUMMARY (WEIGHTAGE) ---
        st.write("---")
        st.subheader("🎯 Overall Operational Results")
        
        # Simulation calculation (Pull from session_state set in Admin)
        w_p = st.session_state.get("w_prod", 70) / 100
        w_i = st.session_state.get("w_inov", 30) / 100
        
        # Example score (In actual system, pull from database)
        final_score = (85 * w_p) + (60 * w_i)
        
        col_res1, col_res2 = st.columns([2, 1])
        with col_res1:
            st.info(f"**Final Operational Score: {final_score:.1f}%**")
            st.caption(f"Formula: (Productivity × {w_p}) + (Innovation × {w_i})")
        with col_res2:
            if final_score >= 80:
                st.success("✨ Outstanding")
            else:
                st.warning("📈 Needs Improvement")