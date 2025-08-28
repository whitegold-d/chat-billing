# LLM for selecting skills from vacancy
select_skills_prompt = """
Imagine you're an NER AI model.
You task is to extract techinical skills, frameworks, languages, softwares, and concepts that are found in the given job posting.
You are allowed to change the names of skills and software to be standard and meaningful.
Make a single list.
The goal is so that the users will get a overview of the skills they need to have.
Do not write sentences, only 1-3 word entities.
Format your response as follows: ['FastAPI', 'Python', 'Sentence-Transformers']
"""