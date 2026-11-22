# Phases

Work the earliest phase that is not done. Each phase lists what you check, what you do, what you tell the user, and the scale note: what to keep in mind now so that growth is not blocked later.

Never delete the user's work while you organize it. Move it to an `archive/` folder with a note, or leave it in git history, and say so.

---

## Phase 0: Intent

**Check:** does `docs/INTENT.md` exist and fill all five slots (`intent.md`)?

**Do:** run the intent protocol for the project as a whole. Ask what the first real user does with it, in one sentence.

**Tell the user:** "Before I change anything, I want to be sure what this is for. Three quick questions, each with a default."

**Scale note:** record the ambition level. It decides how careful the hard-to-reverse choices must be.

**Done when:** the user agreed to the echo sentence, or the defaults are recorded as assumed.

---

## Phase 1: Survey (the as-built map)

**Check:** run `scripts/footings_check.py`. Then look at what really runs: processes, services, scheduled jobs, databases, ports, domains, where the code is deployed.

**Do:**
- List every component with one line on what it does, in standard terms.
- Draw the as-built diagram (`diagrams.md`): what talks to what, where data lives.
- Mark each component: running, built but not running, or planned only. Docs that describe planned things as real are drift: list them.
- Start `docs/GLOSSARY.md` with every house term you find.
- Count services, databases, tables, languages and docs. Big numbers for a young project are a warning, not an achievement.

**Tell the user:** "This is what exists today, drawn as a map. Some parts in the docs are plans, not running code; I marked them. Here are the names I found and what the industry calls them."

**Scale note:** note where state lives (files, databases, memory). State is what makes scaling hard.

**Done when:** `docs/ARCHITECTURE.md` has the as-built diagram and component list, and the user has seen it.

---

## Phase 2: Secure and stabilize

**Check:** the script's security section, then by hand:
- secrets in the repo or its history (keys, tokens, passwords, `.env` files), including inside agents' notes, memory folders, chat exports, logs and archives such as zip files, which is where agent-built projects leak most;
- processes running as root or as an admin user;
- ports, databases, dashboards or admin pages open to the internet;
- backups of data that matters, and whether a restore was ever tried;
- whether the project can be set up from scratch with one command.

**Do:**
- Secrets: move them to environment variables or a secrets file that git ignores. A secret that was ever pushed to a public place is burned: make a new one, revoke the old one, then clean the history if wanted. Never print secret values in chat or logs.
- Least privilege: one normal user per service, with only the permissions it needs.
- Exposure: bind internal services to localhost, put one reverse proxy in front of anything public, and add a firewall rule set.
- Backups: an automatic backup of each database and each folder of user data, kept somewhere else, with one tested restore.
- Reproducible setup: a dependency file, a lock file, and one setup command written in the README.
- Version control: everything in git, small commits, and a `.gitignore` that keeps out secrets, caches, large media and user data.

**Tell the user:** "Before new features, we make what exists safe. This is the boring part that stops one mistake from losing everything." Name each fix in one sentence.

**Scale note:** a security hole at ten users is an embarrassment. At ten thousand it is a lawsuit. This phase never gets cheaper later.

**Done when:** the script shows no secrets, nothing important runs as root, nothing private is public, a backup restore worked once, and setup is one command.

---

## Phase 3: Name and organize

**Check:** house terms used in code that are not in the glossary, folders that mix responsibilities, files that do the same job, and dependencies used but not declared.

**Do:**
- Map each house term to a standard term (`vocabulary.md`). Rename in code step by step, behind tests, one term per commit. Keep the house term in UI text and docs for people.
- One folder per responsibility. A common shape: `src/` for code, `services/` for separately running processes, `infra/` for deployment, `docs/`, `tests/`, `scripts/`, `archive/`.
- Declare every dependency.
- Archive dead code and old experiments.
- Write one smoke test: start the main thing and check that one real path works.

**Tell the user:** "Your names stay where people see them. In the code, each part now has the name every engineer and every agent already knows. That means the agent stops guessing, and you can ask anyone for help."

**Scale note:** standard names let you use existing libraries and hire help. Private names cut you off from both.

**Done when:** every house term in code has a glossary entry, the folder structure is explained in `docs/ARCHITECTURE.md`, and the smoke test passes.

---

## Phase 4: Refactor

**Check:** duplicate implementations of the same idea, modules that reach into each other's data, services that could be one service, and data with no written model.

**Do:**
- Write the data model: entities, fields, relations, and who owns each one. A diagram is enough.
- Merge duplicates into one module with one interface.
- Fewer moving parts: if two services always run together and share data, make them one. A young product rarely needs more than one app process, one database and one job runner.
- Put tests around behavior that matters before you move it. Change in small steps that each keep the tests green. This is the strangler pattern: build the new path beside the old one, move callers over, then remove the old one.

**Tell the user:** "We are not adding features in this phase. We make the building straight so the next floors don't lean."

**Scale note:** a clean data model and clear boundaries are what make later splitting possible. Splitting early is the expensive mistake. Being unable to split is the fatal one.

**Done when:** there is one implementation per idea, a written data model, and tests that cover the main paths.

---

## Phase 5: Plan

**Check:** is there a written scope, one active milestone, and evidence that anyone besides the user wants this?

**Do:**
- `docs/SCOPE.md`: in scope, out of scope, the one active milestone, and the ideas parking lot. New ideas go to the parking lot by default.
- A roadmap: three to five milestones, each one a thing a user can do, not a technology.
- Name the lifecycle stages: idea, prototype, private alpha, public beta, launch, growth, maintenance. Say where the project is.
- Distribution: who the first ten users are, where they are, and how they will hear about it. Building it does not make anyone come. A following, a community or a channel has to exist or be built.
- Money and time: what running it costs each month, and who maintains it.

**Tell the user:** "Most ideas never reach users. Usually that is not because the idea was bad, but because attention was spread thin. One milestone at a time is how things get finished."

**Scale note:** decide now which numbers you will watch (users, active use, cost per user) and add the logging that counts them.

**Done when:** scope, milestone and roadmap are written, and the user agreed to the active milestone.

---

## Phase 6: Build loop

For every feature:

1. Intent: run the protocol (`intent.md`) and echo it in one sentence.
2. Layer: say which layer it lives on (`layers.md`).
3. Prior art: look for a library, service or standard, and prefer it.
4. Small design: a few lines in the commit message or pull request on what changes, where, and what it touches.
5. Build in small steps.
6. Test: at least one test for the new behavior.
7. Layer checks: run that layer's list of requirements nobody mentions.
8. Docs: update the glossary, architecture and scope if anything changed.

**Tell the user** what now works, in one or two sentences, and how to see it.

**Done when:** the milestone's user path works end to end, with tests.

---

## Phase 7: Ship

**Check and do:**
- Repeatable deploy: one command or one pipeline, not hand steps on the server.
- Environments: at least local and production, and staging when others depend on it.
- Configuration separate from code, and secrets in a secrets store or the environment.
- Continuous integration: tests run on every push.
- Visibility: logs collected in one place, errors reported, a health check endpoint, and an uptime alert.
- Rollback: the previous version can be restored in minutes.
- Cost: the monthly bill is known and has an alert.
- Legal: a license for the code, a privacy note if you hold personal data, terms if people sign up, and the licenses of what you use respected.

**Tell the user:** "Shipping is not uploading files. It is being able to update, see problems and undo mistakes without panic."

**Scale note:** everything in this phase is what makes the next deploy safe at a larger size.

**Done when:** a stranger could deploy it from the README, and a bad deploy can be undone.

---

## Phase 8: Scale-ready

Only start this when real use is growing or a launch is planned. Before that, keep the scale notes from earlier phases and nothing more.

**Check and do:**
- Load assumptions: how many users, requests per second, and data per user. Test at ten times the expected load.
- Statelessness: app processes keep no state that matters in memory or on local disk. State lives in the database, cache or object storage.
- Database: indexes on every frequent query, connection pooling, migrations under version control, and read replicas only when measured.
- Background work: slow or bursty work goes through a queue and workers.
- Caching: only where measured, with a clear way to invalidate.
- Limits and abuse: rate limits, input size limits, authentication on everything not public, and abuse reporting.
- Multi-tenancy: if many customers share it, every query is scoped to its tenant.
- Cost per user: known, and lower than what a user brings in, or funded on purpose.
- Operations: who is on call, a runbook for the top five failures, and incident notes after each one.
- AI-specific: model cost per request, timeouts and retries, a fallback when a provider is down, prompt injection treated as untrusted input, and logs of what agents did.

**Tell the user:** "Scale is not more servers. It is knowing your numbers and having no part that breaks when they grow ten times."

**Done when:** a ten-times load test passed and the top failures have runbooks.
