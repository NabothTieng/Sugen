# AI Usage

This project was built with AI assistance (Claude, in chat) for design and
code generation, and calls Gemini (`gemini-2.5-flash` by default) at
runtime as the clinical reasoning engine inside the pipeline itself.
These are two different uses — keep them distinct when describing this:

- **Claude**: helped design the 3-call architecture, wrote `main.py`,
  caught the retrieval bugs documented in `PROGRESS_LOG.md` and
  `README.md`, and drafted the 5 custom eval cases.
- **Gemini**: is the model the *pipeline itself* calls at runtime to
  synthesize episodes, propose codes, and verify them.

> Fill in after your own local session:
> - Any additional prompting/debugging you did yourself.
> - Anything you changed from the generated code and why.
> - Attach or link the full session transcript per the brief's mandatory
>   transcript requirement.
