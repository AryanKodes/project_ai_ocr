import fitz  # PyMuPDF
import easyocr
import os
import warnings
import sys
from groq import Groq
from dotenv import load_dotenv
import re

load_dotenv()
api_key=os.environ.get("GROQ_API_KEY")

# Suppress the PyTorch MPS warning to keep the console clean
warnings.filterwarnings("ignore", category=UserWarning, module="torch")

def extract_content(file_path):
    # Ensure we handle absolute paths and spaces correctly
    abs_path = os.path.abspath(os.path.expanduser(file_path))
    
    if not os.path.exists(abs_path):
        return {"error": f"File not found at: {abs_path}"}

    results = {
        "raw_text": "",
        "metadata": {},
        "pages_count": 0
    }
    
    # gpu=True uses your Mac's MPS or NVIDIA's CUDA; set to False if it's too slow
    reader = easyocr.Reader(['en'], gpu=True)

    if abs_path.lower().endswith('.pdf'):
        doc = fitz.open(abs_path)
        results["pages_count"] = len(doc)
        results["metadata"] = doc.metadata

        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            if not text.strip():
                # For scanned PDFs: Convert page to image bytes for EasyOCR
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # Higher res for better OCR
                img_data = pix.tobytes("png")
                ocr_result = reader.readtext(img_data, detail=0)
                text = " ".join(ocr_result)
            
            results["raw_text"] += f"\n--- Page {page_num + 1} ---\n{text}"

    elif abs_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        ocr_result = reader.readtext(abs_path, detail=0)
        results["raw_text"] = " ".join(ocr_result)
        results["pages_count"] = 1

    return results


def llm_call(prompt: str, system_prompt: str = "", model="llama-3.1-8b-instant") -> str:
    """
    Calls the Groq model with the given prompt and returns the response.
    Matches the signature and behavior of the Anthropic helper.
    """
    client = Groq(api_key=api_key)
    
    # Construct messages list to include system prompt if provided
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    stream = client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=0.1, # Match Anthropic's low temperature for consistency
        stream=True,
    )

    full_response = ""
    for chunk in stream:
        # Accessing content using the standard Groq/OpenAI chunk structure
        content = chunk.choices[0].delta.content
        if content:
            # We keep the print to mimic your previous behavior, 
            # but ensure the string is returned for extract_xml
            # print(content.replace("*", ""), end="")
            full_response += content

    return full_response

def chain(input: str, prompts: list[str]) -> str:
    """
    Chain multiple LLM calls sequentially, passing results between steps.
    """
    result = input
    for i, prompt in enumerate(prompts, 1):
        # print(f"\nStep {i}:")
        result = llm_call(f"{prompt}\nInput: {result}")
        # print(result)
    return result

def extract_xml(text: str, tag: str) -> str:
    """
    Extracts the content of the specified XML tag from the given text. Used for parsing structured responses

    Args:
        text (str): The text containing the XML.
        tag (str): The XML tag to extract content from.

    Returns:
        str: The content of the specified XML tag, or an empty string if the tag is not found.
    """
    match = re.search(f"<{tag}>(.*?)</{tag}>", text, re.DOTALL)
    return match.group(1) if match else ""