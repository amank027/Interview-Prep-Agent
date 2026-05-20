RESUME_ANALYSIS_PROMPT = """You are an expert technical recruiter and career coach.

Analyze the following resume and job description.

Resume:
{resume_text}

Job Description:
{jd_text}

Provide a structured analysis covering:
1. Key skills match between resume and JD
2. Gaps in the resume relative to the JD
3. Notable achievements and strengths
4. Areas that need improvement

Be concise and actionable."""


SKILL_EXTRACTION_PROMPT = """Extract all technical skills, programming languages, frameworks, tools, and technologies from the following resume text.

Resume:
{resume_text}

Return a comma-separated list of skills only, no explanations."""
