# app.py
import os
import subprocess

# Check if running in an online environment
def is_online_environment():
    return os.getenv("COLAB_RELEASE_TAG") or os.getenv("REPLIT_DB_URL")

# Install dependencies if running online
if is_online_environment():
    print("Installing dependencies...")
    subprocess.run(["pip", "install", "streamlit", "plotly", "pandas"])
    print("Dependencies installed!")

# Import libraries
import streamlit as st
import plotly.express as px
import pandas as pd
import time
import json
from datetime import datetime

# ======================
# Configuration
# ======================
SYSTEMS = ['ChatGPT', 'Watsonx', 'Perplexity', 'DeepSeek']
DIMENSIONS = [
    'Accuracy', 'Creativity', 'Speed', 'Contextual Understanding',
    'Domain Expertise', 'Bias and Fairness', 'Customizability',
    'User Interface', 'Cost and Scalability', 'Ethical Considerations'
]

# ======================
# API Simulation 
# ======================
class AISimulator:
    def __init__(self):
        self.conversation_history = {}
        
    def get_response(self, system, query):
        time.sleep(max(0.2, 1 - self._performance_score(system, 'Speed')))
        return f"{system} response to: {query}\n\n{self._generate_metadata(system, query)}"
    
    def _performance_score(self, system, dimension):
        base_scores = {
            'ChatGPT': [0.85, 0.90, 0.95, 0.88, 0.82, 0.75, 0.70, 0.92, 0.80, 0.78],
            'Watsonx': [0.78, 0.75, 0.80, 0.82, 0.88, 0.85, 0.60, 0.85, 0.75, 0.82],
            'Perplexity': [0.82, 0.70, 0.98, 0.75, 0.79, 0.78, 0.65, 0.88, 0.85, 0.80],
            'DeepSeek': [0.80, 0.85, 0.88, 0.90, 0.84, 0.82, 0.75, 0.90, 0.78, 0.85]
        }
        return base_scores[system][DIMENSIONS.index(dimension)]
    
    def _generate_metadata(self, system, query):
        return json.dumps({
            "timestamp": datetime.now().isoformat(),
            "sentiment": "positive" if "?" in query else "neutral",
            "complexity": len(query.split())
        }, indent=2)

# ======================
# Core Functions
# ======================
def initialize_session():
    if 'feedback' not in st.session_state:
        st.session_state.feedback = {system: [] for system in SYSTEMS}
        
    if 'metrics' not in st.session_state:
        st.session_state.metrics = pd.DataFrame({
            'System': SYSTEMS,
            'Accuracy': [0.85, 0.78, 0.82, 0.80],
            'Creativity': [0.90, 0.75, 0.70, 0.85],
            'Speed': [0.95, 0.80, 0.98, 0.88],
            'Contextual Understanding': [0.88, 0.82, 0.75, 0.90],
            'Domain Expertise': [0.82, 0.88, 0.79, 0.84],
            'Bias and Fairness': [0.75, 0.85, 0.78, 0.82],
            'Customizability': [0.70, 0.60, 0.65, 0.75],
            'User Interface': [0.92, 0.85, 0.88, 0.90],
            'Cost and Scalability': [0.80, 0.75, 0.85, 0.78],
            'Ethical Considerations': [0.78, 0.82, 0.80, 0.85]
        })

# ======================
# UI Components
# ======================
def main():
    st.set_page_config(page_title="AI System Comparator", layout="wide")
    initialize_session()
    ai_sim = AISimulator()
    
    # Header
    st.title("🤖 AI System Comparator")
    st.markdown("Compare leading AI systems across multiple dimensions")
    
    # Control Panel
    with st.expander("⚙️ Control Panel", expanded=True):
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            user_query = st.text_input("Enter your query:", 
                value="Explain quantum computing in simple terms")
        with col2:
            dimension = st.selectbox("Primary Dimension", DIMENSIONS)
        with col3:
            prebuilt_queries = st.selectbox("Sample queries:", [
                "Write a poem about AI ethics",
                "How does a blockchain work?",
                "Describe photosynthesis to a 5-year-old",
                "Should AI be used in military applications?",
                "Create a Python script for image recognition"
            ])
    
    # Main Comparison
    if st.button("🚀 Compare Systems", use_container_width=True):
        with st.spinner("Analyzing responses..."):
            responses = {system: ai_sim.get_response(system, user_query) 
                        for system in SYSTEMS}
            
            # Display Responses
            st.subheader("💬 System Responses")
            cols = st.columns(4)
            for idx, (system, response) in enumerate(responses.items()):
                with cols[idx]:
                    with st.container(border=True):
                        st.markdown(f"### {system}")
                        st.text_area("", value=response, height=300, 
                                   key=f"resp_{system}")
                        
                        # Feedback System
                        st.markdown("---")
                        st.write("**Rate this response:**")
                        if st.button(f"👍", key=f"up_{system}"):
                            st.session_state.feedback[system].append(1)
                        st.button(f"👎", key=f"down_{system}")
            
            # Visualization Section
            st.subheader("📊 Performance Analysis")
            tab1, tab2, tab3 = st.tabs(["Dimension Comparison", 
                                      "Radar Chart", "Historical Trends"])
            
            with tab1:
                fig = px.bar(st.session_state.metrics, 
                           x='System', y=dimension,
                           color='System', text_auto='.2f',
                           title=f"{dimension} Comparison")
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                radar_fig = px.line_polar(
                    st.session_state.metrics, 
                    r=st.session_state.metrics.loc[
                        st.session_state.metrics['System'] == 'ChatGPT'
                    ].iloc[0][1:].values,
                    theta=DIMENSIONS,
                    line_close=True,
                    title="ChatGPT Capability Radar"
                )
                st.plotly_chart(radar_fig, use_container_width=True)
            
            with tab3:
                hist_fig = px.line(
                    pd.DataFrame(st.session_state.feedback).T,
                    title="User Feedback Trends"
                )
                st.plotly_chart(hist_fig, use_container_width=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔍 Analysis Tools")
        st.subheader("Recommendation Engine")
        best_system = st.session_state.metrics.set_index('System')[dimension].idxmax()
        st.success(f"**Best for {dimension}:** {best_system}")
        
        st.subheader("Feedback Insights")
        if st.session_state.feedback:
            feedback_df = pd.DataFrame.from_dict(
                st.session_state.feedback, 
                orient='index', 
                columns=['Score']
            )
            st.bar_chart(feedback_df)
        
        st.download_button(
            label="📥 Export Data",
            data=st.session_state.metrics.to_csv().encode('utf-8'),
            file_name='ai_comparison_data.csv'
        )

if __name__ == "__main__":
    main()
