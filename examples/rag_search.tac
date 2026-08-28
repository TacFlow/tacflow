flow rag_search {
    // Hybrid search across all 3 memory tiers (BM25 + Vector + Graph)
    // Demonstrates Trust Type escalation: @user → @verified

    trigger: on_query

    step search_lexical {
        description: "Tier 1 — Exact term search via BM25"
        input: @user query
        action: memory.bm25_search("{{query}}")
        output: @verified lexical_results
    }

    step search_semantic {
        description: "Tier 2 — Semantic similarity via HNSW vector index"
        input: @user query
        action: memory.vector_search("{{query}}")
        output: @verified vector_results
    }

    step search_graph {
        description: "Tier 3 — Relational search via knowledge graph"
        input: @user query
        action: memory.graph_search("{{query}}")
        output: @verified graph_results
    }

    step fuse_results {
        description: "Fuse all 3 tiers using Reciprocal Rank Fusion"
        input: @verified lexical_results, @verified vector_results, @verified graph_results
        action: memory.rrf_fuse([lexical_results, vector_results, graph_results])
        output: @verified fused_results
    }

    step validate_sources {
        description: "Validate provenance of each result before presenting"
        input: @verified fused_results
        action: trust.validate_source("{{fused_results}}")
        output: @verified validated_results
    }

    step generate_answer {
        description: "Generate final answer using validated context only"
        input: @verified validated_results
        action: llm.generate("Answer the query using ONLY the provided context: {{validated_results}}")
        output: @inferred answer
    }

    step respond {
        description: "Send answer with source citations"
        input: @inferred answer
        action: message.send("{{answer}}")
    }
}
