from functions import chat_bot


def main():
    print("Poker AI Starting...")
    document_path = "/Users/nicholasadams/Code/new-tournament-director/.venv/data/tournament-rules.txt"
    chat_bot.chat_bot(document_path)

if __name__ == "__main__":
    main()



