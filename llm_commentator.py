import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_LLM_MODEL

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