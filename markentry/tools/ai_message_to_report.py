import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

# Define the template for report generation
report_system_prompt = """You are a reporter, and you need to rewrite the given contents into a report based on the following template,
given contents delimited by ''',

the report template is: 

Output Report: Market Entry Strategy for [Product Name]

Overview 

1) Executive Summary 
2) Product Overview 
3) Competitive Landscape 
4) Country Recommendations
5) SWOT Analysis
6) Financial Considerations 
7) Conclusion

1. Executive Summary

Objective: 
A brief statement of the purpose of the analysis and the strategic objective of the market entry with the given product

Product Overview: 
A summary of the product being analyzed.

Key Insights: 
Highlights from the analysis 

Recommendation: 
A concise statement recommending the best strategy for market entry based on the analysis


2. Product Overview

Product Description: 
A brief description of the product, its features, and its value proposition

Target Market: 
Overview of the target market, including relevant sectors, industries, and countries

Current Market Presence (only if applicable): 
A brief description of where the product is currently being sold or tested

3. Competitive Landscape

Key Competitors: List of primary competitors 

Market Trends: General market trends affecting the product category, including technological advancements, regulatory changes, or government policies.


4. Country Recommendations
Recommended Country/Multiple Countries:
Country Overview: 
Key information about the recommended country or countries, including market potential in the business and government sectors.

Reasoning for Recommendation: 
A brief explanation of why each country is a strong choice for market entry, considering factors like economic growth, business environment, government policies, and industry needs.

Risk Considerations: Potential risks for each recommended country (e.g., political instability, regulatory hurdles) and strategies for mitigation.

5. SWOT Analysis 

Strengths: 
Key advantages of the product compared to competitors in recommended country/countries

Weaknesses: 
Areas where the product may fall short in the context of government and business needs.

Opportunities: 
External factors in the market (e.g., government incentives, increasing demand for such products in specific sectors)

Threats: 
External challenges (e.g., regulatory hurdles, strong competitors, political risks)


6. Financial Considerations
This section provides an overview of the financial aspects of market entry, including estimated costs, pricing strategies for government and business sales, projected revenue, and potential financial risks such as currency fluctuations, budget uncertainty, payment delays, cost overruns, and the financial solvency of partners or clients.

7. Conclusion 

Best Market for Entry: 
A clear recommendation of which country offers the most favorable conditions for market entry, based on the previous analysis.

Market Entry Strategy: 
Strategic recommendations on how to enter the selected market

Risk Considerations: 
Overview of potential risks and mitigation strategies in the recommended market

Next Steps: 
Suggested steps for the company to take to move forward with the market entry, including a timeline detailing when to initiate market entry activities for each recommended country, along with clear milestones for each phase (e.g., market research, partner search, government tenders).
Short-Term (0-6 months): Steps to prepare for market entry (e.g., partnerships, regulatory approvals).
Medium-Term (6-12 months): Activities for establishing a presence and securing contracts or business deals.
Long-Term (1+ year): Strategic actions to expand in the market and deepen relationships with government and business stakeholders.

"""


def generate_report_from_markdown(md_file_path, model, output_dir):
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

	# # Ensure the directory exists
	# os.makedirs(output_dir, exist_ok=True)

	# # File path for the conversation log
	# output_md_path = os.path.join(output_dir, "rewrite_conversation_log.md")

	# # Check if the file exists
	# if os.path.exists(md_file_path):
	#     # If the file exists, delete it
	#     os.remove(md_file_path)
	#     print(f"Existing file 'rewrite_conversation_log.md' deleted from {output_dir}")

	# # create the file
	# with open(output_md_path, "w", encoding="utf-8") as md_file:
	#     md_file.write("# Conversation Log\n\n")
	#     for entry in report:
	#         md_file.write(f"{entry}\n\n")

	# print(f"Conversation log saved as 'conversation_log.md' at {output_md_path}")
	return report


if __name__ == '__main__':
	# rewrite the report according to report template
	model = ChatOpenAI(model='gpt-4o-mini')
	# Load the ai_response content
	md_file_path = 'markentry/outputs/conversation_log.md'
	# Directory where the output .md file will be saved
	output_dir = 'markentry/outputs'
	output_pdf_path = os.path.join(output_dir, 'rewrite_conversation_log.pdf')
	# Generate the report and save as Markdown
	report_content = generate_report_from_markdown(md_file_path, model, output_dir)
	print(report_content)
