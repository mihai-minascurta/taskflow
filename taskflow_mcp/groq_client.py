import os
from openai import OpenAI


client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1",
)


MCP_URL = "https://beings-congress-activity-lawyer.trycloudflare.com/mcp"


def main():
    response = client.responses.create(
        model="openai/gpt-oss-20b",

        input="What is the status of my Kubernetes nodes?",

        tools=[
            {
                "type": "mcp",
                "server_label": "taskflow_infra",
                "server_description": (
                    "Kubernetes and AWS infrastructure tools "
                    "for the TaskFlow environment."
                ),
                "server_url": MCP_URL,
                "require_approval": "never",
            }
        ],
    )

    print(response.output_text)


if __name__ == "__main__":
    main()
