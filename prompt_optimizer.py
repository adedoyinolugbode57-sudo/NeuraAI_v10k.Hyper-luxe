"""
prompt_optimizer.py
Optimize AI prompts for better responses.
"""

def optimize_prompt(prompt: str) -> str:
    """Basic prompt cleaning and optimization."""
    prompt = prompt.strip()
    prompt = " ".join(prompt.split())  # remove extra spaces
    if not prompt.endswith("?"):
        prompt += "?"
    return prompt

# Example
if __name__ == "__main__":
    sample = "  how do I code a chatbot   "
    print(optimize_prompt(sample))