# EY Techathon Project: Streamlining Public Service Delivery with AI

![Technologies](https://img.shields.io/badge/Technologies-React%20%7C%20FastAPI%20%7C%20PyTesseract%20%7C%20SQL%20%7C%20Selenium%20%7C%20Google%20GenAI-orange)

## Project Overview

This project, created for the EY Techathon, aims to **streamline public service delivery** for citizens who face challenges in accessing government schemes and services. Using **AI-driven solutions**, this platform simplifies the process of identifying and applying for government schemes.

### Key Features

- **Smart Data Extraction**:  
  Users can upload their Aadhaar card images, and the system will automatically extract details (name, address, age, etc.) using **PyTesseract**.
- **Manual Entry**:  
  Users can manually fill in their details like name, age, income, state, disability status, and category.
- **AI-Driven Eligibility Recommendations**:  
  Uses **Google GenAI (Gemini)** to intelligently recommend schemes based on the user’s details.
- **Batch Processing**:  
  Efficiently processes thousands of schemes using batch evaluation for eligibility through **Gemini**.
- **Seamless Navigation**:  
  Each displayed scheme includes a link redirecting users to the official government site for more details and application.

---

## Tech Stack

### Frontend

- **React**: Provides a dynamic and user-friendly interface for entering user details and viewing scheme recommendations.

### Backend

- **FastAPI**: Powers the APIs for integrating the frontend with the logic for eligibility calculation and scheme fetching.

### Data Management

- **PyTesseract**: Extracts text from Aadhaar card images for automated data input.
- **SQL Database**: Stores structured scheme data, securely encrypted.
- **Selenium**: Automates scraping of scheme details from [MyScheme.gov.in](https://myscheme.gov.in).

### AI Model

- **Google GenAI (Gemini)**: Evaluates eligibility for schemes based on complex rules using AI-driven content generation.

---

## Installation & Setup

### Prerequisites

- **Python 3.9+**
- **Node.js** (for React)
- **Tesseract OCR** (Install [here](https://github.com/tesseract-ocr/tesseract))
- **Google GenAI API Key** (Sign up [here](https://cloud.google.com/gen-ai/))

### Steps to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/ayushjpeg/EyTechanton.git
   cd EyTechanton
   ```
2. Backend Setup:
   - Navigate to the backend directory:
   ```bash
   cd backend
   ```
   - Add your Google GenAI API Key in a file named gemini.txt (stored in the backend directory).
   - Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
3. Frontend Setup:
   - Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
   - Install dependencies:
   ```bash
   npm install
   ```
   - Start the development server:
   ```bash
   npm start
   ```
4. Access the application at http://localhost:8000.

---

## Usage

### Manual Entry

1. Fill in personal details such as name, age, income, state, and category.
2. View recommended schemes based on eligibility.

### Aadhaar Upload

1. Upload the front or back side of your Aadhaar card.
2. Automatically populate your details from the extracted text.
3. View eligible schemes and redirect to their respective websites.

### Batch Processing with GenAI

1. Upload your details or fill them in manually.
2. The backend will process scheme eligibility using Google GenAI (Gemini) for large-scale evaluation of schemes.
3. Eligible schemes will be displayed based on advanced eligibility criteria matching.

---

## Demo

https://www.youtube.com/watch?v=torihMpa-ek
