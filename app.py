import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from db import init_db, get_session, create_sample_data, User, Audit
import hashlib

st.set_page_config(page_title="Mini EBS — Streamlit", layout="wide")
init_db()
create_sample_data()

# helpers
def hash_pw(pw: str):
    return hashlib.sha256(pw.encode()).hexdigest()

def audit_log(session, user_id, action, details=""):
    a = Audit(user_id=user_id, action=action, details=details, created_at=datetime.utcnow())
    session.add(a)
    session.commit()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.page = "home"

# sidebar / auth
with st.sidebar:
    st.markdown("<h2 style='color:#004a99'>Mini Oracle EBS</h2>", unsafe_allow_html=True)
    if not st.session_state.logged_in:
        st.subheader("Sign in")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            session = get_session()
            user = session.query(User).filter_by(username=username).first()
            if user and user.password_hash == hash_pw(password):
                st.session_state.logged_in = True
                st.session_state.user = {"id": user.id, "username": user.username, "role": user.role}
                audit_log(session, user.id, "login", "User logged in")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")
    else:
        st.markdown(f"**Signed in as:** {st.session_state.user['username']}")
        if st.button("Logout"):
            session = get_session()
            audit_log(session, st.session_state.user["id"], "logout", "User logged out")
            st.session_state.logged_in = False
            st.session_state.user = None
            st.experimental_rerun()

# app body
if not st.session_state.logged_in:
    st.markdown(\"\"\"
        <div style="background:#f0f6ff;padding:12px;border-radius:8px">
          <h3>Welcome — Mini Oracle EBS (Streamlit)</h3>
          <p style="color:#555">Sign in to open administration panels, user management and audit trail.</p>
        </div>
    \"\"\", unsafe_allow_html=True)
    st.stop()

# Logged in UI
st.markdown("## Dashboard")
session = get_session()
users_count = session.query(User).count()
recent_audit_count = session.query(Audit).filter(Audit.created_at >= datetime.utcnow() - timedelta(days=1)).count()

c1, c2, c3 = st.columns(3)
c1.metric("Users", users_count)
c2.metric("Active Sessions", 1)
c3.metric("Audit (24h)", recent_audit_count)

st.markdown("---")
st.sidebar.markdown("### Navigation")
nav = st.sidebar.radio("", ["Home", "User Management", "Create User", "Audit Trail", "System Status"])

if nav == "Home":
    st.write("Welcome to the Mini EBS dashboard. Use the sidebar to navigate.")
elif nav == "User Management":
    st.header("User Management")
    q = session.query(User)
    df = pd.DataFrame([{"id":u.id, "username":u.username, "email":u.email, "role":u.role, "created_at":u.created_at} for u in q])
    if df.empty:
        st.info("No users yet.")
    else:
        st.dataframe(df)
    st.markdown("**Actions**")
    sel = st.text_input("Enter username to edit/delete")
    if sel:
        user = session.query(User).filter_by(username=sel).first()
        if user:
            st.write("Found:", user.username, user.email, user.role)
            if st.button("Delete user"):
                session.delete(user); session.commit()
                audit_log(session, st.session_state.user["id"], "delete_user", f"Deleted {sel}")
                st.success("Deleted")
                st.experimental_rerun()
            new_email = st.text_input("New email", value=user.email)
            new_role = st.selectbox("Role", options=["admin","finance","viewer"], index=["admin","finance","viewer"].index(user.role))
            if st.button("Save changes"):
                user.email = new_email; user.role = new_role; session.commit()
                audit_log(session, st.session_state.user["id"], "update_user", f"Updated {sel}")
                st.success("Saved")
        else:
            st.warning("No such user")
elif nav == "Create User":
    st.header("Create User")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["admin","finance","viewer"])
    if st.button("Create"):
        if username and password:
            u = User(username=username, email=email, password_hash=hash_pw(password), role=role)
            session.add(u); session.commit()
            audit_log(session, st.session_state.user["id"], "create_user", f"Created {username}")
            st.success("User created")
        else:
            st.error("Provide username & password")
elif nav == "Audit Trail":
    st.header("Audit Trail (recent)")
    q = session.query(Audit).order_by(Audit.created_at.desc()).limit(200)
    df = pd.DataFrame([{"id":a.id, "user_id":a.user_id, "action":a.action, "details":a.details, "created_at":a.created_at} for a in q])
    st.dataframe(df)
elif nav == "System Status":
    st.header("System Status")
    st.write("Version: R12.2.9 (demo)")
    st.write("Instance: Production (demo)")
    st.write("Uptime: demo")
