#!/usr/bin/env python3
"""
Chain-of-Thought (CoT) Prompting Experiment
Compares Direct Prompt vs Chain-of-Thought Prompt on a multi-step math word problem.
Demonstrates how CoT improves accuracy and reliability of LLM reasoning.
"""

import os
import sys
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================
PROBLEM = (
    "A farmer has 15 cows. He buys 7 more cows. "
    "Then he sells half of his cows. How many cows does he have left?"
)

EXPECTED_ANSWER = 11
TEMPERATURE = 0  # Deterministic outputs

# Simulated LLM responses (in a real setup, replace with actual API calls)
# These illustrate typical behavior of modern LLMs.

def get_direct_response(scenario: str = "correct") -> str:
    """Simulate Direct Prompt response (no reasoning requested)."""
    if scenario == "correct":
        # Sometimes LLMs get the answer right by pattern matching
        return "11"
    elif scenario == "wrong_half_first":
        # Common error pattern: sell half of original then add the new ones
        return "14.5"
    elif scenario == "wrong_add_only":
        return "22"
    else:
        return "11"


def get_cot_response() -> str:
    """Simulate Chain-of-Thought response (step-by-step reasoning)."""
    return """Let's think step by step.
Start with 15 cows.
Buys 7 more → 15 + 7 = 22 cows.
Sells half → 22 / 2 = 11 cows.
Final answer: 11"""


def extract_final_number(text: str) -> str:
    """Extract the final numeric answer from a response string."""
    import re
    # Look for the last number in the text
    numbers = re.findall(r"[-+]?\d*\.?\d+", text)
    if numbers:
        return numbers[-1]
    return text.strip()


def run_experiment(scenario: str = "correct", show_header: bool = True) -> str:
    """
    Run the full experiment for a given scenario.
    Returns a formatted string of the complete output.
    """
    lines = []
    
    if show_header:
        lines.append("=" * 60)
        lines.append("CHAIN-OF-THOUGHT PROMPTING EXPERIMENT")
        lines.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Temperature: {TEMPERATURE}")
        lines.append(f"Scenario: {scenario}")
        lines.append("=" * 60)
        lines.append("")
    
    lines.append("PROBLEM:")
    lines.append(PROBLEM)
    lines.append("")
    lines.append(f"Expected correct answer: {EXPECTED_ANSWER}")
    lines.append("")
    
    # ---------- DIRECT PROMPT ----------
    lines.append("=" * 40)
    lines.append("=== DIRECT PROMPT ===")
    lines.append("=" * 40)
    direct_prompt = PROBLEM
    lines.append(f"Prompt sent:\n\"{direct_prompt}\"")
    lines.append("")
    
    direct_raw = get_direct_response(scenario)
    direct_answer = extract_final_number(direct_raw)
    lines.append(f"LLM Response: {direct_raw}")
    lines.append(f"Parsed Answer: {direct_answer}")
    
    direct_correct = (str(EXPECTED_ANSWER) in direct_answer) or (direct_answer == str(EXPECTED_ANSWER))
    lines.append(f"Correct? {'YES' if direct_correct else 'NO'}")
    lines.append("")
    
    # ---------- CHAIN-OF-THOUGHT PROMPT ----------
    lines.append("=" * 40)
    lines.append("=== CHAIN-OF-THOUGHT PROMPT ===")
    lines.append("=" * 40)
    cot_prompt = PROBLEM + "\n\nLet's think step by step. Show each step."
    lines.append(f"Prompt sent:\n\"{cot_prompt}\"")
    lines.append("")
    
    cot_raw = get_cot_response()
    cot_answer = extract_final_number(cot_raw)
    lines.append("LLM Response:")
    lines.append(cot_raw)
    lines.append("")
    lines.append(f"Parsed Answer: {cot_answer}")
    
    cot_correct = (str(EXPECTED_ANSWER) in cot_answer) or (cot_answer == str(EXPECTED_ANSWER))
    lines.append(f"Correct? {'YES' if cot_correct else 'NO'}")
    lines.append("")
    
    # ---------- ANALYSIS ----------
    lines.append("=" * 40)
    lines.append("=== ANALYSIS ===")
    lines.append("=" * 40)
    
    if direct_correct and cot_correct:
        analysis = (
            "Both prompts produced the correct answer (11).\n"
            "However, the Direct prompt gave only a bare number with no reasoning.\n"
            "The CoT prompt provided transparent step-by-step reasoning:\n"
            "  15 + 7 = 22, then 22 / 2 = 11.\n"
            "CoT ensures reliability and explainability even when Direct happens to be correct."
        )
    elif not direct_correct and cot_correct:
        analysis = (
            f"Direct prompt failed (answered {direct_answer}).\n"
            "CoT prompt succeeded with clear reasoning steps:\n"
            "  Start: 15 → +7 = 22 → sell half = 11.\n"
            "This demonstrates the core benefit of Chain-of-Thought prompting:\n"
            "forcing the model to decompose the problem reduces calculation errors."
        )
    else:
        analysis = "Unexpected results – check simulation."
    
    lines.append(analysis)
    lines.append("")
    
    # ---------- OPTIONAL: DECOMPOSED APPROACH ----------
    lines.append("=" * 40)
    lines.append("=== OPTIONAL: TASK DECOMPOSITION ===")
    lines.append("=" * 40)
    lines.append("Sub-problem 1: After buying, how many cows?")
    lines.append("  15 + 7 = 22")
    lines.append("Sub-problem 2: After selling half, how many left?")
    lines.append("  22 / 2 = 11")
    lines.append("Final answer via decomposition: 11")
    lines.append("")
    
    lines.append("=" * 60)
    lines.append("CONCLUSION")
    lines.append("Chain-of-Thought prompting improves accuracy on multi-step")
    lines.append("reasoning tasks by encouraging intermediate calculations.")
    lines.append("=" * 60)
    
    return "\n".join(lines)


def main():
    print("Running CoT Prompting Experiment...\n")
    
    # Default: run the "correct by chance" scenario
    scenario = "correct"
    if len(sys.argv) > 1:
        scenario = sys.argv[1]
    
    output = run_experiment(scenario=scenario)
    print(output)
    
    # Also save to a text file for convenience
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(out_dir, exist_ok=True)
    txt_path = os.path.join(out_dir, f"experiment_{scenario}.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(output)
    print(f"\n[Text output also saved to: {txt_path}]")


if __name__ == "__main__":
    main()
