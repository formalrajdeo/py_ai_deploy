
# streamlit run "/Users/aalyavora/Desktop/PDF Document Analyzer - GenAI copy/app.py"
import os
import requests
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract


def save_uploaded_file(uploaded_file):
    try:
        os.makedirs("uploaded_files", exist_ok=True)
        file_path = os.path.join("uploaded_files", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        print(f"File saved successfully: {file_path}")
        return file_path
    except Exception as e:
        print(f"Error saving file: {e}")
        return None

def extract_text_from_pdf(pdf_path):
    """Converts a PDF file to text."""
    try:
        with open(pdf_path, "rb") as f:
            pdf_reader = PdfReader(f)  # Updated class
            text = ""
            for page_num in range(len(pdf_reader.pages)):  # Updated to use len(pdf_reader.pages)
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                print(f"Page {page_num}: {page_text}")
                text += page_text or ""  # Handle cases where extract_text() returns None
        return text
    except Exception as e:
        print(f"Error converting PDF to text: {e}")
        return ""

def extract_text_from_image(image_path):
    """Extracts text from an image file using OCR."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        print(f"Extracted text from image: {text}")
        return text
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return ""

def get_assistant_response(query, text_content):
    """Sends a query to Gemini and retrieves a response using the provided text content."""
    try:
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyCdw80QhIe2sLDTf1bgO6zQ4UVI12pti8I"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"Answer the following query based on the provided text content:\n\n{query}\n\nText Content:\n{text_content}"
                        }
                    ]
                }
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        response_data = response.json()
        generated_text = response_data.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')
        if generated_text:
            return generated_text
        else:
            return "Gemini couldn't generate a response for your query."
    except requests.exceptions.RequestException as e:
        print(f"Error getting response from Gemini: {e}")
        return f"Error communicating with Gemini: {e}"
