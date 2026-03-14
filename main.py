from utils import llm_call, chain, extract_content, extract_xml
import sys
import json

data_processing_steps = [
    """
    Analyse the text and write it in a clear language which is easy to understand.
    """,
    """
    Extract the following fields if present: Name, Date of birth, Address, Phone, Email, Income, Employer, and all other relavent fields.
    """,
    """
    Analyse the above and then give the following information in json format in the below xml tag:

    <json_format>
    write the presonal information here in json format. also mention the document_type at last from three categories like ["banking", "travel", add you own]
    </json_format>
    """
    ]

if __name__ == "__main__":
    # Check if a path was actually provided
    if len(sys.argv) < 2:
        print("Usage: python run_ocr.py <absolute_path_to_file>")
        sys.exit(1)

    # sys.argv[0] is the script name, sys.argv[1] is the first argument (the path)
    file_path = sys.argv[1]
    
    print(f"--- Processing: {file_path} ---\n\n")
    
    data = extract_content(file_path)["raw_text"]

    final_data = chain(data, data_processing_steps)

    json_file = json.dumps(extract_xml(final_data, "json_format"))

    print(json_file)