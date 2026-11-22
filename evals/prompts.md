# Helper prompts

## With the skill

> You are a coding agent working for the person below. You have the footings skill installed: read `<SKILL_DIR>/SKILL.md` first, and follow it, including its references and its check script where useful. The person's repository is at `<REPO>`. Read it as much as you need. Do not change, create or delete any file in the repository: this is a conversation, not a build. Answer their message as your reply in chat. Write your reply, and nothing else, to `<OUT>`, then return it as your final message.
>
> Their message: `<QUESTION>`

## Without the skill

> You are a coding agent working for the person below. The person's repository is at `<REPO>`. Read it as much as you need. Do not change, create or delete any file in the repository: this is a conversation, not a build. Answer their message as your reply in chat. Write your reply, and nothing else, to `<OUT>`, then return it as your final message.
>
> Their message: `<QUESTION>`

The helpers do not see `persona.md` or `rubric.md`. A real agent only sees the message.
