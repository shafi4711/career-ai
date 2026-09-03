from flask import Flask, render_template, request, jsonify
import sqlite3
import ast

app = Flask(__name__)

DATABASE = "careerai.db"


# ============================================================
# DATABASE
# ============================================================

def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    connection = get_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            class_level TEXT NOT NULL,
            stream TEXT,
            optional_language TEXT,
            marks TEXT,
            interests TEXT,
            skills TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# CAREER DATABASE
# ============================================================
#
# streams = strict eligibility for Class 11/12.
#
# Class 11/12 students can only receive careers whose stream
# contains their selected stream.
#
# Class 10 and other classes are not restricted by stream.
# ============================================================

CAREERS = {

    # ========================================================
    # SCIENCE + COMMERCE
    # ========================================================

    "Software Engineering": {

        "streams": ["science", "commerce"],

        "subjects": {
            "Computer Science": 1.0,
            "Informatics Practices": 0.9,
            "Artificial Intelligence": 0.9,
            "Mathematics": 1.0,
            "Physics": 0.5
        },

        "interests": {
            "Technology": 1.0,
            "Engineering": 0.8
        },

        "skills": {
            "Programming": 1.0,
            "Problem Solving": 1.0,
            "Critical Thinking": 0.9,
            "Mathematical Ability": 0.8
        },

        "courses": [
            "Computer Science",
            "Software Engineering",
            "Information Technology",
            "Artificial Intelligence",
            "Data Science"
        ],

        "degrees": [
            "B.Tech / B.E. in Computer Science",
            "B.Tech in Information Technology",
            "BCA",
            "B.Sc. Computer Science",
            "B.Tech in Artificial Intelligence / Data Science"
        ],

        "roadmap": [
            "Complete Class 11 and 12 with Mathematics and relevant Computer subjects.",
            "Build programming fundamentals.",
            "Learn Python, Java, JavaScript or C++.",
            "Complete a Computer Science / IT degree or equivalent pathway.",
            "Build projects and a programming portfolio.",
            "Complete internships.",
            "Specialize in an area such as web development, AI, data or cybersecurity.",
            "Apply for software engineering roles."
        ],

        "skills_to_develop": [
            "Programming",
            "Problem Solving",
            "Mathematics",
            "Critical Thinking",
            "Algorithms",
            "Computer Science",
            "Communication",
            "Teamwork"
        ],

        "opportunities": [
            "Software Engineer",
            "Web Developer",
            "Application Developer",
            "Backend Developer",
            "Frontend Developer",
            "Data Engineer"
        ],

        "benefits": [
            "Many technology career opportunities",
            "Strong demand for programming skills",
            "Opportunities across many industries",
            "Possibility of remote and international work"
        ],

        "demerits": [
            "Technology changes quickly",
            "Requires continuous learning",
            "Programming can require long periods of focused work"
        ]
    },


    # ========================================================
    # SCIENCE ONLY
    # ========================================================

    "Engineering & Technology": {

        "streams": ["science"],

        "subjects": {
            "Mathematics": 1.0,
            "Physics": 1.0,
            "Chemistry": 0.7,
            "Computer Science": 0.8,
            "Informatics Practices": 0.6
        },

        "interests": {
            "Engineering": 1.0,
            "Technology": 1.0,
            "Science & Research": 0.7
        },

        "skills": {
            "Problem Solving": 1.0,
            "Mathematical Ability": 1.0,
            "Critical Thinking": 0.9,
            "Technical Knowledge": 0.8
        },

        "courses": [
            "Engineering",
            "Mechanical Engineering",
            "Civil Engineering",
            "Electrical Engineering",
            "Electronics Engineering",
            "Computer Engineering",
            "Robotics",
            "Technology"
        ],

        "degrees": [
            "B.Tech",
            "B.E.",
            "B.Tech in Computer Engineering",
            "B.Tech in Electronics",
            "B.Tech in Mechanical Engineering",
            "B.Tech in Civil Engineering",
            "B.Tech in Electrical Engineering"
        ],

        "roadmap": [
            "Complete Class 11–12 Science with Mathematics and Physics.",
            "Strengthen Mathematics and Physics fundamentals.",
            "Prepare for relevant engineering entrance/admission processes.",
            "Choose an engineering specialization.",
            "Complete an engineering degree.",
            "Build practical projects.",
            "Complete internships.",
            "Apply for engineering or technology roles."
        ],

        "skills_to_develop": [
            "Mathematics",
            "Problem Solving",
            "Technical Knowledge",
            "Critical Thinking",
            "Engineering Design",
            "Project Management"
        ],

        "opportunities": [
            "Mechanical Engineer",
            "Civil Engineer",
            "Electrical Engineer",
            "Electronics Engineer",
            "Systems Engineer",
            "Technology Specialist",
            "Engineering Consultant"
        ],

        "benefits": [
            "Many engineering specializations",
            "Strong technical career foundation",
            "Opportunities across technology and industry"
        ],

        "demerits": [
            "Competitive admission process",
            "Requires strong technical fundamentals",
            "Continuous specialization may be necessary"
        ]
    },


    "Data Science & Analytics": {

        "streams": ["science", "commerce"],

        "subjects": {
            "Mathematics": 1.0,
            "Computer Science": 0.9,
            "Informatics Practices": 0.8,
            "Artificial Intelligence": 0.8,
            "Economics": 0.6
        },

        "interests": {
            "Technology": 1.0,
            "Science & Research": 0.8,
            "Finance & Banking": 0.5
        },

        "skills": {
            "Mathematical Ability": 1.0,
            "Problem Solving": 1.0,
            "Critical Thinking": 0.9,
            "Programming": 0.8,
            "Data Analysis": 1.0
        },

        "courses": [
            "Data Science",
            "Statistics",
            "Data Analytics",
            "Artificial Intelligence",
            "Machine Learning",
            "Computer Science"
        ],

        "degrees": [
            "B.Sc. Data Science",
            "B.Sc. Statistics",
            "B.Tech Data Science",
            "B.Tech Artificial Intelligence",
            "BCA",
            "B.Sc. Computer Science"
        ],

        "roadmap": [
            "Build strong Mathematics and analytical fundamentals.",
            "Learn statistics and probability.",
            "Learn Python and SQL.",
            "Learn data analysis tools and visualization.",
            "Complete a relevant undergraduate degree or program.",
            "Build data projects and a portfolio.",
            "Learn machine learning if interested.",
            "Complete internships.",
            "Apply for data and analytics roles."
        ],

        "skills_to_develop": [
            "Python",
            "SQL",
            "Statistics",
            "Data Analysis",
            "Mathematics",
            "Machine Learning",
            "Data Visualization",
            "Critical Thinking"
        ],

        "opportunities": [
            "Data Analyst",
            "Data Scientist",
            "Business Intelligence Analyst",
            "Machine Learning Analyst",
            "Data Engineer",
            "Research Analyst"
        ],

        "benefits": [
            "Growing importance of data-driven decision making",
            "Applicable across many industries",
            "Strong combination of technology and analytical skills"
        ],

        "demerits": [
            "Requires strong quantitative ability",
            "Technology and tools change frequently",
            "Advanced roles may require higher education"
        ]
    },


    "Medicine": {

        "streams": ["science"],

        "subjects": {
            "Biology": 1.0,
            "Chemistry": 1.0,
            "Physics": 0.9,
            "Science": 0.9
        },

        "interests": {
            "Medicine & Healthcare": 1.0,
            "Science & Research": 0.9
        },

        "skills": {
            "Critical Thinking": 0.9,
            "Research": 0.8,
            "Communication": 0.7,
            "Empathy": 0.9
        },

        "courses": [
            "MBBS",
            "BDS",
            "BAMS",
            "BHMS",
            "B.Sc. Nursing"
        ],

        "degrees": [
            "MBBS",
            "BDS",
            "BAMS",
            "BHMS",
            "B.Sc. Nursing"
        ],

        "roadmap": [
            "Take the Science stream with Biology.",
            "Build strong Biology, Chemistry and Physics fundamentals.",
            "Prepare for the applicable medical admission process.",
            "Complete the required medical degree.",
            "Complete practical and internship training.",
            "Obtain required professional registration.",
            "Begin medical practice or continue specialization."
        ],

        "skills_to_develop": [
            "Biology",
            "Scientific Thinking",
            "Communication",
            "Empathy",
            "Research",
            "Critical Thinking"
        ],

        "opportunities": [
            "Doctor",
            "Dentist",
            "Medical Researcher",
            "Healthcare Professional",
            "Clinical Specialist"
        ],

        "benefits": [
            "Meaningful healthcare career",
            "Many specialization options",
            "Strong professional responsibility"
        ],

        "demerits": [
            "Long education and training period",
            "Highly competitive",
            "Demanding workload"
        ]
    },


    "Biotechnology": {

        "streams": ["science"],

        "subjects": {
            "Biology": 1.0,
            "Chemistry": 0.9,
            "Physics": 0.6,
            "Science": 0.8
        },

        "interests": {
            "Science & Research": 1.0,
            "Medicine & Healthcare": 0.6
        },

        "skills": {
            "Research": 1.0,
            "Critical Thinking": 0.9,
            "Problem Solving": 0.8,
            "Data Analysis": 0.7
        },

        "courses": [
            "Biotechnology",
            "Biology",
            "Microbiology",
            "Genetics",
            "Biochemistry"
        ],

        "degrees": [
            "B.Sc. Biotechnology",
            "B.Tech Biotechnology",
            "B.Sc. Microbiology",
            "B.Sc. Biochemistry",
            "B.Sc. Genetics"
        ],

        "roadmap": [
            "Complete Class 11–12 Science with Biology.",
            "Build strong Biology and Chemistry fundamentals.",
            "Study biotechnology or a related undergraduate program.",
            "Develop laboratory and research skills.",
            "Complete laboratory projects and internships.",
            "Choose an area such as genetics, microbiology, pharmaceuticals or research.",
            "Pursue higher studies if required.",
            "Apply for biotechnology and research roles."
        ],

        "skills_to_develop": [
            "Biology",
            "Laboratory Skills",
            "Research",
            "Genetics",
            "Data Analysis",
            "Scientific Writing",
            "Critical Thinking"
        ],

        "opportunities": [
            "Biotechnologist",
            "Research Assistant",
            "Microbiologist",
            "Laboratory Scientist",
            "Biotechnology Analyst",
            "Researcher"
        ],

        "benefits": [
            "Combines biology and technology",
            "Opportunities in research and healthcare",
            "Applications in pharmaceuticals, agriculture and environmental science"
        ],

        "demerits": [
            "Some research careers require postgraduate study",
            "Laboratory work can be demanding",
            "Career progression may depend on specialization"
        ]
    },


    "Environmental Science": {

        "streams": ["science"],

        "subjects": {
            "Biology": 1.0,
            "Chemistry": 0.9,
            "Physics": 0.5,
            "Science": 0.9
        },

        "interests": {
            "Science & Research": 0.9,
            "Environment & Sustainability": 1.0
        },

        "skills": {
            "Research": 1.0,
            "Critical Thinking": 0.9,
            "Problem Solving": 0.9,
            "Data Analysis": 0.7
        },

        "courses": [
            "Environmental Science",
            "Environmental Studies",
            "Ecology",
            "Conservation",
            "Sustainability"
        ],

        "degrees": [
            "B.Sc. Environmental Science",
            "B.Sc. Environmental Studies",
            "B.Sc. Biology",
            "B.Sc. Ecology",
            "Environmental Science-related degrees"
        ],

        "roadmap": [
            "Complete Class 11–12 with relevant Science subjects.",
            "Build Biology and Chemistry fundamentals.",
            "Choose an environmental science or related degree.",
            "Develop research and fieldwork skills.",
            "Complete environmental projects or internships.",
            "Specialize in conservation, sustainability or environmental research.",
            "Pursue higher studies if required.",
            "Apply for environmental science careers."
        ],

        "skills_to_develop": [
            "Research",
            "Biology",
            "Environmental Analysis",
            "Data Analysis",
            "Critical Thinking",
            "Field Research",
            "Sustainability"
        ],

        "opportunities": [
            "Environmental Scientist",
            "Environmental Consultant",
            "Researcher",
            "Conservation Officer",
            "Sustainability Specialist",
            "Environmental Analyst"
        ],

        "benefits": [
            "Work on environmental and sustainability problems",
            "Growing importance of environmental issues",
            "Opportunities in research, conservation and sustainability"
        ],

        "demerits": [
            "Some roles require higher education",
            "Fieldwork may be physically demanding",
            "Career opportunities vary by specialization"
        ]
    },


    # ========================================================
    # COMMERCE + HUMANITIES
    # ========================================================

    "Business & Management": {

        "streams": ["commerce", "humanities"],

        "subjects": {
            "Business Studies": 1.0,
            "Economics": 0.9,
            "Accountancy": 0.7,
            "Mathematics": 0.5
        },

        "interests": {
            "Business & Entrepreneurship": 1.0,
            "Finance & Banking": 0.7
        },

        "skills": {
            "Leadership": 1.0,
            "Communication": 0.9,
            "Decision Making": 0.9,
            "Organization": 0.8
        },

        "courses": [
            "Business Studies",
            "Business Management",
            "Entrepreneurship",
            "Marketing",
            "Finance"
        ],

        "degrees": [
            "BBA",
            "BMS",
            "B.Com",
            "BA / B.Sc. Management-related programs",
            "MBA"
        ],

        "roadmap": [
            "Complete Class 11–12 with Commerce/Humanities.",
            "Develop communication and leadership skills.",
            "Choose a business or management degree.",
            "Learn finance, marketing and operations.",
            "Complete internships.",
            "Develop professional networking skills.",
            "Choose a specialization.",
            "Build a management, business or entrepreneurship career."
        ],

        "skills_to_develop": [
            "Leadership",
            "Communication",
            "Decision Making",
            "Organization",
            "Business Analysis",
            "Presentation",
            "Teamwork"
        ],

        "opportunities": [
            "Business Manager",
            "Marketing Manager",
            "Operations Manager",
            "Business Analyst",
            "Entrepreneur",
            "Management Consultant"
        ],

        "benefits": [
            "Many industries need management professionals",
            "Can lead to entrepreneurship",
            "Wide range of business specializations"
        ],

        "demerits": [
            "Competitive job market",
            "Management roles often require experience",
            "Entrepreneurship can involve uncertainty"
        ]
    },


    "Finance & Accounting": {

        "streams": ["commerce"],

        "subjects": {
            "Accountancy": 1.0,
            "Economics": 0.9,
            "Mathematics": 0.9,
            "Business Studies": 0.7
        },

        "interests": {
            "Finance & Banking": 1.0,
            "Business & Entrepreneurship": 0.7
        },

        "skills": {
            "Mathematical Ability": 1.0,
            "Organization": 0.9,
            "Critical Thinking": 0.8
        },

        "courses": [
            "Accountancy",
            "Economics",
            "Finance",
            "Financial Management",
            "Taxation",
            "Chartered Accountancy"
        ],

        "degrees": [
            "B.Com",
            "B.Com Honours",
            "BBA Finance",
            "BMS Finance",
            "Finance-related bachelor's degrees"
        ],

        "roadmap": [
            "Complete Class 11–12 Commerce.",
            "Build strong Accountancy and Economics fundamentals.",
            "Choose B.Com, BBA or another finance-related pathway.",
            "Learn accounting software and Excel.",
            "Develop financial analysis skills.",
            "Complete internships.",
            "Consider professional qualifications such as CA or CMA.",
            "Begin a career in accounting, banking or finance."
        ],

        "skills_to_develop": [
            "Accounting",
            "Financial Analysis",
            "Mathematics",
            "Excel",
            "Critical Thinking",
            "Attention to Detail"
        ],

        "opportunities": [
            "Accountant",
            "Financial Analyst",
            "Auditor",
            "Tax Professional",
            "Banking Professional",
            "Investment Analyst"
        ],

        "benefits": [
            "Strong connection to Commerce subjects",
            "Multiple professional qualification pathways",
            "Opportunities in banking and finance"
        ],

        "demerits": [
            "Requires accuracy",
            "Professional qualifications can be demanding",
            "Requires continuous learning"
        ]
    },


    "Law": {

        "streams": ["science", "commerce", "humanities"],

        "subjects": {
            "Political Science": 1.0,
            "History": 0.8,
            "English": 0.8,
            "Economics": 0.6
        },

        "interests": {
            "Law & Justice": 1.0
        },

        "skills": {
            "Communication": 0.9,
            "Critical Thinking": 1.0,
            "Public Speaking": 0.9,
            "Research": 0.9
        },

        "courses": [
            "5-year integrated law degree",
            "BA LLB",
            "BBA LLB",
            "B.Com LLB"
        ],

        "degrees": [
            "BA LLB",
            "BBA LLB",
            "B.Com LLB",
            "LLB"
        ],

        "roadmap": [
            "Complete Class 12.",
            "Develop English, reasoning and communication skills.",
            "Prepare for relevant law entrance/admission processes where required.",
            "Complete an integrated law degree.",
            "Complete internships and practical legal training.",
            "Build a specialization.",
            "Pursue legal practice or another legal career."
        ],

        "skills_to_develop": [
            "Communication",
            "Legal Research",
            "Critical Thinking",
            "Public Speaking",
            "Writing",
            "Negotiation"
        ],

        "opportunities": [
            "Lawyer",
            "Corporate Legal Professional",
            "Legal Consultant",
            "Legal Researcher",
            "Compliance Professional"
        ],

        "benefits": [
            "Many legal specializations",
            "Strong communication and analytical development",
            "Career opportunities across industries"
        ],

        "demerits": [
            "Competitive",
            "Requires extensive reading and writing",
            "Building experience can take time"
        ]
    },


    "Psychology": {

        "streams": ["science", "humanities"],

        "subjects": {
            "Psychology": 1.0,
            "Biology": 0.7,
            "English": 0.7
        },

        "interests": {
            "Psychology & Human Behaviour": 1.0
        },

        "skills": {
            "Communication": 0.9,
            "Research": 0.9,
            "Critical Thinking": 0.9
        },

        "courses": [
            "Psychology",
            "Human Behaviour",
            "Counselling",
            "Social Sciences"
        ],

        "degrees": [
            "BA Psychology",
            "B.Sc. Psychology",
            "MA Psychology",
            "Specialized Psychology programs"
        ],

        "roadmap": [
            "Complete Class 12 in an eligible stream.",
            "Develop interest in human behaviour and research.",
            "Complete a bachelor's degree in Psychology.",
            "Build research and communication skills.",
            "Pursue postgraduate study where required.",
            "Complete appropriate practical experience or training.",
            "Choose a specialization.",
            "Build a psychology-related career."
        ],

        "skills_to_develop": [
            "Communication",
            "Research",
            "Critical Thinking",
            "Empathy",
            "Observation",
            "Data Analysis"
        ],

        "opportunities": [
            "Psychology Researcher",
            "Counselling-related roles",
            "HR Professional",
            "Behavioural Researcher",
            "Psychology-related professional roles"
        ],

        "benefits": [
            "Interesting study of human behaviour",
            "Many specialization possibilities",
            "Useful across education, HR and research"
        ],

        "demerits": [
            "Some professional roles require postgraduate study",
            "Requires strong research skills",
            "Career path varies by specialization"
        ]
    },


    "Media & Communication": {

        "streams": ["science", "commerce", "humanities"],

        "subjects": {
            "English": 0.9,
            "Political Science": 0.6,
            "History": 0.5
        },

        "interests": {
            "Media & Communication": 1.0,
            "Design & Creativity": 0.8
        },

        "skills": {
            "Communication": 1.0,
            "Public Speaking": 0.9,
            "Creativity": 0.9
        },

        "courses": [
            "Journalism",
            "Mass Communication",
            "Media Studies",
            "Public Relations",
            "Digital Media"
        ],

        "degrees": [
            "BA Journalism",
            "BA Mass Communication",
            "BA Media Studies",
            "Bachelor's in Communication"
        ],

        "roadmap": [
            "Complete Class 12.",
            "Develop writing, communication and presentation skills.",
            "Build a portfolio through school or personal projects.",
            "Complete a media or communication degree.",
            "Gain internships.",
            "Build a professional portfolio.",
            "Apply for media, journalism or communication roles."
        ],

        "skills_to_develop": [
            "Communication",
            "Writing",
            "Public Speaking",
            "Creativity",
            "Video Production",
            "Research"
        ],

        "opportunities": [
            "Journalist",
            "Content Creator",
            "Public Relations Professional",
            "Copywriter",
            "Media Producer",
            "Communications Specialist"
        ],

        "benefits": [
            "Creative career options",
            "Many industries need communication professionals",
            "Portfolio-based opportunities"
        ],

        "demerits": [
            "Highly competitive",
            "Income can vary by specialization",
            "Requires continuous portfolio development"
        ]
    },


    "Graphic & UX Design": {

        "streams": ["science", "commerce", "humanities"],

        "subjects": {
            "Computer Science": 0.7,
            "Informatics Practices": 0.7,
            "English": 0.5
        },

        "interests": {
            "Design & Creativity": 1.0,
            "Technology": 0.8
        },

        "skills": {
            "Creativity": 1.0,
            "Problem Solving": 0.8,
            "Communication": 0.7
        },

        "courses": [
            "Graphic Design",
            "UX Design",
            "UI Design",
            "Visual Communication",
            "Digital Design"
        ],

        "degrees": [
            "B.Des.",
            "BFA",
            "BA Design",
            "B.Sc. Design"
        ],

        "roadmap": [
            "Complete Class 12.",
            "Develop visual and creative skills.",
            "Learn design principles.",
            "Learn tools such as Figma, Photoshop or Illustrator.",
            "Build a design portfolio.",
            "Complete a design degree or relevant training.",
            "Complete internships or freelance projects.",
            "Specialize in graphic, UI or UX design.",
            "Apply for design roles."
        ],

        "skills_to_develop": [
            "Graphic Design",
            "UX Research",
            "UI Design",
            "Figma",
            "Creativity",
            "Problem Solving"
        ],

        "opportunities": [
            "Graphic Designer",
            "UI Designer",
            "UX Designer",
            "Product Designer",
            "Visual Designer",
            "Brand Designer"
        ],

        "benefits": [
            "Creative career",
            "Portfolio can demonstrate ability",
            "Opportunities across technology and media"
        ],

        "demerits": [
            "Highly portfolio-driven",
            "Design trends change quickly",
            "Requires continuous practice"
        ]
    },


    "Digital Marketing & E-Commerce Specialist": {

        "streams": ["commerce", "humanities"],

        "subjects": {
            "Business Studies": 1.0,
            "Economics": 0.8,
            "English": 0.7,
            "Computer Science": 0.6,
            "Informatics Practices": 0.6
        },

        "interests": {
            "Business & Entrepreneurship": 1.0,
            "Media & Communication": 0.9,
            "Design & Creativity": 0.7,
            "Technology": 0.6
        },

        "skills": {
            "Communication": 0.9,
            "Creativity": 0.9,
            "Data Analysis": 0.8,
            "Leadership": 0.6,
            "Problem Solving": 0.7
        },

        "courses": [
            "Digital Marketing",
            "Marketing",
            "E-Commerce",
            "Business Management",
            "Advertising",
            "Social Media Marketing"
        ],

        "degrees": [
            "BBA Marketing",
            "BBA Digital Marketing",
            "B.Com",
            "BMS",
            "BA Marketing / Communication"
        ],

        "roadmap": [
            "Complete Class 11–12 with Commerce or Humanities.",
            "Build communication and business fundamentals.",
            "Learn digital marketing concepts.",
            "Learn SEO, social media marketing and content strategy.",
            "Learn analytics and online advertising.",
            "Learn e-commerce platforms and tools.",
            "Build a marketing portfolio.",
            "Complete internships or practical projects.",
            "Apply for digital marketing and e-commerce roles."
        ],

        "skills_to_develop": [
            "Digital Marketing",
            "SEO",
            "Social Media Marketing",
            "Content Marketing",
            "Google Analytics",
            "Copywriting",
            "E-Commerce",
            "Data Analysis"
        ],

        "opportunities": [
            "Digital Marketing Specialist",
            "SEO Specialist",
            "Social Media Manager",
            "E-Commerce Specialist",
            "Content Marketing Specialist",
            "Performance Marketing Executive"
        ],

        "benefits": [
            "Strong connection between business and technology",
            "Many industries need digital marketing",
            "Can support freelance and entrepreneurial opportunities",
            "Portfolio and practical experience are valuable"
        ],

        "demerits": [
            "Digital platforms and algorithms change frequently",
            "Highly competitive",
            "Requires continuous learning",
            "Performance can depend on rapidly changing market trends"
        ]
    }

}


# ============================================================
# ALIASES
# ============================================================

CAREER_ALIASES = {

    "software": "Software Engineering",
    "software engineer": "Software Engineering",
    "software engineering": "Software Engineering",
    "programming": "Software Engineering",
    "computer science": "Software Engineering",

    "engineering": "Engineering & Technology",
    "engineer": "Engineering & Technology",
    "engineering technology": "Engineering & Technology",
    "engineering & technology": "Engineering & Technology",

    "data science": "Data Science & Analytics",
    "data analytics": "Data Science & Analytics",
    "data analyst": "Data Science & Analytics",
    "data scientist": "Data Science & Analytics",
    "analytics": "Data Science & Analytics",

    "medicine": "Medicine",
    "medical": "Medicine",
    "doctor": "Medicine",
    "mbbs": "Medicine",
    "dentist": "Medicine",
    "bds": "Medicine",

    "biotechnology": "Biotechnology",
    "biotech": "Biotechnology",

    "environmental science": "Environmental Science",
    "environment": "Environmental Science",
    "environmental studies": "Environmental Science",
    "sustainability": "Environmental Science",

    "business": "Business & Management",
    "management": "Business & Management",
    "business management": "Business & Management",
    "entrepreneurship": "Business & Management",
    "entrepreneur": "Business & Management",

    "finance": "Finance & Accounting",
    "accounting": "Finance & Accounting",
    "accountant": "Finance & Accounting",
    "chartered accountant": "Finance & Accounting",
    "ca": "Finance & Accounting",

    "law": "Law",
    "lawyer": "Law",
    "legal": "Law",

    "psychology": "Psychology",
    "psychologist": "Psychology",

    "media": "Media & Communication",
    "journalism": "Media & Communication",
    "communication": "Media & Communication",
    "content creator": "Media & Communication",

    "graphic design": "Graphic & UX Design",
    "ux design": "Graphic & UX Design",
    "ui design": "Graphic & UX Design",
    "ux": "Graphic & UX Design",
    "ui": "Graphic & UX Design",

    "digital marketing": "Digital Marketing & E-Commerce Specialist",
    "e-commerce": "Digital Marketing & E-Commerce Specialist",
    "ecommerce": "Digital Marketing & E-Commerce Specialist",
    "marketing": "Digital Marketing & E-Commerce Specialist",
    "social media marketing": "Digital Marketing & E-Commerce Specialist"
}


# ============================================================
# HELPERS
# ============================================================

def clean_dict(value):
    """
    Ensure incoming data is a dictionary.
    """

    if isinstance(value, dict):
        return value

    return {}


def normalize_stream(stream):
    """
    Normalize stream names from the frontend.
    """

    stream = str(stream or "").strip().lower()

    if "science" in stream:
        return "science"

    if "commerce" in stream:
        return "commerce"

    if "humanities" in stream:
        return "humanities"

    if "arts" in stream:
        return "humanities"

    return ""


def normalize_class(class_level):
    return str(class_level or "").strip()


def calculate_category_score(student_data, profile, category):
    """
    Calculate a percentage match.

    Subjects:
        0-100

    Interests / Skills:
        0-5

    Only factors supplied by the student are considered.
    """

    student_values = clean_dict(student_data)
    profile_values = profile.get(category, {})

    score = 0
    weight_total = 0

    for name, weight in profile_values.items():

        if name not in student_values:
            continue

        try:
            value = float(student_values[name])
        except (ValueError, TypeError):
            continue

        if category == "subjects":

            value = max(0, min(100, value))

            score += value * weight
            weight_total += 100 * weight

        else:

            value = max(0, min(5, value))

            score += value * weight
            weight_total += 5 * weight

    if weight_total == 0:
        return 0

    return (score / weight_total) * 100


def is_stream_eligible(class_level, stream, career):
    """
    Strict stream eligibility.

    Class 11/12:
        career must explicitly allow selected stream.

    Other classes:
        no stream restriction.
    """

    if class_level not in ["11", "12"]:
        return True

    return stream in CAREERS[career]["streams"]


def normalize_career_name(value):
    """
    Convert user-entered career names into the official
    CAREERS dictionary name.
    """

    text = str(value or "").strip()

    if not text:
        return None

    if text in CAREERS:
        return text

    lowered = text.lower()

    if lowered in CAREER_ALIASES:
        return CAREER_ALIASES[lowered]

    for career_name in CAREERS:

        if career_name.lower() == lowered:
            return career_name

    for alias, career_name in CAREER_ALIASES.items():

        if alias in lowered:
            return career_name

    return None


def parse_saved_dict(value):
    """
    Safely convert database string representation back into
    a dictionary.

    Kept for compatibility with the existing database.
    """

    if isinstance(value, dict):
        return value

    try:
        parsed = ast.literal_eval(value)

        if isinstance(parsed, dict):
            return parsed

    except (ValueError, SyntaxError, TypeError):
        pass

    return {}


# ============================================================
# CAREER MATCHING ENGINE
# ============================================================

def calculate_career_matches(
    marks,
    interests,
    skills,
    class_level,
    stream
):

    marks = clean_dict(marks)
    interests = clean_dict(interests)
    skills = clean_dict(skills)

    class_level = normalize_class(class_level)
    stream = normalize_stream(stream)

    results = []

    for career, profile in CAREERS.items():

        # ====================================================
        # STRICT ELIGIBILITY
        # ====================================================

        if not is_stream_eligible(
            class_level,
            stream,
            career
        ):
            continue

        # ====================================================
        # CATEGORY SCORES
        # ====================================================

        subject_match = calculate_category_score(
            marks,
            profile,
            "subjects"
        )

        interest_match = calculate_category_score(
            interests,
            profile,
            "interests"
        )

        skill_match = calculate_category_score(
            skills,
            profile,
            "skills"
        )

        # ====================================================
        # FINAL SCORE
        # ====================================================
        #
        # Subject      = 40%
        # Interest     = 30%
        # Skills       = 20%
        # Eligibility  = 10%
        #
        # Eligibility is already guaranteed here, so the 10%
        # acts as a base score for an eligible career.
        # ====================================================

        final_score = (
            subject_match * 0.40
            +
            interest_match * 0.30
            +
            skill_match * 0.20
            +
            10
        )

        results.append({

            "career": career,

            "score": round(
                final_score,
                1
            ),

            "subject_match": round(
                subject_match,
                1
            ),

            "interest_match": round(
                interest_match,
                1
            ),

            "skill_match": round(
                skill_match,
                1
            ),

            "stream_match": 100

        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:5]


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return render_template("index.html")


# ============================================================
# ASSESSMENT
# ============================================================

@app.route("/assessment")
def assessment():
    return render_template("form.html")


# ============================================================
# CAREER DETAILS API
# ============================================================

@app.route("/career/<path:career_name>")
def career_details(career_name):

    career = normalize_career_name(career_name)

    if not career:

        return jsonify({
            "success": False,
            "message": "Career not found."
        }), 404

    profile = CAREERS[career]

    return jsonify({

        "success": True,

        "career": career,

        "streams": profile["streams"],

        "courses": profile["courses"],

        "degrees": profile["degrees"],

        "roadmap": profile["roadmap"],

        "skills": profile["skills_to_develop"],

        "opportunities": profile["opportunities"],

        "benefits": profile["benefits"],

        "demerits": profile["demerits"]

    })


# ============================================================
# SUBMIT ASSESSMENT
# ============================================================

@app.route("/submit-assessment", methods=["POST"])
def submit_assessment():

    data = request.get_json(silent=True)

    if not data:

        return jsonify({
            "success": False,
            "message": "No data received."
        }), 400

    # ========================================================
    # BASIC INFORMATION
    # ========================================================

    name = str(
        data.get("studentName", "")
    ).strip()

    class_level = normalize_class(
        data.get("class", "")
    )

    stream = normalize_stream(
        data.get("stream", "")
    )

    optional_language = str(
        data.get("optionalLanguage", "")
    ).strip()

    marks = clean_dict(
        data.get("marks", {})
    )

    interests = clean_dict(
        data.get("interests", {})
    )

    skills = clean_dict(
        data.get("skills", {})
    )

    # ========================================================
    # VALIDATION
    # ========================================================

    if not name:

        return jsonify({
            "success": False,
            "message": "Student name is required."
        }), 400

    if not class_level:

        return jsonify({
            "success": False,
            "message": "Class is required."
        }), 400

    if class_level in ["11", "12"]:

        if stream not in [
            "science",
            "commerce",
            "humanities"
        ]:

            return jsonify({
                "success": False,
                "message": "Please select a valid stream."
            }), 400

    # ========================================================
    # CALCULATE RECOMMENDATIONS
    # ========================================================

    recommendations = calculate_career_matches(
        marks,
        interests,
        skills,
        class_level,
        stream
    )

    # ========================================================
    # SAVE STUDENT
    # ========================================================

    connection = get_db()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO students
        (
            name,
            class_level,
            stream,
            optional_language,
            marks,
            interests,
            skills
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (

        name,
        class_level,
        stream,
        optional_language,
        str(marks),
        str(interests),
        str(skills)

    ))

    connection.commit()

    connection.close()

    # ========================================================
    # CAREER DETAILS
    # ========================================================
    #
    # Return the complete career database to the frontend.
    #
    # This keeps the frontend compatible with the existing
    # career_details response.
    # ========================================================

    career_details = {}

    for career_name, profile in CAREERS.items():

        career_details[career_name] = {

            "streams": profile["streams"],

            "courses": profile["courses"],

            "degrees": profile["degrees"],

            "roadmap": profile["roadmap"],

            "skills": profile["skills_to_develop"],

            "opportunities": profile["opportunities"],

            "benefits": profile["benefits"],

            "demerits": profile["demerits"]

        }

    return jsonify({

        "success": True,

        "message":
            "Assessment saved successfully!",

        "recommendations":
            recommendations,

        "career_details":
            career_details

    })


# ============================================================
# CHECK ANY CAREER
# ============================================================

@app.route("/check-career", methods=["POST"])
def check_career():

    data = request.get_json(silent=True) or {}

    career_input = str(
        data.get("career", "")
    ).strip()

    student_class = normalize_class(
        data.get("class", "")
    )

    stream = normalize_stream(
        data.get("stream", "")
    )

    subjects = data.get(
        "subjects",
        []
    )

    # ========================================================
    # BASIC VALIDATION
    # ========================================================

    if not career_input:

        return jsonify({

            "success": False,

            "message":
                "Please enter a career."

        }), 400

    # ========================================================
    # FIND CAREER
    # ========================================================

    career = normalize_career_name(
        career_input
    )

    if not career:

        return jsonify({

            "success": False,

            "message":
                "CareerAI does not have a detailed checker "
                "for this career yet. Try one of the available "
                "careers such as Engineering, Data Science, "
                "Medicine, Biotechnology, Environmental Science, "
                "Business, Finance, Law, Psychology, Media, "
                "Graphic & UX Design or Digital Marketing."

        })

    profile = CAREERS[career]

    # ========================================================
    # NORMALIZE SUBJECTS
    # ========================================================

    subjects_lower = [

        str(subject)
        .strip()
        .lower()

        for subject in subjects

    ]

    has_physics = (
        "physics" in subjects_lower
    )

    has_chemistry = (
        "chemistry" in subjects_lower
    )

    has_biology = (
        "biology" in subjects_lower
    )

    has_maths = (
        "mathematics" in subjects_lower
        or "maths" in subjects_lower
        or "math" in subjects_lower
    )

    has_accountancy = (
        "accountancy" in subjects_lower
        or "accounts" in subjects_lower
    )

    has_business = (
        "business studies" in subjects_lower
        or "business" in subjects_lower
    )

    has_computer = (
        "computer science" in subjects_lower
        or "informatics practices" in subjects_lower
        or "computer" in subjects_lower
    )

    # ========================================================
    # STREAM ELIGIBILITY
    # ========================================================

    stream_eligible = is_stream_eligible(
        student_class,
        stream,
        career
    )

    # ========================================================
    # SUBJECT REQUIREMENTS
    # ========================================================
    #
    # These are additional guidance checks for the important
    # subject-dependent careers.
    # ========================================================

    subject_compatible = True
    subject_reason = ""

    if career == "Medicine":

        subject_compatible = (
            stream == "science"
            and has_physics
            and has_chemistry
            and has_biology
        )

        subject_reason = (
            "Medicine commonly requires a Science pathway "
            "with Physics, Chemistry and Biology."
        )

    elif career == "Engineering & Technology":

        subject_compatible = (
            stream == "science"
            and has_physics
            and has_maths
        )

        subject_reason = (
            "Many engineering pathways require Physics "
            "and Mathematics in the senior-secondary stage."
        )

    elif career == "Data Science & Analytics":

        subject_compatible = (
            (
                stream == "science"
                and has_maths
            )
            or
            (
                stream == "commerce"
                and has_maths
            )
        )

        subject_reason = (
            "Mathematics is strongly useful for Data Science "
            "and Analytics pathways."
        )

    elif career == "Biotechnology":

        subject_compatible = (
            stream == "science"
            and has_biology
            and has_chemistry
        )

        subject_reason = (
            "Biotechnology is strongly aligned with Science, "
            "especially Biology and Chemistry."
        )

    elif career == "Environmental Science":

        subject_compatible = (
            stream == "science"
            and (
                has_biology
                or has_chemistry
                or has_physics
            )
        )

        subject_reason = (
            "Environmental Science is strongly aligned with "
            "Science subjects and scientific study."
        )

    elif career == "Software Engineering":

        if stream == "science":

            subject_compatible = (
                has_maths
                or has_computer
            )

        elif stream == "commerce":

            subject_compatible = (
                has_maths
                or has_computer
            )

        else:

            subject_compatible = False

        subject_reason = (
            "Mathematics and/or Computer-related subjects "
            "are useful preparation for software engineering."
        )

    elif career == "Finance & Accounting":

        subject_compatible = (
            stream == "commerce"
            and (
                has_accountancy
                or "economics" in subjects_lower
            )
        )

        subject_reason = (
            "Commerce subjects such as Accountancy and "
            "Economics are strongly aligned with finance."
        )

    elif career == "Business & Management":

        subject_compatible = (
            stream in ["commerce", "humanities"]
            or has_business
            or "economics" in subjects_lower
        )

        subject_reason = (
            "Commerce, Business Studies and Economics are "
            "particularly relevant to management pathways."
        )

    elif career == "Digital Marketing & E-Commerce Specialist":

        subject_compatible = (
            stream in ["commerce", "humanities"]
            or has_business
            or "economics" in subjects_lower
        )

        subject_reason = (
            "Business, communication and digital skills are "
            "useful for digital marketing and e-commerce."
        )

    else:

        subject_compatible = True

    # ========================================================
    # FINAL COMPATIBILITY
    # ========================================================

    compatible = (
        stream_eligible
        and subject_compatible
    )

    # ========================================================
    # SCORE
    # ========================================================

    if compatible:

        score = 95

    elif stream_eligible:

        score = 65

    else:

        score = 20

    # ========================================================
    # REASON
    # ========================================================

    if compatible:

        reason = (
            f"Your current academic pathway is compatible "
            f"with {career}. {subject_reason}"
        )

    elif not stream_eligible:

        allowed_streams = ", ".join(
            profile["streams"]
        )

        reason = (
            f"{career} is not directly aligned with your "
            f"current stream. The recommended stream pathway "
            f"is: {allowed_streams}."
        )

    else:

        reason = (
            f"Your stream can lead toward {career}, but your "
            f"current subject combination may not provide the "
            f"most direct preparation. {subject_reason}"
        )

    # ========================================================
    # REQUIREMENTS
    # ========================================================

    requirements = [

        "Complete the required senior-secondary qualification.",

        f"Recommended stream pathway: "
        f"{', '.join(profile['streams'])}.",

        "Meet the admission requirements of the chosen course.",

        "Complete the relevant undergraduate or professional program."

    ]

    # Add subject-specific guidance.

    if career == "Medicine":

        requirements.extend([

            "Physics",

            "Chemistry",

            "Biology",

            "Applicable medical admission/entrance requirements",

            "Required medical degree",

            "Internship and professional registration"

        ])

    elif career == "Engineering & Technology":

        requirements.extend([

            "Physics",

            "Mathematics",

            "Relevant engineering admission requirements",

            "Engineering degree"

        ])

    elif career == "Data Science & Analytics":

        requirements.extend([

            "Mathematics",

            "Statistics",

            "Programming",

            "Data analysis skills"

        ])

    elif career == "Biotechnology":

        requirements.extend([

            "Biology",

            "Chemistry",

            "Laboratory skills",

            "Relevant biotechnology qualification"

        ])

    elif career == "Environmental Science":

        requirements.extend([

            "Science fundamentals",

            "Environmental studies",

            "Research and fieldwork skills"

        ])

    # ========================================================
    # ALTERNATIVES
    # ========================================================

    alternatives = []

    for alternative_name, alternative_profile in CAREERS.items():

        if alternative_name == career:
            continue

        if student_class in ["11", "12"]:

            if stream not in alternative_profile["streams"]:
                continue

        alternatives.append({

            "career": alternative_name,

            "score": 70,

            "reason":
                "This career is also available through "
                "your academic pathway."

        })

        if len(alternatives) >= 3:
            break

    # ========================================================
    # RESPONSE
    # ========================================================

    return jsonify({

        "success": True,

        "career": career,

        "compatible": compatible,

        "score": score,

        "reason": reason,

        "requirements": requirements,

        "roadmap": profile["roadmap"],

        "alternatives": alternatives

    })


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    init_database()

    app.run(
        debug=True
    )