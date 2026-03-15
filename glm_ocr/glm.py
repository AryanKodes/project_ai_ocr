from glmocr import GlmOcr

# Initialize with custom config
with GlmOcr(config_path="config.yaml") as parser:
    result = parser.parse("<your_file_path>")
    print(result.markdown_result)
    
