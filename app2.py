import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.facecolor'] = '#0e1117'
plt.rcParams['axes.facecolor'] = '#0e1117'
plt.rcParams['axes.edgecolor'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'
plt.rcParams['text.color'] = 'white'
plt.rcParams['legend.facecolor'] = '#262730'
plt.rcParams['legend.edgecolor'] = 'white'
from groq import Groq

# Page config
st.set_page_config(
    page_title="Global E-Commerce Intelligence",
    page_icon="🌍",
    layout="wide"
)

# Groq client
client = client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('ecommerce_cleaned.csv')
    df['Order_Date'] = pd.to_datetime(df['Order_Date'], dayfirst=True)
    forecast = pd.read_csv('sales_forecast.csv')
    segments = pd.read_csv('customer_segments.csv')
    return df, forecast, segments

df, forecast, segments = load_data()

# Sidebar navigation
st.sidebar.title("🌍 Navigation")
st.sidebar.markdown("---")
page = st.sidebar.radio("Go to:", [
    "📊 Dashboard",
    "🔮 Sales Forecast",
    "👥 Customer Segments",
    "🤖 AI Assistant"
])

# Sidebar stats
st.sidebar.markdown("---")
st.sidebar.markdown("**Project Info**")
st.sidebar.info("Built with Python, Prophet, KMeans & Groq AI")
st.sidebar.metric("Total Orders", f"{len(df):,}")
st.sidebar.metric("Total Revenue", f"${df['Revenue'].sum():,.0f}")

# ============================================
# PAGE 1 - DASHBOARD
# ============================================
if page == "📊 Dashboard":
    st.title("📊 Global E-Commerce Sales Intelligence")
    st.markdown("**Built by Amulya | AI-Powered Sales Analytics**")
    st.divider()

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Orders", f"{len(df):,}")
    col2.metric("Total Revenue", f"${df['Revenue'].sum():,.0f}")
    col3.metric("Total Profit", f"${df['Profit'].sum():,.0f}")
    col4.metric("Countries", df['Country'].nunique())
    st.divider()

    # Charts
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Revenue by Category")
        cat_revenue = df.groupby('Category')['Revenue'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(cat_revenue.index, cat_revenue.values, color='steelblue')
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
        ax.set_xlabel('Category')
        ax.set_ylabel('Revenue ($)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        st.subheader("Revenue by Country")
        country_revenue = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False).head(8)
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.barh(country_revenue.index, country_revenue.values, color='coral')
        ax.set_xlabel('Revenue ($)')
        plt.tight_layout()
        st.pyplot(fig)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Monthly Revenue Trend")
        monthly = df.groupby('Month')['Revenue'].sum()
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(monthly.index, monthly.values, marker='o', color='steelblue')
        ax.set_xlabel('Month')
        ax.set_ylabel('Revenue ($)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        st.subheader("Revenue by Gender")
        gender_revenue = df.groupby('Customer_Gender')['Revenue'].sum()
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.pie(gender_revenue.values, labels=gender_revenue.index,
               autopct='%1.1f%%', colors=['#3498db', '#e74c3c'])
        plt.tight_layout()
        st.pyplot(fig)

# ============================================
# PAGE 2 - SALES FORECAST
# ============================================
elif page == "🔮 Sales Forecast":
    st.title("🔮 AI Sales Forecasting")
    st.markdown("**Prophet Model | Next 6 Months Revenue Prediction**")
    st.divider()

    forecast['Month'] = pd.to_datetime(forecast['Month'])
    actual = forecast[forecast['Month'] <= df['Order_Date'].max()]
    future = forecast[forecast['Month'] > df['Order_Date'].max()]

    col1, col2, col3 = st.columns(3)
    col1.metric("Months Forecasted", "6")
    col2.metric("Avg Predicted Revenue", f"${future['Predicted_Revenue'].mean():,.0f}")
    col3.metric("Forecast Model", "Prophet AI")
    st.divider()

    # Forecast chart
    st.subheader("Revenue Forecast Chart")
    fig, ax = plt.subplots(figsize=(12, 5))
    monthly = df.groupby('Month')['Revenue'].sum()
    ax.plot(monthly.index, monthly.values, marker='o',
            color='steelblue', linewidth=2, label='Actual Revenue')
    ax.plot(future['Month'].astype(str), future['Predicted_Revenue'],
            marker='s', color='orange', linewidth=2,
            linestyle='--', label='Forecasted Revenue')
    ax.fill_between(future['Month'].astype(str),
                    future['Lower_Bound'], future['Upper_Bound'],
                    alpha=0.2, color='orange', label='Confidence Range')
    ax.axvline(x=monthly.index[-1], color='red',
               linestyle=':', linewidth=1.5, label='Forecast Start')
    ax.set_xlabel('Month')
    ax.set_ylabel('Revenue ($)')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    st.subheader("Forecast Table")
    st.dataframe(future[['Month', 'Predicted_Revenue', 
                          'Lower_Bound', 'Upper_Bound']])

# ============================================
# PAGE 3 - CUSTOMER SEGMENTS
# ============================================
elif page == "👥 Customer Segments":
    st.title("👥 AI Customer Segmentation")
    st.markdown("**KMeans Clustering | 3 Customer Groups**")
    st.divider()

    col1, col2, col3 = st.columns(3)
    high = segments[segments['Segment_Label'] == 'High Value']
    mid = segments[segments['Segment_Label'] == 'Mid Value']
    low = segments[segments['Segment_Label'] == 'Low Value']
    col1.metric("High Value Customers", len(high))
    col2.metric("Mid Value Customers", len(mid))
    col3.metric("Low Value Customers", len(low))
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Customer Count by Segment")
        seg_counts = segments['Segment_Label'].value_counts()
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(seg_counts.index, seg_counts.values,
               color=['#2ecc71', '#3498db', '#e74c3c'])
        ax.set_ylabel('Number of Customers')
        for i, v in enumerate(seg_counts.values):
            ax.text(i, v + 5, str(v), ha='center', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)

    with col2:
        st.subheader("Average Revenue by Segment")
        seg_revenue = segments.groupby('Segment_Label')['Total_Revenue'].mean()
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.bar(seg_revenue.index, seg_revenue.values,
               color=['#2ecc71', '#3498db', '#e74c3c'])
        ax.set_ylabel('Average Revenue ($)')
        for i, v in enumerate(seg_revenue.values):
            ax.text(i, v + 50, f'${v:,.0f}', ha='center', fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)

    st.subheader("Customer Segment Details")
    st.dataframe(segments[['Customer_ID', 'Total_Orders', 
                            'Total_Revenue', 'Total_Profit', 
                            'Segment_Label']])

# ============================================
# PAGE 4 - AI ASSISTANT
# ============================================
elif page == "🤖 AI Assistant":
    st.title("🤖 AI Data Assistant")
    st.markdown("**Ask anything about the E-Commerce data!**")
    st.divider()
    st.info("👋 Hi! I'm your AI Data Assistant. I can answer questions about sales, revenue, customers, forecasts and more. Try the sample questions below or type your own!")
    st.divider()

    # Prepare data summary for AI
    data_summary = f"""
    You are a data analyst assistant. Answer questions based on this E-Commerce data:
    - Total Orders: {len(df):,}
    - Total Revenue: ${df['Revenue'].sum():,.0f}
    - Total Profit: ${df['Profit'].sum():,.0f}
    - Date Range: {df['Order_Date'].min().date()} to {df['Order_Date'].max().date()}
    - Countries: {', '.join(df['Country'].unique())}
    - Categories: {', '.join(df['Category'].unique())}
    - Top Country by Revenue: {df.groupby('Country')['Revenue'].sum().idxmax()}
    - Top Category by Revenue: {df.groupby('Category')['Revenue'].sum().idxmax()}
    - High Value Customers: {len(segments[segments['Segment_Label']=='High Value'])}
    - Sales Forecast: Next 6 months avg ${forecast[forecast['Month'] > str(df['Order_Date'].max().date())[:7]]['Predicted_Revenue'].mean():,.0f}
    Always give short, clear, business-focused answers.
    """

    # Chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.write(message['content'])

    # Sample questions
    st.markdown("**Try asking:**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Which country has highest revenue? ↗"):
            st.session_state.sample_q = "Which country has the highest revenue?"
        if st.button("What is the sales forecast? ↗"):
            st.session_state.sample_q = "What is the sales forecast for next 6 months?"
    with col2:
        if st.button("Which category performs best? ↗"):
            st.session_state.sample_q = "Which category performs best?"
        if st.button("Tell me about customer segments ↗"):
            st.session_state.sample_q = "Tell me about the customer segments"

    # Chat input
    prompt = st.chat_input("Ask me anything about the data...")
    if hasattr(st.session_state, 'sample_q'):
        prompt = st.session_state.sample_q
        del st.session_state.sample_q

    if prompt:
        st.session_state.messages.append({'role': 'user', 'content': prompt})
        with st.chat_message('user'):
            st.write(prompt)

        with st.chat_message('assistant'):
            with st.spinner('Thinking...'):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {'role': 'system', 'content': data_summary},
                        {'role': 'user', 'content': prompt}
                    ]
                )
                answer = response.choices[0].message.content
                st.write(answer)
                st.session_state.messages.append({
                    'role': 'assistant',
                    'content': answer
                })
