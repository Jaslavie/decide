# create fastapi server to handle requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.message_bus import MessageBus
from agents.translator import TranslatorAgent
from agents.planner import PlannerAgent
from tests.context import JASMINE_CONTEXT

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
translator_agent = TranslatorAgent()
planner_agent = PlannerAgent()

# add test context to vector db
async def init_vector_store():
    for context in JASMINE_CONTEXT:
        await message_bus.vector_store.store_embedding(
            context["text"],
            metadata={
                "text": context["text"],
                "category": context["category"],
                "confidence": context["confidence"],
                "timestamp": context["timestamp"]
            }
        )

#* implement subscribe functionality

@app.get("/")
async def root():
    return {"message": "Hello World"}

#* other routes
# get context from vector db
@app.get("/get_context")
async def get_context():
    try:
        # query all vectors from vector db
        query_result = await message_bus.vector_store.query_embedding([], top_k=100) 

        # extract only text and category from the query result
        contexts = [
            {
                "text": match["text"],
                "category": match["metadata"].get("category", "Unknown"),
                "confidence": match["metadata"].get("confidence", 0.0),
                "timestamp": match["metadata"].get("timestamp", 0.0)
            }
            for match in query_result.get("matches", [])
        ] if query_result and "matches" in query_result else []

        return {"contexts": contexts}
    except Exception as e:
        return {"error": str(e)}

# add new context to vector db
@app.post("/add_context")
async def add_context(context: dict):
    try:
        # Validate required fields
        if "text" not in context:
            return {"status": "error", "message": "Missing required field: text"}
        
        # Use default category if not provided
        category = context.get("category", "Unknown")
        
        # store the new context in vector db
        stored_id = await message_bus.vector_store.store_embedding(
            context["text"],
            metadata={
                "text": context["text"],
                "category": category,
                "confidence": context.get("confidence", 0.0),
                "timestamp": context.get("timestamp", 0.0)
            }
        )

        if not stored_id:
            raise Exception("Failed to store context in vector db")
        
        return {
            "status": "success",
            "id": stored_id,
            "text": context["text"],
            "category": category,
            "confidence": context.get("confidence", 0.0),
            "timestamp": context.get("timestamp", 0.0)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

if __name__ == "__main__":
    import uvicorn
    import asyncio

    asyncio.run(init_vector_store())
    uvicorn.run(app, host="0.0.0.0", port=8000)


