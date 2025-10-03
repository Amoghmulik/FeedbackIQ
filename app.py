import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="FeedbackIQ", layout="wide")

# Title
st.title("🧠 FeedbackIQ - Feedback Intelligence")
st.markdown("### AI-Powered Feedback Analysis Dashboard")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('prioritized_feedback.csv')

df = load_data()

# Sidebar
st.sidebar.header("📊 Overview")
st.sidebar.metric("Total Feedback", len(df))
st.sidebar.metric("Critical Issues", len(df[df['priority_level'] == 'CRITICAL']))
st.sidebar.metric("High Priority", len(df[df['priority_level'] == 'HIGH']))

# Main content
tab1, tab2, tab3 = st.tabs(["📋 Priority List", "📊 Analytics", "💡 Insights"])

with tab1:
    st.header("Prioritized Feedback List")
    filter_priority = st.multiselect(
        "Filter by Priority",
        ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
        default=['CRITICAL', 'HIGH']
    )
    filtered_df = df[df['priority_level'].isin(filter_priority)]
    for idx, row in filtered_df.iterrows():
        with st.expander(f"**{row['feedback_id']}** - {row['priority_level']} (Score: {row['priority_score']})"):
            st.write(f"**Original Feedback:** {row['original_text']}")
            st.write(f"**Category:** {row['category']}")
            st.write(f"**Sentiment:** {row['sentiment']}")
            st.write(f"**Urgency:** {row['urgency']}")
            st.write(f"**AI Summary:** {row['ai_summary']}")

with tab2:
    st.header("Analytics Dashboard")
    col1, col2 = st.columns(2)

    with col1:
        priority_counts = df['priority_level'].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.bar(priority_counts.index, priority_counts.values)
        ax1.set_title("Priority Distribution")
        st.pyplot(fig1)

    with col2:
        category_counts = df['category'].value_counts()
        fig2, ax2 = plt.subplots()
        ax2.pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%')
        ax2.set_title("Category Breakdown")
        st.pyplot(fig2)

with tab3:
    st.header("💡 Key Insights")
    critical_issues = df[df['priority_level'] == 'CRITICAL']
    st.markdown(f"""
    ### Summary
    - **Total Feedback Analyzed:** {len(df)}
    - **Critical Issues:** {len(critical_issues)}
    - **Most Common Category:** {df['category'].value_counts().index[0]}
    
    ### Top 3 Priorities:
    """)
    for idx, row in df.head(3).iterrows():
        st.markdown(f"**{idx+1}. {row['feedback_id']}** - {row['original_text'][:100]}...")

st.markdown("---")
st.markdown("*Powered by FeedbackIQ - AI Feedback Intelligence*")
