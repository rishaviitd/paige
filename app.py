from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from mira_sdk import MiraClient, Flow
from dotenv import load_dotenv  # Import dotenv to load .env file
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API key from environment variables
API_KEY = os.getenv("MIRA_API_KEY")
if not API_KEY:
    raise ValueError("API_KEY is not set in the environment variables.")

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
        print(result)

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
