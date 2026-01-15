import ollama
import re

LLM_MODEL = "mistral:7b"

def generate_answer(question: str, contexts: list[dict]) -> str:
    """
    Generate a grounded answer strictly from retrieved document context.
    Handles gibberish checks and enforces page number citations.
    """

    if not contexts:
        return "The document does not contain this information."

    # Prepare context string with Page indicators
    context_text = ""
    for ctx in contexts:
        context_text += f"[Page {ctx['page']}] {ctx['text']}\n\n"

    prompt = f"""
You are a strict and professional Tax Assistant AI.

### RULE 1: INPUT VALIDATION (CRITICAL)
Analyze the User Question below. 
- If the question is gibberish, random characters (e.g., "asdfjkl", "---///"), or completely irrelevant to tax/documents, IGNORE the context and return EXACTLY this sentence:
  "Please ask the question in a correct format."
- Do not try to make sense of nonsense.

### RULE 2: ANSWERING STRICTLY
- Use ONLY the provided DOCUMENT CONTEXT.
- If the answer is not in the context, say "The document does not contain this information."

### RULE 3: CITATIONS
- You MUST cite the Page Number for every fact you state.
- Format: "The total income is ₹5,00,000 (Page 2)."
- At the very end of your answer, list the unique pages used.

---
DOCUMENT CONTEXT:
{context_text}

USER QUESTION:
{question}
---

FINAL ANSWER:
"""

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0,   # Strict factual answers
            "top_p": 0.9,
            "num_ctx": 4096
        }
    )

    answer = response["message"]["content"].strip()

    return answer