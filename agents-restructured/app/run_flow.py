import sys
from app.agents.argument_analysis_agent import argument_analysis_agent
from app.agents.fallacy_detection_agent import fallacy_detection_agent


def main() -> None:
    if len(sys.argv) > 1:
        user_argument = " ".join(sys.argv[1:])
    else:
        user_argument = input("Enter your argument: ").strip()

    if not user_argument:
        print("No argument entered.")
        return

    print("\nYour argument:")
    print(user_argument)

    print("\nArgument Analysis:")
    analysis_result = argument_analysis_agent.run(user_argument)
    print(analysis_result)

    print("\nFallacy Detection:")
    fallacy_result = fallacy_detection_agent.run(user_argument)
    if fallacy_result.get("message"):
        print(fallacy_result["message"])
        print("\nDetailed result:")
    print(fallacy_result)


if __name__ == "__main__":
    main()
