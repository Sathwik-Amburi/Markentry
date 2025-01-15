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
    'data/Airbus/financial_statements/Airbus_ConsolidatedData.pdf'
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

get_product_insights_tool = create_retriever_tool(
	retriever,
	'get_product_insights',
	'Search and return product insights from the relevant product documents',
)