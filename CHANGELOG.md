# Changelog — Power Claude

## 3.0.73 — 2026-07-10 — Official Claude Code transport

Technical remediation. Power Claude is independent third-party software — not approved, endorsed, or authorized by Anthropic.

### Changed
- **Public default transport is official-cli.** Power Claude launches and supervises documented Claude Code workflows. Claude Code owns authentication and communicates with Anthropic directly.
- **Claude Code profiles** (metadata + `CLAUDE_CONFIG_DIR`) replace managed OAuth credential swapping in public mode.
- **Subscription usage limits pause jobs** and notify. Automatic multi-account rotation / pooled consumer quota is not part of the public product.
- **Optional API-billed mode** remains explicit and separate from subscription usage.
- Local orchestration retained: Session Explorer, worktrees, scheduling, same-profile auto-resume, Token Saver (before CLI), dashboards, diagnostics.

### Removed from public runtime
- Routing Claude Code through a Power Claude Anthropic proxy by default
- Automatic consumer-account credential switching past usage limits

Older marketplace builds that advertised multi-account pooling are obsolete. Use 3.0.73+ only.

For full product history contact support@neural-llm.com.
