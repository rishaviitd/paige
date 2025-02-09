from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mira_sdk import MiraClient, Flow
import os

app = FastAPI()

# Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API key from environment variable (safer than hardcoding)
API_KEY = os.getenv("MIRA_API_KEY", "sb-bb42f01a519572327de8dc0794e8f520")
client = MiraClient(config={"API_KEY": API_KEY})

class InputData(BaseModel):
    prompt: str

@app.get("/")
def home():
    return {"message": "Hello from the server"}

@app.post("/generate")
def generate_response(input_data: InputData):
    try:
        version = "1.0.0"
        flow_name = f"@rishaviitd/book-reader/{version}"
        result = client.flow.execute(flow_name, input_data.dict())

        # Print result in the terminal (console.log equivalent)
        print("\n========== API RESPONSE ==========")
        print(result)
        print("=================================\n")

        return result
    except Exception as e:
        print("\n========== ERROR OCCURRED ==========")
        print(str(e))
        print("====================================\n")
        raise HTTPException(status_code=500, detail=str(e))

