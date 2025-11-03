import streamlit as st
import pandas as pd
from pathlib import Path
import os
from datetime import datetime
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from parsers.pdf_parser import extract_text_from_pdf
from parsers.docx_parser import extract_text_from_docx
from extractors import extract_with_langchain, extract_with_openai_vision
from storage.excel_handler import save_to_excel, load_from_excel
from utils.validators import validate_resume_data
from utils.helpers import generate_resume_id, clean_text

load_dotenv()
# Page configuration
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .upload-section {
        border: 2px dashed #1f77b4;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f0f8ff;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #145a8d;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = pd.DataFrame()
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False

# Try to hydrate from persisted Excel on startup
try:
    if st.session_state.processed_data.empty:
        persisted = load_from_excel()
        if persisted is not None and not persisted.empty:
            # Ensure types and fill
            if 'total_experience_years' in persisted.columns:
                persisted['total_experience_years'] = pd.to_numeric(persisted['total_experience_years'], errors='coerce').fillna(0)
            st.session_state.processed_data = persisted.fillna('Not Found')
except Exception as _e:
    pass

def process_single_resume(file, file_content):
    """Process a single resume file and extract all information via LangChain"""
    import traceback
    
    try:
        file_extension = Path(file.name).suffix.lower()
        
        if file_extension == '.pdf':
            # Prefer vision-based direct PDF parsing
            ai_data = extract_with_openai_vision(file_content, file_type='pdf')
            if not ai_data:
                # Fallback to text-based pipeline if vision unavailable/quota/rate-limit
                text = extract_text_from_pdf(file_content)
                if not text or len(text.strip()) < 50:
                    st.warning(f"⚠️ Could not extract sufficient text from {file.name}")
                    return None
                cleaned_text = clean_text(text)
                ai_data = extract_with_langchain(cleaned_text)
            else:
                print("[SUCCESS] Vision extraction succeeded!")
                
        elif file_extension in ['.docx', '.doc']:
            # Prefer vision-based direct DOCX parsing (same as PDF)
            ai_data = extract_with_openai_vision(file_content, file_type='docx')
            if not ai_data:
                # Fallback to text-based pipeline if vision unavailable/quota/rate-limit
                text = extract_text_from_docx(file_content)
                if not text:
                    st.error(f"❌ Failed to extract any text from {file.name}. File might be corrupted or password-protected.")
                    print(f"[ERROR] No text extracted from DOCX file")
                    return None
                elif len(text.strip()) < 50:
                    st.warning(f"⚠️ Could not extract sufficient text from {file.name}")
                    print(f"[ERROR] Insufficient text extracted: {len(text.strip())} chars")
                    print(f"[DEBUG] Extracted text preview (first 500 chars):\n{text[:500]}")
                    return None
                                
                cleaned_text = clean_text(text)
                ai_data = extract_with_langchain(cleaned_text)
            else:
                print("[SUCCESS] Vision extraction succeeded!")
        else:
            print(f"[ERROR] Unsupported file extension: {file_extension}")
            st.error(f"❌ Unsupported file format: {file_extension}")
            return None
            
        if not ai_data:
            st.warning(f"⚠️ AI could not parse {file.name}")
            print(f"[ERROR] AI extraction returned empty result")
            return None

        base = {
            'resume_id': generate_resume_id(),
            'file_name': file.name,
            'upload_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        resume_data = validate_resume_data({**base, **ai_data})
        return resume_data
        
    except Exception as e:
        error_msg = f"Error processing {file.name}: {str(e)}"
        st.error(f"❌ {error_msg}")
        return None

def main():
    st.markdown('<h1 class="main-header">🤖 AI-Powered Resume Screener</h1>', unsafe_allow_html=True)
    st.markdown("---")
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/resume.png", width=80)
        st.title("Navigation")
        page = st.radio("Go to", ["📤 Upload Resumes", "📊 View Data", "📈 Analytics", "ℹ️ About"])
        st.markdown("---")
        st.markdown("### 📋 Quick Stats")
        if not st.session_state.processed_data.empty:
            st.metric("Total Resumes", len(st.session_state.processed_data))
            exp_series = pd.to_numeric(st.session_state.processed_data.get('total_experience_years', pd.Series([])), errors='coerce').fillna(0)
            st.metric("Avg Experience", f"{exp_series.mean():.1f} yrs")
        else:
            st.info("No data yet. Upload resumes to see stats!")
    if page == "📤 Upload Resumes":
        show_upload_page()
    elif page == "📊 View Data":
        show_data_page()
    elif page == "📈 Analytics":
        show_analytics_page()
    else:
        show_about_page()

def show_upload_page():
    st.header("📤 Upload Resume Files")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_files = st.file_uploader(
            "Drag and drop resume files here",
            type=['pdf', 'docx', 'doc'],
            accept_multiple_files=True,
            help="Upload PDF or DOCX files. Multiple files supported."
        )
    
    with col2:
        st.info("📌 **Supported Formats**\n\n- PDF (.pdf)\n- Word (.docx, .doc)\n\n✨ **Multiple uploads supported**")
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) selected")
    
    if uploaded_files:
        if st.button("🚀 Process Resumes", type="primary"):
            process_resumes(uploaded_files)
    
    # Show recent uploads
    if not st.session_state.processed_data.empty:
        st.markdown("---")
        st.subheader("📋 Recently Processed")
        recent = st.session_state.processed_data.tail(5)[['file_name', 'name', 'email', 'total_experience_years', 'upload_date']]
        st.dataframe(recent, use_container_width=True, hide_index=True)

def process_resumes(uploaded_files):
    """Process all uploaded resume files"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    processed_resumes = []
    
    for idx, file in enumerate(uploaded_files):
        status_text.text(f"Processing {file.name}... ({idx+1}/{len(uploaded_files)})")
        
        # Read file content
        file_content = file.read()
        file.seek(0)  # Reset file pointer
        
        # Process resume
        resume_data = process_single_resume(file, file_content)
        
        if resume_data:
            processed_resumes.append(resume_data)
        
        # Update progress
        progress_bar.progress((idx + 1) / len(uploaded_files))
    
    if processed_resumes:
        # Convert to DataFrame
        new_data = pd.DataFrame(processed_resumes)
        
        # Append to existing data
        if st.session_state.processed_data.empty:
            st.session_state.processed_data = new_data
        else:
            st.session_state.processed_data = pd.concat([st.session_state.processed_data, new_data], ignore_index=True)
        
        # Save to Excel (overwrite with current in-memory data)
        output_path = save_to_excel(st.session_state.processed_data, merge=False)
        
        status_text.empty()
        progress_bar.empty()
        
        st.success(f"✅ Successfully processed {len(processed_resumes)} resume(s)!")
        st.balloons()
        
        # Download button
        with open(output_path, 'rb') as f:
            st.download_button(
                label="📥 Download Excel Report",
                data=f,
                file_name=f"resumes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    else:
        status_text.empty()
        progress_bar.empty()
        st.error("❌ No resumes could be processed. Please check file formats.")

def show_data_page():
    st.header("📊 Resume Database")
    
    # Re-hydrate if needed
    if st.session_state.processed_data.empty:
        persisted = load_from_excel()
        if persisted is not None and not persisted.empty:
            if 'total_experience_years' in persisted.columns:
                persisted['total_experience_years'] = pd.to_numeric(persisted['total_experience_years'], errors='coerce').fillna(0)
            st.session_state.processed_data = persisted.fillna('Not Found')
    
    if st.session_state.processed_data.empty:
        st.info("📭 No data available. Please upload resumes first.")
        return
    
    df = st.session_state.processed_data.copy()
    
    # Filters
    st.subheader("🔍 Filters")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        search_query = st.text_input("🔎 Search by name/email", "")
    
    with col2:
        min_exp = st.number_input("Min Experience (years)", min_value=0, max_value=50, value=0)
    
    with col3:
        max_exp = st.number_input("Max Experience (years)", min_value=0, max_value=50, value=50)
    
    with col4:
        degree_filter = st.multiselect("🎓 Degree", options=df['highest_degree'].unique().tolist())
    
    # Apply filters
    filtered_df = df.copy()
    
    if search_query:
        filtered_df = filtered_df[
            filtered_df['name'].str.contains(search_query, case=False, na=False) |
            filtered_df['email'].str.contains(search_query, case=False, na=False)
        ]
    
    filtered_df = filtered_df[
        (filtered_df['total_experience_years'] >= min_exp) &
        (filtered_df['total_experience_years'] <= max_exp)
    ]
    
    if degree_filter:
        filtered_df = filtered_df[filtered_df['highest_degree'].isin(degree_filter)]
    
    # Display data + selection controls
    st.markdown("---")
    st.subheader(f"📋 Results: {len(filtered_df)} resumes")

    # Ensure selection support
    if 'resume_id' not in filtered_df.columns:
        st.error("resume_id column missing; cannot perform row selection/deletion.")
        return

    select_all = st.checkbox("Select all in current view", value=False)

    display_df = filtered_df.copy()
    # Avoid Arrow type issues
    if 'graduation_year' in display_df.columns:
        display_df['graduation_year'] = display_df['graduation_year'].astype(str)

    display_df.insert(0, 'selected', False)
    if select_all:
        display_df['selected'] = True

    # Column selector
    display_columns = st.multiselect(
        "Select columns to display",
        options=display_df.columns.tolist(),
        default=display_df.columns.tolist()
    )

    if display_columns:
        # Use data_editor to enable selection
        edited = st.data_editor(
            display_df[display_columns],
            column_config={
                'selected': st.column_config.CheckboxColumn('Select', default=False)
            },
            disabled=[c for c in display_columns if c != 'selected'],
            use_container_width=True,
            hide_index=True,
            height=400
        )
        
        selected_ids = edited.loc[edited.get('selected', False) == True, 'resume_id'].tolist() if 'resume_id' in edited.columns else []

        col_del, _ = st.columns([1,3])
        with col_del:
            if st.button(f"🗑️ Delete selected ({len(selected_ids)})", type="secondary", disabled=len(selected_ids) == 0):
                # Open confirm modal
                st.session_state['__pending_delete_ids__'] = selected_ids
                st.session_state['__show_confirm_modal__'] = True

    # Confirmation UI (fallback for Streamlit versions without st.modal)
    if st.session_state.get('__show_confirm_modal__'):
        ids = st.session_state.get('__pending_delete_ids__', []) or []
        st.warning(f"This will permanently delete {len(ids)} row(s) from the dataset and Excel.")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Confirm", type="primary", key="confirm_delete_btn"):
                before = len(st.session_state.processed_data)
                st.session_state.processed_data = st.session_state.processed_data[
                    ~st.session_state.processed_data['resume_id'].isin(ids)
                ].reset_index(drop=True)
                save_to_excel(st.session_state.processed_data, merge=False)
                st.session_state['__show_confirm_modal__'] = False
                st.session_state['__pending_delete_ids__'] = []
                st.success(f"Deleted {before - len(st.session_state.processed_data)} row(s).")
                st.rerun()
        with c2:
            if st.button("✖️ Cancel", key="cancel_delete_btn"):
                st.session_state['__show_confirm_modal__'] = False
                st.session_state['__pending_delete_ids__'] = []
    
    # Export options
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Export Filtered Data"):
            if display_columns:
                export_path = save_to_excel(filtered_df, out_path=Path('output')/ 'filtered_resumes.xlsx', selected_columns=display_columns, merge=False)
            else:
                export_path = save_to_excel(filtered_df, out_path=Path('output')/ 'filtered_resumes.xlsx', merge=False)
            with open(export_path, 'rb') as f:
                st.download_button(
                    label="Download Filtered Excel",
                    data=f,
                    file_name=f"filtered_resumes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

def show_analytics_page():
    st.header("📈 Analytics Dashboard")
    
    if st.session_state.processed_data.empty:
        st.info("📭 No data available. Please upload resumes first.")
        return
    
    df = st.session_state.processed_data
    
    # Metrics
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Resumes", len(df))
    
    with col2:
        avg_exp = df['total_experience_years'].mean()
        st.metric("Avg Experience", f"{avg_exp:.1f} years")
    
    col3, col4 = st.columns(2)
    with col3:
        most_common_degree = df['highest_degree'].mode()[0] if not df['highest_degree'].mode().empty else "N/A"
        st.metric("Most Common Degree", most_common_degree)
    
    with col4:
        complete_profiles = df[df['email'] != 'Not Found'].shape[0]
        st.metric("Complete Profiles", f"{complete_profiles}/{len(df)}")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎓 Education Distribution")
        degree_counts = df['highest_degree'].value_counts()
        st.bar_chart(degree_counts)
    
    with col2:
        st.subheader("💼 Experience Distribution")
        exp_bins = pd.cut(df['total_experience_years'], bins=[0, 2, 5, 10, 20, 50], labels=['0-2', '2-5', '5-10', '10-20', '20+'])
        exp_counts = exp_bins.value_counts().sort_index()
        st.bar_chart(exp_counts)
    
    # Top skills
    st.markdown("---")
    st.subheader("🔥 Top Technical Skills")
    all_skills = []
    for skills in df['technical_skills']:
        if isinstance(skills, str) and skills != 'Not Found':
            all_skills.extend([s.strip() for s in skills.split(',')])
    
    if all_skills:
        skill_counts = pd.Series(all_skills).value_counts().head(10)
        st.bar_chart(skill_counts)
    else:
        st.info("No skills data available")

def show_about_page():
    st.header("ℹ️ About Resume Screener")
    
    st.markdown("""
    ### 🎯 Purpose
    This AI-powered Resume Screener helps HR professionals and recruiters to:
    - **Automate** resume parsing and data extraction
    - **Save time** by processing multiple resumes simultaneously
    - **Organize** candidate information in structured format
    - **Filter & Search** candidates based on various criteria
    - **Export** data to Excel for further analysis
    
    ### 🤖 AI Features
    - **Natural Language Processing** (NLP) for text extraction
    - **Named Entity Recognition** (NER) for identifying names, organizations
    - **Pattern Matching** for emails, phones, dates
    - **Intelligent Skills Extraction** using predefined skill database
    - **Experience Calculation** from date ranges
    
    ### 📊 Extracted Information
    - Personal: Name, Email, Phone, Location
    - Education: Degree, College, Graduation Year, CGPA
    - Experience: Total years, Companies, Designations
    - Skills: Technical, Soft Skills, Tools, Languages
    - Additional: Certifications, LinkedIn, GitHub
    
    ### 🛠️ Tech Stack
    - **Frontend**: Streamlit
    - **NLP**: spaCy, NLTK
    - **PDF Parsing**: PyPDF2, pdfplumber
    - **Data Processing**: Pandas
    - **Storage**: Excel (openpyxl)
    
    ### 📝 How to Use
    1. Go to **Upload Resumes** page
    2. Upload PDF/DOCX files (single or multiple)
    3. Click **Process Resumes**
    4. View extracted data in **View Data** page
    5. Analyze insights in **Analytics** page
    6. Export to Excel anytime
    
    ### 👨‍💻 Developer
    Built with ❤️ using Python & Streamlit
    
    ### 📄 License
    MIT License - Free to use and modify
    """)
    
    st.markdown("---")
    st.info("💡 **Tip**: For best results, use well-formatted resumes with clear sections.")

if __name__ == "__main__":
    # Create necessary directories
    Path("uploads").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)
    
    main()