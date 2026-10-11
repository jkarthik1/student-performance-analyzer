# EduTrack — Student Performance Analyzer

An interactive student performance dashboard built using Python 3.13, Streamlit, Pandas, and Plotly.

## Overview

EduTrack is a data-driven web application that helps users analyze student assessment marks and attendance through an interactive dashboard.

The application allows users to upload student datasets, explore class performance, search for individual students, compare internal assessment marks, and identify students who may need academic support.

This project was developed to strengthen practical skills in Python programming, data analysis, data visualization, and web application development.

## Key Features

- **Interactive Dashboard:** Displays total students, class average marks, average attendance, and the top performer.
- **Flexible Dataset Support:** Supports IA1-only datasets and datasets containing both IA1 and IA2.
- **Student Search:** Search student records by name or USN.
- **Student Profiles:** View individual assessment marks, attendance, grade, and rank.
- **Assessment Comparison:** Compare IA1 and IA2 marks when IA2 data is available.
- **Grade Distribution:** Visualize how students are distributed across grade categories.
- **Attendance Monitoring:** Identify students with attendance below the configured 75% threshold.
- **CSV Upload:** Upload a custom dataset and configure the total number of classes.
- **CSV Templates:** Download example templates for IA1-only and IA1 + IA2 datasets.
- **Data Export:** Download processed student analysis as a CSV file.
- **Input Validation:** Validate required columns and check marks and attendance values.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.13 | Application logic and data processing |
| Streamlit | Interactive web application |
| Pandas | Data manipulation and analysis |
| Plotly | Interactive data visualization |
| CSV | Data import and export |
| Git | Version control |
| GitHub | Source code hosting and portfolio |

## How It Works

1. Upload a student dataset in CSV format.
2. Configure the total number of classes.
3. Validate and process the uploaded data.
4. Explore class statistics, student rankings, charts, and attendance.
5. Search for individual students and inspect their profiles.
6. Download the processed analysis when required.

## Performance Calculation

EduTrack calculates a performance score using the available internal assessment marks.

**When only IA1 is available:**

Performance Score = IA1

**When both IA1 and IA2 are available:**

Performance Score = (IA1 + IA2) / 2

When IA2 is available, assessment improvement is calculated as:

Improvement = IA2 − IA1

When IA2 is unavailable, the score uses IA1 alone and assessment improvement is not calculated for that student.

The class average marks are calculated from the student performance scores and are measured out of 100.

### Grade Classification

| Grade | Performance Score |
|---|---:|
| A | 85 and above |
| B | 70 to below 85 |
| C | 55 to below 70 |
| D | Below 55 |

These thresholds are demonstration rules and should be adjusted to match an institution's official grading policy when necessary.

## Dataset Format

The application requires these CSV columns:

| Column | Description |
|---|---|
| `USN` | Unique student identifier |
| `Name` | Student display name |
| `Classes_Attended` | Number of classes attended |
| `IA1` | First internal assessment marks |

The `IA2` column is optional. It can be omitted or contain blank values when second assessment marks are unavailable.

The total number of classes is configured separately in the application.

### Example: IA1-Only Dataset

```csv
USN,Name,Classes_Attended,IA1
STU001,student_01,58,92
STU002,student_02,55,85
STU003,student_03,50,72
```

### Example: IA1 and IA2 Dataset

```csv
USN,Name,Classes_Attended,IA1,IA2
STU001,student_01,58,92,95
STU002,student_02,55,85,82
STU003,student_03,50,72,78
```

These examples use fictional identifiers and names. Never publish real student names, USNs, or identifiable academic records in a public repository.

## Installation and Setup

### Prerequisites

- Python 3.13
- pip
- Git

The application is intended to run in a Python 3.13 environment with the required dependencies installed.

### 1. Clone the Repository

Replace the placeholder with your actual GitHub repository URL.

```bash
git clone <YOUR_REPOSITORY_URL>
cd student-performance-analyzer
```

### 2. Create a Virtual Environment

On Windows:

```bash
py -3.13 -m venv .venv
```

Activate the environment in Command Prompt:

```bash
.venv\Scripts\activate
```

Activate it in Git Bash:

```bash
source .venv/Scripts/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the Application

```bash
python -m streamlit run frontend.py
```

Open the local URL displayed in the terminal to use the application in your browser.

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

The structure above illustrates the main project files. Your actual repository may contain additional modules, charts, or supporting files.

## Skills Demonstrated

- Python programming and application development
- Data manipulation and validation using Pandas
- Interactive dashboard development using Streamlit
- Data visualization using Plotly
- CSV processing and data export
- Basic software project organization
- Git and GitHub version control
- Privacy-conscious use of demonstration data

## Future Improvements

- Add automated tests for calculations and data validation.
- Introduce additional filters for marks, attendance, and grades.
- Improve responsive design and accessibility.
- Generate downloadable class-level reports.
- Explore a suitable machine learning feature with appropriate data and evaluation.

## Limitations

- Results depend on the quality and completeness of uploaded data.
- Grade thresholds are demonstration rules.
- Performance scores summarize available assessment marks; they do not predict future academic results.
- The current application is a data analysis dashboard and does not currently use a machine learning model.

## Privacy and Disclaimer

EduTrack is an educational portfolio project. Use fictional or appropriately anonymized student data in public repositories. Do not publish sensitive academic records or personal information.

The application is intended for demonstration purposes and should not be used as the sole basis for academic decisions.

## Author

Computer Science and Engineering student interested in Python, Data Science, Machine Learning, and Generative AI.
