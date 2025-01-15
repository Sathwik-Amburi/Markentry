from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
import os


current_dir = os.path.dirname(__file__)

file_path = os.path.join(current_dir, '..', 'TestFile-ProductExpert.pdf')

loader = PyPDFLoader(file_path)
pages = loader.load_and_split()

# Add to vectorDB
vectorstore = Chroma.from_documents(
	documents=pages,
	collection_name='rag-chroma',
	embedding=OpenAIEmbeddings(),
)
retriever = vectorstore.as_retriever()

product_data_retriever_tool = create_retriever_tool(
	retriever,
	'retrieve_product_data',
	'Search and return product-related information of the given company',
)
