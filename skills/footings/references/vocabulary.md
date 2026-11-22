# Vocabulary: house terms to standard terms

## Why names matter so much with agents

A standard term carries a large amount of knowledge for free. Say "message queue" to a model and it already knows ordering, retries, dead letters, backpressure, the common libraries and the usual failure modes. A made-up name carries none of that. Its only meaning is whatever context happens to be loaded. When it is not loaded, the agent guesses from the sound of the word, and each session guesses a little differently. That is how one idea ends up built three times in three places, and why nobody can search for a library to do it.

So: **the user's names live in the story, the UI and the pitch. Standard names live in the code, the file names and the technical docs. The glossary joins them.** Software teams call this a shared or ubiquitous language (from Domain-Driven Design): one vocabulary, written down, used everywhere.

## How to map a term

1. Ask what the thing does, not what it is called. Watch what the code does with it.
2. Find the closest standard term from the table below or from the field it belongs to.
3. If it is two things, split it. A name that means a page, a concept, a service and a table at once is four things.
4. Write the row into `docs/GLOSSARY.md`: house term, standard term, one-line meaning, where it lives in code.
5. If nothing standard fits, it may really be new. Say so, describe it in standard parts ("a priority queue with time-based decay"), and still keep the code name descriptive.

Tell the user without making them feel stupid: "What you call X is what engineers call Y. Same idea; using Y in the code means every tool and agent already understands it."

## Common mappings

| The user may say | Usually means |
|---|---|
| organ, module, ability, power | service, module, plugin or feature flag |
| stream, flow, current, pulse, river | event bus, event log, message queue, pub/sub |
| memory, archive, vault | database, document store, vector store, log |
| brain, mind, core, heart | orchestrator, main loop, controller, scheduler |
| perception layer, senses | input pipeline, ingestion, observation API, read model |
| splitter, fragment, shard, spark | work item, job, message, record with a time to live |
| decay, fading, evaporation | time to live (TTL), expiry, garbage collection |
| resonance, echo, harmony | similarity score, embedding similarity, recommendation |
| room, space, realm, zone | namespace, tenant, channel, scope |
| being, entity, creature, persona | agent, actor, user account, record |
| world, cosmos, universe | system, environment, simulation, domain model |
| law, rule, guardian | validation rule, policy, constraint, middleware |
| self-healing, immune system | health checks, automatic restart, circuit breaker, retries |
| dream, reflection, sleep mode | scheduled batch job, offline processing, consolidation job |
| trust layer, truth audit | access control, provenance, audit log, verification |
| evolution, learning loop | feedback loop, evaluation pipeline, fine-tuning, A/B test |
| bridge, connector, portal | API client, adapter, integration, gateway |
| tick, heartbeat, rhythm | scheduler, cron job, game loop tick |
| observer, watcher, guardian agent | monitor, supervisor, watchdog |
| mirror, snapshot | replica, backup, snapshot, cache |

## Grand nouns

Big names make the user and every agent believe the system does more than it does. A grand noun is allowed only when the thing has the features that define it. Otherwise use the honest name, and say why in one sentence.

| Grand noun | Earns the name only if | Usually it is really |
|---|---|---|
| operating system, OS | it controls access to shared resources (processes, memory, files, devices) and programs cannot bypass it; it has a kernel that mediates and services (daemons) around it | an orchestrator, launcher, dashboard, agent framework or platform |
| kernel | it is the privileged core that everything else must go through | a core library or main loop |
| engine | it runs other people's content by rules, and the content is separate from the engine | an app with its content built in |
| platform | other people build things on it through a documented interface | an app |
| ecosystem | several independent parties depend on it and on each other | a product with several parts |
| protocol | it is a written specification that two independent implementations can follow | an API or a format |
| AGI, consciousness, alive | not a claim to put in code or docs | an agent loop with memory |
| universe, metaverse | not a technical term | a shared environment or simulation |

The honest name is not smaller. "An orchestrator for my agents" can be explained in one sentence and built in a month. "An operating system for all AI" can be neither.
