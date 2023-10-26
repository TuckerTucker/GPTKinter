#----- Main Imports
from tkinter import *
import openai

#----- Getting API key from .env
from dotenv import load_dotenv
import os

load_dotenv() # Load environment variables from .env file
openai_api_key = os.getenv("OPENAI_API_KEY") # Get the API key

#----- Declare the GUI
root = Tk()
root.title("GPTKinter")
root.geometry("800x600")

# Rows and Columns
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

# Colours
BG_GRAY = "#303030"
BG_COLOR = "#444444"
TEXT_COLOR = "#ffffff"

# Fonts
FONT = "Helvetica 24"


#----- Send function
def send():
    user_input = e.get("1.0", 'end-1c')  # Get text from Text widget
    send = "You -> " + user_input
    txt.insert(END, "\n" + send)

    # Clear the Text widget
    e.delete("1.0", END)

    # Display "Bot -> Thinking..."
    txt.insert(END, "\n" + "Bot -> Thinking...")
    thinking_index_start = txt.index("end-1c linestart")
    thinking_index_end = txt.index("end-1c")

    # Flush the Tkinter display to show "Thinking..." before making the API call
    root.update_idletasks()

    # Call OpenAI
    openai.api_key = openai_api_key
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"{user_input}"},
        ]
    )

    bot_output = response.choices[0].message.content.strip() + "\n\n"

    # Delete the "Bot -> Thinking..." message
    txt.delete(thinking_index_start, thinking_index_end)

    # Insert the actual bot response
    txt.insert(thinking_index_start, "Bot -> " + bot_output)

#----- The main Chatbox
txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
txt.grid(row=1, column=0, columnspan=2, sticky="nsew")

#----- The input field
e = Text(root, bg="#4f4f4f", fg=TEXT_COLOR, font=FONT, width=80, height=5)
e.grid(row=2, column=0, sticky="nsew", padx=(10, 10), pady=(10, 15))

#----- The Send Button
# Bind the Return key to the send function
e.bind("<Return>", lambda event: (send(), "break") if not event.state & 1 else None)
send_button = Button(root, text="Send", font=FONT, bg=BG_GRAY, command=send)
send_button.grid(row=2, column=1, padx=(0,15))

#----- Initiate The Main Loop
root.mainloop()