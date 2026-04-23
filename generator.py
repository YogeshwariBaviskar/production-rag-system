from openai import OpenAI

client = OpenAI()

def generate_answer(query, docs):
    context = ""

    for i, doc in enumerate(docs):
        context += f"[Doc{i+1}] {doc}\n\n"

    prompt = f"""
Answer the question using ONLY the documents.

Provide citations like [Doc1].

Question:
{query}

Documents:
{context}
"""

    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[{"role":"user","content":prompt}],
        temperature=1
    )

    return response.choices[0].message.content