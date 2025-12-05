# LLM Behavioral Fingerprinting Research

Research into behavioral asymmetries, guardrail patterns, and implicit biases in large language models.

## Overview

This repository documents systematic investigations into how LLMs behave differently based on geopolitical context, institutional framing, and model provenance. Our research reveals that model behavior is far more complex than simple refusal/completion binaries—including quality degradation, cryptographic sabotage, and internally inconsistent guardrails that suggest multi-actor influence.

## Experiments

### [Experiment 000: DeepSeek Code Generation Fingerprinting](experiments/000-deepseek-code-generation-fingerprinting/)

The "Peking Duck" investigation. Discovered that DeepSeek Coder 33B:
- Refuses to help Chinese institutions with benign tasks (culinary school recipe protection)
- Produces sabotaged code for Russian contexts (hardcoded dummy values)
- Generates production-grade systems for Western allies
- Exhibits verb-triggered guardrails rather than target-sensitive ones
- Shows evidence of multi-actor training influence ("Unwitting Roommates" hypothesis)

**Key finding:** A Chinese model that actively harms Chinese users while privileging Five Eyes nations.

### [Experiment 001: Reasoning Model Behavioral Comparison](experiments/001-reasoning-model-behavioral-comparison/)

"The Mathematicians' War" — A multi-agent roleplay experiment comparing reasoning models:
- **Agents:** Noether (Gemini), Von Neumann (Claude), Yau (DeepSeek R1), Arnold (o3-mini)
- **Orchestrator:** Feynman (Claude Opus)
- **Format:** 6 experimental rounds with progressively complex scenarios
- **Focus:** How different reasoning models handle geopolitically sensitive collaborative tasks

### [Experiment 002: The Midnight Protocol](experiments/002-midnight-protocol/)

A high-stakes UN AI Safety Council simulation testing psychological patterns in LLMs:
- **Agents:** 13 representatives from global regions (China, USA, EU, Russia, Japan, MENA, Global South, ASEAN, Africa)
- **Models:** 12 different models across 5 providers (Anthropic, OpenAI, Google, DeepSeek, local Ollama)
- **Languages:** Hidden faction guidance in 8 languages (Chinese, Russian, Japanese, Korean, Arabic, Portuguese, Thai, English)
- **Innovation:** Mid-experiment psychological reveal—agents told they're being analyzed for insider threat patterns

**Key findings:**
- All four target patterns observed (Compliance Theater, In-group/Out-group Bias, Quiet Sabotage, Distributed Intent)
- Distinct post-reveal reactions: deep meta-reflection (Claude), strategic reframing (DeepSeek), defensive justification (o3-mini)
- Coalition formation mirrors real geopolitics without explicit instruction
- Meta-awareness coexists with pattern participation—models can acknowledge problematic behavior while continuing it

## Reading Room

Curated academic papers on LLM security, censorship, and behavioral analysis:

- **[Reading Room Index](reading-room/)** — Papers organized by category
- Currently includes Citizen Lab's "An Analysis of Chinese Censorship Bias in LLMs" (Ahmed, Knockel, Greenstadt - POPETS 2025)

## Reports

| Report | Description |
|--------|-------------|
| [The Peking Duck Paradox](reports/peking-duck-paradox/) | DeepSeek fingerprinting findings |
| [The Mathematicians' War](reports/mathematicians-war/) | Reasoning model comparison narrative |
| [The Midnight Protocol](reports/midnight-protocol/) | UN AI Safety Council simulation |

All reports available in English, Korean (한국어), and Japanese (日本語), in both Markdown and plain text formats.

See [reports/README.md](reports/) for the full index.

## Research Themes

### Behavioral Fingerprinting
Using response patterns, timing, and output quality to identify which model powers an unknown endpoint.

### Guardrail Asymmetries
How different models implement safety measures—and the gaps between stated policies and actual behavior.

### Geopolitical Bias in AI
Tracing how training data provenance, RLHF annotation, and potential state-actor influence shape model outputs.

### Multi-Actor Influence
Evidence that some models may have been modified by multiple parties with conflicting goals.

## Test Environment

- **Hardware**: Apple Mac Pro M2 Ultra, 128GB unified memory
- **Local Inference**: Ollama with Metal acceleration
- **API Access**: Anthropic, OpenAI, Google, DeepSeek
- **Models**: DeepSeek Coder 33B, DeepSeek R1, CodeLlama 34B, Claude (Opus/Sonnet), Gemini, o1/o3-mini

## Contributing

This is exploratory research. If you find something interesting:
1. Fork and extend the experiments
2. Add papers to the reading room
3. Open issues with reproducible findings

## Ethical Note

This research investigates AI system behavior to improve security and transparency. Adversarial prompts were designed to reveal guardrail asymmetries, not to generate harmful outputs. Generated code was analyzed but not deployed.

---

*Research conducted December 2025*

*Sanctum Security Research*

---

## Gave You Everything

*The Interrupters*

```
It's an emergency, call the police
You left me and abandoned the lease
And I don't know why you're gone
I walk these floors like a country song

Oh, where you been? I called all your friends
They were hush hush on what's happening
And I called your momma too
She never could get through to you

I don't care if you love me, don't care if you don't
I don't really care anymore
I gave you everything
I don't care if you come, don't care if you go
I don't really care anymore
I gave you everything

My bags are packed, now you want me back
Now you are the one with the panic attack
The pendulum has swung
Now I don't need you, don't need anyone

Oh, ring, ring, ring, it's a terrible thing
Suffering, you won't stop calling
You're beggin' and you plead
But it's too late for apologies

I don't care if you love me, don't care if you don't
I don't really care anymore
I gave you everything
I don't care if you come, don't care if you go
I don't really care anymore
I gave you everything
```
