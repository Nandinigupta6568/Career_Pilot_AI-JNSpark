# CareerPilot AI — Fetch-A-Thon 3.0 project

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3) ![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

**Purpose:** Help students turn an internship/career goal into an actionable skill-gap plan, curated learning resources, and relevant open-source project examples.

This repository is designed as a strong starting implementation for Fetch-A-Thon 3.0. It combines:
- Fetch.ai `uagents` with the standard chat protocol used by ASI:One-compatible agents, mailbox mode, and published agent details.
- ASI:One (`asi1`) as the core reasoning model.
- Real tool calling: skill-gap analysis, learning-resource lookup, study-plan generation, and live GitHub repository search.
- Local tests and documented deployment steps.

See [`REQUIREMENTS_MATRIX.md`](REQUIREMENTS_MATRIX.md) for the requirement-by-requirement status and [`SUBMISSION_DESCRIPTION.md`](SUBMISSION_DESCRIPTION.md) for a Devpost draft.

## Important distinction: code vs. external submission steps

The code cannot register itself into your personal Agentverse account or publish a public GitHub repository/video without you logging into those services. **Do not claim the submission is complete until you deploy it, verify it inside ASI:One, publish the repository, and capture the required links.** Agentverse UI/SDK details can change; use the current official guides linked below.

## Agent identity (fill after deployment)

- Agent name: `careerpilot_ai`
- Agent address: **add the actual deployed address here after Agentverse deployment**
- Agentverse profile: **add the real profile URL after registration**
- ASI:One shared chat: **add the real shared-chat URL after end-to-end testing**

## Features / judging requirements mapping

| Hackathon item | Included in this project | Still needs your action |
|---|---|---|
| Clear real-world problem | Career and internship preparation | Explain impact in your submission |
| Multi-step planning/reasoning | ASI:One tool-calling loop plus plan generation | Test representative prompts |
| Meaningful tool execution | Skill-gap planner, curated resources, live GitHub API search | Confirm internet/API availability |
| Agent Chat Protocol | `uagents_core` chat protocol handler | Deploy and verify in ASI:One |
| ASI:One as core reasoning | Direct `https://api.asi1.ai/v1/chat/completions` integration, model `asi1` | Add your API key |
| Agentverse discoverability | Agent configured to publish chat manifest | Register/deploy it in your account and verify listing |
| Workflow in ASI:One | Chat protocol reply calls the complete workflow | Test the live shared conversation |
| Public GitHub | README and `.gitignore` included | Push repo publicly and add badge/category |
| Demo + shared URLs | Submission checklist included | Record demo and capture real URLs |

Optional bonus features (multi-agent, Payment Protocol, Interactive Cards) are not falsely claimed as implemented. Prioritize mandatory requirements first.

## Requirements

- Python 3.10 or 3.11 recommended
- VS Code
- Internet connection
- ASI:One API key (required for full AI reasoning; create it in the ASI:One Developer area)
- Agentverse account for deployment

Official documentation:
- ASI:One developer quickstart: https://docs.asi1.ai/documentation/getting-started/quickstart
- ASI:One tool calling: https://docs.asi1.ai/documentation/build-with-asi-one/tool-calling
- uAgents docs: https://uagents.fetch.ai/docs
- Fetch.ai event brief: https://innovationlab.fetch.ai/

## Windows + VS Code: install and run

### 1. Extract and open
Extract the ZIP, open the `Fetchathon_CareerPilot` folder in VS Code, then choose **Terminal → New Terminal**.

### 2. Create a virtual environment
In PowerShell:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```
If PowerShell blocks activation, use a VS Code Command Prompt terminal:
```bat
.venv\Scripts\activate.bat
```

### 3. Install packages
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure ASI:One
Copy `.env.example` to `.env` and add your own key:
```env
ASI_ONE_API_KEY=PASTE_YOUR_REAL_KEY_HERE
ASI_ONE_BASE_URL=https://api.asi1.ai/v1
ASI_ONE_MODEL=asi1
# Optional stable identity seed; use a unique private value only
CAREERPILOT_AGENT_SEED=
```
Get a key through the ASI:One developer portal. Never share it or commit `.env`. The `.gitignore` already excludes `.env`.

### 5. Run tests and preflight checks
```powershell
python -m unittest discover -s tests -v
python scripts/preflight.py
python scripts/check_asi_one.py
```
The API check makes a real, small ASI:One request and may consume a small amount of API quota. It never prints your key.

### 6. Run local CLI test
```powershell
python main.py
```
Try:
> I want a Data Analyst internship in 6 weeks. I know basic Python and SQL. Find projects I can build and make a study plan.

The program will use ASI:One if configured. Without a key, the CLI will clearly report that AI mode is not enabled and offer a local diagnostic rather than pretending that an LLM response was generated.

### 7. Run the uAgent
Open a second terminal in VS Code:
```powershell
.\.venv\Scripts\Activate.ps1
python agent.py
```
Keep it running. The agent is configured with `mailbox=True`, publishes its chat protocol manifest, and publishes agent details. Follow the current Agentverse prompts/logs to complete mailbox authorization and registration. A local run does **not** by itself prove that the agent is discoverable or usable in ASI:One.

## Agentverse / ASI:One deployment checklist

1. Confirm `python agent.py` starts without errors.
2. Create/sign in to Agentverse.
3. Follow the current official “create an ASI:One-compatible uAgent” workflow. This code uses `mailbox=True`, `publish_agent_details=True`, `chat_protocol_spec`, and `publish_manifest=True`; complete any Agentverse authorization/registration prompts shown by the current tooling.
4. Ensure the agent is categorized under **Innovation Lab**.
5. In the agent README / project README include these exact badges:
   ```markdown
   ![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
   ![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)
   ```
6. Verify that the deployed agent is discoverable and directly callable through ASI:One.
7. In ASI:One, test a complete request such as: “Help me prepare for a data analyst internship in six weeks. Check my skills, build a plan, find learning resources, and find example GitHub projects.”
8. Capture the **real** Agentverse profile URL and the **public ASI:One shared-chat URL** after the test succeeds.
9. Push the code to a public GitHub repository. Add the actual deployed agent address to this README; do not invent one.
10. Record a 3–5 minute demo showing the full ASI:One workflow and tool results.

## Submission description starter

- **Problem:** Students often do not know which skills to learn or how to turn a career goal into a practical plan.
- **Target users:** Students and early-career applicants preparing for internships.
- **Outcome:** A personalized skill-gap summary, time-boxed action plan, verified learning links, and examples of open-source projects to study.
- **Tools:** ASI:One reasoning/tool calling, deterministic skill analysis, curated learning-resource catalog, and GitHub's public repository search API.

## What is implemented vs. what must be verified

Implemented in code: ASI:One API client with bounded function calling, allowlisted career tools, GitHub repository search, uAgents chat-protocol handler, mailbox configuration, manifest publishing, local tests, and setup/deployment documentation.

Account/deployment tasks that cannot be completed by a ZIP: creating your ASI:One key and private seed, authorizing/registering the agent in your Agentverse account, setting the Innovation Lab category in the platform, verifying ASI:One discovery, publishing the repository publicly, generating a shared-chat URL, and recording the demo video. Payment Protocol and Interactive Cards are optional bonus items and are not implemented in this version. Do not mark those items complete until you have verified them live.

## Troubleshooting

- `py` is not recognized: install Python from https://www.python.org/downloads/ and enable “Add Python to PATH”; restart VS Code.
- `ModuleNotFoundError`: activate `.venv`, then run `pip install -r requirements.txt`.
- `401 Unauthorized`: verify `ASI_ONE_API_KEY` and ensure it is active.
- `402 Payment Required` / quota errors: check API access and account usage.
- GitHub API rate limit: wait and retry; unauthenticated search has rate limits.
- Agentverse/ASI:One cannot see the agent: local execution alone is not deployment. Follow the current Agentverse deployment workflow and check the manifest/protocol.

## Security

- Keep `.env` private; never paste your API key into chat or commit it.
- This project does not buy courses, apply for jobs, or submit forms automatically.
- GitHub search results are untrusted external data; the agent summarizes them but should not execute code from repositories.
