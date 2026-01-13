"""
Travel Planning Tools for Marbella Agent
Exports weather and task management tools as an MCP server.
"""

from claude_agent_sdk import create_sdk_mcp_server
from .weather_tool import get_weather_forecast
from .task_manager_tool import (
    create_trip,
    add_task,
    list_tasks,
    complete_task,
    update_task,
    delete_task,
    list_trips
)

# Create MCP server with all tools
travel_tools_server = create_sdk_mcp_server(
    name="travel_tools",
    version="1.0.0",
    tools=[
        # Weather tool
        get_weather_forecast,
        # Task management tools
        create_trip,
        add_task,
        list_tasks,
        complete_task,
        update_task,
        delete_task,
        list_trips
    ]
)

__all__ = ["travel_tools_server"]
