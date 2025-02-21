import tkinter as tk
from tkinter import scrolledtext
from functions import chat_bot

class ChatbotUI(tk.Tk):
    def __init__(self, document_path):
        super().__init__()
        self.title("Chatbot UI")
        self.geometry("600x700")  # Increased window size

        # Set font styles
        chat_font = ("Arial", 20)  # Larger font for chat history
        input_font = ("Arial", 20)  # Larger font for input field

        # Use grid layout to manage spacing
        self.grid_rowconfigure(0, weight=1)  # Chat history expands
        self.grid_rowconfigure(1, weight=0)  # Input section stays fixed
        self.grid_columnconfigure(0, weight=1)

        # Chat history area (scrollable) with larger text
        self.chat_history = scrolledtext.ScrolledText(self, state='disabled', wrap=tk.WORD, font=chat_font)
        self.chat_history.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # Expands with window

        # **Frame for input box & send button**
        self.input_frame = tk.Frame(self)
        self.input_frame.grid(row=1, column=0, padx=10, pady=3, sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        # **Multiline Text Input Field Instead of Entry**
        self.entry = tk.Text(self.input_frame, height=1.5, font=input_font)  # Increased height
        self.entry.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        self.placeholder = "Talk to me here..."
        self.entry.insert("1.0", self.placeholder)
        self.entry.bind("<FocusIn>", self.clear_placeholder)
        self.entry.bind("<FocusOut>", self.restore_placeholder)

        # Send Button
        self.send_button = tk.Button(self.input_frame, text="Send", font=input_font, command=self.send_message)
        self.send_button.grid(row=0, column=1)

        # Store document path
        self.document_path = document_path

        # Display a greeting message
        self.display_message("Bot: Hello! I'm your tournament assistant. How can I help you today?")

    def clear_placeholder(self, event):
            """Removes placeholder text when user c;icks the input box"""
            if self.entry.get("1.0", tk.END).strip() == self.placeholder:
                self.entry.delete("1.0", tk.END)
                self.entry.config(fg="white")  # Change text color to normal

    def restore_placeholder(self, event):
        """Restores placeholder text if input is empty when focus is lost."""
        if not self.entry.get("1.0", tk.END).strip():
            self.entry.insert("1.0", self.placeholder)
            self.entry.config(fg="gray")  # Change text color to gray

    def send_message(self):
        # Get the user's input (remove trailing newlines)
        user_input = self.entry.get("1.0", tk.END).strip()

        if not user_input:
            return  # Do nothing if input is empty

        if user_input.lower() == "exit" or user_input.lower() == "quit":
            self.quit()

        # Display the user's message
        self.display_message("---")
        self.display_message(f"You: {user_input}")

        # Call the chatbot to get a response
        bot_response = self.chatbot_response(user_input)

        # Display the bot's response
        self.display_message("---")
        self.display_message(f"Bot: {bot_response}")

        # Clear the input field after sending
        self.entry.delete("1.0", tk.END)

    def display_message(self, message):
        self.chat_history.configure(state='normal')
        self.chat_history.insert(tk.END, message + "\n", "chat")  # Use "chat" tag
        self.chat_history.configure(state='disabled')
        self.chat_history.yview(tk.END)

    def chatbot_response(self, user_input):
        # Ensure we call the function correctly
        response = chat_bot.chat_bot(self.document_path, user_input)  
        return response