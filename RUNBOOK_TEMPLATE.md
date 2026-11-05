# RUNBOOK 範本（讀者是 AI）

這份文件的讀者是 AI（Claude Code）。你要依本範本，為本專案產出一份 `RUNBOOK.md`。

## 任務

1. 讀完本範本與專案內容（至少 `course_agents/hello_agent/agent.py`、`pyproject.toml`）。
2. 在專案根目錄產出 `RUNBOOK.md`。
3. **只寫不執行**：產出 `RUNBOOK.md` 的過程中，不得執行任何 `gcloud`、`agents-cli`、`uvx google-agents-cli`、部署或刪除指令。允許的動作只有讀檔與寫 `RUNBOOK.md`。
4. 寫完後停下來，告訴使用者「RUNBOOK.md 已產出，等待人審」。使用者回覆審查通過之前，不得開始執行其中任何一步。

## 範圍

- 只部署 `course_agents/hello_agent`，目標是使用者自己的 GCP project 的 Agent Runtime（舊名 Vertex AI Agent Engine）。
- 可以新增部署所需檔案（見「補部署骨架」）。
- 不得修改 agent 的 `description` 與 `instruction`。
- 不得修改 `.env`，也不得讀出或印出其內容。

## RUNBOOK.md 的要求

- `RUNBOOK.md` 開頭第一段要寫明：讀者是 AI，執行前必須先讀完整份文件。
- 每一步固定三段格式，缺一不可：

```text
### 步驟 N：標題
執行：<完整、可直接貼上的指令；不得用「略」或「同上」>
驗證：<怎樣算成功；附檢查指令與預期輸出>
失敗：<失敗時的處置；預設是停下來回報>
```

- 需要人做的事，標題加上「（人做）」，AI 只提醒並等待回覆。
- 不確定的指令、旗標、API 名稱，標註「需查證」並在執行前先查官方文件，不得憑印象填寫。

## 必含步驟（依序）

1. **確認 project ID 與帳單**：請使用者提供 project ID，AI 檢查帳單已啟用。這一步必須等人回覆確認才能往下。
2. **啟用必要 API**：逐一列出要啟用的 API 與理由。哪些 API 是必要的若不確定，標註「需查證」，查官方文件後再寫入。
3. **補部署骨架**：缺的檔案由 AI 依官方文件與下方已知事項產生，內容寫進 RUNBOOK 的對應步驟。
4. **本機檢查**：部署前先確認 agent 能在本機載入（例如 import 檢查或 `adk` 指令），並列出打包會包含哪些檔案。
5. **部署**：使用下方「硬性費用防線」規定的旗標。
6. **查進度**：部署指令回傳後，用狀態查詢指令確認結果。
7. **雲端驗證**：對已部署的 Runtime 問一題，必須收到有內容的回答才算成功。
8. **清理**：刪除本次建立的 Agent Runtime。
9. **確認清理**：執行驗證指令，並提醒使用者自己到 Console 確認 Agent Runtime 列表是空的（人做）。

### 補部署骨架：參考清單

以下為另一個已成功部署的專案所需的骨架，供你比對，實際內容仍須查官方文件：

- `agents-cli-manifest.yaml`（deployment_target 為 agent_runtime）
- `Dockerfile`
- `app/fast_api_app.py` 與 `app/app_utils/`
- `.gcloudignore`：**必須存在**。缺少時打包會退回使用 `.gitignore`，可能漏檔或夾帶不該上傳的檔案。同時確認 `.env` 不會被打包上傳。

## 硬性費用防線

下列規則寫進 RUNBOOK，執行時不得放寬：

- 部署指令必須帶 `--min-instances 0`。預設值是 1，會 24 小時開機計費。
- 部署指令必須帶 `--max-instances 1`。
- 不加 `--agent-identity`。
- 不修改 IAM。
- 不建立 Secret Manager 資源。
- 不碰任何非本次建立的資源，包括使用者 project 內既有的其他服務。
- 預算警示是「人做」步驟：請使用者在 Console 的 Billing 設定預算警示。AI 只提醒，不代為設定。
- 模型走 Vertex AI（`GOOGLE_GENAI_USE_VERTEXAI=true`），費用由使用者的試用金支付。

## 停止條件

- 同一步驟重跑一次仍失敗，就停下來，貼出錯誤原文，不得第三次嘗試，也不得自行改用其他做法。
- 任何需要提升權限、修改 IAM、刪除非本次建立的資源的動作，一律停下來問人。
- project ID、帳單狀態、區域無法確認時，停下來問人。
- 發現指令會超出「範圍」與「硬性費用防線」時，停下來問人。

## 已知坑（給 AI 的提示）

來自另一個已成功部署的專案，寫 RUNBOOK 時請納入對應的驗證或失敗處置：

- 參考專案使用的部署形式為 `uvx google-agents-cli deploy --project <id> --region <region> --no-confirm-project --no-wait --min-instances 0 --update-env-vars "..."`，文件釘版 `google-agents-cli@1.3.1`。版本與旗標在本課程使用前需再查證。
- 部署失敗時常只回傳 code 13，且資源會自動刪除，看不到原因。加 `--no-wait`，再用 `deploy --status` 查詳細結果。
- `--update-env-vars` 的值不可含逗號。
- 使用者若用 Git Bash，指令前要加 `MSYS_NO_PATHCONV=1` 當前綴（只加在該指令前，不可全域 export），否則資源路徑會被轉成 Windows 路徑。
- 啟動 log 內 cloudresourcemanager 的 403 traceback 不是致命錯誤，不要因此判定失敗，以部署狀態與雲端驗證為準。
- 模型區域用 `us-central1` 可能出現 404，參考專案改用 `global`。遇到 404 時先檢查模型區域設定。
- 雲端驗證可用 `agents-cli run --url <engine resource> --mode adk "問題"`（需查證是否適用於目前版本）。

## 清理方式

- Agent Runtime 的刪除方式，請你查官方文件，把「刪除指令」與「驗證已刪除的指令」寫進 RUNBOOK。
- 只確認過可在 Console 刪除。CLI 與 SDK 的刪除方式未查證，找不到可靠的官方說法時，就寫 Console 的操作步驟，並標為「人做」。
- 清理只限本次建立的資源。
- 清理完成後，提醒使用者到 Console 確認 Agent Runtime 列表是空的。
