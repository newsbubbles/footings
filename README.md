# footings

**Senior engineering judgement for projects your AI agent builds.** footings is an agent skill. It makes your coding agent act like the experienced engineer your project doesn't have: it asks what you really want, uses the real names for things, checks what nobody told you to check, and takes your project from a messy prototype to something that can grow.

You keep your vision and your names. footings puts something solid under them.

## Who it is for

- You build with Claude Code, Codex, Cursor or another agent, and you are not a professional engineer.
- Your project grew fast: many files, many docs, maybe many services, and you are no longer sure what is real.
- You want it to take off one day, and you want the choices made now to allow that.

Experienced engineers can use it too, as a checklist that never gets tired.

## What it does

- **Resolves intent before building.** For any real change, your agent first says in one sentence what you want, who it is for and how you'll know it works. It asks at most three questions, each with a default.
- **Uses the real word.** Your names stay in your UI and your story. The code uses the standard engineering term, and a glossary joins the two. Agents stop guessing what your words mean.
- **Checks what nobody mentions.** Every request is placed on a layer (interface, services, data, integration, infrastructure, operations), and that layer's hidden requirements get checked: security, backups, failure, cost, scale.
- **Pushes back once, then builds.** If something is unsafe, already exists or will hurt later, your agent says so once, with one alternative. Then it's your call.
- **Walks you through phases.** Intent, survey, secure, name and organize, refactor, plan, build, ship, scale-ready. One phase at a time, with scale in mind from the start.
- **Keeps the project's memory in five short files** under `docs/`: intent, glossary, architecture, scope and decisions. Every session reads them first, so nothing drifts.

## Install

**Claude Code (plugin):**

```
/plugin marketplace add newsbubbles/footings
/plugin install footings@footings
```

**Any agent that supports skills:** copy the `skills/footings` folder into your agent's skills folder. For Claude Code that is `~/.claude/skills/` (all projects) or `.claude/skills/` (one project).

**Any other agent:** clone this repo next to your project and tell your agent: "Read footings/skills/footings/SKILL.md and follow it for all work in this project."

## Use

In your project, say to your agent:

> Use footings on this project. Start with the check and tell me which phase we are in.

To set up the project docs and make every future session load footings:

```bash
python path/to/skills/footings/scripts/footings_check.py init . --agents-file
```

This creates `docs/INTENT.md`, `GLOSSARY.md`, `ARCHITECTURE.md`, `SCOPE.md` and `DECISIONS.md` (it never overwrites), and adds a short note to `AGENTS.md` (and `CLAUDE.md` if you have one).

To run the check by itself:

```bash
python path/to/skills/footings/scripts/footings_check.py .
```

It is read-only, needs only Python 3.8+, and never prints secret values.

## What's inside

```
skills/footings/
  SKILL.md                 the six rules, the phases, how to talk to you
  references/
    intent.md              the intent resolution protocol
    phases.md              each phase: check, do, tell, scale note, done when
    layers.md              the six layers and what nobody mentions on each
    vocabulary.md          common invented names and their standard terms; grand nouns
    pushback.md            how to disagree once, and the hard lines
    stack.md               decisions that are hard vs easy to reverse; boring defaults that grow
    diagrams.md            mermaid templates
  templates/               the five project docs
  scripts/footings_check.py
evals/                     blind A/B tests of the skill against naive questions
```

## License

MIT. Made by [Measured Instruments](https://github.com/newsbubbles).
