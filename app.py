import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="CareerCompassBot",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Load external CSS (for the main page: sidebar, buttons, feature cards, etc.) ---
def load_css(file_path):
    with open(file_path, "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

load_css("static/style.css")

# --- Hero Section (rendered in an iframe via components.html, so it needs the CSS re-injected) ---
def render_hero(css_path):
    with open(css_path, "r") as f:
        css = f.read()

    html = f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>{css}</style>

    <div class="hero-wrapper">
        <div class="hero">
            <div class="hero-badge">🚀 AI-Powered Career Toolkit</div>
            <h1 class="hero-title">🧭 CareerCompassBot</h1>
            <p class="hero-subtitle">
                <span id="typewriter"></span><span class="cursor">|</span>
            </p>
        </div>
    </div>

    <script>
    const lines = [
        "Hi, I'm your AI career assistant 👋",
        "I can build your resume in seconds.",
        "I can match you to the right jobs.",
        "Ask me anything about your career!"
    ];

    let lineIndex = 0;
    let charIndex = 0;
    let deleting = false;
    const el = document.getElementById("typewriter");

    function type() {{
        const current = lines[lineIndex];

        if (!deleting) {{
            el.textContent = current.substring(0, charIndex + 1);
            charIndex++;
            if (charIndex === current.length) {{
                deleting = true;
                setTimeout(type, 1500);
                return;
            }}
        }} else {{
            el.textContent = current.substring(0, charIndex - 1);
            charIndex--;
            if (charIndex === 0) {{
                deleting = false;
                lineIndex = (lineIndex + 1) % lines.length;
            }}
        }}

        const speed = deleting ? 30 : 60;
        setTimeout(type, speed);
    }}

    type();
    </script>
    """
    components.html(html, height=260)

render_hero("static/style.css")

# --- Feature Cards ---
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">📄</div>
            <h3>CV Builder</h3>
            <p>Enter your details and generate a clean, downloadable resume
            or portfolio summary in seconds.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3>Job Recommender</h3>
            <p>Paste your skills and discover the best-matching jobs from
            our dataset, powered by TF-IDF + cosine similarity.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">💬</div>
            <h3>Career Chatbot</h3>
            <p>Ask basic career questions and get quick, rule-based advice
            whenever you need a nudge in the right direction.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

# --- How it works ---
st.markdown("<h2 class='section-title'>How it works</h2>", unsafe_allow_html=True)

steps = st.columns(4, gap="medium")
step_data = [
    ("1", "📝", "Pick a tool", "Choose CV Builder, Job Recommender, or Chatbot from the sidebar."),
    ("2", "⌨️", "Enter details", "Fill in your info, skills, or question."),
    ("3", "⚡", "Get results", "See your resume, matches, or advice instantly."),
    ("4", "📚", "Learn the code", "Every file is written to be read and understood."),
]
for col, (num, icon, title, desc) in zip(steps, step_data):
    with col:
        st.markdown(
            f"""
            <div class="step-card">
                <div class="step-number">{num}</div>
                <div class="step-icon">{icon}</div>
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )





st.markdown('<div class="footer">Made with ❤️ using Streamlit</div>', unsafe_allow_html=True)