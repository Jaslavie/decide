from backend.mcts.state import State
from backend.mcts.simulator import Environment
from backend.mcts.search import Search
from backend.mcts.node import Node
from backend.agents.base_agent import AgentMessage
from backend.agents.translator import TranslatorAgent
from backend.agents.planner import PlannerAgent
from backend.tests.context import JASMINE_CONTEXT
import asyncio

async def run_simulation():
    print("\n=== Starting Decision Simulation ===\n")
    # initialize vector store
    translator = TranslatorAgent()
    planner = PlannerAgent()

    # store test context data
    for context in JASMINE_CONTEXT:
        await translator.vector_store.store_embedding(
            context["text"],
            metadata={
                "text": context["text"],
                "category": context["category"],
                "confidence": context["confidence"]
            }
        )

    # 1. Create sample input data
    user_input = {
        "text": "What is the #1 most important thing to focus on in my project to win the largest hackathon in the US (treehacks)?",
        "attributes": {
            "risk": 0.8,
            "time-constraint": 0.3,
            "importance": 0.6
        }
    }
    print("User input: ", user_input)

    # run pipeline
    translated = await translator.process_input_message(
        AgentMessage(content = user_input, from_agent="user", to_agent="translator", metadata={})
    )

    print("\n=== Starting Planning Agent ===\n")
    final_decisions = await planner.plan(translated)

    # print
    print("top decisions: ", final_decisions)

if __name__ == "__main__":
    asyncio.run(run_simulation())
