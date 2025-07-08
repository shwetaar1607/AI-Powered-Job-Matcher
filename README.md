# AI-Powered Job Matcher

## Project Overview

This Python script leverages the power of the Google Gemini API to assist job seekers in tailoring their resumes to specific job descriptions. It performs a comprehensive skill gap analysis and provides actionable suggestions for resume improvement.

The core functionalities include:
- **Skill Extraction:** Automatically extracts key skills and technologies from both a given job description and a user's resume using the Gemini API's natural language understanding capabilities.
- **Skill Gap Analysis:** Compares the extracted skills to identify:
    - **Matched Skills:** Skills present in both the job description and the resume.
    - **Missing/Underrepresented Skills:** Key skills from the job description that are either absent or not prominently highlighted in the resume.
- **Resume Improvement Suggestions:** Generates personalized advice on how to enhance the resume, focusing on incorporating or emphasizing the identified missing skills. This includes suggestions on phrasing experiences, adding relevant sections, or highlighting keywords.

This tool aims to streamline the resume customization process, making it more efficient and effective for job applications.

## How It Works

1.  **Input:** The script takes a job description and a resume (currently hardcoded as sample strings, but can be easily adapted for user input or file uploads).
2.  **Gemini API Calls:**
    - It sends prompts to the `gemini-1.5-flash` model to extract structured lists of skills from both texts.
    - It then sends a prompt with the job description, resume, and identified missing skills to Gemini to generate improvement suggestions.
3.  **Output:** The script prints:
    - The extracted skills from the JD and resume.
    - A clear breakdown of matched and missing skills.
    - Detailed, actionable resume improvement suggestions.

## Technologies and Libraries

* **Python:** The primary programming language.
* **Google Generative AI (`google.generativeai`):** For interacting with the Gemini API.
* **`json`:** For parsing JSON responses from the API.
* **`re`:** For basic text cleaning (regular expressions).
* **`os`:** (Recommended for API key management) For accessing environment variables.

## Setup and Installation

To run this project locally, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YourGitHubUsername/ai-job-matcher.git](https://github.com/YourGitHubUsername/ai-job-matcher.git)
    cd ai-job-matcher
    ```

2.  **Set Up a Virtual Environment (if you haven't already):**
    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:
    -   On macOS/Linux: `source venv/bin/activate`
    -   On Windows: `venv\Scripts\activate`

3.  **Install Dependencies:**
    ```bash
    pip install google-generativeai
    ```

4.  **Configure Gemini API Key:**
    **IMPORTANT:** Your API key should **NOT** be committed directly to version control.
    -   Go to [Google AI Studio](https://aistudio.google.com/app/apikey) to generate your Gemini API key.
    -   **Option A (Recommended - Environment Variable):** Set your API key as an environment variable (e.g., `GEMINI_API_KEY`).
        -   On macOS/Linux: `export GEMINI_API_KEY="YOUR_API_KEY_HERE"`
        -   On Windows (Command Prompt): `set GEMINI_API_KEY="YOUR_API_KEY_HERE"`
        -   On Windows (PowerShell): `$env:GEMINI_API_KEY="YOUR_API_KEY_HERE"`
        -   Modify the `job_matcher.py` script to load the API key from the environment variable:
            ```python
            import os
            API_KEY = os.getenv("GEMINI_API_KEY")
            if not API_KEY:
                raise ValueError("GEMINI_API_KEY environment variable not set. Please set it before running the script.")
            genai.configure(api_key=API_KEY)
            ```
    -   **Option B (Less Secure - Placeholder):** If you must, replace `"AIzaSyBKegAQxWVXjvTbdJUVZ1UEy6lyV26pZws"` in `job_matcher.py` with your actual API key. **Remember to remove it or replace it with a placeholder before pushing any changes to a public repository.**

## Usage

Once setup is complete, you can run the script from your terminal:

```bash
python job_matcher.py