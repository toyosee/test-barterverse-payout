import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load variables from your local .env file
load_dotenv()

# Fetch environment variables
PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")
# Good practice to default the URL if it's missing from your .env file
PAYSTACK_INITIALIZE_URL = os.getenv("PAYSTACK_INITIALIZE_URL")

st.set_page_config(page_title="Custom Paystack Portal", page_icon="💳")
st.title("Custom Checkout Portal")
st.caption("Environment: Paystack Sandbox / Test Mode")

# User Inputs (Fixed spelling typo: custumor_name -> customer_name)
customer_name = st.text_input("Customer Name", placeholder="Elijah Abolaji")
email = st.text_input("Customer Email Address", placeholder="user@example.com")
amount = st.number_input("Payment Amount", min_value=100, step=50, help="Amount in your local currency")

if st.button("Generate Payment Link", type="primary"):
    # Fixed conditional check to ensure BOTH fields are filled out properly
    if not email or not customer_name or amount <= 0:
        st.error("Please provide a valid name, email address, and payment amount.")
    elif not PAYSTACK_SECRET_KEY:
        st.error("Unexpected error. Please contact administrator")
    else:
        # Paystack expects amounts in the lowest currency unit (e.g., Kobo/Cents)
        amount_in_kobo = int(amount * 100)
        
        headers = {
            "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        
        # FIXED PAYLOAD STRUCTURE: Moved the name into metadata so Paystack parses it
        payload = {
            "email": email,
            "amount": amount_in_kobo,
            "metadata": {
                "custom_fields": [
                    {
                        "display_name": "Customer Name",
                        "variable_name": "customer_name",
                        "value": customer_name
                    }
                ]
            }
        }
        
        with st.spinner("Initializing transaction framework..."):
            try:
                response = requests.post(PAYSTACK_INITIALIZE_URL, json=payload, headers=headers)
                response_data = response.json()
                
                if response_data.get("status"):
                    checkout_url = response_data["data"]["authorization_url"]
                    reference = response_data["data"]["reference"]
                    
                    st.success(f"Transaction Initialized! Reference ID: `{reference}`")
                    st.markdown(f'''
                        <a href="{checkout_url}" target="_blank">
                            <button style="
                                background-color: #38A169;
                                color: white;
                                padding: 10px 20px;
                                border: none;
                                border-radius: 5px;
                                cursor: pointer;
                                font-size: 16px;">
                                Click Here to Complete Test Payment 💳
                            </button>
                        </a>
                    ''', unsafe_allow_html=True)
                else:
                    st.error(f"Paystack Error: {response_data.get('message')}")
            except Exception as e:
                st.error(f"An infrastructure connection error occurred: {e}")
