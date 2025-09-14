# AI LoL Commentator: Real-Time AI-Powered Esports Commentary for League of Legends

![League of Legends Commentary Demo](https://via.placeholder.com/800x400?text=AI+LoL+Commentator+Demo)  
*(Replace with an actual screenshot or GIF of the system in action, e.g., console output with commentary audio playing.)*

## Overview

Welcome to **AI LoL Commentator**, an innovative AI-driven system that transforms League of Legends (LoL) gameplay into an exciting, professional esports broadcast! Built for hackathons like this one, our tool uses real-time data from the LoL Client API (LCU) and Live Client API to detect game events—such as kills, turret destructions, dragon slays, and team fights—and generates dynamic, energetic commentary. 

The commentary is powered by Google's Gemini AI for natural language generation and ElevenLabs for high-quality text-to-speech (TTS) audio output. Imagine watching a spectator mode game with a live announcer hyping up every play, just like a real esports tournament. This project demonstrates how AI can enhance gaming experiences, making them more immersive and accessible for viewers, streamers, and casual players.

Our core idea: Leverage spectator mode in LoL to fetch live game data without interfering with gameplay. We poll the APIs for events, process them into contextual prompts, generate commentary, and convert it to spoken audio—all in real-time!

### Why This Matters
- **For Gamers & Streamers**: Adds professional flair to personal streams or replays.
- **For Esports**: Prototype for automated commentary in lower-tier tournaments or highlight reels.
- **Hackathon Innovation**: Combines API hacking, AI generation, and TTS in a seamless pipeline

## How It Works

The system operates in a continuous loop, monitoring the game's phase and events:

1. **Data Acquisition**:
   - Reads the LoL lockfile to authenticate and connect to the LCU API (for champ select and game flow) and Live Client API (for in-game events).
   - Polls for game phases: Lobby, Champ Select, In-Progress, etc.

2. **Event Detection**:
   - During Champ Select: Tracks team compositions and announces when ready.
   - In-Game: Fetches new events like GameStart, ChampionKill, TurretKilled, DragonKill, BaronKill, etc.
   - Maintains a stateful context (e.g., seen events) to avoid duplicates and build narrative continuity.

3. **AI Commentary Generation**:
   - Uses Gemini AI with a custom system prompt to act as an "energetic esports commentator."
   - First run: Plays a hardcoded welcome message.
   - Subsequent: Builds a chat history for contextual, flowing commentary (e.g., "Blue team just secured the Ocean Dragon at 12:45— that's a massive regen boost!").
   - Keeps responses concise, exciting, and focused on key events.

4. **Audio Output**:
   - Converts generated text to speech using ElevenLabs API (with a chosen voice and model for fast, natural-sounding audio).
   - Saves as MP3 and plays it immediately for real-time narration.

5. **Loop & Polling**:
   - Runs every few seconds (configurable via `POLL_INTERVAL`) to ensure low-latency updates without overwhelming the system.

The code is structured modularly in `Hack.ipynb` (or equivalent script), with functions for API requests, event processing, AI calls, and TTS.

### Example Commentary Flow
- **Game Start**: "Welcome, ladies and gentlemen, to the ultimate battleground..."
- **Kill Event**: "[03:45] Draven killed Lux – Oh snap! Draven axes down Lux in a brutal bot lane skirmish. That's first blood for red team!"
- **Objective**: "[15:20] Team Blue slays the Infernal Dragon – Flames are flying! Blue team powers up with that Infernal buff—watch out for those spicy team fights ahead!"


## Features

- **Real-Time Event Tracking**: Detects and narrates key LoL events like kills, objectives, and game starts.
- **Direct LCU & Client API Access**: Pulls live game data straight from the League client in spectator mode, ensuring **fast, low-latency updates** without relying on external scraping or slow endpoints.
- **Contextual AI Narration**: Maintains chat history for coherent, story-like commentary.
- **High-Quality TTS**: Uses ElevenLabs for expressive, low-latency audio.
- **Spectator-Friendly**: Works entirely in spectator mode—no impact on active players.
- **Extensible**: Easy to add more event types or integrate with streaming tools (e.g., OBS).






## Technologies Used

- **Programming**: Python 3.x
- **APIs**:
  - League of Legends Client API (LCU) & Live Client API for game data.
  - Google Gemini API for AI-generated commentary.
  - ElevenLabs API for TTS.
- **Libraries**:
  - `requests` for HTTP calls.
  - `time`, `uuid`, `os` for utilities.
- **Environment**: Runs locally with LoL client open in spectator mode.
- **No External Dependencies Beyond Basics**: Keeps it lightweight for hackathon demos.

## Setup & Installation

### Prerequisites
- League of Legends client installed and running in spectator mode.
- API Keys:
  - Google Gemini API key (set as `gemini_api_url` in code).
  - ElevenLabs API key (set as `ELEVENLABS_API_KEY`).
- Python packages: Install via `pip install requests elevenlabs` (assuming ElevenLabs SDK).

### Steps
1. Clone the repo:
   ```
   git clone https://github.com/yourusername/ai-lol-commentator.git
   cd ai-lol-commentator
   ```
2. Set environment variables or update code with your API keys.
3. Ensure LoL is running and in spectator mode for a game.
4. Run the script:
   ```
   python hack.py  # Or open Hack.ipynb in Jupyter
   ```
   - The system will start polling and narrating!

**Note**: Disable SSL verification if needed (as in code: `verify=False`). For production, use proper certs.

## Usage

- Launch LoL, enter spectator mode for a match.
- Run the main loop: `main_loop()`.
- Listen to the audio commentary play automatically as events unfold.
- Customize: Adjust `POLL_INTERVAL` for faster/slower polling, or tweak the system prompt for different commentator styles (e.g., humorous or analytical).

### Demo Video
*(Embed or link to a short YouTube/Loom video showing the system narrating a sample game. E.g.,)  
[![Demo Video](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)*

## Limitations & Future Improvements
- **Current Scope**: Focuses on core events; could expand to item builds, gold leads, or player stats.
- **Latency**: Dependent on API polling—future: WebSocket integration for true real-time.
- **Multi-Game Support**: Currently single-game; scale to multiple spectators.
- **Enhancements**: Integrate with Twitch/OBS for overlays, or add multi-language support.

## Contributors
- **You**: API integration, event processing, and main loop.
- **Your Friend**: AI pipeline, TTS integration, and commentary generation.

## License
MIT License – Feel free to fork and build upon!