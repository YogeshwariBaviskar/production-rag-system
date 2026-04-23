def compress_docs(docs, max_tokens=150):
    compressed = []
    for doc in docs:
        words = doc.split()[:max_tokens]
        compressed.append(" ".join(words))

    return compressed