## Multi-agent decision system to optimize outcomes with Monte Carlo Simulations.
The goal of this application is to answer the question: "How can we maximize the rewards (i.e. outcomes) of the decisions we make and optimize our planning process?"
The application will make decisions based on context of the user.
The decision-making process will rely on the analysis of trade-offs between the different options.

## Starting application
Backend:
```
pip install -r requirements.txt
python src/backend/main.py
```
Frontend:
```
npm run dev
```
## Tech stack
- [POMDPs.jl](https://juliapomdp.github.io/MCTS.jl/latest/) framework for Monte Carlo Tree Search.
- [Langchain](https://langchain.com/) framework for multi-agent orchestration.
- [GPT-4](https://platform.openai.com/docs/models/gpt-4) for NLP parsing.
- [FAISS](https://github.com/facebookresearch/faiss) vector database for context storage and retrieval.
- [Redis](https://redis.io/) for caching and agent state management.

## Agent Architecture design
We are using a hierarchical design with 4 agents:
- **Planner** (Planning agent): Selects the best options to test in the simulation.
- **Philosopher** (Reasoning agent): Analyzes each step of the simulation and provides feedback on the decisions.
- **Wizard** (Prediction agent): Predicts the future "next node" based on previous steps by running simulations.
- **Commander** (Decision agent): Evaluates each decision and decides what the optimal path is.

Supporting agents:
- **Translator**: Gathers data and translates to different formats (structured data, vector embeddings, nlp, etc.)

## Memory Architecture
We will attempt to design a lightweight model of how the human brain processes memory.
Storage system is stored in `backend/services/memory_store.py`. It is separated into:
- **Insights**: Short term, lightweight memory of user behavioral patterns stored in-memory.
```
# stored as a summarized list of UserInsight objects
insight = {
    "category": "background",
    "description": "The user has been working on a project for 3 months",
    "confidence": 0.89,
    "timestamp": 1715136000
}
```
- **Context**: Long-term memory of user's background (ex: goals, preferences, history, etc.) with temporal awareness stored in a vector database (for embeddings) and an SQL database (for metadata).
```
# embedding storage
self.vectors = [
    [0.023, -0.156, 0.789, ...],  # 1536 element array
]
# metadata storage
self.metadata = [
    {
        "text":  "Studying CS & Neuroscience at UCI",
        "category": "background",
        "confidence": 0.9,
        "timestamp": 1715136000
    }
]
```

Context retrieval pipeline is stored in `backend/services/vector_store.py`. It includes:
- Similarity search to retrieve content-relevant context.
- Context ranking and filtering to retrieve temporally relevant context.
```
# similarity search through context vector database
# sample input: "How can I win the largest hackathon in the US (treehacks)?"
{
    "matches": [
        {
            "id": "123",
            "text": "User is a designer who has won 15 hackathons", # relevant context
            "category": "background",
            "confidence": 0.9,
            "timestamp": 1715136000
        }
    ]
}
```

## Decision-making framework
We will use the Monte Carlo Tree Search (MCTS) algorithm to simulate decisions and extract the optimal plan. We will also reference the following factors:
- Impact on outcomes in other areas of the user's life.
- Availability of information
- Constraints

## Literature
- [Multi-Agent Orchestration Architecture](https://dev.to/yukooshima/building-a-multi-agent-framework-from-scratch-with-llamaindex-5ecn)
- [Langchain Handbook](https://langchain-ai.github.io/langgraph/concepts/multi_agent/#handoffs)
- [Monte Carlo Tree Search (MCTS)](https://medium.com/@_michelangelo_/monte-carlo-tree-search-mcts-algorithm-for-dummies-74b2bae53bfa)
- [MCTS in Reinforcement Learning](https://www.jair.org/index.php/jair/article/download/11099/26289/20632)
- [Upper Confidence Bound Algorithm](https://kfoofw.github.io/bandit-theory-ucb-analysis/)
- [Context retrieval in llms and types of memeory](https://uptrain.medium.com/a-comprehensive-guide-to-context-retrieval-in-llms-212eb3893075)