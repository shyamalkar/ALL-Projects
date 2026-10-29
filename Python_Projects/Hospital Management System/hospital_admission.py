import streamlit as st
import sqlite3
import hashlib
import uuid
from pathlib import Path
from datetime import datetime
import pandas as pd


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Hospital Admission System",
    page_icon="🏥",
    layout="wide"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).parent

DATABASE = BASE_DIR / "hospital.db"

DOCUMENT_DIR = BASE_DIR / "documents"

DOCUMENT_DIR.mkdir(exist_ok=True)


# ============================================================
# CONSTANTS
# ============================================================

DEPARTMENTS = [
    "Emergency",
    "General Medicine",
    "Cardiology",
    "Neurology",
    "Orthopedics",
    "Pediatrics",
    "Gynecology",
    "Dermatology",
    "ENT",
    "Ophthalmology",
    "General Surgery",
    "ICU",
    "Other"
]


ADMISSION_TYPES = [
    "Regular",
    "Emergency",
    "Referral",
    "Transfer",
    "Day Care",
    "Maternity",
    "Surgery"
]


PRIORITIES = [
    "🔴 Critical",
    "🟠 Serious",
    "🟡 Moderate",
    "🟢 Stable"
]


GENDERS = [
    "Male",
    "Female",
    "Other"
]


BLOOD_GROUPS = [
    "Unknown",
    "A+",
    "A-",
    "B+",
    "B-",
    "AB+",
    "AB-",
    "O+",
    "O-"
]


ROOM_TYPES = [
    "General Ward",
    "Semi-Private",
    "Private",
    "ICU",
    "CCU",
    "NICU",
    "Emergency"
]


PAYMENT_METHODS = [
    "Cash",
    "UPI",
    "Card",
    "Bank Transfer",
    "Insurance",
    "Other"
]


ADMISSION_STATUS = [
    "Admitted",
    "Under Observation",
    "Discharged",
    "Cancelled"
]


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    connection = sqlite3.connect(
        DATABASE,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    # --------------------------------------------------------
    # USERS
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            role TEXT NOT NULL,

            created_at TEXT NOT NULL
        )
    """)


    # --------------------------------------------------------
    # PATIENTS
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            patient_id TEXT UNIQUE NOT NULL,

            full_name TEXT NOT NULL,

            dob TEXT,

            age INTEGER,

            gender TEXT,

            blood_group TEXT,

            phone TEXT,

            email TEXT,

            address TEXT,

            city TEXT,

            emergency_contact TEXT,

            emergency_relation TEXT,

            identity_type TEXT,

            identity_number TEXT,

            medical_history TEXT,

            allergies TEXT,

            medications TEXT,

            previous_surgery TEXT,

            family_history TEXT,

            created_at TEXT NOT NULL
        )
    """)


    # --------------------------------------------------------
    # DOCTORS
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            department TEXT NOT NULL,

            phone TEXT,

            available INTEGER DEFAULT 1
        )
    """)


    # --------------------------------------------------------
    # BEDS
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS beds (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            room_number TEXT NOT NULL,

            bed_number TEXT NOT NULL,

            room_type TEXT NOT NULL,

            status TEXT DEFAULT 'Available',

            patient_id TEXT
        )
    """)


    # --------------------------------------------------------
    # ADMISSIONS
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admissions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            admission_id TEXT UNIQUE NOT NULL,

            patient_id TEXT NOT NULL,

            admission_type TEXT,

            priority TEXT,

            department TEXT,

            doctor TEXT,

            bed_id INTEGER,

            reason TEXT,

            symptoms TEXT,

            accident_details TEXT,

            ambulance_required TEXT,

            attendant_name TEXT,

            attendant_relation TEXT,

            attendant_phone TEXT,

            payment_method TEXT,

            insurance_company TEXT,

            policy_number TEXT,

            estimated_deposit REAL,

            deposit_paid REAL,

            payment_status TEXT,

            status TEXT,

            admission_date TEXT,

            discharge_date TEXT,

            created_at TEXT NOT NULL
        )
    """)


    # --------------------------------------------------------
    # DOCUMENTS
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            patient_id TEXT,

            document_type TEXT,

            file_path TEXT,

            uploaded_at TEXT
        )
    """)


    connection.commit()

    connection.close()


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(password):

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# ============================================================
# CREATE DEFAULT ADMIN
# ============================================================

def create_default_admin():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        ("admin",)
    )

    admin = cursor.fetchone()

    if admin is None:

        cursor.execute("""
            INSERT INTO users
            (
                username,
                password,
                role,
                created_at
            )
            VALUES (?, ?, ?, ?)
        """, (
            "admin",
            hash_password("admin123"),
            "admin",
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        ))

    connection.commit()

    connection.close()


# ============================================================
# ADD SAMPLE DOCTORS
# ============================================================

def create_sample_doctors():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) AS count FROM doctors"
    )

    count = cursor.fetchone()["count"]

    if count == 0:

        doctors = [

            ("Dr. Amit Sharma", "General Medicine"),
            ("Dr. Rahul Das", "Cardiology"),
            ("Dr. Priya Sen", "Neurology"),
            ("Dr. Ankit Roy", "Orthopedics"),
            ("Dr. Sneha Ghosh", "Pediatrics"),
            ("Dr. Rina Paul", "Gynecology"),
            ("Dr. Arindam Bose", "General Surgery"),
            ("Dr. S. Kumar", "Emergency"),
            ("Dr. Neha Gupta", "Dermatology"),
            ("Dr. Raj Singh", "Ophthalmology")

        ]

        for name, department in doctors:

            cursor.execute("""
                INSERT INTO doctors
                (
                    name,
                    department,
                    available
                )
                VALUES (?, ?, ?)
            """, (
                name,
                department,
                1
            ))

    connection.commit()

    connection.close()


# ============================================================
# ADD SAMPLE BEDS
# ============================================================

def create_sample_beds():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) AS count FROM beds"
    )

    count = cursor.fetchone()["count"]

    if count == 0:

        beds = []

        # General Ward
        for i in range(1, 11):

            beds.append(
                (
                    "GW-101",
                    f"B-{i:02d}",
                    "General Ward"
                )
            )

        # Semi Private
        for i in range(1, 6):

            beds.append(
                (
                    "SP-201",
                    f"B-{i:02d}",
                    "Semi-Private"
                )
            )

        # Private
        for i in range(1, 6):

            beds.append(
                (
                    "PR-301",
                    f"B-{i:02d}",
                    "Private"
                )
            )

        # ICU
        for i in range(1, 5):

            beds.append(
                (
                    "ICU-401",
                    f"B-{i:02d}",
                    "ICU"
                )
            )

        # Emergency
        for i in range(1, 5):

            beds.append(
                (
                    "ER-501",
                    f"B-{i:02d}",
                    "Emergency"
                )
            )

        for room, bed, room_type in beds:

            cursor.execute("""
                INSERT INTO beds
                (
                    room_number,
                    bed_number,
                    room_type,
                    status
                )
                VALUES (?, ?, ?, ?)
            """, (
                room,
                bed,
                room_type,
                "Available"
            ))

    connection.commit()

    connection.close()


# ============================================================
# REGISTER USER
# ============================================================

def register_user(username, password):

    connection = get_connection()

    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO users
            (
                username,
                password,
                role,
                created_at
            )
            VALUES (?, ?, ?, ?)
        """, (
            username,
            hash_password(password),
            "receptionist",
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        ))

        connection.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        connection.close()


# ============================================================
# LOGIN
# ============================================================

def login_user(username, password):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM users
        WHERE username = ?
        AND password = ?
    """, (
        username,
        hash_password(password)
    ))

    user = cursor.fetchone()

    connection.close()

    if user:

        return dict(user)

    return None


# ============================================================
# CREATE PATIENT
# ============================================================

def create_patient(data):

    connection = get_connection()

    cursor = connection.cursor()

    patient_id = (
        "PAT-"
        + datetime.now().strftime("%Y")
        + "-"
        + uuid.uuid4().hex[:6].upper()
    )

    cursor.execute("""
        INSERT INTO patients
        (
            patient_id,
            full_name,
            dob,
            age,
            gender,
            blood_group,
            phone,
            email,
            address,
            city,
            emergency_contact,
            emergency_relation,
            identity_type,
            identity_number,
            medical_history,
            allergies,
            medications,
            previous_surgery,
            family_history,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        patient_id,
        data["full_name"],
        data["dob"],
        data["age"],
        data["gender"],
        data["blood_group"],
        data["phone"],
        data["email"],
        data["address"],
        data["city"],
        data["emergency_contact"],
        data["emergency_relation"],
        data["identity_type"],
        data["identity_number"],
        data["medical_history"],
        data["allergies"],
        data["medications"],
        data["previous_surgery"],
        data["family_history"],
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))

    connection.commit()

    connection.close()

    return patient_id


# ============================================================
# GET PATIENTS
# ============================================================

def get_patients():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM patients
        ORDER BY id DESC
    """)

    patients = cursor.fetchall()

    connection.close()

    return [dict(p) for p in patients]


# ============================================================
# GET PATIENT
# ============================================================

def get_patient(patient_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM patients
        WHERE patient_id = ?
    """, (
        patient_id,
    ))

    patient = cursor.fetchone()

    connection.close()

    return dict(patient) if patient else None


# ============================================================
# GET DOCTORS
# ============================================================

def get_doctors(department=None):

    connection = get_connection()

    cursor = connection.cursor()

    if department:

        cursor.execute("""
            SELECT *
            FROM doctors
            WHERE department = ?
            AND available = 1
        """, (
            department,
        ))

    else:

        cursor.execute("""
            SELECT *
            FROM doctors
            WHERE available = 1
        """)

    doctors = cursor.fetchall()

    connection.close()

    return [dict(d) for d in doctors]


# ============================================================
# GET AVAILABLE BEDS
# ============================================================

def get_available_beds(room_type=None):

    connection = get_connection()

    cursor = connection.cursor()

    if room_type:

        cursor.execute("""
            SELECT *
            FROM beds
            WHERE status = 'Available'
            AND room_type = ?
        """, (
            room_type,
        ))

    else:

        cursor.execute("""
            SELECT *
            FROM beds
            WHERE status = 'Available'
        """)

    beds = cursor.fetchall()

    connection.close()

    return [dict(b) for b in beds]


# ============================================================
# CREATE ADMISSION
# ============================================================

def create_admission(data):

    connection = get_connection()

    cursor = connection.cursor()

    admission_id = (
        "ADM-"
        + datetime.now().strftime("%Y")
        + "-"
        + uuid.uuid4().hex[:6].upper()
    )

    admission_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO admissions
        (
            admission_id,
            patient_id,
            admission_type,
            priority,
            department,
            doctor,
            bed_id,
            reason,
            symptoms,
            accident_details,
            ambulance_required,
            attendant_name,
            attendant_relation,
            attendant_phone,
            payment_method,
            insurance_company,
            policy_number,
            estimated_deposit,
            deposit_paid,
            payment_status,
            status,
            admission_date,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        admission_id,
        data["patient_id"],
        data["admission_type"],
        data["priority"],
        data["department"],
        data["doctor"],
        data["bed_id"],
        data["reason"],
        data["symptoms"],
        data["accident_details"],
        data["ambulance_required"],
        data["attendant_name"],
        data["attendant_relation"],
        data["attendant_phone"],
        data["payment_method"],
        data["insurance_company"],
        data["policy_number"],
        data["estimated_deposit"],
        data["deposit_paid"],
        data["payment_status"],
        "Admitted",
        admission_date,
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))

    # Mark bed occupied

    cursor.execute("""
        UPDATE beds
        SET status = 'Occupied',
            patient_id = ?
        WHERE id = ?
    """, (
        data["patient_id"],
        data["bed_id"]
    ))

    connection.commit()

    connection.close()

    return admission_id


# ============================================================
# GET ADMISSIONS
# ============================================================

def get_admissions():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            a.*,
            p.full_name,
            b.room_number,
            b.bed_number,
            b.room_type

        FROM admissions a

        LEFT JOIN patients p
        ON a.patient_id = p.patient_id

        LEFT JOIN beds b
        ON a.bed_id = b.id

        ORDER BY a.id DESC
    """)

    admissions = cursor.fetchall()

    connection.close()

    return [dict(a) for a in admissions]


# ============================================================
# DISCHARGE PATIENT
# ============================================================

def discharge_patient(admission_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT bed_id
        FROM admissions
        WHERE admission_id = ?
    """, (
        admission_id,
    ))

    admission = cursor.fetchone()

    if admission:

        bed_id = admission["bed_id"]

        cursor.execute("""
            UPDATE admissions

            SET status = 'Discharged',
                discharge_date = ?

            WHERE admission_id = ?
        """, (
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            admission_id
        ))

        cursor.execute("""
            UPDATE beds

            SET status = 'Available',
                patient_id = NULL

            WHERE id = ?
        """, (
            bed_id,
        ))

        connection.commit()

    connection.close()


# ============================================================
# INITIALIZE
# ============================================================

initialize_database()

create_default_admin()

create_sample_doctors()

create_sample_beds()


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if "username" not in st.session_state:

    st.session_state.username = None


if "role" not in st.session_state:

    st.session_state.role = None


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in:

    st.title("🏥 Hospital Admission System")

    st.caption(
        "Patient Registration & Admission Management"
    )

    login_tab, register_tab = st.tabs(
        [
            "🔐 Login",
            "📝 Register"
        ]
    )


    # ========================================================
    # LOGIN
    # ========================================================

    with login_tab:

        st.subheader("🔐 Login")

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            use_container_width=True
        ):

            if not username or not password:

                st.warning(
                    "Enter username and password."
                )

            else:

                user = login_user(
                    username,
                    password
                )

                if user:

                    st.session_state.logged_in = True

                    st.session_state.username = (
                        user["username"]
                    )

                    st.session_state.role = (
                        user["role"]
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid username or password."
                    )

        st.info(
            "Demo Admin: **admin** / **admin123**"
        )


    # ========================================================
    # REGISTER
    # ========================================================

    with register_tab:

        st.subheader("📝 Create Account")

        new_username = st.text_input(
            "Username"
        )

        new_password = st.text_input(
            "Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        if st.button(
            "Create Account",
            use_container_width=True
        ):

            if not new_username or not new_password:

                st.warning(
                    "All fields are required."
                )

            elif new_password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            elif len(new_password) < 6:

                st.warning(
                    "Password must contain "
                    "at least 6 characters."
                )

            else:

                result = register_user(
                    new_username,
                    new_password
                )

                if result:

                    st.success(
                        "Account created successfully."
                    )

                else:

                    st.error(
                        "Username already exists."
                    )


    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🏥 Hospital System")

st.sidebar.write(
    f"👤 {st.session_state.username}"
)

st.sidebar.write(
    f"Role: **{st.session_state.role}**"
)


if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True
):

    st.session_state.logged_in = False

    st.session_state.username = None

    st.session_state.role = None

    st.rerun()


# ============================================================
# MAIN APPLICATION
# ============================================================

st.title("🏥 Hospital Admission System")


menu = st.sidebar.radio(
    "Navigation",
    [
        "📊 Dashboard",
        "👤 Register Patient",
        "🏥 New Admission",
        "🔎 Patient Search",
        "🛏️ Bed Management",
        "📋 Admission Records"
    ]
)


# ============================================================
# DASHBOARD
# ============================================================

if menu == "📊 Dashboard":

    st.header("📊 Hospital Dashboard")


    patients = get_patients()

    admissions = get_admissions()

    available_beds = get_available_beds()


    total_patients = len(patients)

    active_admissions = sum(
        1
        for a in admissions
        if a["status"] == "Admitted"
    )

    total_beds = (
        len(available_beds)
        + sum(
            1
            for a in admissions
            if a["status"] == "Admitted"
        )
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "👤 Total Patients",
            total_patients
        )


    with col2:

        st.metric(
            "🏥 Active Admissions",
            active_admissions
        )


    with col3:

        st.metric(
            "🛏️ Available Beds",
            len(available_beds)
        )


    with col4:

        st.metric(
            "🛏️ Total Beds",
            total_beds
        )


    st.divider()


    # --------------------------------------------------------
    # BED SUMMARY
    # --------------------------------------------------------

    st.subheader("🛏️ Bed Summary")


    connection = get_connection()

    bed_df = pd.read_sql_query(
        """
        SELECT
            room_type,
            status,
            COUNT(*) AS count

        FROM beds

        GROUP BY room_type, status
        """,
        connection
    )

    connection.close()


    if not bed_df.empty:

        st.dataframe(
            bed_df,
            use_container_width=True,
            hide_index=True
        )


    st.divider()


    # --------------------------------------------------------
    # RECENT ADMISSIONS
    # --------------------------------------------------------

    st.subheader(
        "📋 Recent Admissions"
    )


    if admissions:

        recent = admissions[:10]

        df = pd.DataFrame(recent)

        columns = [
            "admission_id",
            "full_name",
            "department",
            "doctor",
            "room_number",
            "bed_number",
            "status",
            "admission_date"
        ]

        st.dataframe(
            df[columns],
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No admissions yet."
        )


# ============================================================
# REGISTER PATIENT
# ============================================================

elif menu == "👤 Register Patient":

    st.header("👤 Patient Registration")

    st.write(
        "Enter the patient's basic and medical information."
    )


    with st.form(
        "patient_registration"
    ):

        # ----------------------------------------------------
        # BASIC INFORMATION
        # ----------------------------------------------------

        st.subheader(
            "👤 Basic Information"
        )

        col1, col2 = st.columns(2)

        with col1:

            full_name = st.text_input(
                "Full Name *"
            )

            dob = st.date_input(
                "Date of Birth"
            )

            age = st.number_input(
                "Age",
                min_value=0,
                max_value=120,
                value=25
            )

            gender = st.selectbox(
                "Gender",
                GENDERS
            )


        with col2:

            blood_group = st.selectbox(
                "Blood Group",
                BLOOD_GROUPS
            )

            phone = st.text_input(
                "Phone Number *"
            )

            email = st.text_input(
                "Email"
            )


        # ----------------------------------------------------
        # ADDRESS
        # ----------------------------------------------------

        st.subheader(
            "🏠 Address"
        )

        address = st.text_area(
            "Full Address"
        )

        city = st.text_input(
            "City"
        )


        # ----------------------------------------------------
        # EMERGENCY CONTACT
        # ----------------------------------------------------

        st.subheader(
            "📞 Emergency Contact"
        )

        col1, col2 = st.columns(2)

        with col1:

            emergency_contact = st.text_input(
                "Emergency Contact Number"
            )

        with col2:

            emergency_relation = st.text_input(
                "Relationship"
            )


        # ----------------------------------------------------
        # IDENTITY
        # ----------------------------------------------------

        st.subheader(
            "🪪 Identity Information"
        )

        col1, col2 = st.columns(2)

        with col1:

            identity_type = st.selectbox(
                "Identity Type",
                [
                    "Aadhaar",
                    "Passport",
                    "Voter ID",
                    "Driving Licence",
                    "Other"
                ]
            )

        with col2:

            identity_number = st.text_input(
                "Identity Number"
            )


        # ----------------------------------------------------
        # MEDICAL
        # ----------------------------------------------------

        st.subheader(
            "🩺 Medical History"
        )

        medical_history = st.text_area(
            "Existing Medical Conditions"
        )

        allergies = st.text_area(
            "Known Allergies"
        )

        medications = st.text_area(
            "Current Medications"
        )

        previous_surgery = st.text_area(
            "Previous Surgery / Hospitalization"
        )

        family_history = st.text_area(
            "Family Medical History"
        )


        submitted = st.form_submit_button(
            "💾 Register Patient",
            use_container_width=True
        )


    if submitted:

        if not full_name.strip():

            st.error(
                "Patient name is required."
            )

        elif not phone.strip():

            st.error(
                "Phone number is required."
            )

        else:

            patient_data = {

                "full_name": full_name,

                "dob": str(dob),

                "age": age,

                "gender": gender,

                "blood_group": blood_group,

                "phone": phone,

                "email": email,

                "address": address,

                "city": city,

                "emergency_contact": emergency_contact,

                "emergency_relation": emergency_relation,

                "identity_type": identity_type,

                "identity_number": identity_number,

                "medical_history": medical_history,

                "allergies": allergies,

                "medications": medications,

                "previous_surgery": previous_surgery,

                "family_history": family_history
            }


            patient_id = create_patient(
                patient_data
            )


            st.success(
                "✅ Patient registered successfully."
            )


            st.metric(
                "Patient ID",
                patient_id
            )


# ============================================================
# NEW ADMISSION
# ============================================================

elif menu == "🏥 New Admission":

    st.header("🏥 New Patient Admission")


    patients = get_patients()


    if not patients:

        st.warning(
            "Please register a patient first."
        )

        st.stop()


    patient_options = {

        f"{p['patient_id']} — {p['full_name']}":
        p["patient_id"]

        for p in patients
    }


    selected_patient = st.selectbox(
        "Select Patient",
        list(patient_options.keys())
    )


    patient_id = patient_options[
        selected_patient
    ]


    patient = get_patient(
        patient_id
    )


    st.success(
        f"Selected Patient: "
        f"**{patient['full_name']}**"
    )


    st.divider()


    # --------------------------------------------------------
    # ADMISSION INFORMATION
    # --------------------------------------------------------

    st.subheader(
        "🏥 Admission Information"
    )


    admission_type = st.selectbox(
        "Admission Type",
        ADMISSION_TYPES
    )


    priority = st.selectbox(
        "Priority",
        PRIORITIES
    )


    department = st.selectbox(
        "Department",
        DEPARTMENTS
    )


    # --------------------------------------------------------
    # DOCTOR
    # --------------------------------------------------------

    doctors = get_doctors(
        department
    )


    if doctors:

        doctor_options = [
            doctor["name"]
            for doctor in doctors
        ]

        selected_doctor = st.selectbox(
            "👨‍⚕️ Assigned Doctor",
            doctor_options
        )

    else:

        selected_doctor = "No doctor available"

        st.warning(
            "No doctor currently available "
            "for this department."
        )


    # --------------------------------------------------------
    # MEDICAL INFORMATION
    # --------------------------------------------------------

    st.subheader(
        "🚑 Medical / Emergency Information"
    )


    reason = st.text_area(
        "Reason for Admission *"
    )


    symptoms = st.text_area(
        "Current Symptoms"
    )


    accident_details = st.text_area(
        "Accident / Injury Details"
    )


    ambulance_required = st.radio(
        "Ambulance Required?",
        [
            "No",
            "Yes"
        ],
        horizontal=True
    )


    # --------------------------------------------------------
    # BED
    # --------------------------------------------------------

    st.subheader(
        "🛏️ Room & Bed"
    )


    room_type = st.selectbox(
        "Room Type",
        ROOM_TYPES
    )


    available_beds = get_available_beds(
        room_type
    )


    if available_beds:

        bed_options = {

            f"{b['room_number']} | "
            f"{b['bed_number']}":
            b["id"]

            for b in available_beds
        }


        selected_bed = st.selectbox(
            "Available Bed",
            list(bed_options.keys())
        )


        bed_id = bed_options[
            selected_bed
        ]

    else:

        bed_id = None

        st.error(
            "❌ No available beds "
            "in this room category."
        )


    # --------------------------------------------------------
    # ATTENDANT
    # --------------------------------------------------------

    st.subheader(
        "👨‍👩‍👧 Attendant Information"
    )


    col1, col2 = st.columns(2)


    with col1:

        attendant_name = st.text_input(
            "Attendant Name"
        )

        attendant_relation = st.text_input(
            "Relationship"
        )


    with col2:

        attendant_phone = st.text_input(
            "Attendant Phone"
        )


    # --------------------------------------------------------
    # PAYMENT
    # --------------------------------------------------------

    st.subheader(
        "💳 Payment / Insurance"
    )


    payment_method = st.selectbox(
        "Payment Method",
        PAYMENT_METHODS
    )


    col1, col2 = st.columns(2)


    with col1:

        insurance_company = st.text_input(
            "Insurance Company"
        )

        policy_number = st.text_input(
            "Policy Number"
        )


    with col2:

        estimated_deposit = st.number_input(
            "Estimated Deposit (₹)",
            min_value=0.0,
            value=0.0,
            step=1000.0
        )


        deposit_paid = st.number_input(
            "Deposit Paid (₹)",
            min_value=0.0,
            value=0.0,
            step=1000.0
        )


    if deposit_paid >= estimated_deposit:

        payment_status = "Paid"

    elif deposit_paid > 0:

        payment_status = "Partially Paid"

    else:

        payment_status = "Pending"


    st.info(
        f"Payment Status: **{payment_status}**"
    )


    # --------------------------------------------------------
    # DOCUMENT
    # --------------------------------------------------------

    st.subheader(
        "📄 Upload Identity / Medical Document"
    )


    document_type = st.selectbox(
        "Document Type",
        [
            "ID Proof",
            "Insurance Document",
            "Medical Report",
            "Prescription",
            "Referral Letter",
            "Other"
        ]
    )


    uploaded_document = st.file_uploader(
        "Upload Document",
        type=[
            "pdf",
            "jpg",
            "jpeg",
            "png"
        ]
    )


    st.divider()


    # --------------------------------------------------------
    # ADMISSION BUTTON
    # --------------------------------------------------------

    if st.button(
        "🏥 CONFIRM ADMISSION",
        use_container_width=True,
        type="primary"
    ):

        if not reason.strip():

            st.error(
                "Reason for admission is required."
            )

        elif bed_id is None:

            st.error(
                "Please select an available bed."
            )

        else:

            admission_data = {

                "patient_id": patient_id,

                "admission_type": admission_type,

                "priority": priority,

                "department": department,

                "doctor": selected_doctor,

                "bed_id": bed_id,

                "reason": reason,

                "symptoms": symptoms,

                "accident_details": accident_details,

                "ambulance_required": ambulance_required,

                "attendant_name": attendant_name,

                "attendant_relation": attendant_relation,

                "attendant_phone": attendant_phone,

                "payment_method": payment_method,

                "insurance_company": insurance_company,

                "policy_number": policy_number,

                "estimated_deposit": estimated_deposit,

                "deposit_paid": deposit_paid,

                "payment_status": payment_status
            }


            admission_id = create_admission(
                admission_data
            )


            # ------------------------------------------------
            # SAVE DOCUMENT
            # ------------------------------------------------

            if uploaded_document:

                extension = Path(
                    uploaded_document.name
                ).suffix.lower()


                filename = (
                    patient_id
                    + "_"
                    + uuid.uuid4().hex[:8]
                    + extension
                )


                document_path = (
                    DOCUMENT_DIR
                    / filename
                )


                with open(
                    document_path,
                    "wb"
                ) as file:

                    file.write(
                        uploaded_document.getbuffer()
                    )


                connection = get_connection()

                cursor = connection.cursor()

                cursor.execute("""
                    INSERT INTO documents
                    (
                        patient_id,
                        document_type,
                        file_path,
                        uploaded_at
                    )
                    VALUES (?, ?, ?, ?)
                """, (
                    patient_id,
                    document_type,
                    str(document_path),
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                ))

                connection.commit()

                connection.close()


            # ------------------------------------------------
            # SUCCESS
            # ------------------------------------------------

            st.success(
                "🎉 Patient admitted successfully!"
            )

            st.balloons()


            st.divider()


            st.subheader(
                "🧾 Admission Confirmation"
            )


            col1, col2 = st.columns(2)


            with col1:

                st.metric(
                    "Patient ID",
                    patient_id
                )

                st.write(
                    f"**Patient:** "
                    f"{patient['full_name']}"
                )

                st.write(
                    f"**Department:** "
                    f"{department}"
                )

                st.write(
                    f"**Doctor:** "
                    f"{selected_doctor}"
                )


            with col2:

                st.metric(
                    "Admission ID",
                    admission_id
                )

                st.write(
                    f"**Room:** "
                    f"{selected_bed.split('|')[0]}"
                )

                st.write(
                    f"**Bed:** "
                    f"{selected_bed.split('|')[1]}"
                )

                st.write(
                    "**Status:** Admitted"
                )


# ============================================================
# PATIENT SEARCH
# ============================================================

elif menu == "🔎 Patient Search":

    st.header(
        "🔎 Patient Search"
    )


    search = st.text_input(
        "Search by Patient ID, Name or Phone"
    )


    if search:

        connection = get_connection()

        query = """
            SELECT *
            FROM patients
            WHERE patient_id LIKE ?
            OR full_name LIKE ?
            OR phone LIKE ?
        """

        search_value = f"%{search}%"


        patients = connection.execute(
            query,
            (
                search_value,
                search_value,
                search_value
            )
        ).fetchall()


        connection.close()


        if patients:

            for patient in patients:

                with st.expander(
                    f"{patient['patient_id']} — "
                    f"{patient['full_name']}"
                ):

                    col1, col2 = st.columns(2)


                    with col1:

                        st.write(
                            f"**Patient ID:** "
                            f"{patient['patient_id']}"
                        )

                        st.write(
                            f"**Name:** "
                            f"{patient['full_name']}"
                        )

                        st.write(
                            f"**Age:** "
                            f"{patient['age']}"
                        )

                        st.write(
                            f"**Gender:** "
                            f"{patient['gender']}"
                        )

                        st.write(
                            f"**Blood Group:** "
                            f"{patient['blood_group']}"
                        )

                        st.write(
                            f"**Phone:** "
                            f"{patient['phone']}"
                        )


                    with col2:

                        st.write(
                            f"**Medical History:** "
                            f"{patient['medical_history']}"
                        )

                        st.write(
                            f"**Allergies:** "
                            f"{patient['allergies']}"
                        )

                        st.write(
                            f"**Medications:** "
                            f"{patient['medications']}"
                        )

                        st.write(
                            f"**Address:** "
                            f"{patient['address']}"
                        )

        else:

            st.warning(
                "No patient found."
            )


# ============================================================
# BED MANAGEMENT
# ============================================================

elif menu == "🛏️ Bed Management":

    st.header(
        "🛏️ Bed Management"
    )


    connection = get_connection()

    beds = pd.read_sql_query(
        """
        SELECT
            room_number,
            bed_number,
            room_type,
            status,
            patient_id

        FROM beds

        ORDER BY room_type, room_number, bed_number
        """,
        connection
    )

    connection.close()


    if not beds.empty:

        st.dataframe(
            beds,
            use_container_width=True,
            hide_index=True
        )


    st.divider()


    st.subheader(
        "📊 Bed Availability"
    )


    summary = beds.groupby(
        ["room_type", "status"]
    ).size().reset_index(
        name="Beds"
    )


    st.dataframe(
        summary,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# ADMISSION RECORDS
# ============================================================

elif menu == "📋 Admission Records":

    st.header(
        "📋 Admission Records"
    )


    admissions = get_admissions()


    if not admissions:

        st.info(
            "No admission records."
        )

    else:

        df = pd.DataFrame(
            admissions
        )


        display_columns = [

            "admission_id",

            "patient_id",

            "full_name",

            "admission_type",

            "priority",

            "department",

            "doctor",

            "room_number",

            "bed_number",

            "status",

            "admission_date"

        ]


        st.dataframe(
            df[display_columns],
            use_container_width=True,
            hide_index=True
        )


        st.divider()


        st.subheader(
            "🔄 Patient Discharge"
        )


        active_admissions = [

            a for a in admissions

            if a["status"] == "Admitted"
        ]


        if active_admissions:

            admission_options = {

                f"{a['admission_id']} — "
                f"{a['full_name']}":
                a["admission_id"]

                for a in active_admissions
            }


            selected_admission = st.selectbox(
                "Select Patient",
                list(admission_options.keys())
            )


            selected_admission_id = (
                admission_options[
                    selected_admission
                ]
            )


            if st.button(
                "🏠 Discharge Patient",
                type="primary"
            ):

                discharge_patient(
                    selected_admission_id
                )

                st.success(
                    "Patient discharged and "
                    "bed released successfully."
                )

                st.rerun()

        else:

            st.info(
                "No currently admitted patients."
            )