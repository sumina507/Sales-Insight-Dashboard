# app.py (UPDATED - includes all 6 charts)
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Page config
st.set_page_config(page_title="Sales Insight Dashboard", layout="wide")
st.title("📊 Retail Store Sales Dashboard")
st.markdown("Interactive dashboard for Superstore sales data (2011–2014)")

# Load data from SQLite
@st.cache_data
def load_data():
    conn = sqlite3.connect('sales.db')
    df = pd.read_sql_query("SELECT * FROM sales", conn)
    conn.close()
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
regions = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
categories = st.sidebar.multiselect("Select Category", options=df['Category'].unique(), default=df['Category'].unique())

# Filter data
filtered_df = df[df['Region'].isin(regions) & df['Category'].isin(categories)]

# Key metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"${filtered_df['Profit'].sum():,.0f}")
col3.metric("Avg Discount", f"{filtered_df['Discount'].mean():.1%}")
col4.metric("Number of Orders", filtered_df.shape[0])

# ========== CHART 1: Monthly Sales Trend ==========
st.subheader("1. Monthly Sales Trend")
monthly = filtered_df.groupby(filtered_df['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()
monthly['Order Date'] = monthly['Order Date'].astype(str)
fig1 = px.line(monthly, x='Order Date', y='Sales', title="Sales Over Time (Seasonal Peaks)")
st.plotly_chart(fig1, use_container_width=True)

# ========== CHART 2: Top 10 Products by Sales ==========
st.subheader("2. Top 10 Products by Sales")
top_products = filtered_df.groupby('Product Name')['Sales'].sum().nlargest(10).reset_index()
fig2 = px.bar(top_products, x='Sales', y='Product Name', orientation='h', 
              title="Highest Revenue Products", color='Sales', color_continuous_scale='Viridis')
st.plotly_chart(fig2, use_container_width=True)

# Row 3: Two columns for Charts 3 & 4
col_left, col_right = st.columns(2)

with col_left:
    # ========== CHART 3: Sales by Category ==========
    st.subheader("3. Sales by Category")
    cat_sales = filtered_df.groupby('Category')['Sales'].sum().reset_index()
    fig3 = px.bar(cat_sales, x='Category', y='Sales', color='Category', title="Sales by Product Category")
    st.plotly_chart(fig3, use_container_width=True)

with col_right:
    # ========== CHART 4: Profit by Region ==========
    st.subheader("4. Profit by Region")
    reg_profit = filtered_df.groupby('Region')['Profit'].sum().reset_index()
    fig4 = px.bar(reg_profit, x='Region', y='Profit', color='Region', title="Total Profit by Region")
    st.plotly_chart(fig4, use_container_width=True)

# Row 5: Two columns for Charts 5 & 6
col_left2, col_right2 = st.columns(2)

with col_left2:
    # ========== CHART 5: Correlation Heatmap ==========
    st.subheader("5. Correlation Heatmap")
    numeric_cols = ['Sales', 'Quantity', 'Discount', 'Profit']
    corr = filtered_df[numeric_cols].corr()
    fig5 = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r', 
                     aspect='auto', title="Relationships: Sales, Quantity, Discount, Profit")
    st.plotly_chart(fig5, use_container_width=True)

with col_right2:
    # ========== CHART 6: Profit Distribution by Region (Boxplot) ==========
    st.subheader("6. Profit Distribution by Region")
    fig6 = px.box(filtered_df, x='Region', y='Profit', color='Region', 
                  title="Profit Variability Across Regions", points="outliers")
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")
st.caption("Built with Streamlit, Plotly, and SQLite | 6 Key Visualizations")