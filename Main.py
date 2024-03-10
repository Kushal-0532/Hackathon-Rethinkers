import streamlit as st
import pandas as pd
from datetime import date, timedelta
import os

import openai
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

openai.api_key = "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"
os.environ.get("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")
loan_history_prompt = PromptTemplate(
    input_variables=["loan_data"],
    template="""
You are a financial assistant analyzing a user's loan history:

{loan_data}

Based on the information provided, respond according to these pointers regarding the loan history (Use only one font for your complete response):
- The total number of loans the user has 
- The total amount borrowed across all loans 
- The total remaining balance to be paid off 
- Any loans that are past their due date or have been fully repaid
- Suggestions for better managing their loan repayments or consolidating loans (if applicable)

Respond in a helpful manner, providing clear and actionable recommendations. You are to only give your response in one paragraph only (no LaTeX)
""",
)

credit_score_prompt = PromptTemplate(
    input_variables=["loan_data"],
    template="""
You are a financial assistant analyzing a user's loan history:

{loan_data}

Based on the information provided, respond according to this pointer regarding the loan history (Use only one font for your complete response):
- Calculate whatever the approximate FICO score can be. Ignore any values for which you have not been provided data

""",
)
llm = OpenAI(temperature=0.7, openai_api_key="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")
chain = LLMChain(llm=llm, prompt=loan_history_prompt)
chain1 = LLMChain(llm=llm, prompt=credit_score_prompt)

LOANS = []
CREDIT_SCORES = [
    {'score': 720, 'date': date(2023, 1, 1)},
    {'score': 735, 'date': date(2023, 2, 1)},
    {'score': 745, 'date': date(2023, 3, 1)}
]

def get_new_loan_entry():
    st.header("Add New Loan")
    loan_name = st.text_input("Loan Name")
    amount = st.number_input("Amount Borrowed", step=1000)
    interest_rate = st.number_input("Interest Rate", step=0.01)
    start_date = st.date_input("Start Date")
    term_months = st.number_input("Term (in months)", step=1)
    payments = []
    if st.button("Add Loan"):
        new_loan = {
            'name': loan_name,
            'amount': amount,
            'interest_rate': interest_rate,
            'start_date': start_date,
            'term_months': term_months,
            'payments': payments
        }
        LOANS.append(new_loan)

def app():
    st.set_page_config(page_title="Loan and Credit Tracker", layout="wide", initial_sidebar_state="collapsed")
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600&family=Open+Sans&display=swap');

            body {
                font-family: 'Open Sans', sans-serif;
                background-color: #F9F9F9;
            }

            h1, h2, h3, h4, h5, h6 {
                font-family: 'Montserrat', sans-serif;
                color: #2C3E50;
            }

            .stButton > button {
                background-color: #2C3E50;
                color: #FFFFFF;
                border-radius: 4px;
                transition: all 0.3s ease;
            }

            .stButton > button:hover {
                background-color: #1ABC9C;
            }

            .stDateInput > div > div > div > input[type="date"],
            .stNumberInput > div > div > div > input[type="number"],
            .stTextInput > div > div > div > input {
                border: 1px solid #D3D3D3;
                border-radius: 4px;
                padding: 8px 12px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("Loan and Credit Tracker")

    get_new_loan_entry()

    show_loan_details()
    show_credit_scores()

def show_loan_details():
    st.header("Loan Management")
    loan_data = []
    for loan in LOANS:
        remaining_amount = loan['amount'] - sum(payment['amount'] for payment in loan['payments'])
        due_date = loan['start_date'] + timedelta(days=loan['term_months'] * 30.4375)
        time_remaining = due_date - date.today()
        is_repaid = remaining_amount == 0

        loan_data.append({
            'Loan Name': loan['name'],
            'Amount Borrowed': loan['amount'],
            'Borrowed On': loan['start_date'],
            'Repayment Due Date': due_date,
            'Time Remaining (days)': time_remaining.days,
            'Loan Status': 'Repaid' if is_repaid else 'Outstanding',
            'Remaining Amount': remaining_amount
        })
    global loan_data_str
    loan_data_str = ""
    for loan in loan_data:
        loan_data_str += f"Loan Name: {loan['Loan Name']}\n"
        loan_data_str += f"Amount Borrowed: {loan['Amount Borrowed']}\n"
        loan_data_str += f"Borrowed On: {loan['Borrowed On']}\n"
        loan_data_str += f"Repayment Due Date: {loan['Repayment Due Date']}\n"
        loan_data_str += f"Time Remaining (days): {loan['Time Remaining (days)']}\n"
        loan_data_str += f"Loan Status: {loan['Loan Status']}\n"
        loan_data_str += f"Remaining Amount: {loan['Remaining Amount']}\n\n"
    
    

    loan_df = pd.DataFrame(loan_data)
    st.dataframe(loan_df,width=5000)

    
    s = st.button("Personalised Analysis")
    if s:
        loan_analysis = chain.run(loan_data=loan_data_str)

        st.write(loan_analysis)

def show_credit_scores():
    st.header("Credit Score Monitoring")
    credit_scores_df = pd.DataFrame(CREDIT_SCORES)
    credit_scores_df = credit_scores_df.rename(columns={0: 'Score', 1: 'Date'})
    st.dataframe(credit_scores_df)
    credit_analysis = chain1.run(loan_data=loan_data_str)
    with st.expander("Credit Score Analysis", expanded=True):
        st.write(credit_analysis)

if __name__ == "__main__":
    app()