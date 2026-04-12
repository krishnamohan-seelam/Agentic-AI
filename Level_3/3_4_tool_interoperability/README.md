# Task Manager MCP Server

This directory contains the Task Manager MCP (Model Context Protocol) server implementation and client for testing tool interoperability.

## Files Overview

- **`task_manager_server.py`**: The main MCP server implementation using FastMCP. This provides tools for managing a task/todo list (add, list, complete, delete, get tasks) with persistent storage in JSON format.

- **`task_manager_client.py`**: An interactive Python client that connects to the MCP server and demonstrates using the tools through a LangChain agent.

- **`3_5_mcp_server_try_it.ipynb`**: A Jupyter notebook for learning and experimenting with MCP server concepts. This is primarily educational content.

## Why Use `task_manager_server.py` Instead of the Notebook?

The notebook (`3_5_mcp_server_try_it.ipynb`) is designed as a **learning resource** and **interactive tutorial**. It contains:

- Step-by-step explanations of MCP concepts
- Code examples and exercises
- Educational content for understanding how MCP servers work

However, for **actual server deployment and testing**, you should use `task_manager_server.py` because:

1. **Client Integration**: The client script (`task_manager_client.py`) is specifically configured to launch and communicate with `task_manager_server.py` via stdio transport.

2. **Persistent Storage**: The server includes proper JSON-based storage for tasks, making it suitable for real usage.

3. **FastMCP Framework**: Uses the FastMCP library for a clean, efficient MCP server implementation.

## Running the Server

To run the MCP server:

```bash
python task_manager_server.py
```

## Running the Client

To test the server with the interactive client:

```bash
python task_manager_client.py
```

The client will automatically start the server process and provide a menu-driven interface to test all the task management tools.

## Storage

Tasks are stored in `data/tasks.json` relative to the server script location. The storage is automatically created when the first task is added.
