# UEL Generative AI Retrieval System – Backend

This is the backend component of the UEL Generative AI Retrieval System, developed as part of the thesis **"Building an Information Retrieval System for University Documents Based on Generative AI Technologies"**. The system is designed to enable semantic search and AI-powered question answering for internal academic documents at the University of Economics and Law.

## 🚀 Features

- PDF document parsing and text chunking
- FAISS-based vector search for semantic retrieval
- LangChain integration for prompt orchestration
- GPT-powered answer generation using OpenAI API
- Simple Django-based authentication system
- Conversation history tracking

## 🛠 Tech Stack

- Python 3.9+
- Django 3.2+
- FAISS (Facebook AI Similarity Search)
- LangChain
- OpenAI API
- MongoDB (via PyMongo)

## 📁 Project Structure

```
UEL_GenAI_BE/
├── ai/                # LangChain + OpenAI integration
├── auth/              # User authentication
├── conversation/      # Chat session management
├── db/                # MongoDB interaction
├── vectorstore/       # FAISS vector operations
├── utils/             # PDF reading, text splitting, token management
├── main.py            # Application entrypoint
├── requirements.txt
└── README.md
```

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/mataza060503/UEL_GenAI_BE.git
cd UEL_GenAI_BE
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate       # Windows
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:

```
OPENAI_API_KEY=your_openai_api_key
MONGO_URI=your_mongodb_connection_string
```

5. Run the application:

```bash
python main.py
```

## 🧪 API Endpoints

| Method | Endpoint                      | Description                        |
|--------|-------------------------------|------------------------------------|
| POST   | `/genai/chat`                 | Generate AI response               |
| GET    | `/auth/?username=...`         | Authenticates or creates a user    |
| POST   | `/chat/`                      | Submits a user query               |
| GET    | `/message/?chat_id=...`       | Retrieves messages from a session  |

## 🔗 Related Repositories

- Frontend: [https://github.com/mataza060503/UEL_GenAI](https://github.com/mataza060503/UEL_GenAI)
- Document dataset: [Google Drive](https://drive.google.com/drive/folders/1zKWJumzUqkiBtRqRyaR6We21Swb4sgYV?usp=sharing)

## 📄 License

This project is developed for academic purposes by students of the University of Economics and Law.

## 👥 Authors

- Duy Thanh Tran  
- Quang Phuc Nguyen  
- Hoang Lam Vo
