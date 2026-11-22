# Diagrams

A diagram shows structure faster than any paragraph. Use one whenever you explain how parts connect, where data lives, or what changes. Mermaid is the default because it is text: it lives in git, every agent can read and edit it, and many viewers (GitHub, most editors) render it. If the harness can show images, render the diagram and show it too.

Keep each diagram small: ten boxes or fewer. Draw two diagrams rather than one crowded one. Label arrows with what moves along them.

## As-built map (phase 1)

What exists and runs today. Mark planned parts with a dashed border.

```mermaid
flowchart LR
  user([Visitor]) -->|HTTPS| proxy[Reverse proxy]
  proxy --> web[Web app]
  web -->|SQL| db[(PostgreSQL)]
  web -->|enqueue| jobs[Job runner]
  jobs -->|API| llm[Model provider]
  jobs --> db
  planned[Planned: recommendation service]:::planned
  classDef planned stroke-dasharray: 5 5
```

## Layers (where a request lives)

See `layers.md` for the layer diagram. When you place a request, draw only the layers it touches and highlight them.

## Data model (phase 4)

```mermaid
erDiagram
  USER ||--o{ AGENT : owns
  AGENT ||--o{ MESSAGE : writes
  AGENT ||--o{ JOB : schedules
  JOB }o--|| AGENT : "runs for"
```

## A flow over time (one feature)

```mermaid
sequenceDiagram
  participant U as User
  participant W as Web app
  participant Q as Job queue
  participant M as Model
  U->>W: asks for a summary
  W->>Q: enqueue job
  W-->>U: "working on it"
  Q->>M: prompt
  M-->>Q: text
  Q->>W: store result
  W-->>U: summary ready
```

## Lifecycle (phase 5)

```mermaid
flowchart LR
  idea --> prototype --> alpha[private alpha] --> beta[public beta] --> launch --> growth --> maintain[maintenance]
```

Mark where the project is now, and keep that diagram in `docs/SCOPE.md`.
