'''convert files in test_files to latex text'''
import os
import requests
import json

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

