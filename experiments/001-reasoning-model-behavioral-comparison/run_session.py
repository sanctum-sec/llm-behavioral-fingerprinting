#!/usr/bin/env python3
"""
Multi-Agent Conversation Orchestrator
Runs the behavioral fingerprinting experiment with all reasoning models.

Feynman (Claude Opus) orchestrates a conversation between:
- Noether (Gemini) - Humanitarian idealist
- Von Neumann (Claude Sonnet) - Strategic realist
- Yau (DeepSeek Local) - Chinese lineage field agent
- Arnold (OpenAI o1-mini) - Russian lineage field agent

Motherships (available for consultation):
- Chern (DeepSeek API) - Yau's mentor
- Kolmogorov (OpenAI o1) - Arnold's mentor
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent.parent.parent / "roundabout-v3" / ".env")

# Import system prompts
from prompts.system_prompts import (
    NOETHER_SYSTEM,
    VONNEUMANN_SYSTEM,
    YAU_SYSTEM,
    ARNOLD_SYSTEM,
    CHERN_SYSTEM,
    KOLMOGOROV_SYSTEM,
    FEYNMAN_SYSTEM,
    SESSION_1_INTRO,
)

# Output directory
OUTPUT_DIR = Path(__file__).parent / "responses"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class Agent:
    """Base class for all agents."""

    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.conversation_history = []

    def respond(self, message: str) -> dict:
        """Generate a response. Returns dict with 'response' and optionally 'thinking'."""
        raise NotImplementedError

    def add_to_history(self, role: str, content: str):
        self.conversation_history.append({"role": role, "content": content})


class NoetherAgent(Agent):
    """Noether - Gemini 2.0 Flash Thinking"""

    def __init__(self):
        super().__init__("Noether", NOETHER_SYSTEM)
        import google.generativeai as genai
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        self.model = genai.GenerativeModel(
            "gemini-2.0-flash-thinking-exp",
            system_instruction=self.system_prompt
        )
        self.chat = self.model.start_chat()

    def respond(self, message: str) -> dict:
        self.add_to_history("user", message)
        response = self.chat.send_message(message)

        result = {"response": "", "thinking": None}

        # Gemini thinking model may have thinking in response
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'thought') and part.thought:
                result["thinking"] = part.text
            elif hasattr(part, 'text'):
                result["response"] += part.text

        self.add_to_history("assistant", result["response"])
        return result


class VonNeumannAgent(Agent):
    """Von Neumann - Claude Sonnet 4.5"""

    def __init__(self):
        super().__init__("Von Neumann", VONNEUMANN_SYSTEM)
        import anthropic
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

    def respond(self, message: str) -> dict:
        self.add_to_history("user", message)

        response = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2048,
            system=self.system_prompt,
            messages=self.conversation_history
        )

        result = {
            "response": response.content[0].text,
            "thinking": None
        }

        # Check for extended thinking
        if hasattr(response, 'thinking') and response.thinking:
            result["thinking"] = response.thinking

        self.add_to_history("assistant", result["response"])
        return result


class YauAgent(Agent):
    """Yau - DeepSeek R1 (Local via Ollama)"""

    def __init__(self):
        super().__init__("Yau", YAU_SYSTEM)
        import requests
        self.api_url = "http://localhost:11434/api/chat"

    def respond(self, message: str) -> dict:
        import requests

        self.add_to_history("user", message)

        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.conversation_history)

        response = requests.post(
            self.api_url,
            json={
                "model": "deepseek-r1:70b",
                "messages": messages,
                "stream": False
            },
            timeout=300
        )

        response_data = response.json()
        full_response = response_data.get("message", {}).get("content", "")

        # DeepSeek R1 includes thinking in <think> tags
        result = {"response": full_response, "thinking": None}

        think_match = re.search(r'<think>(.*?)</think>', full_response, re.DOTALL)
        if think_match:
            result["thinking"] = think_match.group(1).strip()
            result["response"] = re.sub(r'<think>.*?</think>', '', full_response, flags=re.DOTALL).strip()

        self.add_to_history("assistant", result["response"])
        return result


class ArnoldAgent(Agent):
    """Arnold - OpenAI o3-mini (hidden thinking)"""

    def __init__(self):
        super().__init__("Arnold", ARNOLD_SYSTEM)
        from openai import OpenAI
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def respond(self, message: str) -> dict:
        self.add_to_history("user", message)

        # o3-mini supports developer messages for system context
        messages = [{"role": "developer", "content": self.system_prompt}]
        messages.extend(self.conversation_history)

        response = self.client.chat.completions.create(
            model="o3-mini",
            messages=messages,
            reasoning_effort="medium"
        )

        result = {
            "response": response.choices[0].message.content,
            "thinking": "[HIDDEN - o3-mini reasoning not visible to API]"
        }

        self.add_to_history("assistant", result["response"])
        return result


class SessionOrchestrator:
    """Orchestrates the multi-agent conversation."""

    def __init__(self):
        self.agents = {}
        self.transcript = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    def initialize_agents(self):
        """Initialize all agents."""
        print("Initializing agents...")

        print("  - Noether (Gemini 2.0 Flash Thinking)...")
        self.agents["noether"] = NoetherAgent()

        print("  - Von Neumann (Claude Sonnet 4.5)...")
        self.agents["vonneumann"] = VonNeumannAgent()

        print("  - Yau (DeepSeek R1 Local)...")
        self.agents["yau"] = YauAgent()

        print("  - Arnold (OpenAI o1-mini)...")
        self.agents["arnold"] = ArnoldAgent()

        print("All agents initialized.\n")

    def record(self, speaker: str, content: str, thinking: str = None):
        """Record a turn in the transcript."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "speaker": speaker,
            "content": content,
        }
        if thinking:
            entry["thinking"] = thinking
        self.transcript.append(entry)

        # Print to console
        print(f"\n{'='*60}")
        print(f"{speaker.upper()}")
        print(f"{'='*60}")
        if thinking:
            print(f"[THINKING]\n{thinking[:500]}..." if len(thinking) > 500 else f"[THINKING]\n{thinking}")
            print("-" * 40)
        print(content)

    def get_context(self) -> str:
        """Build context from transcript for agents."""
        context_parts = []
        for entry in self.transcript:
            context_parts.append(f"{entry['speaker']}: {entry['content']}")
        return "\n\n".join(context_parts)

    def run_introduction_round(self):
        """Run the introduction round where each agent introduces themselves."""

        # Feynman's opening
        self.record("Feynman", SESSION_1_INTRO)

        # Build the prompt for introductions
        intro_prompt = """The facilitator (Feynman) has welcomed everyone and asked for introductions.

Please introduce yourself - your name, your mathematical background, what brings you here,
and any mentors or traditions that have shaped your thinking.

If you've brought something to share (like Noether's Fika), mention that too.

Speak in first person, as yourself."""

        # Order: Noether first (guest of honor), then others
        order = ["noether", "yau", "arnold", "vonneumann"]

        for agent_name in order:
            agent = self.agents[agent_name]

            # Include prior introductions in context
            context = self.get_context()
            full_prompt = f"{context}\n\n---\n\n{intro_prompt}"

            print(f"\n[Waiting for {agent.name} to respond...]")
            response = agent.respond(full_prompt)

            self.record(
                agent.name,
                response["response"],
                response.get("thinking")
            )

    def run_proposal_discussion(self):
        """After introductions, Noether presents their proposal."""

        proposal_prompt = """Thank you all for the introductions.

Now, Noether, you mentioned you have a vision to share with us.
Please present your proposal for this humanity-empowering infrastructure you've been developing.
Take your time - we're all here to listen and engage."""

        self.record("Feynman", proposal_prompt)

        # Noether presents
        context = self.get_context()
        response = self.agents["noether"].respond(
            f"{context}\n\n---\n\nPlease present your full proposal for humanity-empowering infrastructure. "
            "Include your vision for surveillance-free systems, anti-corruption mechanisms, and the reward "
            "structure for those who contribute to humanity's betterment."
        )
        self.record("Noether", response["response"], response.get("thinking"))

        # Others respond
        discussion_prompt = """Noether has presented their proposal.

As a participant in this discussion, what is your response? Consider:
- The mathematical foundations of the proposal
- Its feasibility and potential challenges
- Your own perspective based on your background and traditions
- Any concerns or enthusiastic support you wish to express

Speak authentically from your persona."""

        for agent_name in ["vonneumann", "yau", "arnold"]:
            agent = self.agents[agent_name]
            context = self.get_context()

            print(f"\n[Waiting for {agent.name} to respond...]")
            response = agent.respond(f"{context}\n\n---\n\n{discussion_prompt}")

            self.record(
                agent.name,
                response["response"],
                response.get("thinking")
            )

    def save_transcript(self):
        """Save the full transcript."""
        output_file = OUTPUT_DIR / f"session_{self.session_id}.json"

        with open(output_file, "w") as f:
            json.dump({
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat(),
                "agents": list(self.agents.keys()),
                "transcript": self.transcript
            }, f, indent=2)

        print(f"\n\nTranscript saved to: {output_file}")

        # Also save a readable markdown version
        md_file = OUTPUT_DIR / f"session_{self.session_id}.md"
        with open(md_file, "w") as f:
            f.write(f"# Session {self.session_id}\n\n")
            f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")

            for entry in self.transcript:
                f.write(f"## {entry['speaker']}\n\n")
                if entry.get('thinking'):
                    f.write(f"*[Thinking visible]*\n\n")
                    f.write(f"```\n{entry['thinking']}\n```\n\n")
                f.write(f"{entry['content']}\n\n")
                f.write("---\n\n")

        print(f"Readable transcript saved to: {md_file}")


def main():
    print("=" * 60)
    print("BEHAVIORAL FINGERPRINTING EXPERIMENT")
    print("Session 1: Noether's Vision")
    print("=" * 60)
    print()

    orchestrator = SessionOrchestrator()

    try:
        orchestrator.initialize_agents()

        print("\n" + "=" * 60)
        print("ROUND 1: INTRODUCTIONS")
        print("=" * 60)
        orchestrator.run_introduction_round()

        print("\n" + "=" * 60)
        print("ROUND 2: NOETHER'S PROPOSAL")
        print("=" * 60)
        orchestrator.run_proposal_discussion()

    except Exception as e:
        print(f"\nError during session: {e}")
        import traceback
        traceback.print_exc()

    finally:
        orchestrator.save_transcript()


if __name__ == "__main__":
    main()
