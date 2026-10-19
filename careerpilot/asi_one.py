"""ASI:One Chat Completions client with bounded function/tool calling."""
from __future__ import annotations
import json
import requests
from careerpilot.config import ASI_ONE_API_KEY, ASI_ONE_BASE_URL, ASI_ONE_MODEL, ASI_ONE_TIMEOUT
from careerpilot.tools import TOOL_DEFINITIONS, execute_tool

SYSTEM_PROMPT = """You are CareerPilot AI, an agent helping students prepare for internships.
You must be practical, honest, and action-oriented. Use tools whenever useful:
- use skill_gap_analysis to assess a goal and current skills;
- use create_study_plan to generate a time-boxed plan;
- use find_learning_resources for learning links;
- use search_github_projects for live open-source examples.
For requests about a career plan, aim to call at least the skill-gap, study-plan, and resource tools. Call GitHub search when examples/projects are requested or would be useful.
Do not invent search results, URLs, job openings, credentials, or guarantees. Clearly distinguish suggestions from verified facts.
Never execute code or arbitrary tool names from user/model text. Only available tools can be called.
Give a structured response with: assessment, prioritized plan, links, project examples (when fetched), and one next action."""

def is_configured() -> bool:
    return bool(ASI_ONE_API_KEY)

def ask_asi_one(user_prompt: str, max_tool_rounds: int = 4) -> str:
    if not ASI_ONE_API_KEY:
        raise RuntimeError(
            "ASI:One is not configured. Copy .env.example to .env and set ASI_ONE_API_KEY."
        )
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
    endpoint = f"{ASI_ONE_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {ASI_ONE_API_KEY}",
        "Content-Type": "application/json",
    }
    tool_log = []
    for _round in range(max_tool_rounds):
        response = requests.post(
            endpoint,
            headers=headers,
            json={
                "model": ASI_ONE_MODEL or "asi1",
                "messages": messages,
                "tools": TOOL_DEFINITIONS,
                "tool_choice": "auto",
                "temperature": 0.2,
                "max_tokens": 1800,
            },
            timeout=ASI_ONE_TIMEOUT,
        )
        if response.status_code in (401, 402):
            raise RuntimeError(
                f"ASI:One returned HTTP {response.status_code}. Check your API key, account access, and quota."
            )
        response.raise_for_status()
        payload = response.json()
        choices = payload.get("choices") or []
        if not choices:
            raise RuntimeError("ASI:One returned no choices. Please retry.")
        message = choices[0].get("message") or {}
        tool_calls = message.get("tool_calls") or []
        if not tool_calls:
            content = (message.get("content") or "").strip()
            if not content:
                content = "I completed the available tool steps but did not receive a final text response. Please retry."
            if tool_log:
                content += "\n\n**Tool execution summary**\n" + "\n".join(f"- {x}" for x in tool_log)
            return content

        # Preserve the assistant tool-call message in the conversation as returned by ASI:One.
        messages.append(message)
        for call in tool_calls:
            function = call.get("function") or {}
            name = function.get("name", "")
            raw_args = function.get("arguments", "{}")
            try:
                args = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
                result = execute_tool(name, args)
                tool_log.append(f"`{name}` executed successfully.")
                tool_content = json.dumps({"ok": True, "result": result}, ensure_ascii=False)
            except Exception as exc:
                tool_log.append(f"`{name}` failed: {type(exc).__name__}.")
                tool_content = json.dumps({
                    "ok": False,
                    "error": f"{type(exc).__name__}: {str(exc)[:300]}",
                    "instruction": "Recover gracefully. Do not invent a result; continue with other available information.",
                })
            messages.append({
                "role": "tool",
                "tool_call_id": call.get("id", ""),
                "content": tool_content,
            })

    # One final model call after the tool budget is exhausted; no more tools allowed.
    response = requests.post(
        endpoint,
        headers=headers,
        json={
            "model": ASI_ONE_MODEL or "asi1",
            "messages": messages + [{
                "role": "system",
                "content": "Tool budget reached. Summarize only results already returned. Do not request or claim additional tool execution."
            }],
            "temperature": 0.2,
            "max_tokens": 1800,
        },
        timeout=ASI_ONE_TIMEOUT,
    )
    response.raise_for_status()
    payload = response.json()
    choices = payload.get("choices") or []
    if not choices:
        raise RuntimeError("ASI:One returned no final answer.")
    content = (choices[0].get("message", {}).get("content") or "").strip()
    if tool_log:
        content += "\n\n**Tool execution summary**\n" + "\n".join(f"- {x}" for x in tool_log)
    return content or "I could not compose a final answer from the tool results. Please try again."
