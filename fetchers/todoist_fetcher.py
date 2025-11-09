import streamlit as st
from todoist_api_python.api import TodoistAPI
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from collections import defaultdict


class TodoistFetcher:
    def __init__(self, api_token: str):
        self.api = TodoistAPI(api_token)

    @st.cache_data(ttl=300)
    def get_completed_today(_self, priority: Optional[int] = None) -> List[Dict[str, Any]]:
        """Fetch tasks completed today, optionally filtered by priority"""
        try:
            # Get completed tasks by completion date (requires since and until)
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)

            result = _self.api.get_completed_tasks_by_completion_date(
                since=today_start,
                until=today_end,
                limit=100
            )

            # Handle paginator and flatten
            tasks_raw = list(result)
            tasks = []
            for item in tasks_raw:
                if isinstance(item, list):
                    tasks.extend(item)
                else:
                    tasks.append(item)

            # Filter by priority if specified (priority 4 = p1 in Todoist)
            completed_tasks = []
            for task in tasks:
                task_priority = getattr(task, 'priority', 1)

                # Check priority if specified
                if priority is not None and task_priority != priority:
                    continue

                completed_tasks.append({
                    "content": getattr(task, 'content', ''),
                    "completed_at": getattr(task, 'completed_at', None),
                    "priority": task_priority,
                    "project_id": getattr(task, 'project_id', '')
                })

            return completed_tasks
        except Exception as e:
            import traceback
            st.error(f"Todoist API error: {e}")
            st.error(f"Traceback: {traceback.format_exc()}")
            return []

    def get_active_tasks(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get active tasks, optionally filtered by project"""
        try:
            if project_id:
                result = self.api.get_tasks(project_id=project_id)
            else:
                result = self.api.get_tasks()

            # Convert paginator to list and flatten if needed
            tasks_raw = list(result)

            # Flatten if we got nested lists
            tasks = []
            for item in tasks_raw:
                if isinstance(item, list):
                    tasks.extend(item)
                else:
                    tasks.append(item)

            return [
                {
                    "id": task.id,
                    "content": task.content,
                    "description": getattr(task, 'description', ''),
                    "is_completed": getattr(task, 'is_completed', False),
                    "priority": getattr(task, 'priority', 1),
                    "project_id": getattr(task, 'project_id', '')
                }
                for task in tasks
            ]
        except Exception as e:
            import traceback
            st.error(f"Todoist API error: {e}")
            st.error(f"Traceback: {traceback.format_exc()}")
            return []

    @st.cache_data(ttl=3600)
    def get_contribution_data(_self, days: int = 365) -> Dict[str, int]:
        """Fetch completed tasks for the last N days and aggregate by date.

        Args:
            days: Number of days to fetch (default: 365)

        Returns:
            Dictionary mapping date strings (YYYY-MM-DD) to task counts
        """
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days - 1)

            # Aggregate by date
            contributions = defaultdict(int)

            # Initialize all dates with 0
            current_date = start_date.date()
            end = end_date.date()
            while current_date <= end:
                contributions[current_date.strftime("%Y-%m-%d")] = 0
                current_date += timedelta(days=1)

            # Query in 30-day chunks to avoid API limits
            chunk_start = start_date
            while chunk_start < end_date:
                chunk_end = min(chunk_start + timedelta(days=29), end_date)

                # Get completed tasks for this chunk
                result = _self.api.get_completed_tasks_by_completion_date(
                    since=chunk_start.replace(hour=0, minute=0, second=0, microsecond=0),
                    until=chunk_end.replace(hour=23, minute=59, second=59, microsecond=999999),
                    limit=200  # Reduced limit
                )

                # Handle paginator and flatten
                tasks_raw = list(result)
                tasks = []
                for item in tasks_raw:
                    if isinstance(item, list):
                        tasks.extend(item)
                    else:
                        tasks.append(item)

                # Count tasks by completion date
                for task in tasks:
                    completed_at = getattr(task, 'completed_at', None)
                    if completed_at:
                        # Parse the completed_at timestamp
                        if isinstance(completed_at, str):
                            completed_date = datetime.fromisoformat(completed_at.replace('Z', '+00:00')).date()
                        else:
                            completed_date = completed_at.date()

                        date_str = completed_date.strftime("%Y-%m-%d")
                        contributions[date_str] += 1

                # Move to next chunk
                chunk_start = chunk_end + timedelta(days=1)

            return dict(contributions)
        except Exception as e:
            import traceback
            st.error(f"Todoist API error fetching contribution data: {e}")
            st.error(f"Traceback: {traceback.format_exc()}")
            return {}
