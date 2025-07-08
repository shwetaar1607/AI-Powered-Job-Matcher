import google.generativeai as genai
import json
import re # For basic text cleaning
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# --- Gemini API Configuration ---
# IMPORTANT: Replace "YOUR_GEMINI_API_KEY" with your actual API key.
# Get your API key from Google AI Studio: https://aistudio.google.com/app/apikey
API_KEY = "YOUR_GEMINI_API_KEY" # <--- REPLACE THIS LINE
genai.configure(api_key=API_KEY)

# Initialize the Gemini model
# Using 'gemini-1.5-flash' for faster responses, but 'gemini-1.5-pro' can be used for more detailed results.
model = genai.GenerativeModel('gemini-1.5-flash')

# --- Helper Function for Gemini API Calls ---
def get_gemini_response(prompt, generation_config=None):
    """
    Sends a prompt to the Gemini model and returns the text response.
    Handles potential errors during API call.

    Args:
        prompt (str): The text prompt to send to the model.
        generation_config (dict, optional): Configuration for generation (e.g., response_mime_type).

    Returns:
        str: The generated text response, or an error message.
    """
    try:
        if generation_config:
            response = model.generate_content(prompt, generation_config=generation_config)
        else:
            response = model.generate_content(prompt)

        # Accessing the text from the response
        if response.candidates:
            return response.candidates[0].content.parts[0].text
        else:
            return f"Gemini response had no candidates. Prompt: {prompt}"
    except Exception as e:
        return f"Error calling Gemini API: {e}"

# --- Text Cleaning Helper ---
def clean_text(text):
    """Basic text cleaning to remove extra whitespace and newlines."""
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# --- Sample Job Description (JD) ---
# In a real scenario, this would be scraped or provided by the user.
JOB_DESCRIPTION = """
Job Title: Senior Data Scientist

Company: Tech Innovations Inc.

Location: Remote

About Us:
Tech Innovations Inc. is a leading technology company focused on developing cutting-edge AI solutions. We are looking for a highly skilled Senior Data Scientist to join our dynamic team and drive impactful data-driven initiatives.

Responsibilities:
- Lead the design, development, and deployment of machine learning models for predictive analytics.
- Collaborate with product and engineering teams to define data requirements and integrate models into production systems.
- Conduct in-depth statistical analysis and A/B testing to evaluate model performance and derive actionable insights.
- Develop and maintain robust data pipelines using SQL and Python.
- Communicate complex analytical findings to non-technical stakeholders effectively.
- Mentor junior data scientists and contribute to the team's knowledge sharing.

Qualifications:
- Master's or Ph.D. in Computer Science, Statistics, Mathematics, or a related quantitative field.
- 5+ years of experience in data science or machine learning roles.
- **Expertise in Python (Pandas, NumPy, Scikit-learn)** for data manipulation and modeling.
- Strong proficiency in **SQL** for data extraction and analysis.
- Experience with **cloud platforms (AWS, GCP, Azure)** is a plus.
- Hands-on experience with **deep learning frameworks (TensorFlow, PyTorch)** is highly desirable.
- Proven experience with **A/B testing methodologies** and experimental design.
- Excellent communication and presentation skills.
- Experience with **Big Data technologies (Spark, Hadoop)** is a plus.
"""

# --- Sample Resume ---
# In a real scenario, this would be uploaded by the user.
USER_RESUME = """
John Doe
john.doe@email.com | (123) 456-7890 | LinkedIn: linkedin.com/in/johndoe

Summary:
Highly motivated Data Analyst with 3 years of experience in data analysis, statistical modeling, and dashboard creation. Proven ability to translate complex data into clear insights for business decision-making. Seeking to leverage analytical skills in a challenging data science role.

Experience:
Data Analyst | Analytics Solutions Co. | Jan 2021 - Present
- Performed extensive data cleaning and analysis using Python (Pandas) and SQL.
- Developed interactive dashboards in Tableau to visualize sales trends.
- Conducted statistical analysis on customer behavior data.

Junior Data Analyst | Startup Data | June 2019 - Dec 2020
- Assisted senior analysts with data extraction and reporting.
- Gained experience with basic machine learning concepts.

Education:
B.S. in Statistics | University of Tech | 2019

Skills:
Python (Pandas, Matplotlib), SQL, Tableau, Excel, Statistical Analysis, Data Visualization, Report Generation.
"""
def extract_skills(text, text_type="job description"):
    """
    Extracts key skills and technologies from the given text using Gemini.
    Asks for a JSON response for structured output.

    Args:
        text (str): The job description or resume text.
        text_type (str): 'job description' or 'resume' for prompt context.

    Returns:
        list: A list of extracted skills, or an empty list if an error occurs.
    """
    prompt = f"""
    From the following {text_type}, extract a comprehensive list of key skills, technologies, and tools.
    Focus on technical skills, programming languages, software, and methodologies.
    Provide the output as a JSON array of strings.

    Example Output Format:
    ["Python", "SQL", "Machine Learning", "Data Visualization", "TensorFlow"]

    {text_type} text:
    ---
    {clean_text(text)}
    ---
    """
    # Configure generation to expect JSON
    generation_config = {
        "response_mime_type": "application/json"
    }

    response_text = get_gemini_response(prompt, generation_config)

    try:
        # Gemini might sometimes wrap JSON in markdown, try to clean it
        if response_text.strip().startswith("```json"):
            response_text = response_text.strip()[7:-3].strip() # Remove ```json and ```
        
        skills = json.loads(response_text)
        if isinstance(skills, list) and all(isinstance(s, str) for s in skills):
            # Convert to lowercase for case-insensitive comparison later
            return [s.lower() for s in skills]
        else:
            print(f"Warning: Gemini returned non-list or non-string skills for {text_type}. Response: {response_text}")
            return []
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON for {text_type} skills: {e}")
        print(f"Raw Gemini response: {response_text}")
        return []
    except Exception as e:
        print(f"Unexpected error in extract_skills for {text_type}: {e}")
        return []


def analyze_skill_gap(jd_skills, resume_skills):
    """
    Compares job description skills with resume skills to find gaps.

    Args:
        jd_skills (list): Skills extracted from the job description.
        resume_skills (list): Skills extracted from the resume.

    Returns:
        tuple: (missing_skills, matched_skills)
    """
    # Convert to sets for efficient comparison
    jd_skills_set = set(jd_skills)
    resume_skills_set = set(resume_skills)

    missing_skills = list(jd_skills_set - resume_skills_set)
    matched_skills = list(jd_skills_set.intersection(resume_skills_set))

    # Sort for consistent output
    missing_skills.sort()
    matched_skills.sort()

    return missing_skills, matched_skills


def suggest_resume_improvements(job_description, user_resume, missing_skills):
    """
    Prompts Gemini to suggest improvements for the resume based on missing skills.

    Args:
        job_description (str): The full job description text.
        user_resume (str): The full user resume text.
        missing_skills (list): A list of skills identified as missing.

    Returns:
        str: Gemini's suggestions for resume improvement.
    """
    if not missing_skills:
        return "Great news! Based on the extracted skills, your resume seems to cover all the key requirements. Focus on quantifying your achievements!"

    missing_skills_str = ", ".join(missing_skills)

    prompt = f"""
    I am applying for a job with the following job description:
    ---
    {clean_text(job_description)}
    ---

    And here is my current resume:
    ---
    {clean_text(user_resume)}
    ---

    I have identified the following key skills from the job description that are either missing or not prominently featured in my resume: {missing_skills_str}.

    Please provide specific, actionable advice on how I can improve my resume to better match this job description, focusing on incorporating or highlighting these missing skills. Suggest how to phrase experiences, what sections to add, or what keywords to emphasize. Aim for practical, concise advice.
    """
    response_text = get_gemini_response(prompt)
    return response_text

if __name__ == "__main__":
    print("--- AI-Powered Job Description Analyzer & Resume Matcher ---")
    print("Analyzing job description and matching with your resume...\n")

    # 1. Extract Skills from Job Description
    print("Step 1: Extracting key skills from the Job Description...")
    jd_skills = extract_skills(JOB_DESCRIPTION, "job description")
    if jd_skills:
        print(f"  Job Description Skills ({len(jd_skills)}): {', '.join(jd_skills)}")
    else:
        print("  Could not extract skills from Job Description. Please check API key or JD format.")
        exit()

    # 2. Extract Skills from Resume
    print("\nStep 2: Extracting skills from your Resume...")
    resume_skills = extract_skills(USER_RESUME, "resume")
    if resume_skills:
        print(f"  Resume Skills ({len(resume_skills)}): {', '.join(resume_skills)}")
    else:
        print("  Could not extract skills from Resume. Please check API key or Resume format.")
        exit()

    # 3. Analyze Skill Gap
    print("\nStep 3: Performing Skill Gap Analysis...")
    missing_skills, matched_skills = analyze_skill_gap(jd_skills, resume_skills)

    print("\n--- Skill Match Results ---")
    if matched_skills:
        print(f"✅ Matched Skills ({len(matched_skills)}): {', '.join(matched_skills)}")
    else:
        print("❌ No direct skill matches found.")

    if missing_skills:
        print(f"⚠️ Missing/Underrepresented Skills ({len(missing_skills)}): {', '.join(missing_skills)}")
    else:
        print("🎉 Your resume seems to cover all key skills from the job description!")

    # 4. Suggest Resume Improvements
    print("\nStep 4: Generating Resume Improvement Suggestions...")
    suggestions = suggest_resume_improvements(JOB_DESCRIPTION, USER_RESUME, missing_skills)
    print("\n--- Resume Improvement Suggestions ---")
    print(suggestions)

    print("\n--- Analysis Complete ---")
    print("Remember that AI suggestions are a starting point; always review and refine them.")
