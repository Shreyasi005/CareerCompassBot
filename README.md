# CareerCompassBot 🧭

CareerCompassBot is a multi-page Streamlit career assistant that helps users create a professional CV, find relevant job opportunities from a job dataset, and get career-focused guidance through an AI chatbot.

## Features

- **CV Builder** — Add multiple education, project, and experience entries, preview the resume, and export it as a PDF.
- **Job Recommender** — Match a user's skills and experience with job postings using **TF-IDF and cosine similarity**.
- **Career Chatbot** — Ask career-related questions and receive practical guidance using the **Google Gemini API**.
- **Job Filters** — Filter recommendations by experience level, employment type, location, and fresher/entry-level roles.
- **Responsive UI** — Custom Streamlit styling with a clean dashboard-style interface.

## Tech Stack

- Python
- Streamlit
- Pandas
- Scikit-learn
- FPDF2
- Google Gemini API
- python-dotenv
- Requests

## Project Structure

```text
CareerCompassBot/
├── app.py
├── pages/
│   ├── 1_CV_Builder.py
│   ├── 2_Job_Recommender.py
│   └── 3_Chatbot.py
├── static/
│   └── style.css
├── jobs.csv
├── generate_jobs.py
├── fetch_jobs.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## How to Run Locally

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file from `.env.example` and add your Gemini API key.
5. Start the application:

```bash
streamlit run app.py
```

6. Open the local Streamlit URL shown in the terminal.


