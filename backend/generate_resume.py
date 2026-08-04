from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'Jane Doe - Full Stack Developer', align='C')
        self.ln(20)

pdf = PDF()
pdf.add_page()
pdf.set_font('helvetica', '', 12)
text = """
Jane Doe
Email: jane.doe@example.com
Location: San Francisco, CA

EXPERIENCE
Senior Software Engineer | Tech Solutions Inc. | 2021 - Present
- Architected and deployed microservices using Python and FastAPI.
- Built dynamic, responsive frontends using React and JavaScript.
- Optimized database queries in PostgreSQL and implemented ORM models using SQLAlchemy.
- Deployed applications using Docker and Kubernetes.

Data Scientist | Data Innovations | 2018 - 2021
- Developed predictive models using Machine Learning and Deep Learning.
- Extracted and processed large datasets using SQL and Python.
- Deployed ML pipelines in AWS.

SKILLS
Programming Languages: Python, JavaScript, TypeScript, SQL
Frontend: React, HTML, CSS, Tailwind CSS
Backend: FastAPI, Django, Node.js
Database: PostgreSQL, MongoDB
DevOps & Cloud: Docker, Kubernetes, AWS, Git
AI/ML: Machine Learning, Deep Learning, NLP
"""

pdf.multi_cell(0, 7, text)
pdf.output('sample_resume.pdf')
