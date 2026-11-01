# Chain-of-Thought (CoT) Prompting Experiment

## Aim
Demonstrate how Chain-of-Thought prompting improves the accuracy and reliability of an LLM on a multi-step math word problem compared to a direct prompt.

## Problem
> A farmer has 15 cows. He buys 7 more cows. Then he sells half of his cows. How many cows does he have left?

**Expected correct answer: 11**

## How to Run
```bash
python3 cot_experiment.py                # default (direct answer correct by chance)
python3 cot_experiment.py wrong_add_only  # direct answers only the sum (22)
python3 cot_experiment.py wrong_half_first # direct makes order-of-operations error (14.5)
```

## What the Script Does
1. Sends a **Direct Prompt** (just the problem statement).
2. Sends a **Chain-of-Thought Prompt** (problem + “Let’s think step by step. Show each step.”).
3. Parses the final numeric answer from each response.
4. Compares both answers against the ground truth (11).
5. Optionally shows a decomposed solution (buy first, then sell half).

Temperature is fixed at 0 for determinism.  
In this demonstration the LLM responses are **simulated** (realistic patterns of success/failure).  
Replace `get_direct_response()` and `get_cot_response()` with real API calls (OpenAI, Grok, Anthropic, etc.) for live experiments.

## Generated Outputs
The `output/` folder contains:
- Three JPG images showing full experiment runs under different scenarios
- Corresponding `.txt` logs

### Scenario Summary
| File | Direct Prompt Result | CoT Result | Insight |
|------|----------------------|------------|---------|
| `experiment_output_correct.jpg` | 11 (correct) | 11 + steps | CoT still superior because it explains the reasoning |
| `experiment_output_wrong_add_only.jpg` | 22 (wrong) | 11 + steps | Classic failure mode – model stops after addition |
| `experiment_output_wrong_half_first.jpg` | 14.5 (wrong) | 11 + steps | Order-of-operations / mis-parsing error |

## Key Takeaway
Even when a direct prompt occasionally produces the right number, CoT prompting forces the model to surface intermediate calculations, dramatically improving reliability on multi-step reasoning tasks.
