# EduTrack — Student Performance Analyzer

An interactive student analytics dashboard built with Python, Streamlit, Pandas, and Plotly.

## About the Project

EduTrack is a student performance analysis application that organizes academic records and presents them through an interactive dashboard. It helps users explore exam scores, attendance, grade distribution, and student rankings in one place.

This project was developed to practise Python application development, data processing, data visualization, and building a user-friendly interface.

## Features

- **Class Dashboard:** View the number of students, average exam score, average attendance, and top-performing student.
- **Exam Analysis:** Compare average scores across IA1, IA2, and semester exams.
- **Grade Distribution:** Explore the distribution of students across grades A, B, C, and D.
- **Student Comparison:** Compare assessment scores using interactive charts.
- **Student Profiles:** Select a student to view their scores, attendance, grade, and class rank.
- **Attendance Monitoring:** Highlight attendance below the configured 75% threshold.
- **Data Validation:** Check required CSV columns, numeric values, missing records, and score ranges.
- **Leaderboard:** Display students ranked by their calculated average exam score.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and data processing |
| Streamlit | Interactive web application |
| Pandas | Loading, cleaning, and analyzing tabular data |
| Plotly Express | Interactive data visualizations |
| Plotly Graph Objects | Custom performance chart |
| CSV | Sample dataset format |

## How Performance Is Calculated

The application calculates the performance score as the simple average of IA1, IA2, and Semester marks:

**Performance Score = (IA1 + IA2 + Semester) / 3**

The current grade thresholds are:

| Grade | Performance Score |
|---|---:|
| A | 85 and above |
| B | 70 to below 85 |
| C | 55 to below 70 |
| D | Below 55 |

Students are ranked by performance score, with higher scores receiving better ranks. Equal scores share the same rank.

**Note:** These are demonstration rules defined in the code. They should be adjusted to match the institution's official grading policy before real-world use.

## Dataset

The sample dataset is stored at `data/students.csv`.

| Column | Description |
|---|---|
| `Name` | Student name or fictional sample name |
| `Attendance` | Attendance percentage |
| `IA1` | First internal assessment marks |
| `IA2` | Second internal assessment marks |
| `Semester` | Semester examination marks |

The current application expects the attendance and examination values to be between 0 and 100.

## Getting Started

### Prerequisites

- Python installed on your computer
- pip, Python's package installer

### 1. Clone the repository

Replace the placeholder with the repository URL from GitHub.

```bash
git clone <YOUR_REPOSITORY_URL>
cd student-performance-analyzer
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Run the application

```bash
python -m streamlit run frontend.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser to use the application.

## Project Structure

```text
student-performance-analyzer/
├── data/
│   └── students.csv
├── frontend.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Learning Outcomes

Through this project, I am practising:

- Python programming and reusable functions
- Data loading and validation with Pandas
- Interactive data visualization with Plotly
- Building dashboards with Streamlit
- Organizing project files and managing versions with Git and GitHub

## Future Improvements

- Add filters for attendance, grades, and performance.
- Allow users to upload their own CSV datasets safely.
- Add downloadable analysis reports.
- Improve error handling and automated tests.
- Explore machine learning for a clearly defined prediction task after collecting suitable data and evaluating model performance.

## Limitations

- The application uses the data supplied in the CSV file.
- Grade thresholds and attendance rules are configurable demonstration rules, not official academic policies.
- The performance score is a simple average, not a validated prediction of a student's future results.
- The application does not currently use a machine learning model.

## Disclaimer

This project is intended for educational and demonstration purposes. Its outputs should not be used as the sole basis for academic decisions. Only fictional or appropriately anonymized student data should be published in a public repository.

## Author

Computer Science and Engineering student interested in Python, Data Science, Machine Learning, and Generative AI.