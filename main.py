import os
import requests
import json
from pdfminer.high_level import extract_text as pdfminer_extract_text
from mathpix import request_pdf, get_latex, get_latex_files, unzip_latex
from dotenv import load_dotenv
from studyguide import generate_study_guide
from openai import OpenAI

# --- Step 1: File Discovery ---

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

# --- Step 2: Extraction of text and math from lecture slides ---

def extract_text(file_path):
    """
    Uses pdfminer to extract text from slides
    """
    return pdfminer_extract_text(file_path)


# --- Main Pipeline ---

'''def main():
    # 1. Ask user for the directory containing course materials (e.g., lecture slides).
    directory = input("Enter the directory containing course materials: ").strip()
    if not os.path.isdir(directory):
        print("Invalid directory. Exiting.")
        return

    # 2. Find all course material files.
    materials = find_course_materials(directory)
    if not materials:
        print("No course material files found in the directory.")
        return

    print(f"Found {len(materials)} material file(s). Extracting text via OCR...")
    combined_text = ""
    for file in materials:
        print(f"Processing: {file}")
        text = extract_material_text(file)
        combined_text += "\n" + text

    if not combined_text.strip():
        print("No text could be extracted from the materials. Exiting.")
        return

    # 3. Summarize the extracted text.
    print("Initializing summarization pipeline (this may take a moment)...")
    # For math/technical text (e.g., lecture slides)
    summarizer = pipeline("summarization", model="allenai/led-large-16384-arxiv")
    print("Summarizing the course material...")
    study_guide_summary = summarize_text(combined_text, summarizer)

    # Wrap the summary in a LaTeX section.
    study_guide_content = r"\section{Course Material Summary}" + "\n" + study_guide_summary

    # 4. Generate the LaTeX study guide.
    tex_file = "study_guide.tex"
    generate_latex(study_guide_content, output_file=tex_file)

    # 5. Optionally compile the LaTeX file into a PDF.
    compile_choice = input("Would you like to compile the LaTeX file to PDF? (y/n): ").strip().lower()
    if compile_choice == "y":
        compile_latex(tex_file)
    else:
        print("LaTeX file generated. You can compile it manually if needed.")'''

def main():
    load_dotenv()
    #file_path = "/Users/dbhfly/Projects/study-guide-generator/test_files/1_1-full.pdf"
    #pdf_id = request_pdf(file_path)
    #print(pdf_id)
    file = "/Users/dbhfly/Projects/study-guide-generator/2025_02_20_c1557316265c2c16e256g.tex.zip"
    #unzip_latex(file, "1_1-guide")
    latex_files = get_latex_files("1_1-guide")
    study_guide = generate_study_guide(latex_files)
    print(study_guide)


if __name__ == "__main__":
    main()