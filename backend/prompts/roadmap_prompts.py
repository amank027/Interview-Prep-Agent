SKILL_GAP_PROMPT = """You are a technical career advisor.

Analyze the gap between the candidate's current skills and the target role requirements.

Current skills from resume:
{current_skills}

Required skills from JD:
{required_skills}

List the top skill gaps as a JSON array of strings. Return only valid JSON."""
