https://drive.google.com/file/d/1QPj9sGfpCQqWtEf9Jb7zkqMZNCCmcqiW/view?usp=drive_link

# 🎙️ AI LoL Commentator: Real-Time AI-Powered Esports Commentary for League of Legends

Welcome to **AI LoL Commentator**, an innovative, AI-driven system that transforms ordinary League of Legends (LoL) gameplay into a dynamic, professional esports broadcast. This tool uses real-time data from the LoL Client and Live Client APIs to detect critical in-game events—such as kills, turret takedowns, and objectives—and generates energetic, exciting commentary on the fly.

Powered by Google's **Gemini AI** for natural language generation and **ElevenLabs** for high-fidelity text-to-speech (TTS), our system provides an immersive, audio-enhanced viewing experience.

### Why This Matters

* **For Viewers & Streamers:** Adds a professional, engaging audio layer to streams and replays, elevating the viewer experience.
* **For Esports:** Serves as a prototype for automated commentary, scalable for lower-tier tournaments or dynamic highlight reel creation.
* **For AI Enthusiasts:** Combines API interaction, real-time event processing, and advanced LLM/TTS technologies into a functional, end-to-end application.

---

### How It Works: The AI-Driven Commentary Pipeline

The system operates in a continuous, low-latency loop, monitoring the game state and narrating key moments.

1.  **Data Acquisition:** The program reads the LoL lockfile to securely connect to the local APIs. It then polls the League of Legends Client API (LCU) and Live Client API to fetch real-time game data, including player information and in-game events.
2.  **Event Detection:** The script actively listens for new events as they happen, such as:
    * Game Start: "Welcome, everyone, to the ultimate battleground!"
    * Champion Kills: "Oh, what a play! {KillerName} just took down {VictimName}!"
    * Objective Takes: "The Infernal Dragon has fallen to Team Blue, and the power of the flame is now with them!"
3.  **AI Commentary Generation:** Game events and contextual player data are fed into the **Gemini AI**. The model, acting as a professional esports commentator, generates concise and impactful commentary.
4.  **Audio Output:** The generated text is instantly sent to the **ElevenLabs API** for conversion into a high-quality audio file. This audio is then played directly through your system's speakers, providing a truly live commentary experience. 

---

### Key Features

* **Real-Time Event Tracking:** Captures and narrates key moments like kills, objectives, and game starts as they happen.
* **Direct API Integration:** Utilizes the official LoL APIs for a fast, low-latency data stream without external scraping.
* **Contextual & Dynamic AI:** The Gemini model's chat history ensures that commentary is coherent and follows the game's evolving story.
* **High-Fidelity Audio:** ElevenLabs provides expressive, low-latency voice output for a professional feel.
* **Spectator-Friendly:** Operates non-intrusively in spectator mode, requiring no changes to the live game environment.
* **User-Friendly Setup:** A dedicated `ui.py` script guides you through the setup process and automatically creates the necessary `.env` file.

---

### Technologies Used

* **Programming Language:** Python 3.x
* **APIs:**
    * League of Legends Client API (LCU) & Live Client API
    * Google Gemini API
    * ElevenLabs API
* **Libraries:** All required libraries are listed in `requirements.txt`.

---

### Setup & Installation

#### Prerequisites

* The League of Legends client installed and running a game in spectator mode. This is a mandatory step, as the app requires access to the game's lockfile.

#### Steps

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/ai-lol-commentator.git](https://github.com/yourusername/ai-lol-commentator.git)
    cd ai-lol-commentator
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the setup script:**
    This will prompt you for your API keys and automatically create your `.env` file for you.
    ```bash
    python ui.py
    ```
4.  **Run the main application:**
    With the LoL client open in spectator mode, run the main script to start the commentator.
    ```bash
    python main.py
    ```

---

### Limitations & Future Improvements

* **Latency:** Commentary is dependent on the API polling interval. A future improvement would be to integrate with a WebSocket-based system for true real-time event pushing.
* **Deeper Context:** The current system focuses on major events. Future versions could integrate more nuanced data, such as item builds, gold leads, and player positions, for richer, more strategic commentary.
* **Scalability:** The current implementation is designed for a single spectator instance. Scaling to support multiple concurrent games would require a more robust backend architecture.

---

### License

This project is licensed under the MIT License.

### Steps

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/ai-lol-commentator.git
   cd ai-lol-commentator
