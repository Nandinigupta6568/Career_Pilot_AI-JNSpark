from careerpilot.orchestrator import run_careerpilot


def main() -> None:
    print("=" * 66)
    print("CareerPilot AI | Fetch-A-Thon 3.0")
    print("Career planning + ASI:One reasoning + executable tools")
    print("Type 'quit' to exit.")
    print("=" * 66)

    while True:
        try:
            prompt = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGood luck with your preparation!")
            break
        if prompt.lower() in {"quit", "exit", "q"}:
            print("Good luck with your preparation!")
            break
        if not prompt:
            print("Please enter your career goal and any current skills.")
            continue
        try:
            print("\nCareerPilot AI:\n")
            print(run_careerpilot(prompt))
        except Exception as exc:
            print(f"\nCareerPilot could not complete this request: {exc}")
            print("Check your .env settings and network connection, then retry.")


if __name__ == "__main__":
    main()
