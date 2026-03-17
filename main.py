from predictionguard import PredictionGuard
from dotenv import load_dotenv

# load environment variables (make sure that PREDICTIONGUARD_API_KEY is set in the .env file)
load_dotenv()

def main():
    ## Initialize PredictionGuard Client
    
    client = PredictionGuard()

    ## Set up MCP JSON
    sf_tools_json = [
        {
            "type": "mcp",
            "server_url": "https://<MCP_SERVER_URL>.us-central1.run.app/mcp",
            "server_label": "pg-salesforce-demo",
            "allowed_tools": [
            "execute_sf_query",
            "generate_renewal_pipeline",
            "generate_sales_pipeline"
            ],
            "server_description": "Salesforce Demo for PG GTM"
        }
    ]

    ## Set up System Prompt
    system_prompt = """You are the Go-To-Market agent for Prediction Guard. Given the tools provided, provide valuable information about PG's sales and renewal pipeline. The year is 2026"""

    ## Set up an agent with gpt-oss-120b
    conversation = [{"role": "system", "content": system_prompt}]

    ## allow agent to interact with users on cli
    print("\n=== GTM Agent | PredictionGuard + Salesforce ===")
    print("Type 'quit' to exit.\n")

    while True:
        try:
            user_input = input("\033[1;36mYou:\033[0m ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit"):
            print("Goodbye!")
            break

        conversation.append({"role": "user", "content": user_input})

        response = client.responses.create(
            model="gpt-oss-120b",
            input=conversation,
            tools=sf_tools_json,
        )

        # Extract reply text from the response output item
        reply = ""
        for item in response.get("output", []):
            if item.get("type") == "message":
                for block in item.get("content", []):
                    if block.get("type") == "output_text":
                        reply += block.get("text", "")
            elif "text" in item:
                reply = item["text"]
        reply = reply.strip() or response.get("text", "(no response)")

        print(f"\n\033[1;32mAgent:\033[0m {reply}\n")
        conversation.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    main()
