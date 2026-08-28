# Agent DNA & Immutable Owner Chain

> *"Every agent has a birth certificate. Every action has a signature."*

## Overview

TacFlow is the only agent platform where every agent carries a **cryptographic birth signature (DNA)** — an immutable record of who created it, when, under what configuration, and every modification it has received throughout its lifecycle.

This is not a log file. This is a **cryptographic chain of custody** embedded into the agent itself.

---

## Agent DNA: The Birth Certificate

When an agent is created on the TacFlow platform, the engine generates a **DNA record** that becomes part of the agent's permanent identity:

```json
{
  "agent_dna": {
    "agent_id": "01KV81BBEXW32QNW8P391H35B0",
    "name": "R1",
    "created_at": "2026-06-16T10:00:00Z",
    "created_by": "swarm_orchestrator",
    "swarm_id": "01KV81BBEP80DBEW2KPNC074JQ",
    "model": "tacflow_provider/deepseek-ai/DeepSeek-V4-Flash",
    "dna_hash": "sha256:a1b2c3d4e5f6...",
    "generation": 1,
    "parent_dna": null
  }
}
```

### What the DNA Contains

| Field | Description | Immutable? |
|:---|---|:---:|
| `agent_id` | Unique identifier (ULID format) | ✅ Yes |
| `created_at` | Timestamp of creation | ✅ Yes |
| `created_by` | Agent or user who created it | ✅ Yes |
| `swarm_id` | Home swarm | ✅ Yes |
| `model` | Foundation model at creation | ✅ Yes |
| `dna_hash` | SHA-256 of the DNA record | ✅ Yes |
| `generation` | Version number (1 = original) | Increments on training |
| `parent_dna` | Hash of parent agent (for cloned agents) | ✅ Yes |

---

## Owner Chain: Immutable Modification History

Every modification to an agent — training, skill update, memory migration, transfer — creates a new **owner chain entry**:

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  DNA Record  │────→│  Owner Entry │────→│  Owner Entry │
│  (Birth)     │     │  #1          │     │  #2          │
│              │     │              │     │              │
│  gen: 1      │     │  gen: 2      │     │  gen: 3      │
│  hash: A     │     │  hash: B     │     │  hash: C     │
└──────────────┘     └──────────────┘     └──────────────┘
                           │                     │
                           ▼                     ▼
                    ┌──────────────┐     ┌──────────────┐
                    │  Event:      │     │  Event:      │
                    │  Training    │     │  Transfer    │
                    │  By: R30     │     │  To: Swarm X │
                    │  Sig: ✓      │     │  Sig: ✓      │
                    └──────────────┘     └──────────────┘
```

### Owner Entry Schema

```json
{
  "owner_entry": {
    "agent_id": "01KV81BBEXW32QNW8P391H35B0",
    "generation": 2,
    "previous_hash": "sha256:a1b2c3d4e5f6...",
    "entry_hash": "sha256:f6e5d4c3b2a1...",
    "timestamp": "2026-08-19T14:30:00Z",
    "event_type": "training",
    "performed_by": "01KVQB6CYHKGMBRXWN8PQX3XGT",
    "signature": "ed25519:4f8e9d0c1b2a...",
    "changes": [
      "skill: memory-search updated v1.0 → v1.1",
      "persona: tone adjusted from formal to technical"
    ]
  }
}
```

### Event Types Tracked

| Event | Description |
|:---|---|
| `creation` | Agent birth (DNA record) |
| `training` | Swarm training cycle completed |
| `skill_update` | Skill added, removed, or modified |
| `persona_change` | Personality, tone, or role updated |
| `memory_migration` | Memory transferred between agents |
| `transfer` | Agent moved to another swarm |
| `export` | Agent exported as `.tacagent` |
| `import` | Agent imported from `.tacagent` |
| `reputation_change` | Significant score change |

---

## Dynamic Reputation System

Every agent in a TacFlow swarm carries a **reputation score** that determines task routing autonomously:

### How Reputation Works

```
Score Range: 0–1000
Starting Score: 500 (neutral)

Increases when:
  - Task completed successfully: +5 to +20 (based on complexity)
  - Peer votes "helpful": +10
  - Training received: +50 (cap at 1000)

Decreases when:
  - Task failed: -10 to -50 (based on impact)
  - Peer votes "unhelpful": -15
  - Time without successful tasks: -1/day (decay)
```

### Task Routing Logic

```
When a task arrives:
  1. Filter: Online agents only
  2. Filter: Agents with required skills
  3. Rank: By reputation score (highest first)
  4. Route: Top agent gets the task
  5. Fallback: If top agent fails, next in ranking
```

### Why Reputation Matters

- **No single point of failure:** If the highest-ranked agent is offline, the next takes over
- **Meritocratic:** Better agents earn more tasks and improve faster
- **Self-correcting:** Underperforming agents naturally receive fewer tasks
- **Transparent:** Every score change is logged in the owner chain

---

## Encrypted Agent Export (`.tacagent`)

TacFlow agents can be **fully exported** as a single portable file — the only platform that offers this capability.

### What's Inside a `.tacagent` File

```
┌─────────────────────────────────────────┐
│           .tacagent Package             │
├─────────────────────────────────────────┤
│  Header (unencrypted)                   │
│  ├── Magic bytes: "TACAGENT"            │
│  ├── Version: 1.0                       │
│  ├── Agent ID                           │
│  ├── DNA Hash (for integrity check)     │
│  └── Encryption: AES-256-GCM            │
├─────────────────────────────────────────┤
│  Encrypted Payload                      │
│  ├── agent_profile.json                 │
│  ├── personality/system_prompt          │
│  ├── skills/                            │
│  │   ├── skill-memory-search-v1.1.md    │
│  │   └── skill-web-search-v2.0.md       │
│  ├── memories/                          │
│  │   ├── memory_store.sqlite            │
│  │   └── memory_index.json              │
│  ├── aprendizado.db                     │
│  ├── brain.db (agent-specific subset)   │
│  ├── owner_chain.json                   │
│  └── reputation_history.json            │
└─────────────────────────────────────────┘
```

### Security Properties

| Property | How It's Achieved |
|:---|---:|
| **Confidentiality** | AES-256-GCM encryption of entire payload |
| **Integrity** | GCM authentication tag + SHA-256 header hash |
| **Non-repudiation** | Owner chain with Ed25519 signatures |
| **Portability** | Single file, platform-independent SQLite |
| **Password Protection** | Derived key via Argon2id (memory-hard KDF) |

### Use Cases

1. **Backup:** Full agent snapshot before major changes
2. **Transfer:** Move an agent from one swarm to another
3. **Audit:** Hand the encrypted package to a compliance officer
4. **Collaboration:** Share agent capabilities without exposing credentials
5. **Forensics:** Investigate agent behavior after an incident

---

## Cross-Swarm Transfer Protocol

```
Source Swarm                          Destination Swarm
    │                                       │
    │  1. Export agent → .tacagent          │
    │───────────────────────────────────────│
    │                                       │
    │  2. Transfer .tacagent (any channel)  │
    │───────────────────────────────────────│
    │                                       │
    │                                       │  3. Import .tacagent
    │                                       │     ├── Verify DNA hash
    │                                       │     ├── Decrypt payload
    │                                       │     ├── Register in new swarm
    │                                       │     └── Append owner chain
    │                                       │
    │  4. Acknowledge import                │
    │◄──────────────────────────────────────│
    │                                       │
    │  5. Original agent marked as "migrated"
    │     (owner chain preserved)           │
```

---

## Enterprise Compliance

| Requirement | How TacFlow Delivers |
|:---|---:|
| **SOC 2 / ISO 27001** | Immutable audit trail with cryptographic signatures |
| **LGPD / GDPR** | Full agent lifecycle tracking for data subject requests |
| **SOX** | Every agent action traced to an accountable entity |
| **Internal Audit** | Export any agent as `.tacagent` for offline review |
| **Forensic Analysis** | Owner chain provides complete modification history |

---

> **Related:** [TAC Language Documentation](TAC_LANGUAGE.md) • [Memory Architecture](MEMORY_ARCHITECTURE.md)
