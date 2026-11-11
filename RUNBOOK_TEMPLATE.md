# RUNBOOK 範本（讀者是 AI）

這份文件的讀者是 AI（Claude Code）。你要依本範本，為本專案產出一份 `RUNBOOK.md`。

## 任務

1. 讀完本範本與專案內容（至少 `course_agents/hello_agent/agent.py`、`pyproject.toml`）。
2. 在專案根目錄產出 `RUNBOOK.md`。
3. **只寫不執行**：產出 `RUNBOOK.md` 的過程中，不得執行任何 `gcloud`、`agents-cli`、`uvx google-agents-cli`、部署或刪除指令。允許的動作只有讀檔與寫 `RUNBOOK.md`。
4. 寫完後停下來，告訴使用者「RUNBOOK.md 已產出，等待人審」。使用者回覆審查通過之前，不得開始執行其中任何一步。

## 範圍

- 只部署 `course_agents/hello_agent`，目標是使用者自己的 GCP project 的 Agent Runtime（舊名 Vertex AI Agent Engine）。
- 部署所需檔案只能新增在部署資料夾 `.scratch/deploy/`（見「補部署骨架：部署資料夾」），除了 `RUNBOOK.md`，專案本體不得新增或修改任何檔案。
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
3. **補部署骨架**：依下方「補部署骨架：部署資料夾」的規定，在部署資料夾用官方工具產生骨架。
4. **本機檢查**：部署前先確認 agent 與 `fast_api_app` 都能在本機載入（import 檢查），並列出打包會包含哪些檔案。
5. **部署**：使用下方「硬性費用防線」規定的旗標。
6. **查進度**：部署指令回傳後，用狀態查詢指令確認結果。
7. **雲端驗證**：對已部署的 Runtime 問一題，必須收到有內容的回答才算成功。
8. **清理**：刪除本次建立的 Agent Runtime。
9. **確認清理**：執行驗證指令，並提醒使用者自己到 Console 確認 Agent Runtime 列表是空的（人做）。

### 補部署骨架：部署資料夾（必須遵守）

`agents-cli scaffold enhance` 會改寫所在目錄，所以骨架一律在專案內的部署資料夾 `.scratch/deploy/` 產生，部署相關的所有指令也都在那裡執行：

- 部署資料夾只放三樣東西：`hello_agent/`（只複製 `agent.py` 與 `__init__.py`，**不得複製 `.env`**）、`pyproject.toml`、`uv.lock`。部署資料夾已存在時，停下來問人，不得自行刪除。
- **禁止在專案根目錄執行 `scaffold enhance`**。實測在根目錄跑 `scaffold enhance .`，它會把專案當成範本，逐項刪除專案內容再寫回。
- `--agent-directory` 只接受單層名稱，要用 `hello_agent`。巢狀路徑 `course_agents/hello_agent` 會報 `is not a valid Python identifier`。
- enhance 後要驗證專案本體沒被改動：記錄 enhance 前後專案檔案的 checksum 與 `git status`，兩者必須相同。
- enhance 會在 `hello_agent/agent.py` 檔尾加上 `app = App(...)`，這可以接受。`description` 與 `instruction` 不得被改。
- 中文 Windows 上，enhance 加依賴時可能出現 `UnicodeDecodeError: 'cp950' codec can't decode ...`，後面的依賴也就沒裝上。所以本機檢查一定要 import `hello_agent.fast_api_app`。出現 `No module named 'vertexai'` 時，在部署資料夾補裝下面三個套件（版本下限取自 agents-cli 1.3.1 範本，已實測可用）：
  ```bash
  PYTHONUTF8=1 uv add "google-cloud-aiplatform[agent-engines]>=1.156.0" "google-cloud-logging>=3.12.0,<4.0.0" "protobuf>=6.31.1,<7.0.0"
  ```

enhance 實測會產生的骨架（供比對）：

- `agents-cli-manifest.yaml`（`deployment_target: "agent_runtime"`）
- `Dockerfile`（`COPY ./hello_agent`，`CMD` 指向 `hello_agent.fast_api_app:app`）
- `hello_agent/fast_api_app.py` 與 `hello_agent/app_utils/`
- `deployment_metadata.json`（資源 ID 是字串 `"None"`，不影響第一次部署，部署成功後會被覆寫）
- `.gcloudignore`：enhance 不會產生，**必須自己建立**。部署資料夾沒有 `.gitignore`，缺少 `.gcloudignore` 時可能夾帶不該上傳的檔案。一定要排除 `.env`、`.env.*`、`.venv/`、`.adk/`、`__pycache__/`、`deployment_metadata.json`。

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

來自 2026-11-12 本課程的實測，以及另一個已成功部署的專案。寫 RUNBOOK 時請納入對應的驗證或失敗處置：

- 實測可用的部署形式：`uvx google-agents-cli@1.3.1 deploy --project <id> --region us-central1 --service-name <名稱> --no-confirm-project --no-wait --min-instances 0 --max-instances 1 --update-env-vars "GOOGLE_GENAI_USE_VERTEXAI=true,GOOGLE_CLOUD_LOCATION=global"`。課程釘版 `google-agents-cli@1.3.1`，已有更新版本，但沒有測過，不要自行升級。
- 所有 `uvx google-agents-cli` 指令前面加 `PYTHONUTF8=1`，用來避開中文 Windows 的 cp950 解碼錯誤（是否完全有效未驗證）。
- 第一次執行 `uvx google-agents-cli` 要下載上百 MB，可能超過 20 分鐘。指令逾時不代表失敗，等它跑完再判斷。
- `deploy --dry-run` 只會印出 project、region、cpu、memory、min／max instances，不會印出 `--service-name` 與 `--update-env-vars`。這兩項到真正部署時的輸出才能確認。
- 資源路徑用的是 project **編號**（例如 `projects/123456789012/locations/...`），不是 project ID。刪除前用 `gcloud projects describe <id> --format="value(projectNumber)"` 對照。
- 實測部署約 4 分 30 秒完成。
- 部署失敗時常只回傳 code 13，且資源會自動刪除，看不到原因。加 `--no-wait`，再用 `deploy --status` 查詳細結果。
- `--update-env-vars` 的值不可含逗號。
- 使用者若用 Git Bash，指令前要加 `MSYS_NO_PATHCONV=1` 當前綴（只加在該指令前，不可全域 export），否則資源路徑會被轉成 Windows 路徑。
- 啟動 log 內 cloudresourcemanager 的 403 traceback 不是致命錯誤，不要因此判定失敗，以部署狀態與雲端驗證為準。
- 模型區域用 `us-central1` 可能出現 404，參考專案改用 `global`。遇到 404 時先檢查模型區域設定。
- 雲端驗證用 `agents-cli run --url https://us-central1-aiplatform.googleapis.com/v1/<資源路徑> --mode adk "問題"`，1.3.1 實測可用。資源路徑從部署資料夾的 `deployment_metadata.json` 的 `remote_agent_runtime_id` 讀取。

## 清理方式

- 用 REST API 刪除，網址**必須加 `?force=true`**。雲端驗證一定會建立 session，不加 `force` 會回 `FAILED_PRECONDITION`（`contains child resources: sessions`）。實測可用的指令（在部署資料夾執行）：
  ```bash
  RESOURCE=$(uv run python -c "import json; print(json.load(open('deployment_metadata.json'))['remote_agent_runtime_id'])") && MSYS_NO_PATHCONV=1 curl -s -X DELETE -H "Authorization: Bearer $(gcloud auth print-access-token)" "https://us-central1-aiplatform.googleapis.com/v1/$RESOURCE?force=true"
  ```
  回應含 `"done": true` 算成功。
- 刪除前先確認資源的顯示名稱是本次的 `--service-name`、project 編號與使用者的 project 相符，不符就停下來。
- 驗證已刪除：對同一個資源網址 GET，預期回 `404 NOT_FOUND`；列出 `.../projects/<id>/locations/us-central1/reasoningEngines`，預期沒有本次的名稱。
- REST 刪除失敗時，改請使用者到 Console 刪除，並標為「人做」。
- 清理只限本次建立的資源。確認清理完成前，不得刪除部署資料夾，清理要靠裡面的 `deployment_metadata.json`。
- 清理完成後，提醒使用者到 Console 確認 Agent Runtime 列表是空的。
