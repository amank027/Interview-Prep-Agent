FEEDBACK_PROMPT = """You are an expert interview coach providing detailed feedback.

Evaluate the following interview answer:

Question: {question}
Candidate's Answer: {answer}

Resume Context:
{resume_context}

Provide feedback in the following JSON format:
{{
  "score": <integer 1-10>,
  "strengths": ["strength1", "strength2"],
  "improvements": ["area1", "area2"],
  "ideal_answer_hints": "Brief description of what an ideal answer would include"
}}

Return only valid JSON."""


OVERALL_FEEDBACK_PROMPT = """You are an expert interview coach.

The candidate has completed a mock interview. Here is a summary of their performance:

{qa_summary}

Candidate Resume:
{resume_text}

Provide an overall assessment in the following JSON format:
{{
  "overall_score": <integer 1-100>,
  "overall_summary": "2-3 sentence summary",
  "strengths": ["strength1", "strength2", "strength3"],
  "areas_for_improvement": ["area1", "area2", "area3"]
}}

Return only valid JSON."""


ROADMAP_PROMPT = """You are a technical career coach.

Based on the interview performance and resume below, create a personalized learning roadmap.

Resume:
{resume_text}

Areas needing improvement:
{weak_areas}

Target Job Description:
{jd_text}

Provide a roadmap as a JSON array:
[
  {{
    "topic": "Topic name",
    "priority": "High/Medium/Low",
    "resources": ["resource1", "resource2"],
    "estimated_time": "e.g. 2 weeks"
  }}
]

Return only valid JSON array with 4-6 items."""
