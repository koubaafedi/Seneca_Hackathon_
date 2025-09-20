from api_client import lcu_request, live_request

# --- Data Fetching Functions ---
# These functions wrap the generic request functions to fetch specific game data.
def get_current_summoner():
    """Fetches the current summoner's data from the LCU API."""
    return lcu_request("/lol-summoner/v1/current-summoner")

def get_gameflow_phase():
    """Fetches the current phase of the game (e.g., 'ChampSelect', 'InProgress')."""
    return lcu_request("/lol-gameflow/v1/gameflow-phase")

def get_champselect_session():
    """Fetches champion select session details."""
    return lcu_request("/lol-champ-select/v1/session")

def get_active_player():
    """Fetches detailed stats for the player currently being observed."""
    return live_request("/liveclientdata/activeplayer")

def get_player_list():
    """Fetches a list of all players in the game with basic stats."""
    return live_request("/liveclientdata/playerlist")

def get_game_stats():
    """Fetches general game statistics."""
    return live_request("/liveclientdata/gamestats")

def get_event_data():
    """Fetches a list of all in-game events (kills, objectives, etc.)."""
    return live_request("/liveclientdata/eventdata")