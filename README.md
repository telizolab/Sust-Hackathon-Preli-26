# QueueStorm Investigator – AI-Powered Copilot for Financial Support Operations

## Executive Summary
In times of market volatility or service disruptions, financial institutions face unprecedented high-volume support surges that overwhelm human agents and delay critical resolutions. The QueueStorm Investigator is an automated, evidence-based ticket investigator designed to autonomously cross-reference user complaints against transactional data. By preprocessing these complex inquiries and presenting structured findings, the system significantly reduces resolution times and ensures support teams can prioritize high-impact issues.

## Key Features
- **Automated evidence cross-referencing**: Dynamically analyzes the mismatch between user-reported issues and underlying transactional data (Transaction vs. Complaint).
- **Hardcoded safety guardrails**: Enforces non-negotiable security using regex-based interceptors to block sensitive data leakage and unauthorized financial advice.
- **Schema-validated JSON API contract**: Ensures all inputs and outputs adhere strictly to predefined Pydantic models for reliable integration and predictable system behavior.

## Tech Stack
- **Framework**: FastAPI / Python 3.11+
- **AI Engine**: Groq API (llama3-70b-8192)
- **Deployment**: Docker / Render

## MODELS Used
- **Model**: `llama3-70b-8192`
- **Inference Infrastructure**: Groq API
- **Justification**: The `llama3-70b-8192` model is selected for its superior reasoning capabilities over complex financial context. Executed via Groq's high-speed inference API, it delivers sub-second latency for extensive token generation. This extreme low-latency performance is optimal and required to consistently meet strict 30-second webhook timeout limits standard in production support environments.

## Setup Instructions

1. **Environment Configuration**
   Create a `.env` file in the project root directory and configure your Groq API key:
   ```env
   GROQ_API_KEY=your_secure_api_key_here
   ```

2. **Install Dependencies**
   Install the required production packages via pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application Server**
   Start the FastAPI application utilizing Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```

## Safety & Compliance Logic
Financial compliance and data security are strictly enforced as programmatic hard-stops prior to any output reaching the client. The system employs deterministic regex interceptors acting as a fail-safe against generative deviations:
- **Credential Shield**: Detects and sanitizes the exposure of PII, account numbers, or authentication tokens.
- **Financial Promise Shield**: Prevents the system from making unauthorized guarantees of refunds, fee waivers, or account crediting.
- **Third-Party Shield**: Blocks any prescriptive references to competitor banks or external unauthorized financial entities.

## Known Limitations
While the system architecture emphasizes reliability, the investigative accuracy remains intrinsically dependent on the underlying LLM's reasoning constraints. To mitigate false positives, the system acts as a copilot rather than a fully autonomous agent; all high-risk or ambiguous cases are explicitly flagged for mandatory human review to ensure 100% financial compliance.
