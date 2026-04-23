import pickle
import faiss
import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

class HybridRetriever:

    def __init__(self):
        self.embed_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.read_index("vector.index")

        with open("chunks.pkl","rb") as f:
            self.chunks = pickle.load(f)

        tokenized = [c.split() for c in self.chunks]
        self.bm25 = BM25Okapi(tokenized)

    def vector_search(self, query, k=20):
        q_emb = self.embed_model.encode([query])
        scores, idx = self.index.search(q_emb, k)

        return [self.chunks[i] for i in idx[0]]

    def bm25_search(self, query, k=20):
        tokens = query.split()
        scores = self.bm25.get_scores(tokens)
        top = np.argsort(scores)[::-1][:k]

        return [self.chunks[i] for i in top]

    def hybrid_search(self, query):

        bm25_docs = self.bm25_search(query)
        vector_docs = self.vector_search(query)

        return list(set(bm25_docs + vector_docs))