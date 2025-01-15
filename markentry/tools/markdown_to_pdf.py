import markdown2
from weasyprint import HTML
import os

def markdown_to_pdf(input_md_path, output_pdf_path):
    """
    Convert a Markdown file to a PDF file.

    Parameters:
        input_md_path (str): Path to the input Markdown file.
        output_pdf_path (str): Path to save the output PDF file.
    """
    # Ensure the input file exists
    if not os.path.exists(input_md_path):
        raise FileNotFoundError(f"The file {input_md_path} does not exist.")

    # Read Markdown and convert to HTML
    with open(input_md_path, "r", encoding="utf-8") as file:
        markdown_text = file.read()

    html_text = markdown2.markdown(markdown_text)

    # Convert HTML to PDF
    HTML(string=html_text).write_pdf(output_pdf_path)

    print(f"Document is saved to {output_pdf_path}")

if __name__ == "__main__":
    # Example usage
    input_md_path = "/Users/taizhang/Desktop/Markentry/markentry/outputs/rewrite_conversation_log.md"
    output_pdf_path = "/Users/taizhang/Desktop/Markentry/markentry/outputs/rewrite_conversation_log.pdf"

    markdown_to_pdf(input_md_path, output_pdf_path)