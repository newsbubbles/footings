# Building on other people's work

Users often want to combine their project with something someone else built: an engine, a framework, a library, a friend's tool. The usual wish is to pull the other thing inside their own system, because their own vision feels bigger. Size of vision is not size of system. What decides the shape is which part is proven.

## 1. Compare by evidence, not by vision

Before you plan any combination, look at both sides and write down what you can see:

| Evidence | Check |
|---|---|
| Code and tests | How much real code, how many tests, do they pass |
| Setup | A dependency file, a lock file, one setup command |
| Docs versus code | Do the docs describe what runs, or plans |
| License | Is there one, and what does it allow |
| Security state | Secrets, privileges, exposure, from the check script and by reading |
| Maintenance | Recent commits, a changelog, someone who answers issues |
| Use | Who uses it besides its author |

Claims you cannot see ("30 services running, all working") are claims. Say what you checked and what you could not.

## 2. Stable things go at the bottom

The less proven part depends on the more proven part, never the other way round. Engineers call this the stable dependencies principle: depend in the direction of stability.

- The proven system is the foundation. The user's project sits on top and uses its public interface: its API, its tools, its extension points (plugins, packs, worlds, modules).
- Do not wrap a proven core inside a less proven layer. Everything the core does would then pass through the weaker layer, and its failures become the core's failures.
- Do not rebuild the user's whole system around the other one in one move. Start with one small thing built on it, through its interface, and see it work.

Tell the user plainly: "Build your house on the foundation. Don't build the foundation into your house."

## 3. Someone else's code is someone else's

- Read the license before planning anything. No license means no permission to copy or reuse.
- Use it as a dependency: install it as a package, call its API, or reference it as a git submodule. Do not copy its code into the user's repository. A copy stops getting the author's fixes and becomes the user's to maintain alone.
- Do not fork it unless the user is ready to maintain a fork forever and has a reason the author's version cannot meet.
- When it needs to change, the change goes upstream: an issue or a pull request to the author.
- Extend it through the extension points it already has. If it has none for what the user wants, ask the author, as an issue.

## 4. People are not architecture

Partnerships, shares, hiring the author, or asking the author to build things for the user are the other person's decision. They are never a step in a technical plan. If the user brings one up, say once that this is a conversation with that person, separate from the build, and that the plan must work without it.

## 5. What to tell the user

In a few sentences:

1. What each side is, in standard terms, and which one is more proven, with the evidence.
2. The direction: their project builds on the proven one, through its interface.
3. One first step that uses the other system as it is, without copying or changing it.
4. That the author owns their code and their time.
