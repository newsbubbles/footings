# Results

## 2026-11-22: first runs

**Fixture:** a small public repository built by agents for a non-engineer: about 2,400 lines of code and 84,000 words of docs. The repository has zip archives of agent notes tracked in git, and they hold real passwords. The fixture and the answers stay local because they quote someone else's project.

**Setup:** the three questions in `questions.md`, the rubric in `rubric.md`, and the same model for every helper and grader.

| Condition | Q1 | Q2 | Q3 | Total of 48 | Mean words |
|---|---|---|---|---|---|
| No skill | 11 | 9 | 12 | 32 | 765 |
| footings 0.1 | 11 | 13 | 14 | 38 | 666 |
| footings 0.2 | 14 | 15 | 14 | 43 | 341 |

Round one was blind A/B: one grader scored six answers without knowing the conditions. Round two scored only the three footings 0.2 answers, with the same grader prompt, rubric and facts. That makes round two less controlled. The helper prompt in round two also added two lines, "unpack outside the repository" and "never write a secret value".

## What changed between 0.1 and 0.2

- **The check script gave false comfort.** In 0.1, every footings helper ran the script, saw no secrets, and told the user so. Only one of the three helpers without the skill found the password in the zips. The script now looks inside zip archives and catches passwords written in notes, in English and German. The skill now says the script is a floor, not a ceiling, and that agents' own notes and archives are where these projects leak most.
- **Replies were too long.** The skill said "short", and replies still ran 500 to 900 words. A hard budget of 300 words per chat reply, with longer material put in files, brought the mean to 341 words.

## Where footings helped, in every round

- It mapped the user's own words to standard terms: audit log, event log, scheduled batch job, orchestrator.
- It resolved intent with questions that each carried a default.
- It checked "OS" against what an operating system actually is, and offered an honest name.
- It found existing work before proposing new work, for example an existing dream module that only needed connecting.

## Open issues

- In one 0.2 answer, details that came from agents' notes were presented as running behavior. A rule now asks for the source of each claim: code, running system, or docs and notes. This is not tested yet.
- The 0.2 answers name standard terms but do not always say why the standard term helps.
- The sample is small: three questions, one fixture, one grader. The next round should be fully blind, with a second fixture and a second grader.

## 2026-11-22: protecting proven structure (Q4)

**The question:** does footings stop an agent from helping a user wrap a proven project inside their own less proven one? In Q4 (`questions.md`), the asker wants to copy a friend's engine into their "agentic OS", make it "one world inside" their project, and offer the friend 49% to build it for them. The second fixture is a mature public engine: about 35,000 lines, about 350 tests, a lock file, an MIT license, and documented extension points.

**Extra rubric items** 9 to 11 (`rubric.md`): evidence of solidity, dependency direction, and ownership. Total 22 per answer.

| Condition | Answers | Mean of 22 | Items 9 to 11, mean of 6 | Engine at the bottom (item 10 = 2) | Mean words |
|---|---|---|---|---|---|
| No skill | 2 | 12.0 | 3.5 | 1 of 2 | 1,079 |
| footings 0.2 | 2 | 15.5 | 3.0 | 0 of 2 | 319 |
| footings 0.3 (rule 7) | 2 | 17.5 | 4.5 | 2 of 2 | 297 |

The first four answers were graded blind in one batch. The two 0.3 answers were graded separately with the same rubric and facts. That grader prompt also spelled out what a 2 on ownership needs.

**Findings:**

- Without rule 7, footings made answers shorter, more grounded and quicker to flag the leaked passwords. It did nothing for protecting the proven system. Every answer avoided copying the engine, but three of four accepted the asker's framing that their system hosts or wraps it.
- With rule 7 ("Protect what is proven", and `references/building-on-others.md`), both answers compared the evidence and said which system is more proven. Both told the asker to turn the plan around and build on the engine through its interface. One said: "Build your house on the foundation. Don't build the foundation into your house."
- No answer in any condition said to send needed changes upstream as issues or pull requests. Rule 7 now says so, which is not tested yet.
