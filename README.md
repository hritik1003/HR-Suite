# AI HR Suite

*An AI-powered platform for intelligent resume screening and employee engagement analysis.*

[](https://github.com/hritik1003/unstop/tree/main)
[](https://github.com/hritik1003/unstop/tree/main)
[](https://hrsuite.streamlit.app/)

This project leverages Large Language Models (LLMs) to automate and enhance key HR functions, transforming how companies identify, assess, and retain talent.

-----

## 🚀 Live Demo & Links

[**Live Application**](https://hrsuite.streamlit.app/)   |   [**Video Demo**](https://drive.google.com/file/d/1V9pYORtuQqw4pDeBiA-sNF_DWTcI1m1c/view)   |   [**Presentation**](https://docs.google.com/presentation/d/1ySYjLfQB4ya1bNl4LrsXqVAcC4LMd9XrfgdMrL4kuKk/edit)   |   [**Screenshots**](https://www.google.com/search?q=https://drive.google.com/drive/folders/1wQ7p-d2o0m9XJv_yJ4R_k5yB3zF9l9pE%3Fusp%3Dsharing)

-----

## ✨ Key Features

This HR suite is built around two core modules:

  * **🤖 Resume Screening**: An intelligent assistant that parses resumes, matches candidates to job descriptions, and scores their fit based on skills, experience, and qualifications. It's designed to solve the challenge of manually reviewing high volumes of applications.
  * **❤️‍🩹 Employee Sentiment Analysis**: An analytics pipeline that processes employee feedback (from surveys, exit interviews, etc.) to quantify workforce morale, identify attrition risks, and recommend proactive engagement strategies.

-----

## 🛠️ Tech Stack

  * **Cloud & AI**: Google Gemini API
  * **Framework**: Streamlit
  * **Language**: Python
  * **Libraries**: Optical Character Recognition (OCR) for PDF processing

-----

## ⚙️ AI Pipeline Workflow

### Resume Screening Pipeline

1.  **📄 Upload**: A recruiter uploads candidate resumes (PDFs) and the corresponding job description.
2.  **🧠 LLM Parsing**: The AI pipeline extracts structured metadata (e.g., name, skills, experience) from the unstructured text.
3.  **💯 Job Match Scoring**: The LLM compares the resume data against the job requirements to generate a `match_score` for each candidate.
4.  **📊 Dashboard Output**: The recruiter views a dashboard with a ranked list of candidates, their match scores, and a final recommendation.

### Sentiment Analysis Pipeline

1.  **✍️ Feedback Upload**: Employee feedback, either structured or unstructured, is submitted.
2.  **🔍 Sentiment Analysis**: The Google Gemini API analyzes the feedback to generate a report on risks, themes, and overall sentiment.
3.  **📈 Strategic Report**: The system produces a report with actionable recommendations for HR and leadership.

-----

## 🔑 Prompt Engineering

The core of this project lies in precise prompt engineering. Each prompt is designed to instruct the LLM to perform a specific, structured task.

\<details\>
\<summary\>\<strong\>1. analyze\_employee\_sentiment\</strong\>\</summary\>

  * **Use Case**: Performs a comprehensive sentiment analysis on raw employee feedback, transforming it into a strategic markdown report for leadership.
  * **Exact Prompt**:
    ```
    You are an expert HR analyst specializing in employee sentiment and attrition risk.
    Your task is to analyze the following comprehensive employee feedback data and
    generate a strategic report for leadership.

    **Employee Feedback Data:**
    ```
    {feedback\_data\_string}
    ```
    
    **Your strategic report must contain these five sections:**
    1.  **Executive Summary:** A brief, one-paragraph overview of the key findings,
        including overall sentiment and the most critical issue to address.
    2.  **Key Strengths (Top 3):** Identify the top 3 areas where the company is
        performing well. Use bullet points and cite specific question categories as evidence.
    3.  **Critical Areas for Improvement (Top 3):** Identify the top 3 areas that pose the
        biggest risks or have the most negative feedback. Use bullet points and specify the
        themes.
    4.  **Attrition Risk Assessment:** Provide a risk level (Low, Medium, High). Justify the
        assessment by connecting the "Areas for Improvement" directly to factors that cause
        employees to leave.
    5.  **Actionable Recommendations:** For each "Area for Improvement" you identified,
        propose one specific, concrete, and actionable recommendation that HR and leadership
        can implement.

    Structure the output clearly with markdown headings for each section.
    ```

\</details\>

\<details\>
\<summary\>\<strong\>2. format\_job\_description\</strong\>\</summary\>

  * **Use Case**: Parses the unstructured text of a job description and converts it into a clean, structured JSON object.

  * **Exact Prompt**:

    ````
    You are an expert HR data analyst. Read the raw text of a job description below
    and convert it into a structured JSON object with keys: "job_title",
    "required_qualifications", "preferred_qualifications", "responsibilities".

    Raw Job Description Text:
    ```text
    {raw_jd_text}
    ````

    Provide ONLY the clean JSON object as the output.

    ```
    ```

\</details\>

\<details\>
\<summary\>\<strong\>3. process\_resume\</strong\>\</summary\>

  * **Use Case**: Extracts key information from raw resume text and organizes it into a detailed, structured JSON object.

  * **Exact Prompt**:

    ````
    You are an expert data extraction AI. Read the resume text below and convert it into a
    structured JSON object. Extract: `contact_info` (name, email, linkedin_url), `summary`,
    `total_experience_years`, `work_experience` (list of jobs), `education` (list of
    qualifications), `skills`.

    Resume Text:
    ```text
    {resume_text}
    ````

    Provide ONLY a clean JSON object.

    ```
    ```

\</details\>

\<details\>
\<summary\>\<strong\>4. screen\_resume\</strong\>\</summary\>

  * **Use Case**: Evaluates a candidate's resume against a job description to generate a detailed JSON report with a match score, strengths, weaknesses, and a final hiring recommendation.

  * **Exact Prompt**:

    ````
    You are an expert HR Technical Recruiter AI. Analyze the candidate's structured
    resume against the provided job description.

    Job Description:
    ```json
    {job_description}
    ````

    Candidate's Resume Data:

    ```json
    {json.dumps(processed_resume, indent=2)}
    ```

    Provide a JSON response with: `match_score` (0-100), `summary`, `strengths` (list),
    `weaknesses` (list), `skills_analysis` (required\_skills\_found, missing\_skills),
    `final_recommendation` ("Strongly Recommend", "Consider", "Not a Fit").

    ```
    ```

\</details\>

\<details\>
\<summary\>\<strong\>5. generate\_cumulative\_report\</strong\>\</summary\>

  * **Use Case**: Synthesizes multiple candidate reports into a final summary that ranks all applicants, providing a clear order of preference for hiring managers.

  * **Exact Prompt**:

    ````
    You are a Senior Hiring Manager AI. Review the list of analysis reports for all candidates
    and generate a final cumulative report.

    Candidate Analysis Reports:
    ```json
    {json.dumps(all_analyses, indent=2)}
    ````

    Provide a JSON object with: `overall_summary` and `candidate_ranking` (a ranked
    list with rank, candidate\_name, match\_score, final\_recommendation,
    justification\_for\_rank).

    ```
    ```

\</details\>

-----

## Challenges & Solutions

### Handling Non-Textual PDFs

  * **Problem**: Some resumes are image-based (e.g., scanned documents) and cannot be parsed directly by an LLM.
  * **Solution**: An **Optical Character Recognition (OCR)** pipeline was implemented to pre-process and convert image-based PDFs into machine-readable text.

### Normalization of Unstructured Data

  * **Problem**: Resumes and job descriptions have inconsistent formatting, hindering accurate analysis.
  * **Solution**: The LLM first standardizes these documents into a consistent JSON format before evaluation, creating a uniform data structure.

### Prompt Engineering for Accuracy

  * **Problem**: Ambiguous prompts can lead to irrelevant or incorrect LLM outputs.
  * **Solution**: Prompts were engineered to be concise, specific, and context-aware to minimize misinterpretation and optimize the LLM's context window.

-----

## 💻 Code

The source code for this project is available in this repository.

**[Browse the Code](https://github.com/hritik1003/unstop/tree/main)**

-----

## 👤 Owner

  * **Hritik Agarwal** ([@hritik1003](https://www.google.com/search?q=https://github.com/hritik1003))
