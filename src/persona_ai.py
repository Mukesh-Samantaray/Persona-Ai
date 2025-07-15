import os
import google.generativeai as genai


def format_markdown(comments, posts):
    md = ["## Comments"]
    for i, (date, txt) in enumerate(comments, 1):
        md += [f"### Comment {i}", f"**Date:** {date}", txt, ""]
    md += ["## Posts (text only)"]
    for i, (date, title, body) in enumerate(posts, 1):
        md += [f"### Post {i}", f"**Title:** {title}", f"**Date:** {date}", body, ""]
    return "\n".join(md)


def generate_persona(username, comments, posts):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash")

    text_md = format_markdown(comments, posts)

    prompt = f"""
From the following Reddit content (comments and posts), generate a psychological and behavioral persona report with the following structure:

1. **Name**: u/{username}
2. **Summary** (within 10 words like a quote)
3. **Tags** (e.g., thinker, social, honest, curious)
4. **Motivations**: Estimate percentage for each using slider-like visual:
   - CONVENIENCE
   - WELLNESS
   - SPEED
   - PREFERENCES
   - COMFORT
   - DIETARY NEEDS
   Example format:
   CONVENIENCE: >>>>>>>>-- 80%
   WELLNESS: >>>------- 30%

5. **Personality Spectrum** (visual format like sliders):
   - Introvert  ------*--- Extrovert
   - Intuition  ---*------ Sensing
   - Feeling    --------*- Thinking
   - Perceiving -*-------- Judging
   Format: 10-char scale with * at estimated point.

6. **Behavior & Habits** (bullet points)  — reference comment/post number like (Comment 3) or (Post 2)
7. **Goals & Needs** (bullet points) — reference comment/post number like (Comment 3) or (Post 2)
8. **Frustrations** (bullet points) — reference comment/post number like (Comment 3) or (Post 2)

### Reddit Data:
{text_md}
"""

    response = model.generate_content(prompt)
    result = response.text.strip()
    reddit_content = format_markdown(comments, posts)
    final_output = f"{result}\n\n---\n\n{reddit_content}"

    return final_output
