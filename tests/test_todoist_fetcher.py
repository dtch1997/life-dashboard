import pytest
from unittest.mock import Mock, MagicMock, patch
from fetchers.todoist_fetcher import TodoistFetcher


class TestTodoistFetcher:
    """Tests for TodoistFetcher class"""

    @pytest.fixture
    def mock_api(self):
        """Mock TodoistAPI instance"""
        return Mock()

    @pytest.fixture
    def fetcher(self, mock_api):
        """Create TodoistFetcher with mocked API"""
        with patch('fetchers.todoist_fetcher.TodoistAPI', return_value=mock_api):
            return TodoistFetcher("fake_token")

    def test_init(self):
        """Test fetcher initialization"""
        with patch('fetchers.todoist_fetcher.TodoistAPI') as mock_api_class:
            fetcher = TodoistFetcher("test_token")
            mock_api_class.assert_called_once_with("test_token")
            assert fetcher.api is not None

    def test_get_active_tasks_success(self, fetcher, mock_api):
        """Test successful retrieval of active tasks"""
        # Mock task objects
        mock_task1 = Mock()
        mock_task1.id = "1"
        mock_task1.content = "Task 1"
        mock_task1.description = "Description 1"
        mock_task1.is_completed = False
        mock_task1.priority = 2
        mock_task1.project_id = "project1"

        mock_task2 = Mock()
        mock_task2.id = "2"
        mock_task2.content = "Task 2"
        mock_task2.description = "Description 2"
        mock_task2.is_completed = False
        mock_task2.priority = 1
        mock_task2.project_id = "project2"

        # Mock paginator that returns tasks when converted to list
        mock_paginator = MagicMock()
        mock_paginator.__iter__ = Mock(return_value=iter([mock_task1, mock_task2]))
        mock_api.get_tasks.return_value = mock_paginator

        # Call method
        tasks = fetcher.get_active_tasks()

        # Assertions
        assert len(tasks) == 2
        assert tasks[0]["id"] == "1"
        assert tasks[0]["content"] == "Task 1"
        assert tasks[0]["description"] == "Description 1"
        assert tasks[0]["priority"] == 2
        assert tasks[1]["id"] == "2"
        assert tasks[1]["content"] == "Task 2"

    def test_get_active_tasks_with_project_filter(self, fetcher, mock_api):
        """Test getting tasks filtered by project"""
        mock_task = Mock()
        mock_task.id = "1"
        mock_task.content = "Project Task"
        mock_task.description = ""
        mock_task.is_completed = False
        mock_task.priority = 1
        mock_task.project_id = "project123"

        mock_paginator = MagicMock()
        mock_paginator.__iter__ = Mock(return_value=iter([mock_task]))
        mock_api.get_tasks.return_value = mock_paginator

        tasks = fetcher.get_active_tasks(project_id="project123")

        mock_api.get_tasks.assert_called_once_with(project_id="project123")
        assert len(tasks) == 1
        assert tasks[0]["project_id"] == "project123"

    def test_get_active_tasks_empty_result(self, fetcher, mock_api):
        """Test when no tasks are returned"""
        mock_paginator = MagicMock()
        mock_paginator.__iter__ = Mock(return_value=iter([]))
        mock_api.get_tasks.return_value = mock_paginator

        tasks = fetcher.get_active_tasks()

        assert tasks == []

    def test_get_active_tasks_api_error(self, fetcher, mock_api):
        """Test handling of API errors"""
        mock_api.get_tasks.side_effect = Exception("API Error")

        # Patch streamlit to avoid import errors in tests
        with patch('fetchers.todoist_fetcher.st') as mock_st:
            tasks = fetcher.get_active_tasks()

            assert tasks == []
            mock_st.error.assert_called_once()

    def test_get_active_tasks_missing_attributes(self, fetcher, mock_api):
        """Test handling of tasks with missing optional attributes"""
        mock_task = Mock()
        mock_task.id = "1"
        mock_task.content = "Minimal Task"
        # Simulate missing attributes
        del mock_task.description
        del mock_task.is_completed
        del mock_task.priority
        del mock_task.project_id

        mock_paginator = MagicMock()
        mock_paginator.__iter__ = Mock(return_value=iter([mock_task]))
        mock_api.get_tasks.return_value = mock_paginator

        tasks = fetcher.get_active_tasks()

        # Should use defaults from getattr
        assert len(tasks) == 1
        assert tasks[0]["id"] == "1"
        assert tasks[0]["content"] == "Minimal Task"
        assert tasks[0]["description"] == ""
        assert tasks[0]["is_completed"] == False
        assert tasks[0]["priority"] == 1
        assert tasks[0]["project_id"] == ""
