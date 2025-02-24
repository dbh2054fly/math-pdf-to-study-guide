'''convert files in test_files to latex text'''
import os
import requests
import json
import zipfile
import time

def request_pdf(file_path):
    '''takes absolute path to pdf file and returns extraction id from mathpix. The extraction id is used to get the latex from mathpix.'''
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
    
    return response.json()["pdf_id"]

def get_latex(pdf_id, target_dir, max_attempts=60, sleep_time=5):
    '''takes extraction id and returns the file name of the latex file. The latex file is downloaded from mathpix and saved in the target directory.'''
    headers = {
        "app_id": os.getenv("APP_ID"),
        "app_key": os.getenv("APP_KEY")
    }
    status_url = f"https://api.mathpix.com/v3/pdf/{pdf_id}"
    attempts = 0
    while attempts < max_attempts:
        response = requests.get(status_url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to get latex status from mathpix: {response.status_code} {response.text}")
        status = response.json()
        print(status)
        if "status" not in status:
            print("Status key not found in response, waiting for job to initialize...")
            attempts += 1
            time.sleep(sleep_time)
            continue
        if status["status"] == "completed":
            break
        attempts += 1
        time.sleep(sleep_time)
    if attempts == max_attempts:
        raise Exception("Too many attempts, failed to get latex from mathpix")
    
    url = "https://api.mathpix.com/v3/pdf/" + pdf_id + ".tex"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to get latex from mathpix: {response.status_code} {response.text}")
    
    output_file_name = pdf_id + ".tex.zip"
    full_path = os.path.join(target_dir, output_file_name)
    with open(full_path, "wb") as f:
        f.write(response.content)
    return output_file_name

def unzip_latex(zip_file_name, directory):
    '''unzip latex file'''
    full_path = directory + "/" + zip_file_name
    with zipfile.ZipFile(full_path, "r") as zip_ref:
        zip_ref.extractall(directory)
    return zip_file_name.replace(".zip", "")
    

def get_latex_files(file_list, directory):
    '''get all latex files in the target directory'''
    '''Recursively find and read .tex files from a directory'''

    latex_files_content = []

    for root, dirs, files in os.walk(directory):
        # Calculate current depth by counting path separators
        current_depth = root.count(os.path.sep) - directory.count(os.path.sep)
        
        # If we're already at depth 1 (first level of subdirectories),
        # clear the dirs list to prevent further descent
        if current_depth > 1:
            dirs[:] = []  # This prevents os.walk from going deeper
        
        # Process files as before
        for file in files:
            if file in file_list: 
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    latex_files_content.append(f.read())

    return latex_files_content
