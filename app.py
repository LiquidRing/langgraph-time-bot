#!/usr/bin/env python3
"""
Minimal LangGraph Time Bot

A stateless chat bot that can tell you the current time using LangGraph.
"""

import os
from datetime import datetime, timezone
from typing import Annotated, Literal, TypedDict

from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode


class State(TypedDict):
    """The state of our chat bot."""
    messages: Annotated[list, add_messages]


@tool
def get_current_time() -> dict:
    """Return the current UTC time in ISO-8601 format.
    
    Returns:
        dict: A dictionary with the current UTC time.
        Example: {"utc": "2025-01-21T06:42:00Z"}
    """
    current_time = datetime.now(timezone.utc)
    return {"utc": current_time.strftime("%Y-%m-%dT%H:%M:%SZ")}


def create_model():
    """Create and configure the language model."""
    # Default to OpenAI, but you can easily switch to other providers
    # For Ollama: from langchain_ollama import ChatOllama
    # model = ChatOllama(model="llama3.2", base_url="http://localhost:11434")
    
    # For Gemini: from langchain_google_genai import ChatGoogleGenerativeAI 
    # model = ChatGoogleGenerativeAI(model="gemini-pro")
    
    # For DeepSeek: from langchain_openai import ChatOpenAI
    # model = ChatOpenAI(
    #     base_url="https://api.deepseek.com/v1",
    #     api_key=os.getenv("DEEPSEEK_API_KEY"),
    #     model="deepseek-chat"
    # )
    
    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Bind tools to the model
    tools = [get_current_time]
    return model.bind_tools(tools)


def should_continue(state: State) -> Literal["tools", "end"]:
    """Determine whether to continue with tools or end the conversation."""
    messages = state["messages"]
    last_message = messages[-1]
    
    # If the last message has tool calls, we should use tools
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    
    # Otherwise, we're done
    return "end"


def call_model(state: State) -> dict:
    """Call the language model with the current state."""
    model = create_model()
    messages = state["messages"]
    response = model.invoke(messages)
    
    # Return the new message to be added to state
    return {"messages": [response]}


def create_graph():
    """Create the LangGraph workflow."""
    # Create the graph
    workflow = StateGraph(State)
    
    # Add nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode([get_current_time]))
    
    # Add edges
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END,
        }
    )
    workflow.add_edge("tools", "agent")
    
    # Compile the graph
    return workflow.compile()


# Create the application graph
app = create_graph()


if __name__ == "__main__":
    # Simple test run
    print("🤖 Time Bot is running!")
    print("Ask me 'What time is it?' to test the tool.")
    
    # Test the bot
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ["quit", "exit", "bye"]:
                print("Goodbye!")
                break
                
            if user_input:
                # Create initial state
                initial_state = {"messages": [HumanMessage(content=user_input)]}
                
                # Run the graph
                result = app.invoke(initial_state)
                
                # Get the last AI message
                last_message = result["messages"][-1]
                if isinstance(last_message, AIMessage):
                    print(f"Bot: {last_message.content}")
                    
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}") 