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

## Job Recommendation Approach

The recommender combines the user's entered skills/experience with each job's skills and description. **TF-IDF** converts the text into numerical vectors, while **cosine similarity** calculates how closely the user profile matches each job. Results are ranked by match score.

## Job Data

`jobs.csv` contains sample job postings. `generate_jobs.py` can regenerate the sample dataset. `fetch_jobs.py` can retrieve job postings through the Adzuna API when valid API credentials are configured.

## Security

API keys and secrets should never be committed to GitHub. Store the Gemini key in a local `.env` file or the deployment platform's secrets manager. The repository intentionally includes only `.env.example`.

## Deployment

The app can be deployed using Streamlit Community Cloud by connecting the GitHub repository and selecting `app.py` as the main file. Add `GEMINI_API_KEY` to the deployment secrets before using the chatbot.
