


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# =============== PAGE CONFIG ===============
st.set_page_config(
    page_title="EduTrack | Student Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============== DESIGN SYSTEM ===============
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #F5F7FB;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111B35, #1B3159);
}

[data-testid="stSidebar"] * {
    color: #FFFFFF;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    padding: 9px 12px;
    border-radius: 10px;
}

.hero {
    background: linear-gradient(115deg, #14284F, #2865D8);
    padding: 30px;
    border-radius: 20px;
    color: white;
    margin-bottom: 24px;
    box-shadow: 0 8px 24px rgba(37, 89, 190, .12);
}

.hero h1 {
    color: white;
    font-size: 29px;
    font-weight: 800;
    margin: 0 0 9px 0;
}

.hero p {
    color: #DFE9FF;
    margin: 0;
    font-size: 14px;
}

.kpi {
    background: #FFFFFF;
    border: 1px solid #E5EAF3;
    border-radius: 16px;
    padding: 20px;
    min-height: 125px;
    box-shadow: 0 5px 18px rgba(22, 40, 75, .04);
}

.kpi-label {
    color: #697891;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: .6px;
}

.kpi-value {
    color: #172747;
    font-size: 27px;
    font-weight: 800;
    margin-top: 12px;
    overflow-wrap: anywhere;
}

.kpi-note {
    color: #16866A;
    font-size: 12px;
    margin-top: 7px;
}

.section-title {
    color: #172747;
    font-size: 20px;
    font-weight: 750;
    margin: 26px 0 12px 0;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #E5EAF3;
    padding: 16px;
    border-radius: 14px;
}

div[data-testid="stDataFrame"] {
    border-radius: 12px;
}

footer, #MainMenu {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# =============== LOAD DATA ===============
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "students.csv"

@st.cache_data
def load_data(path):
    return pd.read_csv(path)

try:
    data = load_data(str(DATA_PATH))
except FileNotFoundError:
    st.error("Dataset not found. Check that data/students.csv exists.")
    st.stop()

required = ["Name", "Attendance", "IA1", "IA2", "Semester"]
missing = [col for col in required if col not in data.columns]

if missing:
    st.error("Missing CSV columns: " + ", ".join(missing))
    st.info("Required: Name, Attendance, IA1, IA2, Semester")
    st.stop()

for col in ["Attendance", "IA1", "IA2", "Semester"]:
    data[col] = pd.to_numeric(data[col], errors="coerce")

data["Name"] = data["Name"].astype("string").str.strip()
data = data.dropna(subset=required)
data = data[data["Name"].ne("")].copy()

if data.empty:
    st.error("No valid student records found in the CSV.")
    st.stop()

# Basic data validation
if not data[["Attendance", "IA1", "IA2", "Semester"]].apply(
    lambda col: col.between(0, 100).all()
).all():
    st.error("Attendance and exam marks must be between 0 and 100.")
    st.stop()

# =============== PERFORMANCE ANALYSIS ===============
# Equal-weight average of three exam scores
data["Performance_Score"] = data[
    ["IA1", "IA2", "Semester"]
].mean(axis=1)

def get_grade(score):
    if score >= 85:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 55:
        return "C"
    return "D"

data["Grade"] = data["Performance_Score"].apply(get_grade)

# Competition ranking: tied scores share a rank
data["Rank"] = data["Performance_Score"].rank(
    ascending=False, method="min"
).astype(int)

ranked = data.sort_values(
    ["Performance_Score", "Name"],
    ascending=[False, True]
).reset_index(drop=True)


# =============== REUSABLE COMPONENTS ===============
def hero(title, subtitle):
    st.markdown(f"""
        <div class="hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
    """, unsafe_allow_html=True)


def kpi(label, value, note):
    st.markdown(f"""
        <div class="kpi">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
    """, unsafe_allow_html=True)


def style_chart(fig, height=340):
    fig.update_layout(
        height=height,
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(family="Inter", color="#34425B"),
        margin=dict(l=18, r=18, t=55, b=18),
        legend=dict(orientation="h", y=1.12),
    )
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(gridcolor="#EDF0F6")
    return fig


# =============== SIDEBAR ===============
with st.sidebar:
    st.markdown("# 🎓 EduTrack")
    st.caption("STUDENT ANALYTICS PLATFORM")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        ["Dashboard", "Student Profile"]
    )

    st.divider()
    st.caption("ACADEMIC OVERVIEW")
    st.markdown(f"👥  **{len(data)} Students**")
    st.markdown("📝  IA1 · IA2 · Semester")
    st.markdown("📊  Academic insights")


# =============== DASHBOARD ===============
if page == "Dashboard":

    hero(
        "Student Performance Dashboard",
        "Monitor exam results, attendance and class performance in one place."
    )

    avg_score = data["Performance_Score"].mean()
    avg_attendance = data["Attendance"].mean()
    top_student = ranked.iloc[0]

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi("TOTAL STUDENTS", str(len(data)), "Students in this dataset")

    with c2:
        kpi("AVERAGE EXAM SCORE", f"{avg_score:.1f}%", "IA1, IA2 and Semester")

    with c3:
        kpi("AVERAGE ATTENDANCE", f"{avg_attendance:.1f}%", "Class attendance")

    with c4:
        kpi(
            "TOP PERFORMER",
            str(top_student["Name"]),
            f"{top_student['Performance_Score']:.1f}% exam average"
        )

    st.markdown(
        '<div class="section-title">📊 Exam Performance Overview</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([1.4, 1])

    with left:
        exam_means = data[["IA1", "IA2", "Semester"]].mean()
        exam_means = exam_means.rename_axis("Exam").reset_index(
            name="Average Marks"
        )

        fig = px.bar(
            exam_means,
            x="Exam",
            y="Average Marks",
            color="Exam",
            text_auto=".1f",
            color_discrete_map={
                "IA1": "#3B82F6",
                "IA2": "#14B8A6",
                "Semester": "#8B5CF6"
            },
            title="Class Average by Exam"
        )
        fig.update_traces(textposition="outside")
        fig.update_yaxes(range=[0, 110], title="Average marks (%)")
        st.plotly_chart(style_chart(fig), use_container_width=True)

    with right:
        grade_counts = (
            data["Grade"]
            .value_counts()
            .reindex(["A", "B", "C", "D"], fill_value=0)
            .rename_axis("Grade")
            .reset_index(name="Students")
        )

        fig = px.pie(
            grade_counts,
            names="Grade",
            values="Students",
            hole=0.68,
            color="Grade",
            color_discrete_map={
                "A": "#14B8A6",
                "B": "#3B82F6",
                "C": "#F59E0B",
                "D": "#EF4444"
            },
            title="Grade Distribution"
        )
        fig.update_traces(textinfo="percent+label")
        st.plotly_chart(style_chart(fig), use_container_width=True)

    st.markdown(
        '<div class="section-title">📈 Compare Student Exam Marks</div>',
        unsafe_allow_html=True
    )

    exam_data = ranked[
        ["Name", "IA1", "IA2", "Semester"]
    ].melt(
        id_vars="Name",
        var_name="Exam",
        value_name="Marks"
    )

    fig = px.bar(
        exam_data,
        x="Name",
        y="Marks",
        color="Exam",
        barmode="group",
        color_discrete_map={
            "IA1": "#3B82F6",
            "IA2": "#14B8A6",
            "Semester": "#8B5CF6"
        }
    )
    fig.update_yaxes(range=[0, 100], title="Marks (%)")
    st.plotly_chart(style_chart(fig, 420), use_container_width=True)

    st.markdown(
        '<div class="section-title">🏆 Class Leaderboard</div>',
        unsafe_allow_html=True
    )

    display = ranked[
        ["Rank", "Name", "IA1", "IA2", "Semester",
         "Performance_Score", "Grade"]
    ].copy()

    display["Performance_Score"] = display["Performance_Score"].round(1)

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn("Rank", format="#%d"),
            "Performance_Score": st.column_config.ProgressColumn(
                "Average Score",
                min_value=0,
                max_value=100,
                format="%.1f%%"
            ),
            "IA1": st.column_config.NumberColumn("IA1", format="%.1f"),
            "IA2": st.column_config.NumberColumn("IA2", format="%.1f"),
            "Semester": st.column_config.NumberColumn(
                "Semester", format="%.1f"
            )
        }
    )


# =============== STUDENT PROFILE ===============
else:

    hero(
        "Student Profile",
        "Explore individual exam results, attendance and academic standing."
    )

    names = sorted(data["Name"].unique())

    selected_name = st.selectbox(
        "🔎 Search or select a student",
        names
    )

    student = data[data["Name"] == selected_name].iloc[0]

    st.markdown(
        '<div class="section-title">👤 Academic Summary</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi(
            "CLASS RANK",
            f"#{int(student['Rank'])}",
            f"Out of {len(data)} students"
        )

    with c2:
        kpi(
            "EXAM AVERAGE",
            f"{student['Performance_Score']:.1f}%",
            "IA1, IA2 and Semester"
        )

    with c3:
        kpi(
            "ATTENDANCE",
            f"{student['Attendance']:.1f}%",
            "Recorded attendance"
        )

    with c4:
        kpi(
            "GRADE",
            str(student["Grade"]),
            "Based on exam average"
        )

    st.markdown(
        '<div class="section-title">🎯 Performance Breakdown</div>',
        unsafe_allow_html=True
    )

    left, right = st.columns([1, 1.5])

    with left:
        score = float(student["Performance_Score"])

        fig = go.Figure(go.Pie(
            values=[score, 100 - score],
            labels=["Achieved", "Remaining"],
            hole=0.78,
            marker_colors=["#3B82F6", "#E8EDF5"],
            textinfo="none",
            sort=False,
            direction="clockwise"
        ))

        fig.add_annotation(
            text=f"<b>{score:.1f}%</b><br><sup>Exam Average</sup>",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=22, color="#172747")
        )

        fig.update_layout(
            title="Overall Performance",
            showlegend=False,
            height=340,
            paper_bgcolor="white",
            margin=dict(l=10, r=10, t=55, b=10)
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:
        exam_results = pd.DataFrame({
            "Exam": ["IA1", "IA2", "Semester"],
            "Marks": [
                student["IA1"],
                student["IA2"],
                student["Semester"]
            ]
        })

        fig = px.bar(
            exam_results,
            x="Exam",
            y="Marks",
            color="Exam",
            text_auto=".1f",
            color_discrete_map={
                "IA1": "#3B82F6",
                "IA2": "#14B8A6",
                "Semester": "#8B5CF6"
            },
            title=f"{student['Name']}'s Exam Results"
        )
        fig.update_traces(textposition="outside")
        fig.update_yaxes(range=[0, 110], title="Marks (%)")
        st.plotly_chart(style_chart(fig, 340), use_container_width=True)

    st.markdown(
        '<div class="section-title">📝 Detailed Exam Results</div>',
        unsafe_allow_html=True
    )

    e1, e2, e3 = st.columns(3)

    with e1:
        st.metric("IA1 Marks", f"{student['IA1']:.1f}%")

    with e2:
        st.metric("IA2 Marks", f"{student['IA2']:.1f}%")

    with e3:
        st.metric("Semester Marks", f"{student['Semester']:.1f}%")

    st.markdown(
        '<div class="section-title">📌 Attendance Status</div>',
        unsafe_allow_html=True
    )

    attendance = float(student["Attendance"])

    st.progress(
        int(attendance),
        text=f"Attendance: {attendance:.1f}%"
    )

    if attendance < 75:
        st.warning(
            "Attendance is below 75%. The student may need follow-up."
        )
    else:
        st.success("Attendance meets the 75% threshold.")

    if student["Performance_Score"] < 55:
        st.warning(
            "The exam average is low. Additional academic support may help."
        )

    st.caption(
        "Scoring note: Exam average is calculated as the simple mean of IA1, "
        "IA2 and Semester marks. Grade thresholds are configurable and should "
        "be aligned with your institution's grading rules."
    )


# =============== FOOTER ===============
st.divider()
st.caption("EduTrack | Student Performance Analytics")
