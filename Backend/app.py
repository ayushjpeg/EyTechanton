from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import google.generativeai as genai
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from typing import List
import pytesseract
from PIL import Image
import io
import re

# Configure Gemini
with open("gemini.txt", "r") as f:
    api_key = f.read().strip()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")



# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# Load CSV Data
data = pd.read_csv("data.csv")
data['Eligibility'] = data['Eligibility'].apply(eval)  # Convert string to list

# Pydantic model to parse incoming request data
class UserInfo(BaseModel):
    Name: str
    Age: int
    Gender: str
    State: str
    Income: str = None
    Category: str = None
    Disability: str = None
    Minority: str = None
    Student: str = None
    BPL: str = None
    Location: str = None
    Custom: str = None

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for specific origins (or allow all origins for development)
origins = [
    "http://localhost:3000",  # Replace with your frontend origin
    # Add other origins if needed
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)


def adhaar_read_data(text):
    res = text.split()
    name = None
    dob = None
    adh = None
    sex = None
    add = None

    nameline = []
    dobline = []
    addline = []

    text0 = []
    text1 = []
    text2 = []
    lines = text.split("\n")
    for lin in lines:
        s = lin.strip()
        s = lin.replace("\n", "")
        s = s.rstrip()
        s = s.lstrip()
        text1.append(s)

    if "female" in text.lower():
        sex = "FEMALE"
    else:
        sex = "MALE"

    text1 = list(filter(None, text1))
    text0 = text1[:]

    try:

        # Cleaning first names
        name = text0[0]
        name = name.rstrip()
        name = name.lstrip()
        name = name.replace("8", "B")
        name = name.replace("0", "D")
        name = name.replace("6", "G")
        name = name.replace("1", "I")
        name = re.sub("[^a-zA-Z] +", " ", name)

        # Cleaning DOB
        dob = text0[1][-10:]
        dob = dob.rstrip()
        dob = dob.lstrip()
        dob = dob.replace("l", "/")
        dob = dob.replace("L", "/")
        dob = dob.replace("I", "/")
        dob = dob.replace("i", "/")
        dob = dob.replace("|", "/")
        dob = dob.replace('"', "/1")
        dob = dob.replace(":", "")
        dob = dob.replace(" ", "")

        # Cleaning Adhaar number details
        aadhar_number = ""
        count = 0
        for word in res:
            if len(word) == 4 and word.isdigit():
                aadhar_number = aadhar_number + word + " "
                count += 1
                if count > 2:
                    break
        if len(aadhar_number) >= 12:
            print("Aadhar number is :" + aadhar_number)
        else:
            print("Aadhar number not read")
        adh = aadhar_number

        # cleaning address
        text0 = findword(
            text1, ("Address|Adress|ddress|Addess|Addrss|Addres|Add|Ad|Location)$")
        )
        addline = text0[0]
        add = addline.rstrip()
        add = add.lstrip()
        add = add.replace(" ", "")
        add = add.replace('"', "")
        add = add.replace(";", "")
        add = add.replace("%", "L")
    except:
        pass

    data = {}
    data["Name"] = name
    data["DOB"] = dob
    data["Document Number"] = adh
    data["Sex"] = sex
    data["Document Type"] = "Aadhaar"
    return data


def findword(textlist, wordstring):
    lineno = -1
    for wordline in textlist:
        xx = wordline.split()
        if [w for w in xx if re.search(wordstring, w)]:
            lineno = textlist.index(wordline)
            textlist = textlist[lineno + 1 :]
            return textlist
    return textlist




# Pre-Filtering Function
def prefilter_schemes(data, user_info):
    """
    Filter schemes based on user's basic information (e.g., age, state, etc.).
    """
    filtered_data = []
    for _, row in data.iterrows():
        region = row['Region']
        eligibility = row['Eligibility']

        # Basic checks: State, Age, and Category
        if (
                (not region or region.lower() == user_info["State"].lower() or "Ministry" in region) and
                (not any("age" in crit.lower() and str(user_info["Age"]) not in crit for crit in eligibility)) and
                (not any(
                    "category" in crit.lower() and user_info.get("Category", "").lower() not in crit.lower() for crit in
                    eligibility))
        ):
            filtered_data.append(row)
    return pd.DataFrame(filtered_data)








def check_batch_with_gemini(batch, user_details):
    """
    Use Gemini to evaluate eligibility for a batch of schemes, considering state-specific logic.
    """
    prompt = (
        f"Based on the user's details, determine the best-suited schemes they are eligible for. make sure if a scheme requires a particular state then it must be same as users and if user has told his category or minority status or income or whether he/she is a student or not and also check the custom information and answer accordingly tell only the schemes which they are eligible for dont tell irrevelant schemes\n\n"
        f"User Details: {user_details}\n\n"
        f"Schemes and Eligibility Criteria:\n"
    )
    for _, row in batch.iterrows():
        prompt += (
            f"- Scheme: {row['Scheme Name']}\n"
            f"  Eligibility: {row['Eligibility']}\n"
            f"  URL: {row['URL']}\n"
            f"  Region: {row['Region']}\n"
            f"  Tags: {row['Tags']}\n"
        )

    prompt += (
        "\nRespond in JSON format with the following fields for each eligible scheme:\n"
        "{\n"
        "  'Scheme Name': '<Name>',\n"
        "  'Scheme URL': '<URL>',\n"
        "  'Tags': ['<Tag1>', '<Tag2>', ...],\n"
        "  'Eligibility Criteria to Verify': ['<Criteria1>', '<Criteria2>', ...]\n"
        "}\n"
    )

    response = model.generate_content(prompt)
    return response.text




@app.post("/api/submit")
async def submit_details(user_info: UserInfo):
    # Convert user info to a dictionary for processing
    user_info_dict = user_info.dict()
    print(user_info_dict)

    # Batch processing for Gemini (if applicable)
    BATCH_SIZE = 3000
    eligible_schemes = []
    filtered_data = prefilter_schemes(data, user_info_dict)

    for i in range(0, len(filtered_data), BATCH_SIZE):
        batch = filtered_data.iloc[i:i + BATCH_SIZE]
        gemini_response = check_batch_with_gemini(batch, user_info_dict)
        print(f"Processing batch {i // BATCH_SIZE + 1}...")  # Optional progress indicator
        eligible_schemes.append(gemini_response)

    # Respond with filtered schemes and Gemini results
    print(eligible_schemes)
    return {
        "status": "success",
        "result": eligible_schemes
    }


# @app.post("/upload")
# async def upload_files(files: List[UploadFile]):
#     extracted_data = []
#     for file in files:
#         try:
#             # Read file content
#             contents = await file.read()
#             image = Image.open(io.BytesIO(contents))
#
#             # Extract text from image using pytesseract
#             text = pytesseract.image_to_string(image)
#
#             # Detect document type and extract relevant data
#
#             data = adhaar_read_data(text)
#
#             extracted_data.append(data)
#         except Exception as e:
#             return JSONResponse(
#                 content={"error": f"Failed to process file {file.filename}: {str(e)}"},
#                 status_code=400,
#             )
#     print(extracted_data)
#     return {"extracted_data": extracted_data}

@app.post("/upload")
async def upload_files(files: List[UploadFile]):
    extracted_data = []
    try:
        # Hardcoded data for now
        data = {
            "Name": "Ayush",
            "Age": 21,
            "Gender": "Male",
            "State": "West Bengal"
        }
        extracted_data.append(data)

    except Exception as e:
        return JSONResponse(
            content={"error": f"Failed to process file: {str(e)}"},
            status_code=400,
        )

    print(extracted_data)
    return {"extracted_data": extracted_data}

if __name__ == "__main__":
    import uvicorn
    # Running the FastAPI app with uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)