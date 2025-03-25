![image](https://github.com/user-attachments/assets/4f9d7cdd-9649-4c0f-95f5-ec8223a6919c)

Recruiting AI Agent

Overview

The Recruiting AI Agent is an AI-powered tool designed to automate the resume screening process, reducing manual effort and improving efficiency in hiring. It analyzes job descriptions and resumes to rank candidates based on predefined assessment criteria.

Data Source

The candidate resumes are sourced from the Resume dataset on Kaggle.

The job description used for assessment is based on a LinkedIn Software Engineer JD template.

Input Requirements

Job Description: A detailed JD outlining the key skills, qualifications, and experience required for the role.

Candidate Resumes: Provided in CSV format or as a folder of text files containing resume data.

Key Functionalities

1. Tailored Assessment Criteria

Extracts and identifies key skills, experience, qualifications, and personality traits required for the position.

Builds a customized assessment rubric or scorecard to weigh each criterion based on its importance to the role.

2. Candidate Evaluation

Parses each candidate’s resume and evaluates them against the predefined criteria.

Assigns scores based on demonstrated skills, experience, and relevance to the role.

3. Candidate Ranking and Selection

Analyzes all candidates and ranks them based on their assessment scores.

Identifies the top 3 candidates who best match the job requirements.

Provides an explanation for the selection, detailing why these candidates were chosen.

How to Use

Upload a job description (TXT format).

Upload candidate resumes (CSV or folder of TXT files).

Click Process Candidates and let the AI do the work.

View a ranked list of top candidates along with detailed insights.

Setup Instructions

Clone the repository:

git clone https://github.com/your-repo/recruiting-ai-agent.git
cd recruiting-ai-agent

Install dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app.py

Future Enhancements

Support for additional resume formats (PDF, DOCX, JSON).

Integration with LinkedIn API for real-time candidate sourcing.

AI-powered recommendation engine for alternative role suggestions.

Contributing

Feel free to submit issues or pull requests to enhance the functionality of the AI agent.


