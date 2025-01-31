# File: app.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import time

# Simulated APIs (replace with actual API calls)
def chatgpt_api(query):
    time.sleep(0.5)  # Simulate response time
    return f"ChatGPT: {query}\n\nDetailed explanation of quantum computing fundamentals..."

def watsonx_api(query):
    time.sleep(0.8)
    return f"Watsonx: {query}\n\nTechnical analysis focusing on qubit implementation..."

def perplexity_api(query):
    time.sleep(0.3)
    return f"Perplexity: {query}\n\nConcise summary with key points about quantum computing..."

def deepseek_simulator(query):
    time.sleep(0.6)
    return f"DeepSeek: {query}\n\nPractical applications and current research in quantum computing..."

# Initialize session state
if 'feedback' not in st.session_state:
    st.session_state.feedback = {}
if 'metrics' not in st.session_state:
    st.session_state.metrics = pd.DataFrame({
        'System': ['ChatGPT', 'Watsonx', 'Perplexity', 'DeepSeek'],
        'Accuracy': [0.85, 0.78, 0.82, 0.80],
        'Creativity': [0.90, 0.75, 0.70, 0.85],
        'Speed': [0.95, 0.80, 0.98, 0.88],
        'Contextual Understanding': [0.88, 0.82, 0.75, 0.85]
    })

# UI Layout
st.title("AI System Comparator 🤖")
col1, col2 = st.columns([3, 1])

# Query Input with Prebuilt selection
with col1:
    user_query = st.text_input("Enter your query:", 
              value="Explain quantum computing in simple terms",
              key="main_query")

with col2:
    dimension = st.selectbox("Select Dimension", 
              ['Accuracy', 'Creativity', 'Speed', 'Contextual Understanding'])

# Preloaded queries with auto-fill
prebuilt_query = st.selectbox("Or choose sample query:", [
    "Write a poem about AI ethics",
    "How does a blockchain work?",
    "Describe photosynthesis to a 5-year-old"
])

if prebuilt_query and prebuilt_query != user_query:
    user_query = prebuilt_query
    st.experimental_rerun()

# Compare button
if st.button("Compare Systems"):
    # Get responses
    responses = {
        "ChatGPT": chatgpt_api(user_query),
        "Watsonx": watsonx_api(user_query),
        "Perplexity": perplexity_api(user_query),
        "DeepSeek": deepseek_simulator(user_query)
    }

    # Display responses
    st.subheader("Responses")
    cols = st.columns(4)
    for idx, (system, response) in enumerate(responses.items()):
        with cols[idx]:
            st.markdown(f"**{system}**")
            st.text_area("", value=response, height=200, key=f"resp_{system}")
            
            # Feedback buttons
            st.write("Rate this response:")
            col_fb1, col_fb2 = st.columns(2)
            with col_fb1:
                if st.button("👍", key=f"up_{system}"):
                    st.session_state.feedback[system] = st.session_state.feedback.get(system, 0) + 1
            with col_fb2:
                if st.button("👎", key=f"down_{system}"):
                    st.session_state.feedback[system] = st.session_state.feedback.get(system, 0) - 1

    # Metrics Visualization
    st.subheader(f"Performance Comparison: {dimension}")
    fig = px.bar(st.session_state.metrics, 
                 x='System', y=dimension,
                 color='System',
                 title=f"{dimension} Comparison")
    st.plotly_chart(fig)

    # Fixed Radar Chart
    st.subheader("Comprehensive Analysis")
    radar_fig = go.Figure()
    
    for index, row in st.session_state.metrics.iterrows():
        radar_fig.add_trace(go.Scatterpolar(
            r=row[1:].values,
            theta=st.session_state.metrics.columns[1:],
            name=row['System']
        ))
    
    radar_fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True
    )
    st.plotly_chart(radar_fig)

# Summary Dashboard
st.sidebar.header("Summary Dashboard")
if st.session_state.feedback:
    st.sidebar.subheader("User Feedback")
    feedback_df = pd.DataFrame.from_dict(st.session_state.feedback, 
                                       orient='index', columns=['Score'])
    st.sidebar.bar_chart(feedback_df)

# Recommendation System
st.sidebar.subheader("Recommendation")
try:
    best_system = st.session_state.metrics.set_index('System')[dimension].idxmax()
    st.sidebar.markdown(f"**Best for {dimension}:**")
    st.sidebar.success(f"{best_system} 🏆")
except KeyError:
    st.sidebar.error("No data available for this dimension")

# Run with: streamlit run app.py

pip install streamlit plotly pandas
streamlit run app.py
