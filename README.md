# 讓 Claude Code 替你部署：ADK Agent 從地端到 GCP

GDGC 入門課的學員實作專案。學員請 Claude Code 寫出一個 ADK Agent 並在本機驗收，接著請它依範本寫出部署文件 `RUNBOOK.md`，學員審過後，再交給它部署到自己 GCP project 的 Agent Runtime，驗證後清理。

## 開始之前

先完成 [docs/課前準備.md](docs/課前準備.md)。

## 檔案

| 路徑 | 用途 |
|---|---|
| `docs/課前準備.md` | 上課前要裝好的工具與檢查指令 |
| `docs/學員版實作講義.md` | 上課實作步驟與提示詞 |
| `course_agents/hello_agent/` | 實作用的最小 Agent |
| `RUNBOOK_TEMPLATE.md` | 給 Claude Code 讀的部署文件範本 |

## 安全提醒

- Gemini API Key 只放在 `course_agents/hello_agent/.env`，`.env` 已列入 `.gitignore`。不要貼進聊天、AI 對話或 Git commit。
- 上雲會用到自己 GCP project 的試用金，實作結束記得清理，並到 Console 確認 Agent Runtime 列表是空的。
