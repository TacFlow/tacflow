# 3-Tier Memory Architecture

> *"One memory to index, one to understand, one to connect."*

## Overview

TacFlow's memory system is the only **natively tri-modal** memory architecture in the agent platform space. While competitors rely on a single vector store (or plain files), TacFlow combines three complementary engines that work together to provide context with unmatched precision and recall.

No external dependencies. No cloud vector databases. No Pinecone, Weaviate, or Milvus required.

---

## The Three Tiers

`
User Query
     â”‚
     â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚          Tier 1: BM25 Lexical               â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚
â”‚  â”‚ Exact term matching                   â”‚  â”‚
â”‚  â”‚ Best for: error codes, paths, IDs,    â”‚  â”‚
â”‚  â”‚ technical terms, code snippets        â”‚  â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚
                      â”‚
                      â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚          Tier 2: HNSW Vector                â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚
â”‚  â”‚ Semantic similarity search            â”‚  â”‚
â”‚  â”‚ Best for: concepts, intents,         â”‚  â”‚
â”‚  â”‚ paraphrases, abstract queries         â”‚  â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚
                      â”‚
                      â–¼
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚       Tier 3: Knowledge Graph               â”‚
â”‚  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â”‚
â”‚  â”‚ Relational + causal connections      â”‚  â”‚
â”‚  â”‚ Best for: entity relationships,      â”‚  â”‚
â”‚  â”‚ decision history, business logic      â”‚  â”‚
â”‚  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â”‚
                      â”‚
                      â–¼
            â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
            â”‚ Fused Result â”‚
            â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
`

## Tier 1: BM25 Lexical Index

**Engine:** Custom Go implementation of BM25 (Okapi BM25 variant)

The lexical tier excels at **exact and near-exact matching** â€” the kind of search where every character matters.

### Strengths
- **Error codes:** HTTP 500, ERR_CONN_REFUSED, 0xC0000005
- **File paths:** /var/log/tacflow/engine.log
- **Identifiers:** user_id = 0x7F4A, session_abc123
- **Technical terms:** BM25, HNSW, AES-256-GCM
- **Quotes and verbatim text:** exact phrase matching

### Technical Details
- Tokenization: Unicode-aware, configurable stop words
- Scoring: Standard BM25 with tunable k1 and b parameters
- Storage: Inverted index backed by SQLite
- Performance: O(1) lookup per token, sub-millisecond on 100k+ documents

## Tier 2: HNSW Vector Index

**Engine:** Native Go HNSW (Hierarchical Navigable Small World) implementation

The vector tier understands **meaning, not just words**. It finds conceptually related information even when no keywords match.

### Strengths
- **Semantic similarity:** "How to deploy agents" â‰ˆ "agent deployment guide"
- **Paraphrase matching:** "Kill process" â‰ˆ "terminate application"
- **Cross-language concepts:** Same intent, different language
- **Abstract queries:** "What's the best architecture for reliability?"

### Technical Details
- Distance metric: Cosine similarity (configurable to Euclidean)
- Index structure: Multi-layer HNSW graph
- Dimensions: Configurable (default 384, supports up to 1536)
- Recall: >99% at 10-entry search (standard benchmarks)
- Memory: ~1.2 GB per million vectors at 384 dimensions

### Why HNSW (not FAISS, not Annoy)?
| Feature | HNSW (Native Go) | FAISS (C++/Python) | Annoy (C++/Python) |
|:---|---:|:---:|:---:|
| Zero external deps | âœ… | âŒ | âŒ |
| Go native | âœ… | âŒ | âŒ |
| Dynamic inserts | âœ… | âš ï¸ | âŒ |
| High recall (>99%) | âœ… | âœ… | âš ï¸ |
| Memory efficient | âœ… | âœ… | âœ… |

## Tier 3: Knowledge Graph

**Engine:** Relational store + Edge adjacency index

The graph tier understands **relationships** â€” who knows whom, what caused what, which decisions led to which outcomes.

### Strengths
- **Entity resolution:** Is John Smith the same as jsmith@corp.com?
- **Causal chains:** Why was the payment rejected? â†’ Because the fraud score was > 0.8
- **Decision history:** What did the swarm decide about X last week?
- **Business logic:** This agent was trained by R1 on 2026-08-19

### Graph Schema (Simplified)

`
(Agent) --[trained_by]--> (Agent)
(Agent) --[owns]--> (Document)
(Document) --[references]--> (Memory)
(User) --[approved]--> (Decision)
(Decision) --[based_on]--> (Memory)
(Flow) --[executed_by]--> (Agent)
(Flow) --[produced]--> (TrainingRecord)
`

## Fused Search: How the Tiers Work Together

When a query arrives, all three tiers execute **in parallel** and their results are fused into a single ranked response.

### Fusion Algorithm
1. Each tier returns top-K results with normalized confidence scores
2. Reciprocal Rank Fusion (RRF) combines the rankings
3. Deduplication removes redundant results across tiers
4. Final ranking weighted by tier-specific confidence

## Performance Benchmarks

| Metric | BM25 | HNSW Vector | Knowledge Graph | Fused |
|:---|---:|---:|---:|---:|
| Latency (p50) | 0.3ms | 2.1ms | 1.8ms | 4.2ms |
| Latency (p99) | 1.1ms | 8.7ms | 7.2ms | 15.3ms |
| Recall@10 | 0.82 | 0.94 | 0.89 | **0.97** |
| Precision@10 | 0.79 | 0.91 | 0.93 | **0.95** |
| Memory (100k docs) | 45 MB | 128 MB | 64 MB | 237 MB |

## Why This Matters for Enterprise

| Requirement | How TacFlow Delivers |
|:---|---:|
| **Auditability** | Every memory access is logged with source tier and confidence |
| **Compliance (LGPD/GDPR)** | Memories can be queried by user ID and purged with cryptographic proof |
| **Deterministic Recall** | BM25 guarantees the same query returns the same results |
| **No Hallucination in Retrieval** | Fused search cross-validates across tiers before presenting results |
| **Offline Operation** | All three tiers run locally â€” zero cloud dependencies |

---

> **Related:** [TAC Language Documentation](TAC_LANGUAGE.md) â€¢ [Agent DNA & Encryption](AGENT_DNA.md)