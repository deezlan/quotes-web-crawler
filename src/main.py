from src.crawler import crawl
from src.indexer import build_index, save_index, load_index
from src.search import print_index, find_pages


def run_shell():
    index = {}
    print("Search Engine Shell — type 'help' for commands, 'quit' to exit.\n")

    while True:
        try:
            user_input = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[shell] Exiting.")
            break

        if not user_input:
            continue

        parts = user_input.split(maxsplit=1)
        command = parts[0].lower()
        argument = parts[1] if len(parts) > 1 else ""

        if command == "quit" or command == "exit":
            print("[shell] Exiting.")
            break

        elif command == "help":
            print("\nAvailable commands:")
            print("  build              Crawl the website and build the index")
            print("  load               Load the index from disk")
            print("  print <word>       Print index entry for a word")
            print("  find <query>       Find pages containing all query terms")
            print("  quit               Exit the shell\n")

        elif command == "build":
            print("[shell] Starting crawl...")
            pages = crawl()
            index = build_index(pages)
            save_index(index)
            print(f"[shell] Index built with {len(index)} unique words.")

        elif command == "load":
            index = load_index()
            if index:
                print(f"[shell] Index loaded with {len(index)} unique words.")

        elif command == "print":
            if not argument:
                print("[shell] Usage: print <word>")
            else:
                print_index(index, argument)

        elif command == "find":
            if not argument:
                print("[shell] Usage: find <query>")
            else:
                find_pages(index, argument)

        else:
            print(f"[shell] Unknown command: '{command}'. Type 'help' for options.")


if __name__ == "__main__":
    run_shell()