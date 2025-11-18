import streamlit as st
import pandas as pd
from datetime import datetime
from rules_engine import predict_rule_based

st.set_page_config(page_title="ITSM Problem Classifier", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = "welcome"
#Welcome Page Allow to shows the information of the student that development the proejct
def go_to_main():
    st.session_state.page = "main"

def go_home():
    st.session_state.page = "welcome"

if st.session_state.page == "welcome":
    st.markdown("""
        <div style='text-align: center; padding: 60px 20px;'>
            <h1 style='color:#2C3E50;'>Rule-Based Problem Classification in IT Service Management</h1>
            <h3 style='color:#16A085;'>A Final Year Project</h3>
            <br>
            <p style='font-size:22px; color:#555;'>
                <b>Student Name:</b> JOHN DOE<br>
                <b>Matric Number:</b> CS/1922<br>
                <b>Supervisor:</b> Me<br>
                <b>Department:</b> NETWORKING AND CLOUD COMPUTING
            </p>
            <br><br>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🚀 Get Started", use_container_width=True):
        go_to_main()

elif st.session_state.page == "main":

    if "ticket_count" not in st.session_state:
        st.session_state.ticket_count = 0
    if "tickets" not in st.session_state:
        st.session_state.tickets = []

    st.title("Rule-Based Problem Classification in IT Service Management")
    st.write("""
    This tool classifies IT problem tickets into categories 
    like **Network**, **Hardware**, **Software**, **Access**, or **Other** 
    based on rule-based logic and automatically generates a **Ticket ID**.
    """)

    st.header("🔍 Classify a Problem Ticket")

    desc = st.text_area(
        "Enter Problem Description:",
        placeholder="e.g., Unable to connect to the office WiFi since morning."
    )
    dept = st.selectbox("Select Department:", ["HR", "Finance", "Engineering", "Sales", "Admin", "Support"])

    if st.button("Classify Ticket"):
        if desc.strip():
            st.session_state.ticket_count += 1
            ticket_id = f"TKT-{st.session_state.ticket_count:03d}"

            pred = predict_rule_based(desc, dept)

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            st.session_state.tickets.append({
                "Ticket ID": ticket_id,
                "Department": dept,
                "Description": desc,
                "Predicted Category": pred,
                "Date/Time": timestamp
            })

            st.success(f"🎟️ **Ticket ID:** {ticket_id}")
            st.info(f"✅ **Predicted Category:** {pred}")
            st.write(f"🕒 *Logged on:* {timestamp}")

        else:
            st.warning("Please enter a problem description first!")

    # Divider
    st.markdown("---")

    st.subheader("🗂️ Submitted Tickets (Session History)")
    if st.session_state.tickets:
        df_history = pd.DataFrame(st.session_state.tickets)
        st.dataframe(df_history)
    else:
        st.write("No tickets have been submitted yet.")

    # Divider
    st.markdown("---")

    st.subheader("📊 Example Tickets and Predictions")

    sample_data = [
        ("Cannot connect to VPN from office", "Engineering"),
        ("Laptop not powering on after update", "Support"),
        ("User account locked after failed login", "HR"),
        ("Printer jammed with error code 32", "Admin"),
        ("Application crashes when saving report", "Finance"),
    ]
    df_samples = pd.DataFrame(sample_data, columns=["Description", "Department"])
    df_samples["Predicted Category"] = df_samples.apply(
        lambda r: predict_rule_based(r["Description"], r["Department"]), axis=1
    )
    st.dataframe(df_samples)

    # Back Button
    st.markdown("---")
    if st.button("🏠 Back to Home", use_container_width=True):
        go_home()

    # Footer
    st.markdown("""
    ---  
    **Project:** Rule-Based Problem Classification in IT Service Management  
    **Supervisor:** Mrs. ADEIFE, O.T  
    """)

