# Agentic-AI

This repository contains a collection of Jupyter Notebook exercises and tutorials focused on building and working with Agentic AI systems. The materials primarily cover concepts using popular frameworks like **LangChain** and **LangGraph**, providing hands-on practice for creating resilient, tool-augmented, and graph-based AI agents.

## Repository Structure

The exercises are located in the `Level_2` directory and cover various foundational to advanced concepts in Agentic AI:

### LangChain Basics & Tooling
* **`2_1_instantiate_prebuilt_agent.ipynb`**: Demonstrates how to instantiate prebuilt LangChain agents that can utilize multiple external tools to answer questions.
* **`2_2_structured_output_tutorial.ipynb`**: Explains how to enforce structured outputs using LangChain and Pydantic to ensure the LLM returns consistent, typed data objects.
* **`2_3_integrate_tools.ipynb`**: Shows the pattern of augmenting an agent by integrating an external tool, specifically using a Wikipedia search tool as an example.
* **`2_4_llm_call_chain.ipynb`**: Covers building progressive LLM call chains (e.g., generation -> summary -> condensation) chaining steps modularly.
* **`2_12_streaming_output_tutorial.ipynb`**: Teaches how to implement real-time streaming output using LangChain to display LLM responses chunk-by-chunk as they are generated.

### Building ReAct (Reasoning & Acting) Agents
* **`2_5_write_effective_prompts.ipynb`**: Focuses on writing strong system prompts intended to guide the specific behavior and reasoning processes of a ReAct agent.
* **`2_6_agent_class_structure.ipynb`**: Explores implementing the core object-oriented class structure required for a ReAct agent to manage state, conversation history, and LLM calls.
* **`2_6_1_implement_loops.ipynb`**: Dives into implementing the internal control loop (Thought -> Action -> Observation) that allows a ReAct agent to continually reason until it reaches a final answer.

### LangGraph Fundamentals
* **`2_7_define_concepts_of_nodes_edges_graphs_and_state_in_langgraph.ipynb`**: Introduces the fundamental components of LangGraph: defining Graph State, creating Node functions, creating Edges, and compiling workflows.
* **`2_8_define_and_manage_state_in_a_langgraph.ipynb`**: Deepens state management in LangGraph using Pydantic models with reducers for handling state updates across complex pipelines.
* **`2_11_construct_a_basic_chatbot_agent_in_langgraph.ipynb`**: Combines various state and graph concepts to construct a functioning chatbot agent (e.g., a calculator assistant) featuring tools and conditional routing edges.

### Productionization & Resiliency
* **`2_9_debug_with_logging.ipynb`**: Explains how to enhance your agents with production-ready structured logging, including tracking tool execution times and summary statistics.
* **`2_10_error_handling.ipynb`**: Covers building resilient API structures capable of elegantly handling common LLM pitfalls such as timeouts, rate limits, and fallbacks.

## Getting Started

To explore these concepts, navigate to the `Level_2` directory and open the `.ipynb` notebooks in Jupyter Notebook, VS Code, or Google Colab. Each notebook contains specific instructions and challenges for writing or completing the agent code.
