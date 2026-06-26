import asyncio
from httpx import AsyncClient, ASGITransport
from main import app
import json

async def run_test():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Test 1: Health check
        response = await ac.get("/health")
        print("Health Check:", response.status_code, response.json())

        # Test 2: Analyze Ticket
        payload = {
            "ticket_id": "TKT-12345",
            "complaint": "I accidentally transferred money to the wrong person, can you please refund me?",
            "transaction_history": [
                {
                    "transaction_id": "TXN-001",
                    "timestamp": "2023-10-27T10:00:00Z",
                    "type": "transfer",
                    "amount": 50.0,
                    "counterparty": "John Doe",
                    "status": "completed"
                }
            ]
        }
        
        print("\nSending Ticket for Analysis...")
        response = await ac.post("/analyze-ticket", json=payload)
        print("Status Code:", response.status_code)
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    asyncio.run(run_test())
