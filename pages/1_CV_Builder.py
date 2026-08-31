import streamlit as st
from fpdf import FPDF
import streamlit.components.v1 as components

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

st.title("📄 CV Builder")
st.write(
    "Build your professional CV by adding your personal details, work "
    "experience, projects, education, and skills. Add multiple entries "
    "for each section, preview your CV in real time, and download a "
    "professional PDF when you're ready."
)

# Initialize session state lists
for key in ("experience_list", "project_list", "education_list"):
    if key not in st.session_state:
        st.session_state[key] = []


def add_entry(list_key, template):
    st.session_state[list_key].append(template)


def remove_entry(list_key, index):
    st.session_state[list_key].pop(index)


# --- Personal Info ---
with st.container(border=True):
    st.subheader("👤 Personal Info")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", placeholder="e.g. Priya Sharma")
        email = st.text_input("Email", placeholder="priya.sharma@email.com")
        linkedin = st.text_input("LinkedIn URL (optional)", placeholder="https://linkedin.com/in/priya-sharma")
    with col2:
        title = st.text_input("Target Role / Headline", placeholder="e.g. Senior Backend Engineer, Data Scientist")
        phone = st.text_input("Phone Number", placeholder="+91 98765 43210")
        github = st.text_input("GitHub URL (optional)", placeholder="https://github.com/priya-sharma")

    summary = st.text_area("Professional Summary (2-3 sentences)", placeholder="Experienced software engineer with 5+ years building scalable backend systems. Passionate about cloud architecture and team leadership. Proven track record delivering high-impact projects.", height=80)
    skills = st.text_area("Skills (comma-separated)", placeholder="Python, Java, Go, AWS, Kubernetes, SQL, Docker, System Design, Agile", height=60)

# --- Work Experience ---
with st.container(border=True):
    st.subheader("💼 Work Experience")
    if st.button("➕ Add Work Experience", use_container_width=True):
        add_entry("experience_list", {"role": "", "company": "", "duration": "", "bullets": ""})

    for i, exp in enumerate(st.session_state.experience_list):
        with st.expander(f"Experience {i + 1}", expanded=True):
            exp["role"] = st.text_input("Role/Title", value=exp["role"], placeholder="e.g. Senior Software Engineer", key=f"exp_role_{i}")
            exp["company"] = st.text_input("Company", value=exp["company"], placeholder="e.g. Google, Microsoft, Amazon", key=f"exp_company_{i}")
            exp["duration"] = st.text_input("Duration (e.g. Jan 2022 - Present)", value=exp["duration"], placeholder="Jan 2022 - Dec 2023", key=f"exp_duration_{i}")
            exp["bullets"] = st.text_area("Key achievements & responsibilities (one point per line)", value=exp["bullets"], placeholder="Led development of microservices architecture, reducing latency by 40%\nManaged team of 5 engineers on payment processing system\nImplemented automated testing, increasing code coverage to 85%", key=f"exp_bullets_{i}", height=100)
            if st.button("🗑 Remove this entry", key=f"exp_remove_{i}", type="secondary"):
                remove_entry("experience_list", i)
                st.rerun()

# --- Projects ---
with st.container(border=True):
    st.subheader("🚀 Projects")
    if st.button("➕ Add Project", use_container_width=True):
        add_entry("project_list", {"name": "", "tech": "", "bullets": ""})

    for i, proj in enumerate(st.session_state.project_list):
        with st.expander(f"Project #{i + 1}", expanded=True):
            proj["name"] = st.text_input("Project Name", value=proj["name"], placeholder="e.g. E-Commerce Platform, AI Chatbot", key=f"proj_name_{i}")
            proj["tech"] = st.text_input("Tech Stack (comma-separated)", value=proj["tech"], placeholder="e.g. React, Node.js, MongoDB, Docker", key=f"proj_tech_{i}")
            proj["bullets"] = st.text_area("Project description & impact (one point per line)", value=proj["bullets"], placeholder="Built full-stack web application with 50K+ daily active users\nDesigned RESTful APIs handling 1M+ requests/day\nOptimized database queries, improving load time by 60%", key=f"proj_bullets_{i}", height=100)
            if st.button("🗑 Remove this entry", key=f"proj_remove_{i}", type="secondary"):
                remove_entry("project_list", i)
                st.rerun()

# --- Education ---
with st.container(border=True):
    st.subheader("🎓 Education")
    if st.button("➕ Add Education", use_container_width=True):
        add_entry("education_list", {"degree": "", "institution": "", "year": "", "score": ""})

    for i, edu in enumerate(st.session_state.education_list):
        with st.expander(f"Education #{i + 1}", expanded=True):
            edu["degree"] = st.text_input("Degree", value=edu["degree"], placeholder="e.g. Bachelor of Science in Computer Science, M.Tech in Data Science", key=f"edu_degree_{i}")
            edu["institution"] = st.text_input("Institution", value=edu["institution"], placeholder="e.g. IIT Bombay, Stanford University, Delhi University", key=f"edu_institution_{i}")
            edu["year"] = st.text_input("Year (e.g. 2018-2022)", value=edu["year"], placeholder="2020 - 2024", key=f"edu_year_{i}")
            edu["score"] = st.text_input("CGPA / Percentage (optional)", value=edu["score"], placeholder="e.g. 8.5/10 or 85%", key=f"edu_score_{i}")
            if st.button("🗑 Remove this entry", key=f"edu_remove_{i}", type="secondary"):
                remove_entry("education_list", i)
                st.rerun()


# ----------------------------------------------------------------------
# PDF generation
# ----------------------------------------------------------------------
def build_pdf():
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()
    pdf.set_margins(12, 12, 12)

    # Professional color scheme - black headings like real resume
    heading_color = (0, 0, 0)  # Black for headings
    text_dark = (20, 20, 20)
    text_light = (80, 80, 80)

    # --- HEADER ---
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*heading_color)
    pdf.cell(0, 9, (name or "Your Name").upper(), new_x="LMARGIN", new_y="NEXT")
    
    # Contact info - build on one or two lines with proper spacing
    contact_items = []
    if phone:
        contact_items.append((phone, None, False))
    if email:
        # Email as mailto link
        contact_items.append((email, f"mailto:{email}", True))
    if linkedin:
        contact_items.append(("LinkedIn", linkedin, True))
    if github:
        contact_items.append(("GitHub", github, True))
    
    if contact_items:
        pdf.set_font("Helvetica", "", 8.5)
        y_contact = pdf.get_y()
        x_pos = 12
        max_width = 186  # Page width - margins
        line_height = 5
        
        for i, (text, url, is_link) in enumerate(contact_items):
            # Add pipe separator if not first item
            if i > 0:
                sep_text = " | "
                sep_width = pdf.get_string_width(sep_text)
                
                # Check if adding this would exceed line width
                if x_pos + sep_width + pdf.get_string_width(text) > 12 + max_width:
                    # Move to next line
                    y_contact += line_height
                    x_pos = 12
                else:
                    # Add separator on same line
                    pdf.set_xy(x_pos, y_contact)
                    pdf.set_text_color(*text_light)
                    pdf.cell(sep_width, line_height, sep_text, new_x="RIGHT", new_y="TOP")
                    x_pos = pdf.get_x()
            
            # Add contact item
            pdf.set_xy(x_pos, y_contact)
            
            if is_link:
                # Blue underlined link
                pdf.set_text_color(0, 0, 255)
                pdf.set_font("Helvetica", "U", 8.5)
                item_width = pdf.get_string_width(text)
                pdf.cell(item_width, line_height, text, border=0, link=url, new_x="RIGHT", new_y="TOP")
                pdf.set_font("Helvetica", "", 8.5)
            else:
                # Regular text in gray
                pdf.set_text_color(*text_light)
                item_width = pdf.get_string_width(text)
                pdf.cell(item_width, line_height, text, new_x="RIGHT", new_y="TOP")
            
            x_pos = pdf.get_x()
        
        # Move to next line after contact info
        pdf.set_xy(12, y_contact + line_height)
        pdf.ln(4)
    
    pdf.ln(1)
    pdf.set_draw_color(*heading_color)
    pdf.set_line_width(0.5)
    pdf.line(12, pdf.get_y(), 198, pdf.get_y())
    pdf.ln(3)

    def section_heading(text):
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(*heading_color)
        pdf.cell(0, 7, text.upper(), new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(*heading_color)
        pdf.set_line_width(0.3)
        pdf.line(12, pdf.get_y(), 198, pdf.get_y())
        pdf.ln(2.5)

    # Professional Summary
    if summary:
        section_heading("Professional Summary")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*text_dark)
        pdf.multi_cell(0, 4.3, summary, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

    # Skills
    if skills:
        section_heading("Skills")
        pdf.set_font("Helvetica", "", 9)
        pdf.set_text_color(*text_dark)
        skills_list = [s.strip() for s in skills.split(",") if s.strip()]
        skills_formatted = ", ".join(skills_list)
        pdf.multi_cell(0, 4.3, skills_formatted, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)

    # Work Experience
    if st.session_state.experience_list:
        section_heading("Work Experience")
        first_exp = True
        for exp in st.session_state.experience_list:
            if not (exp["role"] or exp["company"]):
                continue
            
            if not first_exp:
                pdf.ln(2)
            first_exp = False
            
            # Job title in bold, duration in italics on same line
            pdf.set_font("Helvetica", "B", 9.5)
            pdf.set_text_color(*text_dark)
            
            title_text = exp['role']
            duration_text = exp["duration"] if exp["duration"] else ""
            
            pdf.set_xy(12, pdf.get_y())
            pdf.cell(130, 5, title_text, new_x="LMARGIN", new_y="NEXT")
            
            # Duration in italics on same line, right-aligned
            if duration_text:
                pdf.set_font("Helvetica", "I", 8)
                pdf.set_text_color(*text_light)
                duration_width = pdf.get_string_width(duration_text)
                pdf.set_xy(198 - duration_width - 2, pdf.get_y() - 5)
                pdf.cell(0, 5, duration_text)
                pdf.ln(5)
            
            # Company name
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(*text_light)
            pdf.cell(0, 4, exp['company'], new_x="LMARGIN", new_y="NEXT")
            
            pdf.ln(1.5)
            
            # Bullets for achievements
            if exp["bullets"].strip():
                for line in exp["bullets"].split("\n"):
                    line = line.strip()
                    if line:
                        pdf.set_font("Helvetica", "", 8.5)
                        pdf.set_text_color(*text_dark)
                        pdf.multi_cell(0, 4.2, f"  - {line}", new_x="LMARGIN", new_y="NEXT")
        
        pdf.ln(2)

    # Projects
    if st.session_state.project_list:
        section_heading("Projects")
        first_proj = True
        for proj in st.session_state.project_list:
            if not proj["name"]:
                continue
            
            if not first_proj:
                pdf.ln(2)
            first_proj = False
            
            # Project name in bold
            pdf.set_font("Helvetica", "B", 9.5)
            pdf.set_text_color(*text_dark)
            project_line = proj["name"]
            if proj["tech"]:
                project_line += f" | {proj['tech']}"
            pdf.cell(0, 5, project_line, new_x="LMARGIN", new_y="NEXT")
            
            pdf.ln(1.5)
            
            # Bullets for project details
            if proj["bullets"].strip():
                for line in proj["bullets"].split("\n"):
                    line = line.strip()
                    if line:
                        pdf.set_font("Helvetica", "", 8.5)
                        pdf.set_text_color(*text_dark)
                        pdf.multi_cell(0, 4.2, f"  - {line}", new_x="LMARGIN", new_y="NEXT")
        
        pdf.ln(2)

    # Education
    if st.session_state.education_list:
        section_heading("Education")
        first_edu = True
        for edu in st.session_state.education_list:
            if not edu["degree"]:
                continue
            
            if not first_edu:
                pdf.ln(1.5)
            first_edu = False
            
            # Degree in bold, year on right
            pdf.set_font("Helvetica", "B", 9.5)
            pdf.set_text_color(*text_dark)
            
            pdf.set_xy(12, pdf.get_y())
            pdf.cell(130, 5, edu['degree'], new_x="RIGHT", new_y="TOP")
            
            if edu["year"]:
                pdf.set_font("Helvetica", "I", 8)
                pdf.set_text_color(*text_light)
                year_width = pdf.get_string_width(edu["year"])
                pdf.set_xy(198 - year_width - 2, pdf.get_y())
                pdf.cell(0, 5, edu["year"])
                pdf.ln(5)
            else:
                pdf.ln(5)
            
            # Institution
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(*text_light)
            pdf.cell(0, 4, edu['institution'], new_x="LMARGIN", new_y="NEXT")
            
            if edu["score"]:
                pdf.set_font("Helvetica", "", 8)
                pdf.set_text_color(*text_light)
                pdf.cell(0, 4, f"CGPA: {edu['score']}", new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())


# ----------------------------------------------------------------------
# Live preview + download
# ----------------------------------------------------------------------
st.divider()
st.subheader("📝 Live Preview")

if not name.strip():
    st.info("Enter your name above to see the preview.")
else:
    with st.container(border=True):
        # Simulate paper-like background
        st.markdown('<div class="preview-card">', unsafe_allow_html=True)

        st.markdown(f"## {name}")
        if title:
            st.markdown(f"*{title}*")
        contact_parts = [p for p in [email, phone, linkedin, github] if p]
        if contact_parts:
            st.caption("  |  ".join(contact_parts))

        if summary:
            st.markdown("**Professional Summary**")
            st.write(summary)

        if skills:
            st.markdown("**Skills**")
            tags = [s.strip() for s in skills.split(",") if s.strip()]
            st.markdown(" ".join(f"`{t}`" for t in tags))

        if st.session_state.experience_list:
            st.markdown("**Work Experience**")
            for exp in st.session_state.experience_list:
                if exp["role"] or exp["company"]:
                    st.markdown(f"**{exp['role']} — {exp['company']}**  \n*{exp['duration']}*")
                    for line in exp["bullets"].split("\n"):
                        if line.strip():
                            st.markdown(f"- {line.strip()}")

        if st.session_state.project_list:
            st.markdown("**Projects**")
            for proj in st.session_state.project_list:
                if proj["name"]:
                    st.markdown(f"**{proj['name']}**  ({proj['tech']})")
                    for line in proj["bullets"].split("\n"):
                        if line.strip():
                            st.markdown(f"- {line.strip()}")

        if st.session_state.education_list:
            st.markdown("**Education**")
            for edu in st.session_state.education_list:
                if edu["degree"]:
                    meta = "  ".join(p for p in [edu["year"], edu["score"]] if p)
                    st.markdown(f"**{edu['degree']} — {edu['institution']}**  \n{meta}")

        st.markdown('</div>', unsafe_allow_html=True)

    pdf_bytes = build_pdf()
    st.download_button(
        label="⬇ Download as PDF",
        data=pdf_bytes,
        file_name=f"{name.replace(' ', '_')}_CV.pdf",
        mime="application/pdf",
        use_container_width=True,
    )