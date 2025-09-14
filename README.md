https://drive.google.com/file/d/1QPj9sGfpCQqWtEf9Jb7zkqMZNCCmcqiW/view?usp=drive_link

# 🎙️ AI LoL Commentator

**Real-Time AI-Powered Esports Commentary for League of Legends**

---

## Overview

Welcome to **AI LoL Commentator**, an innovative, AI-driven system that transforms ordinary **League of Legends (LoL)** gameplay into a dynamic, professional esports broadcast. This tool uses real-time data from the **LoL Client** and **Live Client APIs** to detect critical in-game events—such as kills, turret takedowns, and objectives—and generates energetic, exciting commentary on the fly.  

Powered by **Google's Gemini AI** for natural language generation and **ElevenLabs** for high-fidelity text-to-speech (TTS), our system provides an immersive, audio-enhanced viewing experience. This project demonstrates a seamless pipeline for live, AI-powered narration, making it an ideal showcase for hackathon innovation.

---

## Why This Matters

- **For Viewers & Streamers:** Adds a professional, engaging audio layer to streams and replays, elevating the viewer experience.  
- **For Esports:** Serves as a prototype for automated commentary, scalable for lower-tier tournaments or dynamic highlight reel creation.  
- **For AI Enthusiasts:** Combines API interaction, real-time event processing, and advanced LLM/TTS technologies into a functional, end-to-end application.

---

## How It Works: The AI-Driven Commentary Pipeline

The system operates in a continuous, low-latency loop, monitoring the game state and narrating key moments:

1. **Data Acquisition**  
   - Reads the LoL lockfile to securely connect to the local APIs.  
   - Polls the **League of Legends Client API (LCU)** and **Live Client API** to fetch real-time game data, including player information and in-game events.  

2. **Event Detection**  
   The script actively listens for new events as they happen, such as:  
   - **Game Start:** `"Welcome, everyone, to the ultimate battleground!"`  
   - **Champion Kills:** `"Oh, what a play! {KillerName} just took down {VictimName}!"`  
   - **Objective Takes:** `"The Infernal Dragon has fallen to Team Blue, and the power of the flame is now with them!"`  
   - **Player Stats Updates:** When no new events are detected, the system provides an update on a specific player's stats to maintain a continuous narrative flow.  

3. **AI Commentary Generation**  
   - Game events and contextual player data are fed into the **Gemini AI**.  
   - The model, acting as a professional esports commentator, generates concise and impactful commentary.  

4. **Audio Output**  
   - The generated text is instantly sent to the **ElevenLabs API** for conversion into high-quality audio.  
   - Audio is played directly through your system’s speakers, providing a truly live commentary experience.

---

## Key Features

- **Real-Time Event Tracking:** Captures and narrates key moments like kills, objectives, and game starts as they happen.  
- **Direct API Integration:** Utilizes official LoL APIs for a fast, low-latency data stream without external scraping.  
- **Contextual & Dynamic AI:** Gemini model ensures commentary is coherent and follows the game's evolving story.  
- **High-Fidelity Audio:** ElevenLabs provides expressive, low-latency voice output for a professional feel.  
- **Spectator-Friendly:** Operates non-intrusively in spectator mode, requiring no changes to the live game environment.  
- **User-Friendly Setup:** `ui.py` guides you through setup and automatically creates your `.env` file.  

---

## Technologies Used

- **Programming Language:** Python 3.x  
- **APIs:** League of Legends Client API (LCU), Live Client API, Google Gemini AI, ElevenLabs API  
- **Libraries:** All dependencies listed in `requirements.txt`  

---

## Setup & Installation

### Prerequisites

- **League of Legends client installed** and running a game in **spectator mode** (required for API access).

### Steps

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/ai-lol-commentator.git
   cd ai-lol-commentator
