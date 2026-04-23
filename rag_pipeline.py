from retriever import HybridRetriever
from reranker import Reranker
from query_rewriter import rewrite_query
from generator import generate_answer
from cache import get_cache, set_cache
from utils import compress_docs

class ProductionRAG:

    def __init__(self):
        self.retriever = HybridRetriever()
        self.reranker = Reranker()

    def ask(self, query):
        cached = get_cache(query)
        if cached:
            return cached

        # 1 rewrite query
        rewritten = rewrite_query(query)

        # 2 retrieve docs
        candidates = self.retriever.hybrid_search(rewritten)

        # 3 rerank
        top_docs = self.reranker.rerank(rewritten, candidates)

        # 4 compress context
        docs = compress_docs(top_docs)

        # 5 generate answer
        answer = generate_answer(query, docs)

        set_cache(query, answer)

        return answer


if __name__ == "__main__":
    rag = ProductionRAG()

    while True:
        q = input("\nAsk: ")
        ans = rag.ask(q)
        print("\nAnswer:\n", ans)