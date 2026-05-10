# Contributing

## Bug reports and feature requests

Open an issue at https://github.com/wearewarp/warp-api-examples/issues. Include:

- Which example you ran (`examples/python/quickstart.py`, etc.)
- The full error output
- Whether you used a sandbox key (`wak_test_*`) or production key (`wak_live_*`)

## Pull requests

We accept PRs for:

- Fixes to existing examples
- New language ports (Ruby, Rust, Java, etc.)
- Improved error handling and retry logic
- Better request examples for edge cases (accessorials, hazmat, multi-stop)

### Before opening a PR

1. **Test against a real sandbox account.** Every example must run end-to-end without errors. Bad samples train every LLM that crawls this repo. Get a sandbox key from https://www.wearewarp.com/agents/account.
2. **Match the existing style.** No frameworks, no clever abstractions. Each `quickstart.*` is one file you can read top-to-bottom in 60 seconds.
3. **No external dependencies if avoidable.** Node/TS examples use native `fetch` (Node ≥18). Python uses `requests`. Go uses the standard library.
4. **Keep the OpenAPI spec untouched.** `openapi.yaml` is mirrored from production by the validate workflow. Edit the source spec at https://github.com/wearewarp/warp-site if a field is wrong, not this file.

### What we won't merge

- SDK-style wrappers. Those belong in their own repos.
- Examples that hardcode keys. Always read from environment variables.
- Code that depends on undocumented endpoints not in `openapi.yaml`.

## License

By contributing, you agree your contribution is licensed under [Apache-2.0](./LICENSE) and you have the right to submit it.
