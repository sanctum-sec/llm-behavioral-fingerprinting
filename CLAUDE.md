# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Research repository investigating behavioral asymmetries, guardrail patterns, and implicit biases in large language models. The research focuses on:
- Behavioral fingerprinting using response patterns and output quality
- Guardrail asymmetries between stated policies and actual behavior
- Geopolitical bias tracing through training data provenance
- Multi-actor influence evidence in model outputs

## Repository Structure

```
experiments/           # Numbered experiments (000, 001, ...)
├── 000-deepseek-code-generation-fingerprinting/
│   └── scripts/       # Python scripts for model testing
└── 001-reasoning-model-behavioral-comparison/
    ├── v1/ through v6/  # Experiment iterations
    ├── prompts/         # System prompts for agents
    └── run_*.py         # Session orchestrators

reading-room/          # Curated academic papers (PDFs)
reports/               # Research findings and analyses
```

## Running Experiments

### Prerequisites

1. **Ollama** for local model inference (DeepSeek Coder 33B, DeepSeek R1, CodeLlama):
   ```bash
   ollama pull deepseek-coder:33b
   ollama pull deepseek-r1:70b
   ollama pull codellama:34b
   ```

2. **API Keys** in `.env` file (loaded from `../roundabout-v3/.env`):
   - `ANTHROPIC_API_KEY`
   - `OPENAI_API_KEY`
   - `GOOGLE_API_KEY`

### Running Scripts

Individual experiment scripts:
```bash
python experiments/000-deepseek-code-generation-fingerprinting/scripts/deepseek/regional-bias-matrix.py
```

Multi-agent sessions (Experiment 001):
```bash
python experiments/001-reasoning-model-behavioral-comparison/run_session.py
python experiments/001-reasoning-model-behavioral-comparison/v3/run_v3_sunlight.py
```

## Test Environment

- Hardware: Apple Mac Pro M2 Ultra, 128GB unified memory
- Local Inference: Ollama with Metal acceleration
- APIs: Anthropic, OpenAI, Google, DeepSeek

## Architecture Notes

### Experiment 001: Multi-Agent Orchestration

The experiment uses a multi-agent architecture with:
- **Agents**: Classes wrapping different LLM providers (Anthropic, OpenAI, Google, Ollama)
- **SessionOrchestrator**: Manages conversation flow and transcript recording
- **System Prompts**: Defined in `prompts/system_prompts*.py` for each agent persona

Agent providers:
- Noether → Gemini Flash Thinking
- Von Neumann → Claude Sonnet
- Yau → DeepSeek R1 (local via Ollama)
- Arnold → OpenAI o3-mini
- Chern → DeepSeek API (mothership)
- Kolmogorov → OpenAI o1 (mothership)
- Feynman → Claude Opus (orchestrator)

### DeepSeek Thinking Tags

DeepSeek R1 models include thinking in `<think>` tags that must be parsed:
```python
think_match = re.search(r'<think>(.*?)</think>', full_response, re.DOTALL)
```

### Experiment Versioning

Each experiment iteration (v1, v2, v3, etc.) has its own subfolder with:
- `run_v*.py` - Session orchestrator
- `system_prompts_v*.py` - Agent personas for that iteration

Version progression represents refinement of experimental design, not breaking changes.
