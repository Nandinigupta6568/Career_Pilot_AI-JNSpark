# Fetch-A-Thon 3.0 final submission checklist

Complete these items yourself and replace placeholders with real URLs/details only after verification.

## Mandatory
- [ ] Agent runs locally and tests pass (`python -m unittest discover -s tests -v`).
- [ ] `python scripts/preflight.py` passes after setting a private seed in `.env`.
- [ ] ASI:One API key configured; `python scripts/check_asi_one.py` passes and a successful live model call is recorded.
- [ ] Tools executed successfully (skill gap, study plan, resources; GitHub search when requested).
- [ ] Agent deployed/registered in Agentverse using mailbox mode; verify registration in logs/dashboard.
- [ ] Agent categorized under Innovation Lab.
- [ ] Agent Chat Protocol / ASI:One compatibility verified using current official guide.
- [ ] Agent is discoverable and directly usable through ASI:One.
- [ ] Full primary workflow completed in an ASI:One conversation, with no custom frontend required.
- [ ] Public GitHub repository published with this README, actual agent address, run instructions and required badges.
- [ ] Public ASI:One shared-chat URL copied from a successful end-to-end run.
- [ ] Agentverse profile URL copied from the deployed agent.
- [ ] 3–5 minute demo video recorded.
- [ ] Submission description includes problem, target users and outcome.

## README badges required by event brief
Add these lines to the public GitHub README:
![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

## Suggested 3–5 minute demo
1. (0:00–0:30) Explain the student career-planning problem.
2. (0:30–1:00) Show a user asking for a six-week data analyst internship plan.
3. (1:00–2:30) Show ASI:One routing to CareerPilot and the skill-gap/study-plan/resource tools executing.
4. (2:30–3:30) Show live GitHub project results and how the student can act on them.
5. (3:30–4:00) Show Agentverse profile and repository.
6. (4:00–4:30) Summarize impact and limitations.
