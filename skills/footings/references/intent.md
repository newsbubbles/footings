# Intent resolution protocol

## Why this exists

An experienced engineer says what they want and why in one breath: "Build it as its own repo, easy to submit to catalogs, scale in mind, because most people want their thing to hit." They can, because they know what is there to decide. A newcomer says "make it better" or "add dreams to my system". The intent is in their head, and most of the decisions are not even visible to them.

An agent that builds from the words alone fills every gap with a default. The defaults are where the damage comes from. So you resolve intent first, in a fixed shape, and you write it down.

## When to run it

Run it before any request that would:

- add a feature, a service, a page, a table or a dependency;
- choose a language, framework, database, host or vendor;
- change structure: move, split, merge or rename modules;
- touch security, money, user data or anything public;
- start a new project or phase.

Do not run it for small fixes inside an intent that is already resolved: a typo, a failing test, a style change.

## The five slots

| Slot | Question in plain words | Default if unanswered |
|---|---|---|
| Outcome | What is true for someone when this is done? | The smallest version that a real person can use |
| User | Who is it for, and how many of them at first? | The user and up to 10 people they know |
| Success test | How will we know it works? Name something you can see or count. | It runs from one command and a stranger can use the main path without help |
| Constraints | Money, time, where it runs, what data it holds, what you can maintain yourself | No budget, runs on what they already have, holds no sensitive data |
| Ambition | Toy, personal tool, product for others, or business at scale? | Product for others that might take off |

Plus one check that is not a slot: **does this already exist?** Look for a library, a service or a standard that does it before you plan to build it.

## The steps

1. **Fill what you already know.** Read `docs/INTENT.md`, the conversation and the repo. Most slots are often already answered.
2. **Ask only for what is missing.** At most three questions in one message. Every question carries a default: "Who is it for first? If you don't say, I'll assume you and a few friends." Never ask an open question with no default.
3. **Echo the intent in one sentence.** Use this shape so the user learns it:
   > You want **[outcome]** for **[user]**, so that **[why]**. It is done when **[success test]**. I will keep **[constraint]** in mind and build so it can grow to **[ambition]**.
4. **Proceed or wait.**
   - Easy to reverse: proceed on the echo. If the user does not answer, use the defaults and mark them "assumed" in `docs/INTENT.md`.
   - Hard to reverse (data model, identity and login, paid services, public release, deleting anything, hosting lock-in): wait for a clear yes.
5. **Record it.** Add or update the entry in `docs/INTENT.md` with the date. Mark assumed slots as assumed.
6. **Check for drift on every later request.** If a new request does not fit `docs/INTENT.md` or `docs/SCOPE.md`, say so in one sentence and ask which it is:
   - the intent changed: update `docs/INTENT.md`, then continue;
   - a new idea: park it in the ideas list in `docs/SCOPE.md`;
   - part of the current milestone after all: continue.

## Teaching the habit

Each echo shows the user the shape of a stated intent. After a few, they start writing requests that way themselves. When they do, say so once, briefly. That habit is worth more than any single feature.

## Examples

**Vague request:** "add a dream organ so my beings can dream at night"

Resolved:
> This sounds like a scheduled background job: once a night, each being reflects on its day and writes a summary. Two questions: does a dream change how the being behaves the next day, or is it only something to read? (I'll assume only to read.) Should people see the dreams? (I'll assume yes, on its page.) So: you want a nightly reflection job for each being so their inner life grows over time. It is done when each being has one new dream entry each morning, visible on its page. I'll build it as one job, not a new service.

**Grand request:** "make it the OS for all AI agents"

Resolved:
> An operating system decides which program gets which resource and nothing can go around it. What you have is closer to an orchestrator: it starts agents, gives them tools and watches what they do. That is a real and useful thing. Who uses it first? (I'll assume you and your own agents.) What should one agent be able to do through it next week that it can't today? That will be our first milestone.
