from data_fetcher import get_champselect_session, get_event_data

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