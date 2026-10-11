
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="EduTrack | Student Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f5f7fb;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

section[data-testid="stSidebar"] {
    background: #101c36;
}

section[data-testid="stSidebar"] * {
    color: white;
}

.hero {
    background: linear-gradient(120deg, #142544, #2756a8);
    color: white;
    padding: 28px;
    border-radius: 18px;
    margin-bottom: 24px;
}

.hero h1 {
    color: white;
    font-size: 29px;
    margin: 0;
}

.hero p {
    color: #dce7ff;
    margin-bottom: 0;
}

.metric-card {
    background: white;
    border: 1px solid #e6eaf2;
    border-radius: 15px;
    padding: 20px;
    min-height: 125px;
    overflow-wrap: anywhere;
    box-shadow: 0 3px 12px rgba(20, 37, 68, 0.04);
}

.metric-label {
    color: #65718a;
    font-size: 14px;
    font-weight: 600;
}

.metric-value {
    color: #172644;
    font-size: clamp(21px, 2vw, 30px);
    font-weight: 800;
    margin-top: 10px;
    line-height: 1.3;
}

.section-title {
    color: #172644;
    font-size: 21px;
    font-weight: 750;
    margin-top: 24px;
    margin-bottom: 12px;
}

.profile-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #e6eaf2;
    margin-bottom: 18px;
}

.stButton button {
    border-radius: 10px;
    font-weight: 600;
    min-height: 42px;
}

.stTextInput input {
    border-radius: 10px;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# DEFAULT DATA
# =========================================================
SAMPLE_DATA = pd.DataFrame({
    "USN": [
        "4SJ25CS001", "4SJ25CS002", "4SJ25CS003",
        "4SJ25CS004", "4SJ25CS005", "4SJ25CS006",
        "4SJ25CS007", "4SJ25CS008", "4SJ25CS009",
        "4SJ25CS010"
    ],
    "Name": [
        "Aarav", "Ananya", "Rahul", "Priya", "Arjun",
        "Meera", "Kiran", "Sneha", "Vijay", "Diya"
    ],
    "Classes_Attended": [58, 55, 50, 45, 40, 35, 30, 60, 25, 52],
    "IA1": [92, 85, 72, 60, 48, 38, 90, 95, 55, 78],
    "IA2": [96, 88, 68, 75, 52, 42, 78, 94, 50, 86]
})

DATA_PATH = Path("data/students.csv")

# =========================================================
# SESSION STATE
# =========================================================
if "total_classes" not in st.session_state:
    st.session_state.total_classes = 60

if "student_data" not in st.session_state:
    if DATA_PATH.exists():
        try:
            st.session_state.student_data = pd.read_csv(DATA_PATH)
        except Exception:
            st.session_state.student_data = SAMPLE_DATA.copy()
    else:
        st.session_state.student_data = SAMPLE_DATA.copy()

# =========================================================
# DATA PROCESSING
# Supports IA1 only, IA1 + IA2, and partially entered IA2.
# =========================================================
def prepare_data(raw_df, total_classes):
    df = raw_df.copy()

    required = ["USN", "Name", "Classes_Attended", "IA1"]
    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(
            "Missing required columns: " + ", ".join(missing)
        )

    if df.empty:
        raise ValueError("The CSV contains no student records.")

    df["USN"] = df["USN"].astype("string").str.strip()
    df["Name"] = df["Name"].astype("string").str.strip()

    if df["USN"].isna().any() or df["Name"].isna().any():
        raise ValueError("USN and Name cannot be empty.")

    if (df["USN"] == "").any() or (df["Name"] == "").any():
        raise ValueError("USN and Name cannot be empty.")

    if df["USN"].duplicated().any():
        raise ValueError("Duplicate USN values found in the CSV.")

    df["Classes_Attended"] = pd.to_numeric(
        df["Classes_Attended"], errors="coerce"
    )
    df["IA1"] = pd.to_numeric(df["IA1"], errors="coerce")

    if df["Classes_Attended"].isna().any():
        raise ValueError("Classes_Attended must contain valid numbers.")

    if df["IA1"].isna().any():
        raise ValueError("Every student must have a valid IA1 mark.")

    # IA2 is optional. If missing, create an empty column.
    if "IA2" not in df.columns:
        df["IA2"] = float("nan")
    else:
        df["IA2"] = pd.to_numeric(df["IA2"], errors="coerce")

    if total_classes < 1:
        raise ValueError("Total classes must be at least 1.")

    if (df["Classes_Attended"] < 0).any():
        raise ValueError("Classes attended cannot be negative.")

    if (df["Classes_Attended"] > total_classes).any():
        raise ValueError(
            "Classes attended cannot exceed total classes conducted."
        )

    if ((df["IA1"] < 0) | (df["IA1"] > 100)).any():
        raise ValueError("IA1 marks must be between 0 and 100.")

    valid_ia2 = df["IA2"].notna()

    if ((df.loc[valid_ia2, "IA2"] < 0) |
            (df.loc[valid_ia2, "IA2"] > 100)).any():
        raise ValueError("IA2 marks must be between 0 and 100.")

    # Calculate each student's average using available assessments only.
    # IA1 only -> IA1 is the average.
    # IA1 + IA2 -> average of both.
    df["Performance_Score"] = df[["IA1", "IA2"]].mean(
        axis=1, skipna=True
    )

    # Improvement is available only for students who have both marks.
    df["Improvement"] = df["IA2"] - df["IA1"]

    df["Attendance"] = (
        df["Classes_Attended"] / total_classes * 100
    ).round(2)

    df["Grade"] = df["Performance_Score"].apply(
        lambda x: "A" if x >= 85
        else "B" if x >= 70
        else "C" if x >= 55
        else "D"
    )

    df["Rank"] = (
        df["Performance_Score"]
        .rank(method="min", ascending=False)
        .astype(int)
    )

    df["Attendance_Status"] = df["Attendance"].apply(
        lambda x: "Good" if x >= 85
        else "Needs Attention" if x >= 75
        else "Low"
    )

    return df.sort_values("Rank").reset_index(drop=True)


def show_metric(label, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def hero(title, subtitle):
    st.markdown(
        f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def search_students(data, query):
    if not query.strip():
        return data.copy()

    q = query.strip()

    mask = (
        data["Name"].astype(str).str.contains(
            q, case=False, na=False, regex=False
        )
        | data["USN"].astype(str).str.contains(
            q, case=False, na=False, regex=False
        )
    )

    return data[mask].copy()


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("# 🎓 EduTrack")
    st.caption("Student Performance Analytics")
    st.divider()

    page = st.radio(
        "Navigation",
        ["Dashboard", "Student Profile", "Data Upload"]
    )

    st.divider()
    st.caption("Academic Analytics")

# =========================================================
# PROCESS ACTIVE DATA
# =========================================================
try:
    df = prepare_data(
        st.session_state.student_data,
        st.session_state.total_classes
    )
    data_error = None
except Exception as error:
    df = pd.DataFrame()
    data_error = str(error)

# =========================================================
# DASHBOARD
# =========================================================
if page == "Dashboard":
    hero(
        "Student Performance Dashboard",
        "Monitor student marks, attendance, and academic progress."
    )

    if data_error:
        st.error(data_error)
        st.info("Open Data Upload to correct or replace the dataset.")
        st.stop()

    ia2_available = df["IA2"].notna().any()

    total_students = len(df)
    average_marks = df["Performance_Score"].mean()
    average_attendance = df["Attendance"].mean()
    top_student = df.loc[df["Performance_Score"].idxmax()]

    # KPI cards
    cols = st.columns(4, gap="medium")

    with cols[0]:
        show_metric("Total Students", str(total_students))

    with cols[1]:
        show_metric("Class Average Marks", f"{average_marks:.1f} / 100")

    with cols[2]:
        show_metric("Average Attendance", f"{average_attendance:.1f}%")

    with cols[3]:
        show_metric("Top Performer", str(top_student["Name"]))

    # Assessment summary
    st.markdown(
        '<div class="section-title">Academic Overview</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns(2, gap="large")

    with left:
        grade_counts = (
            df["Grade"].value_counts()
            .reindex(["A", "B", "C", "D"], fill_value=0)
            .rename_axis("Grade")
            .reset_index(name="Students")
        )

        fig_grade = px.pie(
            grade_counts,
            names="Grade",
            values="Students",
            hole=0.58,
            title="Grade Distribution"
        )
        fig_grade.update_layout(
            margin=dict(t=55, b=15, l=15, r=15)
        )
        st.plotly_chart(fig_grade, use_container_width=True)

    with right:
        assessment_names = ["IA1"]
        assessment_averages = [df["IA1"].mean()]

        if ia2_available:
            assessment_names.append("IA2")
            assessment_averages.append(df["IA2"].mean())

        assessment_summary = pd.DataFrame({
            "Assessment": assessment_names,
            "Average Marks": assessment_averages
        })

        fig_marks = px.line(
            assessment_summary,
            x="Assessment",
            y="Average Marks",
            markers=True,
            title="Average Marks by Assessment"
        )
        fig_marks.update_yaxes(range=[0, 100])
        fig_marks.update_layout(
            margin=dict(t=55, b=15, l=15, r=15),
            yaxis_title="Average Marks"
        )
        st.plotly_chart(fig_marks, use_container_width=True)

    # Searchable student table
    st.markdown(
        '<div class="section-title">Search Students</div>',
        unsafe_allow_html=True
    )

    search_query = st.text_input(
        "Search by student name or USN",
        placeholder="Type a name or USN...",
        key="dashboard_search"
    )

    filtered_df = search_students(df, search_query)

    st.caption(f"Showing {len(filtered_df)} of {len(df)} students")

    display_columns = [
        "Rank", "USN", "Name", "Classes_Attended",
        "Attendance", "IA1", "Performance_Score", "Grade"
    ]

    if ia2_available:
        display_columns.extend(["IA2", "Improvement"])

    table_df = filtered_df[display_columns].rename(columns={
        "Classes_Attended": "Classes Attended",
        "Attendance": "Attendance (%)",
        "Performance_Score": "Average Marks",
        "Improvement": "IA Improvement"
    })

    st.dataframe(
        table_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Attendance (%)": st.column_config.NumberColumn(
                format="%.1f%%"
            ),
            "Average Marks": st.column_config.NumberColumn(
                format="%.1f"
            ),
            "IA Improvement": st.column_config.NumberColumn(
                format="%+.1f"
            )
        }
    )

    if filtered_df.empty:
        st.info("No matching students found.")

    st.download_button(
        "Download Student Report CSV",
        data=filtered_df.to_csv(index=False).encode("utf-8"),
        file_name="edutrack_student_report.csv",
        mime="text/csv"
    )

    # Support lists
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("### Attendance Follow-up")
        low_attendance = df[df["Attendance"] < 75].sort_values(
            "Attendance"
        )

        if low_attendance.empty:
            st.success("No students below 75% attendance.")
        else:
            st.dataframe(
                low_attendance[["USN", "Name", "Attendance"]].rename(
                    columns={"Attendance": "Attendance (%)"}
                ),
                use_container_width=True,
                hide_index=True
            )

    with col2:
        st.markdown("### Students Needing Academic Support")
        low_marks = df[df["Performance_Score"] < 55].sort_values(
            "Performance_Score"
        )

        if low_marks.empty:
            st.success("No students below 55 average marks.")
        else:
            st.dataframe(
                low_marks[["USN", "Name", "Performance_Score", "Grade"]].rename(
                    columns={"Performance_Score": "Average Marks"}
                ),
                use_container_width=True,
                hide_index=True
            )

# =========================================================
# STUDENT PROFILE
# =========================================================
elif page == "Student Profile":
    hero(
        "Student Profile",
        "View individual marks, academic progress, and attendance."
    )

    if data_error:
        st.error(data_error)
        st.stop()

    profile_query = st.text_input(
        "Search student by name or USN",
        placeholder="Type a name or USN...",
        key="profile_search"
    )

    matching = search_students(df, profile_query)

    if matching.empty:
        st.warning("No matching students found.")
        st.stop()

    selected_usn = st.selectbox(
        "Select Student",
        matching["USN"].tolist(),
        format_func=lambda usn: (
            f"{matching.loc[matching['USN'] == usn, 'Name'].iloc[0]} ({usn})"
        )
    )

    student = df[df["USN"] == selected_usn].iloc[0]
    ia2_available_for_student = pd.notna(student["IA2"])

    st.markdown('<div class="profile-card">', unsafe_allow_html=True)
    st.subheader(f"🎓 {student['Name']}")
    st.write(f"**USN:** {student['USN']}")
    st.write(f"**Rank:** {student['Rank']} of {len(df)}")
    st.markdown("</div>", unsafe_allow_html=True)

    cols = st.columns(4, gap="medium")

    with cols[0]:
        show_metric("Average Marks", f"{student['Performance_Score']:.1f}/100")

    with cols[1]:
        show_metric("Attendance", f"{student['Attendance']:.1f}%")

    with cols[2]:
        show_metric("Grade", student["Grade"])

    with cols[3]:
        value = (
            f"{student['Improvement']:+.1f}"
            if ia2_available_for_student else "Not available"
        )
        show_metric("IA Improvement", value)

    left, right = st.columns(2, gap="large")

    with left:
        student_assessments = {"Assessment": ["IA1"], "Marks": [student["IA1"]]}

        if ia2_available_for_student:
            student_assessments["Assessment"].append("IA2")
            student_assessments["Marks"].append(student["IA2"])

        marks_data = pd.DataFrame(student_assessments)

        fig = px.line(
            marks_data,
            x="Assessment",
            y="Marks",
            markers=True,
            title="Student Assessment Marks"
        )
        fig.update_yaxes(range=[0, 100])
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("### Attendance Details")
        st.progress(min(float(student["Attendance"]) / 100, 1.0))

        st.write(f"**Attendance:** {student['Attendance']:.1f}%")
        st.write(
            f"**Classes attended:** {student['Classes_Attended']} / "
            f"{st.session_state.total_classes}"
        )

        if student["Attendance"] >= 85:
            st.success("Good attendance")
        elif student["Attendance"] >= 75:
            st.info("Attendance needs attention")
        else:
            st.warning("Low attendance")

    st.markdown("### Academic Feedback")

    if student["Performance_Score"] >= 85:
        st.success("Excellent performance. Keep it up!")
    elif student["Performance_Score"] >= 70:
        st.info("Good performance. Keep revising regularly.")
    elif student["Performance_Score"] >= 55:
        st.warning("Focus on topics where marks were lost.")
    else:
        st.error("A focused study plan and academic support are recommended.")

    if ia2_available_for_student:
        if student["Improvement"] > 0:
            st.success(
                f"IA2 marks improved by {student['Improvement']:.1f}."
            )
        elif student["Improvement"] < 0:
            st.warning(
                f"IA2 marks decreased by {abs(student['Improvement']):.1f}."
            )
        else:
            st.info("IA1 and IA2 marks are the same.")

# =========================================================
# DATA UPLOAD
# =========================================================
elif page == "Data Upload":
    hero(
        "Data Management",
        "Upload student records and set total classes conducted."
    )

    st.markdown("### Step 1 — Upload Student CSV")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="Required: USN, Name, Classes_Attended, IA1. IA2 is optional."
    )

    uploaded_df = None

    if uploaded_file is not None:
        try:
            uploaded_df = pd.read_csv(uploaded_file)

            st.success(
                f"CSV loaded successfully: {len(uploaded_df)} student records."
            )

            st.dataframe(
                uploaded_df,
                use_container_width=True,
                hide_index=True
            )

        except Exception as error:
            st.error(f"Could not read the CSV file: {error}")

    st.markdown("### Step 2 — Enter Total Classes")

    total_classes_input = st.number_input(
        "Total classes conducted",
        min_value=1,
        max_value=500,
        value=int(st.session_state.total_classes),
        step=1
    )

    st.caption(
        "The app uses this number to calculate every student's attendance."
    )

    apply_col, reset_col = st.columns(2, gap="medium")

    with apply_col:
        if st.button(
            "Apply Dataset & Settings",
            type="primary",
            use_container_width=True
        ):
            if uploaded_file is None or uploaded_df is None:
                st.warning("Upload a valid CSV file before applying.")
            else:
                try:
                    # Validate the entire dataset before changing active data.
                    prepare_data(uploaded_df, int(total_classes_input))

                    st.session_state.student_data = uploaded_df.copy()
                    st.session_state.total_classes = int(total_classes_input)

                    st.success("Dataset and settings applied successfully!")
                    st.rerun()

                except Exception as error:
                    st.error(f"Could not apply dataset: {error}")

    with reset_col:
        if st.button(
            "Reset Default Dataset",
            use_container_width=True
        ):
            st.session_state.student_data = SAMPLE_DATA.copy()
            st.session_state.total_classes = 60
            st.success("Default dataset restored.")
            st.rerun()

    st.divider()
    st.markdown("### CSV Format")

    st.write(
        "IA1 is required. IA2 is optional: either omit the IA2 column "
        "or leave marks blank until they are available."
    )

    st.code(
        "USN,Name,Classes_Attended,IA1\n"
        "4SJ25CS001,Aarav,58,92\n"
        "4SJ25CS002,Ananya,55,85",
        language="csv"
    )

    st.download_button(
        "Download IA1-Only CSV Template",
        data=SAMPLE_DATA[[
            "USN", "Name", "Classes_Attended", "IA1"
        ]].to_csv(index=False).encode("utf-8"),
        file_name="student_ia1_template.csv",
        mime="text/csv"
    )

    st.download_button(
        "Download IA1 + IA2 CSV Template",
        data=SAMPLE_DATA.to_csv(index=False).encode("utf-8"),
        file_name="student_ia1_ia2_template.csv",
        mime="text/csv"
    )

# =========================================================
# FOOTER
# =========================================================
st.divider()
st.caption("EduTrack • Student Performance Analytics")
