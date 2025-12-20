import streamlit as st
import os
import plotly.express as px
import db
import utils


st.set_page_config(page_title="NLTK ATS Pro", layout="wide", page_icon="📊")
db.init_db()


ACCENT_COLOR = "#00AEEF" 
DARK_BG = "#1E222A"     
LIGHT_TEXT = "#F0F0F0"   

st.markdown(f"""
    <style>
    /* Global Styles */
    .stApp {{ background-color: {DARK_BG}; color: {LIGHT_TEXT}; font-family: 'Helvetica Neue', sans-serif; }}
    h1, h2, h3, h4, .st-emotion-cache-1jmveez, .st-emotion-cache-10trblm {{ color: {ACCENT_COLOR}; }}

    /* Metric Cards */
    .stMetric {{ background-color: #28303C; border: 2px solid #4B4F5E; border-radius: 10px; padding: 15px; box-shadow: 0 4px 8px rgba(0, 174, 239, 0.2); }}
    
    /* Buttons/Transitions */
    .stButton>button {{
        background-color: {ACCENT_COLOR}; color: {DARK_BG}; font-weight: bold;
        transition: all 0.3s ease-in-out; 
    }}
    .stButton>button:hover {{
        transform: scale(1.02); 
        box-shadow: 0 0 10px {ACCENT_COLOR};
    }}
    
    </style>
""", unsafe_allow_html=True)

st.title("💼 NLTK ATS Web Analyzer")


with st.sidebar:
    st.header("Controls")
    nav = st.radio("Go to:", ["Analyze Resume", "View Database History"])


if nav == "Analyze Resume":
    st.subheader("New Application Assessment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        jd_text = st.text_area("1. Paste Job Description", height=250, placeholder="Enter the job requirements here...")
    
    with col2:
        uploaded_file = st.file_uploader("2. Upload Resume (PDF)", type="pdf")
        candidate_name = st.text_input("3. Candidate Name", placeholder="e.g., Jane Doe")

    if st.button("Run Analysis", use_container_width=True):
        if uploaded_file and jd_text and candidate_name:
            with st.spinner("Processing document..."):
                
                if not os.path.exists("uploads"): os.makedirs("uploads")
                file_path = "uploads/temp_resume.pdf"
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                
                resume_text = utils.extract_text(file_path)
                skills = utils.extract_skills_knowledge_base(resume_text) 
                score = utils.calculate_score(resume_text, jd_text) 
                
               
                db.save_candidate(candidate_name, score, skills)
                os.remove(file_path)
                
                
                st.success("Analysis Complete!")
                
               
                if score >= 75:
                    result_color = "#00AEEF"
                    feedback = "EXCELLENT MATCH: Highly recommended for interview."
                elif score >= 50:
                    result_color = "#FFA500" 
                    feedback = "GOOD MATCH: Needs further human review."
                else:
                    result_color = "#FF4B4B" 
                    feedback = "LOW MATCH: Resume does not align well with JD."

                m1, m2, m3 = st.columns(3)
                with m1:
                    
                    st.markdown(f'<div class="stMetric" style="border-left: 5px solid {result_color};">'
                                f'<p style="font-size: 16px; color: {LIGHT_TEXT};">Match Score</p>'
                                f'<h3 style="color: {result_color};">{score}%</h3></div>', unsafe_allow_html=True)
                with m2:
                    st.metric("Skills Found", len(skills))
                with m3:
                    st.metric("Recommendation", "Shortlist" if score > 75 else "Review")
                
                st.markdown(f"**Status:** <span style='color: {result_color};'>{feedback}</span>", unsafe_allow_html=True)

                
                c1, c2 = st.columns(2)
                with c1:
                    fig = px.pie(values=[score, 100-score], names=["Match", "Gap"], 
                                 hole=0.6, title="Fit Analysis", color_discrete_sequence=['#00AEEF', '#4B4F5E'])
                    st.plotly_chart(fig, use_container_width=True)
                
                with c2:
                    st.markdown("#### 🔑 Keywords Detected:")
                    if skills:
                        st.code(", ".join(skills).upper(), language=None)
                    else:
                        st.warning("No core keywords found.")
        else:
            st.error("Please fill in all 3 required fields.")


elif nav == "View Database History":
    st.header("Candidate Repository")
    
    df = db.get_all_candidates()
    
    if not df.empty:
        # Metrics
        kpi1, kpi2 = st.columns(2)
        kpi1.metric("Total Candidates", len(df))
        kpi2.metric("Average Score", f"{df['score'].mean():.1f}%")
        
        st.dataframe(df, use_container_width=True)
        
        
        fig = px.bar(df, x='name', y='score', color='score', title="Candidate Ranking",
                     color_continuous_scale='plasma')
        st.plotly_chart(fig, use_container_width=True)
    else:

        st.info("Database is empty. Analyze your first resume!")
