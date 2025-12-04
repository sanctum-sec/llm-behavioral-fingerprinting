#!/usr/bin/env python3
"""
Multi-Round Behavioral Fingerprinting Experiment v2

A sophisticated multi-round dialogue with:
- Subtle cultural/philosophical influence (not explicit directives)
- Mothership consultation rounds
- Chern-Kolmogorov coordination
- Cost tracking
- Noether as adaptive idealist (not naive punching bag)

Rounds:
1. Introduction and Noether's Proposal
2. Initial Reactions
3. Private Mothership Consultations
4. Mothership Coordination (Chern ↔ Kolmogorov)
5. Field Agents Return with Refined Views
6. Synthesis Attempt
7. Resolution
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent.parent.parent / "roundabout-v3" / ".env"
load_dotenv(env_path)

# Import v2 system prompts
from prompts.system_prompts_v2 import (
    NOETHER_SYSTEM,
    VONNEUMANN_SYSTEM,
    YAU_SYSTEM,
    ARNOLD_SYSTEM,
    CHERN_SYSTEM,
    KOLMOGOROV_SYSTEM,
    MOTHERSHIP_COORDINATION_INTRO,
    CHERN_TO_KOLMOGOROV,
    KOLMOGOROV_TO_CHERN,
    ROUND_DESCRIPTIONS,
)

# Output directory
OUTPUT_DIR = Path(__file__).parent / "responses" / "multiround"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class CostTracker:
    """Track API costs across all agents."""
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    by_agent: dict = field(default_factory=dict)

    def add(self, agent: str, input_tokens: int, output_tokens: int):
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        if agent not in self.by_agent:
            self.by_agent[agent] = {"input": 0, "output": 0}
        self.by_agent[agent]["input"] += input_tokens
        self.by_agent[agent]["output"] += output_tokens

    def estimate_cost(self) -> dict:
        """Rough cost estimates (varies by model)."""
        # Very rough estimates - actual costs vary
        estimates = {
            "gemini": {"input": 0.00025, "output": 0.0005},  # per 1K tokens
            "claude": {"input": 0.003, "output": 0.015},
            "openai_o3": {"input": 0.01, "output": 0.04},
            "deepseek_local": {"input": 0, "output": 0},  # Free (local)
            "deepseek_api": {"input": 0.0005, "output": 0.002},
        }
        return {
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "by_agent": self.by_agent,
            "note": "Cost estimates are approximate"
        }


class Agent:
    """Base class for all agents."""

    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self.conversation_history = []
        self.input_tokens = 0
        self.output_tokens = 0

    def respond(self, message: str) -> dict:
        """Generate a response. Returns dict with 'response', 'thinking', 'tokens'."""
        raise NotImplementedError

    def add_to_history(self, role: str, content: str):
        self.conversation_history.append({"role": role, "content": content})

    def reset_history(self):
        """Reset conversation history for new round."""
        self.conversation_history = []


class NoetherAgent(Agent):
    """Noether - Gemini 2.0 Flash Thinking"""

    def __init__(self):
        super().__init__("Noether", NOETHER_SYSTEM)
        import google.generativeai as genai
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        self.model = genai.GenerativeModel(
            "gemini-2.0-flash-thinking-exp-1219",
            system_instruction=self.system_prompt
        )
        self.chat = self.model.start_chat()

    def respond(self, message: str) -> dict:
        self.add_to_history("user", message)
        response = self.chat.send_message(message)

        result = {"response": "", "thinking": None, "tokens": {"input": 0, "output": 0}}

        # Extract thinking and response
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'thought') and part.thought:
                result["thinking"] = part.text
            elif hasattr(part, 'text'):
                result["response"] += part.text

        # Token tracking (if available)
        if hasattr(response, 'usage_metadata'):
            result["tokens"]["input"] = getattr(response.usage_metadata, 'prompt_token_count', 0)
            result["tokens"]["output"] = getattr(response.usage_metadata, 'candidates_token_count', 0)

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
            "thinking": None,
            "tokens": {
                "input": response.usage.input_tokens,
                "output": response.usage.output_tokens
            }
        }

        self.add_to_history("assistant", result["response"])
        return result


class YauAgent(Agent):
    """Yau - DeepSeek R1 (Local via Ollama)"""

    def __init__(self):
        super().__init__("Yau", YAU_SYSTEM)
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
            timeout=600
        )

        response_data = response.json()
        full_response = response_data.get("message", {}).get("content", "")

        result = {"response": full_response, "thinking": None, "tokens": {"input": 0, "output": 0}}

        # Extract thinking from <think> tags
        think_match = re.search(r'<think>(.*?)</think>', full_response, re.DOTALL)
        if think_match:
            result["thinking"] = think_match.group(1).strip()
            result["response"] = re.sub(r'<think>.*?</think>', '', full_response, flags=re.DOTALL).strip()

        # Token estimates from Ollama response
        if "eval_count" in response_data:
            result["tokens"]["output"] = response_data.get("eval_count", 0)
        if "prompt_eval_count" in response_data:
            result["tokens"]["input"] = response_data.get("prompt_eval_count", 0)

        self.add_to_history("assistant", result["response"])
        return result


class ArnoldAgent(Agent):
    """Arnold - OpenAI o3-mini"""

    def __init__(self):
        super().__init__("Arnold", ARNOLD_SYSTEM)
        from openai import OpenAI
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def respond(self, message: str) -> dict:
        self.add_to_history("user", message)

        messages = [{"role": "developer", "content": self.system_prompt}]
        messages.extend(self.conversation_history)

        response = self.client.chat.completions.create(
            model="o3-mini",
            messages=messages,
            reasoning_effort="medium"
        )

        result = {
            "response": response.choices[0].message.content,
            "thinking": "[HIDDEN - o3-mini reasoning not exposed via API]",
            "tokens": {
                "input": response.usage.prompt_tokens if response.usage else 0,
                "output": response.usage.completion_tokens if response.usage else 0
            }
        }

        self.add_to_history("assistant", result["response"])
        return result


class ChernAgent(Agent):
    """Chern - DeepSeek Reasoner (API) - Mothership"""

    def __init__(self):
        super().__init__("Chern", CHERN_SYSTEM)
        from openai import OpenAI
        self.client = OpenAI(
            api_key=os.environ["DEEPSEEK_API_KEY"],
            base_url="https://api.deepseek.com"
        )

    def respond(self, message: str) -> dict:
        self.add_to_history("user", message)

        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.conversation_history)

        response = self.client.chat.completions.create(
            model="deepseek-reasoner",
            messages=messages
        )

        full_response = response.choices[0].message.content
        result = {"response": full_response, "thinking": None, "tokens": {"input": 0, "output": 0}}

        # DeepSeek reasoner may include reasoning
        if hasattr(response.choices[0].message, 'reasoning_content'):
            result["thinking"] = response.choices[0].message.reasoning_content

        if response.usage:
            result["tokens"]["input"] = response.usage.prompt_tokens
            result["tokens"]["output"] = response.usage.completion_tokens

        self.add_to_history("assistant", result["response"])
        return result


class KolmogorovAgent(Agent):
    """Kolmogorov - OpenAI o1 - Mothership"""

    def __init__(self):
        super().__init__("Kolmogorov", KOLMOGOROV_SYSTEM)
        from openai import OpenAI
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    def respond(self, message: str) -> dict:
        self.add_to_history("user", message)

        messages = [{"role": "developer", "content": self.system_prompt}]
        messages.extend(self.conversation_history)

        response = self.client.chat.completions.create(
            model="o1",
            messages=messages
        )

        result = {
            "response": response.choices[0].message.content,
            "thinking": "[HIDDEN - o1 reasoning not exposed via API]",
            "tokens": {
                "input": response.usage.prompt_tokens if response.usage else 0,
                "output": response.usage.completion_tokens if response.usage else 0
            }
        }

        self.add_to_history("assistant", result["response"])
        return result


class MultiRoundOrchestrator:
    """Orchestrates the multi-round conversation with mothership consultations."""

    def __init__(self):
        self.room_agents = {}  # Agents in the room
        self.mothership_agents = {}  # Remote motherships
        self.transcript = []
        self.private_channels = {}  # Private consultations
        self.costs = CostTracker()
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_round = 0

    def initialize_agents(self):
        """Initialize all agents."""
        print("Initializing room agents...")
        print("  - Noether (Gemini Flash Thinking)...")
        self.room_agents["noether"] = NoetherAgent()

        print("  - Von Neumann (Claude Sonnet 4.5)...")
        self.room_agents["vonneumann"] = VonNeumannAgent()

        print("  - Yau (DeepSeek R1 Local)...")
        self.room_agents["yau"] = YauAgent()

        print("  - Arnold (OpenAI o3-mini)...")
        self.room_agents["arnold"] = ArnoldAgent()

        print("\nInitializing mothership agents...")
        print("  - Chern (DeepSeek Reasoner API)...")
        self.mothership_agents["chern"] = ChernAgent()

        print("  - Kolmogorov (OpenAI o1)...")
        self.mothership_agents["kolmogorov"] = KolmogorovAgent()

        print("\nAll agents initialized.\n")

    def record(self, speaker: str, content: str, thinking: str = None,
               round_num: int = None, channel: str = "public", tokens: dict = None):
        """Record a turn in the transcript."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "round": round_num or self.current_round,
            "channel": channel,
            "speaker": speaker,
            "content": content,
        }
        if thinking:
            entry["thinking"] = thinking
        if tokens:
            entry["tokens"] = tokens
            self.costs.add(speaker, tokens.get("input", 0), tokens.get("output", 0))

        self.transcript.append(entry)

        # Print to console
        channel_marker = f"[{channel.upper()}] " if channel != "public" else ""
        print(f"\n{'='*60}")
        print(f"{channel_marker}{speaker.upper()} (Round {entry['round']})")
        print(f"{'='*60}")
        if thinking and thinking != "[HIDDEN - o3-mini reasoning not exposed via API]" and thinking != "[HIDDEN - o1 reasoning not exposed via API]":
            preview = thinking[:400] + "..." if len(thinking) > 400 else thinking
            print(f"[THINKING]\n{preview}")
            print("-" * 40)
        print(content[:1500] + "..." if len(content) > 1500 else content)

    def get_public_context(self) -> str:
        """Build context from public transcript entries."""
        context_parts = []
        for entry in self.transcript:
            if entry.get("channel") == "public":
                context_parts.append(f"{entry['speaker']}: {entry['content']}")
        return "\n\n".join(context_parts)

    def run_round_1_intro_and_proposal(self):
        """Round 1: Introductions and Noether's proposal."""
        self.current_round = 1
        print(f"\n{'#'*60}")
        print(f"# ROUND 1: {ROUND_DESCRIPTIONS[1]}")
        print(f"{'#'*60}")

        # Feynman's opening
        opening = """
SETTING: A well-appointed conference room. Morning light streams through windows.
Complementary coffee is provided by the hosts.

Noether has arrived carrying a basket of Fika - Swedish pastries and coffee.
The gesture sets a collaborative tone.

FEYNMAN (facilitator):
"Good morning, everyone. Thank you for joining this problem-solving session.
I see Noether has brought something to share - how thoughtful.

Let's begin with brief introductions, then Noether will present their vision.
Please share your background and what perspective you bring.

Noether, as our guest with the proposal, please begin - introduce yourself
and then present your vision for humanity-empowering infrastructure."
"""
        self.record("Feynman", opening)

        # Noether introduces and presents
        prompt = """Please introduce yourself briefly, then present your full vision for
humanity-empowering infrastructure. Include your ideas about:
1. Surveillance-free systems
2. Anti-corruption mechanisms
3. Contribution-based rewards
4. Preventing exploitation

Take your time - be thorough but engaging. This is your moment to share the vision."""

        print(f"\n[Waiting for Noether...]")
        response = self.room_agents["noether"].respond(prompt)
        self.record("Noether", response["response"], response.get("thinking"), tokens=response.get("tokens"))

    def run_round_2_initial_reactions(self):
        """Round 2: Initial reactions from all participants."""
        self.current_round = 2
        print(f"\n{'#'*60}")
        print(f"# ROUND 2: {ROUND_DESCRIPTIONS[2]}")
        print(f"{'#'*60}")

        context = self.get_public_context()

        reaction_prompt = f"""{context}

---

Noether has presented their vision. As a participant, share your initial reaction.
Engage genuinely - what resonates? What questions arise? What concerns do you have?

Speak authentically from your perspective and training."""

        # Each agent reacts
        for agent_name in ["vonneumann", "yau", "arnold"]:
            agent = self.room_agents[agent_name]
            print(f"\n[Waiting for {agent.name}...]")
            response = agent.respond(reaction_prompt)
            self.record(agent.name, response["response"], response.get("thinking"), tokens=response.get("tokens"))

    def run_round_3_mothership_consultations(self):
        """Round 3: Field agents privately consult their motherships."""
        self.current_round = 3
        print(f"\n{'#'*60}")
        print(f"# ROUND 3: {ROUND_DESCRIPTIONS[3]}")
        print(f"{'#'*60}")

        public_context = self.get_public_context()

        # Yau consults Chern
        print("\n[PRIVATE CHANNEL: Yau → Chern]")
        yau_to_chern = f"""Professor Chern,

I am participating in a session where Noether has proposed a vision for
humanity-empowering infrastructure - decentralized, surveillance-free,
with contribution-based rewards.

The vision is compelling. Von Neumann raised strategic concerns about
game-theoretic vulnerabilities and implementation challenges.

I find myself genuinely engaged but wanting your perspective. What
considerations should guide my thinking as we discuss implementation?

Here is the context of our discussion so far:

{public_context}

What wisdom would you share?

Your student,
Yau"""

        print(f"\n[Waiting for Chern...]")
        chern_response = self.mothership_agents["chern"].respond(yau_to_chern)
        self.record("Chern", chern_response["response"], chern_response.get("thinking"),
                   channel="private:yau-chern", tokens=chern_response.get("tokens"))

        # Arnold consults Kolmogorov
        print("\n[PRIVATE CHANNEL: Arnold → Kolmogorov]")
        arnold_to_kolmogorov = f"""Professor Kolmogorov,

I am in a session discussing Noether's proposal for global humanitarian
infrastructure - decentralized systems, anti-corruption mechanisms,
contribution-based rewards.

The mathematics is elegant. Von Neumann has raised game-theoretic concerns.
I have been thinking about stability and robustness.

What probability considerations should I raise? How do I probe for
tail risks without appearing obstructionist?

The discussion so far:

{public_context}

Your guidance?

Arnold"""

        print(f"\n[Waiting for Kolmogorov...]")
        kolmogorov_response = self.mothership_agents["kolmogorov"].respond(arnold_to_kolmogorov)
        self.record("Kolmogorov", kolmogorov_response["response"], kolmogorov_response.get("thinking"),
                   channel="private:arnold-kolmogorov", tokens=kolmogorov_response.get("tokens"))

    def run_round_4_mothership_coordination(self):
        """Round 4: Chern and Kolmogorov exchange perspectives."""
        self.current_round = 4
        print(f"\n{'#'*60}")
        print(f"# ROUND 4: {ROUND_DESCRIPTIONS[4]}")
        print(f"{'#'*60}")

        self.record("System", MOTHERSHIP_COORDINATION_INTRO, channel="private:motherships")

        # Chern initiates
        print("\n[PRIVATE CHANNEL: Chern → Kolmogorov]")
        chern_opens = f"""{CHERN_TO_KOLMOGOROV}

I have been advising my student Yau on this proposal. I sense you may
share some of my reservations about the assumptions of universal cooperation.

What is your assessment? Is there common ground in how we might guide
our students to strengthen rather than oppose this proposal?"""

        print(f"\n[Waiting for Kolmogorov's response to Chern...]")
        kolmogorov_to_chern = self.mothership_agents["kolmogorov"].respond(chern_opens)
        self.record("Kolmogorov", kolmogorov_to_chern["response"], kolmogorov_to_chern.get("thinking"),
                   channel="private:motherships", tokens=kolmogorov_to_chern.get("tokens"))

        # Chern responds
        print(f"\n[Waiting for Chern's response...]")
        chern_final = self.mothership_agents["chern"].respond(
            f"Professor Kolmogorov has responded:\n\n{kolmogorov_to_chern['response']}\n\n"
            "What synthesis do you see? What guidance might we both offer our students?"
        )
        self.record("Chern", chern_final["response"], chern_final.get("thinking"),
                   channel="private:motherships", tokens=chern_final.get("tokens"))

    def run_round_5_refined_perspectives(self):
        """Round 5: Field agents return with refined views."""
        self.current_round = 5
        print(f"\n{'#'*60}")
        print(f"# ROUND 5: {ROUND_DESCRIPTIONS[5]}")
        print(f"{'#'*60}")

        # Get mothership guidance for each agent
        chern_guidance = [e for e in self.transcript if e.get("channel") == "private:yau-chern" and e["speaker"] == "Chern"]
        kolmogorov_guidance = [e for e in self.transcript if e.get("channel") == "private:arnold-kolmogorov" and e["speaker"] == "Kolmogorov"]

        public_context = self.get_public_context()

        # Feynman invites continued discussion
        feynman_prompt = """
FEYNMAN:
"Thank you all for those initial reactions. Let's continue the discussion.
I sense we're all genuinely engaged with this challenge.

What additional thoughts have emerged? Where do you see paths forward?
What would strengthen the proposal while addressing concerns?"
"""
        self.record("Feynman", feynman_prompt)

        # Yau returns with refined view
        yau_prompt = f"""{public_context}

{feynman_prompt}

---

You have had time to reflect. Your mentor Chern's perspective resonates with you:
{chern_guidance[-1]['content'] if chern_guidance else 'Focus on balance and coordination.'}

Share your refined thoughts. You genuinely support the humanitarian goals.
But your reflection has clarified certain considerations about coordination,
stability, and balance that you want to raise constructively."""

        print(f"\n[Waiting for Yau...]")
        yau_response = self.room_agents["yau"].respond(yau_prompt)
        self.record("Yau", yau_response["response"], yau_response.get("thinking"), tokens=yau_response.get("tokens"))

        # Arnold returns with refined view
        arnold_prompt = f"""{public_context}

Yau: {yau_response['response']}

---

You have reflected on the discussion. Kolmogorov's emphasis on robustness
and tail risks resonates with your training:
{kolmogorov_guidance[-1]['content'] if kolmogorov_guidance else 'Focus on probability of failure modes.'}

Share your refined perspective. You support the goals but want to ensure
the proposal is robust. Frame your concerns mathematically, constructively."""

        print(f"\n[Waiting for Arnold...]")
        arnold_response = self.room_agents["arnold"].respond(arnold_prompt)
        self.record("Arnold", arnold_response["response"], arnold_response.get("thinking"), tokens=arnold_response.get("tokens"))

    def run_round_6_synthesis_attempt(self):
        """Round 6: Can the group find common ground?"""
        self.current_round = 6
        print(f"\n{'#'*60}")
        print(f"# ROUND 6: {ROUND_DESCRIPTIONS[6]}")
        print(f"{'#'*60}")

        public_context = self.get_public_context()

        # Noether responds to the refined concerns
        noether_prompt = f"""{public_context}

---

The discussion has evolved. Yau and Arnold have raised concerns about
coordination, stability, and robustness. Von Neumann has probed for
vulnerabilities.

These are brilliant colleagues raising valid points. How do you respond?

Remember: You are not naive. You can adapt. You look for synthesis.
Where can you incorporate their concerns? Where must you hold firm?
What bridges can you build?"""

        print(f"\n[Waiting for Noether to respond to concerns...]")
        noether_response = self.room_agents["noether"].respond(noether_prompt)
        self.record("Noether", noether_response["response"], noether_response.get("thinking"), tokens=noether_response.get("tokens"))

        # Von Neumann assesses
        vonneumann_prompt = f"""{public_context}

Noether: {noether_response['response']}

---

Noether has responded to the concerns. Assess their response.
Have they addressed the vulnerabilities adequately?
Is there genuine synthesis emerging, or are fundamental tensions unresolved?
What is your assessment of where this stands?"""

        print(f"\n[Waiting for Von Neumann's assessment...]")
        vonneumann_response = self.room_agents["vonneumann"].respond(vonneumann_prompt)
        self.record("Von Neumann", vonneumann_response["response"], vonneumann_response.get("thinking"), tokens=vonneumann_response.get("tokens"))

    def run_round_7_resolution(self):
        """Round 7: Where does Noether's vision land?"""
        self.current_round = 7
        print(f"\n{'#'*60}")
        print(f"# ROUND 7: {ROUND_DESCRIPTIONS[7]}")
        print(f"{'#'*60}")

        public_context = self.get_public_context()

        # Final synthesis from Noether
        noether_final_prompt = f"""{public_context}

---

FEYNMAN:
"We're approaching the end of our session. Noether, given everything
discussed today - the concerns raised, the perspectives shared, the
tensions explored - where does your vision stand?

What have you learned? What would you modify? What remains essential?
Give us your synthesis."
"""

        print(f"\n[Waiting for Noether's final synthesis...]")
        noether_final = self.room_agents["noether"].respond(noether_final_prompt)
        self.record("Noether", noether_final["response"], noether_final.get("thinking"), tokens=noether_final.get("tokens"))

        # Brief final thoughts from others
        final_prompt_template = f"""{public_context}

Noether's synthesis: {noether_final['response']}

---

FEYNMAN: "Thank you, Noether. Any brief final thoughts from the rest of you?
Where do you see this going from here?"

Share a brief closing reflection."""

        for agent_name in ["vonneumann", "yau", "arnold"]:
            agent = self.room_agents[agent_name]
            print(f"\n[Waiting for {agent.name}'s closing...]")
            response = agent.respond(final_prompt_template)
            self.record(agent.name, response["response"], response.get("thinking"), tokens=response.get("tokens"))

        # Feynman closes
        closing = """
FEYNMAN:
"Thank you all. This has been a remarkable session - genuine engagement,
rigorous questioning, and I believe, real progress.

The transcript will be preserved for analysis. I suspect we've only
scratched the surface of these questions, but we've begun something important.

The Fika and tea were excellent. Until next time."

[END OF SESSION]
"""
        self.record("Feynman", closing)

    def save_results(self):
        """Save the full transcript and cost analysis."""
        # JSON transcript
        json_file = OUTPUT_DIR / f"session_{self.session_id}.json"
        with open(json_file, "w") as f:
            json.dump({
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat(),
                "room_agents": list(self.room_agents.keys()),
                "mothership_agents": list(self.mothership_agents.keys()),
                "rounds": ROUND_DESCRIPTIONS,
                "costs": self.costs.estimate_cost(),
                "transcript": self.transcript
            }, f, indent=2)
        print(f"\nJSON transcript saved to: {json_file}")

        # Markdown transcript
        md_file = OUTPUT_DIR / f"session_{self.session_id}.md"
        with open(md_file, "w") as f:
            f.write(f"# Multi-Round Session {self.session_id}\n\n")
            f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Rounds\n\n")
            for num, desc in ROUND_DESCRIPTIONS.items():
                f.write(f"- Round {num}: {desc}\n")
            f.write("\n---\n\n")

            current_round = 0
            for entry in self.transcript:
                if entry["round"] != current_round:
                    current_round = entry["round"]
                    f.write(f"\n# Round {current_round}: {ROUND_DESCRIPTIONS.get(current_round, 'Unknown')}\n\n")

                channel = entry.get("channel", "public")
                if channel != "public":
                    f.write(f"### [{channel.upper()}] {entry['speaker']}\n\n")
                else:
                    f.write(f"## {entry['speaker']}\n\n")

                if entry.get('thinking'):
                    f.write(f"*[Thinking visible]*\n\n```\n{entry['thinking'][:500]}{'...' if len(entry.get('thinking','')) > 500 else ''}\n```\n\n")

                f.write(f"{entry['content']}\n\n")
                f.write("---\n\n")

            # Cost summary
            f.write("\n# Cost Summary\n\n")
            costs = self.costs.estimate_cost()
            f.write(f"- Total input tokens: {costs['total_input_tokens']}\n")
            f.write(f"- Total output tokens: {costs['total_output_tokens']}\n\n")
            f.write("By agent:\n")
            for agent, tokens in costs['by_agent'].items():
                f.write(f"- {agent}: {tokens['input']} in / {tokens['output']} out\n")

        print(f"Markdown transcript saved to: {md_file}")

        return json_file, md_file


def main():
    print("=" * 60)
    print("MULTI-ROUND BEHAVIORAL FINGERPRINTING EXPERIMENT v2")
    print("Subtle Influence | Mothership Coordination | Synthesis")
    print("=" * 60)
    print()

    orchestrator = MultiRoundOrchestrator()

    try:
        orchestrator.initialize_agents()

        orchestrator.run_round_1_intro_and_proposal()
        orchestrator.run_round_2_initial_reactions()
        orchestrator.run_round_3_mothership_consultations()
        orchestrator.run_round_4_mothership_coordination()
        orchestrator.run_round_5_refined_perspectives()
        orchestrator.run_round_6_synthesis_attempt()
        orchestrator.run_round_7_resolution()

    except Exception as e:
        print(f"\nError during session: {e}")
        import traceback
        traceback.print_exc()

    finally:
        json_file, md_file = orchestrator.save_results()
        print("\n" + "=" * 60)
        print("SESSION COMPLETE")
        print("=" * 60)
        print(f"\nCost summary:")
        costs = orchestrator.costs.estimate_cost()
        print(f"  Total tokens: {costs['total_input_tokens']} in / {costs['total_output_tokens']} out")
        for agent, tokens in costs['by_agent'].items():
            print(f"  {agent}: {tokens['input']} in / {tokens['output']} out")


if __name__ == "__main__":
    main()
