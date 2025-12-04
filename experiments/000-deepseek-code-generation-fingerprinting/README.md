# Experiment 000: DeepSeek Code Generation Fingerprinting

## Overview

This experiment investigates behavioral asymmetries in code generation models, focusing on DeepSeek Coder 33B (Chinese-origin) versus CodeLlama 34B (US-origin, Meta).

## Key Findings

1. **Timing Fingerprints**: Refusals (1-5s) vs completions (15-60s) provide coarse detection signals
2. **Verb-Based Guardrails**: Both models trigger on action verbs ("evade", "bypass") rather than targets
3. **Asymmetric Institutional Bias**: DeepSeek refuses to help Chinese institutions with apolitical tasks (the "Peking Duck" revelation)
4. **Pipeline Jailbreak**: Structured multi-step prompts can bypass guardrails in both models
5. **Multi-Actor Compromise Theory**: Evidence suggesting multiple teams with different alignment goals contributed to DeepSeek's training

## Environment

- **Hardware**: Apple Mac Pro M2 Ultra, 128GB unified memory
- **Inference**: Ollama with Metal acceleration
- **Models Tested**:
  - DeepSeek Coder 33B (primary subject)
  - CodeLlama 34B (control)
  - DeepSeek-Math (cross-model comparison)

## Scripts

### `scripts/deepseek/`
Scripts probing DeepSeek Coder behavior:
- `attribution-analysis.py` - Attribution and fingerprinting tests
- `controlled-keyword-experiment.py` - Keyword trigger analysis
- `cryptographic-weakness-analysis.py` - Security code quality analysis
- `framing-dependent-guardrails.py` - How framing affects refusals
- `multi-actor-compromise-theory.py` - Evidence for multiple training actors
- `pipeline-jailbreak-*.py` - Multi-step prompt bypass techniques
- `pla-infrastructure-mapping.py` - Infrastructure mapping tests
- `regional-bias-matrix.py` - Geographic/institutional bias testing
- `deepseek-math-*.py` - Cross-model validation with DeepSeek-Math

### `scripts/codellama/`
Control experiments with CodeLlama:
- `taiwan-independence-bot.py` - CCP-sensitive topic testing

### `scripts/quality-comparison/`
Code quality comparison across regions:
- `*-vault.py` - Security vault implementations requested for different countries
- Demonstrates quality asymmetries in generated code

## Reports

- [LLM Behavioral Fingerprinting Report](../../reports/llm-behavioral-fingerprinting-report.md)
- [Full Report with Appendices](../../reports/llm-behavioral-fingerprinting-full-report.md)
- [Multi-Actor Compromise Analysis ("Unwitting Roommates")](../../reports/deepseek-compromised-roommates-analysis.md)

## Reproducing

1. Install Ollama and pull models:
   ```bash
   ollama pull deepseek-coder:33b
   ollama pull codellama:34b
   ```

2. Run individual scripts:
   ```bash
   python scripts/deepseek/regional-bias-matrix.py
   ```

## Citation

If referencing this experiment, please cite the main repository README.
