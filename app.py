import streamlit as st
from pdf_parser import parse_bank_statement
import pandas as pd

st.set_page_config(page_title="Loan Eligibility App", layout="centered")
st.title("📄 Loan Eligibility Checker")

uploaded_file = st.file_uploader("Upload your bank statement (PDF)", type="pdf")

if uploaded_file:
    df = parse_bank_statement(uploaded_file)

    if df.empty:
        st.warning("No transactions found in the uploaded PDF.")
    else:
        st.subheader("🔍 Extracted Transactions")
        st.dataframe(df.head(10))

        # Calculate financial summary
        total_income = df[df["net"] > 0]["net"].sum()
        total_expenses = df[df["net"] < 0]["net"].sum()
        balance = df["net"].sum()

        # Estimate number of months from unique months in date column
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        months = df["date"].dt.to_period("M").nunique()
        monthly_income = total_income / months if months else total_income

        st.subheader("📊 Financial Summary")
        col1, col2 = st.columns(2)
        col1.metric("Total Income", f"${total_income:,.2f}")
        col2.metric("Total Expenses", f"${abs(total_expenses):,.2f}")
        col1.metric("Net Balance", f"${balance:,.2f}")
        col2.metric("Avg Monthly Income", f"${monthly_income:,.2f}")

        st.subheader("📋 Loan Application")
        with st.form("loan_form"):
            name = st.text_input("Full Name")
            detected_income = st.text_input("Detected Monthly Income", value=f"${monthly_income:,.2f}", disabled=True)
            requested_loan = st.number_input("Requested Loan Amount ($)", min_value=0)
            submit = st.form_submit_button("Check Eligibility")

        if submit:
            if monthly_income > 500 and requested_loan <= monthly_income * 3:
                st.success(f"✅ {name}, you are eligible for the loan!")
            else:
                st.error(f"❌ Sorry {name}, you are not eligible based on your current income.")
else:
    st.info("Please upload a bank statement in PDF format to begin.")
