# Mini Oracle EBS — Streamlit Demo

This is a simplified educational demo that mimics parts of Oracle E-Business Suite R12 (GL / Admin panels) using **Streamlit** and **SQLite**.

## Features
- Login / simple authentication (demo only)
- Dashboard with quick metrics and activity
- User management: create, edit, delete, list
- Audit trail logging for actions
- Simple Oracle-like styling and layout

## Run locally
1. Clone the repository.
2. Create a virtual environment and install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

Default demo users (passwords are simple hashes for demo only):
- admin / admin
- finance_user / 12345
- viewer / 123

> **Note:** This is a learning/demo project — do NOT use as-is in production. Password handling and security are intentionally simplified.
