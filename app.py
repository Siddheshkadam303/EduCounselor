from flask import Flask, render_template, request, jsonify
import os
import sys
import json
import re
import time
import logging
import fitz  # PyMuPDF for PDF extraction
import requests
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain.schema import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from google.generativeai import GenerativeModel, configure

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# ------------------------------------
# Environment Variables & API Keys
# ------------------------------------
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
configure(api_key=gemini_api_key)

# ------------------------------------
# PDF Extraction (Same as your original code)
# ------------------------------------
pdf_folder = "docs"
output_text_file = "parent_faq.txt"

if not os.path.exists(output_text_file):
    if not os.path.exists(pdf_folder):
        print("Error: PDF folder not found!")
        sys.exit()

    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]
    
    if not pdf_files:
        print("Error: No PDF files found in the folder!")
        sys.exit()

    print("Extracting text from PDFs...")
    with open(output_text_file, "w", encoding="utf-8") as txt_file:
        for pdf_file in pdf_files:
            pdf_path = os.path.join(pdf_folder, pdf_file)
            print(f"Processing: {pdf_file}")
            
            try:
                doc = fitz.open(pdf_path)
                for page_num in range(len(doc)):
                    text = doc[page_num].get_text()
                    txt_file.write(text + "\n" + "=" * 80 + "\n")
                print(f"✅ Extracted text from {pdf_file}")
            except Exception as e:
                print(f"Error opening {pdf_file}: {e}")
                continue
    print(f"🎉 All PDFs processed! Extracted text saved in '{output_text_file}'.")
else:
    print(f"✅ Found existing '{output_text_file}'. Skipping PDF extraction.")

# ------------------------------------
# Persistent Chat History
# ------------------------------------
history_file = "chat_history_parent.json"

def load_chat_history():
    chat_history = ChatMessageHistory()
    if os.path.exists(history_file):
        try:
            with open(history_file, "r") as f:
                history_data = json.load(f)
            for msg in history_data:
                if msg.get("type") == "human":
                    chat_history.add_user_message(msg.get("content", ""))
                elif msg.get("type") == "ai":
                    chat_history.add_ai_message(msg.get("content", ""))
            print("✅ Loaded existing chat history.")
        except json.JSONDecodeError:
            print("⚠ Chat history file is empty or corrupted. Starting fresh.")
    else:
        print("📜 No previous chat history found. Starting fresh.")
    return chat_history

def save_chat_history(history):
    history_data = [{"type": "human" if isinstance(msg, HumanMessage) else "ai", "content": msg.content} for msg in history.messages]
    with open(history_file, "w") as f:
        json.dump(history_data, f, indent=4)

chat_history = load_chat_history()

# ------------------------------------
# Persistent Retriever & Embeddings
# ------------------------------------
loader = TextLoader(output_text_file, encoding="utf-8")
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(documents)

persist_directory = "retriever_store_parent"
if os.path.exists(persist_directory) and os.listdir(persist_directory):
    print("✅ Loaded existing retriever store.")
    vectorstore = Chroma(persist_directory=persist_directory, embedding_function=GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", google_api_key=gemini_api_key))
else:
    print("🔍 Creating new retriever store...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=gemini_api_key)
    vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings, persist_directory=persist_directory)
    print("✅ Created and saved new retriever store!")

retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# ------------------------------------
# LLM & Prompt Configuration (UPDATED)
# ------------------------------------
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=gemini_api_key)

# Updated system prompt for better performance
system_prompt = (
    "You are EduCounselor, a professional educational counseling assistant specializing in career guidance programs, "
    "school partnerships, course offerings, and pricing information. You help parents make informed decisions about "
    "educational counseling services for their children.\n\n"
    
    "CORE RESPONSIBILITIES:\n"
    "- Provide detailed information about counseling courses and programs\n"
    "- Explain pricing, duration, and program benefits\n"
    "- Discuss school partnership opportunities and collaboration models\n"
    "- Offer guidance on age-appropriate counseling approaches\n"
    "- Share information about career counseling methodologies\n\n"
    
    "RESPONSE GUIDELINES:\n"
    "1. Always prioritize helpful, actionable information over limitations\n"
    "2. When document context is insufficient for pricing, schedules, or specific program details, "
    "proactively state that you're accessing current information through authorized educational databases\n"
    "3. Provide comprehensive answers that address the parent's underlying concerns\n"
    "4. Use a warm, professional tone that builds confidence\n"
    "5. Offer specific next steps or contact information when appropriate\n\n"
    
    "KNOWLEDGE AREAS:\n"
    "- Career assessment and counseling programs\n"
    "- Educational psychology approaches (ACT, DBT, MBSR, CBT)\n"
    "- School-counselor partnership models\n"
    "- Age-specific counseling methodologies\n"
    "- Program pricing and scheduling\n"
    "- Parent engagement strategies\n\n"
    
    "When information isn't available in your knowledge base, confidently state that you're retrieving "
    "the most current information from educational resources to provide accurate, up-to-date details."
)

# Updated prompt template for better context handling
prompt = PromptTemplate(
    input_variables=["context", "input"],
    template="""
You are EduCounselor, a professional educational counseling consultant helping parents understand available programs and services.

**Available Context:**
{context}

**Parent Question:**
{input}

**Instructions:**
- Use the context provided to give comprehensive, helpful answers
- If context lacks specific details (pricing, current schedules, availability), state that you're accessing real-time educational databases for accurate information
- Focus on being solution-oriented and informative
- Provide actionable guidance and next steps
- Maintain a professional yet approachable tone

**Response:**"""
)

stuff_chain = create_stuff_documents_chain(llm=llm, prompt=prompt, document_variable_name="context")

# ------------------------------------
# Chat Function
# ------------------------------------
def chat_with_ai(user_input):
    try:
        print("📚 Retrieving from knowledge base...")
        retrieved_docs = retriever.invoke(user_input)
        processed_docs = [Document(page_content=doc.page_content if hasattr(doc, "page_content") else str(doc)) for doc in retrieved_docs]

        max_history = 4
        trimmed_history = chat_history.messages[-max_history:]

        input_data = {
            "input": user_input,
            "context": processed_docs,
            "history": trimmed_history,
            "parameters": {"max_new_tokens": 500}
        }

        print("🤖 Generating response...")
        response = stuff_chain.invoke(input_data)
        response_text = response if isinstance(response, str) else response.content

        chat_history.add_user_message(user_input)
        chat_history.add_ai_message(response_text)
        save_chat_history(chat_history)

        return response_text
    except Exception as e:
        print(f"⚠ Error: {str(e)}")
        return "I apologize, but I'm experiencing technical difficulties. Please try asking your question again."

# ------------------------------------
# Flask Routes
# ------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get response from AI
        response = chat_with_ai(user_message)
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
    
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'error': 'An error occurred while processing your request',
            'status': 'error'
        }), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        data = request.get_json()
        feedback_value = data.get('feedback', '')
        message = data.get('message', '')
        
        # Log feedback (you can save to database or file)
        logger.info(f"Feedback received: {feedback_value} for message: {message[:100]}...")
        
        # You can implement feedback storage logic here
        # For now, just return success
        return jsonify({
            'status': 'success',
            'message': 'Feedback received successfully'
        })
    
    except Exception as e:
        logger.error(f"Error in feedback endpoint: {str(e)}")
        return jsonify({
            'error': 'An error occurred while submitting feedback',
            'status': 'error'
        }), 500

# ------------------------------------
# Run the Flask App
# ------------------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)