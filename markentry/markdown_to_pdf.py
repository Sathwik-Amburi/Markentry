import markdown2
from weasyprint import HTML


file_path = "/Users/taizhang/Desktop/Markentry/markentry/outputs/conversation_log.md"

output_path = "/Users/taizhang/Desktop/Markentry/markentry/outputs/conversation_log.pdf"
# Read Markdown and convert to HTML
with open(file_path, "r", encoding="utf-8") as file:
    markdown_text = file.read()

html_text = markdown2.markdown(markdown_text)

# Convert HTML to PDF
HTML(string=html_text).write_pdf(output_path)

print(f"Document is saved to {output_path}")
