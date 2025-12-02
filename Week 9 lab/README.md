Week 9 Streamlit App (Demo)
==========================

Files created under: /mnt/data/week9_streamlit_app

How to run (on your computer):
1. Create a virtual environment and activate it (optional but recommended).
2. Install dependencies:
   pip install -r requirements.txt
3. Run:
   streamlit run Home.py

Notes:
- This demo creates a local sqlite DB at DATA/intelligence_platform.db inside the project directory on first run.
- The registration page creates users; passwords are hashed with SHA256 for demo purposes (not production secure).
- The Dashboard and Analytics pages show how Week 8 DB functions are imported and used.
