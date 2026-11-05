from google.adk.agents import Agent


root_agent = Agent(
    name="hello_agent",
    model="gemini-3.6-flash",
    description="一個給入門課使用的最小 Agent。",
    instruction=(
        "你是友善的入門助教。"
        "請使用繁體中文回答，先直接回答問題，再給一個簡短例子。"
    ),
)
