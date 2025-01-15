from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.tools.retriever import create_retriever_tool
import os


current_dir = os.path.dirname(__file__)

competitor_data_file_path = os.path.join(
	current_dir,
	'..',
	'data/RAG_Data-CompetitiorExpert.pdf',
)

loader = PyPDFLoader(competitor_data_file_path)
pages = loader.load_and_split()

# Add to vectorDB
vectorstore = Chroma.from_documents(
	documents=pages,
	collection_name='rag-chroma',
	embedding=OpenAIEmbeddings(),
)
retriever = vectorstore.as_retriever()

competitor_data_retriever_tool = create_retriever_tool(
	retriever,
	'retrieve_competitor_data',
	'Search and return information about competitors of the given company',
)
