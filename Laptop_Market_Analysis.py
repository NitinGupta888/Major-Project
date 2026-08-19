import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# Dashboard Title
# ==========================================

st.markdown("""
<h1 style='text-align:center; color:#3A86FF; font-size:42px;'>
💻 Laptop Market Analysis
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<h4 style='text-align:center; color:#555;'>
Laptop Market Analytics Dashboard
</h4>
""", unsafe_allow_html=True)

st.markdown("""
<p style='text-align:center; color:gray;'>
Analyze laptop prices, brands, specifications, operating systems, ratings, and market trends.
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# Dashboard Banner
# ==========================================

st.markdown("""
<div style="
background:linear-gradient(90deg,#3A86FF,#8338EC);
padding:25px;
border-radius:15px;
text-align:center;
color:white;
margin-bottom:20px;
">

<h2>📊 Laptop Market Analysis Dashboard</h2>

<p style="font-size:18px;">
Laptop Pricing & Specification Analysis
</p>

</div>
""", unsafe_allow_html=True)


# ==========================================
# Load Dataset
# ==========================================

df = pd.read_csv("laptop_data.csv")


# ==========================================
# Sidebar Filters
# ==========================================

st.sidebar.markdown("---")

st.sidebar.header("🔍 Filters")


brand = st.sidebar.selectbox(
    "🏷️ Select Brand",
    ["All"] + sorted(df["Brand"].unique().tolist())
)


processor = st.sidebar.selectbox(
    "🧠 Select Processor",
    ["All"] + sorted(df["Processor"].unique().tolist())
)


os = st.sidebar.selectbox(
    "💻 Operating System",
    ["All"] + sorted(df["OS"].unique().tolist())
)


ram = st.sidebar.selectbox(
    "🧠 Select RAM",
    ["All"] + sorted(df["RAM"].unique().tolist())
)


# ==========================================
# Apply Filters
# ==========================================

filtered_df = df.copy()


if brand != "All":

    filtered_df = filtered_df[
        filtered_df["Brand"] == brand
    ]


if processor != "All":

    filtered_df = filtered_df[
        filtered_df["Processor"] == processor
    ]


if os != "All":

    filtered_df = filtered_df[
        filtered_df["OS"] == os
    ]


if ram != "All":

    filtered_df = filtered_df[
        filtered_df["RAM"] == ram
    ]


st.sidebar.success(
    f"💻 Total Records : {len(filtered_df)}"
)


# ==========================================
# Search Laptop
# ==========================================

search = st.sidebar.text_input(
    "🔍 Search Laptop"
)


if search:

    filtered_df = filtered_df[
        filtered_df["Model"].str.contains(
            search,
            case=False,
            na=False
        )
    ]


# ==========================================
# Dashboard Summary
# ==========================================

st.markdown("---")

st.subheader("📊 Dashboard Summary")


col1, col2, col3, col4 = st.columns(4)


total_laptops = len(filtered_df)

average_price = filtered_df["Price"].mean()

highest_price = filtered_df["Price"].max()

average_rating = filtered_df["Rating"].mean()


col1.metric(
    "💻 Total Laptops",
    total_laptops
)


col2.metric(
    "💰 Average Price",
    f"₹ {average_price:,.0f}"
)


col3.metric(
    "💎 Highest Price",
    f"₹ {highest_price:,.0f}"
)


col4.metric(
    "⭐ Rating",
    round(average_rating, 2)
)


# ==========================================
# Laptop Data
# ==========================================

st.markdown("---")

st.subheader("📋 Laptop Data")


st.dataframe(
    filtered_df,
    use_container_width=True,
    height=350
)


# ==========================================
# Laptop Market Analytics
# ==========================================

st.markdown("---")

st.subheader("📊 Laptop Market Analytics")


# ==========================================
# ROW 1
# ==========================================

col1, col2 = st.columns(2)


# ==========================================
# Chart 1 : Brand-wise Average Price
# ==========================================

with col1:

    st.markdown("### 🏷️ Brand-wise Average Price")

    brand_price = (
        filtered_df
        .groupby("Brand")["Price"]
        .mean()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.bar(
        brand_price.index,
        brand_price.values
    )

    ax.set_ylabel("Average Price (₹)")
    ax.set_xlabel("Brand")
    ax.set_title("Average Price by Brand")

    plt.xticks(rotation=25)

    st.pyplot(fig)


# ==========================================
# Chart 2 : Operating System
# ==========================================

with col2:

    st.markdown("### 💻 Operating System")

    os_count = filtered_df["OS"].value_counts()

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.pie(
        os_count,
        labels=os_count.index,
        autopct="%1.1f%%",
        startangle=90
    )

    ax.axis("equal")

    st.pyplot(fig)


# ==========================================
# ROW 2
# ==========================================

col3, col4 = st.columns(2)


# ==========================================
# Chart 3 : RAM vs Price
# ==========================================

with col3:

    st.markdown("### 🧠 RAM vs Price")

    ram_price = (
        filtered_df
        .groupby("RAM")["Price"]
        .mean()
    )

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.plot(
        ram_price.index,
        ram_price.values,
        marker="o",
        linewidth=3
    )

    ax.set_xlabel("RAM")
    ax.set_ylabel("Average Price (₹)")
    ax.set_title("RAM vs Average Laptop Price")

    st.pyplot(fig)


# ==========================================
# Chart 4 : Processor Distribution
# ==========================================

with col4:

    st.markdown("### 🧠 Processor Distribution")

    processor_count = (
        filtered_df["Processor"]
        .value_counts()
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(6, 4))

    ax.bar(
        processor_count.index,
        processor_count.values
    )

    ax.set_xlabel("Processor")
    ax.set_ylabel("Number of Laptops")
    ax.set_title("Processor Distribution")

    plt.xticks(rotation=30)

    st.pyplot(fig)


# ==========================================
# Top 5 Expensive Laptops
# ==========================================

st.markdown("---")

st.subheader("💎 Top 5 Most Expensive Laptops")


top_laptops = (
    filtered_df
    .sort_values(
        by="Price",
        ascending=False
    )
    .head(5)
)


fig, ax = plt.subplots(figsize=(8, 4))


ax.barh(
    top_laptops["Model"],
    top_laptops["Price"]
)


ax.set_xlabel("Price (₹)")
ax.set_ylabel("Laptop")
ax.set_title("Top 5 Most Expensive Laptops")

ax.invert_yaxis()

st.pyplot(fig)


# ==========================================
# Price Distribution
# ==========================================

st.markdown("---")

st.subheader("💰 Laptop Price Distribution")


fig, ax = plt.subplots(figsize=(10, 5))


ax.hist(
    filtered_df["Price"],
    bins=10,
    edgecolor="black"
)


ax.set_xlabel("Price (₹)")
ax.set_ylabel("Number of Laptops")
ax.set_title("Laptop Price Distribution")


st.pyplot(fig)


# ==========================================
# Storage Analysis
# ==========================================

st.markdown("---")

st.subheader("💾 Storage Analysis")


storage = filtered_df["Storage"].value_counts()


fig, ax = plt.subplots(figsize=(8, 4))


ax.bar(
    storage.index,
    storage.values
)


ax.set_xlabel("Storage")
ax.set_ylabel("Number of Laptops")
ax.set_title("Storage Distribution")


plt.xticks(rotation=25)

st.pyplot(fig)


# ==========================================
# Rating Distribution
# ==========================================

st.markdown("---")

st.subheader("⭐ Rating Distribution")


fig, ax = plt.subplots(figsize=(8, 4))


ax.hist(
    filtered_df["Rating"],
    bins=7,
    edgecolor="black"
)


ax.set_xlabel("Rating")
ax.set_ylabel("Number of Laptops")
ax.set_title("Laptop Rating Distribution")


st.pyplot(fig)


# ==========================================
# Laptop Count by Brand
# ==========================================

st.markdown("---")

st.subheader("🏆 Laptop Count by Brand")


brand_count = (
    filtered_df["Brand"]
    .value_counts()
)


fig, ax = plt.subplots(figsize=(9, 4))


ax.bar(
    brand_count.index,
    brand_count.values
)


ax.set_xlabel("Brand")
ax.set_ylabel("Number of Laptops")
ax.set_title("Laptop Count by Brand")


plt.xticks(rotation=30)

st.pyplot(fig)


# ==========================================
# Filtered Laptop Data
# ==========================================

st.markdown("---")

st.subheader("📋 Filtered Laptop Data")


st.dataframe(
    filtered_df,
    use_container_width=True,
    height=350
)


# ==========================================
# Footer
# ==========================================

st.markdown("---")

st.markdown("""
<p style='text-align:center; color:gray;'>
Laptop Market Analysis Project |
Python • NumPy • Pandas • Matplotlib • Streamlit
</p>
""", unsafe_allow_html=True)