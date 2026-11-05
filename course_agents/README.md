# 課堂最小 Agent

這個資料夾只供 GDGC 入門課實作。學員會修改 `hello_agent/agent.py` 裡的
`description` 與 `instruction`，再用 ADK Web 在本機和 Agent 對話。

從專案根目錄執行：

```bash
uv sync
cp course_agents/hello_agent/.env.example course_agents/hello_agent/.env
# 編輯 .env，填入自己的 Gemini API Key
uv run adk web course_agents --port 8000
```

瀏覽器開啟 <http://127.0.0.1:8000>，選擇 `hello_agent` 後提問。

以上是本機階段，不會建立任何雲端資源。要上雲，請讓 Claude Code 依根目錄 `RUNBOOK_TEMPLATE.md` 處理。
