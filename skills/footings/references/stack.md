# Stack choices with scale in mind

Assume the user wants it to take off. Most projects do not, so do not build for millions on day one. But never choose something that makes growth impossible. The way to hold both is to sort every decision into one of two kinds.

## Two kinds of decision

**Hard to reverse (one-way doors).** Get these right early, and ask for a clear yes:
- the data model and where each kind of data lives;
- identity: how users log in, what a user ID is;
- tenancy: whether many customers share one system;
- the main language and runtime;
- hosting that locks you in (proprietary databases, platform-only features);
- the license of the code and of the content;
- anything public: domain, API shape others will depend on, the project name.

**Easy to reverse (two-way doors).** Choose fast, choose simple, change later:
- UI framework details, styling, component libraries;
- which cloud machine size;
- caching, queues and workers (add them when measured);
- internal module layout;
- most libraries behind a small interface of your own.

## Boring defaults that grow

Unless the intent gives a reason not to, prefer these. They are well known to every engineer and every model, they have libraries for everything, and each one grows a long way before it needs replacing.

| Need | Default | Grows to |
|---|---|---|
| Main database | PostgreSQL | millions of rows on one machine, replicas, managed hosting |
| Vector search | pgvector inside the same PostgreSQL | a dedicated vector store only when measured |
| Files and media | object storage (S3-compatible) | a CDN in front |
| Background jobs | a job queue on the database or Redis | a dedicated queue |
| Web app | one framework the user's agent knows well, one process | several stateless copies behind a load balancer |
| Auth | a proven library or provider, never hand-rolled | single sign-on, organizations |
| Deploy | a container or a platform deploy from git | the same, more copies |
| Reverse proxy and certificates | Caddy or nginx with automatic certificates | a load balancer |
| Scheduling | cron or the platform scheduler | a workflow engine when jobs depend on each other |
| Observability | structured logs, an error reporter, an uptime check | metrics and tracing |
| Local models | one model server behind an API, like a remote provider | a pool of model servers |

## Rules of thumb

- **One of each until it hurts.** One app process, one database, one job runner. A second one needs a measured reason.
- **A new service needs a reason a module cannot meet:** a different language, a different scaling need, a different owner, or isolation for safety.
- **Thirty services on one server is not an architecture.** It is thirty things that can fail. Merge until each remaining one has a reason.
- **Your own interface around every vendor.** Call the model provider, payment provider and email sender through one small module of your own, so you can switch.
- **State in one place.** If a fact lives in two places, one of them is a cache and must say so.
- **Measure before you optimize.** "It might be slow" is not a reason. A number is.
