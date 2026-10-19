"""ASI:One-compatible Fetch.ai uAgent using the standard chat protocol."""
import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())
from datetime import datetime, timezone
from uuid import uuid4
import os
from dotenv import load_dotenv

from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)

from careerpilot.orchestrator import run_careerpilot

# Optional seed: set CAREERPILOT_AGENT_SEED in your private .env to retain identity.
# Without it, uAgents creates a local identity; use the Agentverse deployment flow
# to configure the persistent identity and reachable endpoint for your deployment.
load_dotenv()
agent_seed = os.getenv("CAREERPILOT_AGENT_SEED", "").strip()
agent_kwargs = {
    "name": "careerpilot_ai",
    "port": 8001,
    "mailbox": True,
    "publish_agent_details": True,
}
if agent_seed:
    agent_kwargs["seed"] = agent_seed
agent = Agent(**agent_kwargs)

chat_proto = Protocol(spec=chat_protocol_spec)


def create_chat_message(text: str, end_session: bool = False) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    # ASI:One chat sessions should be explicitly closed after a completed reply.
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(
        timestamp=datetime.now(timezone.utc),
        msg_id=uuid4(),
        content=content,
    )


@chat_proto.on_message(ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.now(timezone.utc),
            acknowledged_msg_id=msg.msg_id,
        ),
    )

    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info("Chat session started.")
        elif isinstance(item, TextContent):
            ctx.logger.info("Received a career-planning request.")
            try:
                # Run the complete plan + real tool-calling workflow.
                answer = run_careerpilot(item.text)
            except Exception:
                ctx.logger.exception("CareerPilot workflow failed.")
                answer = (
                    "I couldn't complete that request. Please check that the "
                    "ASI:One API key is configured and retry with your career goal "
                    "and current skills."
                )
            await ctx.send(sender, create_chat_message(answer, end_session=True))
        elif isinstance(item, EndSessionContent):
            ctx.logger.info("Chat session ended.")
        else:
            ctx.logger.info("Unsupported chat content received.")


@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info("Acknowledgement received.")


agent.include(chat_proto, publish_manifest=True)


if __name__ == "__main__":
    print("Starting CareerPilot AI uAgent...")
    print(f"Agent address: {agent.address}")
    print("Mailbox mode enabled. Confirm Agentverse registration and ASI:One discovery in your account.")
    agent.run()
