import os
import requests
import json
from pdfminer.high_level import extract_text as pdfminer_extract_text
from mathpix import request_pdf, get_latex, get_latex_files, unzip_latex
from dotenv import load_dotenv
from studyguide import generate_study_guide
from openai import OpenAI


def find_course_materials(directory):
    """
    Recursively search the given directory for PDF and TXT files.
    Returns a list of file paths.
    """
    materials = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.pdf', '.txt')):
                materials.append(os.path.join(root, file))
    return materials


def main():
    load_dotenv()
    # 1. Ask user for the directory containing course materials (e.g., lecture slides).
    relative_path = input("Enter the relative path to thedirectory containing course pdfs: ").strip()
    directory = os.path.abspath("test_files/" + relative_path)
    if not os.path.isdir(directory):
        print("Invalid directory. Exiting.")
        return
    
    # 2. Get list of pdf files in directory
    pdf_files = find_course_materials(directory)
    if not pdf_files:
        print("No pdf files found in the directory.")
        return
    print("\nFound PDF files:")
    for pdf_file in pdf_files:
        print(f"  - {os.path.basename(pdf_file)}")
    
    # 3. Get pdf ids from mathpix
    pdf_ids = []
    for pdf_file in pdf_files:
        pdf_id = request_pdf(pdf_file)
        pdf_ids.append(pdf_id)
    print(pdf_ids)

    #4. Get latex zip files from mathpix into directory
    latex_zip_files = []
    for pdf_id in pdf_ids:
        latex_zip_file = get_latex(pdf_id, directory)
        latex_zip_files.append(latex_zip_file)
    print("\nGenerated LaTeX ZIP files:")
    for zip_file in latex_zip_files:
        print(f"  - {os.path.basename(zip_file)}")
    
    #5. Unzip latex zip files
    latex_files = []
    for latex_zip_file in latex_zip_files:
        latex_files.append(unzip_latex(latex_zip_file, directory))
    print("\nExtracted LaTeX files:")
    for tex_file in latex_files:
        print(f"  - {os.path.basename(tex_file)}")

    #6. read latex files
    
    latex_files_content = get_latex_files(latex_files, directory)
    print(latex_files_content)

    #7. Generate study guide
    study_guide = generate_study_guide(latex_files_content)
    print(study_guide)

if __name__ == "__main__":
    main()