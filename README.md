### multi-agent decision system to optimize outcomes with Monte Carlo Simulations.
The goal of this application is to answer the question: "How can we maximize the rewards (i.e. outcomes) of the decisions we make and optimize our planning process?"
The application will make decisions based on context of the user.
The decision-making process will rely on the analysis of trade-offs between the different options.

### Starting application
Backend:
```
pip install -r requirements.txt
python src/backend/main.py
```
Frontend:
```
npm run dev
```
### Tech stack
- [POMDPs.jl](https://juliapomdp.github.io/MCTS.jl/latest/) framework for Monte Carlo Tree Search.
- [Langchain](https://langchain.com/) framework for multi-agent orchestration.
- [GPT-4](https://platform.openai.com/docs/models/gpt-4) for NLP parsing.
- [Pinecone](https://www.pinecone.io/) vector database for context storage.
- [Redis](https://redis.io/) for caching and agent state management.

### Architecture design
We are using a hierarchical design with 4 agents and 1 supervisor:
- **Planner** (Planning agent): Selects the best options to test in the simulation.
- **Philosopher** (Reasoning agent): Analyzes each step of the simulation and provides feedback on the decisions.
- **Wizard** (Prediction agent): Predicts the future "next node" based on previous steps by running simulations.
- **Commander** (Decision agent): Evaluates each decision and decides what the optimal path is.
- **Supervisor** (Supervisor agent): Orchestrates the decision-making process by delegating tasks and monitoring performance.

Supporting agents:
- **Input Agent**: Gathers information from the user and converts natural language to structured data.

### Decision making framework
We will use the Monte Carlo Tree Search (MCTS) algorithm to simulate decisions and extract the optimal plan. We will also reference the following factors:
- Impact on outcomes in other areas of the user's life.
- Availability of information
- Constraints

### Literature
- [Multi-Agent Orchestration Architecture](https://dev.to/yukooshima/building-a-multi-agent-framework-from-scratch-with-llamaindex-5ecn)
- [Langchain Handbook](https://langchain-ai.github.io/langgraph/concepts/multi_agent/#handoffs)
- [Monte Carlo Tree Search (MCTS)](https://medium.com/@_michelangelo_/monte-carlo-tree-search-mcts-algorithm-for-dummies-74b2bae53bfa)
- [MCTS in Reinforcement Learning](https://www.jair.org/index.php/jair/article/download/11099/26289/20632)
- [Upper Confidence Bound Algorithm](https://kfoofw.github.io/bandit-theory-ucb-analysis/)