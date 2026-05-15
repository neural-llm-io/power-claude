# Changelog — Power Claude

All notable changes to the Power Claude VS Code extension are
recorded here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and we use [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Conventions

- **`[Unreleased]`** lives at the top and collects WIP changes between releases.
  Release tooling (`scripts/release/bump.sh`) promotes that block to a versioned
  heading and writes a fresh empty `[Unreleased]` stub.
- **LLM-agnostic posture**: anything written here should describe user-visible
  behavior, not the assistant that authored it. The release tooling, CI hooks,
  and prose conventions are deliberately portable across Claude / GPT / Gemini
  / Copilot / human-only workflows — keep it that way when adding sections.
  Claude-specific automation lives behind harness hooks under `~/.claude/` and
  is not part of the shipped artifact.
- **Tags**: each released version is anchored by an annotated git tag
  (`vMAJOR.MINOR.PATCH`). Historical 0.10–0.14 commits pre-date the standalone
  repo extraction (2026-05-10) and are not retroactively tagged here; their
  history is in the originating NDP monorepo.

## [Unreleased]

### Data correctness (Stabilization P0)

- **A-01 — JSONL apiKeyId attribution**: All JSONL token buckets previously
  collapsed into a single `_unknown` account, causing the per-account chart
  to show "1 account" regardless of how many profiles were active. Buckets
  are now stamped with the current active profile at aggregate time; accounts
  written before a profile switch fall back to `_unknown` (documented
  limitation, grand-total cost is correct).
- **A-02/A-03 — "$0.00/day" while other panels showed $446**: `todayDollarsTotal()`
  returned 0 when today's UTC date had no API buckets yet (e.g., fresh session
  after midnight). Now falls back to the most-recent previous day, labelled
  `source="last-known"` in the UI. One source-of-truth function drives all
  panels — the contradiction is impossible.
- **A-05 — Account status / utilization bar desync**: "Healthy" pill and the
  5h session bar could disagree (healthy pill cached in run.json, bar reading
  live rate-limits.json). Single read of `rate-limits.json` now drives both
  signals. "Healthy + red bar" is structurally impossible.

### Security (D-03)

- **Path traversal prevention**: User-supplied account names and session IDs
  are validated via `assertSafeName()` before being interpolated into
  `path.join()` calls. Characters outside `[A-Za-z0-9._@-]`, sequences
  containing `..`, and inputs outside 1–128 chars are rejected with an
  explicit error message.
- **API token redaction improved**: Tokens in proxy error logs are truncated
  to 8 chars + `…` (was 15–20 chars, leaking more key material than needed).

### UX / Information Architecture (B-stream)

- **B-01/B-02/B-03 — Account row visual redesign**: Removed duplicate inner
  color dot beside the account name and the second darker inner stripe.
  Single color encoding: edge stripe per account. Overlay by status:
  active+healthy = green diff overlay; active+cooling = red overlay;
  cooling-not-active = orange overlay; healthy-not-active = no overlay.
- **B-04**: Removed trivial "Each row is one Claude account" helper text.
- **B-05 — Sessions tab split**: Sessions tab is now three tabs:
  **Sessions** (Resume active session), **History** (sparklines + 7-day
  bars + snapshots), **Activity** (commits + rate-limit handler events).
- **B-06 — Usage Heatmap relocated**: Per-account rate-limit heatmap and
  fairness chart moved from the Overview tab to the Usage tab.
- **B-07 — IA deduplication**: Data points that appeared in multiple panels
  under different headings now have a single primary location.
- **B-08 — Available-accounts indicator heatmap**: "Next available in" chip
  changes color based on healthy-account count: ≥8 green, ≥4 yellow,
  ≥1 orange, 0 red. Thresholds live in `AVAIL_THRESHOLDS` constant.
- **B-09 — Sidebar ↔ webview linking**: Clicking an account in the sidebar
  tree now opens the dashboard, switches to the Overview tab, and
  smooth-scrolls to the account row with a 1.8s highlight pulse animation.
- **B-10 — Sidebar decluttered**: 7 tree sections → 3: Accounts (grouped
  by status), System Health (read-only), Quick Actions. LLM Usage and
  Metrics sections removed from the sidebar (available in the main panel).
- **B-11**: Tooltip audit pass — every `title=` attribute explains a
  non-obvious fact; trivial self-describing tooltips removed.
- **B-12**: Plan badge variant for expired subscriptions: `PRO (EXPIRED)`
  greyed badge + "Renew" action button.
- **B-14 — Rotation queue indicator**: Each cooling/blocked account now
  shows a small queue chip (`next`, `+1`, `+2`, …) representing its
  position in the recovery order. Powered by the same epoch-sort logic
  the rotation engine uses.

### Number formatting (C-stream)

- **C-01/C-02 — Centralized `fmt` namespace**: All numeric renders now go
  through `fmt.n()`, `fmt.dollars()`, `fmt.tokens()`, `fmt.percent()`,
  `fmt.duration()`, `fmt.bytes()` in `src/shared/util/formatNumber.ts`.
  No more raw `.toLocaleString()` calls inside data-bound strings.
- **C-03**: Utilization bars show `87%` not `0.87`.
- **C-04**: Currency always renders as `$X,XXX.XX`; loading / missing data
  shows em-dash `—` instead of `$0`.
- **C-05**: Token counts use thousands-separator in full form and `1.2k`/
  `1.2M`/`1.2B` in compact contexts. Both forms via `fmt.tokens(n, {compact})`.
- **C-06**: Timestamps are UTC-formatted (`2026-05-11 14:32 UTC`). Events
  within the last 24h show relative format ("3 hours ago"); older events
  show the absolute UTC timestamp.
- **C-07**: Loading-state convention: em-dash placeholder, never raw `0`
  or blank while data is fetching.

### Cost projections (A-12)

- **`rollingWindowCost(run, prices, windowDays, now)`**: Rolling N-day (default 7) sum of
  `bucketCost()` for buckets within the window. Exported for the Usage tab "7-day total"
  panel.
- **`monthlyProjection(run, prices, now)`**: Daily average of the last 7 days × 30.
  Returns `null` when fewer than 2 distinct days have data (avoids misleading single-day
  extrapolations). Used by the Usage tab cost projection panel.
- **`annualProjection(run, prices, now)`**: Daily average × 365, same null guard.
- All three functions accept a `now: Date` argument (default `new Date()`) so tests can
  pin the clock without wall-clock sensitivity.

### Public-mirror repo + leak audit (E-02 follow-through)

- **`scripts/release/sync-public.sh`** (new): produces a filtered snapshot
  of the dev repo for the public-facing
  `github.com/neural-llm-io/power-claude` mirror. Internal release runbook
  documents the one-time GitHub rename plan separating dev and public
  trees. Drops
  `docs/internal/`, `docs/PUBLISH-PREFLIGHT.md`, `scripts/build/`,
  `scripts/release/`, `scripts/pre-commit/`, `scripts/setup/`, `test/`,
  `out-tests/`, `.mocharc.json`, `.claude/`, `.power-claude/`, `.vscode/`,
  `.vscode-test/`, `.github/`, `out/`, `bin/*.js`, `dist/`, `*.vsix`,
  `*.tsbuildinfo`, `node_modules/`. 260 tracked → **228 public files**.
- **Safety-net leak audit** on the snapshot OUTPUT: absolute maintainer
  home-directory paths, PEM private keys (with key body),
  `sk-ant-{kind}{digits}-{32+ chars}` Anthropic tokens, `sk_live_/sk_test_`
  Stripe keys, `ghp_/gho_/ghs_/ghu_/ghr_` GitHub PATs, `AKIA…`/`ASIA…`
  AWS keys, and any residual `scripts/build/` directory. Hits abort
  before the push.
- **`npm run sync:public`** (dry-run) and **`npm run sync:public:push`**
  (force-push to the public remote) wired into `package.json`.
- **`.gitignore` tightened**: `.claude/state/`, `.claude/projects/`,
  `.power-claude/state/`, `.power-claude/logs/`, `bin/power-claude-proxy.js`,
  `bin/power-claude-cli.js`, `bin/*.sha256`, `*.tsbuildinfo`, `.env*.local`,
  `.scratch/` are now ignored — the public-mirror sync output never gets
  recommitted, and runtime state stops leaking into commits.
- **`package.json` `repository.url` + `bugs.url`** point at the
  marketplace-facing public repo `neural-llm-io/power-claude`. The dev
  tree's git origin is documented to repoint at the separated private
  dev repo once the one-time GitHub rename completes (see internal
  runbook for the procedure).
- **`scripts/build/embed-public-key.js` and `docs/PUBLISH-PREFLIGHT.md`**:
  hardcoded maintainer-home-directory paths rewritten to repo-relative
  form so the dev-repo tree no longer leaks the maintainer's machine
  layout.
- **Dev-repo cleanup punch list** (manual, see launch-runbook): the
  existing `.claude/state/session-index.json` and
  `.claude/state/vscode-windows.json` are tracked stubs (2-commit history,
  small leak surface). Remove with `git rm --cached`. The new `.gitignore`
  prevents recurrence.

### Source-code protection hardening

- **`.vscodeignore` overhaul**: previous releases shipped a 9.9 MB / 264-file
  VSIX that included `.vscode-test/` (the downloaded VS Code test harness,
  ~120 `.d.ts` files), `.claude/state/` (local session/window state),
  `.github/` (CI workflows), `test/`, `out-tests/`, `.mocharc.json`, and
  `scripts/build/` (the obfuscation scripts themselves). Updated ignore
  list now excludes every one of those, plus `.power-claude/`,
  `scripts/release/`, `scripts/pre-commit/`, `scripts/setup/`, and any
  `.tsbuildinfo`. Verified output: **1.76 MB / 86 files**, runtime only.
- **`!**/*.d.ts` negation removed** — that single re-include line pulled
  every `.d.ts` under `.vscode-test/` back into the VSIX even though
  the directory was explicitly excluded. Declaration files are never
  needed at runtime; removing the negation closed the leak.
- **`build:prod` script added**: `NODE_ENV=production node esbuild.config.mjs`.
  Wires `sourcemap: false` and `minify: true` into esbuild so the bundle
  is minified BEFORE the obfuscator runs (~2 MB → ~520 KB pre-obfuscation,
  then back to ~1.9 MB after RC4 string-array + control-flow-flattening).
  `build:protected` now invokes `build:prod` instead of `build`.
- **Pre-publish leak audit** snippet documented in
  `docs/marketplace/launch-runbook.md` — single bash one-liner that
  packages a throwaway VSIX, greps for leak-prone paths, and fails the
  command if any are present. Run before every `vsce publish`.

### Marketplace assets (E-11)

- **Animated hero SVG**: `docs/marketplace/screenshots/hero-insight-graph.svg` — a
  GitLens-style session-lane visualization, vector-rendered so it scales
  faithfully from listing thumbnails (~280px) to full-screen marketing pages.
  Opacity fade-in animation when viewed live; the resting state is what
  rasterizes for static contexts.
- **Gallery screenshots (1–6)**: Six SVG/PNG pairs covering Insight Graph hero,
  Session Detail → Files, multi-track Timeline, Accounts table with rotation
  queue chips, Inline session blame, and Usage analytics. Listed in
  `docs/marketplace/listing.md` matched to filename, resolution (1280×720 for
  hero, 1280×800 for the rest).
- **Render pipeline**: `docs/marketplace/screenshots/render.mjs` discovers a
  local Playwright install (repo / global / npx cache), launches headless
  Chromium, and screenshots each SVG at 2× pixel density. Run once before
  `vsce publish`; commits PNGs alongside SVGs.

### Payment / licensing (E-14) — confirmed already shipped

The extension does NOT integrate with Stripe / Paddle / FastSpring. License
validation goes through the Neural-LLM License Gate at
`https://api.neural-llm.com/license/validate`. Server-side handler is
`com_neurallicense` on neural-llm.com, sourcing subscription state from
HikaShop via the NDP `ndp/data` Reader. No additional payment-processor work
needed for v1.0.0.

### Free-tier upsell prompts (E-13)

- **Proxy panel locked card**: When `licenseStatus.tier === "expired"` the
  Proxy panel in the Settings tab renders a locked-state card with an
  "Upgrade to Pro →" CTA and an "Enter license key" button instead of the
  live proxy controls.
- **Rotation Controls locked card**: Same gating for the Rotation Controls
  section — expired-tier users see an upgrade prompt; all rotation toggles
  are hidden until a valid license is entered.
- **Feature matrix**: `docs/marketplace/feature-matrix.md` documents the
  full Free vs Pro breakdown and all webview trigger points.

### Inline Session Blame (F-04)

- **Session blame annotations**: Right-of-line text renders the session ID,
  model, relative time, cost, and token count for files touched during the
  active session. Toggle via command or `powerClaude.sessionBlame.enabled`
  setting.

### Commands (A-06, A-07)

- **`powerClaude.openAccountLogs`**: Opens the last 30 handler-log events
  mentioning the selected account. Offers quick-actions to open the full
  handler.jsonl, tail with grep, or view combined.jsonl when no events match.
- **`powerClaude.openClaudeAi`**: Opens `https://claude.ai/settings/usage`
  in the system browser.

### Account lifecycle (A-09)

- **`expiredSubscription` status**: Accounts whose Pro subscription has lapsed
  now surface with a `PRO (EXPIRED)` badge and a "Renew" action button in
  the accounts table and sidebar tree. They are excluded from rotation.

### Tests (D-04, D-06)

- **Vitest unit test suite** (`test/unit/`):
  - `calc.test.ts` — 25+ cases for A-02/A-03: `todayDollarsBreakdown`,
    `todayDollarsTotal`, `bucketCost`, `bucketsForDate`, `todayUtcIsoDate`.
  - `jsonlReader.test.ts` — A-01: JSONL account attribution, profile-name
    resolution, malformed-line resilience, `pickBetterBucketSource` heuristic.
  - `assertSafeName.test.ts` — D-03: path traversal, forbidden chars,
    length bounds, label propagation.
  - `format.test.ts` — C-02: `fmt.*` helpers for dollars, tokens, percent,
    duration, bytes, numbers, delta.
  - `insight-cost.test.ts` — F-13: `computeSessionCost` arithmetic, model
    lookup, fallback pricing, subscription savings stub.
- **GitHub Actions CI** (`.github/workflows/ci.yml`): type-check → Vitest
  unit tests → VSIX package dry-run on every PR and main push. Runs on
  Node 18 and Node 20 matrices. Publish dry-run uploads VSIX artifact on
  main-branch pushes.

## [0.15.0] — 2026-05-11 — Proxy, Parallel Mode, License Gate

### Mission expansion

The first paid release. Power Claude moves from reactive (hook-based) to
**pre-emptive** rotation via a local HTTP proxy that intercepts every
Claude Code request, reads `anthropic-ratelimit-unified-*` headers in
real time, and rotates accounts BEFORE quota is hit. Parallel account
mode delivers the long-requested throughput multiplier: with N healthy
accounts, effective ITPM is Nx single-account. Subscription enforcement
via signed JWTs and embedded Ed25519 public-key verification.

### Added

- **Proxy core** (`src/proxy/`) — Node.js HTTP server (port 3456, no
  third-party deps) that proxies Claude Code requests to api.anthropic.com.
  Reads response rate-limit headers, tracks per-account quota, rotates
  pre-emptively at configurable threshold (default 0.98). SSE streaming
  passthrough preserved. State written to `~/.power-claude/state/` with
  flock locking compatible with the bash handler.
- **Parallel account mode** — distribute requests across multiple healthy
  accounts simultaneously. Modes: `single` (default), `round-robin`,
  `least-utilized`. Tunable pool via `powerClaude.proxy.parallelPool`,
  `parallelMode`, `parallelMinAccounts`, `parallelMaxConcurrent`. CLI
  configurator: `power-claude parallel` (interactive), `parallel
  add/remove <account>`, `parallel status`. With 3 healthy accounts in
  parallel, effective throughput is ~3x single account.
- **Account pinning** — lock rotation to specific accounts, plan tiers, or
  user-defined tags. CLI: `power-claude pin <account>`, `tag <account>
  <label>`, `serve --pin=<list>`, `serve --pin-tier=max`.
- **Rich CLI dashboard** — `power-claude list` shows a per-account table
  with plan tier, 5h/7d quota bars, reset countdowns, OAuth token expiry,
  pin/parallel flags. `power-claude status` shows a live operational
  dashboard with parallel pool distribution and throughput multiplier.
  `--json` for scripting.
- **Subscription enforcement** — License Gate server at gate.neural-llm.com
  issues short-lived (1hr) signed JWTs per machine fingerprint. Heartbeat
  every 5min with code-integrity hash verification. Client-side: proxy
  refuses to start without a valid license (30-min offline grace period).
  Forced version updates via server-side `minVersion`.
- **Build-time code protection** — moderate javascript-obfuscator applied
  to the compiled bundle. SHA-256 sidecar files (`out/extension.js.sha256`)
  uploaded to the server for code-integrity comparison. Embedded Ed25519
  public key for verifying signed gate responses (MITM protection).
- **Emergency Recovery** — `power-claude emergency` always-works command
  (zero dependencies, offline-capable) that stops the proxy, kills
  watchers, restores best-available credentials, clears stale state, and
  validates the token. Pre-rotation safety checks prevent bad credential
  swaps (atomic write via `rename()`, post-rotation probe with
  auto-rollback). Exhaustion-lockout countdown with auto-recovery.
  First-run onboarding banner. One-click emergency buttons in the
  VS Code extension Debug tab.
- **VS Code proxy integration** — auto-start the proxy on activate
  (gated by `powerClaude.proxy.autoStart`). Status bar shows live
  utilization. Tree view "Proxy" section with start/stop/status.
  Dashboard webview shows per-account parallel-pool gauges.
- **Hook fallback** — `scripts/hooks/rate-limit/handler.sh` now detects
  the active proxy via `proxy-status.json` mtime and defers rotation
  when the proxy is handling it. Seamless fallback when the proxy is
  down.

### Changed

- **Pricing fallback** verified against 2026-05 Anthropic published
  rates. No changes needed (Opus $15/$75, Sonnet $3/$15, Haiku $1/$5
  per MTok).
- **`.vscodeignore`** added — VSIX trimmed from 195 files / 2.07MB to
  ~75 files / 0.8–1.0MB. Source TypeScript, `node_modules`, dev configs,
  and unused brand assets are no longer shipped.
- **First marketplace publish** as `neural-llm.power-claude`.

### Security

- All license-gate responses signed with Ed25519. The client verifies the
  signature using the embedded public key. Tampered or replayed responses
  are rejected.
- JWT session tokens are never written to disk and are cryptographically
  bound to the machine fingerprint (`vscode.env.machineId` + OS
  identifiers).
- Max 2 concurrent sessions per license (home + work). The third
  activation terminates the oldest session.

## [0.14.0-dev] — 2026-05-10 — Insight Graph

### Mission expansion

Power Claude's fourth pillar lands: **GitLens-quality visualization of what
every Claude Code session changed.** Sessions become the central node of an
insight graph that joins commits, sub-agents, bug flags, plans, hooks,
rate-limits, and cost. Rotation, watchdog, and task-tracking remain pillars
1-3; the insight graph is the marketing wedge.

### Added

- **Session Detail webview redesign** (F-05) — four new tabs: **Overview**,
  **Graph**, **Cost**, **Hooks** added alongside the existing Files /
  Timeline / Resilience / Search / Notes / Metadata. The Overview tab
  surfaces every linked node type at a glance (commits, sub-agents, bug
  flags, plans, rate-limit events, lineage parent), plus key KPIs (model,
  duration, cost, tokens, files).
- **Insight Graph data joiners** (F-08…F-12, F-15) — pure data functions
  that link a session to its commits (via git refs), bug flags filed,
  rate-limit events fired, sub-agents spawned, plans drafted, and parent
  session (when auto-resumed). Live under `src/extension/insight/joiners/`.
- **Per-session cost engine** (F-13) — token-level cost computation
  (input + output + cache create + cache read) using live or fallback
  Anthropic pricing.
- **Inline Session Blame** (F-04) — GitLens-style annotation on the active
  editor line showing which Claude Code session most recently touched the
  file. Toggle via `powerClaude.toggleSessionBlame` (off by default).
- **File-session activity status bar** (F-21) — `$(history) N sessions ·
  Md active` for the focused file. Click to QuickPick into any touching
  session.
- **Insight Bundle export** (F-20) — button on every Session Detail
  Overview tab; writes the full session graph (linked commits, sub-agents,
  bug flags, plans, rate-limits, lineage, cost) as a shareable JSON file.
- **Insight Snapshot — Daily/Weekly markdown** (F-22) — new command
  `powerClaude.exportInsightSnapshot` aggregates every session in a chosen
  window (today / 24h / 7d / 30d) into a single markdown summary suitable
  for daily-standup notes or PR descriptions.
- **Outgoing Changes tab** (F-03) — new Changes tab in Session Detail that
  runs `git diff --name-status` between the session's start and end
  snapshot refs, groups files by directory, and shows A/M/D badges.
  Filterable via the same input pattern as the Files tab.
- **Multi-track Timeline tab** (F-06) — new Timeline tab replaces the
  prior stub. SVG-based synchronized tracks for Lifecycle, Hooks,
  Rate-Limit, Account, Sub-agents, and Commits. Hover any dot for detail.
- **Hot Files tab** (F-17) — new tab ranks the files this session
  touched by total cross-session activity. Heat color encodes how many
  workspace sessions have touched each file. Filterable.
- **Hover Cards** (F-07) — CSS popover primitive applied to commit-SHA
  and sub-agent references in the Overview tab. Rich hover preview with
  author, timestamp, tokens, cost.
- **Account rotation track in timeline** (F-18) — when the rate-limit
  rotator switches accounts during a session, the new account label
  appears on the timeline's Account track.
- **Public extension API documented** (F-19) — `PowerClaudePublicApi` is
  now documented in the README with examples for reading session state,
  contributing tabs, and registering session enrichers.
- **Hook-event ribbon** (F-14) — the Hooks tab in Session Detail now leads with a
  horizontal SVG ribbon showing every hook event as a colored dot on the session's
  time axis: green=pass (exit 0), yellow=warn (exit 1), red=block (exit 2+). A
  legend shows per-result counts. The detail table with phase, hook name, badge,
  and message follows below the ribbon.
- **Sessions Lane View** (F-02) — new command `powerClaude.openSessionsLaneView`
  opens a GitLens-Commit-Graph-style SVG panel where each row is a Claude Code
  session lane colored by model (Opus=purple, Sonnet=blue, Haiku=green). Yellow
  dots mark git commits made during each session. Time flows left-to-right. Click
  any lane label to open that session's full detail view.
- **Session History — faceted search** (F-16) — new collapsible "Session History"
  panel in the Sessions tab. Renders all indexed sessions (up to 300) as a
  searchable, sortable `dataTable` with columns for status, title/ID, model,
  age, duration, tokens, files, and tags. Filter chips scope by model family
  (Opus/Sonnet/Haiku/Unknown) and session status. Free-text search covers title,
  id, first prompt, and model name. Click any session ID chip to open its
  Session Detail view.

### Refactored

- Repository moved out of the NDP monorepo to its own standalone
  Neural-LLM repository for clean marketplace shipping.

## [0.13.1] — 2026-05-07 — Watchdog hotfix

### Fixed

- **Watchdog false-positive on healthy-idle sessions.** The
  heartbeat-stale rule fired on every active session ~2 minutes
  after the user submitted a message they were still composing a
  reply to. Heartbeats only tick on `PostToolUse`; pure text turns
  don't increment them; the JSONL itself is idle while the user
  composes. Added a guard: when the most recent semantic record is
  an assistant `end_turn`, the session is healthy-idle (waiting for
  the next user message) — heartbeat-stale is suppressed.
- **Watchdog auto-resume now silent by default.** Removed the
  QuickPick prompt from the auto-resume flow. The whole point of
  the plugin is uninterrupted automation — stopping to ask the user
  defeats it. The configured `powerClaude.resumePrompt` is injected
  silently. `ended_with_pending_tasks` triggers do NOT auto-resume
  (intentional pauses); they surface in the Sessions UI ⚠️ only.
- **New runtime command `powerClaude.sessionResumeWithPrompt`** for
  per-session manual resume with an editable prompt (InputBox).
  Available for future Sessions Explorer context-menu wiring; not
  surfaced in the command palette by design (per
  user requirement that auto-resume never prompts).

## [0.13.0] — 2026-05-07 — Continuous Automation

### Mission expansion

Power Claude is no longer "rotation + extras." The product is now organized
around three pillars of continuous, uninterrupted Claude Code automation:

1. **Multi-account rotation** (existing) — recover from rate limits in
   the active session without losing context.
2. **Session-resilience watchdog** (new) — recover from process kill,
   OOM, IDE crash, network drop, and tool truncation that the rotator
   can't see.
3. **Deterministic task tracking** (new) — three-state TodoWrite-derived
   status so a session that says "done" can be verified to actually be
   done.

Rate-limit rotation is now one mechanism, not the headline feature.

### Added

- **Session-resilience watchdog.** New `Watchdog` polls active sessions
  every 30 seconds and applies four detection rules:
  - **heartbeat-stale** — no `lifecycle:heartbeat` record in N seconds
    AND JSONL stalled. Catches process kill, OOM, IDE crash, network
    drop. Default 120s; configurable via
    `powerClaude.watchdog.heartbeatStaleSec`.
  - **tool-truncation** — last assistant record has
    `stop_reason: tool_use` with no follow-up tool_result and JSONL
    stalled. Catches mid-tool deaths. Default 60s; configurable via
    `powerClaude.watchdog.toolTruncationStaleSec`.
  - **ended-with-pending-tasks** — session ended cleanly via the Stop
    hook BUT `finalTodoStatus` shows pending or in_progress items.
    Surfaced in the UI; never silently auto-resumed. Toggle via
    `powerClaude.watchdog.flagIncompleteOnStop`.
  - **rate-limit** (existing path, unchanged) — `pending-recovery.json`
    triggers immediate auto-resume.
- **One-click resume QuickPick.** When the watchdog fires, the user
  picks: resume with the recommended prompt (reason-aware — heartbeat-
  stale, tool-truncation, and unfinished-tasks each get tailored
  wording), edit the prompt before sending, resume silently (no prompt
  injection), or cancel. Watchdog never silently injects prompts —
  user always confirms.
- **Inline JSONL lifecycle markers.** Three new hooks at
  `~/.claude/hooks/lifecycle/{session-start,heartbeat,session-end}.sh`
  append `{"type":"lifecycle",...}` records to each session's JSONL.
  Heartbeats are sampled (every 5th tool call by default) to keep
  transcript size bounded; `session_ended` includes the final TodoWrite
  status snapshot. Idempotent, exit-0-always, line-atomic via O_APPEND
  under PIPE_BUF.
- **Deterministic task-bundle completion.** New
  `src/sessionCompletion.ts` exposes `readTaskBundleStatus(jsonlPath)`
  / `readTaskBundleStatusSync(jsonlPath)` — returns
  `{ status: "complete" | "incomplete" | "unknown",
     unfinishedTodos: string[], totalTodos, ... }`. Sources strictly
  from the most recent TodoWrite snapshot in the JSONL — no
  linguistic guessing, no "looks done" heuristics.
- **Session Explorer three-state UI.** Tree icons and label badges
  reflect task-bundle status: `pass` icon + ✅ badge when complete,
  `warning` icon + 🟡 badge when incomplete, neutral when unknown.
  Tooltip lists the unfinished todo names so you can see what to
  resume before clicking.
- **Public API additions.** `PublicSessionInfo` adds
  `taskBundleStatus: PublicTaskBundleStatus` and
  `unfinishedTodos: readonly string[]`. Computed on demand via the
  256 KB tail read; existing `incomplete: boolean` is preserved as
  a derived alias for one release of wire compat.
- **Five new settings under `powerClaude.watchdog.*`** — see Settings
  reference in README. All configurable per-trigger.

### Fixed

- **`auto-resume-events.jsonl` was never populated.** The TypeScript
  reader at `src/autoResumeHistory.ts` looked for
  `~/.claude/state/logs/auto-resume-events.jsonl`, but the bash
  rotator at `~/.claude/bin/lib/rate-limit/events.sh` writes to
  `~/.claude/state/logs/rate-limit/events.jsonl` with a different
  field schema (snake_case `kind` / `session_id`, vs camelCase
  `event` / `sessionId`). Result: every Power Claude
  Self-Diagnostics report surfaced an empty array. The reader now
  reads the actual bash path and adapts the schema, including a
  reverse map from bash event kinds (`RATE_LIMIT_DETECTED`,
  `ROTATED`, `OPPORTUNISTIC_ROTATE`, etc.) to the typed event union.
  Unknown kinds map to `system_error` with the original kind
  preserved in `details.bashKind`.
- **Heuristic completion-detection retired.** The previous
  `detectIncomplete(jsonlPath)` tail-byte heuristic (last user vs
  last assistant) gave false positives on healthy sessions whose
  trailing records were `attachment` types (e.g. user typed but
  didn't submit a follow-up after `end_turn`). The deterministic
  TodoWrite scan replaces it. Existing `SessionSnapshot.incomplete`
  field remains on the wire one release for downstream consumers
  but is now derived from `taskBundleStatus === "incomplete"`.

### Migration notes

- **Lifecycle hooks now auto-install.** On first activation after
  upgrading, Power Claude prompts to install the three lifecycle
  hooks (bundled inside the .vsix at `scripts/lifecycle/*.sh`).
  Accept once; the extension copies the scripts to
  `~/.claude/hooks/lifecycle/` and registers them in
  `~/.claude/settings.json` (atomic read-modify-write, idempotent,
  never destroys unrelated entries). Manual install / re-install /
  uninstall via the command palette:
  - `Power Claude: Install Session Lifecycle Hooks`
  - `Power Claude: Uninstall Session Lifecycle Hooks`
  Opt out of the prompt via
  `powerClaude.promptInstallLifecycleHooks: false`. Without the
  lifecycle hooks the watchdog degrades to coarser JSONL-idle
  detection — still works but loses heartbeat / final-TodoWrite
  precision.
- `powerClaude.watchdog.enabled` defaults to true. Disable to
  silence non-rate-limit detection entirely; rate-limit auto-resume
  continues to work independently via the existing pathway.
- `incomplete` boolean fields on `PublicSessionInfo` and
  `SessionSnapshot.sessions[]` are deprecated in favor of
  `taskBundleStatus`. They will remain wire-compatible through v0.14
  but will be removed in v0.15.

## [0.12.0] — 2026-05-04

### Added — Session Explorer

- **Searchable session history with file linkage.** New activity-bar
  view (`Session Explorer`) lists every Claude Code session that ran
  in the workspace, grouped Pinned / Today / Yesterday / This week /
  Older / Archived. Each session is bidirectionally linked to the
  files the agent read, wrote, or edited — extracted from the JSONL
  transcript's `tool_use` events with no extra instrumentation.
- **Files Touched sidebar** — second tree view that follows the
  selected session and groups every file by Read / Written / Edited
  with op counts and last-touched timestamps. Per-row commands open
  the file or diff it against the session's git snapshot.
- **Session Detail webview** — multi-tab editor surface (Files,
  Timeline, Search, Notes, Metadata) with full-text transcript
  search, a markdown-editable notes pane that persists, and clickable
  diff actions per file row. Notes, tags, ratings, and pinned status
  persist in `<wsRoot>/.claude/state/session-tags.json` and survive
  index rebuilds.
- **Session Graph webview** (Cytoscape.js) — bipartite force-directed
  graph of sessions ↔ files. Edges colored by op type (Read/Edit/
  Write). Layout switcher with `dagre` (git-graph-style hierarchical
  lanes), `fcose` force-directed, concentric, circle. Op-type filter
  checkboxes, click-to-isolate node neighborhood, draggable nodes.
- **Pre-commit review webview** — diffs the working tree against the
  session's snapshot-end ref (`refs/power-claude/sessions/<id>/end`) file by
  file. Per-file Stage / Unstage / Revert (with confirm) / Open
  actions. Auto-generated draft commit message from session title +
  tags + file count.
- **Tagging + auto-tags.** User-applied tags (any string) plus 12
  auto-derived tags: `long-running`, `rate-limited`, `incomplete`,
  `abandoned`, `mvct-edit`, `domain-edit:<name>`, `test-edit`,
  `claude-md-edit`, `phpstan-edit`, `acl-edit`, `fix-only`,
  `read-only`. Auto-tags recompute on every index rebuild.
- **Search** — command palette `Power Claude: Search Sessions`
  (`Ctrl+Alt+S` / `Cmd+Alt+S`). Field filters (`tag:`, `model:`,
  `path:`, `status:`, `branch:`, `since:`, `before:`) plus free
  text. Backed by an in-memory inverted index that rebuilds on every
  session-index reload.
- **Per-resume prompt choice** — right-click → Resume opens a small
  picker ("Continue with prompt" vs "Resume silently") so resuming
  via the explorer can intentionally skip the configured wake-up
  prompt. New `powerClaude.sessionExplorer.rememberResumeChoice`
  setting (default `false`) caches the answer for the rest of the
  window.
- **Auto-archive support** — sessions whose last-active timestamp
  exceeds `powerClaude.sessionExplorer.autoArchiveAfterDays` (default
  `30`, set `0` to disable) are flagged archived and shown under the
  Archived group instead of Older. User-applied tags/notes/ratings
  persist regardless. `powerClaude.sessionExplorer.archivedGroupVisible`
  hides the Archived group entirely if preferred.
- **Persistence** — `<wsRoot>/.claude/state/session-index.json` (auto-
  built record store, capped at 1000 entries with prune-by-lastActiveAt)
  and `<wsRoot>/.claude/state/session-tags.json` (user metadata, never
  auto-pruned).
- **Resume / discovery / snapshot reuse** — the new module reuses the
  existing `powerClaude.resumeSavedSessions` plumbing, the existing
  `sessions.ts` discovery functions, and the session-snapshot ref
  reader extracted into `@vscode-extensions/shared/session/SnapshotRefs`. No
  new instrumentation in Claude Code itself.

### Implementation notes (monorepo-internal)

- New shared module: `@vscode-extensions/shared/session` (types, transcript
  parser, files-touched extractor, repository, indexer, tag store,
  search index, query parser). Other extensions can consume the
  module without invoking the rotator.
- New power-claude feature module: `src/sessionExplorer/` (tree
  providers, three webviews, command handlers, vendored Cytoscape +
  fcose + dagre layouts under `media/sessionExplorer/`).
- Pre-existing duplicate-case warnings in `src/webviewView.ts` are
  unrelated to this release and unchanged.

### Fixed (in-place on 0.11.3 — no version bump)
- **Fallback usage bar was permanently red 100% on every healthy
  account.** Root cause: the renderer collapsed two distinct
  Anthropic API states ("not signaled" and "unavailable") into a
  single "exhausted" rendering. The fallback header is missing on
  any account that hasn't been routed to the fallback model — which
  is the *normal/healthy* default — and treating that as exhaustion
  made the bar useless. Now three-state:
  - **`""` (header missing)** → idle slate `—` with tooltip
    explaining that fallback is dormant and this is the healthy
    default. No false-alarm red.
  - **`"available"`** → real `fallbackUtilization` heat-ramp bar
    with tooltip explaining the account has been routed to the
    backup model and this is how much of that bucket is consumed.
  - **`"unavailable"`** → red 100% bar with tooltip clarifying that
    BOTH primary and fallback are blocked until reset.
  - Stale session (reset elapsed) → bar suppressed, same as the
    session bar.
- Tooltips now describe what fallback IS (backup model like Haiku
  4.5 instead of Opus, why Anthropic routes to it, and what
  exhaustion means) instead of just emitting "available" /
  "unavailable" with no context.

## [0.11.3] — 2026-05-04 — second bug-hunt pass

### Fixed
- **`windowFirstRender` reset on every panel collapse + re-open**, so
  the user's selected tab was clobbered back to "sessions" with VS Code
  filter every time. Now persists via `context.globalState` — the
  default landing tab fires once on FIRST EVER render across this
  user's VS Code install, then never again.
- **`renderResumeSessionsInline` was called twice per render** (Overview
  + Sessions tabs), each invocation doing sync `readdirSync` + per-file
  `statSync` + 256 KB tail-reads on every active session. Now memoized
  per `renderBody()` — reset to null at the top, computed once,
  reused thereafter.
- **Legacy `[power-claude]` console prefixes + `class="power-claude"` body
  class + `power-claude-pulse` keyframe** all renamed to `power-claude`
  for marketplace brand discipline. No more "[power-claude]" warnings
  visible in the Output panel of a curious buyer.

## [0.11.2] — 2026-05-04 — bug-hunt fixes

### Fixed
- **Every LLM-Usage command was unregistered.** `registerCommandsWithLlmUsage`
  was defined but never invoked — every `powerClaude.refreshLlmUsage`,
  `openLlmUsagePrices`, `openLlmUsageData`, `openLlmUsageAnchors`,
  `saveLlmUsagePrices`, `resetLlmUsagePrices`, `addLlmUsageOverride`,
  `changeLlmUsageAccountPlan`, and `openUsageWebview` failed with
  "command not found." Clicking the LLM-usage status bar item threw.
  Wired the registration into activate().
- **Dashboard rebuilt HTML on every tab open/close anywhere in the
  window.** `tabGroups.onDidChangeTabs` was unfiltered; switching tabs
  in any group fired a full re-render after a 500ms debounce. Now
  filters to events that touch a Claude-Code or Anthropic tab.
- **Refresh storm from `~/.claude/state/` writes.** The home-dir
  `fs.watch` callback called `refresh()` synchronously, but the state
  dir holds many unrelated files (`vscode-windows.json` heartbeat
  every 15s from every VS Code window, `rate-limits.json`, cooldown
  sentinels, lockout files). Routed the home-dir watcher through the
  same `debouncedRefresh(200ms)` already used for the workspace
  watcher.

## [0.11.1] — 2026-05-04 — extension-host freeze fix

### Fixed
- **Extension-host freeze on activate against large `~/.claude/projects/`**
  (~1.5 GB / 424 JSONL files observed locally). The combination of
  `LlmUsageDataSource.readAll()` calling `readJsonlBuckets()`
  synchronously, plus `runAutoSnapshot` re-stat'ing every JSONL on each
  interval tick, plus the immediate-on-activate `rescanIfStale` /
  `syncLlmUsageIfStale` subprocess fires, was blocking the renderer
  long enough to trip VS Code's "window not responding" dialog.
- **`jsonlReader.ts`**: lowered `TOTAL_FILE_LIMIT` from 200 → 50 (worst-
  case read budget drops from 1.6 GB to 400 MB) and added a 60-second
  module-level result-cache TTL so back-to-back calls within the same
  minute reuse the prior aggregate instead of re-walking. New exported
  `invalidateBucketCache()` for manual-refresh paths.
- **`llmUsage/dataSource.ts`**: defers the JSONL bucket read by 5 s on
  first activation. The initial snapshot uses the upstream `data.json`
  numbers (which may undercount); after 5 s a timer triggers a refresh
  that runs the JSONL reader normally. Avoids racing the JSONL walk
  with VS Code's initial render.
- **`extension.ts`**: `runAutoSnapshot` now short-circuits when the
  Claude project directory's mtime hasn't changed since the last run
  (with a 5-min catch-all). The directory mtime ticks on session
  start/end/rename — i.e. the only events the snapshot cares about —
  so within an active session of continuous JSONL appends, we don't
  re-stat 424 files every interval tick.
- **`extension.ts`**: `rescanIfStale` and `syncLlmUsageIfStale` are no
  longer fired immediately on activate. Both now run on `setTimeout`
  (5 s and 15 s respectively) so VS Code's activation phase isn't
  competing with subprocess spawns + downstream JSONL reads.

## [0.11.0] — 2026-05-03 — recursive cleanup pass

### Fixed
- `recommend.json` schema gate now accepts both v1 and v2 (was rejecting v2
  files silently → "No recommendation yet" message even with populated 15KB
  recommendation file). Same fix for `prices.json` and `data.json`.
- Anchors panel now derives synthetic anchors from `recommend.json.coverage`
  when `anchors.json` is empty — was showing "0 recorded" forever.
- `_unknown` apiKeyId rendered as "Unattributed" with explanatory tooltip
  (was confusing literal `_unknown` text on cost-distribution chart).
- "UNKNOWN" plan tier replaced by "Auto" badge that resolves from the
  recommender's `currentPortfolio.accounts[].plan` when explicit override
  isn't set. Tooltip explains how to set the plan.
- Email truncation removed (account chips were chopping real addresses).
- Snapshot pills no longer render literal "red"/"green"/"yellow" — now
  show OK / Warn / Alert.
- "Refresh budget: 0/0" stub replaced with "— no data yet" when watchdog
  hasn't reported.
- Sessions filter default switched from "vscode" to "all" when no Claude
  Code tabs detected (was hiding all sessions on first paint).
- Auth-fail row pill contrast: dark-red pill with white text on saturated
  red row tint (was light pink on faint pink — invisible).
- Status timeline degenerate-sparkline guard ("need 3+ snapshots" message).

### Added
- ACTIVE-row indicator reworked as vertical edge accent (12px gutter cell
  with rotated label) — no longer wastes a column on every other row.
- "Next account available" hero meta laid out inline (dot + email + API on
  one row, was stacked column).
- Half-finished session detection — sessions whose JSONL ends with a user
  message and no assistant reply get a yellow ⚠ INCOMPLETE badge + row tint.
- JSONL-direct token bucket reader — when the upstream usage sync source
  undercounts (some sources cap at minimal token totals), the rotator
  falls back to direct read of `~/.claude/projects/*.jsonl`. Source badge
  in the LLM Usage header tells the user which path is providing numbers.
- Background freshness loop — periodically refreshes when data is stale.
- One-time, dismissible prompt to install the rate-limit anchor hook when
  `~/.claude/hooks/rate-limit/handler.sh` is missing the marker. Per-day
  per-workspace dedupe; never auto-modifies global Claude config without
  explicit consent. Opt-out via the dedicated configuration key.
- Hash-stable refresh dedup: countdown timers and timestamps stripped
  before hash comparison so "same data, ticked second" no longer triggers
  a full iframe rebuild.
- Scroll position preservation across iframe rebuilds (vscode.setState
  + restore on first paint).

### Changed
- Staleness banner thresholds raised from 60s/300s to 600s/1800s/3600s
  with new info tier (10min). Auto-rescan absorbs short-term lag without
  surfacing a banner.
- Refresh debounce raised 180ms → 500ms (fewer iframe rebuilds).
- Font-size floor: body min 13px (was inheriting 11px from some themes);
  worst sub-px sizes (9px, 0.65em) bumped to 11px / 0.78em.
- Marketplace metadata cleaned: marketplace-friendly description, useful
  keywords (claude, claude-code, anthropic, rate-limit, …).
- esbuild bundling — `out/extension.js` is a single self-contained CJS
  bundle (`vscode` is the only external).

## [0.10.1] — 2026-04-30

### Added
- Account rotation dashboard (accounts / sessions / history tabs).
- Cross-system links (git ↔ session refs ↔ events).
- Auto-deploy watcher — sentinel-based zero-friction "edit src → live
  extension" reload (opt-out via the auto-reload configuration key).
- LLM usage analytics sub-module.
