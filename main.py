
import summarizer

def run_app():
    print("=== HIGH-ACCURACY EXTRACTIVE SUMMARIZER ===")
    print("Paste your paragraph. Type 'exit' to quit.\n")

    while True:
        text = input("Enter/Paste Text:\n").strip()

        if text.lower() in ["exit", "quit"]:
            print("Summarizer closed.")
            break

        if not text:
            continue

        summary = summarizer.summarize_text(text, top_n=2)
        print("\n--- Key Accurate Summary ---")
        print(summary)
        print("-" * 45 + "\n")

if __name__ == "__main__":
    run_app()