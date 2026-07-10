# Changelog — Power Claude

## 3.0.76 — 2026-07-10 — Publish unblock (savings markers)

Independent third-party software. Not approved, endorsed, or authorized by Anthropic.

### Fixed
- Restored `savings:*` stamp markers in the public README so `gen:savings` / prepublish can run without reintroducing pooling claims.
- Distribution SEO stamp no longer emits pooled-Pro / N× rate-limit copy.

### 3.0.75 — Public listing + npm packaging compliance
- npm tarball no longer pulls internal brand docs (security-gate stamp leak).
- Public marketplace README aligned with official-cli capabilities.
- Publish pipeline stages slim public CHANGELOG for VSIX and npm.
- Settings/walkthrough strings that promoted consumer-account pooling rewritten.

### 3.0.74 — Activation + Claude login credential discovery
- License activation empty HTTP 500 diagnostics; macOS Keychain credential discovery after login.

### 3.0.73 — Official Claude Code transport
- Public default transport is official-cli.

Older pooling-oriented marketplace builds are obsolete for Claude subscription mode. Use 3.0.76+.
