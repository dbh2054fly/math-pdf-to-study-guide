from openai import OpenAI
import os
def generate_study_guide(latex_content):
    '''generate a study guide from a list of latex files'''
    # load the latex files

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    # generate a study guide
    study_guide = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful math professor."},
            {
                "role": "user",
                "content": f"Generate a study guide from the following latex : {latex_content}. Ensure the output is in LaTeX format."
            }
        ]
    )
    
    study_guide_text = study_guide.choices[0].message.content
    return study_guide_text

    
