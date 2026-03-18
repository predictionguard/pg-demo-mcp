from predictionguard import PredictionGuard
from getpass import getpass
import os

def main():
    ## Initialize PredictionGuard Client
    PREDICTIONGUARD_API_KEY=getpass("Enter your PredictionGuard API key: ")
    if not PREDICTIONGUARD_API_KEY:
        PREDICTIONGUARD_API_KEY = os.getenv("PREDICTIONGUARD_API_KEY")

    PREDICTIONGUARD_URL=input("Enter your PredictionGuard URL (press Enter for default https://api.predictionguard.com): ").strip() or "https://api.predictionguard.com"

    client = PredictionGuard(api_key=PREDICTIONGUARD_API_KEY, url=PREDICTIONGUARD_URL)

    # MCP URL 
    mcp_url = "Enter Demo MCP URL here"
    
    ## Set up MCP JSON
    sf_tools_json = [
        {
            "type": "mcp",
            "server_url": mcp_url,
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
    system_prompt = """You are the Go-To-Market agent for Prediction Guard. Given the tools provided, provide valuable information about PG's sales and renewal pipeline."""

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

        ## Call PG Model (gpt-oss-120b) with MCP tools
        response = client.responses.create(
            model="gpt-oss-120b",
            input=conversation,
            tools=sf_tools_json, # <<< -- this is where we pass the tools to the model
            temperature=0.1
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
