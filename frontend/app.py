import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuration
st.set_page_config(
    page_title="Hate Speech Detection & Mitigation",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API Base URL
API_BASE_URL = "http://localhost:5000/api"

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
    .stat-box {
        padding: 1.5rem;
        border-radius: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .danger-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def fetch_statistics():
    """Fetch statistics from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/statistics")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error fetching statistics: {e}")
        return None

def analyze_text(text, user_id, username):
    """Analyze text via API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze",
            json={
                'text': text,
                'user_id': user_id,
                'username': username
            }
        )
        return response.json()
    except Exception as e:
        st.error(f"Error analyzing text: {e}")
        return None

def fetch_users():
    """Fetch all users"""
    try:
        response = requests.get(f"{API_BASE_URL}/users")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error fetching users: {e}")
        return None

def fetch_violations():
    """Fetch all violations"""
    try:
        response = requests.get(f"{API_BASE_URL}/violations")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error fetching violations: {e}")
        return None

# Sidebar Navigation
st.sidebar.title("🛡️ Navigation")
page = st.sidebar.radio(
    "Select Page",
    ["🏠 Dashboard", "🔍 Text Analyzer", "👥 User Management", "📊 Violations Log", "ℹ️ About"]
)

# Main Content
if page == "🏠 Dashboard":
    st.markdown('<p class="main-header">🛡️ Hate Speech Detection & Mitigation Dashboard</p>', unsafe_allow_html=True)
    
    # Fetch statistics
    stats_data = fetch_statistics()
    
    if stats_data and stats_data.get('success'):
        stats = stats_data['statistics']
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Users", stats['total_users'], delta=None)
        with col2:
            st.metric("Active Users", stats['active_users'], delta=None)
        with col3:
            st.metric("Suspended Users", stats['suspended_users'], delta=None)
        with col4:
            st.metric("Total Violations", stats['total_violations'], delta=None)
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Posts Analysis")
            
            # Pie chart for posts
            posts_data = {
                'Type': ['Clean Posts', 'Hate Speech Posts'],
                'Count': [stats['clean_posts'], stats['hate_speech_posts']]
            }
            fig1 = px.pie(
                posts_data,
                values='Count',
                names='Type',
                color_discrete_sequence=['#28a745', '#dc3545']
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Violations by Category")
            
            # Bar chart for violations by category
            if stats_data.get('violations_by_category'):
                cat_df = pd.DataFrame(
                    list(stats_data['violations_by_category'].items()),
                    columns=['Category', 'Count']
                )
                fig2 = px.bar(
                    cat_df,
                    x='Category',
                    y='Count',
                    color='Category'
                )
                st.plotly_chart(fig2, use_container_width=True)
        
        # Recent Violations
        st.markdown("---")
        st.subheader("🚨 Recent Violations")
        
        if stats_data.get('recent_violations'):
            violations_df = pd.DataFrame(stats_data['recent_violations'])
            st.dataframe(violations_df, use_container_width=True)
        else:
            st.info("No violations recorded yet.")
    else:
        st.warning("⚠️ Could not fetch statistics. Make sure the backend API is running.")

elif page == "🔍 Text Analyzer":
    st.markdown('<p class="main-header">🔍 Real-time Text Analyzer</p>', unsafe_allow_html=True)
    
    st.info("💡 Enter text to analyze for hate speech, abusive language, or offensive content.")
    
    # User input
    col1, col2 = st.columns([1, 1])
    with col1:
        user_id = st.number_input("User ID", min_value=1, value=1, step=1)
    with col2:
        username = st.text_input("Username", value=f"user_{user_id}")
    
    # Text input
    text_input = st.text_area(
        "Enter text to analyze:",
        height=150,
        placeholder="Type or paste text here..."
    )
    
    # Analyze button
    if st.button("🔍 Analyze Text", type="primary"):
        if text_input:
            with st.spinner("Analyzing text..."):
                result = analyze_text(text_input, user_id, username)
                
                if result and result.get('success'):
                    analysis = result['result']
                    action = result['action_taken']
                    message = result['message']
                    
                    # Display results
                    st.markdown("### Analysis Results")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Hate Speech Detected", "Yes" if analysis['is_hate_speech'] else "No")
                    with col2:
                        st.metric("Confidence Score", f"{analysis['confidence']:.2%}")
                    with col3:
                        st.metric("Category", analysis['category'].title())
                    
                    # Action message
                    if analysis['is_hate_speech']:
                        if action == 'suspended':
                            st.markdown(f'<div class="danger-box">🚫 {message}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="warning-box">⚠️ {message}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="success-box">✅ {message}</div>', unsafe_allow_html=True)
                    
                    # User status
                    if result.get('user_status'):
                        st.markdown("### User Status")
                        user_status = result['user_status']
                        st.json(user_status)
                else:
                    st.error("❌ Error analyzing text. Please try again.")
        else:
            st.warning("⚠️ Please enter text to analyze.")

elif page == "👥 User Management":
    st.markdown('<p class="main-header">👥 User Management</p>', unsafe_allow_html=True)
    
    users_data = fetch_users()
    
    if users_data and users_data.get('success'):
        users = users_data['users']
        
        if users:
            st.markdown(f"### Total Users: {len(users)}")
            
            # Convert to DataFrame
            users_df = pd.DataFrame(users)
            
            # Display filters
            col1, col2 = st.columns(2)
            with col1:
                status_filter = st.selectbox("Filter by Status", ["All", "Active", "Suspended"])
            with col2:
                sort_by = st.selectbox("Sort by", ["Username", "Warning Count", "Created Date"])
            
            # Apply filters
            filtered_df = users_df.copy()
            if status_filter == "Active":
                filtered_df = filtered_df[filtered_df['is_suspended'] == False]
            elif status_filter == "Suspended":
                filtered_df = filtered_df[filtered_df['is_suspended'] == True]
            
            # Display users
            st.dataframe(filtered_df, use_container_width=True)
            
            # User details
            st.markdown("---")
            st.subheader("User Actions")
            
            user_ids = [u['id'] for u in users]
            selected_user_id = st.selectbox("Select User", user_ids)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("⚠️ Warn User"):
                    try:
                        response = requests.post(f"{API_BASE_URL}/users/{selected_user_id}/warn")
                        if response.status_code == 200:
                            st.success("User warned successfully!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
            
            with col2:
                if st.button("🚫 Suspend User"):
                    try:
                        response = requests.post(f"{API_BASE_URL}/users/{selected_user_id}/suspend")
                        if response.status_code == 200:
                            st.success("User suspended successfully!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
            
            with col3:
                if st.button("✅ Unsuspend User"):
                    try:
                        response = requests.post(f"{API_BASE_URL}/users/{selected_user_id}/unsuspend")
                        if response.status_code == 200:
                            st.success("User unsuspended successfully!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
        else:
            st.info("No users found in the database.")
    else:
        st.warning("⚠️ Could not fetch users. Make sure the backend API is running.")

elif page == "📊 Violations Log":
    st.markdown('<p class="main-header">📊 Violations Log</p>', unsafe_allow_html=True)
    
    violations_data = fetch_violations()
    
    if violations_data and violations_data.get('success'):
        violations = violations_data['violations']
        
        if violations:
            st.markdown(f"### Total Violations: {violations_data['total']}")
            
            # Convert to DataFrame
            violations_df = pd.DataFrame(violations)
            
            # Filters
            col1, col2 = st.columns(2)
            with col1:
                category_filter = st.multiselect(
                    "Filter by Category",
                    options=['All'] + list(violations_df['category'].unique()),
                    default=['All']
                )
            with col2:
                action_filter = st.multiselect(
                    "Filter by Action",
                    options=['All'] + list(violations_df['action_taken'].unique()),
                    default=['All']
                )
            
            # Apply filters
            filtered_df = violations_df.copy()
            if 'All' not in category_filter:
                filtered_df = filtered_df[filtered_df['category'].isin(category_filter)]
            if 'All' not in action_filter:
                filtered_df = filtered_df[filtered_df['action_taken'].isin(action_filter)]
            
            # Display table
            st.dataframe(filtered_df, use_container_width=True)
            
            # Download button
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"violations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No violations recorded yet.")
    else:
        st.warning("⚠️ Could not fetch violations. Make sure the backend API is running.")

elif page == "ℹ️ About":
    st.markdown('<p class="main-header">ℹ️ About the System</p>', unsafe_allow_html=True)
    
    st.markdown("""
    ## Hate Speech Detection & Mitigation System
    
    ### 🎯 Overview
    This full-stack application uses Natural Language Processing (NLP) and Machine Learning to detect 
    and mitigate hate speech on social media platforms in real-time.
    
    ### ✨ Key Features
    
    1. **Real-time Detection**: Analyzes user content instantly using trained ML models
    2. **Automated Moderation**: Issues warnings and automatically suspends repeat offenders
    3. **Categorization**: Classifies hate speech into categories (racial, gender-based, religious, etc.)
    4. **Multilingual Support**: Detects hate speech in multiple languages
    5. **Behavioral Tracking**: Logs all offenses with timestamps and user history
    6. **Moderation Dashboard**: Comprehensive admin panel for monitoring and management
    
    ### 🛠️ Technology Stack
    
    **Backend:**
    - Flask (REST API)
    - SQLAlchemy (Database ORM)
    - scikit-learn & Transformers (ML Models)
    - NLTK (Text Processing)
    
    **Frontend:**
    - Streamlit (Dashboard)
    - Plotly (Data Visualization)
    - Pandas (Data Analysis)
    
    ### 📊 How It Works
    
    1. **Text Analysis**: User submits text → System preprocesses and analyzes
    2. **Detection**: ML model predicts if content contains hate speech
    3. **Classification**: Categorizes type of hate speech
    4. **Action**: Issues warning or suspends user based on violation history
    5. **Logging**: Records all incidents for moderation review
    
    ### 🔒 Moderation Policy
    
    - **1st Offense**: Warning issued to user
    - **2nd Offense**: Account automatically suspended
    - **Manual Review**: Admins can warn, suspend, or unsuspend users
    
    ### 📈 Categories Detected
    
    - Racial hate speech
    - Gender-based discrimination
    - Religious intolerance
    - Homophobic content
    - General offensive/abusive language
    
    ### 🚀 Getting Started
    
    1. Ensure backend API is running on `http://localhost:5000`
    2. Launch this dashboard with `streamlit run frontend/app.py`
    3. Use the Text Analyzer to test hate speech detection
    4. Monitor users and violations through the dashboard
    
    ### 👨‍💻 Developer
    Created as a comprehensive solution for promoting safe and respectful online communities.
    
    ---
    
    **Version**: 1.0.0  
    **Last Updated**: October 2025
    """)
    
    # System Status
    st.markdown("### 🔌 System Status")
    
    try:
        response = requests.get("http://localhost:5000/")
        if response.status_code == 200:
            st.success("✅ Backend API: Online")
        else:
            st.error("❌ Backend API: Offline")
    except:
        st.error("❌ Backend API: Not reachable")
    
    st.success("✅ Frontend Dashboard: Online")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>© 2025 Hate Speech Detection System | Built with ❤️ using Python</p>",
    unsafe_allow_html=True
)
