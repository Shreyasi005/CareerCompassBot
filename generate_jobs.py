"""
Generates jobs.csv with postings formatted the way real job boards
(Naukri, Foundit, Indeed, Glassdoor) actually structure a listing:
title, company, location, experience band, salary range, employment type,
"posted X days ago", a short key-skills tag list, and a full description
broken into "About the Role / Key Responsibilities / Requirements" sections
— instead of one flat sentence.

Run this once to (re)generate jobs.csv:
    python generate_jobs.py
"""

import pandas as pd

JOBS = [
    {
        "job_title": "Backend Developer",
        "company": "TechNova Solutions",
        "location": "Bengaluru, Karnataka",
        "experience": "1-3 Yrs",
        "salary": "₹6,00,000 - 9,00,000 P.A.",
        "employment_type": "Full-Time",
        "posted": "3 days ago",
        "key_skills": "Java, Spring Boot, MongoDB, Redis, REST API",
        "description": (
            "About the Role: We are looking for a Backend Developer to join our "
            "platform team, building and maintaining the services that power our "
            "core product.\n\n"
            "Key Responsibilities:\n"
            "- Design and build REST APIs using Spring Boot\n"
            "- Work with MongoDB and Redis to optimize data access and caching\n"
            "- Debug and resolve authentication and session issues (JWT, OTP flows)\n"
            "- Write unit tests and participate in code reviews\n\n"
            "Requirements:\n"
            "- 1-3 years of experience with Java and Spring Boot\n"
            "- Familiarity with REST API design and testing tools like Postman\n"
            "- Working knowledge of MongoDB or another NoSQL database\n"
            "- Good debugging and problem-solving skills"
        ),
    },
    {
        "job_title": "Full Stack Developer",
        "company": "BrightSoft Technologies",
        "location": "Pune, Maharashtra",
        "experience": "0-2 Yrs",
        "salary": "₹4,50,000 - 7,50,000 P.A.",
        "employment_type": "Full-Time",
        "posted": "1 day ago",
        "key_skills": "Java, Spring Boot, React, WebSocket, MongoDB",
        "description": (
            "About the Role: Join our product team to build end-to-end features "
            "spanning our React frontend and Spring Boot backend, including "
            "real-time functionality.\n\n"
            "Key Responsibilities:\n"
            "- Build UI components in React and integrate them with backend APIs\n"
            "- Implement real-time features using WebSocket/STOMP\n"
            "- Collaborate with the design team on responsive layouts\n"
            "- Fix bugs reported by QA before each release\n\n"
            "Requirements:\n"
            "- Comfortable with both Java/Spring Boot and React/JavaScript\n"
            "- Understanding of REST APIs and basic WebSocket concepts\n"
            "- Familiarity with Git-based workflows\n"
            "- Fresh graduates with strong personal projects are encouraged to apply"
        ),
    },
    {
        "job_title": "Python Developer",
        "company": "DataForge Analytics",
        "location": "Hyderabad, Telangana",
        "experience": "0-1 Yrs",
        "salary": "₹3,50,000 - 5,50,000 P.A.",
        "employment_type": "Full-Time",
        "posted": "5 days ago",
        "key_skills": "Python, Pandas, NumPy, Streamlit",
        "description": (
            "About the Role: We're hiring a Python Developer to support our data "
            "tooling team, building internal dashboards and automating data "
            "workflows.\n\n"
            "Key Responsibilities:\n"
            "- Write Python scripts to clean and process datasets\n"
            "- Build small internal tools and dashboards using Streamlit\n"
            "- Work with Pandas/NumPy for data manipulation\n"
            "- Document scripts and tools for the wider team\n\n"
            "Requirements:\n"
            "- Solid fundamentals in Python\n"
            "- Exposure to Pandas and NumPy through coursework or projects\n"
            "- Bonus: experience with Streamlit or another dashboarding tool"
        ),
    },
    {
        "job_title": "Machine Learning Intern",
        "company": "VisionAI Labs",
        "location": "Remote",
        "experience": "0 Yrs (Internship)",
        "salary": "₹15,000 - 25,000 /month",
        "employment_type": "Internship",
        "posted": "2 days ago",
        "key_skills": "Python, scikit-learn, TF-IDF, Machine Learning",
        "description": (
            "About the Role: A 6-month internship working on our recommendation "
            "systems team, helping build and evaluate text-based matching "
            "models.\n\n"
            "Key Responsibilities:\n"
            "- Assist in building recommendation features using TF-IDF and "
            "cosine similarity\n"
            "- Experiment with scikit-learn models under mentor guidance\n"
            "- Help clean and prepare text datasets\n"
            "- Present findings in weekly team syncs\n\n"
            "Requirements:\n"
            "- Final-year student or recent graduate in CS or a related field\n"
            "- Basic understanding of Python and scikit-learn\n"
            "- Curiosity about NLP/text-based ML — no prior job required"
        ),
    },
    {
        "job_title": "Frontend Developer",
        "company": "PixelWorks Digital",
        "location": "Kolkata, West Bengal",
        "experience": "0-2 Yrs",
        "salary": "₹3,00,000 - 5,00,000 P.A.",
        "employment_type": "Full-Time",
        "posted": "6 days ago",
        "key_skills": "HTML, CSS, JavaScript, React",
        "description": (
            "About the Role: We're looking for a Frontend Developer to help "
            "build responsive, accessible web interfaces for our client "
            "projects.\n\n"
            "Key Responsibilities:\n"
            "- Build responsive UIs using HTML, CSS, and JavaScript\n"
            "- Develop reusable components in React\n"
            "- Ensure mobile-friendly design and basic accessibility standards\n"
            "- Work closely with designers to match Figma mockups closely\n\n"
            "Requirements:\n"
            "- Strong fundamentals in HTML/CSS/JavaScript\n"
            "- Some experience with React (coursework or personal projects count)\n"
            "- An eye for clean, usable UI"
        ),
    },
    {
        "job_title": "Software Engineer Intern",
        "company": "CloudBridge Systems",
        "location": "Gurugram, Haryana",
        "experience": "0 Yrs (Internship)",
        "salary": "₹12,000 - 20,000 /month",
        "employment_type": "Internship",
        "posted": "4 days ago",
        "key_skills": "Java, Spring Boot, REST API, Postman",
        "description": (
            "About the Role: A hands-on backend internship supporting our core "
            "services team, working directly with senior engineers.\n\n"
            "Key Responsibilities:\n"
            "- Support backend services written in Java/Spring Boot\n"
            "- Fix reported bugs and write unit tests\n"
            "- Test REST endpoints using Postman before release\n"
            "- Document findings and raise blockers early\n\n"
            "Requirements:\n"
            "- Pursuing or recently completed a B.Tech in CS or related field\n"
            "- Basic Java and Spring Boot knowledge\n"
            "- Willingness to learn and ask questions"
        ),
    },
    {
        "job_title": "Data Analyst",
        "company": "InsightHub Analytics",
        "location": "Mumbai, Maharashtra",
        "experience": "1-3 Yrs",
        "salary": "₹5,00,000 - 8,00,000 P.A.",
        "employment_type": "Full-Time",
        "posted": "1 week ago",
        "key_skills": "Python, Pandas, Matplotlib, SQL",
        "description": (
            "About the Role: Join our analytics team to turn raw business data "
            "into dashboards and insights that drive decisions.\n\n"
            "Key Responsibilities:\n"
            "- Analyze datasets using Python, Pandas, and SQL\n"
            "- Build dashboards to visualize key business metrics\n"
            "- Present findings to non-technical stakeholders\n"
            "- Maintain data quality across recurring reports\n\n"
            "Requirements:\n"
            "- Strong SQL and Python (Pandas) skills\n"
            "- Experience with Matplotlib or another visualization library\n"
            "- Clear communication skills for presenting data findings"
        ),
    },
    {
        "job_title": "Java Developer",
        "company": "CoreStack Technologies",
        "location": "Chennai, Tamil Nadu",
        "experience": "2-4 Yrs",
        "salary": "₹7,00,000 - 11,00,000 P.A.",
        "employment_type": "Full-Time",
        "posted": "2 weeks ago",
        "key_skills": "Java, Spring Boot, MySQL",
        "description": (
            "About the Role: We need a Java Developer to design and maintain "
            "backend services for our enterprise clients.\n\n"
            "Key Responsibilities:\n"
            "- Design and implement backend services in Java/Spring Boot\n"
            "- Work with MySQL for relational data storage\n"
            "- Collaborate with QA to resolve reported defects\n"
            "- Participate in sprint planning and code reviews\n\n"
            "Requirements:\n"
            "- 2+ years of professional Java/Spring Boot experience\n"
            "- Solid understanding of relational databases (MySQL)\n"
            "- Experience working in an Agile/Scrum team"
        ),
    },
    {
        "job_title": "Chatbot Developer",
        "company": "ChatSmart AI",
        "location": "Remote",
        "experience": "0-2 Yrs",
        "salary": "₹4,00,000 - 6,50,000 P.A.",
        "employment_type": "Full-Time",
        "posted": "3 days ago",
        "key_skills": "Python, NLP, Chatbot Development",
        "description": (
            "About the Role: Build and improve rule-based and ML-based "
            "chatbots that power customer support for our clients.\n\n"
            "Key Responsibilities:\n"
            "- Build rule-based and ML-based chatbot flows in Python\n"
            "- Apply basic NLP techniques to improve response accuracy\n"
            "- Test conversations against real user queries\n"
            "- Iterate on chatbot scripts based on user feedback\n\n"
            "Requirements:\n"
            "- Comfortable with Python\n"
            "- Basic exposure to NLP concepts (even through coursework)\n"
            "- Interest in conversational design"
        ),
    },
    {
        "job_title": "React Developer",
        "company": "AppFlow Studio",
        "location": "Noida, Uttar Pradesh",
        "experience": "1-3 Yrs",
        "salary": "₹5,50,000 - 8,50,000 P.A.",
        "employment_type": "Full-Time",
        "posted": "5 days ago",
        "key_skills": "React, JavaScript, REST API",
        "description": (
            "About the Role: We're expanding our frontend team and need a "
            "React Developer to build and maintain client-facing "
            "applications.\n\n"
            "Key Responsibilities:\n"
            "- Build and maintain client-side applications using React.js\n"
            "- Integrate frontend with REST APIs built by the backend team\n"
            "- Optimize components for performance\n"
            "- Write clean, reusable, well-documented code\n\n"
            "Requirements:\n"
            "- 1+ years hands-on experience with React\n"
            "- Comfortable consuming REST APIs\n"
            "- Familiarity with state management (Context API/Redux) is a plus"
        ),
    },
]

df = pd.DataFrame(JOBS)
df.to_csv("jobs.csv", index=False)
print(f"Wrote {len(df)} realistic postings to jobs.csv")
