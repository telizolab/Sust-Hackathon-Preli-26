import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from dotenv import load_dotenv

from models import AnalyzeTicketRequest, AnalyzeTicketResponse
from llm_service import analyze_ticket_with_llm
from safety_filter import apply_safety_filters

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="QueueStorm Investigator API")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Global exception handler for Pydantic validation failures.
    Returns a standard 400 error without leaking internal details.
    """
    logger.warning(f"Validation error on {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=400,
        content={"detail": "Malformed input data. Please check your request schema."},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for all other unhandled exceptions.
    Returns a standard 500 error to prevent stack trace leaks.
    """
    logger.error(f"Internal server error on {request.url}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again later."},
    )

@app.get("/health")
async def health_check():
    """Instantly returns status ok."""
    return {"status": "ok"}

@app.post("/analyze-ticket", response_model=AnalyzeTicketResponse)
async def analyze_ticket(request: AnalyzeTicketRequest):
    """
    Analyzes a support ticket using the Groq LLM, applies safety filters,
    and returns a structured JSON response.
    """
    logger.info(f"Processing ticket {request.ticket_id}")
    
    # 1. Call LLM
    llm_output_dict = await analyze_ticket_with_llm(request)
    
    # 2. Extract fields that need safety filtering
    customer_reply = llm_output_dict.get("customer_reply", "")
    recommended_action = llm_output_dict.get("recommended_next_action", "")
    
    # 3. Apply Safety Filters
    safe_reply, safe_action = apply_safety_filters(customer_reply, recommended_action)
    
    # 4. Update the dictionary with safe values
    llm_output_dict["customer_reply"] = safe_reply
    llm_output_dict["recommended_next_action"] = safe_action
    
    # 5. Ensure the ticket_id is preserved from request just in case
    llm_output_dict["ticket_id"] = request.ticket_id
    
    # 6. Validate and return using Pydantic model
    return AnalyzeTicketResponse(**llm_output_dict)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
