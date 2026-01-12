"""
Task Management Tools for Trip Planning
SQLite-based task management with trip organization.
"""

import aiosqlite
import os
from datetime import datetime
from typing import Any
from claude_agent_sdk import tool

# Database file path
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "trips_database.db")


async def init_database():
    """Initialize the database schema if it doesn't exist."""
    async with aiosqlite.connect(DB_PATH) as db:
        # Create trips table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS trips (
                trip_id TEXT PRIMARY KEY,
                trip_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create tasks table
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                trip_id TEXT NOT NULL,
                description TEXT NOT NULL,
                category TEXT,
                priority TEXT,
                due_date TEXT,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (trip_id) REFERENCES trips(trip_id)
            )
        """)

        await db.commit()


def generate_trip_id(trip_name: str) -> str:
    """Generate a trip_id from trip_name (lowercase, underscores)."""
    return trip_name.lower().replace(" ", "_").replace("-", "_")


@tool(
    "create_trip",
    "Create a new trip to organize planning tasks. Returns the trip_id for adding tasks.",
    {
        "trip_name": str
    }
)
async def create_trip(args: dict[str, Any]) -> dict[str, Any]:
    """
    Create a new trip.

    Args:
        trip_name: Name of the trip (e.g., "Summer 2026 Marbella")

    Returns:
        Confirmation with trip_id
    """
    trip_name = args.get("trip_name")

    if not trip_name:
        return {
            "content": [{
                "type": "text",
                "text": "Error: trip_name is required"
            }],
            "is_error": True
        }

    await init_database()

    trip_id = generate_trip_id(trip_name)

    try:
        async with aiosqlite.connect(DB_PATH) as db:
            # Check if trip already exists
            async with db.execute(
                "SELECT trip_id FROM trips WHERE trip_id = ?",
                (trip_id,)
            ) as cursor:
                existing = await cursor.fetchone()

            if existing:
                return {
                    "content": [{
                        "type": "text",
                        "text": f"Trip '{trip_name}' already exists with ID: {trip_id}"
                    }]
                }

            # Insert new trip
            await db.execute(
                "INSERT INTO trips (trip_id, trip_name) VALUES (?, ?)",
                (trip_id, trip_name)
            )
            await db.commit()

        return {
            "content": [{
                "type": "text",
                "text": f"✓ Created trip '{trip_name}' with ID: {trip_id}\n\nYou can now add tasks using this trip_id."
            }]
        }

    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"Error creating trip: {str(e)}"
            }],
            "is_error": True
        }


@tool(
    "add_task",
    "Add a task to a trip with optional category, priority, and due date.",
    {
        "trip_id": str,
        "description": str,
        "category": str,
        "priority": str,
        "due_date": str
    }
)
async def add_task(args: dict[str, Any]) -> dict[str, Any]:
    """
    Add a task to a trip.

    Args:
        trip_id: The trip ID to add the task to
        description: Task description
        category: Optional category ('accommodation', 'activities', 'dining', 'transport', 'other')
        priority: Optional priority ('low', 'medium', 'high')
        due_date: Optional due date in ISO format (YYYY-MM-DD)

    Returns:
        Confirmation with task_id
    """
    trip_id = args.get("trip_id")
    description = args.get("description")
    category = args.get("category")
    priority = args.get("priority")
    due_date = args.get("due_date")

    if not trip_id or not description:
        return {
            "content": [{
                "type": "text",
                "text": "Error: trip_id and description are required"
            }],
            "is_error": True
        }

    await init_database()

    try:
        async with aiosqlite.connect(DB_PATH) as db:
            # Verify trip exists
            async with db.execute(
                "SELECT trip_name FROM trips WHERE trip_id = ?",
                (trip_id,)
            ) as cursor:
                trip = await cursor.fetchone()

            if not trip:
                return {
                    "content": [{
                        "type": "text",
                        "text": f"Error: Trip '{trip_id}' not found. Create it first using create_trip."
                    }],
                    "is_error": True
                }

            # Insert task
            cursor = await db.execute(
                """INSERT INTO tasks
                   (trip_id, description, category, priority, due_date, status)
                   VALUES (?, ?, ?, ?, ?, 'pending')""",
                (trip_id, description, category, priority, due_date)
            )
            task_id = cursor.lastrowid
            await db.commit()

        # Build response
        response = f"✓ Added task #{task_id}: {description}\n"
        if category:
            response += f"  Category: {category}\n"
        if priority:
            response += f"  Priority: {priority}\n"
        if due_date:
            response += f"  Due: {due_date}\n"
        response += f"  Trip: {trip[0]}"

        return {
            "content": [{
                "type": "text",
                "text": response
            }]
        }

    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"Error adding task: {str(e)}"
            }],
            "is_error": True
        }


@tool(
    "list_tasks",
    "List all tasks for a trip, optionally filtered by status.",
    {
        "trip_id": str,
        "status": str
    }
)
async def list_tasks(args: dict[str, Any]) -> dict[str, Any]:
    """
    List tasks for a trip.

    Args:
        trip_id: The trip ID to list tasks for
        status: Optional filter ('all', 'pending', 'completed'). Default: 'all'

    Returns:
        Formatted list of tasks
    """
    trip_id = args.get("trip_id")
    status_filter = args.get("status", "all").lower()

    if not trip_id:
        return {
            "content": [{
                "type": "text",
                "text": "Error: trip_id is required"
            }],
            "is_error": True
        }

    if status_filter not in ["all", "pending", "completed"]:
        status_filter = "all"

    await init_database()

    try:
        async with aiosqlite.connect(DB_PATH) as db:
            # Verify trip exists and get trip name
            async with db.execute(
                "SELECT trip_name FROM trips WHERE trip_id = ?",
                (trip_id,)
            ) as cursor:
                trip = await cursor.fetchone()

            if not trip:
                return {
                    "content": [{
                        "type": "text",
                        "text": f"Error: Trip '{trip_id}' not found"
                    }],
                    "is_error": True
                }

            # Build query based on status filter
            if status_filter == "all":
                query = "SELECT * FROM tasks WHERE trip_id = ? ORDER BY created_at"
                params = (trip_id,)
            else:
                query = "SELECT * FROM tasks WHERE trip_id = ? AND status = ? ORDER BY created_at"
                params = (trip_id, status_filter)

            async with db.execute(query, params) as cursor:
                tasks = await cursor.fetchall()

        if not tasks:
            return {
                "content": [{
                    "type": "text",
                    "text": f"No {status_filter} tasks found for '{trip[0]}'"
                }]
            }

        # Format tasks
        response = f"**Tasks for '{trip[0]}'** ({status_filter})\n\n"

        pending_count = 0
        completed_count = 0

        for task in tasks:
            task_id, t_trip_id, description, category, priority, due_date, status, created_at, completed_at = task

            if status == "pending":
                pending_count += 1
                status_icon = "☐"
            else:
                completed_count += 1
                status_icon = "✓"

            response += f"{status_icon} **#{task_id}** {description}\n"

            if category or priority or due_date:
                details = []
                if category:
                    details.append(f"Category: {category}")
                if priority:
                    details.append(f"Priority: {priority}")
                if due_date:
                    details.append(f"Due: {due_date}")
                response += f"    {' | '.join(details)}\n"

            if completed_at:
                response += f"    Completed: {completed_at}\n"

            response += "\n"

        # Summary
        response += "---\n"
        response += f"Total: {len(tasks)} tasks ({pending_count} pending, {completed_count} completed)"

        return {
            "content": [{
                "type": "text",
                "text": response
            }]
        }

    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"Error listing tasks: {str(e)}"
            }],
            "is_error": True
        }


@tool(
    "complete_task",
    "Mark a task as completed.",
    {
        "task_id": int
    }
)
async def complete_task(args: dict[str, Any]) -> dict[str, Any]:
    """
    Mark a task as completed.

    Args:
        task_id: The ID of the task to complete

    Returns:
        Confirmation with timestamp
    """
    task_id = args.get("task_id")

    if task_id is None:
        return {
            "content": [{
                "type": "text",
                "text": "Error: task_id is required"
            }],
            "is_error": True
        }

    await init_database()

    try:
        async with aiosqlite.connect(DB_PATH) as db:
            # Get task details before updating
            async with db.execute(
                "SELECT description, status FROM tasks WHERE task_id = ?",
                (task_id,)
            ) as cursor:
                task = await cursor.fetchone()

            if not task:
                return {
                    "content": [{
                        "type": "text",
                        "text": f"Error: Task #{task_id} not found"
                    }],
                    "is_error": True
                }

            description, current_status = task

            if current_status == "completed":
                return {
                    "content": [{
                        "type": "text",
                        "text": f"Task #{task_id} is already completed: {description}"
                    }]
                }

            # Update task status
            now = datetime.now().isoformat()
            await db.execute(
                "UPDATE tasks SET status = 'completed', completed_at = ? WHERE task_id = ?",
                (now, task_id)
            )
            await db.commit()

        return {
            "content": [{
                "type": "text",
                "text": f"✓ Completed task #{task_id}: {description}\nCompleted at: {now}"
            }]
        }

    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"Error completing task: {str(e)}"
            }],
            "is_error": True
        }


@tool(
    "update_task",
    "Update task details (description, category, priority, or due date).",
    {
        "task_id": int,
        "description": str,
        "category": str,
        "priority": str,
        "due_date": str
    }
)
async def update_task(args: dict[str, Any]) -> dict[str, Any]:
    """
    Update task details.

    Args:
        task_id: The ID of the task to update
        description: New description (optional)
        category: New category (optional)
        priority: New priority (optional)
        due_date: New due date (optional)

    Returns:
        Confirmation of updated fields
    """
    task_id = args.get("task_id")
    description = args.get("description")
    category = args.get("category")
    priority = args.get("priority")
    due_date = args.get("due_date")

    if task_id is None:
        return {
            "content": [{
                "type": "text",
                "text": "Error: task_id is required"
            }],
            "is_error": True
        }

    if not any([description, category, priority, due_date]):
        return {
            "content": [{
                "type": "text",
                "text": "Error: At least one field to update must be provided (description, category, priority, or due_date)"
            }],
            "is_error": True
        }

    await init_database()

    try:
        async with aiosqlite.connect(DB_PATH) as db:
            # Verify task exists
            async with db.execute(
                "SELECT description FROM tasks WHERE task_id = ?",
                (task_id,)
            ) as cursor:
                task = await cursor.fetchone()

            if not task:
                return {
                    "content": [{
                        "type": "text",
                        "text": f"Error: Task #{task_id} not found"
                    }],
                    "is_error": True
                }

            # Build update query dynamically
            updates = []
            params = []

            if description:
                updates.append("description = ?")
                params.append(description)
            if category:
                updates.append("category = ?")
                params.append(category)
            if priority:
                updates.append("priority = ?")
                params.append(priority)
            if due_date:
                updates.append("due_date = ?")
                params.append(due_date)

            params.append(task_id)  # For WHERE clause

            query = f"UPDATE tasks SET {', '.join(updates)} WHERE task_id = ?"
            await db.execute(query, params)
            await db.commit()

        # Build response
        updated_fields = []
        if description:
            updated_fields.append(f"description: {description}")
        if category:
            updated_fields.append(f"category: {category}")
        if priority:
            updated_fields.append(f"priority: {priority}")
        if due_date:
            updated_fields.append(f"due_date: {due_date}")

        return {
            "content": [{
                "type": "text",
                "text": f"✓ Updated task #{task_id}\nChanged: {', '.join(updated_fields)}"
            }]
        }

    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"Error updating task: {str(e)}"
            }],
            "is_error": True
        }


@tool(
    "delete_task",
    "Delete a task permanently.",
    {
        "task_id": int
    }
)
async def delete_task(args: dict[str, Any]) -> dict[str, Any]:
    """
    Delete a task.

    Args:
        task_id: The ID of the task to delete

    Returns:
        Confirmation
    """
    task_id = args.get("task_id")

    if task_id is None:
        return {
            "content": [{
                "type": "text",
                "text": "Error: task_id is required"
            }],
            "is_error": True
        }

    await init_database()

    try:
        async with aiosqlite.connect(DB_PATH) as db:
            # Get task details before deleting
            async with db.execute(
                "SELECT description FROM tasks WHERE task_id = ?",
                (task_id,)
            ) as cursor:
                task = await cursor.fetchone()

            if not task:
                return {
                    "content": [{
                        "type": "text",
                        "text": f"Error: Task #{task_id} not found"
                    }],
                    "is_error": True
                }

            description = task[0]

            # Delete task
            await db.execute(
                "DELETE FROM tasks WHERE task_id = ?",
                (task_id,)
            )
            await db.commit()

        return {
            "content": [{
                "type": "text",
                "text": f"✓ Deleted task #{task_id}: {description}"
            }]
        }

    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"Error deleting task: {str(e)}"
            }],
            "is_error": True
        }


@tool(
    "list_trips",
    "List all trips with task counts.",
    {}
)
async def list_trips(args: dict[str, Any]) -> dict[str, Any]:
    """
    List all trips with task counts.

    Returns:
        List of all trips with task statistics
    """
    await init_database()

    try:
        async with aiosqlite.connect(DB_PATH) as db:
            # Get all trips with task counts
            async with db.execute("""
                SELECT
                    t.trip_id,
                    t.trip_name,
                    t.created_at,
                    COUNT(CASE WHEN tk.status = 'pending' THEN 1 END) as pending_count,
                    COUNT(CASE WHEN tk.status = 'completed' THEN 1 END) as completed_count,
                    COUNT(tk.task_id) as total_count
                FROM trips t
                LEFT JOIN tasks tk ON t.trip_id = tk.trip_id
                GROUP BY t.trip_id, t.trip_name, t.created_at
                ORDER BY t.created_at DESC
            """) as cursor:
                trips = await cursor.fetchall()

        if not trips:
            return {
                "content": [{
                    "type": "text",
                    "text": "No trips found. Create a trip using create_trip to get started!"
                }]
            }

        # Format trips
        response = "**Your Trips:**\n\n"

        for trip in trips:
            trip_id, trip_name, created_at, pending, completed, total = trip

            response += f"**{trip_name}** (ID: {trip_id})\n"
            response += f"  Created: {created_at}\n"
            response += f"  Tasks: {total} total ({pending} pending, {completed} completed)\n\n"

        return {
            "content": [{
                "type": "text",
                "text": response
            }]
        }

    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"Error listing trips: {str(e)}"
            }],
            "is_error": True
        }
