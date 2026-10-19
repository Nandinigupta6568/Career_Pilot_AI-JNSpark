#  CareerPilot — AI Career Planning Agent

**From career goals to an actionable learning roadmap.**

CareerPilot is an AI-powered career-planning agent that helps students, beginners, and job seekers understand the skills they need, create structured study plans, discover learning resources, and explore relevant GitHub projects.

Built for the **Fetch-A-Thon 3.0 — ASI:One Agent Challenge**.

##  Problem Statement

Students and aspiring professionals often struggle to decide which skills to learn, which resources to trust, and how to turn a career goal into a practical plan. CareerPilot brings these steps together in one AI-powered conversation.

##  Our Solution

CareerPilot takes a user's career goal and current skill level and helps turn them into a practical learning roadmap. It combines career guidance with tools that analyze skill gaps, create study plans, find learning resources, and search GitHub project examples.

##  Key Features

- **Skill Gap Analysis:** Identifies skills a user may need to develop for a target career.
- **Personalized Study Plans:** Creates structured learning schedules based on the user's goals and current knowledge.
- **Learning Resource Discovery:** Recommends relevant tutorials, documentation, and learning platforms.
- **GitHub Project Discovery:** Finds example repositories that can inspire portfolio projects.
- **Conversational Career Guidance:** Lets users describe their goals naturally and receive an organized response.

##  Technology Stack

- **Python** — core agent implementation
- **ASI:One** — conversational AI experience
- **ASI:One API** — AI-powered responses
- **Fetch.ai uAgents / Agentverse** — agent development and registration
- **Tool-based workflow** — connects career-planning requests to specialized functions

##  How It Works

1. The user describes a career goal and current skills.
2. CareerPilot analyzes the user's needs.
3. It uses tools for skill-gap analysis, study-plan creation, learning-resource discovery, and GitHub project search.
4. The results are combined into an actionable career roadmap.
5. The user can ask follow-up questions to refine the plan.

##  Getting Started

### Prerequisites

- Python installed
- Git installed
- An ASI:One API key
- A private agent seed for your own agent setup

### 1. Clone the repository

```bash
git clone https://github.com/Nandinigupta6568/Career_Pilot_AI-JNSpark.git
```

### 2. Create a virtual environment

**Windows:**

```powershell
py -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```powershell
py -m pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and fill in the required values using your own API key and private agent seed.

```powershell
Copy-Item .env.example .env
```

Open `.env` in and update the following variables according to the names already defined in `.env.example`.

| Variable | What to enter |
|---|---|
| `ASI_ONE_API_KEY` | Your own valid ASI:One API key. Never use someone else's private key (sk_6625590b3a174c768c5e231dd38bd69da2bc07d764f0408ebbe71c21960c3423). |
| `CAREERPILOT_AGENT_SEED` | A unique private seed generated for your own agent identity. |

**Important:** The variable names above must match those in your actual `.env.example` file. If your project uses different names, use the exact names provided in that file.

#### Generate a private agent seed

Generate a random seed using Python:

```powershell
py -c "import secrets; print(secrets.token_hex(32))"
```

Copy the generated value into the `CAREERPILOT_AGENT_SEED` variable in `.env`, then save the file.

Each person registering their own agent should use a unique seed.


### Step 5: Verify your configuration

After saving `.env`, run:

```powershell
py -m scripts.preflight
```

If the configuration check passes, verify the API connection:

```powershell
py -m scripts.check_asi_one
```


### 5. Run the preflight check

```powershell
py -m scripts.preflight
```

### 6. Check the ASI:One API connection

```powershell
py -m scripts.check_asi_one
```

### 7. Start the agent

```powershell
py agent.py
```

Keep the terminal open while testing the local agent.

##  Project Links

- **ASI:One Demo:** https://asi1.ai/chat/19ca7341-b213-4886-9b99-b0883a695c0a?from=profile&handle=career-pilot-ai
- **Agentverse Profile:** https://agentverse.ai/agents/details/agent1qvcywc2skafar0p0ds0z2jus4msq2d9lvxkwwxrwpmx2cdfex0dk2hvf0y5/profile
- **GitHub Repository:** https://github.com/Nandinigupta6568/Career_Pilot_AI-JNSpark.git

##  Target Users

- Students exploring career options
- Beginners entering the technology industry
- Job seekers preparing for internships and entry-level roles
- Self-learners building technical skills and portfolios

##  Future Improvements

- More personalized recommendations based on a user's progress
- Interactive learning-plan cards
- Integration with additional career and learning data sources
- Multi-agent collaboration for deeper career research
- Progress tracking and portfolio milestones

##  Security

CareerPilot uses environment variables for sensitive configuration. Keep API keys and private agent seeds out of source control. Users deploying their own agent should configure their own credentials.

##  Built For

**Fetch-A-Thon 3.0 — ASI:One Agent Challenge**

CareerPilot aims to make career planning more structured, accessible, and actionable by turning a user's intent into a practical next step.

---

*Built with Python, ASI:One, and Fetch.ai agent technology.*