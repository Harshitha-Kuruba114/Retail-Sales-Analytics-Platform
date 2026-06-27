import streamlit as st
import pandas as pd
import os
import plotly.express as px
# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(
    page_title="Retail Sales Analytics Platform",
    page_icon="📊",
    layout="wide"
)

# --------------------------
# LOAD DATA
# --------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", "SampleSuperstore.csv")


@st.cache_data
def load_data():
    return pd.read_csv(CSV_PATH)


df = load_data()

# Remove extra spaces from column names
df.columns = df.columns.str.strip()
# --------------------------
# TITLE
# --------------------------
st.title("📊 Retail Sales Analytics Platform")

st.markdown("Interactive Retail Sales Dashboard")

# --------------------------
# SIDEBAR
# --------------------------
st.sidebar.header("Filters")

region = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

category = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

segment = st.sidebar.multiselect(
    "Segment",
    sorted(df["Segment"].unique()),
    default=sorted(df["Segment"].unique())
)

state = st.sidebar.multiselect(
    "State",
    sorted(df["State"].unique()),
    default=sorted(df["State"].unique())
)

# --------------------------
# FILTER DATA
# --------------------------
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Segment"].isin(segment)) &
    (df["State"].isin(state))
]
if filtered_df.empty:
    st.warning("⚠️ No data available for the selected filters.")
    st.stop()
# --------------------------
# KPI CARDS
# --------------------------

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df.shape[0]
avg_discount = filtered_df["Discount"].mean() * 100

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Sales",
    f"${total_sales:,.2f}"
)

col2.metric(
    "📈 Total Profit",
    f"${total_profit:,.2f}"
)

col3.metric(
    "📦 Orders",
    total_orders
)

col4.metric(
    "🏷 Average Discount",
    f"{avg_discount:.2f}%"
)

st.divider()

# --------------------------
# FILTERED DATA
# --------------------------

st.subheader("📋 Filtered Dataset")

st.write("Rows:", filtered_df.shape[0])
st.write("Columns:", filtered_df.shape[1])

st.dataframe(filtered_df, width="stretch")
# ==========================================
# SALES BY CATEGORY BAR CHART
# ==========================================

st.divider()
st.subheader("📊 Sales by Category")

# Group data
sales_category = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

# Create bar chart
fig = px.bar(
    sales_category,
    x="Category",
    y="Sales",
    color="Category",
    title="Sales by Category",
    text_auto=".2s"
)

# Display chart
st.plotly_chart(fig, width="stretch")
# ==========================================
# SALES BY REGION BAR CHART
# ==========================================

st.divider()
st.subheader("🌍 Sales by Region")

# Group data
sales_region = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
    .reset_index()
)

# Create chart
fig = px.bar(
    sales_region,
    x="Region",
    y="Sales",
    color="Region",
    title="Sales by Region",
    text_auto=".2s"
)

# Display chart
st.plotly_chart(fig, width="stretch")
# ==========================================
# PROFIT BY SEGMENT PIE CHART
# ==========================================

st.divider()
st.subheader("🥧 Profit by Segment")

profit_segment = (
    filtered_df.groupby("Segment")["Profit"]
    .sum()
    .reset_index()
)

fig = px.pie(
    profit_segment,
    names="Segment",
    values="Profit",
    title="Profit Distribution by Segment",
    hole=0.4
)

st.plotly_chart(fig, width="stretch")

# ==========================================
# TOP 10 SUB-CATEGORIES
# ==========================================
st.divider()
st.subheader("🏆 Top 10 Sub-Categories by Sales")

top_sub = (
    filtered_df.groupby("Sub-Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_sub,
    x="Sales",
    y="Sub-Category",
    orientation="h",
    color="Sales",
    title="Top 10 Sub-Categories by Sales",
    text_auto=".2s"
)

fig.update_layout(
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(fig, width="stretch")
# ==========================================
# PROFIT VS SALES
# ==========================================

st.divider()
st.subheader("📈 Profit vs Sales")

fig = px.scatter(
    filtered_df,
    x="Sales",
    y="Profit",
    color="Category",
    size="Quantity",
    hover_data=["State", "Sub-Category"],
    title="Profit vs Sales Analysis"
)

st.plotly_chart(fig, width="stretch")
# ==========================================
# TOP 10 STATES
# ==========================================

st.divider()
st.subheader("🌎 Top 10 States by Sales")

state_sales = (
    filtered_df.groupby("State")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    state_sales,
    x="State",
    y="Sales",
    color="Sales",
    text_auto=".2s",
    title="Top 10 States"
)

st.plotly_chart(fig, width="stretch")
# ==========================================
# DOWNLOAD DATA
# ==========================================

st.divider()

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="filtered_sales.csv",
    mime="text/csv",
)
