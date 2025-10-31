# Life Dashboard - Design Document
## Streamlit Implementation

### Project Overview
A personal life dashboard that aggregates data from multiple sources (Todoist, Google Docs/Sheets, GitHub, etc.) into a unified, customizable interface. Built with Streamlit for rapid development and easy deployment.

### Core Requirements
- **Multi-source data aggregation**: Pull from various APIs and services
- **Flexible panel system**: Easy to add/remove/configure panels
- **Secure credential management**: Safe storage of API keys
- **Auto-refresh capabilities**: Keep data current without manual intervention
- **Free hosting**: Deploy without ongoing costs
- **Mobile responsive**: Usable on phone/tablet

---

## Architecture

### High-Level Architecture
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│  Streamlit App  │────▶│  Data Fetchers  │────▶│  External APIs  │
│   (app.py)      │     │   (./fetchers)  │     │  (Todoist, etc) │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │
│   UI Renderer   │     │  Cache Layer    │
│  (./components) │     │  (st.cache_data)│
│                 │     │                 │
└─────────────────┘     └─────────────────┘
```

### Component Structure
```
life-dashboard/
├── app.py                      # Main application entry point
├── requirements.txt            # Python dependencies
├── config.py                   # Dashboard configuration
├── .streamlit/
│   ├── config.toml            # Streamlit UI configuration
│   └── secrets.toml           # Local secrets (gitignored)
├── fetchers/
│   ├── __init__.py
│   ├── base.py                # Abstract fetcher class
│   ├── todoist_fetcher.py     # Todoist API integration
│   ├── google_fetcher.py      # Google Sheets/Docs integration
│   ├── github_fetcher.py      # GitHub API integration
│   └── weather_fetcher.py     # Weather API integration
├── components/
│   ├── __init__.py
│   ├── panels.py              # Panel rendering logic
│   ├── metrics.py             # Metric card components
│   └── charts.py              # Chart components
├── utils/
│   ├── __init__.py
│   ├── date_helpers.py        # Date/time utilities
│   ├── formatting.py          # Text formatting utilities
│   └── cache_manager.py       # Cache management
└── tests/
    ├── test_fetchers.py
    └── test_components.py
```

---

## Dependencies

### Core Dependencies

```txt
# requirements.txt
# Core
streamlit==1.32.0               # Main framework
pandas==2.2.0                   # Data manipulation
python-dotenv==1.0.0            # Environment variable management

# API Clients
todoist-api-python==2.1.3      # Official Todoist client
google-auth==2.27.0             # Google authentication
google-auth-oauthlib==1.2.0     # Google OAuth flow
google-auth-httplib2==0.2.0
gspread==6.0.0                  # Google Sheets client
PyGithub==2.1.1                 # GitHub API client
requests==2.31.0                # HTTP requests for generic APIs

# Data Visualization
plotly==5.19.0                  # Interactive charts
altair==5.2.0                   # Declarative charts
matplotlib==3.8.0               # Static charts (optional)

# Utilities
pytz==2024.1                    # Timezone handling
python-dateutil==2.8.2          # Date parsing
pyyaml==6.0.1                   # YAML config parsing
```

### Optional Dependencies

```txt
# requirements-dev.txt
pytest==8.0.0                   # Testing
black==24.1.0                   # Code formatting
pylint==3.0.0                   # Linting
streamlit-autorefresh==1.0.1    # Auto-refresh component
streamlit-elements==0.1.0       # Advanced UI components
```

---

## API Integrations

### 1. Todoist Integration

**API Endpoints Needed:**
- `GET /tasks` - Active tasks
- `GET /completed/get_all` - Completed tasks
- `GET /projects` - Project list

**Implementation:**
```python
# fetchers/todoist_fetcher.py
from todoist_api_python import TodoistAPI
from datetime import datetime, timedelta
import streamlit as st

class TodoistFetcher:
    def __init__(self):
        self.api = TodoistAPI(st.secrets["todoist_api_key"])
    
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_completed_this_week(_self):
        """Fetch completed tasks from the last 7 days"""
        # Note: _self prefix tells Streamlit not to hash this parameter
        try:
            tasks = _self.api.get_completed_items()
            week_ago = datetime.now() - timedelta(days=7)
            return [
                task for task in tasks 
                if task.completed_at > week_ago
            ]
        except Exception as e:
            st.error(f"Todoist API error: {e}")
            return []
    
    def get_active_tasks(self, project_id=None):
        """Get active tasks, optionally filtered by project"""
        filters = {"project_id": project_id} if project_id else {}
        return self.api.get_tasks(**filters)
```

### 2. Google Sheets Integration

**Setup Required:**
1. Create service account in Google Cloud Console
2. Share sheets with service account email
3. Store service account JSON in secrets

**Implementation:**
```python
# fetchers/google_fetcher.py
import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
import json

class GoogleSheetsFetcher:
    def __init__(self):
        creds_dict = json.loads(st.secrets["gcp_service_account"])
        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        self.client = gspread.authorize(creds)
    
    @st.cache_data(ttl=600)  # Cache for 10 minutes
    def get_sheet_data(_self, sheet_name, range_name):
        """Fetch data from a specific sheet and range"""
        try:
            sheet = _self.client.open(sheet_name)
            worksheet = sheet.sheet1
            return worksheet.get(range_name)
        except Exception as e:
            st.error(f"Google Sheets error: {e}")
            return []
```

### 3. GitHub Integration

**Implementation:**
```python
# fetchers/github_fetcher.py
from github import Github
import streamlit as st

class GitHubFetcher:
    def __init__(self):
        self.g = Github(st.secrets.get("github_token", None))
        self.user = self.g.get_user()
    
    @st.cache_data(ttl=900)  # Cache for 15 minutes
    def get_recent_commits(_self, days=7):
        """Get recent commits across all repos"""
        commits = []
        since = datetime.now() - timedelta(days=days)
        
        for repo in _self.user.get_repos():
            try:
                repo_commits = repo.get_commits(
                    author=_self.user,
                    since=since
                )
                commits.extend(list(repo_commits))
            except:
                continue
        
        return sorted(commits, key=lambda x: x.commit.date, reverse=True)
```

---

## Panel System Design

### Panel Configuration

```python
# config.py
from enum import Enum
from typing import Dict, Any, Callable
from dataclasses import dataclass

class PanelSize(Enum):
    SMALL = "small"   # 1/3 width
    MEDIUM = "medium" # 1/2 width  
    LARGE = "large"   # full width

@dataclass
class PanelConfig:
    id: str
    title: str
    icon: str
    fetcher: str  # Name of fetcher class
    render_func: str  # Name of render function
    size: PanelSize
    refresh_interval: int  # seconds
    enabled: bool = True
    config: Dict[str, Any] = None

# Panel definitions
PANELS = [
    PanelConfig(
        id="todoist_wins",
        title="Weekly Wins",
        icon="🏆",
        fetcher="TodoistFetcher",
        render_func="render_todoist_wins",
        size=PanelSize.SMALL,
        refresh_interval=300,
        config={"filter": "completed", "days": 7}
    ),
    PanelConfig(
        id="current_thoughts",
        title="Current Thoughts",
        icon="💭",
        fetcher="GoogleSheetsFetcher", 
        render_func="render_thoughts",
        size=PanelSize.MEDIUM,
        refresh_interval=600,
        config={"sheet": "Life Dashboard", "range": "A1:A5"}
    ),
    PanelConfig(
        id="github_activity",
        title="Code Activity",
        icon="💻",
        fetcher="GitHubFetcher",
        render_func="render_github",
        size=PanelSize.SMALL,
        refresh_interval=900,
        config={"days": 7}
    ),
]
```

### Panel Renderer

```python
# components/panels.py
import streamlit as st
from typing import Dict, Any
import importlib

class PanelRenderer:
    def __init__(self):
        self.fetchers = {}
        self._initialize_fetchers()
    
    def _initialize_fetchers(self):
        """Dynamically load fetcher classes"""
        for panel in PANELS:
            if panel.fetcher not in self.fetchers:
                module = importlib.import_module(f'fetchers.{panel.fetcher.lower()}')
                fetcher_class = getattr(module, panel.fetcher)
                self.fetchers[panel.fetcher] = fetcher_class()
    
    def render_panel(self, panel: PanelConfig):
        """Render a single panel"""
        with st.container():
            st.subheader(f"{panel.icon} {panel.title}")
            
            # Get fetcher and fetch data
            fetcher = self.fetchers[panel.fetcher]
            
            # Call the appropriate render function
            render_func = getattr(self, panel.render_func)
            render_func(fetcher, panel.config)
    
    def render_todoist_wins(self, fetcher, config):
        """Render Todoist completed tasks"""
        tasks = fetcher.get_completed_this_week()
        
        if tasks:
            for task in tasks[:5]:  # Show top 5
                st.checkbox(
                    task.content,
                    value=True,
                    disabled=True,
                    key=f"task_{task.id}"
                )
        else:
            st.info("No completed tasks this week")
```

---

## State Management

### Session State Structure

```python
# app.py - State initialization
def initialize_state():
    """Initialize session state variables"""
    if 'last_refresh' not in st.session_state:
        st.session_state.last_refresh = datetime.now()
    
    if 'selected_panels' not in st.session_state:
        st.session_state.selected_panels = [p.id for p in PANELS if p.enabled]
    
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    
    if 'date_range' not in st.session_state:
        st.session_state.date_range = (
            datetime.now() - timedelta(days=7),
            datetime.now()
        )
```

### Caching Strategy

```python
# utils/cache_manager.py
import streamlit as st
from datetime import datetime, timedelta
from functools import wraps

def timed_cache(seconds=300):
    """Custom cache decorator with time-based expiration"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}_{str(args)}_{str(kwargs)}"
            cache_time_key = f"{cache_key}_time"
            
            # Check if cache exists and is still valid
            if cache_key in st.session_state:
                cached_time = st.session_state.get(cache_time_key)
                if cached_time and (datetime.now() - cached_time).seconds < seconds:
                    return st.session_state[cache_key]
            
            # Fetch new data
            result = func(*args, **kwargs)
            st.session_state[cache_key] = result
            st.session_state[cache_time_key] = datetime.now()
            
            return result
        return wrapper
    return decorator
```

---

## Main Application

```python
# app.py
import streamlit as st
from datetime import datetime
from components.panels import PanelRenderer
from config import PANELS, PanelSize
import time

# Page config
st.set_page_config(
    page_title="Life Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def main():
    # Initialize state
    initialize_state()
    
    # Header
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.title("🎯 Life Dashboard")
    with col2:
        st.caption(f"Last refresh: {st.session_state.last_refresh.strftime('%H:%M')}")
    with col3:
        if st.button("🔄 Refresh"):
            st.session_state.last_refresh = datetime.now()
            st.cache_data.clear()
            st.rerun()
    
    # Settings sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Panel selection
        selected = st.multiselect(
            "Active Panels",
            options=[p.id for p in PANELS],
            default=st.session_state.selected_panels,
            format_func=lambda x: next(p.title for p in PANELS if p.id == x)
        )
        st.session_state.selected_panels = selected
        
        # Date range filter
        date_range = st.date_input(
            "Date Range",
            value=st.session_state.date_range,
            max_value=datetime.now()
        )
        
        # Auto-refresh
        auto_refresh = st.checkbox("Auto-refresh (5 min)")
        if auto_refresh:
            st.empty()  # Placeholder for auto-refresh logic
    
    # Main dashboard area
    renderer = PanelRenderer()
    
    # Group panels by row based on size
    active_panels = [p for p in PANELS if p.id in st.session_state.selected_panels]
    
    # Render panels in dynamic layout
    current_row = []
    current_width = 0
    
    for panel in active_panels:
        panel_width = {
            PanelSize.SMALL: 1,
            PanelSize.MEDIUM: 2,
            PanelSize.LARGE: 3
        }[panel.size]
        
        if current_width + panel_width > 3:
            # Render current row
            render_row(current_row, renderer)
            current_row = [panel]
            current_width = panel_width
        else:
            current_row.append(panel)
            current_width += panel_width
    
    # Render final row
    if current_row:
        render_row(current_row, renderer)

def render_row(panels, renderer):
    """Render a row of panels"""
    if not panels:
        return
    
    # Calculate column widths
    widths = []
    for panel in panels:
        if panel.size == PanelSize.SMALL:
            widths.append(1)
        elif panel.size == PanelSize.MEDIUM:
            widths.append(2)
        else:  # LARGE
            widths.append(3)
    
    # Create columns
    cols = st.columns(widths)
    
    # Render panels in columns
    for col, panel in zip(cols, panels):
        with col:
            renderer.render_panel(panel)

if __name__ == "__main__":
    main()
```

---

## Deployment Strategy

### 1. Streamlit Cloud Deployment

**Steps:**
1. Push code to GitHub repository
2. Connect repository to Streamlit Cloud
3. Configure secrets in Streamlit Cloud dashboard
4. Set Python version in `.python-version` file

**Secrets Configuration:**
```toml
# .streamlit/secrets.toml (Streamlit Cloud UI)
todoist_api_key = "xxx"
github_token = "xxx"

[gcp_service_account]
type = "service_account"
project_id = "xxx"
private_key_id = "xxx"
private_key = "xxx"
client_email = "xxx"
client_id = "xxx"
```

### 2. Local Development

```bash
# Setup script (setup.sh)
#!/bin/bash

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create local secrets file
mkdir -p .streamlit
cat > .streamlit/secrets.toml << 'EOL'
# Add your secrets here
todoist_api_key = ""
github_token = ""
EOL

# Run app
streamlit run app.py
```

---

## Testing Strategy

```python
# tests/test_fetchers.py
import pytest
from unittest.mock import Mock, patch
from fetchers.todoist_fetcher import TodoistFetcher

def test_todoist_fetcher_completed_tasks():
    """Test fetching completed tasks"""
    with patch('streamlit.secrets', {'todoist_api_key': 'test'}):
        fetcher = TodoistFetcher()
        # Mock API response
        with patch.object(fetcher.api, 'get_completed_items') as mock:
            mock.return_value = [...]
            tasks = fetcher.get_completed_this_week()
            assert len(tasks) > 0
```

---

## Security Considerations

1. **API Key Management**
   - Never commit secrets to Git
   - Use Streamlit secrets management
   - Implement key rotation reminders
   - Consider OAuth where possible

2. **Data Privacy**
   - Cache personal data locally only
   - Clear cache on logout
   - No persistent storage of sensitive data

3. **Rate Limiting**
   - Implement exponential backoff
   - Respect API rate limits
   - Use caching aggressively

---

## Future Enhancements

### Phase 1 (MVP)
- [ ] Basic Todoist integration
- [ ] Google Sheets integration
- [ ] Simple metric cards
- [ ] Manual refresh button

### Phase 2 
- [ ] GitHub integration
- [ ] Weather widget
- [ ] Interactive charts
- [ ] Auto-refresh
- [ ] Dark mode

### Phase 3
- [ ] Notion integration
- [ ] Calendar view
- [ ] Export functionality
- [ ] Mobile optimization
- [ ] Custom themes

### Phase 4
- [ ] AI insights (Claude API)
- [ ] Predictive metrics
- [ ] Goal tracking
- [ ] Webhook support

---

## Performance Optimization

1. **Caching**
   - Use `st.cache_data` for API calls
   - Implement tiered caching (memory → disk)
   - Cache invalidation strategies

2. **Lazy Loading**
   - Load panels on-demand
   - Paginate large datasets
   - Progressive enhancement

3. **Async Operations**
   - Use async/await for API calls
   - Parallel data fetching
   - Background refresh

---

## Monitoring & Logging

```python
# utils/logger.py
import logging
import streamlit as st

def setup_logger():
    """Configure application logger"""
    logger = logging.getLogger('life_dashboard')
    logger.setLevel(logging.INFO)
    
    # Console handler
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

# Use in fetchers
logger = setup_logger()
logger.info(f"Fetching Todoist tasks for user")
```

---

## Development Timeline

### Week 1: Foundation
- Set up repository and project structure
- Implement base fetcher class
- Create Todoist integration
- Basic panel rendering

### Week 2: Core Features  
- Google Sheets integration
- Caching system
- State management
- Basic UI layout

### Week 3: Polish
- Error handling
- Loading states
- Responsive design
- Deploy to Streamlit Cloud

### Week 4: Enhancement
- Additional integrations
- Charts and visualizations
- Settings persistence
- Documentation

---

## Success Metrics

1. **Technical**
   - Page load time < 2 seconds
   - API response caching working
   - Zero runtime errors

2. **Functional**
   - All panels updating correctly
   - Data freshness maintained
   - Mobile responsive

3. **User Experience**
   - Intuitive navigation
   - Customizable layout
   - Clear data visualization

---

## Dependencies Summary

### Critical Dependencies
- **Streamlit**: Core framework (version pinning important)
- **pandas**: Data manipulation 
- **todoist-api-python**: Official client preferred
- **gspread**: Most stable Google Sheets client

### API Requirements
- Todoist API key
- Google Cloud service account
- GitHub personal access token (optional)
- Weather API key (optional)

### Deployment Requirements
- GitHub repository
- Streamlit Cloud account (free)
- Python 3.9+

---

## Questions to Resolve

1. **Data Sources Priority**
   - Which integrations are must-have vs nice-to-have?
   - Any specific Google Sheets structure to follow?

2. **UI Preferences**
   - Dark mode important?
   - Mobile usage priority?
   - Preferred chart types?

3. **Refresh Strategy**
   - How fresh does data need to be?
   - Auto-refresh intervals?

4. **Privacy Concerns**
   - Any data that shouldn't be cached?
   - Need for authentication/multi-user support?