
import sys
from utils import extract_content

if __name__ == "__main__":
    # Check if a path was actually provided
    if len(sys.argv) < 2:
        print("Usage: python run_ocr.py <absolute_path_to_file>")
        sys.exit(1)

    # sys.argv[0] is the script name, sys.argv[1] is the first argument (the path)
    file_path = sys.argv[1]
    
    print(f"--- Processing: {file_path} ---\n\n")
    
    data = extract_content(file_path)
    
    # Print the result
    print(f"\n\n{data}\n\n")