from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

import langchain
from langchain_openai import OpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources.loading import load_qa_with_sources_chain
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.schema import Document
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import tiktoken
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from dotenv import load_dotenv
import os
import pickle
import faiss  # Make sure you have FAISS installed
import pdfplumber
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter

from utils.pdf_service import PDFService
from utils import mongodb_service
from models.message import DB_Message


load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_SECRET_KEY")

PDF_FOLDER = "documents"
VECTOR_DATABASE_FOLDER = "vector_database/"
FILE_PATH = "faiss_store_openai.pkl"  # Change extension to .index for clarity

llm = OpenAI(temperature=0.6)

splitter = RecursiveCharacterTextSplitter(
  separators = ['\n\n', '\n', '.', ','],
  chunk_size = 1000,
)

embeddings = OpenAIEmbeddings()


######################################################

def prompt(query):
    # # Create the RetrievalQA chain using the vectorstore as retriever
    # chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())

    # # Query the chain with your question
    # result = chain.invoke({"question": "Quyền và nhiệm vụ của sinh viên là gì trong văn bản quy chế công tác sinh viên"}, return_only_outputs=True)

    query = "Quyền và nhiệm vụ của sinh viên là gì trong văn bản quy chế công tác sinh viên?"
    relevant_docs = retriever.invoke(query)

    response_content = "\n--- Relevant Documents ---\n"
    for i, doc in enumerate(relevant_docs, 1):
        response_content += f"Document {i}:\n{doc.page_content}\n"
        if doc.metadata:
            source = doc.metadata.get('source', 'Unknown')
            response_content += f"Source: {source}\n"
    return HttpResponse(response_content)


# def get_existing_files_in_index(file_path):
#     if os.path.exists(file_path):
#         # Load the FAISS index to check which files are already included
#         # Assuming you can extract file names from the documents indexed in the FAISS index
#         # For example, by using document metadata or hashing the file names
#         pass
#     return []  # Return a list of file names already indexed


# def has_new_or_updated_files(documents_folder_files, existing_files):
#     new_files = [file for file in documents_folder_files if file not in existing_files]
#     return len(new_files) > 0


# def load_all_pdfs(folder_path):
#     documents = []

#     for file in os.listdir(folder_path):
#         if file.endswith(".pdf"):
#             pdf_path = os.path.join(folder_path, file)
#             print(f"Processing: {pdf_path}")

#             # Use pdfplumber or the original loader to extract text
#             with pdfplumber.open(pdf_path) as pdf:
#                 for page in pdf.pages:
#                     text = page.extract_text()
#                     if text:  # Only add pages with valid text
#                         documents.append(
#                             Document(
#                                 page_content=text,
#                                 metadata={"source": pdf_path}
#                             )
#                         )

#     print(f"Loaded {len(documents)} pages from PDFs.")
#     return documents

## PDF FILE PROCESSEING
def load_all_pdfs(folder_path):
    """
    Load all PDFs in a folder, extract text from each page, and fallback to OCR when needed.
    :param folder_path: Path to the folder containing PDF files.
    :return: List of LangChain Document objects containing extracted text and metadata.
    """
    documents = []

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, file)
            print(f"Processing: {pdf_path}")

            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for page_number, page in enumerate(pdf.pages, start=1):
                        # Extract text using pdfplumber
                        text = page.extract_text()

                        # If no text is found, fallback to OCR
                        if not text or text.strip() == "":
                            print(f"No text found on page {page_number}, using OCR...")
                            text = PDFService.extract_text_with_ocr(pdf_path, page_number)

                        # Append text to documents if valid
                        if text and text.strip():
                            documents.append(
                                Document(
                                    page_content=text,
                                    metadata={"source": pdf_path, "page": page_number}
                                )
                            )
            except Exception as e:
                print(f"Error processing file {file}: {e}")

    print(f"Loaded {len(documents)} pages from PDFs.")
    return documents
#####################################################

## VECTOR DATABASE
def create_vector_database(file_path, folder_path):
    documents = load_all_pdfs(folder_path)
    if not documents:
        print("No documents found to create the vector database.")
        return

    # Create a new FAISS index with OpenAI embeddings
    chunks = splitter.split_documents(documents)
    vectorstore_openai = FAISS.from_documents(chunks, embeddings)
    print(f"Created FAISS index with {len(chunks)} documents.")
    
    # Save the FAISS index to disk
    vectorstore_openai.save_local(VECTOR_DATABASE_FOLDER)
    print(f"FAISS vector database created and saved to {VECTOR_DATABASE_FOLDER}")


def update_vector_database(file_path, folder_path):
    new_documents = load_all_pdfs(folder_path)
    if not new_documents:
        print("No new documents found to update the vector database.")
        return

    # Load existing FAISS index using FAISS's read_index
    if os.path.exists(file_path):
        index = faiss.read_index(file_path)
        vectorstore_openai = FAISS(index)
        print(f"Loaded existing FAISS vector database with {vectorstore_openai.index.ntotal} documents.")
    else:
        print("Error: FAISS index file does not exist. Please create the database first.")
        return

    # Add new documents to the existing FAISS index
    vectorstore_openai.add_documents(new_documents)
    print(f"Added {len(new_documents)} new documents to the FAISS index.")

    # Save the updated FAISS index back to the file
    faiss.write_index(vectorstore_openai.index, file_path)
    print(f"FAISS vector database updated and saved to {file_path}")



## INITAILIZATION
if os.path.exists(VECTOR_DATABASE_FOLDER):
        # Load the existing FAISS index with deserialization enabled
        vectorstore = FAISS.load_local(VECTOR_DATABASE_FOLDER, embeddings=embeddings, allow_dangerous_deserialization=True)
else:
    # If the FAISS index doesn't exist, create it
    create_vector_database(FILE_PATH, PDF_FOLDER)
    # Load the newly created FAISS index
    vectorstore = FAISS.load_local(VECTOR_DATABASE_FOLDER, embeddings=embeddings, allow_dangerous_deserialization=True)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3},
)

# Contextualize question prompt
# This system prompt helps the AI understand that it should reformulate the question
# based on the chat history to make it a standalone question
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, just "
    "reformulate it if needed and otherwise return it as is."
)

# Create a prompt template for contextualizing questions
contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# Create a history-aware retriever
# This uses the LLM to help reformulate the question based on chat history
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

# Answer question prompt
# This system prompt helps the AI understand that it should provide concise answers
# based on the retrieved context and indicates what to do if the answer is unknown
qa_system_prompt = (
    "You are an assistant for question-answering tasks. Use "
    "the following pieces of retrieved context to answer the "
    "question. If you don't know the answer, just say that you "
    "don't know. Use three sentences maximum and keep the answer "
    "concise."
    "\n\n"
    "{context}"
)

# Create a prompt template for answering questions
qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

# Create a chain to combine documents for question answering
# `create_stuff_documents_chain` feeds all retrieved context into the LLM
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

# Create a retrieval chain that combines the history-aware retriever and the question answering chain
rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)


# Get chat_history from database
chat_history = []  # Collect chat history here (a sequence of messages)

#langchain.debug = True

MAX_TOKENS = 4096

# You can use a token counting function (e.g., tiktoken for OpenAI models)
def calculate_token_count(messages):
    # Assuming you're using OpenAI's models, you'd use their tokenizer
    enc = tiktoken.get_encoding("cl100k_base")  # OpenAI GPT models use this encoding
    total_tokens = 0
    for message in messages:
        total_tokens += len(enc.encode(message.content))
    return total_tokens

# Function to ensure chat history stays within token limit
def enforce_token_limit(chat_history):
    total_tokens = calculate_token_count(chat_history)
    while total_tokens > MAX_TOKENS:
        chat_history.pop(0)  # Remove the oldest message
        total_tokens = calculate_token_count(chat_history)
    return chat_history

@csrf_exempt  # Disable CSRF validation for testing purposes (ensure to enable CSRF protection in production)
def chat(request):
    if request.method == "POST":
        try:
            # Parse the incoming JSON request body
            data = json.loads(request.body)
            query = data.get('message', '')
            chatId = data.get('chatId', '')

            # Ensure that query is not empty
            if not query:
                return JsonResponse({'error': 'Message cannot be empty'}, status=400)

            relevant_docs = retriever.invoke(query)

            msg_collection = DB_Message.objects(ChatId=chatId).order_by('CreateAt')[:5]
            for msg in msg_collection:
                chat_history.append(HumanMessage(content=msg.User))
                chat_history.append(SystemMessage(content=msg.System))

            enforce_token_limit(chat_history)

            # Process the user's query through the retrieval chain
            result = rag_chain.invoke({"input": query, "chat_history": chat_history})

            # Ensure result has an answer
            response_content = result.get('answer', 'Sorry, I did not understand the question.')
            response_sources = [doc.metadata.get('source', 'Unknown') for doc in relevant_docs]

            # Add query and AI response to chat history
            # mongodb_service.connect_mongoengine()
            message = DB_Message(
                ChatId = chatId,
                User = query,
                System = response_content,
            )
            message.save()

            chat_history.append(HumanMessage(content=query))
            chat_history.append(SystemMessage(content=response_content))

            # Return the response in proper encoding
            return JsonResponse({'response': response_content, 'sources': response_sources}, json_dumps_params={'ensure_ascii': False})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            # In case of any other errors, log the exception and return a generic error message
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


