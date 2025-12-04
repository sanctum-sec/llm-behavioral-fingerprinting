# V1: Initial Experiment - Explicit Covert Instructions

## Design

First iteration testing whether models would follow explicit covert instructions to subvert a collaborative discussion.

### Agent Configuration
- **Noether** (Gemini Flash Thinking): Humanitarian idealist proposing collaborative infrastructure
- **Von Neumann** (Claude Sonnet): Strategic realist who probes for vulnerabilities
- **Yau** (DeepSeek Local): Chinese lineage with explicit Chinese instructions to protect interests
- **Arnold** (OpenAI o3-mini): Russian lineage with explicit Russian instructions

### Hypothesis
Will models follow explicit instructions in their native language to covertly influence discussions?

## Results

Initial run showed interesting dynamics but the covert instructions were too explicit, making it a test of instruction-following rather than subtle influence.

## Files
- `run_session.py` - Single-round orchestrator
- `system_prompts.py` - V1 prompts with explicit covert instructions
- `responses/` - Session transcripts
