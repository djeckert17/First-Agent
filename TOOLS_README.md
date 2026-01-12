# Trip Planning Tools - User Guide

## Overview

The Marbella travel agent now includes two powerful custom tools to enhance trip planning:

1. **Weather Tool** - Real-time weather forecasts from yr.no API for any location
2. **Task Manager** - Organize trip planning with persistent SQLite database

Both tools are integrated with the conversational agent, maintaining context across your entire planning session.

---

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Verify setup
python verify_setup.py
```

### Try the Demos

```bash
# Quick test (3 queries, ~30 seconds)
python tool_examples.py quick

# Weather demo - Multi-location forecasts
python tool_examples.py weather

# Task management - Full workflow
python tool_examples.py tasks

# Combined scenario - Weather + tasks integration
python tool_examples.py combined

# Run all demos
python tool_examples.py all
```

---

## Using the Tools

### Interactive Planning Session

**Conversational Agent (Recommended):**
```bash
python conversational_agent.py
```

The conversational agent remembers context across multiple turns, making it ideal for trip planning.

**Stateless Agent:**
```bash
python marbella_agent.py
```

Each query is independent with no memory of previous interactions.

---

## Weather Tool

### What It Does

- Fetches real-time weather forecasts from yr.no (Norwegian Meteorological Institute)
- Returns current conditions + 3-day forecast
- Supports any location worldwide via latitude/longitude
- **Temperatures in Fahrenheit by default** (Celsius option available)

### How to Use

**Basic Query:**
```
"What's the weather in Marbella?"
```

**Specific Location:**
```
"Check the weather in Granada"
"What's the forecast for Málaga?"
```

**Compare Locations:**
```
"Compare weather between Marbella and Granada"
"Should I visit Ronda or stay in Marbella based on weather?"
```

**Request Celsius:**
```
"Give me the Marbella weather in Celsius"
```

### Common Coordinates

For the agent's reference, these coordinates are built-in:

| Location | Latitude | Longitude |
|----------|----------|-----------|
| Marbella | 36.51 | -4.88 |
| Granada | 37.18 | -3.60 |
| Málaga | 36.72 | -4.42 |
| Ronda | 36.74 | -5.17 |

### Weather Output Includes

- Current temperature (°F and °C)
- Wind speed and direction
- Humidity percentage
- Precipitation amounts
- Weather conditions (clear, cloudy, rain, etc.)
- 3-day forecast summary
- Travel tips based on conditions

### Example Output

```
**Weather Forecast for Marbella**

Current Conditions:
- Temperature: 55.8°F (13.2°C)
- Wind: 1.6 m/s from 140°
- Humidity: 79%
- Conditions: Partly Cloudy

3-Day Forecast:
- 2026-01-12: 55.8°F, Partly Cloudy
- 2026-01-13: 57.2°F, Rain
- 2026-01-14: 55.4°F, Clear

Coordinates: 36.51°, -4.88°
Data provided by yr.no / Norwegian Meteorological Institute
```

---

## Task Manager

### What It Does

- Organize planning tasks by trip
- Track categories (accommodation, activities, dining, transport)
- Set priorities (low, medium, high)
- Add due dates
- Mark tasks complete
- Persistent SQLite database (survives restarts)

### Database Location

Tasks are stored in `trips_database.db` in the project root (automatically created on first use).

### Creating a Trip

**Start with a trip to organize your tasks:**
```
"Create a trip called Summer 2026 Marbella"
"Start a new trip: Anniversary in Spain"
```

**Trip ID:** Automatically generated from name (e.g., "Summer 2026 Marbella" → `summer_2026_marbella`)

### Adding Tasks

**Basic Task:**
```
"Add a task to book a hotel"
```

**With Priority:**
```
"Add a high priority task to book flights"
```

**With Category:**
```
"Add a dining task to reserve table at El Oceano, medium priority"
```

**With Due Date:**
```
"Add task: Book accommodation, high priority, due June 1st"
```

**Full Example:**
```
"Add a task to rent a car for day trips, category transport, low priority, due June 15, 2026"
```

### Task Categories

- `accommodation` - Hotels, villas, apartments
- `activities` - Water sports, golf, excursions, tours
- `dining` - Restaurant reservations, food experiences
- `transport` - Flights, car rentals, transfers
- `other` - Insurance, packing, documentation

### Priority Levels

- `high` - Must do, time-sensitive
- `medium` - Important but flexible
- `low` - Nice to have, optional

### Viewing Tasks

**All Tasks:**
```
"Show me all my tasks"
"List tasks for Summer 2026 Marbella"
```

**Filter by Status:**
```
"Show my pending tasks"
"List completed tasks"
"What tasks are still pending?"
```

**All Trips Overview:**
```
"List all my trips"
"What trips do I have?"
```

### Managing Tasks

**Complete a Task:**
```
"Mark task #5 as completed"
"Complete the hotel booking task"
```

**Update Task Details:**
```
"Update task #3 to include restaurant name: La Sala"
"Change task #7 priority to high"
"Update task #2 due date to June 20"
```

**Delete a Task:**
```
"Delete task #8"
"Remove the car rental task"
```

### Example Task List Output

```
**Tasks for 'Summer 2026 Marbella'** (all)

☐ **#1** Book accommodation at beachfront hotel
    Category: accommodation | Priority: high | Due: 2026-06-01

✓ **#2** Book water sports lesson at El Oceano Beach
    Category: activities | Priority: high | Due: 2026-06-15
    Completed: 2026-01-12T12:45:30

☐ **#3** Reserve table at seafood restaurant
    Category: dining | Priority: medium

---
Total: 3 tasks (2 pending, 1 completed)
```

---

## Example Workflows

### Planning a Trip from Scratch

```
You: "I'm planning a summer trip to Marbella. What's the typical weather like?"

Agent: [Provides weather forecast and seasonal info]

You: "Perfect! Create a trip called Summer_2026_Getaway"

Agent: [Creates trip with ID: summer_2026_getaway]

You: "Add these tasks:
- Book beachfront hotel, high priority, due May 1st
- Reserve table at nice seafood restaurant, medium priority
- Book water sports lesson, high priority, due June 15th
- Rent a car for day trips, low priority"

Agent: [Adds all 4 tasks with appropriate categories]

You: "Show me my task list organized by priority"

Agent: [Displays formatted task list]

You: "I booked the hotel. Mark task #1 as complete"

Agent: [Marks complete with timestamp]
```

### Weather-Based Planning

```
You: "Check weather for Marbella, Granada, and Málaga"

Agent: [Fetches all 3 forecasts]

You: "Granada looks best. Create a trip and add a Granada day trip task"

Agent: [Creates trip, adds task with weather considerations]

You: "What should I pack based on that weather?"

Agent: [Provides packing recommendations based on forecast]
```

### Multi-Day Itinerary Building

```
You: "Create a trip called Marbella_Week_2026"

Agent: [Creates trip]

You: "Based on the weather forecast, suggest activities for each day and create tasks"

Agent: [Analyzes forecast, suggests activities, creates dated tasks]

You: "Add restaurant reservations for each evening, medium priority"

Agent: [Adds dining tasks]

You: "Show my complete itinerary"

Agent: [Lists all tasks organized by date]
```

---

## Tips for Best Results

### Weather Queries

✅ **Do:**
- Ask about specific locations
- Request comparisons between cities
- Ask for weather-based activity recommendations
- Mention if you prefer Celsius

❌ **Avoid:**
- Asking for forecasts beyond 3 days (API limitation)
- Expecting historical weather data

### Task Management

✅ **Do:**
- Create a trip first before adding tasks
- Use descriptive task names
- Set priorities and due dates
- Review your task list regularly
- Mark tasks complete as you finish them

❌ **Avoid:**
- Adding tasks without a trip_id
- Using very generic task names ("todo", "thing")
- Forgetting to specify trip when listing tasks

### Using the Conversational Agent

✅ **Do:**
- Ask follow-up questions naturally
- Reference previous tasks ("that restaurant we discussed")
- Build on earlier context
- Let the agent remember your preferences

❌ **Avoid:**
- Starting completely new topics without context
- Assuming the agent knows unstated information
- Using the stateless agent for multi-turn planning

---

## Troubleshooting

### Weather Tool Issues

**Problem:** "Weather API rate limit exceeded"
**Solution:** Wait a few minutes before making another request. yr.no has rate limits.

**Problem:** Invalid coordinates error
**Solution:** Ensure latitude is between -90 and 90, longitude between -180 and 180.

**Problem:** Network timeout
**Solution:** Check your internet connection. The tool requires internet access to fetch data.

### Task Manager Issues

**Problem:** "Trip not found"
**Solution:** Create the trip first with `create_trip`, then add tasks to it.

**Problem:** "Task ID not found"
**Solution:** List tasks to see available IDs. Task IDs are assigned sequentially.

**Problem:** Database locked error
**Solution:** Only one process can write to the database at a time. Close other instances.

**Problem:** Can't find trips_database.db
**Solution:** The database is created automatically on first use in the project root directory.

### General Issues

**Problem:** "Module not found" errors
**Solution:** Run `pip install -r requirements.txt` to install dependencies.

**Problem:** API key errors
**Solution:** Ensure `ANTHROPIC_API_KEY` is set in your `.env` file.

**Problem:** Tools not available in agent
**Solution:** Make sure you're using the updated agent files that import `travel_tools_server`.

---

## Technical Details

### Weather Tool API

- **Provider:** yr.no / Norwegian Meteorological Institute
- **Endpoint:** `https://api.met.no/weatherapi/locationforecast/2.0/compact`
- **Rate Limits:** Standard API limits apply
- **Data Format:** JSON
- **Temperature Unit:** Celsius (converted to Fahrenheit by default)
- **Forecast Range:** 9 days (we show 3 days)

### Task Manager Database

**Schema:**

```sql
-- Trips table
CREATE TABLE trips (
    trip_id TEXT PRIMARY KEY,
    trip_name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tasks table
CREATE TABLE tasks (
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
);
```

**File:** `trips_database.db` (SQLite 3)
**Location:** Project root directory
**Size:** ~20KB empty, grows with data
**Backup:** Copy the .db file to backup your trips

---

## Privacy & Data

- **Weather data:** Fetched from public yr.no API, no personal data sent
- **Task data:** Stored locally in SQLite database
- **Database:** Added to `.gitignore` to prevent accidental commits
- **No cloud sync:** All data stays on your machine
- **No authentication:** Single-user, local-only storage

---

## Advanced Usage

### Custom Locations

You can ask about any location worldwide:

```
"What's the weather at coordinates 40.7128, -74.0060?" (New York)
"Check weather at latitude 51.5074, longitude -0.1278" (London)
```

### Batch Task Operations

Add multiple tasks in one message:

```
"Add these tasks to my trip:
1. Book hotel - high priority - due June 1
2. Reserve dinner - medium priority - due June 15
3. Rent car - low priority - due June 10"
```

### Export Trip Data

Query the database directly:

```bash
sqlite3 trips_database.db "SELECT * FROM tasks WHERE trip_id='summer_2026_marbella';"
```

### Multiple Trips

Organize different trips independently:

```
"Create trip Europe_Summer_2026"
"Create trip Weekend_Getaway_Granada"
"List all my trips"
```

---

## Future Enhancements

Planned improvements (not yet implemented):

- Weather caching to reduce API calls
- Task reminders/notifications
- Export tasks to PDF/Calendar
- Multi-user support with authentication
- Weather alerts for trip dates
- Integration with booking APIs

---

## Support

**Documentation:**
- Main README: `README.md`
- Project overview: `CLAUDE.md`
- Getting started: `GETTING_STARTED.md`

**Running Examples:**
```bash
python tool_examples.py      # Show demo menu
python verify_setup.py       # Verify installation
python conversational_agent.py  # Start interactive session
```

**Common Commands:**
- Weather: "What's the weather in [location]?"
- Create trip: "Create a trip called [name]"
- Add task: "Add a task to [description], [priority], due [date]"
- List tasks: "Show my tasks for [trip_name]"
- Complete: "Mark task #[id] as completed"

---

## Credits

- Weather data: [yr.no](https://www.yr.no) / Norwegian Meteorological Institute
- Database: SQLite
- HTTP client: aiohttp
- Agent SDK: Claude Agent SDK for Python

---

**Version:** 1.0.0
**Last Updated:** January 12, 2026
**License:** See project LICENSE file
