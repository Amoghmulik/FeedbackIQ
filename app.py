import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from groq import Groq

# -------------------- Page Config --------------------
st.set_page_config(page_title="FeedbackIQ", layout="wide")

# -------------------- Title --------------------
st.title("🧠 FeedbackIQ - Feedback Intelligence")
st.markdown("### AI-Powered Feedback Analysis Dashboard")

# -------------------- Load Data --------------------
@st.cache_data
def load_data():
    df = pd.read_csv('prioritized_feedback.csv')
    # Fill missing values with 'Unknown'
    df['category'] = df['category'].fillna('Unknown')
    df['priority_level'] = df['priority_level'].fillna('LOW')
    df['ai_summary'] = df['ai_summary'].fillna('AI summary pending')
    return df

df = load_data()

# -------------------- Sidebar --------------------
st.sidebar.header("📊 Overview")
st.sidebar.metric("Total Feedback", len(df))
st.sidebar.metric("Critical Issues", len(df[df['priority_level'] == 'CRITICAL']))
st.sidebar.metric("High Priority", len(df[df['priority_level'] == 'HIGH']))

# -------------------- Tabs --------------------
tab1, tab2, tab3 = st.tabs(["📋 Priority List", "📊 Analytics", "💡 Insights"])

# -------------------- TAB 1: Priority List --------------------
with tab1:
    st.header("Prioritized Feedback List")

    # Filter by priority
    filter_priority = st.multiselect(
        "Filter by Priority",
        ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW'],
        default=['CRITICAL', 'HIGH', 'MEDIUM']
    )
    filtered_df = df[df['priority_level'].isin(filter_priority)]

    # Color-coded priorities
    def highlight_priority(priority):
        if priority == "CRITICAL":
            return "background-color: #ff9999"
        elif priority == "HIGH":
            return "background-color: #ffcc99"
        elif priority == "MEDIUM":
            return "background-color: #fff2cc"
        else:
            return "background-color: #ccffcc"

    st.dataframe(filtered_df[['feedback_id','original_text','category','priority_level','priority_score']].style.applymap(
        highlight_priority, subset=["priority_level"]
    ))

    # Download filtered CSV
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Prioritized Feedback", csv, "feedback_results.csv", "text/csv")

# -------------------- TAB 2: Analytics --------------------
with tab2:
    st.header("Analytics Dashboard")
    col1, col2 = st.columns(2)

    with col1:
        priority_counts = filtered_df['priority_level'].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.bar(priority_counts.index, priority_counts.values, color=['#ff9999','#ffcc99','#fff2cc','#ccffcc'])
        ax1.set_title("Priority Distribution")
        st.pyplot(fig1)

    with col2:
        category_counts = filtered_df['category'].value_counts()
        fig2, ax2 = plt.subplots()
        ax2.pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%', startangle=90)
        ax2.set_title("Category Breakdown")
        st.pyplot(fig2)

# -------------------- TAB 3: Insights --------------------
with tab3:
    st.header("💡 Key Insights")

    critical_issues = filtered_df[filtered_df['priority_level'] == 'CRITICAL']
    st.markdown(f"""
    ### Summary
    - **Total Feedback Analyzed:** {len(filtered_df)}
    - **Critical Issues:** {len(critical_issues)}
    - **Most Common Category:** {filtered_df['category'].mode()[0]}
    
    ### Top 3 Priorities:
    """)
    for idx, row in filtered_df.head(3).iterrows():
        st.markdown(f"**{idx+1}. {row['feedback_id']}** - {row['original_text'][:120]}...")

    # AI Summary
    st.markdown("### 🤖 AI Insights")
    try:
        client = Groq(api_key="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")
        top_feedback_text = "\n".join(filtered_df.head(10)['original_text'].tolist())
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": f"Summarize insights from this feedback:\n{top_feedback_text}"}]
        )
        st.write(response.choices[0].message["content"])
    except Exception as e:
        st.warning("AI summary not available. Check your Groq API key.")

# -------------------- Footer --------------------
st.markdown("---")
st.markdown("*Powered by FeedbackIQ - AI Feedback Intelligence*")
