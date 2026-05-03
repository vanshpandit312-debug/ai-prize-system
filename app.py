import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import random
import matplotlib.pyplot as plt

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Business AI System", page_icon="🚀", layout="centered")
plt.style.use("ggplot")

# ---------------- LOAD MODEL ----------------
base_path = os.path.dirname(__file__)

def load_model():
    try:
        with open(os.path.join(base_path, "model.pkl"), "rb") as f:
            return pickle.load(f)
    except:
        return None

model = load_model()

# ---------------- UI STYLE ----------------
st.markdown("""
<style>
body {
    background-color: #f4f6f9;
}
.title {
    text-align: center;
    font-size: 36px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: gray;
}
.stButton>button {
    width: 100%;
    border-radius: 10px;
    background-color: #28a745;
    color: white;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "login" not in st.session_state:
    st.session_state.login = False

# ---------------- LOGIN ----------------
if not st.session_state.login:

    st.markdown('<div class="title">🔐 Secure Login</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">AI Business Dashboard Access</div>', unsafe_allow_html=True)

    phone = st.text_input("📱 Enter Mobile Number")

    if st.button("Send OTP"):
        otp = random.randint(1000, 9999)
        st.session_state.otp = otp
        st.success(f"Demo OTP: {otp}")

    otp_input = st.text_input("Enter OTP")

    if st.button("Verify"):
        if "otp" in st.session_state and otp_input == str(st.session_state.otp):
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Invalid OTP")

# ---------------- DASHBOARD ----------------
else:

    st.markdown('<div class="title">🚀 Business AI System</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Smart Decision Dashboard</div>', unsafe_allow_html=True)

    st.markdown("---")

    menu = st.selectbox("Select Feature", [
        "💰 Price Optimizer",
        "📈 Sales Predictor",
        "📊 Profit Calculator",
        "📅 Daily Collection",
        "📊 Dashboard Summary"
    ])

    # ---------------- PRICE OPTIMIZER ----------------
    if menu == "💰 Price Optimizer":
        st.subheader("💰 Price Optimization")

        cost = st.number_input("Enter Cost Price", min_value=1)

        if st.button("Calculate Optimal Price"):
            prices = []
            profits = []

            for i in range(1, 11):
                price = cost + i
                profit = (price - cost) * (100 - i*5)
                prices.append(price)
                profits.append(profit)

            best_price = prices[np.argmax(profits)]

            st.success(f"Best Price: ₹{best_price}")

            fig, ax = plt.subplots()
            ax.plot(prices, profits)
            ax.set_title("Profit vs Price")
            ax.set_xlabel("Price")
            ax.set_ylabel("Profit")

            st.pyplot(fig)

    # ---------------- SALES ----------------
    elif menu == "📈 Sales Predictor":
        st.subheader("📈 Sales Prediction")

        if model:
            val = st.number_input("Enter Value")
            if st.button("Predict Sales"):
                result = model.predict([[val]])
                st.success(f"Predicted Sales: {result[0]}")
        else:
            st.warning("Model not available")

        # demo graph
        data = np.random.randint(50, 150, size=10)
        st.line_chart(data)

    # ---------------- PROFIT ----------------
    elif menu == "📊 Profit Calculator":
        st.subheader("📊 Profit Analysis")

        revenue = st.number_input("Revenue")
        expense = st.number_input("Expense")

        if st.button("Calculate Profit"):
            profit = revenue - expense
            st.success(f"Profit: ₹{profit}")

            labels = ["Revenue", "Expense", "Profit"]
            values = [revenue, expense, profit]

            fig, ax = plt.subplots()
            ax.bar(labels, values)
            ax.set_title("Profit Breakdown")

            st.pyplot(fig)

    # ---------------- DAILY ----------------
    elif menu == "📅 Daily Collection":
        st.subheader("📅 Daily Entry")

        amount = st.number_input("Enter Amount")

        if st.button("Save Data"):
            file_path = os.path.join(base_path, "records.csv")

            df = pd.DataFrame({"Amount": [amount]})

            if os.path.exists(file_path):
                df.to_csv(file_path, mode='a', header=False, index=False)
            else:
                df.to_csv(file_path, index=False)

            st.success("Saved Successfully!")

    # ---------------- SUMMARY ----------------
    elif menu == "📊 Dashboard Summary":
        st.subheader("📊 Business Analytics")

        file_path = os.path.join(base_path, "records.csv")

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)

            st.metric("💰 Total Collection", int(df["Amount"].sum()))
            st.metric("📊 Entries", len(df))
            st.metric("📈 Average", int(df["Amount"].mean()))

            st.line_chart(df)
            st.bar_chart(df)
            st.area_chart(df)

        else:
            st.warning("No data available")

    # ---------------- LOGOUT ----------------
    if st.button("🚪 Logout"):
        st.session_state.login = False
        st.rerun()
