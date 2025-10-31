import streamlit as st
from todoist_api_python.api import TodoistAPI
from datetime import datetime, timedelta
from typing import List, Dict, Any


class TodoistFetcher:
    def __init__(self, api_token: str):
        self.api = TodoistAPI(api_token)

    @st.cache_data(ttl=300)
    def get_completed_tasks(_self, days: int = 7) -> List[Dict[str, Any]]:
        """Fetch completed tasks from the last N days"""
        try:
            # Get all tasks
            tasks = _self.api.get_tasks()

            # Filter completed tasks
            # Note: Todoist API doesn't directly provide completed tasks
            # We'll need to use the sync API or activity log
            # For now, return active tasks as placeholder
            return [
                {
                    "content": task.content,
                    "completed_at": None,
                    "project_id": task.project_id
                }
                for task in tasks[:5]  # Limit to 5 for demo
            ]
        except Exception as e:
            st.error(f"Todoist API error: {e}")
            return []

    def get_active_tasks(self, project_id: str = None) -> List[Dict[str, Any]]:
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
