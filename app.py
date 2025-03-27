import streamlit as st
import pandas as pd
import altair as alt

# Title of the app
st.title("Pharmacy Sales Dashboard")

# Allow users to upload a CSV file
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)
    st.success("Data loaded successfully!")
    
    # Display the first few rows of the data
    st.subheader("Raw Data")
    st.dataframe(df.head())

    # Sidebar filter for a specific product
    product_filter = st.sidebar.multiselect(
        "Select Products:",
        options=df["Product"].unique(),
        default=df["Product"].unique()
    )

    # Filter the DataFrame based on the selection
    filtered_df = df[df["Product"].isin(product_filter)]
    st.write("Filtered Data", filtered_df)
        
    # --- Data Processing ---
    # Ensure that the Date column is a datetime type
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])

    # Create a Revenue column (assuming Revenue = Quantity * Price)
    if "Quantity" in df.columns and "Price" in df.columns:
        df["Revenue"] = df["Quantity"] * df["Price"]
        total_revenue = df["Revenue"].sum()
        st.metric("Total Revenue", f"${total_revenue:,.2f}")

    # --- Visualization 1: Top Selling Products ---
    if "Product" in df.columns and "Quantity" in df.columns:
        st.subheader("Top Selling Products")
        # Group by Product and sum the quantities sold
        product_sales = df.groupby("Product")["Quantity"].sum().reset_index()
        product_sales = product_sales.sort_values(by="Quantity", ascending=False)
        st.bar_chart(product_sales.set_index("Product"))
    
    # --- Visualization 2: Monthly Sales Trend ---
    if "Date" in df.columns and "Revenue" in df.columns:
        st.subheader("Monthly Sales Trend")
        # Extract month from the Date column
        df["Month"] = df["Date"].dt.to_period("M").astype(str)
        monthly_sales = df.groupby("Month")["Revenue"].sum().reset_index()
        
        # Create a line chart using Altair
        line_chart = alt.Chart(monthly_sales).mark_line(point=True).encode(
            x="Month",
            y="Revenue"
        ).properties(width=700, height=400)
        st.altair_chart(line_chart, use_container_width=True)
else:
    st.info("Awaiting CSV file upload.")