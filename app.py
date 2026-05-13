import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import date

# Page Settings
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="centered"
)

# Title
st.title("Daily Expense Tracker")

# Sidebar
st.sidebar.header("Expense Tracker Menu")

# File Name
FILE_NAME = "expenses.csv"

# Load old data
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    # Add missing columns if not present
    if "Subcategory" not in df.columns:
        df["Subcategory"] = ""

    if "Date" not in df.columns:
        df["Date"] = ""

else:
    df = pd.DataFrame(
        columns=[
            "Expense",
            "Amount",
            "Category",
            "Subcategory",
            "Date"
        ]
    )

# User Inputs
expense_name = st.text_input("Enter Expense Name")

amount = st.number_input(
    "Enter Amount",
    min_value=0
)

category = st.selectbox(
    "Select Category",
    ["Food", "Travel", "Shopping", "Bills", "Books", "Other"]
)

# Subcategory
subcategory = st.text_input("Enter Subcategory")

# Date
expense_date = st.date_input(
    "Select Date",
    date.today()
)

# Add Expense Button
if st.button("Add Expense"):

    new_expense = pd.DataFrame([{
        "Expense": expense_name,
        "Amount": amount,
        "Category": category,
        "Subcategory": subcategory,
        "Date": expense_date
    }])

    # Add data
    df = pd.concat([df, new_expense], ignore_index=True)

    # Save CSV
    df.to_csv(FILE_NAME, index=False)

    st.success("Expense Added Successfully!")

# Show data
if not df.empty:

    # Total Expense
    total_expense = df["Amount"].sum()

    st.metric("Total Expenses", f"₹{total_expense}")

    # Table
    st.subheader("All Expenses")
    st.dataframe(df)

    # Pie Chart
    st.subheader("Expense Distribution")

    category_total = df.groupby("Category")["Amount"].sum()

    fig, ax = plt.subplots()

    ax.pie(
        category_total,
        labels=category_total.index,
        autopct='%1.1f%%'
    )

    st.pyplot(fig)

    # Category Bar Chart
    st.subheader("Category Comparison")

    category_bar = df.groupby("Category")["Amount"].sum()

    st.bar_chart(category_bar)

    # Subcategory Bar Chart
    st.subheader("Subcategory Comparison")

    subcategory_bar = df.groupby("Subcategory")["Amount"].sum()

    st.bar_chart(subcategory_bar)
