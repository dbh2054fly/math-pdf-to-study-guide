This is a tool to generate a study guide from a set of lecture slides.

## Usage

1. Install the requirements

```bash
pip install -r requirements.txt
```

2. get API keys from OpenAI and Mathpix

3. Create a new directory called test_files

4. Create a new directory within test_files of your choice

5. Put the pdf files in the new directory

6. Run the script and specify your directory's relative path to test_files

```bash
python main.py
```

## Requirements

- Python 3.10+
- OpenAI API key
- Mathpix API key


User flow:

As a user, I want to import the pdf files for a subject into a new directory within the test_files directory.
I then want to simply run the script, input the relative path to the directory, and generate an output latex file within the same directory.

Unzip flow:

1. The user specifies the relative path to the directory with the pdf files.
2. Obtain the absolute path to the directory with the pdf files.
3. For each pdf file within the directory, obtain the pdf id from mathpix.
4. For each pdf id, get the latex zip file from mathpix and save into the directory that the user specified. At this point, the directory contains the pdf files and the latex zip files.
5. Unzip the latex zip files within the directory. At this point, the directory contains the pdf files, the latex zip files, and subdirectories each with its respective latex file and image directory.
6. Read the contents of each latex file and put them into a list of text. 
7. Generate a study guide from the list of latex files.

