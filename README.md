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
