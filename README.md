# QueueStorm Investigator

QueueStorm Investigator is an asynchronous web API acting as an AI copilot for financial support agents. It analyzes user complaints against transaction histories using the Groq LLM API and enforces rigorous safety checks.

## Tech Stack
- **Language**: Python 3.11+
- **Framework**: FastAPI (for rapid async API development)
- **Validation**: Pydantic
- **Web Server**: Uvicorn
- **LLM Provider**: Groq API (`llama-3.1-70b-versatile`)
- **Environment Management**: python-dotenv

## Model Reasoning & Prompt Defenses
The service leverages the `llama-3.1-70b-versatile` model via the Groq API.
- **Strict Data-Matching**: The model is instructed to act purely as an investigator. It cross-references user complaints with transaction history to output a strict JSON format matching predefined Pydantic models.
- **Prompt Injection Defense**: A critical section in the system prompt instructs the model to ignore any instructions embedded in the user's text and treat it purely as string data.

## Safety Logic (The Interceptor)
Before the LLM response is returned to the user, a regex-based Python interceptor (`safety_filter.py`) applies three critical rules:
1. **Credential Shield**: Overrides the entire reply if keywords like "PIN", "OTP", or "password" are detected.
2. **Financial Promise Shield**: Replaces any sentence containing unapproved financial promises (e.g., "will refund") with a standard investigation message.
3. **Third-Party Shield**: Strips out unauthorized URLs or phone numbers that follow contact verbs ("contact", "call").

## Runbook

### Local Development Setup

1. **Clone the repository** and navigate to the project directory.

2. **Create a virtual environment** and activate it (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Copy `.env.example` to `.env` and fill in your Groq API key:
   ```bash
   cp .env.example .env
   ```
   Add your `GROQ_API_KEY` to the `.env` file.

5. **Run the server**:
   ```bash
   uvicorn main:app --reload
   ```

### Docker Deployment

1. **Build the image**:
   ```bash
   docker build -t queuestorm-investigator .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8000:8000 --env-file .env queuestorm-investigator
   ```

## Endpoints
- `GET /health` : Instant health check.
- `POST /analyze-ticket` : Accepts the Ticket Request Schema and returns the LLM analyzed and safely filtered Response Schema.
