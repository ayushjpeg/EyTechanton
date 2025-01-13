import pandas as pd
import google.generativeai as genai

# Configure Gemini
with open("gemini.txt", "r") as f:
    api_key = f.read().strip()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Load CSV Data
data = pd.read_csv("data.csv")

# Preprocess Eligibility Rules
data['Eligibility'] = data['Eligibility'].apply(eval)  # Convert string to list


# Gather User Information
def get_user_info():
    user_info = {}
    # Mandatory fields
    user_info["Name"] = input("Enter your name: ").strip()
    user_info["State"] = input("Enter your state: ").strip()
    user_info["Age"] = int(input("Enter your age: ").strip())
    user_info["Gender"] = input("Enter your gender (M/F/Other): ").strip()
    # Optional fields
    optional_fields = ["Income", "Category", "Disability", "Minority", "Student", "BPL", "Urban/Rural"]
    for field in optional_fields:
        response = input(f"Do you want to provide {field} information? (yes/no): ").strip().lower()
        if response == "yes":
            user_info[field] = input(f"Enter {field}: ").strip()
    # Custom input
    custom_response = input("Do you want to provide any custom information? (yes/no): ").strip().lower()
    if custom_response == "yes":
        user_info["Custom"] = input("Enter custom information: ").strip()
    return user_info


user_info = get_user_info()


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


filtered_data = prefilter_schemes(data, user_info)

# Batch Processing
BATCH_SIZE = 3000


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


# Evaluate Filtered Schemes in Batches
eligible_schemes = []
for i in range(0, len(filtered_data), BATCH_SIZE):
    batch = filtered_data.iloc[i:i + BATCH_SIZE]
    gemini_response = check_batch_with_gemini(batch, user_info)
    print(f"Processing batch {i // BATCH_SIZE + 1}...")  # Optional progress indicator
    eligible_schemes.append(gemini_response)

# Display Results
print("\nThe best-suited schemes for you:")
for response in eligible_schemes:
    print(response)
