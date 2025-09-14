import os
import time
import requests
import uuid
from requests.auth import HTTPBasicAuth
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
from IPython.display import Audio, display
import pygame
from mutagen.mp3 import MP3
import google.generativeai as genai
import warnings
warnings.filterwarnings("ignore")

# --- Environment Variable Loading ---
# This section loads API keys and configuration settings from a .env file.
# This keeps sensitive information separate from the code.
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")
GEMINI_LLM_MODEL = os.getenv("GEMINI_LLM_MODEL")
LOL_LOCKFILE_PATH = os.getenv("LOL_LOCKFILE_PATH")
POLL_INTERVAL = os.getenv("POLL_INTERVAL")

# --- LCU (League Client Update) API Communication ---
def read_lockfile(path=LOL_LOCKFILE_PATH):
    """
    Reads the lockfile created by the League Client to get the port and
    authentication password for the LCU API.
    """
    with open(path, "r") as f:
        name, pid, port, password, protocol = f.read().split(":")
    return port, password

# Read the lockfile to get connection details
port, password = read_lockfile()
lcu_auth = HTTPBasicAuth("riot", password)

def lcu_request(endpoint):
    """Generic GET request to the LCU API."""
    lcu_url = f"https://127.0.0.1:{port}{endpoint}"
    # The 'verify=False' flag is necessary because the LCU API uses a self-signed certificate.
    resp = requests.get(lcu_url, auth=lcu_auth, verify=False)
    return resp.json()

# --- Live Client API Communication ---
def live_request(endpoint):
    """Generic GET request to the Live Client API."""
    # The Live Client API uses a fixed port (2999) and no authentication.
    url = f"https://127.0.0.1:2999{endpoint}"
    resp = requests.get(url, verify=False)
    return resp.json()

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

# --- AI Commentator Class (Gemini) ---
class LeagueCommentator:
    """Handles communication with the Gemini LLM for generating commentary."""
    def __init__(self):
        # Configure the Gemini API with the provided key.
        genai.configure(api_key=GEMINI_API_KEY)
        # Define the personality and role of the commentator.
        self.system_prompt = """
            You are a professional League of Legends esports commentator. 
            Your job is to provide an exciting and engaging play-by-play commentary.
            Use a vibrant and energetic tone. Focus on the most important events like kills, objectives taken (Dragons, Barons, Towers), and teamfights.
            Keep your commentary concise and impactful. Do not state that you are an AI model.
            Don't use any special caracters like *
        """
        # Initialize the model with the specified system prompt.
        self.model = genai.GenerativeModel(
            model_name=GEMINI_LLM_MODEL,
            system_instruction=self.system_prompt
        )
        # Start a chat session to maintain conversation history.
        self.chat = self.model.start_chat()

    def get_caption_from_gemini(self, event_or_context_text):
        """
        Sends event or context text to the Gemini model to get commentary.
        """
        user_prompt = f"The following events just happened in the game:\n{event_or_context_text}\n\nProvide commentary based only on the major events, make it brief."
        try:
            # Send the user message to the chat session
            response = self.chat.send_message(user_prompt)
            return response.text
        except Exception as e:
            print(f"API call failed: {e}")
            return "Our commentator seems to be having a technical issue. Please stand by."

# --- Audio Generation and Playback (ElevenLabs) ---
# Initialize the ElevenLabs client if API keys are available.
if ELEVENLABS_API_KEY and VOICE_ID:
    elevenlabs_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
else:
    print("Warning: ElevenLabs API key or voice ID not found. Audio generation will be skipped.")

def get_audio_from_elevenlabs(text_to_speak):
    """
    Generates audio from text, saves it as an MP3, plays it, and cleans up the file.
    """
    if not ELEVENLABS_API_KEY or not VOICE_ID:
        return

    try:
        # Generate audio from the provided text.
        audio = elevenlabs_client.text_to_speech.convert(
            text=text_to_speak,
            voice_id=VOICE_ID,
            model_id="eleven_flash_v2",
            output_format="mp3_44100_128",
        )
        
        # Save the audio stream to a temporary file.
        filename = str(uuid.uuid4())
        save_file_path = f"{filename}.mp3"

        with open(save_file_path, "wb") as f:
            for chunk in audio:
                if chunk:
                    f.write(chunk)
        
        # Get the audio duration to know how long to sleep.
        audio_file = MP3(save_file_path)
        audio_duration = audio_file.info.length

        # Initialize the pygame mixer for playback.
        pygame.mixer.init()
        pygame.mixer.music.load(save_file_path)
        pygame.mixer.music.play()

        # Wait for the audio to finish playing.
        if audio_duration > 0:
            time.sleep(audio_duration)

        # Stop the mixer and delete the temporary file.
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        os.remove(save_file_path)
        
    except Exception as e:
        print(f"Error during audio generation or playback: {e}")

# --- Game Context Management ---
class LoLContext:
    """Stores and manages game state information, such as events and player data."""
    def __init__(self):
        # A set to track seen event IDs to prevent duplicate commentary.
        self.seen_event_ids = set()
        self.champ_select_done = False
        self.players_info = []
        self.teams_info = {}
    
    def update_champ_select(self):
        """Updates the stored player and team info after champion select."""
        try:
            session = get_champselect_session()
            self.players_info = session.get("myTeam", [])
            self.teams_info = {
                "myTeam": session.get("myTeam", []),
                "theirTeam": session.get("theirTeam", [])
            }
            if self.players_info:
                self.champ_select_done = True
        except:
            pass

    def get_new_events(self):
        """Fetches and returns only the new events that haven't been seen yet."""
        events = []
        try:
            all_events = get_event_data().get("Events", [])
            for e in all_events:
                if e["EventID"] not in self.seen_event_ids:
                    self.seen_event_ids.add(e["EventID"])
                    events.append(e)
        except:
            pass
        return events

# --- Event to Text Conversion ---
def event_to_text(event):
    """Converts a raw game event object into a human-readable text string."""
    etype = event["EventName"]
    t = int(event.get("EventTime",0))
    mm, ss = divmod(t, 60)

    if etype == "GameStart":
        desc = "The game has started!"
    elif etype == "MinionsSpawning":
        desc = "Minions have spawned."
    elif etype == "ChampionKill":
        desc = f'{event.get("KillerName","?")} killed {event.get("VictimName","?")}'
    elif etype == "TurretKilled":
        desc = f'{event.get("KillerName","?")} destroyed {event.get("TurretKilled","a turret")}'
    elif etype == "DragonKill":
        desc = f'{event.get("KillerName","?")} killed a {event.get("DragonType","dragon")} dragon'
    elif etype == "BaronKill":
        desc = f'{event.get("KillerName","?")} killed Baron Nashor'
    else:
        desc = etype

    return f"[{mm:02d}:{ss:02d}] {desc}"

# --- Data Processing Functions (from previous responses) ---
def process_player_data(player_data):
    """
    Extracts and formats relevant player data for LLM commentary.
    """
    if not isinstance(player_data, list) or not player_data:
        return ""

    commentary_string = ""
    for player in player_data:
        champion_name = player.get('championName', 'Unknown Champion')
        summoner_name = player.get('summonerName', 'Unknown Summoner')
        team = player.get('team', 'Unknown Team')
        position = player.get('position', 'NONE')
        level = player.get('level', 0)
        
        scores = player.get('scores', {})
        kills = scores.get('kills', 0)
        deaths = scores.get('deaths', 0)
        assists = scores.get('assists', 0)

        runes = player.get('runes', {})
        keystone_rune = runes.get('keystone', {}).get('displayName', 'Unknown Keystone')
        primary_tree = runes.get('primaryRuneTree', {}).get('displayName', 'Unknown Rune Tree')
        
        spells = player.get('summonerSpells', {})
        spell_one = spells.get('summonerSpellOne', {}).get('displayName', 'Unknown Spell')
        spell_two = spells.get('summonerSpellTwo', {}).get('displayName', 'Unknown Spell')

        player_summary = (
            f"Player: {summoner_name} ({champion_name}) on team {team}.\n"
            f"Role: {position}.\n"
            f"Scores: {kills}/{deaths}/{assists}, Level: {level}.\n"
            f"Keystone Rune: {keystone_rune} ({primary_tree} tree).\n"
            f"Summoner Spells: {spell_one} and {spell_two}.\n\n"
        )
        
        commentary_string += player_summary

    return commentary_string

def process_active_player_data(active_player_data):
    """
    Extracts and formats relevant active player data for LLM commentary.
    """
    if not isinstance(active_player_data, dict) or not active_player_data:
        return ""

    summoner_name = active_player_data.get('summonerName', 'Unknown Summoner')
    champion_stats = active_player_data.get('championStats', {})
    level = active_player_data.get('level', 0)
    current_gold = active_player_data.get('currentGold', 0)

    current_health = champion_stats.get('currentHealth', 0)
    max_health = champion_stats.get('maxHealth', 0)
    attack_damage = champion_stats.get('attackDamage', 0)
    ability_power = champion_stats.get('abilityPower', 0)
    armor = champion_stats.get('armor', 0)
    magic_resist = champion_stats.get('magicResist', 0)
    move_speed = champion_stats.get('moveSpeed', 0)
    
    full_runes = active_player_data.get('fullRunes', {})
    keystone_rune = full_runes.get('keystone', {}).get('displayName', 'Unknown Keystone')
    primary_tree = full_runes.get('primaryRuneTree', {}).get('displayName', 'Unknown Rune Tree')
    
    abilities = active_player_data.get('abilities', {})
    q_ability = abilities.get('Q', {}).get('displayName', 'Q Ability')
    w_ability = abilities.get('W', {}).get('displayName', 'W Ability')
    e_ability = abilities.get('E', {}).get('displayName', 'E Ability')
    r_ability = abilities.get('R', {}).get('displayName', 'R Ability')

    player_summary = (
        f"Active Player: {summoner_name} (Level {level})\n"
        f"Health: {current_health:.1f}/{max_health:.1f}\n"
        f"Gold: {current_gold:.1f}\n"
        f"Stats:\n"
        f" - AD: {attack_damage:.1f}, AP: {ability_power:.1f}\n"
        f" - Armor: {armor:.1f}, Magic Resist: {magic_resist:.1f}\n"
        f" - Move Speed: {move_speed:.1f}\n"
        f"Runes: {keystone_rune} ({primary_tree} tree)\n"
        f"Abilities:\n"
        f" - Q: {q_ability}\n"
        f" - W: {w_ability}\n"
        f" - E: {e_ability}\n"
        f" - R: {r_ability}\n"
    )
    return player_summary

# --- Main Program Loop ---
def main_loop():
    """
    The main control loop that fetches game data and provides commentary.
    """
    is_first_run = True
    ctx = LoLContext()
    # Instantiate the LeagueCommentator to handle all LLM interactions.
    lolCommentator = LeagueCommentator()
    while True:
        # Handle the initial welcome message on the first run.
        if is_first_run:
            is_first_run = False
            intro = "Welcome, everyone, to the ultimate battleground where legends are made! I'm your host, bringing you the fastest plays and sharpest calls from today's high-stakes tournament. Get ready for insane strategies and jaw-dropping action as our top contenders prove they're the best in the game."
            print(intro)
            get_audio_from_elevenlabs(intro)
        
        # Get the current game phase.
        phase = get_gameflow_phase()
        
        # 1. Pregame: Champion Select
        if phase in ["Lobby", "Matchmaking", "ChampSelect"] and not ctx.champ_select_done:
            ctx.update_champ_select()
            if ctx.champ_select_done:
                text = "Champ select is done. Teams and bans are set."
                caption = lolCommentator.get_caption_from_gemini(text)
                print(caption)
                get_audio_from_elevenlabs(caption)
        
        # 2. In-game: Fetching Events and Player Data
        if phase == "InProgress":
            context = ""
            new_events = ctx.get_new_events()
            
            # If there are new major events, generate commentary on them.
            if new_events:
                for e in new_events:
                    text = event_to_text(e)
                    context = context + text + "\n"
                
                caption = lolCommentator.get_caption_from_gemini(context)
                print(caption)
                get_audio_from_elevenlabs(caption)
            
            # If there are no new events, provide a general update based on player data.
            else: 
                # Fetch player data and active player stats.
                commentary_string_from_player_list = process_player_data(get_player_list())
                commentary_string_from_active_data = process_active_player_data(get_active_player())
                
                # Combine the data and send it to the LLM for general commentary.
                caption = lolCommentator.get_caption_from_gemini(commentary_string_from_player_list + "\n" + commentary_string_from_active_data)
                print(caption)
                get_audio_from_elevenlabs(caption)
        
        # Wait for the next poll interval.
        # time.sleep(int(POLL_INTERVAL))

# --- Program Entry Point ---
if __name__ == '__main__':
    print("🚀 Starting AI commentator...")
    main_loop()
