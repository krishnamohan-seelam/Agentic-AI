#!/usr/bin/env python3
"""
Task Manager MCP Client - Interactive Script

This script provides an interactive interface to test the Task Manager MCP server.
It allows you to perform various agentic actions through a menu-driven interface.
"""

import asyncio
import os
import sys
import json
import traceback
from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import MCP and LangChain components
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

# Constants
DEFAULT_REQUIRED_KEYS = ("OPENAI_API_KEY",)

# Path to your MCP server implementation
# Change this to task_manager_server_solution.py to test the solution
SERVER_PATH = Path(__file__).parent / "task_manager_server_solution.py"
if not SERVER_PATH.exists():
    SERVER_PATH = Path(__file__).parent / "task_manager_server.py"
    print(
        "Warning: task_manager_server_solution.py not found; using task_manager_server.py instead."
    )

# MCP client configuration
mcp_config = {
    "task_manager": {
        "transport": "stdio",
        "command": sys.executable,
        "args": [str(SERVER_PATH)],
    }
}

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


@lru_cache(maxsize=1)
def configure_environment(required_keys=None):
    """
    Factory function to configure environment variables.
    Executes once and caches results.
    """
    if required_keys is None:
        required_keys = DEFAULT_REQUIRED_KEYS

    IN_COLAB = "COLAB_GPU" in os.environ or "COLAB_TPU_ADDR" in os.environ

    if IN_COLAB:
        try:
            from google.colab import userdata
        except Exception:
            print("Not required in local environment")

        print("Configuring for Google Colab environment...")
        for key in required_keys:
            try:
                os.environ[key] = userdata.get(key)
            except Exception:
                print(f"Warning: Could not find {key} in Colab secrets.")
    else:
        print("Configuring for local environment...")

    # Validation
    for key in required_keys:
        if not os.getenv(key):
            raise ValueError(f"Missing required environment variable: {key}")

    return True


async def run_agent(user_message: str, verbose: bool = False):
    """Run a LangChain agent with your Task Manager MCP tools."""
    try:
        client = MultiServerMCPClient(mcp_config)
        tools = await client.get_tools()

        if verbose:
            print(f"Available tools: {[t.name for t in tools]}\n")

        agent = create_agent(model=llm, tools=tools)
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": user_message}]}
        )

        return result["messages"][-1].content
    except Exception as e:
        traceback.print_exc()
        return f"Error: {type(e).__name__}: {str(e)}"


def display_menu():
    """Display the main menu options."""
    print("\n" + "=" * 50)
    print("Task Manager MCP Client - Interactive Menu")
    print("=" * 50)
    print("1. Check Available Tools")
    print("2. Add Sample Tasks")
    print("3. List All Tasks")
    print("4. Complete a Task")
    print("5. Delete a Task")
    print("6. Test Priority Validation")
    print("7. Clear All Tasks")
    print("8. Exit")
    print("=" * 50)


async def handle_choice(choice: str):
    """Handle the user's menu choice."""
    if choice == "1":
        print("\n--- Checking Available Tools ---")
        response = await run_agent("What tools do you have available?", verbose=True)
        print(f"Response: {response}")

    elif choice == "2":
        print("\n--- Adding Sample Tasks ---")
        response = await run_agent(
            "Add these tasks: "
            "1) 'Review pull request' with high priority, "
            "2) 'Update documentation' with medium priority, "
            "3) 'Clean up old branches' with low priority"
        )
        print(f"Response: {response}")

    elif choice == "3":
        print("\n--- Listing All Tasks ---")
        response = await run_agent("List all my tasks")
        print(f"Response: {response}")

    elif choice == "4":
        print("\n--- Completing a Task ---")
        task_name = input("Enter the task name to complete: ").strip()
        if task_name:
            response = await run_agent(
                f"Mark the '{task_name}' task as completed, then show me only pending tasks"
            )
            print(f"Response: {response}")
        else:
            print("No task name provided.")

    elif choice == "5":
        print("\n--- Deleting a Task ---")
        task_name = input("Enter the task name to delete: ").strip()
        if task_name:
            response = await run_agent(
                f"Delete the '{task_name}' task, then list all remaining tasks"
            )
            print(f"Response: {response}")
        else:
            print("No task name provided.")

    elif choice == "6":
        print("\n--- Testing Priority Validation ---")
        response = await run_agent(
            "Try to add a task called 'Test task' with priority 'urgent'"
        )
        print(f"Response: {response}")

    elif choice == "7":
        print("\n--- Clearing All Tasks ---")
        storage_file = Path(__file__).parent / "data" / "tasks.json"
        if storage_file.exists():
            storage_file.write_text(json.dumps({"tasks": {}}, indent=2))
            print("Task storage cleared.")
        else:
            print("No storage file found (tasks may not have been created yet).")

    elif choice == "8":
        print("\nExiting program...")
        return False

    else:
        print("Invalid choice. Please select 1-8.")

    return True


async def main():
    """Main function to run the interactive client."""
    print("Task Manager MCP Client")
    print(f"Server path: {SERVER_PATH}")

    # Configure environment
    try:
        configure_environment(DEFAULT_REQUIRED_KEYS)
        print("Environment setup complete!")
    except Exception as e:
        print(f"Environment setup failed: {e}")
        return

    # Check if server file exists
    if not SERVER_PATH.exists():
        print(f"Warning: Server file not found at {SERVER_PATH}")
        print(
            "Make sure to implement task_manager_server_solution.py or update SERVER_PATH"
        )

    # Main loop
    continue_running = True
    while continue_running:
        display_menu()
        try:
            choice = input("Enter your choice (1-8): ").strip()
            continue_running = await handle_choice(choice)
        except KeyboardInterrupt:
            print("\n\nExiting due to keyboard interrupt...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            continue

        if continue_running:
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    # Workaround for Windows subprocess issues (if running in certain environments)
    import io

    if hasattr(sys.stderr, "fileno"):
        try:
            sys.stderr.fileno()
        except (AttributeError, io.UnsupportedOperation):
            # Create a log file for stderr instead
            log_dir = Path(__file__).parent / "logs"
            log_dir.mkdir(exist_ok=True)
            sys.stderr = open(log_dir / "stderr.log", "w")

    # Run the async main function
    asyncio.run(main())
