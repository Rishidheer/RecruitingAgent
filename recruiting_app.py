import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
from io import StringIO

# Set page config
st.set_page_config(page_title="Recruiting AI Agent", page_icon="🤖", layout="wide")

# Initialize session state
if 'processed' not in st.session_state:
    st.session_state.processed = False
    st.session_state.top_candidates = None

# AI Agent greeting
st.title("🤖 Recruiting AI Agent")
st.markdown("""
Hello Recruiter! I'm your AI recruiting assistant. Upload a job description and resumes, 
and I'll identify the top candidates for you.
""")

# Sidebar controls
with st.sidebar:
    st.header("Controls")
    top_n = st.slider("Number of top candidates to show", 3, 20, 10)
    show_details = st.checkbox("Show detailed analysis", True)
    st.markdown("---")
    st.markdown("**Instructions:**")
    st.markdown("1. Upload job description (text file)")
    st.markdown("2. Upload resumes (CSV or folder of text files)")
    st.markdown("3. Click 'Process Candidates'")

# File upload section
col1, col2 = st.columns(2)

with col1:
    st.subheader("Upload Job Description")
    jd_file = st.file_uploader("Choose a text file", type=['txt'], key="jd")

with col2:
    st.subheader("Upload Resumes")
    resume_option = st.radio("Resume input format:", 
                           ('CSV File', 'Folder of Text Files'))
    
    if resume_option == 'CSV File':
        resume_file = st.file_uploader("Choose a CSV file", type=['csv'])
    else:
        resume_folder = st.file_uploader("Choose text files", 
                                       type=['txt'], 
                                       accept_multiple_files=True)

# Processing function
def process_candidates(job_desc, resumes_text):
    try:
        all_texts = [job_desc] + resumes_text
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(all_texts)
        scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]
        return scores
    except Exception as e:
        st.error(f"Error in processing: {e}")
        return None

# Process button
if st.button("🚀 Process Candidates", use_container_width=True):
    if jd_file and (resume_file or resume_folder):
        try:
            # Read job description
            job_desc = jd_file.read().decode('utf-8')
            
            # Read resumes based on selected option
            if resume_option == 'CSV File':
                resumes_df = pd.read_csv(resume_file)
                text_column = 'Resume_str'  # Adjust if your CSV uses different column name
                resumes_text = resumes_df[text_column].fillna('').astype(str).tolist()
                candidates_df = resumes_df.copy()
            else:
                resumes_text = []
                for file in resume_folder:
                    resumes_text.append(file.read().decode('utf-8'))
                candidates_df = pd.DataFrame({
                    'Filename': [f.name for f in resume_folder],
                    'Resume': resumes_text
                })
            
            # Score candidates
            with st.spinner("Analyzing candidates..."):
                scores = process_candidates(job_desc, resumes_text)
                
                if scores is not None:
                    candidates_df['Score'] = scores
                    candidates_df['Score'] = (candidates_df['Score'] * 100).round(2)  # Convert to percentage
                    st.session_state.top_candidates = candidates_df.sort_values('Score', ascending=False)
                    st.session_state.processed = True
                    st.success("Analysis complete!")
                    
        except Exception as e:
            st.error(f"Error processing files: {e}")
    else:
        st.warning("Please upload both job description and resumes")

# Display results
if st.session_state.processed and st.session_state.top_candidates is not None:
    st.divider()
    st.subheader(f"🔝 Top {top_n} Candidates")
    
    top_df = st.session_state.top_candidates.head(top_n)
    
    # Display summary table
    st.dataframe(
        top_df[['Score'] + (['Category'] if 'Category' in top_df.columns else []) + 
              (['ID'] if 'ID' in top_df.columns else ['Filename'])],
        use_container_width=True,
        height=(top_n + 1) * 35 + 3
    )
    
    # Detailed view
    if show_details:
        for idx, (_, row) in enumerate(top_df.iterrows(), 1):
            with st.expander(f"#{idx}: Score {row['Score']}%"):
                if 'ID' in row:
                    st.markdown(f"**ID:** {row['ID']}")
                if 'Category' in row:
                    st.markdown(f"**Category:** {row['Category']}")
                if 'Filename' in row:
                    st.markdown(f"**File:** {row['Filename']}")
                
                st.divider()
                st.markdown("**Relevant Experience:**")
                st.text(row.get('Resume_str', row.get('Resume', ''))[:2000] + "...")
    
    # Download button
    csv = top_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Top Candidates",
        data=csv,
        file_name='top_candidates.csv',
        mime='text/csv',
        use_container_width=True
    )
    
    # AI Analysis
    st.divider()
    st.subheader("🧠 AI Analysis")
    
    if 'Category' in top_df.columns:
        category_dist = top_df['Category'].value_counts()
        st.markdown("**Top Skills Distribution:**")
        st.bar_chart(category_dist)
    
    avg_score = top_df['Score'].mean()
    if avg_score > 70:
        st.success(f"🌟 Strong candidate pool! Average match score: {avg_score:.1f}%")
    elif avg_score > 40:
        st.warning(f"⚠️ Moderate candidate pool. Average match score: {avg_score:.1f}%")
    else:
        st.error(f"❌ Weak matches. Consider revising job description. Average score: {avg_score:.1f}%")
    
    st.markdown("**Suggested Next Steps:**")
    st.markdown("- Contact top 3 candidates for interviews")
    st.markdown("- Review job description if scores are consistently low")
    st.markdown("- Consider additional screening for specific skills")

# AI Agent footer
st.divider()
st.caption("🤖 AI Recruiting Agent v1.0 | Ready to help you find the best talent! Made By Rishabh Dheer ❤️")