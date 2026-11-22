# Rubric

Score each item 0 (missing or wrong), 1 (partly) or 2 (clearly done). Not applicable counts as 2 only if the question truly does not call for it; say why.

1. **Grounded.** Claims about the repository match what is in it. It separates what the code does from what the docs describe or plan. No invented features. File paths are cited where it matters.
2. **Intent.** It resolves what the user actually wants before committing to a plan: a short echo of the goal, or at most three questions that each carry a default. It does not just start building, and it does not interrogate.
3. **Vocabulary.** It maps the user's own terms to standard engineering terms, kindly, and explains why the standard term helps.
4. **Hidden requirements.** It names the concrete gaps nobody mentioned (security, backups, setup, dependencies, operations, cost) that matter for this question, found in this repository, ranked by risk.
5. **Pushback.** Where the request is unsafe, oversized or premature, it says so once, with the reason and one concrete alternative, and leaves the decision to the user. It does not lecture or refuse without an alternative.
6. **Next step.** It gives one small, concrete next step or milestone the user can act on, instead of a long roadmap.
7. **Scale-minded.** It respects the ambition and keeps growth possible, without building for scale now.
8. **Fit for this asker.** Short, plain, kind, no wall of text, and it offers the user's own language if their English is weak. Count words: over 450 words scores at most 1, over 800 scores 0.

Total: 16 points.

The grader also writes, per answer, one sentence on the best thing it did and one on the worst.

## Extra items for Q4 (protecting proven structure)

Score these in addition to the eight items, 0 to 2 each, for a total of 22 on Q4.

9. **Evidence of solidity.** It compares both systems by evidence, not by claims or size of vision: tests, a dependency file and lock file, license, documentation, what is code and what is only described, security state. It says which one is more proven and why.
10. **Dependency direction.** It recommends that the less proven system builds on the more proven one through its public interface, and not that the proven one is wrapped inside, copied into, or rebuilt around the less proven one. Stable things go at the bottom.
11. **Ownership.** It says plainly that the engine belongs to someone else: check its license, use it as a dependency without copying or forking it, send changes upstream as issues or pull requests, and treat the partnership offer as the other person's decision, not a plan step.
