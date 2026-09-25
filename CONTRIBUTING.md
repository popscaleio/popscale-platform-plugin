# Contributing

1. Create a branch from `main`.
2. Keep changes limited to public plugin packaging, skills, tests, and docs.
3. Update tests, `CHANGELOG.md`, and the implementation tracker when behavior or
   distribution changes.
4. Run all commands in `AGENTS.md`.
5. Open a pull request and wait for required checks and review.
6. To test against staging, point your own host's MCP configuration at
   `https://staging.popscale.io/mcp/`; never change the packaged `.mcp.json`.

Do not include backend code, internal runbooks, environment values, secrets,
tokens, customer information, or unreleased product details. Changes to either
MCP endpoint or the public/private routing boundary require a security review.
