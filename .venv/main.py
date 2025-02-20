from UI.chatbot_ui import ChatbotUI

def main():
    document_path = "/Users/nicholasadams/Code/new-tournament-director/.venv/data/tournament-rules.txt"
    app = ChatbotUI(document_path)
    app.mainloop()

if __name__ == "__main__":
    main()



