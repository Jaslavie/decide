from backend.mcts.state import State
from backend.mcts.simulator import Environment
from backend.mcts.search import Search
from backend.mcts.node import Node
from backend.agents.base_agent import AgentMessage
from backend.agents.translator import TranslatorAgent
from backend.agents.planner import PlannerAgent
import asyncio

async def run_simulation():
    print("\n=== Starting Decision Simulation ===\n")

    # 1. Create sample input data
    user_input = {
        "text": "What is the best way to build a winning hackathon project?",
        "attributes": {
            "risk": 0.8,
            "time-constraint": 0.3,
            "importance": 0.6
        }
    }
    print("User input: ", user_input)

    # 2. create initial state and agents
    translator = TranslatorAgent()
    planner = PlannerAgent()

    # run pipeline
    translated = await translator.process_input_message(
        AgentMessage(content = user_input)
    )

    print("starting planner agent")
    final_decisions = await planner.plan(translated)

    # print
    print("top decisions: ", final_decisions)

if __name__ == "__main__":
    asyncio.run(run_simulation())
