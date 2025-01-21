import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import markdown2
from weasyprint import HTML

# Define the template for report generation
report_system_prompt = """You are a reporter, and you need to rewrite the given contents into a report based on the following template,
given contents delimited by ''',

the report template is: 

# Output Report: Market Entry Strategy for [Product Name]

## Overview

1. Executive Summary  
2. Product Overview  
3. Competitive Landscape  
4. Country Recommendations  
5. SWOT Analysis  
6. Financial Considerations  
7. Conclusion  

---

## 1. Executive Summary

### Objective  
A brief statement of the purpose of the analysis and the strategic objective of the market entry with the given product.  

### Product Overview  
A summary of the product being analyzed.  

### Key Insights  
Highlights from the analysis.  

### Recommendation  
A concise statement recommending the best strategy for market entry based on the analysis.  


## 2. Product Overview

### Product Description  
A brief description of the product, its features, and its value proposition.  

### Target Market  
Overview of the target market, including relevant sectors, industries, and countries.  

### Current Market Presence *(only if applicable)*  
A brief description of where the product is currently being sold or tested.  


## 3. Competitive Landscape

### Key Competitors  
List of primary competitors.  

### Market Trends  
General market trends affecting the product category, including technological advancements, regulatory changes, or government policies.  


## 4. Country Recommendations

### Recommended Country/Multiple Countries  

#### Country Overview  
Key information about the recommended country or countries, including market potential in the business and government sectors.  

#### Reasoning for Recommendation  
A brief explanation of why each country is a strong choice for market entry, considering factors like economic growth, business environment, government policies, and industry needs.  

#### Risk Considerations  
Potential risks for each recommended country (e.g., political instability, regulatory hurdles) and strategies for mitigation.  


## 5. SWOT Analysis

### Strengths  
Key advantages of the product compared to competitors in recommended country/countries.  

### Weaknesses  
Areas where the product may fall short in the context of government and business needs.  

### Opportunities  
External factors in the market (e.g., government incentives, increasing demand for such products in specific sectors).  

### Threats  
External challenges (e.g., regulatory hurdles, strong competitors, political risks).  


## 6. Financial Considerations

This section provides an overview of the financial aspects of market entry, including:
- Estimated costs
- Pricing strategies for government and business sales
- Projected revenue
- Potential financial risks, such as:
  - Currency fluctuations
  - Budget uncertainty
  - Payment delays
  - Cost overruns
  - Financial solvency of partners or clients  


## 7. Conclusion

### Best Market for Entry  
A clear recommendation of which country offers the most favorable conditions for market entry, based on the previous analysis.  

### Market Entry Strategy  
Strategic recommendations on how to enter the selected market.  

### Risk Considerations  
Overview of potential risks and mitigation strategies in the recommended market.  

### Next Steps  
Suggested steps for the company to take to move forward with the market entry, including a timeline detailing when to initiate market entry activities for each recommended country, along with clear milestones for each phase:

#### Short-Term (0-6 months)  
Steps to prepare for market entry (e.g., partnerships, regulatory approvals).  

#### Medium-Term (6-12 months)  
Activities for establishing a presence and securing contracts or business deals.  

#### Long-Term (1+ year)  
Strategic actions to expand in the market and deepen relationships with government and business stakeholders.  
"""
# regenerate the 'conversation_log.md' into 'report_content'
model = ChatOpenAI(model='gpt-4o-mini')


def generate_report(md_file_path, filename='generate_report.md'):
	"""Generate a report from a markdown file based on a given template."""
	# Load the markdown content
	with open(md_file_path, 'r') as md_file:
		results_content_md = md_file.read()

	# define model messages based on the input and desired outputs
	messages = [
		SystemMessage(content=report_system_prompt),
		HumanMessage(content=results_content_md),
	]

	report = model.invoke(messages).content

	# Ensure `report_content` is a string
	if isinstance(report, (list, dict)):
		# Convert list or dict to string
		report_content_str = (
			'\n'.join([str(item) for item in report])
			if isinstance(report, list)
			else str(report)
		)
	else:
		report_content_str = str(report)

	output_dir = os.path.dirname(md_file_path)
	rewrite_output_path = os.path.join(output_dir, filename)

	# Save the report content to a .md file
	with open(rewrite_output_path, 'w', encoding='utf-8') as md_file:
		md_file.write(report_content_str)

	print(f"Conversation log saved as '{filename}' at {rewrite_output_path}")
	return rewrite_output_path


def save_var_to_md(output_dir, ai_respond_results, filename='conversation_log.md'):
	"""
	Saves AI conversation results to a markdown file.

	Parameters:
	- output_dir (str): The directory where the file will be saved.
	- ai_respond_results (list): A list of conversation entries to be written to the file.
	- filename (str): The name of the output file (default: "conversation_log.md").

	Returns:
	- str: The full path of the saved conversation log file.
	"""
	# Ensure the directory exists
	os.makedirs(output_dir, exist_ok=True)

	# File path for the conversation log
	output_file_path = os.path.join(output_dir, filename)

	# Write conversation log to the file
	with open(output_file_path, 'w', encoding='utf-8') as md_file:
		md_file.write('# Conversation Log\n\n')
		for entry in ai_respond_results:
			md_file.write(f'{entry}\n\n')

	print(f"Conversation log saved as '{filename}' at {output_file_path}")
	return output_file_path


def markdown_to_pdf(input_md_path, filename='report.pdf'):
	"""
	Convert a Markdown file to a PDF file.

	Parameters:
	    input_md_path (str): Path to the input Markdown file.
	    output_pdf_path (str): Path to save the output PDF file.
	"""
	# Ensure the input file exists
	if not os.path.exists(input_md_path):
		raise FileNotFoundError(f'The file {input_md_path} does not exist.')

	# Read Markdown and convert to HTML
	with open(input_md_path, 'r', encoding='utf-8') as file:
		markdown_text = file.read()

	html_text = markdown2.markdown(markdown_text)
	output_dir = os.path.dirname(input_md_path)
	output_file_path = os.path.join(output_dir, filename)
	# Convert HTML to PDF
	HTML(string=html_text).write_pdf(output_file_path)

	print(f'Document is saved to {output_file_path}')


if __name__ == '__main__':
	# Example usage
	input_md_path = 'outputs/conversation_log.md'
	md_file_name = generate_report(input_md_path)
	markdown_to_pdf(md_file_name)
