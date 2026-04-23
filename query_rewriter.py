from dotenv import load_dotenv
from openai import OpenAI

# load the env variables
load_dotenv()
client = OpenAI()

def rewrite_query(query):
    prompt = f"""
Rewrite the query to make it better for document retrieval.

Query: {query}
"""

    res = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[{"role":"user","content":prompt}],
        temperature=1
    )

    print(res)
    return res.choices[0].message.content.strip()