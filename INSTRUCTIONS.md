Project Title
EduRAG: Intelligent Tutor Using RAG and LangChain

Objective
Develop a backend-powered AI tutoring system that leverages Retrieval-Augmented Generation (RAG), LLM APIs, and a SQL-based knowledge base to deliver smart, context-aware educational responses to student queries.

Allowed Technologies
Backend Framework: FastAPI
LLM APIs: OpenAI
Vector Stores: Qdrant

Database: SQLite

Libraries: LangChain, SQLAlchemy, etc.


Core Features
1. Content Upload & Knowledge Base Management
Accept text-based content files (e.g., .txt) with metadata: topic, title, grade.
Store both content and metadata in a relational SQL database.

2. Vector Embedding & Semantic Retrieval
Convert raw content into embeddings using LLM embedding models.
Store and retrieve content based on semantic similarity using a vector store.

3. RAG-Based Question Answering
Implement a Retrieval-Augmented Generation pipeline that:
Retrieves relevant content using vector search.
Uses an LLM to generate a user-facing answer grounded in the retrieved content.

4. System Prompt & Tutor Persona
Define a system prompt that guides the AI to act like an educational tutor.

Support configurable "personas" (e.g., friendly, strict, humorous) to vary response tone.

5. Natural Language SQL Querying
Accept natural-language questions about the database (e.g., “What topics are covered in Grade 5?”).
Use an LLM to convert the query into SQL and return human-readable answers.

6. API Endpoints
Build an API interface that includes:
Method
Endpoint
Description
POST
/upload-content
Uploads new textbook content with metadata
POST
/ask
Accepts a user question and returns an AI answer
GET
/topics
Filters and retrieves topics (e.g., by grade)
GET
/metrics
Returns stats: topics count, files uploaded, etc

7. Use type based approach and make sure to add unit test.

Final Deployment Task (Mandatory)
To complete the assessment, deploy your backend project locally using Nginx as a reverse proxy. This will demonstrate your ability to handle production-like deployment setups.
Requirements:

Use Uvicorn to run the app.
Configure Nginx to route requests to your backend (e.g., localhost:80 to localhost:8000).
Include the nginx.conf or related setup instructions in your repository.
Mention setup steps clearly in your README.md.

This task will be part of the evaluation process and is essential for assessing how well you can handle real-world deployment environments.

📊 User Feedback Loop – Let users rate the quality of AI responses.
🧾 Answer Logging – Save previously asked questions and generated responses.

🧪 Interactive Playground – Create a lightweight UI (CLI, Streamlit, or HTML page) to interact with the tutor.



