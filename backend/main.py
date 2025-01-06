# create fastapi server to handle requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.services.message_bus import MessageBus
from backend.agents.input import InputAgent
from backend.agents.planner import PlannerAgent

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize message bus
message_bus = MessageBus()

# initialize agents
input_agent = InputAgent()
planner_agent = PlannerAgent()

#* implement subscribe functionality

@app.get("/")
async def root():
    return {"message": "Hello World"}

#* add more routes later

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


