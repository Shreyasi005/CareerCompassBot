import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Apply purple/indigo aesthetic styling
st.markdown("""
    <style>
        h1 {
            background: linear-gradient(135deg, #6366f1 0%, #7c3aed 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        h2 {
            color: #a78bfa;
        }
        .stButton>button {
            background: linear-gradient(135deg, #6366f1, #7c3aed) !important;
            border: none !important;
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #7c3aed, #a78bfa) !important;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 Job Recommender")
st.write(
    "Paste your skills and experience below, optionally narrow things down "
    "with the filters, and I'll rank the postings that match you best using "
    "TF-IDF + cosine similarity."
)

# Load dataset
df = pd.read_csv("jobs.csv")

# --- Filters ---
st.subheader("🔎 Filters")
with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        experience_options = ["Any"] + sorted(df["experience"].unique().tolist())
        experience_filter = st.selectbox("Experience Level", experience_options)
    with col2:
        employment_options = ["Any"] + sorted(df["employment_type"].unique().tolist())
        employment_filter = st.selectbox("Employment Type", employment_options)
    with col3:
        location_options = sorted(df["location"].unique().tolist())
        location_filter = st.multiselect("Preferred Location(s)", location_options)

    fresher_only = st.checkbox("🎓 I'm a fresher — only show 0 Yrs / Internship / entry-level roles")

user_profile = st.text_area(
    "✍️ Your skills / experience",
    placeholder="e.g. Java, Spring Boot, REST API, MongoDB, debugging authentication issues, Postman testing",
    height=140,
)

top_n = st.slider("How many matches to show?", min_value=1, max_value=10, value=5)

if st.button("🔍 Find Matching Jobs", use_container_width=True):
    if not user_profile.strip():
        st.warning("Please enter some skills or experience first.")
    else:
        # Apply filters
        filtered = df.copy()
        if experience_filter != "Any":
            filtered = filtered[filtered["experience"] == experience_filter]
        if employment_filter != "Any":
            filtered = filtered[filtered["employment_type"] == employment_filter]
        if location_filter:
            filtered = filtered[filtered["location"].isin(location_filter)]
        if fresher_only:
            filtered = filtered[
                filtered["experience"].str.startswith("0")
                | filtered["experience"].str.contains("Internship", case=False)
            ]

        if filtered.empty:
            st.warning(
                "No postings match your filters. Try loosening one of them "
                "(e.g. clear the location filter or set Experience to 'Any')."
            )
        else:
            # TF-IDF + Cosine Similarity
            match_text = (filtered["key_skills"] + ". " + filtered["description"]).tolist()
            documents = [user_profile] + match_text
            vectorizer = TfidfVectorizer(stop_words="english")
            tfidf_matrix = vectorizer.fit_transform(documents)
            user_vector = tfidf_matrix[0:1]
            job_vectors = tfidf_matrix[1:]
            scores = cosine_similarity(user_vector, job_vectors).flatten()

            results = filtered.copy()
            results["match_score"] = scores
            results = results.sort_values("match_score", ascending=False).head(top_n)

            st.divider()
            st.caption(f"Showing top {len(results)} of {len(filtered)} filtered postings")

            for _, row in results.iterrows():
                with st.container(border=True):
                    # Header row with title and score
                    col_title, col_score = st.columns([3, 1])
                    with col_title:
                        st.markdown(f"### {row['job_title']}")
                        st.markdown(f"**{row['company']}**  ·  {row['location']}")
                    with col_score:
                        score_pct = int(row['match_score'] * 100)
                        st.metric("Match", f"{score_pct}%")
                        # Progress bar
                        st.markdown(f"""
                            <div class="match-bar">
                                <div class="match-bar-fill" style="width:{score_pct}%;"></div>
                            </div>
                        """, unsafe_allow_html=True)

                    # Meta info
                    meta_cols = st.columns(3)
                    meta_cols[0].caption(f"💼 {row['employment_type']}")
                    meta_cols[1].caption(f"📅 {row['experience']}")
                    meta_cols[2].caption(f"🕒 Posted {row['posted']}")

                    st.write(f"💰 {row['salary']}")

                    # Skills tags
                    skill_tags = [s.strip() for s in row["key_skills"].split(",")]
                    st.markdown(" ".join(f'<span class="skill-tag">{tag}</span>' for tag in skill_tags), unsafe_allow_html=True)

                    with st.expander("📋 View full job description"):
                        st.markdown(row["description"])

                    st.button(
                        "Apply Now",
                        key=f"apply_{row['job_title']}_{row['company']}",
                        disabled=True,
                        help="Demo only — this app doesn't connect to a real job board",
                    )