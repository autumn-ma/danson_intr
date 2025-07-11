# EduRAG: Intelligent Tutor Using RAG and LangChain

This project is a backend-powered AI tutoring system that leverages Retrieval-Augmented Generation (RAG), LLM APIs, and a SQL-based knowledge base to deliver smart, context-aware educational responses to student queries.

## Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory and add the following variables:
   ```
   DATABASE_URL=<url>
   QDRANT_HOST=<host>
   QDRANT_PORT=<port>
   QDRANT_API_KEY=<key>
   ```

4. **Run the application:**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

## Nginx Configuration

To run the application with Nginx as a reverse proxy, you can use the provided `nginx.conf` file. Make sure Nginx is installed on your system.

1. **Copy the Nginx configuration file:**
   ```bash
   sudo cp nginx.conf /etc/nginx/sites-available/edurag
   ```

2. **Create a symbolic link to enable the site:**
   ```bash
   sudo ln -s /etc/nginx/sites-available/edurag /etc/nginx/sites-enabled/
   ```

3. **Test the Nginx configuration and restart the service:**
   ```bash
   sudo nginx -t
   sudo systemctl restart nginx
   ```

The application should now be accessible at `http://localhost`.


## Project Screenshot
The feature usage are shown under screenshots.
