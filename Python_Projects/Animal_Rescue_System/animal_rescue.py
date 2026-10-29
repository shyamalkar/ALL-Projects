import streamlit as st
import streamlit as st
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
import uuid
import pandas as pd


import streamlit as st

import sqlite3, hashlib, uuid
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="Animal Rescue", page_icon="🐾", layout="wide")
BASE = Path(__file__).parent
UPLOADS = BASE / "uploads"
UPLOADS.mkdir(exist_ok=True)
DB = BASE / "animal_rescue.db"

ANIMALS = ["Dog", "Cat", "Cow", "Goat", "Bird", "Monkey", "Horse", "Wild Animal", "Other"]
EMERGENCIES = ["🔴 Critical", "🟠 Serious", "🟡 Moderate", "🟢 Low"]
PROBLEMS = ["Accident / Injury", "Bleeding", "Sick / Weak", "Trapped", "Abandoned",
            "Animal Abuse", "Stray Animal in Danger", "Unable to Walk", "Other"]
STATUSES = ["Report Submitted", "Rescue Team Notified", "Team Assigned",
            "Rescue Team On The Way", "Animal Rescued", "Treatment / Shelter", "Case Closed"]

def connect():
    db = sqlite3.connect(DB, check_same_thread=False)
    db.row_factory = sqlite3.Row
    return db

def query(sql, values=(), one=False):
    with connect() as db:
        cur = db.execute(sql, values)
        return cur.fetchone() if one else cur.fetchall()

def init_db():
    with connect() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL, role TEXT NOT NULL, phone TEXT,
            created_at TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS reports(
            id INTEGER PRIMARY KEY, report_id TEXT UNIQUE NOT NULL,
            username TEXT NOT NULL, phone TEXT, animal_type TEXT NOT NULL,
            emergency_level TEXT NOT NULL, problem_type TEXT NOT NULL,
            description TEXT NOT NULL, image_path TEXT, latitude REAL,
            longitude REAL, location_name TEXT, status TEXT NOT NULL,
            created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
        """)
        if not db.execute("SELECT 1 FROM users WHERE username='admin'").fetchone():
            db.execute("INSERT INTO users VALUES(NULL,?,?,?,?,?)",
                       ("admin", hashlib.sha256(b"admin123").hexdigest(),
                        "admin", "", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

def stamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def password_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register(username, password, phone):
    try:
        with connect() as db:
            db.execute("INSERT INTO users(username,password,role,phone,created_at) VALUES(?,?,?,?,?)",
                       (username, password_hash(password), "user", phone, stamp()))
        return True, "Account created. You can now log in."
    except sqlite3.IntegrityError:
        return False, "That username already exists."

def login(username, password):
    return query("SELECT * FROM users WHERE username=? AND password=?",
                 (username, password_hash(password)), one=True)

def user_reports(username):
    return query("SELECT * FROM reports WHERE username=? ORDER BY id DESC", (username,))

def all_reports():
    return query("SELECT * FROM reports ORDER BY id DESC")

def save_report(data):
    rid = "AR-" + uuid.uuid4().hex[:8].upper()
    now = stamp()
    with connect() as db:
        db.execute("""INSERT INTO reports
        (report_id,username,phone,animal_type,emergency_level,problem_type,
         description,image_path,latitude,longitude,location_name,status,created_at,updated_at)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (rid, data["username"], data["phone"], data["animal"], data["emergency"],
         data["problem"], data["description"], data["image"], data["lat"], data["lon"],
         data["location"], STATUSES[0], now, now))
    return rid

def update_status(rid, status):
    with connect() as db:
        db.execute("UPDATE reports SET status=?, updated_at=? WHERE report_id=?",
                   (status, stamp(), rid))

def show_report(r, admin=False):
    with st.expander(f"{r['report_id']} — {r['animal_type']} — {r['status']}"):
        a, b = st.columns(2)
        with a:
            st.write(f"**Reporter:** {r['username']} · {r['phone'] or 'No phone'}")
            st.write(f"**Emergency:** {r['emergency_level']}")
            st.write(f"**Problem:** {r['problem_type']}")
            st.write(f"**Description:** {r['description']}")
            st.write(f"**Location:** {r['location_name'] or 'Not provided'}")
        with b:
            if r["image_path"] and Path(r["image_path"]).exists():
                st.image(r["image_path"], use_container_width=True)
            st.write(f"**Created:** {r['created_at']}")
            st.write(f"**Status:** {r['status']}")
            if r["latitude"] is not None and r["longitude"] is not None:
                st.link_button("🗺️ Open Google Maps",
                    f"https://www.google.com/maps/search/?api=1&query={r['latitude']},{r['longitude']}")
        if admin:
            idx = STATUSES.index(r["status"]) if r["status"] in STATUSES else 0
            status = st.selectbox("Update rescue status", STATUSES, index=idx, key=f"s_{r['report_id']}")
            if st.button("💾 Update Status", key=f"u_{r['report_id']}"):
                update_status(r["report_id"], status)
                st.success("Status updated.")
                st.rerun()

init_db()
for key, default in {"logged_in": False, "username": None, "role": None}.items():
    if key not in st.session_state:
        st.session_state[key] = default

if not st.session_state.logged_in:
    st.title("🐾 Animal Rescue")
    st.caption("Help an animal in need.")
    tab_login, tab_register = st.tabs(["🔐 Login", "📝 Register"])
    with tab_login:
        with st.form("login"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)
        if submit:
            user = login(username.strip(), password)
            if user:
                st.session_state.update(logged_in=True, username=user["username"], role=user["role"])
                st.rerun()
            else:
                st.error("Invalid username or password.")
        st.info("Demo rescue team account: admin / admin123")
    with tab_register:
        with st.form("register"):
            username = st.text_input("Choose username")
            phone = st.text_input("Phone number")
            password = st.text_input("Create password", type="password")
            confirm = st.text_input("Confirm password", type="password")
            submit = st.form_submit_button("Create Account", use_container_width=True)
        if submit:
            if not username.strip() or not phone.strip() or not password:
                st.warning("Username, phone number and password are required.")
            elif password != confirm:
                st.error("Passwords do not match.")
            elif len(password) < 6:
                st.warning("Password must contain at least 6 characters.")
            else:
                ok, message = register(username.strip(), password, phone.strip())
                (st.success if ok else st.error)(message)
    st.stop()

st.sidebar.title("🐾 Animal Rescue")
st.sidebar.write(f"👤 **{st.session_state.username}**")
st.sidebar.success("🚑 Rescue Team" if st.session_state.role == "admin" else "👤 Reporter")
if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.update(logged_in=False, username=None, role=None)
    st.rerun()

if st.session_state.role == "admin":
    st.title("🚑 Rescue Team Dashboard")
    st.caption("Monitor and manage incoming animal rescue reports.")
    reports = all_reports()
    metrics = [len(reports),
               sum(r["emergency_level"] == "🔴 Critical" for r in reports),
               sum(r["status"] == "Animal Rescued" for r in reports),
               sum(r["status"] == "Case Closed" for r in reports)]
    cols = st.columns(4)
    for col, label, value in zip(cols, ["📋 Total Reports", "🔴 Critical", "🐾 Rescued", "✅ Closed"], metrics):
        col.metric(label, value)
    st.divider()
    if reports:
        for report in reports:
            show_report(report, admin=True)
    else:
        st.info("No rescue reports yet.")
else:
    st.title("🐾 Animal Rescue")
    st.subheader("🚨 Report an Animal in Distress")
    st.write("Report an injured, sick, trapped, abandoned or abused animal.")
    user = query("SELECT phone FROM users WHERE username=?", (st.session_state.username,), one=True)
    with st.form("rescue_report", clear_on_submit=False):
        st.subheader("🐾 Animal Information")
        animal = st.selectbox("Animal Type", ANIMALS)
        emergency = st.selectbox("Emergency Level", EMERGENCIES)
        problem = st.selectbox("Problem Type", PROBLEMS)
        description = st.text_area("Describe the situation", height=120)
        st.subheader("📞 Contact Information")
        phone = st.text_input("Phone number", value=user["phone"] or "")
        st.subheader("📷 Evidence / Animal Photo")
        image_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp"])
        if image_file:
            st.image(image_file, caption="Uploaded animal image", use_container_width=True)
        st.subheader("📍 Location")
        st.info("Enter the approximate GPS coordinates of the animal.")
        c1, c2 = st.columns(2)
        lat = c1.number_input("Latitude", -90.0, 90.0, 0.0, format="%.6f")
        lon = c2.number_input("Longitude", -180.0, 180.0, 0.0, format="%.6f")
        location = st.text_input("Location / Area Name", placeholder="Example: Contai, Purba Medinipur")
        submitted = st.form_submit_button("🚨 SUBMIT RESCUE REQUEST", use_container_width=True)

    if submitted:
        if not description.strip():
            st.warning("Please describe the animal's condition.")
        elif not phone.strip():
            st.warning("Please provide a contact phone number.")
        else:
            image_path = ""
            if image_file:
                image_path = str(UPLOADS / f"{uuid.uuid4().hex}_{Path(image_file.name).name}")
                Path(image_path).write_bytes(image_file.getvalue())
            rid = save_report({"username": st.session_state.username, "phone": phone.strip(),
                "animal": animal, "emergency": emergency, "problem": problem,
                "description": description.strip(), "image": image_path, "lat": lat,
                "lon": lon, "location": location.strip()})
            st.success("🎉 Rescue report submitted successfully!")
            st.balloons()
            st.metric("Report ID", rid)
            st.metric("Status", STATUSES[0])
            st.link_button("🗺️ View location on Google Maps",
                f"https://www.google.com/maps/search/?api=1&query={lat},{lon}")

    st.divider()
    st.subheader("📋 My Rescue Reports")
    reports = user_reports(st.session_state.username)
    if not reports:
        st.info("You haven't submitted any rescue reports yet.")
    else:
        for report in reports:
            show_report(report)


