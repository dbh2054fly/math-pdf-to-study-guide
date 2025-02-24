'''convert files in test_files to latex text'''
import os
import requests
import json
import zipfile
def request_pdf(file_path):
    '''request pdf from mathpix'''
    options = {
        "conversion_formats": {
            "tex.zip": True
        }
    }
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found{file_path}")
    
    with open(file_path, "rb") as f:
        response = requests.post(
            "https://api.mathpix.com/v3/pdf",
            headers={
                "app_id": os.getenv("APP_ID"),
                "app_key": os.getenv("APP_KEY")
            },
            data={
                "options_json": json.dumps(options)
            },
            files={
                "file": f
            }
        )
    
    if response.status_code != 200:
        raise Exception(f"Failed to request pdf from mathpix: {response.status_code} {response.text}")
    
    return response.json()

def get_latex(pdf_id):
    '''get latex from mathpix'''
    headers = {
        "app_id": os.getenv("APP_ID"),
        "app_key": os.getenv("APP_KEY")
    }
    url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".tex"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to get latex from mathpix: {response.status_code} {response.text}")
    output_file_name = pdf_id + ".tex.zip"
    with open(output_file_name, "wb") as f:
        f.write(response.content)
    return output_file_name

def unzip_latex(zip_file_name, target_dir):
    '''unzip latex file'''
    with zipfile.ZipFile(zip_file_name, "r") as zip_ref:
        zip_ref.extractall("/Users/dbhfly/Projects/study-guide-generator/test_files/" + target_dir)
    return zip_file_name.replace(".zip", "")
    

def get_latex_files(target_dir):
    '''get all latex files in the target directory'''
    '''Recursively find and read .tex files from a nested directory'''
    base_path = "/Users/dbhfly/Projects/study-guide-generator/test_files/"
    full_target_path = os.path.join(base_path, target_dir)

    latex_files_content = []

    for root, _, files in os.walk(full_target_path):  # Recursively iterate through directories
        for file in files:
            if file.endswith(".tex"):  # Ensure we only process .tex files
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    latex_files_content.append(f.read())  

    return latex_files_content
