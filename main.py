from data_fetcher import get_gameflow_phase, get_player_list, get_active_player
from llm_commentator import LeagueCommentator
from audio_player import get_audio_from_elevenlabs
from utils import LoLContext, event_to_text, process_player_data, process_active_player_data

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