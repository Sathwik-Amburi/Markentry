from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
from markentry.tools.tavily_search import tavily_search
import os


current_dir = os.path.dirname(__file__)

pdf_file_path = os.path.join(
	current_dir,
	'..',
	'data/Airbus/financial_statements/Airbus_2023_FinancialStatements.pdf',
)

loader = PyPDFLoader(pdf_file_path)
pages = loader.load_and_split()

# Add to vectorDB
vectorstore = Chroma.from_documents(
	documents=pages,
	collection_name='rag-chroma',
	embedding=OpenAIEmbeddings(),
)
retriever = vectorstore.as_retriever()

retriever_tool = create_retriever_tool(
	retriever,
	'retrieve_financial_statements',
	'Search and return financial insights from the Financial Statements of the given company',
)

tools = [retriever_tool, tavily_search]
