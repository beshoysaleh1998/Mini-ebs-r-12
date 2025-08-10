import streamlit as st
import sqlite3
from utils.db import init_db, get_users, add_user

# إعداد الصفحة
st.set_page_config(page_title="Oracle EBS R12 (Simplified)", layout="wide")

# تهيئة قاعدة البيانات
init_db()

# الهيدر
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/logo.png", width=80)
with col2:
    st.title("Oracle E-Business Suite R12 (Simplified)")

st.markdown("---")

# تبويبات النظام
tab1, tab2, tab3 = st.tabs(["🏠 Dashboard", "👥 User Management", "📊 Audit Trail"])

# Dashboard
with tab1:
    st.subheader("System Status")
    st.metric("Active Users", len(get_users()))
    st.metric("System Health", "✅ OK")

# User Management
with tab2:
    st.subheader("Add New User")
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    if st.button("Add User"):
        if name and email:
            add_user(name, email)
            st.success(f"User {name} added successfully!")
        else:
            st.error("Please enter all fields.")

    st.subheader("User List")
    users = get_users()
    st.table(users)

# Audit Trail
with tab3:
    st.subheader("Recent Activity")
    st.write("Coming soon...")
