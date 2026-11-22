# footings evals

A blind A/B test. Helper agents answer naive questions about a real, public, vibe-coded repository, once with the footings skill loaded and once without it. A separate grader scores the answers against the rubric without knowing which condition is which.

The helpers never change the repository. They only read it and answer, the way a coding agent would reply in chat.

## Files

- `persona.md`: who is asking, so the helpers can read the questions in context.
- `questions.md`: the questions, written in the asker's voice.
- `rubric.md`: what a good answer does, scored 0, 1 or 2 per item.
- `fixtures/` (not in git): the cloned repository. Any small public repo built mostly by an agent for a non-engineer works.
- `runs/` (not in git): answers and grades. They quote other people's code, so they stay local.

## Running

1. Clone a fixture repository into `fixtures/<name>`.
2. For each question, start two helper agents with the prompts in `prompts.md`: one with the skill, one without.
3. Save each answer to `runs/<date>/<question>-<A|B>.md`, with the condition hidden behind a random letter.
4. Start one grader agent with `rubric.md` and all answers. It scores without knowing the conditions.
5. Unblind, compare, and record the result in `RESULTS.md`.
