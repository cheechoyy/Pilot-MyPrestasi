import streamlit as st
import pandas as pd
from datetime import date
import plotly.express as px

# --- IMPORT MODULE FUNCTIONS ---
# Keeping operational and interpersonal for now
from operational_view import show_operational_page
from interpersonal_view import show_interpersonal_page

# =====================================================================
# --- STAFF SPECIFIC CLINICAL FORM FUNCTION ---
# =====================================================================
def show_staff_clinical_update():
    st.markdown("<h2 style='color:#2b3674;'>🩺 Update Data: Clinical Excellence</h2>", unsafe_allow_html=True)
    st.info("Please enter your procedure records, CPD activities, and documentation audit. This data will be sent to the HOD for verification.")

    # 1. Static Identity (Auto-detect logged-in user)
    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #2ecc71; margin-bottom: 20px;'>
            <strong>Officer Name:</strong> Dr. Portal (Current Login)<br>
            <strong>Department:</strong> Outpatient
        </div>
    """, unsafe_allow_html=True)

    # 2. Tabs for different entry categories
    tab1, tab2, tab3, tab4 = st.tabs(["🛠️ Procedure Log (Skills)", "📚 CPD Claim (Knowledge)", "📝 Documentation Audit", "📜 Policy Declaration"])

    # --- TAB 1: SKILLS (PROCEDURE LOG) ---
    with tab1:
        st.markdown("### Add Clinical Procedure Log")
        with st.form("form_skills", clear_on_submit=True):
            c1, c2 = st.columns(2)
            tarikh = c1.date_input("Procedure Date")
            jenis = c2.selectbox("Procedure Type", ["Intubation", "Central Line Insertion", "Chest Tube", "Appendectomy", "Others"])
            
            c3, c4 = st.columns(2)
            komplikasi = c3.radio("Were there any complications?", ["No", "Yes"], horizontal=True)
            peranan = c4.selectbox("Your Role", ["Primary Surgeon / Operator", "First Assistant", "Observer"])
            
            nota = st.text_area("Additional Notes / Learning Points (Optional)")
            
            submitted = st.form_submit_button("Submit Procedure Log", type="primary", use_container_width=True)
            if submitted:
                st.success("✅ Procedure log successfully submitted and pending HOD verification.")

    # --- TAB 2: KNOWLEDGE (CPD) ---
    with tab2:
        st.markdown("### CPD / CME Points Claim")
        with st.form("form_cpd", clear_on_submit=True):
            tajuk = st.text_input("Program / Course Title")
            
            # Full list based on standard CPD log form
            senarai_kategori_cpd = [
                "A1 - SCIENTIFIC MEETINGS/CONGRESS",
                "A2 - WORKSHOPS/COURSES/SKILL COURSES INCLUDING ATLS/CCRISP/CPR...",
                "B1A - HOSPITAL/DEPARTMENT CME",
                "B1B - SMALL GROUP DISCUSSION/CASE CONFERENCE",
                "B1C - PARTICIPATION IN INTER-DEPARTMENT CLINICAL MEETING / EPI REVIEW",
                "B1D - JOURNAL CLUB MEETING",
                "B1E - FORMAL GRAND WARD ROUND",
                "B1F - EXTERNAL CME LECTURE/ TOPIC SEMINAR",
                "B2A - MORBIDITY AND MORTALITY REVIEWS",
                "B2B - AUDIT MEETINGS",
                "B2C - PARTICIPATION IN ACCREDITATION EXERCISE",
                "B2D - PARTICIPATION IN QUALITY ASSURANCE (QA) ACTIVITIES",
                "C1 - SCHOLARLY ACTIVITIES/TRAINING/PRESENTATION",
                "C2 - SCHOLARLY ACTIVITIES/RESEARCH/PUBLICATION",
                "DA - ONLINE CME MODULES (PER MODULE)",
                "DB - SELF-STUDY (RELEVANT BOOKS, PUBLICATIONS, PODCASTS ETC.)",
                "DC - EXTERNAL LECTURE/ TOPIC SEMINAR (PER HOUR)",
                "E - PROFESSIONAL DEVELOPMENT"
            ]
            kategori = st.selectbox("CPD Category", senarai_kategori_cpd)
            
            c1, c2, c3 = st.columns(3)
            mula = c1.date_input("Start Date")
            tamat = c2.date_input("End Date")
            mata = c3.number_input("CPD Points Claimed", min_value=0, step=1)
            
            sijil = st.file_uploader("Upload Certificate/Proof (PDF/JPG)", type=['pdf', 'jpg', 'png'])
            
            sub_cpd = st.form_submit_button("Submit CPD Claim", type="primary", use_container_width=True)
            if sub_cpd:
                if tajuk == "":
                    st.error("Please enter the program title.")
                else:
                    st.success(f"✅ Claim of {mata} CPD points for '{tajuk}' has been submitted to the HPU system.")

    # --- TAB 3: DOCUMENTATION (UPDATED WITH TIMELINESS METRIC) ---
    with tab3:
        st.markdown("### 📝 Clinical Documentation Form (Timeliness)")
        st.write("Please record the status of your patient notes entry here for Department monitoring.")
        
        with st.form("doc_entry_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                patient_id = st.text_input("Patient ID / RN", placeholder="e.g.: RN123456")
                doc_type = st.selectbox("Documentation Type", ["Admission Note", "Progress Note", "Discharge Summary"])
                
            with col2:
                # Staff selects their status
                status = st.radio("Entry Status (Target: < 4 hours)", 
                                  ["On-time", "Delayed", "Overdue"], 
                                  horizontal=True)
                completion_time = st.number_input("Estimated Completion Time (Hours)", min_value=0.5, step=0.5, value=1.0)
                
            # Reason field mandatory if delayed
            reason = st.text_area("Reason for Delay (Mandatory if 'Delayed' or 'Overdue')", 
                                  placeholder="State the reason for delay (e.g.: Involved with emergency case in Red Zone)...")
            
            submitted = st.form_submit_button("Save Documentation Record", type="primary", use_container_width=True)
            
            if submitted:
                if not patient_id:
                    st.error("Please enter Patient ID / RN.")
                elif status in ["Delayed", "Overdue"] and not reason:
                    st.warning("⚠️ Please state the reason for delay for HOD audit purposes.")
                else:
                    st.success(f"✅ Documentation record for patient {patient_id} successfully submitted to the database.")

    # --- TAB 4: POLICIES & PROTOCOLS ---
    with tab4:
        st.markdown("### SOP Declaration & Compliance")
        st.info("Please read and confirm your compliance with the latest facility policies. This confirmation will be recorded as proof of compliance.")
        
        with st.container(border=True):
            p1 = st.checkbox("I have read and understood the **Infection Control Guidelines 2026**.")
            p2 = st.checkbox("I have updated my annual **BLS/ALS Certificate** and attached a copy to the Training Unit.")
            p3 = st.checkbox("I acknowledge the latest **Patient Confidentiality Policy (PDPA)** of the facility.")
            
        if st.button("Confirm Declaration", type="primary", use_container_width=True):
            if p1 and p2 and p3:
                st.success("✅ Your compliance declaration has been recorded in the database.")
            else:
                st.error("Please tick all boxes to confirm your declaration.")

# =====================================================================
# --- STAFF SPECIFIC OPERATIONAL FORM FUNCTION ---
# =====================================================================
def show_staff_operational_update():
    st.markdown("<h2 style='color:#2b3674;'>⚙️ Update Data: Operational Excellence</h2>", unsafe_allow_html=True)
    st.info("Please enter your daily productivity records and innovation reports.")

    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #39B8FF; margin-bottom: 20px;'>
            <strong>Officer Name:</strong> Dr. Portal (Current Login)<br>
            <strong>Department:</strong> Outpatient
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["⏱️ Productivity & Efficiency", "💡 Innovation & Problem Solving"])

    with tab1:
        st.markdown("### Productivity & Efficiency Log")
        with st.form("form_ops_prod", clear_on_submit=True):
            tarikh_kerja = st.date_input("Review Date")
            c1, c2 = st.columns(2)
            pesakit_dilihat = c1.number_input("Total Patients Seen Today", min_value=0, step=1)
            discaj_dibuat = c2.number_input("Total Discharges Managed", min_value=0, step=1)
            masa_rata = st.number_input("Average Consultation Time (Minutes)", min_value=0, step=1)
            
            if st.form_submit_button("Submit Productivity Log", type="primary", use_container_width=True):
                st.success("✅ Productivity data successfully recorded.")

    with tab2:
        st.markdown("### Innovation & Problem Solving Proposal")
        with st.form("form_ops_innov", clear_on_submit=True):
            isu = st.text_input("Operational Issue/Problem Identified")
            solusi = st.text_area("Proposed Solution / Innovation Implemented")
            
            if st.form_submit_button("Submit Innovation Proposal", type="primary", use_container_width=True):
                if isu == "":
                    st.error("Please enter the issue/problem.")
                else:
                    st.success("✅ Your innovation idea has been submitted to the system for evaluation.")

# =====================================================================
# --- STAFF SPECIFIC INTERPERSONAL FORM FUNCTION ---
# =====================================================================
def show_staff_interpersonal_update():
    st.markdown("<h2 style='color:#2b3674;'>🤝 Update Data: Interpersonal Excellence</h2>", unsafe_allow_html=True)
    st.info("Please record patient feedback, emotional management, teamwork, and mentorship sessions.")

    st.markdown("""
        <div style='background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #05CD99; margin-bottom: 20px;'>
            <strong>Officer Name:</strong> Dr. Portal (Current Login)<br>
            <strong>Department:</strong> Outpatient
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["😊 Patient Experience", "🧠 Emotional Intel.", "👥 Teamwork", "🎓 Mentorship"])

    with tab1:
        st.markdown("### Patient Feedback")
        with st.form("form_int_px", clear_on_submit=True):
            c1, c2 = st.columns(2)
            pujian = c1.number_input("Number of Compliments/Appreciations Received", min_value=0, step=1)
            aduan = c2.number_input("Number of Complaints/Reprimands Received", min_value=0, step=1)
            catatan = st.text_area("Summary of Patient Feedback / Action Taken")
            
            if st.form_submit_button("Save Patient Experience Record", type="primary", use_container_width=True):
                st.success("✅ Patient experience record updated.")
                
    with tab2:
        st.markdown("### Emotional Intelligence (Self-Reflection)")
        with st.form("form_int_ei", clear_on_submit=True):
            refleksi = st.text_area("Self-Reflection on Stress & Emotion Management")
            tindakan = st.text_input("Improvement Steps (e.g.: Counseling Session, Recreation)")
            
            if st.form_submit_button("Save Emotional Intel Record", type="primary", use_container_width=True):
                st.success("✅ Emotional intelligence reflection log successfully recorded.")

    with tab3:
        st.markdown("### Teamwork & Collaboration")
        
        # --- SUB-MENU UNTUK 2 VARIASI TEAMWORK ---
        teamwork_mode = st.radio(
            "Pilih Jenis Rekod:", 
            ["MDT & 360° Feedback", "Teamwork Contribution Points"], 
            horizontal=True,
            label_visibility="collapsed"
        )
        
        st.write("---")
        
        # ==========================================
        # VARIASI 1: BORANG ASAL (MDT)
        # ==========================================
        if teamwork_mode == "MDT & 360° Feedback":
            st.markdown("#### MDT Meeting & Collaboration Record")
            with st.form("form_int_team", clear_on_submit=True):
                projek = st.text_input("Activity Name / Meeting Case (MDT)")
                peranan = st.text_input("Your Role in the Team")
                jabatan_terlibat = st.multiselect("Departments Involved", ["Physician", "Surgeon", "Pharmacy", "Dietetics", "Physiotherapy", "Others"])
                
                if st.form_submit_button("Save Teamwork Record", type="primary", use_container_width=True):
                    if not jabatan_terlibat:
                        st.error("Please select at least one department.")
                    else:
                        st.success("✅ Team collaboration data successfully recorded.")
                        
        # ==========================================
        # VARIASI 2: BORANG LAKARAN (CONTRIBUTION)
        # ==========================================
        elif teamwork_mode == "Teamwork Contribution Points":
            st.markdown("#### Teamwork Contribution & Support")
            st.write("Record your contributions or assistance provided to your colleagues.")
            
            with st.container(border=True):
                # Form to Add Contribution Point
                with st.form("form_int_team_add", clear_on_submit=True):
                    # 1. Select Colleague
                    rakan_sekerja = st.selectbox(
                        "Colleague Name (Dr. / Officer):", 
                        ["Dr. Ahmad Kamil", "Dr. Siti Nurhaliza", "Dr. Chong Wei", "Dr. Sarah", "Dr. Muthu"]
                    )
                    
                    st.write("")
                    st.markdown("**Select Support Provided:**")
                    
                    # 2. Support Categories (Based on your sketch)
                    col_s1, col_s2, col_s3 = st.columns(3)
                    
                    with col_s1:
                        gen_support = st.checkbox("General Clinical Support (+1 Point)")
                        if gen_support:
                            st.caption("E.g., ward round cover, answering calls.")
                    
                    with col_s2:
                        proc_support = st.checkbox("Procedural Assistance (+2 Points)")
                        if proc_support:
                            proc_name = st.text_input("Procedure Name:", placeholder="E.g., Intubation")
                    
                    with col_s3:
                        cons_support = st.checkbox("Consultation Support (+1 Point)")
                        if cons_support:
                            st.caption("E.g., discussing complex cases.")
                    
                    st.write("")
                    
                    # Submit Button
                    submitted_team = st.form_submit_button("➕ Add Point", type="primary", use_container_width=True)
                    
                    if submitted_team:
                        total_points = 0
                        if gen_support: total_points += 1
                        if proc_support: total_points += 2
                        if cons_support: total_points += 1
                        
                        if total_points == 0:
                            st.error("Please select at least one support category to add points.")
                        elif proc_support and not proc_name:
                            st.error("Please state the Procedure Name for Procedural Assistance.")
                        else:
                            st.success(f"✅ Successfully added {total_points} contribution point(s) for assisting {rakan_sekerja}.")
                            
            # Display Current Summary (Optional based on your sketch)
            st.write("")
            with st.expander("📊 My Contribution Summary (This Month)"):
                sum_df = pd.DataFrame({
                    "Support Category": ["General Clinical", "Procedural", "Consultation"],
                    "Points Earned": [4, 6, 2]
                })
                st.dataframe(sum_df, use_container_width=True, hide_index=True)

    with tab4:
        st.markdown("### Mentorship Session")
        with st.form("form_int_mentor", clear_on_submit=True):
            peranan_m = st.radio("Your Role:", ["As Mentor (Teaching)", "As Mentee (Learning)"], horizontal=True)
            nama_rakan = st.text_input("Colleague's Name (Mentor/Mentee)")
            tarikh_sesi = st.date_input("Session Date")
            topik = st.text_area("Discussion Topic / Skills Taught")
            
            if st.form_submit_button("Save Mentorship Log", type="primary", use_container_width=True):
                st.success("✅ Mentorship session log has been saved.")

# =====================================================================
# --- STAFF MAIN DASHBOARD ---
# =====================================================================
def show_staff_dashboard():
    if "staff_view" not in st.session_state:
        st.session_state["staff_view"] = "Dashboard"

    # --- STAFF SPECIFIC SIDEBAR ---
    with st.sidebar:
        st.markdown('<div class="user-avatar" style="background-color: #2ecc71; width: 60px; height: 60px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 30px; margin: 0 auto;">👨‍⚕️</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'><b>Dr. Portal</b><br>Medical Officer</p>", unsafe_allow_html=True)
        st.divider()
        
        st.write("**Main Menu**")
        if st.button("🏠 Dashboard", width="stretch", type="primary" if st.session_state["staff_view"] == "Dashboard" else "secondary"):
            st.session_state["staff_view"] = "Dashboard"
            st.rerun()
            
        if st.button("📊 My Performance", width="stretch", type="primary" if st.session_state["staff_view"] == "My Performance" else "secondary"):
            st.session_state["staff_view"] = "My Performance"
            st.rerun()
            
        st.write("")
        st.write("**Self Data Update**")
        if st.button("🩺 Clinical Excellence", width="stretch", type="primary" if st.session_state["staff_view"] == "Clinical" else "secondary"):
            st.session_state["staff_view"] = "Clinical"
            st.rerun()
            
        if st.button("⚙️ Operational", width="stretch", type="primary" if st.session_state["staff_view"] == "Operational" else "secondary"):
            st.session_state["staff_view"] = "Operational"
            st.rerun()
            
        if st.button("🤝 Interpersonal", width="stretch", type="primary" if st.session_state["staff_view"] == "Interpersonal" else "secondary"):
            st.session_state["staff_view"] = "Interpersonal"
            st.rerun()
        
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        
        if st.button("🚪 Logout", type="primary", width="stretch"): 
            st.session_state.clear()
            st.rerun()

    # --- CONTENT: MY PERFORMANCE ---
    if st.session_state["staff_view"] == "My Performance":
        st.title("📊 My Performance")
        st.markdown("<p style='color: #666; font-size: 1.1rem; margin-top: -15px;'>Summary of your evaluations and skills achievements.</p>", unsafe_allow_html=True)
        st.write("")

        col1, col2 = st.columns(2, gap="large")
        with col1:
            with st.container(border=True):
                st.subheader("⭐ Score Summary")
                st.metric(label="Clinical Excellence", value="85%", delta="Up 2%")
                st.metric(label="Operational Output", value="92%", delta="Up 5%")
                st.metric(label="Interpersonal Rating", value="High", delta="Unchanged")
        
        with col2:
            with st.container(border=True):
                st.subheader("📈 CUSUM Progress")
                st.info("Based on the last 20 procedures, your skills are consistent and stable.")
                st.progress(85, text="Procedure Observation Consistency (85%)")
                st.write("---")
                st.caption("Policy & Protocol Compliance")
                st.progress(95, text="Compliance Rate (95%)")

    # --- CONTENT: STAFF DATA ENTRY MODULES ---
    elif st.session_state["staff_view"] == "Clinical":
        show_staff_clinical_update()

    elif st.session_state["staff_view"] == "Operational":
        show_staff_operational_update()

    elif st.session_state["staff_view"] == "Interpersonal":
        show_staff_interpersonal_update()

    # --- CONTENT: STAFF MAIN DASHBOARD ---
    else:
        st.title("🩺 Medical Officer Dashboard")
        st.markdown("<p style='color: #666; font-size: 1.1rem; margin-top: -15px;'>Summary of Tasks, Schedule & Daily Analysis</p>", unsafe_allow_html=True)
        st.write("")

        col_cal, col_msg = st.columns([1, 1], gap="large")

        with col_cal:
            with st.container(border=True):
                st.markdown("#### 📅 Today's Schedule")
                st.caption(f"Current Date: {date.today().strftime('%d %B %Y')}")
                st.info("**10:30 - 11:30 AM** | 🛏️ Grand Rounds (General Ward)")
                st.success("**13:30 - 13:45 PM** | 🩺 New Patient Examination (Clinic)")
                st.warning("**14:00 - 14:30 PM** | 💉 LMP Procedure (Treatment Room)")

        with col_msg:
            with st.container(border=True):
                st.markdown("#### 💬 Messages & Notifications")
                st.caption("Your primary inbox")
                st.markdown("""
                **🏥 Main Hospital Lab** <span style='color:gray; font-size:0.8em; float:right;'>14:03</span><br>
                <small>Lab results for Patient A are ready for review.</small>
                <hr style="margin:0.5em 0;">
                **👩‍🔬 Dr. Siti Nurhaliza** <span style='color:gray; font-size:0.8em; float:right;'>13:27</span><br>
                <small>Patient X referral attached. Can we discuss briefly?</small>
                <hr style="margin:0.5em 0;">
                **👨‍⚕️ Dr. Ahmad Kamil** <span style='color:gray; font-size:0.8em; float:right;'>08:12</span><br>
                <small>RE: Shift swap this weekend. I agree.</small>
                """, unsafe_allow_html=True)

        st.write("")

        with st.container(border=True):
            st.markdown("#### 📈 Clinical Analysis")
            col_chart, col_metrics = st.columns([1.5, 1], gap="large")
            
            with col_chart:
                df_chart = pd.DataFrame({
                    "Department": ["ICU", "Med/Surg", "ED", "Pediatric Ward"],
                    "Completed Cases": [12, 10, 6, 8],
                    "Active Cases": [6, 4, 2, 3]
                })
                fig = px.bar(
                    df_chart, x="Department", y=["Completed Cases", "Active Cases"], 
                    barmode="stack", color_discrete_sequence=["#2ea78e", "#e0e0e0"] 
                )
                fig.update_layout(margin=dict(t=20, l=0, r=0, b=0), height=300, legend_title_text="Case Status")
                st.plotly_chart(fig, use_container_width=True)

            with col_metrics:
                m1, m2 = st.columns(2)
                with m1:
                    with st.container(border=True):
                        st.markdown("**Inpatient LOS**")
                        st.metric("ICU", "3.4 Days")
                        st.metric("Med/Surg", "2.2 Days")
                with m2:
                    with st.container(border=True):
                        st.markdown("**Risk & Quality**")
                        st.metric("Sepsis Score", "3")
                        st.metric("Readmissions", "4")
                
                m3, m4 = st.columns(2)
                with m3:
                    with st.container(border=True):
                        st.markdown("**Attendance**")
                        st.metric("Present", "94%")
                with m4:
                    with st.container(border=True):
                        st.markdown("**Procedures**")
                        st.metric("Completed", "18/20")
                        
    # --- GLOBAL FIXED FOOTER ---
    st.markdown("""
        <style>
        .custom-footer {
            position: fixed; left: 0; bottom: 0; width: 100%;
            background-color: #f8f9fa; color: #6c757d; text-align: center;
            padding: 12px 0; font-size: 0.9rem; font-weight: 500;
            border-top: 1px solid #e9ecef; z-index: 999;
        }
        .block-container { padding-bottom: 70px !important; }
        </style>
        <div class="custom-footer">
            Copyright © 2026 MyPrestasi HPU | National Health Facility
        </div>
    """, unsafe_allow_html=True)