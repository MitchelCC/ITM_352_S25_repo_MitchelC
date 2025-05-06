from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = '1234'  

# In-memory storage (replace with database in production)
users = {}
user_data = {}  # {username: {'interests': [], 'liked_careers': []}}

# General interest categories mapped to careers
GENERAL_INTEREST_CAREERS = {
    "Helping": ["Social Worker", "Counselor", "Teacher", "Nurse", "Nonprofit Manager", "Music Therapist", "Athletic Trainer", "Conservation Officer"],
    "Healthcare": ["Nurse", "Physical Therapist", "Pharmacist"],
    "Labor": ["Carpenter", "Construction Manager", "Farmer", "Chef", "Pastry Chef"],
    "Technology": ["Software Developer", "Data Scientist", "Cybersecurity Analyst", "Game Developer", "Sound Engineer", "Agricultural Engineer"],
    "Sales": ["Sales Manager", "Retail Salesperson", "Marketing Specialist", "Sports Marketing Manager", "Travel Agent", "Fashion Buyer"],
    "Creative": ["Graphic Designer", "Content Creator", "Art Director", "Journalist", "Copywriter", "Technical Writer", "Musician", "Fashion Designer", "Stylist", "Chef", "Pastry Chef"],
    "Business": ["Financial Analyst", "Accountant", "Investment Banker", "School Administrator", "Nonprofit Manager", "Sales Manager", "Marketing Specialist", "Digital Marketer", "Brand Manager", "Market Research Analyst", "Sports Marketing Manager", "Esports Manager", "Food Service Manager"],
    "Science": ["Biologist", "Chemist", "Physicist", "Environmental Scientist", "Agronomist"],
    "Education": ["Teacher", "School Administrator", "Education Consultant"],
    "Public Service": ["Lawyer", "Paralegal", "Judge", "Conservation Officer", "Sustainability Consultant"],
    "Sports": ["Athletic Trainer", "Sports Coach", "Sports Marketing Manager"],
    "Travel": ["Travel Agent", "Tour Guide", "Flight Attendant"],
    "Engineering": ["Civil Engineer", "Mechanical Engineer", "Electrical Engineer", "Agricultural Engineer"],
    "Architecture": ["Architect"],
    "Fashion": ["Fashion Designer", "Stylist", "Fashion Buyer"],
    "Gaming": ["Game Developer", "Esports Manager", "Game Tester"]
}

# Function to generate career path outline
def get_career_path(career):
    career_paths = {
        "Software Developer": {
            "education": "Bachelor's in Computer Science or related field",
            "steps": [
                "Learn programming (Python, Java, etc.)",
                "Build a portfolio of projects",
                "Gain experience through internships",
                "Obtain relevant certifications"
            ]
        },
        "Data Scientist": {
            "education": "Bachelor's/Master's in Data Science or Statistics",
            "steps": [
                "Master Python/R and SQL",
                "Learn machine learning techniques",
                "Complete data analysis projects",
                "Pursue internships in data science"
            ]
        },
        "Cybersecurity Analyst": {
            "education": "Bachelor's in Cybersecurity or IT",
            "steps": [
                "Learn networking and security fundamentals",
                "Obtain certifications (CompTIA Security+, CEH)",
                "Practice in CTF challenges",
                "Gain experience in IT roles"
            ]
        },
        "Nurse": {
            "education": "Bachelor's or Associate's in Nursing",
            "steps": [
                "Complete nursing school",
                "Pass NCLEX-RN exam",
                "Gain clinical experience",
                "Pursue specialized certifications"
            ]
        },
        "Physical Therapist": {
            "education": "Doctorate in Physical Therapy",
            "steps": [
                "Complete DPT program",
                "Pass licensure exam",
                "Gain clinical experience",
                "Pursue specialized certifications"
            ]
        },
        "Pharmacist": {
            "education": "Doctor of Pharmacy (PharmD)",
            "steps": [
                "Complete PharmD program",
                "Pass licensure exams (NAPLEX)",
                "Gain pharmacy experience",
                "Pursue residency for specialization"
            ]
        },
        "Civil Engineer": {
            "education": "Bachelor's in Civil Engineering",
            "steps": [
                "Learn engineering software (AutoCAD)",
                "Gain internship experience",
                "Obtain PE license",
                "Work on infrastructure projects"
            ]
        },
        "Mechanical Engineer": {
            "education": "Bachelor's in Mechanical Engineering",
            "steps": [
                "Learn CAD software",
                "Gain internship experience",
                "Obtain PE license",
                "Work on mechanical systems"
            ]
        },
        "Electrical Engineer": {
            "education": "Bachelor's in Electrical Engineering",
            "steps": [
                "Learn circuit design",
                "Gain internship experience",
                "Obtain PE license",
                "Work on electrical systems"
            ]
        },
        "Teacher": {
            "education": "Bachelor's in Education",
            "steps": [
                "Complete teacher training program",
                "Obtain teaching certification",
                "Gain classroom experience",
                "Pursue professional development"
            ]
        },
        "School Administrator": {
            "education": "Master's in Education Administration",
            "steps": [
                "Gain teaching experience",
                "Complete administrative training",
                "Obtain administrative license",
                "Develop leadership skills"
            ]
        },
        "Education Consultant": {
            "education": "Master's in Education or related field",
            "steps": [
                "Gain teaching experience",
                "Learn consulting skills",
                "Build a professional network",
                "Develop expertise in education trends"
            ]
        },
        "Financial Analyst": {
            "education": "Bachelor's in Finance or Economics",
            "steps": [
                "Learn financial modeling",
                "Obtain certifications (CFA)",
                "Gain analytical experience",
                "Build industry knowledge"
            ]
        },
        "Accountant": {
            "education": "Bachelor's in Accounting",
            "steps": [
                "Learn accounting software",
                "Obtain CPA certification",
                "Gain accounting experience",
                "Stay updated on tax laws"
            ]
        },
        "Investment Banker": {
            "education": "Bachelor's/Master's in Finance or MBA",
            "steps": [
                "Gain financial experience",
                "Build analytical skills",
                "Network in finance industry",
                "Obtain relevant certifications"
            ]
        },
        "Athletic Trainer": {
            "education": "Bachelor's in Athletic Training",
            "steps": [
                "Complete accredited program",
                "Obtain BOC certification",
                "Gain clinical experience",
                "Work with sports teams"
            ]
        },
        "Sports Coach": {
            "education": "Bachelor's in Sports Science or related field",
            "steps": [
                "Gain coaching experience",
                "Obtain coaching certifications",
                "Develop leadership skills",
                "Work with athletes"
            ]
        },
        "Sports Marketing Manager": {
            "education": "Bachelor's in Marketing or Sports Management",
            "steps": [
                "Learn marketing strategies",
                "Gain sports industry experience",
                "Build a professional network",
                "Develop campaign portfolios"
            ]
        },
        "Environmental Scientist": {
            "education": "Bachelor's in Environmental Science",
            "steps": [
                "Learn field research techniques",
                "Gain lab experience",
                "Work on environmental projects",
                "Pursue certifications"
            ]
        },
        "Conservation Officer": {
            "education": "Bachelor's in Environmental Science or Wildlife Management",
            "steps": [
                "Learn conservation laws",
                "Gain field experience",
                "Obtain relevant certifications",
                "Work with wildlife agencies"
            ]
        },
        "Sustainability Consultant": {
            "education": "Bachelor's in Environmental Studies or Business",
            "steps": [
                "Learn sustainability practices",
                "Gain consulting experience",
                "Build a professional network",
                "Develop expertise in green solutions"
            ]
        },
        "Journalist": {
            "education": "Bachelor's in Journalism or Communications",
            "steps": [
                "Develop writing skills",
                "Build a portfolio of articles",
                "Gain reporting experience",
                "Network with media professionals"
            ]
        },
        "Copywriter": {
            "education": "Bachelor's in English or Marketing",
            "steps": [
                "Learn persuasive writing",
                "Build a portfolio of copy",
                "Gain marketing experience",
                "Freelance for clients"
            ]
        },
        "Technical Writer": {
            "education": "Bachelor's in English or Technical Communication",
            "steps": [
                "Learn technical documentation",
                "Gain industry experience",
                "Build a portfolio",
                "Obtain certifications"
            ]
        },
        "Musician": {
            "education": "Bachelor's in Music or Self-Taught",
            "steps": [
                "Master an instrument",
                "Perform publicly",
                "Build a fanbase",
                "Network in the music industry"
            ]
        },
        "Music Therapist": {
            "education": "Bachelor's in Music Therapy",
            "steps": [
                "Complete accredited program",
                "Obtain MT-BC certification",
                "Gain clinical experience",
                "Work with clients"
            ]
        },
        "Sound Engineer": {
            "education": "Bachelor's in Audio Engineering",
            "steps": [
                "Learn audio software",
                "Gain studio experience",
                "Build a portfolio of work",
                "Network in the industry"
            ]
        },
        "Travel Agent": {
            "education": "Associate's or Bachelor's in Tourism",
            "steps": [
                "Learn travel booking systems",
                "Gain customer service experience",
                "Build destination knowledge",
                "Obtain certifications"
            ]
        },
        "Tour Guide": {
            "education": "High School Diploma or Tourism Training",
            "steps": [
                "Learn local history",
                "Develop public speaking skills",
                "Gain guiding experience",
                "Obtain certifications"
            ]
        },
        "Flight Attendant": {
            "education": "High School Diploma or Associate's",
            "steps": [
                "Complete airline training",
                "Develop customer service skills",
                "Learn safety procedures",
                "Gain hospitality experience"
            ]
        },
        "Lawyer": {
            "education": "Juris Doctor (JD)",
            "steps": [
                "Pass bar exam",
                "Gain legal experience",
                "Build a professional network",
                "Specialize in a legal field"
            ]
        },
        "Paralegal": {
            "education": "Associate's or Bachelor's in Paralegal Studies",
            "steps": [
                "Learn legal research",
                "Gain law firm experience",
                "Obtain certifications",
                "Support legal teams"
            ]
        },
        "Judge": {
            "education": "Juris Doctor (JD)",
            "steps": [
                "Gain extensive legal experience",
                "Pass bar exam",
                "Serve as a lawyer",
                "Apply for judicial positions"
            ]
        },
        "Biologist": {
            "education": "Bachelor's/Master's in Biology",
            "steps": [
                "Conduct field research",
                "Gain lab experience",
                "Publish research",
                "Pursue advanced degrees"
            ]
        },
        "Chemist": {
            "education": "Bachelor's/Master's in Chemistry",
            "steps": [
                "Learn lab techniques",
                "Gain research experience",
                "Publish findings",
                "Pursue advanced degrees"
            ]
        },
        "Physicist": {
            "education": "PhD in Physics",
            "steps": [
                "Conduct theoretical research",
                "Gain lab experience",
                "Publish research",
                "Work in academia or industry"
            ]
        },
        "Construction Manager": {
            "education": "Bachelor's in Construction Management",
            "steps": [
                "Learn project management",
                "Gain construction experience",
                "Obtain certifications (CCM)",
                "Oversee building projects"
            ]
        },
        "Carpenter": {
            "education": "Apprenticeship or Vocational Training",
            "steps": [
                "Learn woodworking skills",
                "Gain on-site experience",
                "Obtain certifications",
                "Work on construction projects"
            ]
        },
        "Architect": {
            "education": "Bachelor's/Master's in Architecture",
            "steps": [
                "Learn design software",
                "Gain internship experience",
                "Obtain licensure (NCARB)",
                "Design building projects"
            ]
        },
        "Fashion Designer": {
            "education": "Bachelor's in Fashion Design",
            "steps": [
                "Learn design software",
                "Build a portfolio",
                "Gain industry experience",
                "Create a brand"
            ]
        },
        "Stylist": {
            "education": "Associate's in Fashion or Self-Taught",
            "steps": [
                "Learn fashion trends",
                "Build a client portfolio",
                "Gain styling experience",
                "Network in the industry"
            ]
        },
        "Fashion Buyer": {
            "education": "Bachelor's in Fashion Merchandising",
            "steps": [
                "Learn market trends",
                "Gain retail experience",
                "Develop negotiation skills",
                "Work with designers"
            ]
        },
        "Digital Marketer": {
            "education": "Bachelor's in Marketing",
            "steps": [
                "Learn SEO and SEM",
                "Gain campaign experience",
                "Obtain certifications",
                "Build a portfolio"
            ]
        },
        "Brand Manager": {
            "education": "Bachelor's in Marketing or Business",
            "steps": [
                "Learn brand strategies",
                "Gain marketing experience",
                "Develop leadership skills",
                "Build a professional network"
            ]
        },
        "Market Research Analyst": {
            "education": "Bachelor's in Marketing or Statistics",
            "steps": [
                "Learn data analysis",
                "Gain research experience",
                "Master survey tools",
                "Build a portfolio"
            ]
        },
        "Farmer": {
            "education": "Associate's in Agriculture or Self-Taught",
            "steps": [
                "Learn farming techniques",
                "Gain field experience",
                "Develop business skills",
                "Manage crops or livestock"
            ]
        },
        "Agricultural Engineer": {
            "education": "Bachelor's in Agricultural Engineering",
            "steps": [
                "Learn engineering principles",
                "Gain field experience",
                "Design farming equipment",
                "Obtain certifications"
            ]
        },
        "Agronomist": {
            "education": "Bachelor's in Agronomy or Crop Science",
            "steps": [
                "Learn soil science",
                "Gain field research experience",
                "Work with farmers",
                "Publish findings"
            ]
        },
        "Game Developer": {
            "education": "Bachelor's in Computer Science or Game Design",
            "steps": [
                "Learn game engines (Unity, Unreal)",
                "Build a game portfolio",
                "Gain development experience",
                "Work on game projects"
            ]
        },
        "Esports Manager": {
            "education": "Bachelor's in Sports Management or Business",
            "steps": [
                "Learn esports industry trends",
                "Gain event management experience",
                "Build a professional network",
                "Manage teams or events"
            ]
        },
        "Game Tester": {
            "education": "High School Diploma or Associate's",
            "steps": [
                "Learn testing methodologies",
                "Gain gaming experience",
                "Develop bug reporting skills",
                "Work with development teams"
            ]
        },
        "Social Worker": {
            "education": "Bachelor's/Master's in Social Work",
            "steps": [
                "Complete social work degree",
                "Obtain licensure (LCSW)",
                "Gain field experience",
                "Specialize in a social work area"
            ]
        },
        "Counselor": {
            "education": "Master's in Counseling or Psychology",
            "steps": [
                "Complete counseling degree",
                "Obtain licensure (LPC)",
                "Gain supervised clinical experience",
                "Pursue specialized certifications"
            ]
        },
        "Nonprofit Manager": {
            "education": "Bachelor's in Nonprofit Management or Business",
            "steps": [
                "Gain volunteer experience",
                "Learn fundraising strategies",
                "Develop leadership skills",
                "Network with nonprofit professionals"
            ]
        },
        "Sales Manager": {
            "education": "Bachelor's in Business or related field",
            "steps": [
                "Gain sales experience",
                "Develop leadership skills",
                "Learn CRM software",
                "Build a professional network"
            ]
        },
        "Marketing Specialist": {
            "education": "Bachelor's in Marketing or Communications",
            "steps": [
                "Learn digital marketing tools",
                "Build a portfolio of campaigns",
                "Gain experience through internships",
                "Obtain certifications (Google Analytics)"
            ]
        },
        "Retail Salesperson": {
            "education": "High School Diploma",
            "steps": [
                "Develop customer service skills",
                "Learn product knowledge",
                "Practice sales techniques",
                "Gain retail experience"
            ]
        },
        "Chef": {
            "education": "Culinary School or Apprenticeship",
            "steps": [
                "Learn cooking techniques",
                "Gain kitchen experience",
                "Develop a signature style",
                "Pursue certifications (ServSafe)"
            ]
        },
        "Pastry Chef": {
            "education": "Culinary School with Pastry Focus",
            "steps": [
                "Master baking techniques",
                "Gain experience in bakeries",
                "Develop dessert recipes",
                "Pursue pastry certifications"
            ]
        },
        "Food Service Manager": {
            "education": "Associate's or Bachelor's in Hospitality",
            "steps": [
                "Gain restaurant experience",
                "Learn inventory management",
                "Develop leadership skills",
                "Obtain food safety certifications"
            ]
        },
        "Graphic Designer": {
            "education": "Bachelor's in Graphic Design",
            "steps": [
                "Learn design software (Adobe Creative Suite)",
                "Build a strong portfolio",
                "Practice design principles",
                "Freelance or intern for experience"
            ]
        },
        "Content Creator": {
            "education": "Bachelor's in Communications or Media",
            "steps": [
                "Learn content creation tools",
                "Build a personal brand",
                "Create consistent content",
                "Engage with audience"
            ]
        },
        "Art Director": {
            "education": "Bachelor's in Fine Arts or Design",
            "steps": [
                "Gain design experience",
                "Develop leadership skills",
                "Build a creative portfolio",
                "Network in the industry"
            ]
        }
    }
    return career_paths.get(career, {
        "education": "Relevant degree or certification",
        "steps": [
            "Pursue relevant education",
            "Gain practical experience",
            "Build a professional network",
            "Continue learning industry trends"
        ]
    })

# Mock career statistics (simulated, could be pulled from Google in reality)
MOCK_CAREER_STATS = {
    "Social Worker": {"avg_salary": "$50,000", "job_growth": "9% per year", "employment": "0.7 million"},
    "Counselor": {"avg_salary": "$48,000", "job_growth": "8% per year", "employment": "0.3 million"},
    "Teacher": {"avg_salary": "$60,000", "job_growth": "4% per year", "employment": "4 million"},
    "Nurse": {"avg_salary": "$75,000", "job_growth": "6% per year", "employment": "3.1 million"},
    "Nonprofit Manager": {"avg_salary": "$65,000", "job_growth": "7% per year", "employment": "0.2 million"},
    "Music Therapist": {"avg_salary": "$45,000", "job_growth": "5% per year", "employment": "0.05 million"},
    "Athletic Trainer": {"avg_salary": "$50,000", "job_growth": "10% per year", "employment": "0.03 million"},
    "Conservation Officer": {"avg_salary": "$55,000", "job_growth": "3% per year", "employment": "0.02 million"},
    "Physical Therapist": {"avg_salary": "$90,000", "job_growth": "17% per year", "employment": "0.25 million"},
    "Pharmacist": {"avg_salary": "$125,000", "job_growth": "2% per year", "employment": "0.3 million"},
    "Carpenter": {"avg_salary": "$45,000", "job_growth": "2% per year", "employment": "0.9 million"},
    "Construction Manager": {"avg_salary": "$95,000", "job_growth": "8% per year", "employment": "0.4 million"},
    "Farmer": {"avg_salary": "$40,000", "job_growth": "1% per year", "employment": "0.8 million"},
    "Chef": {"avg_salary": "$50,000", "job_growth": "5% per year", "employment": "1.2 million"},
    "Pastry Chef": {"avg_salary": "$45,000", "job_growth": "4% per year", "employment": "0.1 million"},
    "Software Developer": {"avg_salary": "$110,000", "job_growth": "15% per year", "employment": "1.5 million"},
    "Data Scientist": {"avg_salary": "$120,000", "job_growth": "14% per year", "employment": "0.5 million"},
    "Cybersecurity Analyst": {"avg_salary": "$100,000", "job_growth": "31% per year", "employment": "0.2 million"},
    "Game Developer": {"avg_salary": "$85,000", "job_growth": "10% per year", "employment": "0.1 million"},
    "Sound Engineer": {"avg_salary": "$60,000", "job_growth": "6% per year", "employment": "0.05 million"},
    "Agricultural Engineer": {"avg_salary": "$80,000", "job_growth": "5% per year", "employment": "0.03 million"},
    "Sales Manager": {"avg_salary": "$70,000", "job_growth": "4% per year", "employment": "0.5 million"},
    "Retail Salesperson": {"avg_salary": "$30,000", "job_growth": "2% per year", "employment": "4.5 million"},
    "Marketing Specialist": {"avg_salary": "$65,000", "job_growth": "6% per year", "employment": "0.7 million"},
    "Sports Marketing Manager": {"avg_salary": "$75,000", "job_growth": "7% per year", "employment": "0.05 million"},
    "Travel Agent": {"avg_salary": "$40,000", "job_growth": "-6% per year", "employment": "0.1 million"},
    "Fashion Buyer": {"avg_salary": "$60,000", "job_growth": "3% per year", "employment": "0.04 million"},
    "Graphic Designer": {"avg_salary": "$50,000", "job_growth": "3% per year", "employment": "0.3 million"},
    "Content Creator": {"avg_salary": "$55,000", "job_growth": "8% per year", "employment": "0.2 million"},
    "Art Director": {"avg_salary": "$90,000", "job_growth": "2% per year", "employment": "0.1 million"},
    "Journalist": {"avg_salary": "$45,000", "job_growth": "-11% per year", "employment": "0.4 million"},
    "Copywriter": {"avg_salary": "$60,000", "job_growth": "5% per year", "employment": "0.15 million"},
    "Technical Writer": {"avg_salary": "$75,000", "job_growth": "7% per year", "employment": "0.1 million"},
    "Musician": {"avg_salary": "$40,000", "job_growth": "1% per year", "employment": "0.2 million"},
    "Fashion Designer": {"avg_salary": "$65,000", "job_growth": "3% per year", "employment": "0.05 million"},
    "Stylist": {"avg_salary": "$45,000", "job_growth": "4% per year", "employment": "0.03 million"},
    "Financial Analyst": {"avg_salary": "$85,000", "job_growth": "6% per year", "employment": "0.3 million"},
    "Accountant": {"avg_salary": "$70,000", "job_growth": "4% per year", "employment": "1.2 million"},
    "Investment Banker": {"avg_salary": "$120,000", "job_growth": "5% per year", "employment": "0.2 million"},
    "School Administrator": {"avg_salary": "$90,000", "job_growth": "4% per year", "employment": "0.3 million"},
    "Digital Marketer": {"avg_salary": "$65,000", "job_growth": "6% per year", "employment": "0.5 million"},
    "Brand Manager": {"avg_salary": "$90,000", "job_growth": "5% per year", "employment": "0.1 million"},
    "Market Research Analyst": {"avg_salary": "$65,000", "job_growth": "13% per year", "employment": "0.2 million"},
    "Biologist": {"avg_salary": "$65,000", "job_growth": "5% per year", "employment": "0.1 million"},
    "Chemist": {"avg_salary": "$75,000", "job_growth": "3% per year", "employment": "0.09 million"},
    "Physicist": {"avg_salary": "$100,000", "job_growth": "5% per year", "employment": "0.02 million"},
    "Environmental Scientist": {"avg_salary": "$70,000", "job_growth": "8% per year", "employment": "0.1 million"},
    "Agronomist": {"avg_salary": "$60,000", "job_growth": "6% per year", "employment": "0.03 million"},
    "Lawyer": {"avg_salary": "$120,000", "job_growth": "4% per year", "employment": "0.8 million"},
    "Paralegal": {"avg_salary": "$50,000", "job_growth": "10% per year", "employment": "0.3 million"},
    "Judge": {"avg_salary": "$130,000", "job_growth": "2% per year", "employment": "0.03 million"},
    "Civil Engineer": {"avg_salary": "$90,000", "job_growth": "6% per year", "employment": "0.3 million"},
    "Mechanical Engineer": {"avg_salary": "$95,000", "job_growth": "4% per year", "employment": "0.3 million"},
    "Electrical Engineer": {"avg_salary": "$100,000", "job_growth": "5% per year", "employment": "0.3 million"},
    "Architect": {"avg_salary": "$80,000", "job_growth": "3% per year", "employment": "0.1 million"},
    "Game Developer": {"avg_salary": "$85,000", "job_growth": "10% per year", "employment": "0.1 million"},
    "Esports Manager": {"avg_salary": "$70,000", "job_growth": "15% per year", "employment": "0.02 million"},
    "Game Tester": {"avg_salary": "$40,000", "job_growth": "8% per year", "employment": "0.05 million"}
}

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('form'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in users:
            users[username] = password
            user_data[username] = {'interests': [], 'liked_careers': []}
            session['username'] = username
            return redirect(url_for('form'))
        return "Username already exists. <a href='/register'>Try again</a>"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('form'))
        return "Invalid credentials. <a href='/login'>Try again</a>"
    return render_template('login.html')

@app.route('/form')
def form():
    if 'username' not in session:
        return redirect(url_for('login'))
    if session['username'] not in user_data:
        session.pop('username', None)
        return redirect(url_for('login'))
    return render_template('form.html')

@app.route('/results', methods=['GET', 'POST'])
def results():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    if username not in user_data:
        session.pop('username', None)
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        interests = request.form.getlist('interests')
        matched_careers = set()
        for interest in interests:
            if interest in GENERAL_INTEREST_CAREERS:
                matched_careers.update(GENERAL_INTEREST_CAREERS[interest])
        matched_careers = list(matched_careers)
        career_paths = {career: get_career_path(career) for career in matched_careers}
        user_data[username]['interests'] = interests
        session['matched_careers'] = matched_careers
        session['career_paths'] = career_paths
        liked_careers = user_data[username]['liked_careers']
        return render_template('results.html', careers=matched_careers, career_paths=career_paths, liked_careers=liked_careers)
    
    # Handle GET request (e.g., after liking/unliking a career)
    matched_careers = session.get('matched_careers', [])
    career_paths = session.get('career_paths', {})
    liked_careers = user_data[username]['liked_careers']
    return render_template('results.html', careers=matched_careers, career_paths=career_paths, liked_careers=liked_careers)

@app.route('/like_career/<career>')
def like_career(career):
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    if username not in user_data:
        session.pop('username', None)
        return redirect(url_for('login'))
    # Check if the career exists in GENERAL_INTEREST_CAREERS
    all_careers = sum(GENERAL_INTEREST_CAREERS.values(), [])
    if career in all_careers and career not in user_data[username]['liked_careers']:
        user_data[username]['liked_careers'].append(career)
    return redirect(url_for('results'))

@app.route('/unlike_career/<career>')
def unlike_career(career):
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    if username not in user_data:
        session.pop('username', None)
        return redirect(url_for('login'))
    # Check if the career exists in GENERAL_INTEREST_CAREERS and is in liked_careers
    all_careers = sum(GENERAL_INTEREST_CAREERS.values(), [])
    if career in all_careers and career in user_data[username]['liked_careers']:
        user_data[username]['liked_careers'].remove(career)
    return redirect(url_for('results'))

@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    if username not in user_data:
        session.pop('username', None)
        return redirect(url_for('login'))
    interests = user_data[username]['interests']
    liked_careers = user_data[username]['liked_careers']
    career_stats = {career: MOCK_CAREER_STATS.get(career, {}) for career in liked_careers}
    return render_template('profile.html', interests=interests, liked_careers=liked_careers, career_stats=career_stats)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('matched_careers', None)
    session.pop('career_paths', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)