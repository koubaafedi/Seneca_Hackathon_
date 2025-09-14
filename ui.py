import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
import subprocess
import threading
import logging

# Set up logging for debugging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Set CustomTkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

def load_env():
    """Load existing .env file values into the entry fields."""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    logging.debug(f"Checking for .env file at: {env_path}")
    if os.path.exists(env_path):
        with open(env_path, 'r') as env_file:
            content = env_file.read()
            logging.debug(f"Loaded .env content:\n{content}")
            for line in content.splitlines():
                if '=' in line:
                    key, value = line.strip().split('=', 1)
                    if key == 'GEMINI_API_KEY':
                        entry_gemini_api_key.delete(0, ctk.END)
                        entry_gemini_api_key.insert(0, value)
                    elif key == 'GEMINI_LLM_MODEL':
                        entry_gemini_llm_model.delete(0, ctk.END)
                        entry_gemini_llm_model.insert(0, value)
                    elif key == 'ELEVENLABS_API_KEY':
                        entry_elevenlabs_api_key.delete(0, ctk.END)
                        entry_elevenlabs_api_key.insert(0, value)
                    elif key == 'LOL_LOCKFILE_PATH':
                        entry_lol_lockfile_path.delete(0, ctk.END)
                        entry_lol_lockfile_path.insert(0, value.strip('"'))
    else:
        logging.debug("No .env file found")

def browse_lockfile():
    """Open a file dialog to select the League lockfile."""
    file_path = filedialog.askopenfilename(
        title="Select League of Legends Lockfile",
        filetypes=[("Lockfile", "lockfile")]
    )
    if file_path:
        entry_lol_lockfile_path.delete(0, ctk.END)
        entry_lol_lockfile_path.insert(0, file_path)

def toggle_api_key_visibility(entry, button):
    """Toggle visibility of API key in the entry field."""
    current_show = entry.cget("show")
    entry.configure(show="" if current_show == "*" else "*")
    button.configure(text="Hide" if current_show == "*" else "Show")

def write_env_and_run():
    """Write .env file and run main.py in a separate thread to keep UI responsive."""
    # Collect values
    gemini_api_key = entry_gemini_api_key.get()
    gemini_llm_model = entry_gemini_llm_model.get()
    elevenlabs_api_key = entry_elevenlabs_api_key.get()
    lol_lockfile_path = entry_lol_lockfile_path.get()

    # Validate required fields
    if not all([gemini_api_key, gemini_llm_model, elevenlabs_api_key, lol_lockfile_path]):
        messagebox.showerror("Error", "Please fill in all required fields.")
        logging.error("Validation failed: Missing required fields")
        return

    # Define .env file path
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    logging.debug(f"Writing .env file to: {env_path}")

    # Write to .env file
    env_content = f"""GEMINI_API_KEY={gemini_api_key}
GEMINI_LLM_MODEL={gemini_llm_model}
ELEVENLABS_API_KEY={elevenlabs_api_key}
LOL_LOCKFILE_PATH="{lol_lockfile_path}"
VOICE_ID=zGDcfWXcfXiClzqvQasP
"""
    logging.debug(f".env content to write:\n{env_content}")

    # Disable button and show loading
    run_button.configure(state="disabled", text="Launching...")
    progress_bar.start()
    output_text.delete("1.0", ctk.END)  # Clear previous output

    def run_task():
        try:
            # Check write permissions
            if not os.access(os.path.dirname(env_path), os.W_OK):
                logging.error(f"No write permission for directory: {os.path.dirname(env_path)}")
                messagebox.showerror("Error", f"No write permission for directory: {os.path.dirname(env_path)}")
                return

            # Write .env file
            with open(env_path, 'w') as env_file:
                env_file.write(env_content)
            
            # Verify file was written
            if os.path.exists(env_path):
                with open(env_path, 'r') as env_file:
                    written_content = env_file.read()
                logging.debug(f".env file written successfully at: {env_path}\nContent:\n{written_content}")
                root.after(0, lambda: output_text.insert("1.0", f".env file written at: {env_path}\nContent:\n{written_content}"))
                messagebox.showinfo("Success", f".env file written successfully at {env_path}!")
            else:
                logging.error("Failed to confirm .env file creation")
                messagebox.showerror("Error", "Failed to confirm .env file creation.")
                return

            # Execute main.py
            try:
                main_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'main.py')
                logging.debug(f"Executing main.py at: {main_path}")
                subprocess.run(["python", main_path], check=True)
                root.after(0, lambda: output_text.insert(ctk.END, "\nmain.py executed successfully!"))
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to run main.py: {str(e)}")
                messagebox.showerror("Error", f"Failed to run main.py: {str(e)}")
            except FileNotFoundError:
                logging.error("main.py not found in the current directory")
                messagebox.showerror("Error", "main.py not found in the current directory.")
        except Exception as e:
            logging.error(f"Failed to write .env file: {str(e)}")
            messagebox.showerror("Error", f"Failed to write .env file: {str(e)}")
        finally:
            # Re-enable button and stop loading
            root.after(0, lambda: run_button.configure(state="normal", text="Launch System"))
            root.after(0, lambda: progress_bar.stop())
            root.after(0, lambda: progress_bar.set(0))

    # Run in a separate thread to avoid freezing the UI
    threading.Thread(target=run_task, daemon=True).start()

# Create the main window
root = ctk.CTk()
root.title("LoL AI Commentator Setup - Hyprland Edition")
root.geometry("900x700")
root.resizable(False, False)
root.attributes('-alpha', 0.95)

# Fonts and colors
title_font = ("Courier New", 28, "bold")
label_font = ("Courier New", 14)
entry_font = ("Courier New", 14)
button_font = ("Courier New", 16, "bold")
bg_color = "#0a0a0a"
fg_color = "#00ff99"
entry_bg = "#1e1e1e"
button_bg = "#004d40"
button_active_bg = "#00ff99"
accent_color = "#00ff99"

# Main frame with subtle border
main_frame = ctk.CTkFrame(root, fg_color=bg_color, corner_radius=10, border_width=2, border_color=accent_color)
main_frame.pack(expand=True, fill="both", padx=60, pady=60)

# Title with glow effect
title_label = ctk.CTkLabel(
    main_frame,
    text="LoL AI Commentator Setup",
    font=title_font,
    text_color=accent_color,
)
title_label.pack(pady=20)

# Subtitle
ctk.CTkLabel(
    main_frame,
    text="Power your AI-driven League commentary with a futuristic Hyprland-inspired interface",
    font=("Courier New", 12),
    text_color="#ffffff",
    wraplength=600
).pack(pady=10)

# Form frame
form_frame = ctk.CTkFrame(main_frame, fg_color=bg_color)
form_frame.pack(pady=20, fill="x", padx=20)

# Labels and Entries with animations
for i, (label_text, entry_var, default_value, show) in enumerate([
    ("Gemini API Key:", "entry_gemini_api_key", None, "*"),
    ("Gemini LLM Model:", "entry_gemini_llm_model", "gemini-2.5-flash-lite", ""),
    ("ElevenLabs API Key:", "entry_elevenlabs_api_key", None, "*"),
    ("LoL Lockfile Path:", "entry_lol_lockfile_path", "D:/Riot Games/League of Legends/lockfile", ""),
]):
    ctk.CTkLabel(form_frame, text=label_text, font=label_font, text_color=fg_color).grid(row=i, column=0, padx=10, pady=10, sticky="e")
    
    entry = ctk.CTkEntry(
        form_frame,
        font=entry_font,
        text_color=fg_color,
        fg_color=entry_bg,
        border_color=accent_color,
        border_width=2,
        width=400,
        show=show,
        corner_radius=8
    )
    entry.grid(row=i, column=1, padx=10, pady=10)
    if default_value:
        entry.insert(0, default_value)
    globals()[entry_var] = entry

    # Add show/hide button for API keys
    if show == "*":
        toggle_button = ctk.CTkButton(
            form_frame,
            text="Show",
            font=label_font,
            width=80,
            fg_color=button_bg,
            hover_color=button_active_bg,
            command=lambda e=entry: toggle_api_key_visibility(e, toggle_button)
        )
        toggle_button.grid(row=i, column=2, padx=5, pady=10)

# File picker button for lockfile
browse_button = ctk.CTkButton(
    form_frame,
    text="Browse",
    font=label_font,
    width=80,
    fg_color=button_bg,
    hover_color=button_active_bg,
    command=browse_lockfile
)
browse_button.grid(row=3, column=2, padx=5, pady=10)

# Output text box for verification
output_text = ctk.CTkTextbox(
    main_frame,
    font=("Courier New", 12),
    text_color=fg_color,
    fg_color=entry_bg,
    height=100,
    wrap="word",
    state="disabled"
)
output_text.pack(pady=10, fill="x", padx=20)

# Progress bar for launching
progress_bar = ctk.CTkProgressBar(main_frame, mode="indeterminate", width=300, fg_color=entry_bg, progress_color=accent_color)
progress_bar.pack(pady=10)
progress_bar.set(0)

# Run button with animation
run_button = ctk.CTkButton(
    main_frame,
    text="Launch System",
    font=button_font,
    fg_color=button_bg,
    hover_color=button_active_bg,
    text_color=fg_color,
    command=write_env_and_run,
    width=200,
    height=50,
    corner_radius=10
)
run_button.pack(pady=30)

# Keyboard binding for Enter key
root.bind('<Return>', lambda e: write_env_and_run())

# Load existing .env
load_env()

# Start the GUI loop
root.mainloop()