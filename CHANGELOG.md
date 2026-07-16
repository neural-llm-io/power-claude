# Changelog — Power Claude

Independent third-party software. Not approved, endorsed, or authorized by Anthropic.

All notable changes to the Power Claude VS Code extension are recorded here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.88] — 2026-07-15

### Fixed

- **Sessions list no longer dims or flickers** on every background data tick (lazy table no longer re-requests solely because filter chips exist; load state is a thin edge pulse, not a full fade).
- **Dashboard no longer freezes VS Code** when many sessions are indexed — session list prep is cached, active-window scans are short-cached, and poll/debounce intervals are less aggressive on the extension host.
- **Session detail drill-down includes Resume** so you can continue a session from the item view without hunting the tree menu.

## [3.0.87] — 2026-07-15

### Added — Flow Explorer (production surface)

- **Flow Explorer** is a real dashboard surface: session link graph, multi-agent fan-out, evidence panels, and analytics projections from live sessions (not sandbox-only fixtures).
- **Taken-path walk** and Combined flow join blueprint SessionStart/hooks to live runtime so the graph matches what actually ran.
- **Local-history + hook events** feed the explorer; CLI `pc flow` and fail-hard validation keep sandbox and production on the same contract.

### Fixed

- **Uninstall / purge** removes extension dirs and scrubs `extensions.json`; bare purge keeps the sentinel until the VSIX is gone so reinstall stays honest.
- **Onboarding**: CLI install no longer suppresses the VS Code Auto-Rotation walkthrough.
- **Sessions**: origin/model no longer invented; last-wins gateway routing; production-ready origin/model/index surface.
- **Auto-resume**: FP-safe candidacy predicate shared by UI and actuator (resume only when truly eligible).
- **Flow Explorer polish**: clear evidence panel on mode switch; payload attach honesty; real durations and extends parity.

## [3.0.86] — 2026-07-14

### Fixed

- **Dashboard account Usage column + per-account drawers** render again after a land dropped the UI helpers while leaving the call sites.
- **Session machine/client origin guards** — auto-resume could open sessions from other hosts or clients when origin detection failed; host/client checks work again so resume stays on the intended machine.

## [3.0.85] — 2026-07-14

### Added — Auto-Rotation Engine (opt-in)

- **Manual multi-account is the default.** You switch and manage your own Claude accounts; nothing rotates across accounts until you opt in.
- **Optional Auto-Rotation Engine** restores classic continuity when you turn it on: Power Claude can select the next healthy account from *your* pool when limits or health signals fire.
- **Clear risk path before enable** — firm grey-area warning and explicit acknowledgment (`pc rotation engine enable --i-understand`). CLI also covers `disable`, `status`, `warning`, `export-audit`, and `appeal-kit`.
- **Always-visible ON/OFF** in the CLI and status-bar tooltip, plus an onboarding step so the mode is never ambiguous.
- **Appeal Kit** templates and an optional scrubbed rotation audit export if you need a paper trail of how accounts were used.

## [3.0.84] — 2026-07-14

### Added — account groups (isolated context)
- Partition Claude accounts into named groups (Work / Personal / clients) with **isolated** projects/memory trees.
- Select an **active group** from the dashboard or `pc scope use`.
- Drag accounts between groups in **Your Profiles**; CLI: `pc scope create|add|use|list`.
- Guide on neural-llm.com (account groups / scopes).

## [3.0.82] — 2026-07-13

### Fixed — honest account status
- Accounts that fail authentication now show **Needs login** instead of looking healthy or only rate-limited.

## [3.0.81] — 2026-07-13

### Fixed
- Maintenance release — no user-visible product changes.

## [3.0.80] — 2026-07-11

### Fixed — CLI command listing
- Fixed CLI routing so cross-model session commands resolve correctly.

## [3.0.79] — 2026-07-11

### Fixed — shipping reliability + account status honesty
- Resolved build issues that could block a Marketplace release.
- Update notices open the correct Marketplace listing.
- Account status and response-summary styling fixes for clearer limits and login needs.

## [3.0.78] — 2026-07-10

### Fixed — CLI npm upgrade path
- CLI update notices now show `npm install -g power-claude@…` for terminal installs (not the VS Code Marketplace).
- Extension still points at Marketplace / Open VSX when a release is tagged and published.
- `postinstall` fails soft when merge-driver scripts are absent so `npm install -g power-claude` works for customers.

## [3.0.77] — 2026-07-10

### Fixed — marketplace listing media and walkthrough
- Marketplace listing media and Getting Started walkthrough steps match the official Claude Code workflow (no pool/proxy product claims).

## [3.0.76] — 2026-07-10

### Fixed — public listing copy
- Public README and listing copy use official-cli product language (no pooling keywords).

## [3.0.75] — 2026-07-10

### Fixed — marketplace listing and install package
- Marketplace README and Settings walkthrough no longer promote pooling claims.
- Install package no longer ships internal brand-asset guides customers do not need.

## [3.0.74] — 2026-07-10

### Fixed
- **License activation empty HTTP 500** — client surfaces empty-body server errors clearly; server aborts with JSON when the signing key is unreadable.
- **Claude account link after successful login** — discover credentials from CLAUDE_CONFIG_DIR, default path, and macOS Keychain (`Claude Code-credentials`); poll after `claude auth login` so Keychain/file lag no longer reports "couldn't read the new credentials".

### Notes
- Claude/Gemini OAuth credential handling remains provider-specific; multi-LLM API-key providers can keep independent credential flows.
- The same credential/activation fixes apply on maintained restore lines (version line may differ).

### Changed — Session search moved out of the status bar

The bottom-bar "Search Sessions" button has been removed. It was easy to mistake for another
extension's button and awkward to use. You can still search within your open Claude session
tabs — from the Command Palette ("Power Claude: Search Open Session Tabs"), its keyboard
shortcut (Ctrl/Cmd+Alt+Shift+S), or the dashboard Sessions list — all cleaner, more
discoverable places than a status-bar button.

## [3.0.73] — 2026-07-10

### Official Claude Code transport migration (public runtime)

> Technical remediation. Power Claude is independent third-party software — not approved, endorsed, or authorized by Anthropic.

### Changed
- **Public default transport is `official-cli`.** Power Claude launches and supervises documented Claude Code workflows. Claude Code owns authentication and communicates with Anthropic directly.
- **Claude Code profiles** replace managed OAuth credential swapping. Power Claude stores profile metadata (`CLAUDE_CONFIG_DIR` path, labels, session bindings) only — not access/refresh tokens.
- **Subscription usage limits pause the job** and notify. Automatic multi-account rotation / pooled consumer quota is removed from the public path.
- **Optional `anthropic-api` mode** for explicit pay-as-you-go API billing (user consent required; separate from subscription).
- **Legacy proxy** (`legacy-proxy`) remains internal-only (compile + runtime flags) and is not selected by default or as a fallback.

### Removed from public runtime
- `ANTHROPIC_BASE_URL` ownership pointing Claude Code at a Power Claude Anthropic proxy
- OAuth refresh / Bearer injection / request-body interception for account selection
- Preemptive and reactive consumer-account rotation past usage limits

### Unchanged (local orchestration)
- Session Explorer, worktrees, scheduling, watchdog, same-profile auto-resume, Token Saver (pre-CLI), dashboards, diagnostics, licensing

See product documentation for the official Claude Code transport model.

---

All notable changes to the Power Claude VS Code extension are
recorded here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and we use [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.72] — 2026-07-08

### Added — Scroll-to-top / scroll-to-bottom buttons in the Claude Code chat

- **New setting — `powerClaude.chatScrollNav.enabled` (default ON)** — shows two
 small purple floating **↑ / ↓** buttons on the right edge of the *Claude Code
 chat thread*. One click jumps a long conversation straight to its beginning or
 to the newest message, instead of scrolling by hand. The buttons only appear
 while the thread is actually long enough to scroll, so short chats stay clean.
- The buttons live on the chat itself (the surface you actually scroll), work in
 desktop VS Code and code-server alike, survive Claude Code auto-updates via
 Power Claude's self-heal, and respect `prefers-reduced-motion` — the jump is
 instant instead of animated when reduced motion is on.

## [3.0.71] — 2026-07-08

### Fixed — turns no longer stall on a request-caching error

A caching-order bug in the proxy could make a turn get rejected with a `cache_control` error and, because that looked like a normal stop, leave the chat sitting there until you manually continued it. The proxy now keeps the cache markers in a valid order — and guards against any future rewrite that would break them — so those turns go through, and token-saver and warm compacting stay on.

### Improved — auto-resume recovers from more interruptions instead of stalling

Auto-resume now treats recovery as the default for an interrupted turn — including authentication hiccups (recovered by rotating to a healthy account), request timeouts, and unexpected error responses — rather than only a fixed list of rate-limit codes. Genuinely non-retryable requests (a malformed 400/404) still surface to you instead of retrying in a loop. One shared policy now drives both the extension and the background hook, with a guard that keeps the two from drifting apart.

## [3.0.70] — 2026-07-07

### Improved — clearer savings and cost figures

Savings percentages and financial figures now round and format more consistently across
the headline and cost views, so the numbers read cleanly at a glance.

## [3.0.69] — 2026-07-07

### Removed — the `pc rotation-engine` command (it only ever reported a constant)

Power Claude has run a single rotation + auto-resume engine since the older engine was
retired on 2026-06-28, so `pc rotation-engine` had nothing left to report or switch — it
always answered "v2". The command has been removed from the CLI (and from the CLI
reference). Nothing is lost: if a leftover `POWER_CLAUDE_ROTATION_ENGINE` environment
variable, `powerClaude.rotationEngine` setting, or `state/rotation-engine` toggle is still
present from an old install, the proxy already detects it and tells you to clear it at
startup.

## [3.0.68] — 2026-07-07
### Changed — The CLI Command Reference tab is now point-and-click for everyone

You no longer need to know `pc` syntax to use it. Every safe command now has a
**Run** button, and commands that need a value collect it right there before you
run: commands that act on an account (remove, rotate, switch, re-login, pin, …)
show a **dropdown of your actual accounts** to pick from, and commands that take
a key, version, session-id, or file path show a **little box** you type into —
then Run. Nothing is ever guessed, and the **Copy** button is still on every row
if you'd rather grab the command and edit it yourself. The long list is now
organized into **collapsible sections** with a command-count on each, plus a
**live filter** box and **Expand all / Collapse all**, so you can jump straight
to what you need instead of scrolling. The kill-switch and "first 5 minutes"
sections open automatically.

### Added — Power Claude purple scrollbars

- **New setting — `powerClaude.scrollbarTheme.enabled` (default ON)** — themes VS
 Code's scrollbars in Power Claude's brand violet via the global
 `workbench.colorCustomizations` setting. VS Code has no per-extension or
 per-tab scrollbar API, so this necessarily affects scrollbars across the whole
 editor, not just Power Claude's own views — the setting description says so up
 front. Turning it off restores whatever you had before (your own colors, or no
 override at all) — it never deletes settings.json keys it didn't add. Applies
 and reverts live, no window reload needed. A one-time, dismissible
 notification explains the change on first apply.
- **Files**: `related module` (pure capture/apply/restore
 logic + brand colors), `related module` (globalState
 snapshot, settings listener, uninstall revert), `package.json` new
 "Power Claude: 🎨 Branding & Theme" configuration section, `related module`
 wiring in `activate()` and both `performFullUninstall` call sites.

### Fixed — The session "Lifetime" tab now draws a real workflow chart (was showing raw diagram text)

The Lifetime tab used Mermaid to draw the session's flow, but Mermaid can't
render inside the VS Code webview — so instead of a chart you got the raw
diagram source as text with an error notice. It now renders a clean,
left-to-right **workflow flow** of the session's legs (resumed-from → start →
prompt → work → sub-agent → rate-limit → recovery → end) with color-coded
connected boxes and labeled transitions, using the same reliable chart engine
as the Graph tab. The collapsible **Leg details** list below the chart keeps
every leg's full, untruncated detail (tokens / time / files / agents /
outcome), and the Mermaid source stays available via **Copy Mermaid**.

## [3.0.67] — 2026-07-07
### Added

- **`pc session set-note <id> <note> [--append]`** — set or append a session's freeform
 note from the terminal, the CLI peer of the Session Detail notes field (writes the same
 `SessionMetadata.notes` the editor reads). Primary consumer: the resume-stalled batch
 finisher, which now stamps each session it finishes with a provenance note ("resumed →
 merged to local main", "triage judged it already done", …) so the session list makes
 clear HOW each abandoned session was completed.

### Fixed

- **Session Graph tab is now readable instead of an overlapping tangle.** The
 interactive flow graph packed nodes far too tightly and let long labels overflow
 their boxes, so at narrow (code-server / mobile) widths it collapsed into an
 unreadable pile. Nodes now size to their content, the layout has real breathing
 room, and the graph fits itself to the viewport after every layout/expand. The
 **Mermaid** sub-view now renders an actual diagram (it previously showed raw
 Mermaid source); the diagram source is still one click away via **Copy**. The
 **Tree** sub-view is now a real collapsible tree — each branch (e.g. a sub-agent
 and everything it did) folds independently, with **Expand all** / **Collapse all**
 and a per-branch action count, so you can follow the agentic flow one branch at a time.
- **Session origin is now correct for VS Code / code-server sessions.** The Session
 History list mislabeled nearly every VS Code and browser (code-server) session as
 "CLI" — it fell back to an unreliable signal whenever Claude Code didn't stamp an
 explicit entrypoint (the case for ~89% of indexed sessions). It now consults the
 reliable client field first, so VS Code / code-server sessions are labeled and
 origin-filtered correctly (and become eligible for same-surface auto-resume).

### Added

- **Pin favorite sessions from the Session History list.** Each row now has a ⭐ pin
 toggle — click it to mark a session a favorite (or unpin it). A new **Favorites**
 filter lets you narrow the list to just your pinned sessions. Pin state is shared with
 the Session Explorer and detail view.
- **Started + Last-active dates in the Session History list.** The list now shows each
 session's actual start date and last-active (last-modified) date instead of only a
 relative age. Hover either date for the full start / last-active / ended timestamps
 and the session duration.
- **Per-leg detail list on the session Lifetime tab.** Below the lifetime diagram is a
 new collapsible **Leg details** list that shows every leg in order — start, first
 prompt, work, each sub-agent, rate-limits, recoveries, end — with its full,
 untruncated detail (tokens, elapsed time, files, agents, outcome) that the diagram
 boxes cut off.

### Changed

- **Session-list filters collapse behind a toggle.** The Origin / Status / Model filter
 chips now tuck behind a **🔧 Search Tools** toggle so the list isn't a wall of buttons
 by default; the chips for any filters you've actually applied stay visible. Combined
 with the new date columns (which are searchable), you can filter by day from the
 search box.

## [3.0.66] — 2026-07-07

### Changed

- **On/off settings for the recent Session features.** The Session Explorer
 "Copy Session Id / Name / Prompt" actions (`powerClaude.sessionExplorer.copySession.enabled`)
 and the `resume` deep-link handler that lets a `pc resume-stalled` session id open in a
 terminal (`powerClaude.resumeDeepLink.enabled`) can now be turned off — both on by default.
 (The tab session-id suffix already had its own toggle, off by default.)

## [3.0.64] — 2026-07-06

### Added — End-of-response status strips are now on by default, branded, and color-matched to the rest of Power Claude

The Landed / Remaining / Optional summary at the end of Claude's replies is now the
**default** experience (previously off), rendered as branded ⚡ Power Claude status
strips right in the chat:

- **⚡ Power Claude header** on the panel so it's recognizable at a glance (hover it
 for what each strip means).
- **A green "Complete" strip** — every multi-step reply now ends with a status, and
 when nothing genuinely needs you it shows *all requested work complete* instead of
 an empty box. So a clean session reads as done at a glance.
- **Remaining is now high-bar** — it lists ONLY things that truly need a decision or
 action from you. Routine standard steps (commit, push, publish, deploy) never clog
 it up, so you only read what actually needs you.
- **Colors now match the rest of the app** — the red / amber / green match the session
 status colors used on the tab icons, the session-history badges, and the Sessions
 panel (they used to be a slightly different, off-palette red and orange).
- **One opt-out** — a new *Response Summary: Enforce* setting (on by default). Turn it
 off to go back to a strip only when there's something to report. You can also switch
 rendering back to plain text (Response Summary: Render).
- **Reliability backstop** — a lightweight guard notices if a multi-step reply forgot
 its status strip. It ships in a silent observe-only mode (no behavior change);
 activate the nudge only after it's proven quiet on your own sessions.

## [3.0.63] — 2026-07-06

### Fixed — The "Fork timeline" now shows real detail at every leg (and was pointing at dead sessions)

The 🌳 Tree tab's **Fork timeline** used to render a wall of indistinguishable
rows — `→ Bash 3.6s`, `→ Bash 3.7s`, … — with no way to tell what each leg
actually did. Two problems, both fixed:

- **It was reading the wrong location.** After the trace store moved from
 `.claude/state/trace` to `.hurc-harness/state/trace`, the reader kept looking
 at the old path, so the timeline was showing long-finished sessions whose
 detail was gone. It now reads the current location (falling back to the old
 one only if that's all a workspace has).
- **Every leg now carries its detail.** Each row shows the exact command run or
 file touched (`Bash git status`, `Read cart.php`), a red ✗ on failures, a
 token count on sub-agent legs, and the wall-clock time — and **clicking a leg
 opens its full record** (the exact input, output, thinking, and per-turn token
 usage). The same detail lands in the terminal via `pc tree --source spans`.

### Added — Big dashboard tables now load lazily, with a "Neural Core" loading animation

The dashboard's large tables — the Sessions history list, the Events tab's
handler/proxy event stream, API request traces, recent commits, and session
refs, plus the session-detail Files and Hot Files tabs — now use lazy
server-model pagination: the extension host keeps the full dataset and the
webview receives only the page you are looking at. Searching, sorting,
filtering, and paging round-trip to the host, which computes the slice over
the *entire* dataset — so search now finds rows the old DOM render cap used
to hide, CSV export still covers the full filtered set, and a thousand-row
event log no longer ships (and re-ships, every refresh tick) a
multi-megabyte table to the webview. While a page fetch is in flight, tables
show the new **Neural Core** loader — counter-rotating violet/cyan arc
rings around a pulsing, glowing core with orbiting synapse dots — built on
the shared injectable-loader contract so every loading state in the
dashboard carries the same brand (and honors `prefers-reduced-motion` with
a gentle static pulse). Small fixed tables (Debug diagnostics, Live State,
Settings, Accounts) keep their instant eager render.

session detail (Files / Hot Files tabs).*

### Added — Session Graph tab is now a granular, chart-style flow of the whole session

The session-detail **Graph** tab now draws the *entire session flow* as an
interactive chart — the AI-workflow-visualizer view: every prompt, every
assistant turn, every tool call (with the exact command or file it ran on),
every sub-agent spawn, and every recorded decision is its own color-coded box,
annotated with its offset from session start, wall-clock duration, token
count, and estimated cost. Failed tool calls get a red ✗ border; commits,
plans, rate-limit events, and the auto-resume lineage parent attach to the leg
they occurred in. Long sessions stay fast: the chart opens at a readable level
of detail and dashed **▸ boxes expand on tap** (a turn reveals its tool calls;
an agent reveals its inner transcript), so the initial render never exceeds
the webview element budget — with an "Expand all" button when the whole flow
fits. Tapping any transcript-backed box opens the existing detail drawer
(exact tool input, output/stderr, thinking, per-turn usage, raw-JSONL deep
link). The tab's **Mermaid** view now exports the same granular flow as
copy/paste `flowchart TD` source for mermaid.live/docs, and the CLI gains
parity via `pc tree --format mermaid` — both emit identical source from the
same serializer. The **Tree** view remains as a dependency-free chronological
fallback.

### Added — Worktree lifecycle badges: see at a glance which worktrees are safe to delete

Every linked git worktree's root folder now carries a lifecycle badge wherever
VS Code renders file decorations (Explorer, tabs): a **link-blue ✓** means
LANDED — Power Claude verified the tree is clean and every file its branch
changed is byte-identical in local `main`, so deleting that worktree loses
nothing (the "it finished but never got cleaned up" case); orange **●** means
uncommitted work in progress; yellow **◆** means committed work not yet landed;
gray **D** means detached HEAD. The landed check is content-based, so
squash-style verified lands classify correctly even though the branch ref is
never an ancestor of main. Same accuracy contract as the LANDED response
strip: a badge is only shown when verified — probe errors show no badge rather
than a wrong one. Toggle via
`powerClaude.sessionAwareness.worktreeBadges.enabled` (default on).

### Added — Session Graph tab is now a granular, chart-style flow of the whole session

The session-detail **Graph** tab now draws the *entire session flow* as an
interactive chart — the AI-workflow-visualizer view: every prompt, every
assistant turn, every tool call (with the exact command or file it ran on),
every sub-agent spawn, and every recorded decision is its own color-coded box,
annotated with its offset from session start, wall-clock duration, token
count, and estimated cost. Failed tool calls get a red ✗ border; commits,
plans, rate-limit events, and the auto-resume lineage parent attach to the leg
they occurred in. Long sessions stay fast: the chart opens at a readable level
of detail and dashed **▸ boxes expand on tap** (a turn reveals its tool calls;
an agent reveals its inner transcript), so the initial render never exceeds
the webview element budget — with an "Expand all" button when the whole flow
fits. Tapping any transcript-backed box opens the existing detail drawer
(exact tool input, output/stderr, thinking, per-turn usage, raw-JSONL deep
link). The tab's **Mermaid** view now exports the same granular flow as
copy/paste `flowchart TD` source for mermaid.live/docs, and the CLI gains
parity via `pc tree --format mermaid` — both emit identical source from the
same serializer. The **Tree** view remains as a dependency-free chronological
fallback.

### Added — Link-blue LANDED strip: a trustworthy "work is on local main" signal

The end-of-response summary gains a third strip alongside 🟥 Remaining and 🟧
Optional: a **Landed** strip painted in your theme's link blue
(`textLink.foreground`, with a matching square icon) that appears only when the
assistant has *mechanically verified* its worktree work is fully merged to your
local `main` — an empty diff against main over its file set AND a clean
worktree, meaning you could delete the worktree and lose nothing. The
instruction the assistant receives makes accuracy mandatory: the strip may
never be emitted aspirationally, so blue present = landed, blue absent = not
landed — no prose-parsing required. Link blue was chosen (over the initial
teal) so the strip can't be mistaken for the success green used elsewhere.
Works in both render modes (`strips` paints the strip in the chat; `text` mode
uses a 🔵 LANDED line). Toggle via
`powerClaude.responseSummary.landed.enabled` (default on). Pushing to GitHub
remains your step.

### Fixed — "Chat connection lost" veil no longer pops up when the chat is just idle

The dead-chat recovery veil was appearing whenever the chat sat idle after a finished
turn — not only when the connection actually dropped. It now only appears while Claude
Code is genuinely mid-response but the stream has frozen, and it clears the instant the
turn finishes, so an idle chat never triggers it.

### Fixed — Rate-limit banner always shows the account (never Claude Code's raw one)

When Power Claude's local rotation proxy was momentarily unreachable, the in-chat
rate-limit banner could fall back to Claude Code's own "You've used N% of your weekly
limit" message — which is misleading with a multi-account rotation pool and names no
account. The banner now always shows a Power Claude message that names the last-known
account being served, even while the proxy reconnects, so you can always tell which
account a limit message refers to.

### Fixed — Session tab icons are more consistent

Power Claude's coloured state icon now shows on many more session tabs. It matches
each tab to its session by the session's title, and titles were only being filled
in for very recently-used sessions — so an older tab you'd reopened often showed
Claude Code's plain icon instead. Titles are now filled in for a much wider set of
sessions, and the icon no longer briefly flickers back to the plain one whenever
the background status connection reconnects.

### Changed

- **Documentation correction: Warm Compacting is free** — the docs previously (incorrectly) described Warm Compacting as license-gated. It has always run for free, no license required, same as Token Saver — this is a documentation-only fix, not a behavior change. There is no ongoing free tier: after the 7-day trial, a Pro subscription is required for multi-account rotation, the proxy, parallel dispatch, account pinning, and the watchdog.

 (AGENTS.md "Publish routes (SOP)"), each with a front-door script — Route 1
 releases from a fresh worktree at the main tip (`related module`,
 the mandatory default for agents) and Route 2 releases from a clean local main
 (`related module`, which refuses a dirty tree and points at the
 absorb SOP instead of loosening the no-clobber guard). No user-facing change.

 were tagged from unlanded worktree commits while local main sat at 3.0.56, and a
 union CHANGELOG merge scrambled newest-first ordering). `ship.sh` now enforces
 TAG-ON-MAIN (the shipped commit must be local-main history), MAIN-AGREES (main's
 package.json must equal the shipped version), CHANGELOG ordering/uniqueness, and
 runs the shared `version-check.sh --released` surface check; `release.sh` runs
 `version-check.sh` right after every bump; a new read-only
 `related module` (`make version-doctor`) reports cross-surface
 sync (main pkg ↔ tags local/remote ↔ CHANGELOG ↔ npm dist-tag) any day, and both
 publish-route front doors run it as preflight. The scrambled 3.0.60–62 CHANGELOG
 sections were reordered newest-first. No user-facing change.
### Added — Show the session id on its tab (optional)

Turn on **Power Claude › Custom Session Titles: Show Session Id Suffix**
(`powerClaude.customSessionTitles.showSessionIdSuffix`, off by default) to append a
session's short id — e.g. ` · a9cb7f06` — to its editor-tab title, so you can read and
reference the real session id straight from the tab. VS Code truncates long tab titles,
so the suffix may not always be visible; for the full id use **Copy Session Id** in the
Session Explorer or on a dashboard row.

### Added — Message Timeline: see the history of your own asks

A new command, **Power Claude: Show Message Timeline**, opens a panel listing
every message you've sent to a session, each with its timestamp — plus a summary
of how many there are, the timeframe they span, and the longest and typical gaps
between them. Each entry expands to show the full message. It's a read-only view
of your own side of the conversation, handy for retracing a long session.

### Added — Copy a session's id, name, or opening prompt

Right-click any session in the Session Explorer and choose **Copy Session Id**,
**Copy Session Name**, or **Copy Session Prompt Text** to put it on your clipboard.
Handy for referencing a specific session when you resume it, paste a
`claude --resume` command, or coordinate across sessions — the id is more
dependable than a title, which can change over time.

### Fixed — "Search Sessions" now works, and sits with the rest of Power Claude

The **Search Sessions** button in the status bar now reliably opens the search box and returns
results. Before, clicking it could appear to do nothing — if you had never opened the Sessions
view in that window, it was searching an empty index and silently finding nothing. It now builds
the index on demand (with a brief "indexing sessions…" indicator) before searching, and every
outcome lands in a visible panel instead of a toast that some setups suppress: if no Claude tabs
are open it searches all your sessions, and if a search comes up empty it offers to widen the
search rather than dead-ending.

The button also moved from the far-left of the status bar — where it looked like it belonged to
some other extension — to sit alongside the rest of the Power Claude status-bar items on the right.

### Added — A quick highlight shows which command you just copied

When you click **Copy** on a command in the Power Claude command list, that row now lights up
with a brief Power-Claude-orange sweep that fades out — so at a glance you can see exactly which
command landed on your clipboard. The same confirmation plays when you copy a session ID.

### Added — Clearer, colour-coded banners for important CLI notices

Important messages in the `pc` command line — an available update, and the rotation
kill-switch (emergency-off / rotation-disabled) — now render as distinct, colour-coded
banners instead of plain white text that blended into ordinary output. An available
update appears as a highlighted callout and the kill-switch shows a bold bordered box,
so an out-of-date or stopped rotator is impossible to miss. Colour is used only in a
real terminal — piped or captured output stays clean and readable, and `NO_COLOR` is
honoured.

### Added — A recovery veil when the chat connection drops (no more messages vanishing into the void)

When Claude Code's connection is interrupted — usually because the extension host reloaded or was
recycled (for example after an extension update, a window reload, or heavy load) — the chat can keep
accepting what you type while silently saving nothing: you send a message, it spins forever, and
everything you typed is lost on the next reload. Power Claude now detects this and drops a dismissible
purple veil over the chat that tells you the connection was lost and to reload the window — and it
**rescues the message you were typing**, copying it to your clipboard and showing it in the veil so a
reload never loses your words.

Turn it off or tune how quickly it triggers under Settings → Power Claude → Dead Chat Veil
(`powerClaude.deadChatVeil.enabled` / `powerClaude.deadChatVeil.stallSeconds`).

## [3.0.62] — 2026-07-02

### Fixed — Updating no longer freezes your running sessions; account list is accurate

Installing an update no longer restarts the editor out from under live Claude sessions
(auto-reload-on-install is off by default). The account list no longer shows usable
accounts as "cooling" — accounts with real headroom now show as available.

### Added — Force a rotation when the pool looks stuck

`pc rotate --force` (or `-f`) now switches to the best available account even when every
account reads "cooling", for when you know accounts are still usable.

### Fixed — The Sessions tab no longer freezes low-memory devices

Opening the Sessions tab on a workspace with a long history (hundreds to thousands of
sessions) could lock up the dashboard — on a phone browser it could freeze the whole
device. The list was building every session into the page at once (pagination only hid
the extra rows, it didn't remove them) and re-reading every session file on each refresh.
The table now renders your 200 most recent sessions (a banner tells you when older ones
are truncated — search and status counts still cover your whole history), the Events and
API-trace tables are bounded the same way, and per-session file reads are cached so a
refresh no longer re-scans your entire history.

### Fixed — Dashboard now fits small screens and narrow panels

The dashboard is now usable at phone widths and in narrow editor splits. The Runout
Forecast banner (previously unreadable on small screens) restacks vertically with a
full-width forecast track; the tab bar, account heat rows, usage cards, events table,
routing strip, and table toolbars all wrap or shrink instead of overflowing; popover
menus never open wider than the panel; and long URLs / IDs / env-vars break instead of
pushing the layout sideways.

### Added — One consistent session status everywhere, and you can set it yourself

Every place Power Claude shows a session's status — the dashboard Sessions list, the
editor tab, the in-chat session picker, and the Session Explorer — now shows the SAME
badge, colour, and label for a given session, from one shared source. Previously the same
session could look "saved" in one place and "abandoned" in another.

The Sessions list also counts correctly now. "Unfinished" and "Abandoned" were under-counting
(Unfinished often showed 0 even when you had unanswered work), and the list was capped at your
300 most recent sessions; it now classifies from your real pending-task and activity signals
and covers your whole history.

You can also set a session's status yourself: a small status dropdown on each row in the
Sessions list, on the session detail view, and a `pc session set-status` terminal command.
Mark a session complete, incomplete, abandoned, or archived — or "Auto" to let Power Claude
decide. A manual choice sticks until the session is next worked on, then returns to automatic.

### Fixed — Session badges no longer vanish from the chat session list after an update

When Claude Code updated itself in the background, the little status dots next to each row in
the in-chat session list could disappear until you reloaded the window. Power Claude now
re-applies them automatically after such an update.

### Fixed — Reloading or updating the extension no longer freezes your other sessions

Reloading the VS Code window or installing a Power Claude update could cut off every
running Claude session at once — the shared rotation proxy was shut down as the window went
away, even though a reload brings it right back seconds later. The proxy now stays up across
a reload and is re-adopted the moment the window returns, so your in-flight sessions keep
working. A proxy left behind by a genuine close (you actually quit, not reloaded) is cleaned
up automatically on the next launch, so nothing is left running for no reason.

## [3.0.61] — 2026-07-02

### Fixed — Updating Power Claude no longer freezes your running sessions

Installing an update no longer restarts the editor out from under your live Claude sessions.
Auto-reload-on-install is off by default; reload the window yourself after updating.

### Fixed — Account list no longer shows usable accounts as "cooling"

The account view could read "0 serveable / all cooling" while rotation was actively serving.
Accounts with real remaining headroom now show as available, matching what the rotator uses.

## [3.0.60] — 2026-07-02

### Fixed — Updating Power Claude no longer freezes your running sessions

Installing a new version no longer restarts the editor out from under your live Claude
sessions. Auto-reload-on-install is off by default; reload the window yourself after an update.
## [3.0.59] — 2026-07-02

### Fixed — Updating Power Claude no longer freezes your running sessions

Installing a new version could briefly freeze every running Claude session at "thinking"
for up to a minute and a half. The rotation proxy held onto its network port while it
waited for old streaming connections to close on their own — and they never did, so the
port stayed unavailable until the system force-killed it. The proxy now closes those
connections and shuts down cleanly in a couple of seconds, so an update no longer stalls
your in-flight sessions. A session that was mid-response at the exact moment of a restart
now recovers on its own instead of hanging.

### Changed — Automatic reload-on-install is now off by default

Power Claude no longer tries to auto-restart the editor the instant a newer build is
installed. That behavior proved unreliable — some editors can only load a new extension at
a full restart, and the auto-restart could disrupt live sessions. After installing an
update, reload the window (or restart the editor) yourself to pick it up. Developers can
re-enable the old behavior in Settings, but it now stays off unless explicitly turned on.

### Fixed — Reopened Claude tabs keep their session instead of starting empty

A Claude tab reopened after a window reload could silently come back as a brand-new empty
session — no error, no notice — even though the old session still existed. Claude Code's
native tab restore throws away the tab's saved session whenever it is more than 10 minutes
old, and a slow reload or a heavily loaded machine blows that window routinely. Power Claude
now extends that native restore window to 7 days, so a previously-open tab reliably comes
back with the session it had. Toggle: `powerClaude.sessionRestore.extendNativeTtl`
(on by default; off = the stock 10-minute behavior).

### Fixed — No more stalling when accounts are still available

Power Claude will no longer stop rotating and sit idle while healthy accounts remain. A
safety check that decided "all accounts are exhausted" was using a session counter that
several parallel sessions inflate together, so it could falsely conclude the whole pool
was spent while plenty of accounts were free. It now asks the rotator directly whether a
usable account exists before pausing — so with a pool of accounts, a single session keeps
moving instead of stalling.

### Fixed — Interrupted sessions now resume automatically after a rate limit

When a session was interrupted by a rate limit, it could sit waiting until you manually
resumed it. Automatic resume of the interrupted session is now on by default — Power
Claude picks the work back up on its own once an account frees up. (Automatic opening of
unrelated session tabs stays off, as before.)

### Fixed — Orphaned background services now clean themselves up

If Power Claude was ever installed to temporary or sandbox locations, leftover background
service entries for those now-gone locations could linger and produce a "stale service
detected" notice. Power Claude now removes those orphaned entries automatically whenever
it starts, so the notice no longer keeps coming back.

### Fixed — Reliable proxy connection when Power Claude runs from a non-default location

When Power Claude was installed to a custom home directory (advanced/sandbox setups), the
editor could try to reach the rotation proxy on the wrong port, showing "proxy unreachable"
even though the proxy was running. The editor, the proxy, and the command line now always
agree on the port, and the installer wires the correct location into your shell — so it works
the same whether Power Claude lives in the default spot or somewhere custom.

### Added — Session detail: the Token Tree, Graph, and Lifetime views now tell the whole story

The session Token Tree previously showed little beyond bare tool names. It is now a
collapsible, indented tree where every step carries rich context — what ran, what it
touched, tokens, timing — with a per-node detail drawer and deep links to related
sessions, files, and commits. The Graph tab now renders a real, populated flow of the
session (commits, sub-agents, plans, rate-limit events) in selectable view modes, and
the Lifetime tab draws the session's legs — including rate limits and recoveries — as a
readable chronological chart.

### Fixed — Session detail: Lifetime tab no longer shows a broken diagram

The Lifetime tab could show a "Syntax error in text" graphic instead of the session
chart. The chart now renders correctly, and in the rare case a diagram cannot render,
the tab shows the readable diagram source with a Copy button instead of an error
graphic.

### Fixed — The Getting Started walkthrough now opens correctly

The first-run walkthrough referenced step content that was not being packaged with the
extension, so opening it showed an "unable to read file" error. The walkthrough content now
ships, so the guide renders end to end.

## [3.0.56] — 2026-07-01

### Added — Detached Sessions: run as many in parallel as you actually use

Detached Sessions used to cap out at **4** turns running at once. That cap is gone —
set the limit to however many sessions you run in parallel (people running ~20 at a time
hit the old ceiling constantly). You control it under
*Settings → `powerClaude.detachedSessions.maxConcurrent`*; the default stays 1.
There's no hard cap now, but a recommendation of **≤ 64** is shown, because each detached
turn is a full Claude process that uses real memory and counts against your account quota.

### Added — see at a glance that Detached Sessions is working

When Detached Sessions is on, a **status-bar indicator** now shows how many detached turns
are running right now (and reminds you they keep going even if you refresh or close the
window). The dashboard's Rotation Controls card gained a matching live status line, and
every detached start / stop / completion is now recorded so the activity is visible instead
of happening invisibly in the background. Click the indicator to jump to the Sessions view.

### Fixed — per-message time chips now show reliably (especially in code-server)

The little send-time next to each chat message could silently stop appearing — worst when
you run many sessions at once, which is exactly when it's most useful. An internal version
mismatch was making Power Claude re-patch the chat view on every window, and with several
windows open those patches raced and wiped out the time chips. That's fixed, so the times
stay put.

## [3.0.53] — 2026-07-01

### Fixed — the CLI wires itself onto your PATH automatically

On install and update, the `pc` command is now linked into `~/.local/bin` (already on
your PATH) automatically — no more *"Power Claude CLI is not on your PATH, run
'power-claude install'"* prompt and no editing of your shell startup files. The
command-line tools (`pc rotate`, `pc watch`, `pc status`) just work right after install.

## [3.0.52] — 2026-07-01

### Fixed — Cursor / VSCodium / code-server now get the current version

The Open VSX marketplace (which Cursor, VSCodium, Gitpod and code-server install from)
had silently stalled on an older build, so those editors kept showing — and re-installing —
a stale version even though the VS Code Marketplace was current. This release re-syncs the
Open VSX channel so every editor serves the latest Power Claude.

## [3.0.51] — 2026-07-01

### Fixed — Updates now actually take effect (the proxy no longer keeps running old code)

When you installed a new Power Claude version, the extension would find the already-running proxy
"healthy" and keep using it — so the new code sat on disk while the **old proxy kept running**,
making every update look like it did nothing or "regressed." Power Claude now detects when the
running proxy is a different version than the one you just installed and **restarts it onto the
new code automatically** (safely — it will never restart in a loop). Updates take effect on their
own; no more manual proxy restarts.

## [3.0.50] — 2026-07-01

### Fixed — Usage Heatmap now shows real requests per account (not rate-limit hits)

The heatmap was plotting each account's rate-limit *hits* as if they were requests, so only the
2-3 accounts that happened to hit a limit ever appeared — accounts rotating cleanly and serving
traffic showed 0 and looked idle, making it seem like "only a couple accounts rotate." Power
Claude now tracks a genuine per-account, per-day request count and the heatmap plots that, so
every account actually carrying traffic is visible and the spread is honest.

### Fixed — Uninstall tears down every background writer up front

Uninstall now disposes all of Power Claude's background writers (leader-election heartbeat,
watchers, collectors) the instant an uninstall is requested — before removing files — so none of
them can re-create the data directory mid-removal.

## [3.0.49] — 2026-07-01

### Fixed — Your rotation-mode choice now actually takes effect (and the dashboard shows the truth)

The account-rotation strategy you select (Balanced / Round-robin / Smart) now reliably controls
how requests are spread across your accounts, and every dashboard panel shows the mode you
actually chose. Previously the mode was read from several places that could disagree, so
switching modes sometimes appeared to do nothing and one panel could say "Smart" while another
said "least-utilized."

### Fixed — Usage Heatmap updates live again instead of freezing on old numbers

Per-account request counts were no longer being recorded, so the heatmap sat on stale data.
They are recorded again, so the heatmap reflects current activity.

### Fixed — Uninstall now fully removes Power Claude

`pc uninstall --purge` could leave the data directory behind because a still-running editor
window immediately re-created it. The background leader-election now stops the moment an
uninstall is requested, so the purge sticks and Power Claude is actually gone.

### Fixed — Faster recovery after a temporary rate-limit

Restored the fast-resume path so, after the proxy rotates to a fresh account, your interrupted
session resumes promptly instead of falling into slow retry cycles.

## [3.0.47] — 2026-06-30

### Changed — Dashboard reorganized for clarity

The dashboard is cleaner and easier to read. **Settings** now shows only what you configure
(the VS Code Settings entry, routing mode, rotation safety toggles, auto-rewake, data
freshness). Live status moved to where it belongs: **System Protection Layers** and scan
diagnostics are on **Debug** (beside the live-state panel), and **Power Mode** status is on
**Overview** alongside "what's happening now". The **Sessions** list now shows each session's
name instead of a raw ID, the top-right refresh button is restyled, busy indicators clear the
instant work finishes (no guessed timeouts), and missing rate-limit fields now show an explicit
"MISSING" marker instead of looking like real zeros.

## [3.0.46] — 2026-06-30

### Fixed — Smart mode now fans a hard-limited account's traffic onto its peers right away

When an account hits Anthropic's short-term per-account rate limit (the "temporarily limiting
requests" response — not your usage cap), Smart mode now briefly steps that account to the back
of the line and sends the next request to a cooler account in your pool, then lets it rejoin
automatically a few seconds later. Previously a single busy session making one request at a time
could keep landing on the same account and re-tripping its limit while other accounts sat idle —
so you got throttled even though your pool had room. Load now spreads across all of your accounts
under sustained one-at-a-time traffic, not just during bursts.

## [3.0.45] — 2026-06-30

### Fixed — Account rotation now records every request, so it spreads load correctly

Power Claude forwards each request to a rotating account, but a state-file format mismatch meant
those forwarded requests were never recorded — so the usage dashboard sat frozen and rotation
couldn't make good "least-busy" decisions from stale numbers. Rotation now records every served
request again: the dashboard reflects real per-account usage and load spreads evenly across your
pool, reducing how often you hit a limit.

### Fixed — The dashboard is now readable in light editor themes

Power Claude's dashboard was tuned for dark editor themes, so in a light theme — for example
code-server running in light mode — many panels, status badges, and the LLM usage / cost tab
were washed out: light text on a light background. The dashboard now automatically detects
whether your editor is in a light or dark theme and adapts its colors to stay readable in both,
switching live the moment you change themes. Power Claude's brand styling (its orange accent and
status colors) is preserved.

### Fixed — The Usage tab's scaling & recommendation numbers are now statistically honest

The "All recommended options" table and the right-sizing cards on the Usage tab could show
impossible figures — thousands of "cap-hits per week" and tens of thousands of "throttle hours"
in a week that only has 168 — and could star a recommendation purely because it was the cheapest,
even when its own numbers said it would be heavily throttled. Two root causes are fixed: a
background counter of past rate-limit events grew without bound on long-running editors, and the
throttle math compared cached-token totals against billed-token limits. The estimates are now
built from the provider's own rate-limit utilization, are bounded to what is physically possible
(a weekly limit can be hit at most once a week; a week has 168 hours), and the recommended option
is the one that genuinely keeps you unthrottled — never just the cheapest. When there isn't yet
enough rate-limit data to estimate throttling, the table now says so ("insufficient data") instead
of showing a made-up number, and the "savings vs Max-200" card reports the honest figure for small
fleets instead of an inflated one. Per-account run-out ETAs are also more robust to a single odd
reading and can no longer show a time in the past. The per-account "plan burn" bar now measures
against the provider's own observed limit when that signal is available (labelled "observed" vs
"est"), and the scaling / what-if simulators note that their seat counts rest on community-reported
limit estimates rather than presenting them as exact.

### Fixed — Uninstalling on a server now fully cleans up on its own

When Power Claude is uninstalled in browser-based or remote editors (code-server, VS Code
Remote-SSH / server), the editor sometimes can't run its uninstall step — which previously left
Power Claude's background services running. The built-in watchdog now finishes the job
automatically: once it confirms the extension is gone, it fully stops and removes the rotation
proxy, the monitor timer, and the rest of the local machinery (your saved accounts are still
kept).

### Added — A branded "running" indicator so you can always tell a session is working

Power Claude now shows its own animated loader — a Power Claude lightning bolt inside two
counter-spinning rings — in the Claude Code chat whenever a session is actively working.
Claude Code's built-in "Thinking…" line only appears while the model is streaming and quietly
disappears during tool steps, which can make a busy session look stalled. The Power Claude
indicator keys off the persistent stop/interrupt control instead, so it stays visible for the
whole turn. Choose how it appears with the new `powerClaude.animatedLoader.mode` setting:
**append** (default — show it beside the native status), **override** (replace the native
status line), or **off**. Reload the VS Code window after changing it.

### Fixed — A brief rate-limit no longer makes a running turn look stopped

When one account hit a short, transient rate-limit mid-turn, that error could reach Claude
Code and end the turn — the working indicator vanished and the session was quietly resumed in
the background, so it looked stopped even though work continued. Power Claude now transparently
retries on another available account before the turn is ever interrupted, so a passing
rate-limit no longer breaks your flow. Genuine "all accounts are out of quota" limits still
surface as before.

## [3.0.42] — 2026-06-29

Intermediate same-day build during rapid iteration, immediately superseded by [3.0.45]. Its changes
are consolidated into 3.0.45 — install that instead. Recorded here so the version history stays
complete and correctly dated.

## [3.0.41] — 2026-06-29

Intermediate same-day build during rapid iteration, immediately superseded by [3.0.45]. Its changes
are consolidated into 3.0.45 — install that instead. Recorded here so the version history stays
complete and correctly dated.

## [3.0.40] — 2026-06-29

### Changed — A smoother first-time setup that opens itself

The very first time you install Power Claude, the setup guide now opens **on its own** right
after the welcome message — no extra click needed to get started. It also picks the right
format for where you're working: in desktop VS Code (and over Remote-SSH) it opens the built-in
"Get Started" walkthrough, while in browser-based editors like code-server it opens the welcome
page instead, so the guide always shows up correctly. You can still reopen it any time from the
"Setup Guide" button, the dashboard, the **Power Claude: Show Welcome Guide** command, or
`pc onboard` in a terminal.

### Fixed — Uninstall now removes everything it should

Uninstalling Power Claude (from the Extensions panel, `pc uninstall`, or "Uninstall Everything")
now fully stops and removes **all** of its background services — including the rotation proxy and
the hourly monitor timer — instead of sometimes leaving one running. It also clears stray
temporary files and writes a small receipt so a removal is verifiable. Your saved accounts and
data are still kept unless you choose a full purge.

### Changed — Clearer high-memory notification

The "high memory" notice now makes clear it is reporting the **shared** editor extension host
(every extension plus your Claude session history), rather than implying Power Claude itself is
leaking memory.

## [3.0.39] — 2026-06-28

### Added — See a session's whole lifetime at a glance

The session detail view has a new **Lifetime** tab: a clear top-to-bottom flow chart of
everything a session went through, in order — when it started and on which model, the first
prompt, the work it did (messages, tokens, files, commits), any rate-limit pauses and the
auto-resume that followed, watchdog-triggered recoveries (with what was rescued), and how it
ended. Each leg is colour-coded by type, and a compact lifecycle map alongside it shows where
the run finally landed. It turns "what actually happened in this session?" into a diagram you
can read in seconds — far clearer than the old node-and-line graph.

## [3.0.38] — 2026-06-28

### Fixed — Even rotation across all your accounts, and more reliable auto-resume

Requests now spread evenly across every account that has capacity, instead of piling onto
a few. The old routing could over-pick an account whose short-term window looked fresh even
though its weekly quota was nearly used up — concentrating load and triggering rate limits.
Routing now ranks by the tighter of your 5-hour and weekly windows, so no single account is
hammered while others sit idle. "Round-robin" mode is also fixed — it previously behaved like
least-utilized; it now genuinely rotates one account at a time.

Auto-resume after a rate limit is more dependable: a brief proxy hiccup no longer locks a
session out of its automatic retry, so interrupted work picks back up on its own instead of
stalling.

### Changed — One rotation engine

Power Claude now runs a single, cleaner rotation engine (the "v2" engine) for everyone. The
old engine has been fully retired, so there is no chance of silently falling back to it. The
developer-only `pc rotation-engine` command is now informational only.

### Removed

- The `powerClaude.rotationEngine` setting (there is only one engine now).

## [3.0.37] — 2026-06-27

### Added — Interactive Mode: the calibration feature is now wired end-to-end

Builds on the calibration engine + System Index (3.0.35):

- **Purple "⚡ Power Claude — Interactive Mode" modal** — a deliberately-distinct
 violet webview (not the normal Claude chrome) that asks one short calibration
 question; command `Power Claude: Calibrate a setting (Interactive Mode)`.
- **Auto-resume eagerness calibrates itself** — the modal + `pc calibrate` learn
 your preferred `autoNudge.aggressiveness` over time and set it for you; the
 result reaches both the extension (VS Code setting) and the Stop hook (mirror),
 reconciled on activation so a CLI-set value is never clobbered.
- **Always easy to turn off** — `powerClaude.calibration.enabled` (master),
 per-setting toggles, and the global `pc emergency off` all stop interviews
 instantly; the off control + "how to disable" are shown in the modal itself.
- **Onboarding "Tailor Power Claude" step** — pick a calibration posture
 (gentle / balanced / precise) during setup; shown in the CLI quickstart, the
 VS Code walkthrough, and the docs.
- **Just-in-time setup offers** — the first time a feature would help, a gentle
 one-time, dismissible offer to enable it (`powerClaude.jitSetup.enabled`).
- **Post-update "What's new"** — after an update installs, a one-time notice with
 a link to the changelog (respects `powerClaude.updateNotifier.enabled`).
- **Change a setting via chat** — a `change-setting` skill that reads the System
 Index, validates, confirms, and honours the kill switch before applying.

### Fixed — Even account rotation, reliable auto-resume, and a cleaner Events tab

- **Your accounts share the load evenly again.** Account selection now ranks each
 account by the _worse_ of its 5-hour and weekly usage, so an account that looks
 fresh on the 5-hour window but is exhausted for the week is no longer picked
 first. This ends the pattern where one or two accounts absorbed nearly all the
 traffic (and then hit limits) while the rest sat idle.
- **Sessions resume reliably after a brief reroute.** A turn cut short by a
 momentary throttle used to occasionally stop without resuming; it now continues
 automatically.
- **The Events tab shows what matters.** Once-a-minute internal housekeeping lines
 (no account, opaque message) no longer flood the feed, so rotations, account
 status changes, and sign-in events are easy to find.

## [3.0.36] — 2026-06-27

### Fixed — Dashboard sessions table: selection no longer lost on refresh, columns no longer cut off

- **Row selection now survives the dashboard's periodic refresh.** The Sessions
 table is rebuilt from fresh HTML on every data tick; the shared table primitive
 restored search / sort / page size across that rebuild but **dropped the checkbox
 selection**, so a checked row (or "select all") silently un-checked itself every
 couple of seconds and the "Resume selected (N)" count fell back to `0`. The
 selected row-ids are now persisted alongside the other table state and re-applied
 (with the count re-emitted) after each refresh, so selection and the count hold
 steady. (`related module`)
- **Wide tables no longer overflow the panel.** In a narrow side-bar the sessions
 table could push its columns off the right edge with no usable scrollbar ("data
 flows off the page, half cut off"). The table wrapper can now shrink to the panel
 and scroll horizontally within it instead of overflowing. (listing media)

## [3.0.35] — 2026-06-26

### Added — System Index (drift-free settings + features catalogue)

- **New single-source catalogue of every setting and feature**, generated from
 `package.json` `contributes.configuration` (settings) + `related module`
 (features) by `related module` (`npm run emit:system-index`). One
 generation produces three surfaces that can never drift: `data/system-index.json`
 (machine/agent), `docs/system-index.md` (human reference, publishable to the site), and
 `docs/agent-index.md` (agent how-to for changing a setting safely). A verify invariant
 (`related module`, auto-discovered by `npm run verify`)
 fails the build if any artifact drifts from the sources.

### Added — Interactive calibration engine foundation

- **Reusable, context-agnostic calibration engine** added to the shared library : converges on the best value for a setting from short user "interview"
 answers until a chosen confidence target is met (or a max-observations cap forces a best-so-far
 result). Generic over boolean/enum/ordinal/scalar/set; Wilson-bound confidence; priors that
 don't consume the interview budget. The basis for the upcoming interactive auto-resume/auto-nudge
 calibration and reusable for other "learn the user's preference over time" settings.

### Added — `pc calibrate` (interactive auto-resume eagerness calibration)

- **Power Claude now learns your preferred auto-resume eagerness over time** instead of making
 you find and tune the setting. A short, occasional interview (one prompt at most per
 session-end) converges on `powerClaude.autoNudge.aggressiveness` and writes it for you once it
 is confident. Distinct from `pc calibrate-nudges` (which only *reports* classifier behavior).
- Surface-aware write so the value takes effect everywhere: in the extension it updates the VS
 Code setting (which re-mirrors to the Stop hook); headless, `pc calibrate` writes the hook
 mirror immediately and queues a pending-apply the extension reconciles to the VS Code SSoT.
- Always dismissible: answer, `snooze`, or `never` (`abandon`) — and it stops asking once
 converged or after a hard cap, so it never nags. Consumes the shared shared calibration engine
 engine 

### Improved — `pc resume-stalled`: readable report, regression safety, never takes over an open session

- **The stalled-session list is now actually readable.** Instead of a flat bullet dump, the
 dry-run prints an aligned table — when each session was last active (local time), its age,
 repo, state, open-todo count, and the session id as a clickable link to its transcript — and
 after a real run you get a per-session report (what each one finished, what still needs you,
 what merged) plus a durable `<run>.report.md` you can re-open or share.
- **It won't regress old work.** Each session is resumed in a worktree branched from your
 *current* `main`, and the resume is now told, before it changes anything, to verify the task
 isn't already done (finished by a newer session or commit) and to never undo newer work — if
 the work is already there it reports "already complete" and exits without editing. Sessions
 that have been idle a long time get an intensified version of that check.
- **It will never take over a session you have open.** Open tabs were already excluded at scan
 time; now liveness is re-checked again at the moment of takeover, so a session you open in the
 gap between previewing and running is skipped (`skipped-now-live`) rather than hijacked.

### Fixed — Rotation reaches native-IDE sessions (no more "doctor green but still 429s")

- **Native VS Code (IDE) `claude` sessions now route through the rotation proxy.** Previously
 only shell- and code-server-launched sessions were routed; sessions launched from the native
 VS Code extension host ran with `ANTHROPIC_BASE_URL` unset, hit a single account directly, and
 got **no rotation and no multi-account bandwidth** — so you could see lots of 429s while
 `pc doctor` stayed green and the pool was healthy. `pc tune` now writes a **circuit-broken**
 proxy-routing block into `~/.vscode-server/server-env-setup` (probes the proxy once at server
 launch; falls back to direct if the proxy is down or a kill-switch is set, so a dead proxy can
 never strand the IDE). Takes effect on the next VS Code server relaunch.
- **Transient edge throttles no longer trigger pointless rotations.** An Anthropic edge throttle
 ("Server is temporarily limiting requests (not your usage limit)") arriving only in the
 assistant message was mis-promoted to a per-account usage cap and force-rotated, churning the
 pool and parking sessions. It is now correctly treated as transient (short wait, no rotation);
 genuine per-account caps still rotate.

### Added — `pc route-audit`

- New diagnostic the health check lacks: **are your live sessions actually using the proxy?**
 `pc route-audit [--minutes N] [--json]` reports, grouped by launcher, how many `claude`
 sessions route through the proxy vs go direct, the proxy upstream status histogram, the
 org-throttle-vs-per-account error split, and a root-cause verdict.

### Fixed — Dashboard accuracy, trial messaging, tooltips, jq dependency, anchor capture

- **Stale-data banner** no longer false-fires or renders the broken "Data is &lt;absolute date&gt;
 old" text. Freshness now comes from the rotation proxy's live heartbeat + the collector's
 embedded render time (never file mtimes), so the banner can only ever mean the proxy actually
 stopped — and it no longer overlaps the fallback-mode banner.
- **Free-trial banner** no longer promotes the "14-day Premium Trial" as if it were a *second*
 trial while you are already on the free trial. The founder-pricing offer is reframed as an
 upgrade, hidden in the final 48 h, and now honors the `POWER_CLAUDE_NO_TRIAL_BANNER` suppress
 flag (the CLI already did; the webview ignored it).
- **Tooltips** are now consistent UI-wide: SVG `title` attributes are pre-stripped (no native
 flash before upgrade) and the Session Detail panel loads the same styled tooltip system as the
 main dashboard.
- **`pc relogin` / rate-limit rotation** no longer dies with `jq: command not found` on a host
 without `jq`. A version-pinned, sha256-verified static `jq` is vendored and resolved
 automatically (a system `jq` still wins when present), so the 467-call-site shell layer is
 self-contained on any box.
- **Rate-limit anchor capture** now actually records. The cap-hit hook was sourced but never
 *called*; it is wired at the confirmed-rotation point, consolidated into Power Claude with a
 single home-relative `~/.power-claude/state/anchors.json` SSoT, and the "Capture status" panel
 reports the honest wiring state ("Armed" vs "Not wired") instead of crying "Inactive" on a
 healthy, just-quiet pool.

### Added — Finish every stalled session in one command (`pc resume-stalled`)

- New `pc resume-stalled [window]` command (and a Session Explorer button) that finds
 every abandoned or stalled Claude Code session in a time window (e.g. `30m`, `1d`,
 `1w`), resumes each in its own isolated git worktree in parallel, and merges the
 finished work into your local `main` — never pushed. It reads Claude Code's
 per-process registry first, so a session you still have open is skipped, never taken
 over. Each session is marked off with a one-line result (what it finished, or what
 still needs you). Transient rate-limits are retried with backoff rather than failing
 the session. Runs as a goal — complete only when every session is terminal.

### Added — Guided getting-started on your first CLI install

- Running `pc install` for the first time in a terminal now prints the same
 getting-started quickstart as `pc onboard` (install → activate → add account →
 rotate → safety), so a CLI / headless setup is actively walked through instead
 of getting only a one-line hint. It shows once per machine and is mutually
 exclusive with the VS Code first-run welcome banner — whichever you reach first
 onboards you and the other stays quiet. Repeat installs, piped output, and
 `--json` keep the quiet one-line nudge, so scripts and CI are unaffected.

## [3.0.34] — 2026-06-26

### Fixed — Rotation reaches native-IDE sessions (no more "doctor green but still 429s")

- **Native VS Code (IDE) `claude` sessions now route through the rotation proxy.** Previously
 only shell- and code-server-launched sessions were routed; sessions launched from the native
 VS Code extension host ran with `ANTHROPIC_BASE_URL` unset, hit a single account directly, and
 got **no rotation and no multi-account bandwidth** — so you could see lots of 429s while
 `pc doctor` stayed green and the pool was healthy. `pc tune` now writes a **circuit-broken**
 proxy-routing block into `~/.vscode-server/server-env-setup` (probes the proxy once at server
 launch; falls back to direct if the proxy is down or a kill-switch is set, so a dead proxy can
 never strand the IDE). Takes effect on the next VS Code server relaunch.
- **Transient edge throttles no longer trigger pointless rotations.** An Anthropic edge throttle
 ("Server is temporarily limiting requests (not your usage limit)") arriving only in the
 assistant message was mis-promoted to a per-account usage cap and force-rotated, churning the
 pool and parking sessions. It is now correctly treated as transient (short wait, no rotation);
 genuine per-account caps still rotate.

### Added — `pc route-audit`

- New diagnostic the health check lacks: **are your live sessions actually using the proxy?**
 `pc route-audit [--minutes N] [--json]` reports, grouped by launcher, how many `claude`
 sessions route through the proxy vs go direct, the proxy upstream status histogram, the
 org-throttle-vs-per-account error split, and a root-cause verdict.

### Fixed — Dashboard accuracy, trial messaging, tooltips, jq dependency, anchor capture

- **Stale-data banner** no longer false-fires or renders the broken "Data is &lt;absolute date&gt;
 old" text. Freshness now comes from the rotation proxy's live heartbeat + the collector's
 embedded render time (never file mtimes), so the banner can only ever mean the proxy actually
 stopped — and it no longer overlaps the fallback-mode banner.
- **Free-trial banner** no longer promotes the "14-day Premium Trial" as if it were a *second*
 trial while you are already on the free trial. The founder-pricing offer is reframed as an
 upgrade, hidden in the final 48 h, and now honors the `POWER_CLAUDE_NO_TRIAL_BANNER` suppress
 flag (the CLI already did; the webview ignored it).
- **Tooltips** are now consistent UI-wide: SVG `title` attributes are pre-stripped (no native
 flash before upgrade) and the Session Detail panel loads the same styled tooltip system as the
 main dashboard.
- **`pc relogin` / rate-limit rotation** no longer dies with `jq: command not found` on a host
 without `jq`. A version-pinned, sha256-verified static `jq` is vendored and resolved
 automatically (a system `jq` still wins when present), so the 467-call-site shell layer is
 self-contained on any box.
- **Rate-limit anchor capture** now actually records. The cap-hit hook was sourced but never
 *called*; it is wired at the confirmed-rotation point, consolidated into Power Claude with a
 single home-relative `~/.power-claude/state/anchors.json` SSoT, and the "Capture status" panel
 reports the honest wiring state ("Armed" vs "Not wired") instead of crying "Inactive" on a
 healthy, just-quiet pool.

### Added — Finish every stalled session in one command (`pc resume-stalled`)

- New `pc resume-stalled [window]` command (and a Session Explorer button) that finds
 every abandoned or stalled Claude Code session in a time window (e.g. `30m`, `1d`,
 `1w`), resumes each in its own isolated git worktree in parallel, and merges the
 finished work into your local `main` — never pushed. It reads Claude Code's
 per-process registry first, so a session you still have open is skipped, never taken
 over. Each session is marked off with a one-line result (what it finished, or what
 still needs you). Transient rate-limits are retried with backoff rather than failing
 the session. Runs as a goal — complete only when every session is terminal.

### Added — Guided getting-started on your first CLI install

- Running `pc install` for the first time in a terminal now prints the same
 getting-started quickstart as `pc onboard` (install → activate → add account →
 rotate → safety), so a CLI / headless setup is actively walked through instead
 of getting only a one-line hint. It shows once per machine and is mutually
 exclusive with the VS Code first-run welcome banner — whichever you reach first
 onboards you and the other stays quiet. Repeat installs, piped output, and
 `--json` keep the quiet one-line nudge, so scripts and CI are unaffected.

## [3.0.32] — 2026-06-25

### Fixed — Power Mode now spreads across your whole account pool

- Power Mode rotation routes each request across **all** of your serveable accounts
 instead of leaning on one, so usage spreads evenly across the pool. This is the fix
 for "I'm still getting rate-limited while my other accounts sit idle" — with a healthy
 pool, no single account is driven to its limit while the rest go untouched. What the
 proxy routes and what the dashboard's Power status shows are now derived from the same
 source, so they can never disagree.

- The running proxy is no longer interrupted when you reload or reactivate your editor,
 and a newer proxy can't be overwritten by an older one on reload — no more "rotation
 stopped working after a window reload" surprises.

### Changed — rotation engine rebuilt

- Rotation, health, and auto-resume now run on a rebuilt internal engine. Behavior is
 unchanged for you; it is simpler, covered by deterministic end-to-end tests under
 concurrent load, and every editor (VS Code, code-server) is now a thin view of one
 shared engine — so the engine keeps working no matter which editor you use.

## [3.0.31] — 2026-06-24

### Added — Export / Import accounts from the Accounts panel

- New **Export** and **Import** buttons on the dashboard's *Your Accounts* panel
 (and **Power Claude: Export Accounts** / **Power Claude: Import Accounts** in the
 Command Palette) let you move your whole account pool to another workspace or
 computer without re-logging in. Export confirms the credential warning and writes
 the bundle owner-only (`0600`); Import lets you choose whether to skip duplicates
 and rescans the dashboard automatically. This brings the VS Code surface to parity
 with the existing `pc export` / `pc import` CLI commands — both now share one
 implementation, so a bundle made on either side imports on the other.

### Fixed

- `pc import` (and the new Import button) no longer **overwrite** `~/.power-claude/
 profiles/.emails.json` with only the imported bundle's email mappings — the local
 mappings are now always merged in, so importing without `--dedup` can't drop the
 email identities of accounts you already had.

## [3.0.30] — 2026-06-24

### Changed

- **Re-login now steers you to the correct account.** When you re-authenticate a saved account, the OAuth screen now requests the account chooser, and the terminal shows a prominent reminder of exactly which account to authorize — with a note to click "Switch account" (or use an incognito window) if a different account is already signed in. Power Claude already verifies the authorized account against Anthropic and refuses to save a mismatch, so a wrong pick is never persisted; this just makes it easier to pick the right account the first time and avoid a wasted attempt.

### Fixed

- **No more "native fallback" while the proxy is healthy.** The routing layer now answers the health endpoint your editor probes, so a working proxy is correctly used instead of being bypassed to a direct connection.
- **No trivial stalls or parks.** A capacity/overloaded response rotates to another account or falls through directly instead of parking; a cold or stale-flagged account is probed rather than written off; and an account whose access token only needs a refresh is used (refreshed transparently) instead of being treated as dead — so far more of your accounts stay usable.
- **Development and production builds now use the same data home, ending a class of misrouting and persistent rate-limiting.** A development build used to isolate itself onto a separate `~/.power-claude-development` data home, which pulled the proxy port, the background hooks, and the emergency-stop switch out of alignment with the default home — so sessions could be routed to a nearly-empty account pool and stay throttled. Both build types now resolve the single default `~/.power-claude` home; sandbox/QA isolation is still fully supported through an explicit `POWER_CLAUDE_HOME` override.
- **Expired logins now correctly show "needs re-login" instead of the misleading "refreshable."** An account whose saved login was permanently revoked was displayed as "refreshable" — as if rotation could silently recover it — when it actually required a manual re-login. The dashboard now surfaces these accounts as needing action.
- **Self-healing rotation is much harder to break silently.** If the required `jq` tool is missing, install and `pc doctor` now say so loudly with the exact command to fix it — instead of letting rotation quietly do nothing while everything looked healthy. Stale background services left over from an earlier (different-home) install are now detected so they can be cleaned up, the hourly monitor service is pinned to the correct home, and `pc doctor` gained checks for `jq` and for the rotation system services. Background event logging also stays valid even on a box without `jq`.

## [3.0.29] — 2026-06-23

### Removed

- **The in-app Savings Calculator is gone.** The interactive ROI calculator — the adjustable "sessions / hours / accounts" sliders on the dashboard Overview tab that estimated a hypothetical "hours reclaimed per month" — has been removed. It modeled generic estimates rather than your real usage, so it added clutter without telling you anything about your account. The `pc savings` command keeps only the savings Power Claude has *actually* captured from local telemetry (Token Saver + File-Context Chip); its `--sessions/--hours/--accounts` flags are gone.

## [3.0.28] — 2026-06-23

### Changed

- **New installs and updates take effect in place.** Installing or updating Power Claude now hot-activates its runtime — evaluating and importing the install manifest with a safe fallback if in-place activation can't complete — so a freshly installed build starts working without a separate manual window reload. The status-bar tab-state legend is also clearer about the current rotation state.

## [3.0.27] — 2026-06-21

### Fixed

- **The local proxy is supervised as its own long-lived service.** The rotation proxy is owned by its own session/process group rather than running as a child of the editor window, so reloading or closing a window no longer tears the proxy down with it. Sessions keep reaching the proxy across window reloads instead of failing with "connection refused" until a manual restart.

## [3.0.26] — 2026-06-19

### Fixed

- **Rotation no longer freezes while the proxy is serving.** The Stop-hook rotation guard treated a missing `extension-active` sentinel as "extension disabled" and stopped rotating — but that single global sentinel is deleted whenever *any* window reloads, so one window reloading wrongly froze rotation for every other live window. Rotation now also accepts a live window heartbeat and a running proxy as proof the extension is active, so a rate-limited session rotates to a healthy account instead of looping on the limited one.
- **Stalled sessions auto-resume even without a prior recovery entry.** A session that stalled with no pending-recovery record was skipped by the auto-rewake watchdog; it now recovers (bounded by a per-session breaker), closing a class of "stopped and never resumed" hangs.
- **"Stop everything" reaches every data-home.** Emergency-off and emergency-on now write and clear the stop sentinel across all Power Claude data-homes, so a stop issued from one home reliably halts a proxy running under another (previously a stop could leave a second proxy still serving).

## [3.0.21] — 2026-06-16

### Fixed

- **Auto-rewake failure lookup.** The rate-limit auto-rewake hook now correctly identifies the failure entry by searching for the extension version in the failures file, preventing spurious "no failure found" bail-outs after a 429 recovery restart.

## [3.0.20] — 2026-06-13

### Added

- **Session Actions — one-click recovery on the line that broke.** When a turn dies with "Prompt is too long", Power Claude now detects the error on the chat line and injects a branded Heal button right there — click it and the session is trimmed and resumed automatically. Heal is the first of a family of Session Actions matched to how a session got stuck (Heal, Unstick, Revive, Re-run tool, Finish tasks, Resume, Repair turn). Every action is available three ways — the inline button, the `Power Claude: Session Actions` command, and the CLI (`pc session action heal <session-id>`) — and each is settings-gated (`powerClaude.sessionActions.*`). Manual by default; you stay in control.

## [3.0.19] — 2026-06-10

### Added

- Safe Install/Update Lifecycle — account data SSoT prevents data loss during extension updates.
- Display bucket model for account health with improved client detection.
- Configuration options for masking sensitive data and including API trace in Event Log.

### Fixed

- Resolve session client more reliably in Stop hooks.
- Respect focus gate when showing terminal for resumed Claude sessions.
- Update community fallback weekly token limits for max plans.
- Streamlined error handling in account token resolution.

## [3.0.17] — 2026-06-06

### Added

- **🧪 Detached Sessions (experimental · Pro).** Keep a Claude turn running when your browser tab sleeps, refreshes, or you close the window — the CLI's persistence, now behind Power Claude's graphical UI. The turn runs in its own systemd user service (its own cgroup), so a code-server refresh can't reap it; the dashboard reattaches and replays what you missed when you return. Default OFF; opt in from the dashboard's Rotation Safety Controls or the Setup & Optimize wizard. Requires Linux with a `systemd --user` manager.
- **Setup & Optimize wizard.** The first-run guide is now re-runnable any time (`Power Claude: Run Setup & Optimize Wizard`) and its "Optimize" step has one-click buttons that actually apply settings (auto-resume, Detached Sessions) instead of only describing them.
- **More ways to install Power Claude.** Beyond the VS Code Marketplace, Power Claude is now published to **npm** (`npm install -g power-claude` for the terminal / CI CLI) and **Open VSX** (Cursor / VSCodium / Gitpod / Windsurf), with a direct **`.vsix`** attached to every GitHub Release. Pick whatever fits your editor and workflow — it's the same extension everywhere.

## [3.0.16] — 2026-06-03

### Fixed

- **Tab Warming no longer creates duplicate "same chat" tabs.** When the optional Tab Warming preloader loaded your already-open Claude sessions after a window restore, each dormant tab could come back as a *second* copy instead of just loading the one you already had. Warming now reveals the existing tab in place (it can only load a tab, never reopen or duplicate it), so turning the feature on is safe. This is the load-only companion to auto-resume: warming just loads the sessions you have open, it never continues them.

## [3.0.11] — 2026-05-29

### Fixed

- **Auto-resume no longer opens your sessions in the wrong editor.** If you run Claude Code in more than one place at once — a desktop or Remote-SSH window, a browser code-server tab, a terminal — a session that paused in one could be re-opened as a tab in another. Each editor now only auto-resumes the sessions that actually started in it. (Cross-environment resume is still available, but it is now an explicit opt-in instead of the default, so nothing reopens where you didn't expect it.)
- **Rate-limit messages now describe what is actually happening.** A brief automatic retry is no longer worded as if every account had hit its usage cap with a long countdown. The message now distinguishes a short, transient throttle from a real 5-hour or weekly usage limit, and only shows a reset time when there genuinely is one.
- **Installing a new build now takes effect instead of silently reverting to the old one.** After an install, the active-version pointer the supervised proxy resolves its binary from is advanced to the newly installed build. Previously the install left that pointer on the previous version, so the supervisor relaunched the old proxy — the version appeared not to apply.
- **Dev builds now check the dev update channel, not production.** A development build now resolves its site and update-manifest URLs to the dev domain (matching where dev artifacts are published), so it polls the channel it was actually deployed to. Production builds are unchanged.

### Changed

- **Objective Mode is on by default.** A clearly multi-step request ("finish all the failing tests", "keep going until the build is green") now becomes a standing objective that Power Claude works toward, instead of stopping to hand you a remaining-tasks list. It stays token-light — a deterministic check decides continue-vs-pause, and only a genuinely ambiguous "is it done?" call ever consults a small, fast model — and it still stops for real blockers (a missing credential, an approval gate, a destructive action, a real decision). A one-off question never starts an autonomous loop. Turn it off with the `powerClaude.autoNudge.objectiveMode` setting.
- **Auto-resume decisions spend fewer model calls.** When a paused turn is clearly waiting on you ("say the word and I'll…", "your call", "I'll continue once the other session's edit lands"), Power Claude now recognizes it as a deliberate pause without consulting a model — so routine pauses are classified for free and the model is reserved for genuinely ambiguous cases.
- **The version label is consistent everywhere it appears.** The status-bar badge and the dashboard "Version:" chip render from one shared formatter, so their text and dev-build marking can no longer drift.

## [3.0.10] — 2026-05-26

### Fixed

- Maintenance and stability release.

## [3.0.9] — 2026-05-24

### Fixed

- Maintenance and stability release.

## [3.0.8] — 2026-05-22

### Fixed

- **Autocompact thrashing now actually auto-recovers instead of sitting stuck.** When Claude Code's own compaction loop fails — it prints *"Autocompact is thrashing: the context refilled to the limit… try reading in smaller chunks, or use /clear to start fresh"* and the session can no longer make progress — Power Claude detects it and recovers the session into a fresh, trimmed context automatically (the thrashed history is left behind; the new window is seeded with where-you-were summary + unfinished todos + files touched). Two gaps that previously left a thrashing session unrecovered are closed: (1) the thrash-recovery path was incorrectly buried behind the *mass-auto-open* dev gate (off by default in production because bulk session re-opening had shipped buggy) — it is now governed solely by its own dedicated `watchdog.compactThrashAutoRecover` setting (on by default), since single-session thrash recovery is a distinct, fault-confirmed path that opens a focus-preserving terminal (not a workspace tab); (2) recovery was a **one-shot** that got silently dropped whenever the session wasn't in the recovery index yet at the instant of detection — because a thrashed session emits no heartbeats, the internal "already handled" suppression could never clear, so the deferred recovery never retried. Recovery is now **retryable with a bounded budget**: a non-terminal outcome (index not ready, a transient engine hiccup) releases the suppression so the next watchdog tick retries, capped at five attempts (~a minute). When auto-recover is turned off, the thrash notice now carries a one-click **"Recover now"** action instead of a passive "go find the command" message.

## [3.0.7] — 2026-05-19

### Fixed

- Maintenance and stability release.

## [3.0.6] — 2026-05-17

### Fixed

- Maintenance and stability release.

## [3.0.5] — 2026-05-15

### Fixed

- **Action buttons now give instant feedback when clicked.** Clicking a slow action (e.g. "Start Proxy", which takes several seconds to bind) appeared to do nothing — the spinner was being silently reverted by the dashboard's background refresh before the action finished. The shared webview refresh engine now preserves in-flight buttons across refreshes, and the proxy on/off control clears its spinner the instant the proxy actually comes up or down. Applies to every action button.
- **"Your Accounts" no longer shows an account as available while also reporting "all accounts rate-limited".** A row could read healthy from stale data while the pool banner said the opposite. Account rows now degrade to a neutral "warming" state when there is no fresh measurement, so a row can never claim availability the pool doesn't have. The capacity banner also distinguishes a cold-start "warming up" pool from a genuinely rate-limited one (no more false "all rate-limited" on a fresh install).

### Changed

- **First-run welcome now tells you what was set up and what to do next.** The install notification reports the background services that were auto-enabled (Linux) and, when no Claude account is linked yet, prompts you to run `pc add` — the most common "it isn't working yet" gap. Buttons open the dashboard or the setup guide directly.
- **Power (balanced) mode is on by default** so rotation works the moment a second account is added, without a manual toggle.

### Build

- **Packaging now targets Node 20.** `.vsix` packaging (`vsce`) requires Node 20+ (pinned via `.nvmrc` 20.20.2 and `engines.node`); the previous Node 18 default crashed packaging.

## [3.0.4] — 2026-05-12

### Changed

- **Version numbering unified at 3.x — one source of truth across build, downloads, and changelog.** The shipped build number, the public download artifact, the release-status map, and the marketing changelog had drifted onto two parallel schemes (an internal `1.4.x` and a public `3.x`), which let a mislabeled artifact mark the real current build as deprecated. This release realigns the real build onto the public `3.x` line so every surface agrees on the same version going forward; the release-status map (`configs/releases/power-claude.json`) remains the single source of truth for which versions are downloadable vs deprecated.

## [1.4.13] — 2026-05-09

### Fixed

- **Blacklist-based auto-resume: unknown stop types now resume instead of silently stalling.** The prior whitelist approach only resumed sessions for explicitly classified error types. Two gaps: (1) unknown `api_error` entries in the transcript fell through a `*) : ;;` no-op and were never resumed; (2) `StopFailure` events where `handler.sh` didn't write `pending-recovery.json` exited immediately without checking account health. Fixed by flipping to a blacklist: everything resumes unless it is a known non-retryable client error (400/404/413), the session is explicitly stopped, or no healthy account is available. The old wedge-storm protection is preserved by the existing circuit breaker (CB_MAX_TRIPS=3 / 600s window) rather than the early exits.

## [1.4.12] — 2026-05-07

### Fixed

- **Sessions stalling after account quota reset — "no healthy account" false negative in auto-rewake.** When a 5-hour quota window rolled over, the scorer read the persisted `utilization5h=1` from disk without checking whether the reset epoch (`reset5hMs`) had already passed. Accounts were hard-blocked for the entire next window even though they were fully fresh. Added a window-reset guard in `scoreOneFromState` that zeroes `utilization5h`/`utilization7d` when `Date.now() >= reset5hMs` — mirroring the same logic already present in `quotaTracker.getLiveSession5hUtilization()` for the live proxy tracker. Previously only 2/13 accounts were selectable after a mass-exhaustion event; all 13 are now correctly recognised as available once their window resets.

## [1.4.11] — 2026-05-06

### Changed

- **Account rows are denser — more accounts fit on screen without scrolling.** The "Your Accounts" table rows previously stood about five lines tall for roughly two lines of content: the Status & Recovery and Usage cells each left a large empty vertical band. The cells now sit compactly at the top of each row with the inter-element gaps tightened, so the status pill, recovery line, progress bar, usage bars, and "N rate-limits today" footer keep all their information in a fraction of the height.
- **The "Paused" / dimmed cue when paid features lapse now applies only to the value panels — not the whole dashboard.** When a trial/license is expired, in offline grace, or payment-paused, only the paid-value surfaces (Power Mode status, lifetime-savings ribbon, throughput metrics, and the runout forecast) are visually muted with a small "PAUSED" tag. The account table, navigation, and the rest of the dashboard chrome stay at full clarity and remain fully interactive, so account management never looks disabled.

### Added

- **A one-time "Your trial ended — activate to keep Power Mode" dialog** appears when a trial or license fully expires (or a subscription is paused after failed payment). It has a single primary action (Activate / Update payment), a secondary "View pricing", and dismiss (×, Esc, or click-outside). It shows once per expiry state-change rather than nagging on every refresh.

### Fixed

- **Expired-state button noise reduced to one banner with one clear call to action.** When paid features lapsed, two stacked banners could appear at once with up to five buttons between them — including a contradictory "Power Mode requires a signed policy" notice beneath the "Paid features locked" banner. The redundant Power Mode banner is now suppressed in the expired case (the locked-features banner is the single source of the activation CTA), and the remaining license-required notices carry one primary (Activate) plus one secondary (Find my key) instead of three buttons.

- **"Running elsewhere" banner no longer false-fires on your own session.** The conversation-sync banner in the Claude Code chat ("Running elsewhere — N new messages from another window") used a window-blind gate: the proxy marks any live-but-idle session "runningElsewhere", which matches your own session between turns and Power Claude's own rate-limit auto-resume — producing alarming false counts (observed: "67 new messages" from one long agentic turn). Three changes: (1) a **render witness** is now the authoritative gate — an arriving transcript line is counted as "from another window" only if this webview provably did not render it within a settle window (own activity always renders here; a genuinely concurrent writer's lines never do until reload); (2) the count includes **only real conversational turns** (assistant messages and genuine user prompts — tool bookkeeping records are excluded); (3) sessions that Power Claude **auto-resumed after a rate limit** show an informative "Auto-resumed by Power Claude" notice instead of the misleading elsewhere-warning for 30 minutes after the resume (the rate-limit inject hook records the resume in the session's recovery history; the proxy publishes `autoResumed` on the session state). Both banner variants carry an explanatory hover tooltip.
- **Auto-resume now self-heals through full-pool saturation instead of looping.** When every pooled account is rate-capped (`all-accounts-exhausted`), the Stop-hook chain corroborates the saturation against the proxy witness feed and *parks* the session — no account burned — rather than resuming into a dead pool and re-failing every few seconds. It drives its backoff off the soonest projected account-reset time, defers the work-resume across cycles until the pool actually resets, and the saturation circuit breaker now truly pauses (clean stop) on a persistent wedge instead of re-triggering. Non-saturation stalls keep the immediate always-resume behavior.
- **"Retrying in 5s" that never restarted is fixed — every transient error now actually resumes.** When the Claude CLI surfaced a recoverable API error as in-transcript text (e.g. "API Error: Server is temporarily limiting requests… retrying in 5s") with no machine-readable error on the stop event, the auto-resume fallback only recognized a narrow set (timeout / overloaded / network / 5xx) and silently treated a 429 / "temporarily limiting" / "rate limit" / "throttled" / "too many requests" / "capacity" / "quota" / "usage limit" turn as a clean stop — so the session promised a retry and then stalled forever. The transcript-tail probe now covers the full Anthropic transient set, and the final resume/clean-stop gate was widened to match every stall token the chain can produce (incl. `proxy-down` and hyphenated/`overloaded_error` variants). Non-retryable 4xx (400/404/413/`invalid_request`) still fail fast; auth failures still recover by rotation.
- **Rate-limit messages are now unambiguous about what happened, what the system is doing, and when.** Previously the resume directive always claimed "the rotator already swapped to a fresh account" — even for transient server-error/throttle/capacity stalls where the *same* account simply waited out a brief cooloff — and the all-accounts case showed a vague "temporarily limiting" line indistinguishable from a single brief throttle. Messages now distinguish three cases explicitly: (a) **full saturation** — "all accounts at usage limit… parking until the soonest resets at ~3:47 PM"; (b) **rotation** — "rotated you to a fresh account, you have room now"; (c) **transient wait** — "a brief stall cleared on your current account, no switch needed." The proxy's synthetic-429 body (the text the CLI displays) was clarified to match, and the parked-session message states a concrete local reset clock time instead of a bare seconds count.

## [1.4.9] — 2026-05-02

### Fixed

- Maintenance and stability release.

## [1.4.8] — 2026-04-29

### Fixed

- **Usage popup: consistent account count** — Pool popup now always fetches live data on open instead of using the stale snapshot baked at extension start. Eliminates the "12 total" vs "13 accounts" discrepancy seen when accounts were added between extension restarts.
- **Usage popup: consistent "healthy" definition** — Pool endpoint's `healthyCount` now uses `serveableNow` (5h utilization < 80%) instead of the old 95% threshold, aligning it with the dashboard's account table and Stop-hook summary. Accounts at 80–95% utilization no longer show as healthy in the popup while appearing exhausted in the dashboard.
- **Usage popup: accurate legend and tooltips** — Legend and dot tooltips now state the correct 80% threshold instead of the legacy "default 90%".
- **sessionStateWatcher: `autoResumed` field added to hydrated path** — Fixes a TypeScript compile error where the `autoResumed` field added to `SessionState` was missing from the full-parse code path.

## [1.4.7] — 2026-04-24

### Added

- **🏷️ Version badge in the status bar.** A small `v<version>` item now sits at the
 far-right of the status bar, so you can confirm at a glance exactly which build is
 running — without opening the dashboard or dropping to the terminal.
- **🔬 Dev builds are now unmistakable.** When you are running an internal **dev**
 build (not the shipped customer build) it is marked everywhere it matters: the
 status-bar badge reads `v<version>-dev` on an amber background, the dashboard
 header chip turns amber and shows `-dev`, and `pc version` prints
 `power-claude <version> (dev)`. A dev build can no longer be mistaken for a release.

### Changed

- **Status-bar text is readable on every theme.** The rotation status bar used a
 fixed brand foreground colour that was low-contrast against the themed status-bar
 background (hard to read). It now uses the theme's own status-bar foreground, which
 is guaranteed to contrast — so the account counts, balance, and daily spend stay
 legible under any colour theme.
- **Releases auto-bump — the same version can never ship twice.** The release process
 now advances to the next free version automatically when no version is supplied, and
 refuses to re-publish a version that has already shipped (an existing release tag or
 a built artifact). Bumping the version is part of the process, not a manual step that
 can be forgotten.

### Fixed

 structured logger (no user-facing change).

## [1.4.6] — 2026-04-18

### Changed

## [1.4.4] — 2026-04-11

### Added

- **🔖 Version is now visible in the dashboard.** The panel header shows a
 `Version: vX.Y.Z` chip on every tab — the same value `pc version` prints in the
 terminal and the one the in-extension update check compares against — so you can
 always confirm exactly which build you're running without digging through
 Settings or the Extensions panel.

### Fixed

- **No more false "Running elsewhere — N messages from another window".** A
 session you have open in only one window no longer reads as if it's being
 driven somewhere else (which previously appeared right after a reload/reinstall).
 The window-liveness check now confirms the writing process is actually alive
 before attributing a session to "another window", so a reloaded window's own
 stale heartbeat — or a crashed extension host's leftover — can't trigger it.
- **Activation deep-links validate against the environment that issued the key.**
 A key minted by the dev site now activates against dev (and a production key
 against production), instead of always checking the hard-coded production
 endpoint — with the issuing origin allow-listed before use so a crafted link
 can't redirect activation to a hostile host.

## [1.4.3] — 2026-04-10

### Added

- **🚀 Getting Started — a real onboarding for the extension and the CLI, from
 one shared source.** First-run now opens a native VS Code **Walkthrough**
 ("Get Started with Power Claude": install → activate → add an account →
 start rotating → everyday safety), the empty Accounts panel offers a
 **Get Started** button, and two commands — **Power Claude: Open Getting
 Started** and **Power Claude: Open Documentation** — are available from the
 Command Palette. The terminal gets the same quickstart via **`pc onboard`**
 (aliases `pc welcome` / `pc getting-started`; `--markdown` / `--json`), and
 `pc install` now points you straight to it. Every surface — the walkthrough,
 the welcome panel, the CLI, and the online docs at
 **neural-llm.com/docs/power-claude** — renders from a *single* content source
 (`source`), so the steps can never drift apart, and each step
 links back to the online docs so you can return any time.
- **⑂ Live fork-level tracing — watch the agent's whole decision tree as it
 runs.** The harness now *emits* a structured span at every orchestration
 leg — each prompt, every tool call, every (recursively nested) sub-agent, and
 decision points — to a local per-session sink, **as it happens**. The 🌳 Tree
 dashboard tab gains a **Fork timeline** showing that live tree (sub-agents and
 their tool calls, with wall-clock per leg), and the terminal gains
 by default (zero overhead), and a tracing hiccup can never block or slow a
 tool — the worst case is a missing span. Because the model meters tokens per
 message (not per tool call), the spans capture **structure + timing** while
 token *cost* stays on the token icicle above; the two complement each other.
 Export the whole trace to any OpenTelemetry backend with
 `pc tree --otlp --source spans`. Emission is vendor-neutral (works under any harness LLM, not just
 Claude).
- **🌳 Token Tree — see exactly where your tokens go across the whole agent
 run.** A new view reconstructs a session's *orchestration tree* — every
 prompt, every main-loop turn, and every sub-agent (including sub-agents that
 spawn their own sub-agents, followed to any depth) — and rolls up token counts
 and an estimated cost at every branch. Branch width is proportional to tokens,
 so a runaway sub-agent or an uncompressed context jumps out at a glance.
 Available two ways: a **🌳 Tree** sub-tab on the LLM Usage dashboard (icicle
 chart, hover for input/output/cache-read/cache-write + cost), and a
 `pc tree [sessionId]` CLI for terminal/non-VS-Code use (`--metric cost`,
 `--top N`, `--depth N`, `--list`, `--json`). The dashboard tree **updates
 live** while a session runs — including while a long sub-agent is still
 accruing tokens — with a green **● live** indicator; it refreshes only when the
 active session actually changes, so an idle session costs nothing. Export the
 reconstructed tree to **any OpenTelemetry backend** (Grafana Tempo, Honeycomb,
 SigNoz…) with `pc tree --otlp` (OTLP/JSON to stdout) or
 `pc tree --otlp --otlp-endpoint <url>` (POST to an OTLP/HTTP collector; also
 honors `$OTEL_EXPORTER_OTLP_ENDPOINT` / `$OTEL_SERVICE_NAME`) — one span per
 node, sub-agents nested under their parent, reconstructed entirely from local
 data with no API key. Cache-read tokens are priced far below fresh input, so
 the cost view reflects real money rather than cheap cache hits, and
 streaming-snapshot duplicates in the transcript are collapsed so totals are
 counted once. Reads only Claude Code's local session transcripts — no cloud
 calls. 

### Fixed

- **Uninstall and Emergency Off now genuinely STOP everything.** Previously,
 uninstalling the extension or hitting Emergency Off left the background proxy
 serving and sessions auto-resuming — the spawned machinery outlived the
 trigger. Both now perform a real, provable teardown: the proxy is stopped
 (by PID and by process-name sweep, catching daemon-started proxies the editor
 never tracked), detached `claude --resume` processes are reaped, the watchdog
 is stopped, and the respawn + auto-resume signals (`proxy-mode.last`,
 `pending-recovery.json`, auto-rewake counters) are cleared so nothing
 relaunches on the next start. While Emergency Off is active, the proxy and
 `pc serve` now refuse to start (runtime kill switch, not just a status badge);
 Emergency On restores. The kill decision lives in one shared module consumed
 by both the VS Code extension and the `pc` CLI, so the behavior is identical
 whichever surface triggers it.

## [1.4.2] — 2026-04-04

### Fixed

- Maintenance and stability release.

## [1.4.1] — 2026-04-02

### Fixed — Rotation proxy no longer crash-loops on a fresh install with zero linked accounts

On a brand-new install the proxy treated an empty account pool as fatal and
exited, which under its `Restart=always` systemd unit crash-looped until
`StartLimitBurst` latched the service in a `failed` state. That latched state
survived reinstalls (it lives in systemd, not the extension), so a perfectly
good build looked broken — rotation silently never started and nothing listened
on the proxy port — until a manual `systemctl --user reset-failed`. Zero linked
accounts is now the expected first-run state: the systemd unit gates its start
on a non-empty `profiles/` directory (a skipped start is recorded as
condition-not-met, never a failure), and the launcher exits cleanly on an empty
pool. The proxy starts on its own the moment you link your first account.

### Fixed — `node`-less editors (Remote-SSH / code-server) resolve the editor's bundled Node everywhere

The proxy launcher and the cron watchdog now resolve Node through the same
canonical resolver the `pc` CLI uses (persisted editor execPath → PATH → nvm →
editor-bundled, including code-server's `/app/code-server/lib`). Their previous
inline copies missed the code-server layout, so a code-server install could fail
to (re)start the proxy even though Node was present inside the editor. `pc
doctor` also no longer reports a false failure for the `pc` launcher on installs
that use the wrapper-script form instead of a symlink.

### Fixed — Runout forecast no longer says "Pool runs dry in ~X" when the pool is ALREADY dry

When every account had been rate-limited and was on cooldown, the dashboard's
availability banner correctly read "0/N accounts can serve requests right now",
but the **runout forecast** headline contradicted it with a future countdown —
e.g. "Pool runs dry in ~2h 26m (all 12 accounts dry)" — a timer for an outage
that had already happened. Cause: the forecast measured exhaustion only from
Anthropic's utilization headers, while real availability is governed by the
rotator's cooldown status. A 429 puts an account on cooldown (unavailable *now*)
even while its 5h utilization header still reads under 100% (the header lags), so
a cooling account was projected from its burn slope as if it were live capacity
heading toward a *future* wall.

The forecast now treats any account the rotator can't serve from right now
(`cooling`, in addition to the existing `blocked`/`expired`) as being at the wall
*now* — so an all-cooling pool reports "Pool is dry — all N accounts exhausted"
(present tense) and the recovery clock ("Next window resets in …") carries the
wait. A cooling account that is also at its utilization cap keeps its **MAXED**
chip; a sub-maxed, transiently-rate-limited one now shows **cooling** instead of
a misleading future ETA. Mixed pools are unaffected: cooling accounts no longer
count as available capacity, so surviving healthy accounts still read "Pool stays
available". Regression tests now exercise `cooling` accounts directly and assert
the forecast↔availability invariant the suite previously never crossed.

### Added — Token trip odometer (resettable, per-project usage counters for client billing)

The LLM Usage tab gains a **💰 Trips** sub-tab: resettable, *named* token-usage
counters that work like a car's trip odometer. Start one per client or project,
and it tracks tokens burned from that point — independent of the lifetime /
today / 7-day totals. Each trip shows tokens (in / out / total), an estimated
$ value for invoicing reference, and elapsed time. Reset zeroes a trip in place
(keep billing from now), Close freezes its total, and you can run several trips
at once and delete finished ones. Trips persist across reloads
(`~/.power-claude/state/token-trips.json`) and derive their odometer from the
existing daily-token ledger, so the feature adds **no** proxy overhead. The list
renders through the shared paginated table primitive.

### Fixed — Auto-resume no longer re-fires on a finished turn's own summary (stale "Thinking…" footer)

When a completed turn ended with the structured response summary — the "Your
Request" banner, the "What I did" list, and a "⚠️ REMAINING TASKS" block — the
stop-classifier read that banner's "REMAINING …:" header as in-scope work and
auto-resumed the turn. Because that re-prompt starts a real turn, Claude Code's
own "Thinking… / Esc to interrupt" footer stayed lit after you'd stopped, making
it look like work was still in progress (Power Claude can't repaint Claude Code's
native footer; its only lever is whether to re-prompt). The REMAINING TASKS in
that block are, by the banner's own convention, items needing *you* — not work to
continue.

Auto-resume now strips Power Claude's own summary scaffolding from the text
before classifying, so a finished turn parks (the footer clears) while genuine
mid-work continuations ("I'll wire up the fix next") still auto-resume. The
stop-classifier itself is unchanged (it stays vendor-neutral); the fix lives in
the Power Claude tail-extraction layer.

### Changed — Account & Usage popup now shows a true pool-wide utilization aggregate

The "Pool best utilization" section was renamed and split, because a single `0%`
(the most-available reserve account) sitting above a list of accounts at 58–89%
read as broken data. The popup now shows two clearly-labeled sections:

- **Pool utilization** — a capacity-weighted aggregate across the whole pool.
 Each account is weighted by its plan-tier token capacity (Pro / Max-5x /
 Max-20x), so the figure equals total tokens used ÷ total pool capacity — the
 honest "how loaded is my whole pool" number, not a naive mean that would treat
 a Pro account and a Max-20x account as equal-sized. A muted "busiest: …" line
 names the single most-utilized account for context.
- **Most-available** — the lowest-utilization healthy account, the one rotation
 routes to next, now shown with its account name. A low or `0%` value here reads
 correctly as available reserve headroom instead of an apparent pool total.

`pc status` gained a matching `Pool util:` line, so the CLI and the popup report
the same aggregate from one shared computation.

### Fixed — Concurrent-session ("double-launch") guard no longer false-alarms on VS Code reloads

The launch-agnostic double-launch guard warned on a *dying* `claude --resume` process whenever a VS Code window reloaded or a session was re-resumed: the prior driver (plus its MCP-server children) takes longer than the old single 2-second grace to tear down, so for a moment it looked like a second live driver — then it exited seconds later. The guard now (a) consults the heartbeat sidecar for parity with `liveness.ts` (a fresh owner heartbeat means the session is already owned, so the warning is suppressed) and (b) replaces the single 2s sleep with a bounded exit-poll (up to 6×1s, inside the hook's 8s timeout) that suppresses the instant the foreign driver drains. A genuinely persistent concurrent driver still warns.

### Changed — Auto-resume is now deterministic-first, with item-level triage and an audit view

The trivial-stop auto-resume gate was rebuilt. Previously it leaned on an LLM
confirmation for the two highest-value cases ("I'll continue…" and "remaining
tasks…") — but that confirmation called the API with a raw key, so on a
subscription/OAuth setup it silently never ran and those stops never resumed.

What's new:

- **Deterministic-first decision.** A tier engine now classifies every stop
 locally with **no model call** for the common cases: clear trivial
 continuations resume immediately, genuine stops (a real question, a
 completion summary, "what would you like to work on?", an open approval gate)
 stay parked, and only a genuinely *mixed* remaining list escalates to a model.
 Across a large sample of real stops the model is consulted on only ~4% of
 them (balanced mode).
- **Item-level triage on mixed lists.** When a stop mixes work the agent can
 finish now with items that need you (a commit, a deferred decision, a peer
 session's files), it now **does the safe subset and defers the rest** to you,
 instead of parking the whole thing.
- **Works without an API key.** The model call for triage now uses the same
 transport the agent itself uses (the local rotation proxy, then an OAuth
 profile), so it works on subscription setups.
- **Configurable aggressiveness** — `powerClaude.autoNudge.aggressiveness`
 (`conservative` | `balanced` | `aggressive`).
- **In-chat marker + audit view.** Auto-resumed turns are marked with a `↻`
 header in chat, and **Power Claude: Auto-Resume Audit** opens a report of
 which sessions/turns were resumed, parked, or escalated (with the triage
 split).
- **Calibration:** `pc calibrate-nudges` replays your real stops (or a labeled
 fixture) through the classifier to tune behavior before changing it.

### Fixed — Sessions killed by a transient transport failure now auto-resume again

A regression left the bash **resume engine** (`handler.sh` + `auto-rewake.sh`)
unregistered from the Claude Code Stop hook — only `session-end.sh` and
`auto-nudge.sh` were wired. Because `auto-nudge.sh` deliberately *vetoes* bare
"API Error" tails on the premise that the resume engine handles transport
recovery, the veto was handing off to nothing. When the proxy restarted under
in-flight requests (the "socket connection closed unexpectedly" class), the
interrupted sessions died and **none auto-resumed** — they sat waiting for a
manual dashboard resume.

- **The resume engine is wired again, and it self-heals.** `handler.sh` →
 `auto-rewake.sh` are now registered on both `Stop` and `StopFailure` by the
 rate-limit hook registrar (`related module`), with `rate-limit-*`
 markers so the lifecycle installer leaves them intact and every re-install
 refreshes rather than duplicates. handler.sh runs first (it classifies the
 stall and writes `pending-recovery.json`); auto-rewake.sh polls for that entry
 and re-wakes the session in place via `exit 2`.
- **In-place resume, no wrong-workspace tabs.** The bash path continues the same
 session in the same terminal — it does not use the extension's tab spawner, so
 it carries none of the "opens in the wrong workspace" risk that keeps the
 extension auto-open gates off by default. Works on code-server / SSH / plain
 terminal too, where no extension exists.

### Fixed — The dev failure-monitor no longer silently dies

`pc dev monitor`'s systemd timer could be left pinned to a throwaway
`POWER_CLAUDE_HOME` under `/tmp` (a test sandbox leaked one via `dev.test.ts`).
When that temp dir was cleaned up, every 15-minute tick failed at
`status=209/STDOUT` *before the scan ran* — so the monitor recorded nothing for
days while still showing as "enabled".

- **Sandbox guard.** `fm_install_cron` now refuses to wire a real user-level
 systemd timer / crontab to a `/tmp` (or `pc-dev-*` / `pc-test-*`) home, and
 ensures the log directory exists before systemd opens it. Tests can no longer
 leak a user timer.

### Added — `pc dev monitor enable --persistent` (rolling window)

For chasing a connection/rotation bug over days without re-enabling: a rolling
window (default 7d, `--rolling-days N`) that `scan.sh` renews on every tick. The
monitor watches indefinitely while the timer stays healthy, yet still
self-disables one window after the last tick — it can never get orphaned-on
forever (the DEV-ONLY contract).

### Added — Search Open Session Tabs (find the session by what was SAID in it)

When you keep many Claude sessions open, finding the one that discussed a
particular thing means clicking through tabs one by one — the title rarely
matches what you actually remember, which is something said *inside* the
conversation. This searches the **content** of your sessions and takes you
straight to the right one.

- **Searches what was said, not just titles.** Power Claude streams each session's
 transcript and matches your query against the conversation bodies — user
 messages, Claude's replies, tool calls, and tool output — then ranks the hits
 and previews each matching turn with your query **highlighted**. (The existing
 session search only ever looked at titles, first prompts, and file paths.)
- **Three ways in.** A **🔎 Search Sessions** button in the status bar (always
 visible, bottom-left) opens it in one click; a keybindable QuickPick — **Search
 Open Session Tabs** (`Ctrl+Alt+Shift+S` / `Cmd+Alt+Shift+S`) — searches the tabs
 you have open right now; and a content-search box at the top of the dashboard
 **Sessions** list with a toggle to widen from open tabs to *every* indexed
 session.
- **One click reveals the tab.** Selecting a match foregrounds that session's
 Claude tab (no wake-up prompt injected); a secondary **Resume** opens a closed
 one. Note: VS Code does not let one extension scroll inside another's webview, so
 the highlighted content is shown in Power Claude's own panel, then the tab is
 revealed.
- **Also in the CLI.** `pc session search <query>` searches live sessions by
 default (`--all` to widen), with `--json` and a ranked table — the same shared
 engine the editor uses, so results agree.
- **Pro feature** (`powerClaude.openTabSearch.enabled`); the reveal-tab action
 itself stays free.

### Added — Claude Core: Warm Compacting (no more multi-minute compaction freeze)

Claude Code freezes a session for minutes when the context window fills and it has
to summarize the whole conversation inline. Warm Compacting removes that wait by
pre-summarizing the earlier part of the conversation **in the background**, before
the wall — stored **sidecar-only**, never in your live context, never touching the
transcript — so when the limit is near only the recent tail is needed and the proxy
substitutes the pre-built compact context instead of letting the freeze happen.

- **On by default with the live splice enabled** (`powerClaude.warmCompacting.applyRewrite`).
 When your session nears the wall the proxy replaces the early conversation with the
 pre-built warm summary on the outbound request, keeping the recent tail verbatim, so
 Claude Code's `input_tokens` never crosses the autocompact threshold. Flip
 `applyRewrite` off for a measure-only mode that builds + reports the projected token
 drop without altering a request. **No regression by construction** — if anything is
 unsafe (stale marker, unsafe boundary, oversized merge) it falls back to normal
 compaction, so the worst case is exactly today's behavior.
 actually shrank; marker validation catches edited/rewound sessions; a kill switch
 (`POWER_CLAUDE_WARM_COMPACT=0`) disables it out-of-band.
- **Visible, not silent.** A brand-stamped `⚡ Warm Compact` indicator shows in the
 statusline (CLI `pc statusline` + the VS Code dashboard); honest per mode
 (`calibrating` until the live splice is on). Inspect it with `pc warm-compact`.
- **On by default**, license-gated, and tunable: `powerClaude.warmCompacting.enabled`,
 `…triggerPercentOfCompactThreshold`, `…maxWarmCompactsPerSession`,
 `…maxWarmSummaryTokens`, `…maxInjectedCompactTokens`, `…autocompactPercentOfWindow`,
 `…applyRewrite`.

### Added — Claude Core: Tab Warming (open 20 sessions, never click through them to load)

Claude Code only loads a session's conversation when its tab is first revealed —
that's why reopening a window with 20 sessions makes you click through all 20 just
to "wake" each one. Tab Warming does it for you, automatically, the moment VS Code
finishes restoring.

- **Every open session tab is pre-loaded for you.** Shortly after the window
 settles, Power Claude reveals each open Claude tab once — using Claude Code's own
 open command, which reveals the *existing* tab (never a duplicate) — forcing the
 conversation to render, then **returns you to the tab you were on**. Click any
 tab afterward and it's instant.
- **As unobtrusive as the platform allows.** Loading a webview *requires* revealing
 it (VS Code offers no way to load a hidden tab), so the sweep is briefly visible —
 but it runs **once**, only after you've been **idle** a few seconds, **accelerates
 adaptively** when your machine keeps up, and **aborts and restores your tab the
 instant you interact**. It never strands you on the wrong tab.
- **Load, or fully resume.** By default tabs are loaded for instant viewing but
 left dormant. Flip `powerClaude.tabWarming.resumeOnLoad` to also inject your
 wake-up prompt as each loads — i.e. resume every session on restore.
- **On by default**, license-gated, and tunable: `powerClaude.tabWarming.enabled`,
 `powerClaude.tabWarming.resumeOnLoad`, `…minTabs`, `…maxTabs`, and `…idleQuietMs`.
 Built on the same session-open path as the dashboard's per-row Open/Resume and
 bulk "Resume selected" actions (single source of truth).
- Grouped with the rest of the **Claude Core** enhancements under one Settings
 heading (**Power Claude: 🧩 Claude Core**) and one docs page
 (product docs).

### Added — Claude Core: rate-limit lockout visibility (know WHY every session is paused, and WHEN it resumes)

When every Claude account in your pool is rate-limited at once, Power Claude
keeps each session's retry loop alive so it can auto-resume the instant a window
clears — but until now that looked identical to a hung session: Claude Code just
showed a "thinking" spinner with no reason and no ETA. This surfaces the truth.

- **A clear signal on four surfaces.** A red *"All Claude accounts rate-limited ·
 auto-resume ~32m (22:30)"* banner appears in the VS Code status bar, in the
 Claude Code statusline (when wired via `pc statusline --install`), as a
 one-time onset toast, and as a `Lockout:` row in `pc status` — all driven by a
 single shared reader so they can never disagree. Everything clears
 automatically the moment an account recovers.
- **Your sessions still resume themselves — even hours later.** This is purely
 about visibility; the existing auto-resume is unchanged. When the long
 (5-hour / weekly) window finally clears, Power Claude resumes the paused
 sessions on its own. You don't have to babysit or manually restart anything.
- **Two independent toggles.** `powerClaude.claudeCore.lockoutVisibility.enabled`
 (the always-on status-bar banner + statusline + `pc status` row) and
 `powerClaude.claudeCore.lockoutVisibility.toast` (the interrupting onset
 notification). Both ON by default.

### Added — Token Saver (Context Optimization): get more out of the tokens you already pay for

Power Claude can now trim the low-signal noise out of what Claude reads — the
bulky `tool_result` blocks in each request (command output, build logs, diffs,
JSON dumps) — on the wire, before they reach the model, so leaner context leaves
more room for real work and you hit context-limit walls less often.

- **Reversible and audited.** Lossless where possible (JSON is whitespace-minified)
 and never fabricates — it only drops or collapses low-signal noise. High-signal
 lines (errors, stack frames, diff changes, hunk headers) are always preserved,
 and the verbatim original is retained.
- **You choose how aggressive.** `Conservative` / `Standard` / `Aggressive`
 profiles plus per-kind toggles (command output, logs, diffs, JSON), under
 *Settings → Power Claude: Context Optimization (Token Saver)*.
- **Measured, not guessed.** Lifetime tokens-saved and per-kind tallies are
 tracked and surfaced via `pc status` and the proxy status endpoint.
- **See it on the dashboard.** The Power Mode card shows a live Token Saver
 ribbon: realized savings (today / last 7 days / lifetime) *plus* a projected
 monthly run-rate, each with a labeled ≈$ estimate. It reads durable telemetry
 (`context-optimize.json`), so your lifetime savings stay visible even while the
 proxy is stopped or restarting — previously the ribbon was hidden whenever the
 proxy was not actively running.
- **Projected, not just realized.** Alongside what you've already saved, both the
 dashboard ribbon and `pc savings` project your monthly run-rate at the current
 pace — clearly labeled an estimate, not a guarantee.
- **On by default** at the `standard` profile; dial it down or turn it off via
 `powerClaude.contextOptimize.enabled` / `.profile`.

### Added — Concurrent-window state safety: run ten windows without corrupting settings or rotation state

Power Claude is built for developers who keep many VS Code windows open against one Claude account pool. Every window read-modify-writes the same shared files — Claude Code's settings file and the live account-rotation state — so without coordination they race: two windows flip the active account at the same instant and one update vanishes, or a half-written settings file lands corrupt (classic last-write-wins).

- **Atomic cross-process lock.** Every write to the shared state goes through a `O_CREAT | O_EXCL` file lock, so exactly one window writes at a time and the others queue for a few milliseconds. No torn files, no lost rotation updates.
- **Stale-lock recovery.** The lock records the holder's PID and start time; if a window crashes mid-write, the next writer detects the dead holder and reclaims the lock automatically — no wedged state, no manual cleanup.
- **Zero added dependencies.** The lock is a tiny synchronous primitive (`related module`) consumed by the settings writer and the proxy rotation-state writer; nothing is added to the shipped bundle.
- **Companion to the double-launch guard.** That guard protects a single *session transcript* from two drivers; this protects the shared *state files* from concurrent writers. Together they make heavy multi-window use safe.

### Added — Session Checkpoints + Bash-Gap: see what `/rewind` can't undo

Claude Code's native checkpointing (`/rewind`) only tracks files edited through Claude's own editing tools — it is blind to files changed by bash commands, external edits, or other sessions. Power Claude now surfaces the full picture and names exactly what native checkpointing would silently fail to restore.

- **Three-layer view.** For any session, Power Claude reports L0 (Claude's native `/rewind` checkpoints, read from Claude Code's native checkpoint store), L1 (the durable session-ledger snapshot git refs), and the diff between them.
- **Bash-gap analysis.** Computes `files changed since session start` minus `files Claude edited via its tools` — the set native `/rewind` **cannot** restore. Power Claude's own session snapshot ref can, so nothing is silently unrecoverable.
- **CLI (the surface that ships today).** `pc session checkpoints <id>` and `pc session bash-gap <id>` (both `--format=table|json`) for headless workflows.
- **Shared, consumer-blind core.** The checkpoint reader and bash-gap set-math live in shared session core (one implementation), consumed by the CLI today and written once so future surfaces (proxy, Session Explorer) reuse it rather than re-implementing.

### Fixed — Account & Usage popup no longer flickers, vanishes, or hides behind the banner

The pool-aware "Account & Usage" popup — the Power Claude view that replaces Claude Code's single-account usage panel while rotation is active — was unreliable: it could flicker, close itself the instant it opened (leaving only a dimmed backdrop), show an empty shell with no pool data, or render *behind* the Power Claude banner pinned at the top of the chat.

- **Now a Power Claude-owned dialog.** Rather than rewriting Claude Code's own popup in place — which fought the editor's re-rendering and caused the flicker / self-close / empty-shell behaviour — Power Claude now suppresses the native popup and shows its own dialog, which it fully controls. Open, close, and the 30-second refresh are stable.
- **Always on top.** Power Claude dialogs now sit above every Power Claude surface (banners, the request anchor, tooltips), so the popup can no longer be buried behind the banner.
- **Reliable dismissal.** Click-outside and Esc both close the dialog, and the gesture that opens it can no longer immediately dismiss it.
- **One shared dialog.** The usage popup and the "session active in another window" confirm prompt now use a single reusable dialog component, so they look and behave consistently.

### Added — Auto-Resume now continues on self-promised stops and broader "remaining work" phrasing

Auto-Resume gained a detector for the most common avoidable stop: the assistant says it will keep going — *"I'll continue this automatically once the install finishes"*, *"let me wrap this up"* — and then ends its turn anyway. Instead of leaving the session parked until you type "continue", Auto-Resume now picks the work back up.

- **New "promised-continuation" rule.** Matches self-promised continuations and resumes them.
- **Broader "remaining work" detection.** The existing remaining-tasks rule now also recognises *"remaining sequence / plan / checklist"*, *"the rest of the …"*, and *"left to do"* — not just the literal *"remaining tasks/steps"*.
- **Both ON by default, both gated.** Each match is confirmed by a fast model check before resuming, so genuine stopping points, finished work, and anything waiting on *you* are left alone; the existing veto rules still hold back *"once you've verified"*-style waits and approval gates.
- **Fix — new rules now reach existing installs.** The rule catalog is merged into an already-set-up install instead of being written only once, so this detector (and future ones) arrive on machines provisioned by an earlier version. Your own per-rule on/off edits are preserved.

### Added — DEV-ONLY failure monitor (`pc dev monitor`)

A toggleable diagnostics tool for chasing rotation/connection problems. When enabled it scans the rotator logs and the Claude Code session transcripts on a 15-minute schedule, reading only the bytes written since the previous run, and records **every** failure it sees — rate-limit/server/client/auth events from the recoverable-failures log, WARN/ERROR or failed-outcome lines from the events log, FAILED/NO_SPAWN/ROTATION_DISABLED/ERROR auto-rewake messages, and the literal "Unable to connect to API" / "ConnectionRefused" / "API Error" strings that surface in the session transcript even when the proxy logs are quiet.

- `pc dev monitor enable [--hours N]` turns it ON (default 24h) and installs the schedule; `disable` turns it off and removes the schedule; `status` reports whether it is on, when it auto-expires, whether the schedule is installed, and the findings count; `show [--last N]` prints recent findings.
- It **auto-expires** so it can't be left running indefinitely, and while it is on a dedicated status-bar indicator (`🔬 Failure Monitor ON · exp …`) is shown so it is never silently active. This is a debugging aid, not normal operation — it is intentionally noisy and lives in a clearly-marked Dev / Debug command group.

### Fixed — Editor-tab session icons were missing on almost every tab, randomly coloured, and clobbered the native attention icon

The Power Claude state icon on Claude Code editor tabs (running / incomplete / complete / idle) was broken in several ways at once:

- **Missing on most tabs.** The tab icon is matched to a session by its title, and the title is read from the session transcript. The reader only scanned the first 32 KB of the file, but modern sessions front-load large records (system prompt, attachments, images, skill/agent listings) that push the title record to ~65–120 KB in — so the title was found for almost no session and the icon never appeared. The reader now scans a generous head plus a tail fallback and finds the title reliably; tab-icon coverage for open sessions is restored. (The same under-scanning reader was duplicated in the watchdog resume picker; both now share one fixed implementation.)
- **Still missing on restored and idle tabs — the deeper cause.** Reading the title correctly was not enough: an icon could only be attached while Claude Code fired its internal `rename_tab` event, which happens when a session is being (re)titled — not when a tab is merely opened, and not when tabs are restored on a window reload. So only the one session actively generating a title ever registered, and every restored or idle tab kept Claude Code's native icon indefinitely — the "only one tab has the state icon" symptom, and the steady state after any reload. Power Claude now also hooks Claude Code's panel-setup path, which runs on **every** tab open *and* restore, registering each session tab by its (reload-persistent) title; construction-time tabs that have not been titled yet are held and promoted the moment their title becomes known. Combined with the live session-state feed, every open session tab now shows its state icon immediately on restore — no rename required.
- **Colours had no rhyme or reason.** The icon rotated through three colour *variants* chosen by hashing the session title, so the same state rendered in different shades on different tabs. The variant system is removed — **colour now always encodes state** (green = running, amber = incomplete, blue = complete, slate = idle).
- **Overwrote Claude Code's own attention icon.** The icon unconditionally replaced the tab icon, hiding Claude Code's pending-permission and unseen-completion indicators. It now **yields**: it only decorates the default state and steps aside whenever Claude Code is signalling for attention, so those cues are never hidden.
- **New composite icon.** All four states now render a single composite glyph — a constant identity mark plus a state-coloured corner dot — and the previously-suppressed "idle" state is shown (drawn weaker) so a tab is never ambiguous between "idle" and "no icon".
- Because VS Code does not allow a custom tooltip on an editor tab, the focused session's state and a short explanation are surfaced in the **status-bar legend** instead.

### Fixed — Power Claude decorations silently vanished after every Claude Code update

The editor-tab icons and all in-chat decorations (message timestamps + state tint, session-list badges, the "Your Request" banner) are injected into Claude Code's *own* `extension.js` and webview bundles. Whenever Claude Code auto-updated, it re-extracted fresh, unpatched copies of those bundles and loaded them into the running extension host and webview. Power Claude re-applied the patches on disk, but a running extension host cannot be hot-patched — Claude Code only re-reads those bundles on a window reload — so the decorations disappeared and stayed gone, with no indication why, until the user happened to reload.

**Fix.** Power Claude now watches the installed Claude Code version. When it changes, and after the self-heal has re-applied the patches to the new bundle, it surfaces a one-time prompt — *"Claude Code updated — reload to restore Power Claude"* — with a Reload button. It fires at most once per version (the baseline is persisted the moment the prompt appears, so reopening windows never re-nags), seeds silently on first install, and honours the existing `powerClaude.autoReloadOnRedeploy` opt-out (it never reloads without consent).

### Fixed — "Your Request" banner tooltip was truncated to ~280 characters

The pinned "This session" banner clamps its visible body to two lines and relies on the hover tooltip to reveal the full original request. But the request text was being sliced to a 280-char cap *before* it reached the tooltip, so hovering showed the same truncated string as the banner — the rest was unrecoverable. The cap is now applied only to the on-screen body; the tooltip carries the complete, untruncated request text.

### Fixed — Account dashboard "flickered" through a wrong state on every refresh

On each refresh the account rows would briefly flash an incorrect state — often every account momentarily shown as healthy/available — before settling, and the metric tiles popped in and out. It could also look as though the rows were being re-sorted. Root cause: the dashboard's data file had **two independent writers** — the bundled in-process collector and a host-side render script — running on different cadences with different status vocabularies and metric namespaces. Whichever wrote last won, so the view oscillated between two snapshots, and a status token one writer emitted was grouped inconsistently by the other.

**Fix.** The in-process collector is now the **single authoritative writer** of the dashboard data file. The host render script still runs for its live API probe and profile self-healing, but its rendered output is diverted to a scratch file the dashboard never reads, so it can no longer overwrite the collector's output. The collector emits a stable metric set that is always present (tiles no longer appear and disappear) and carries the host script's System-Protection and event-stream sections forward, so the System Protection panel, recovery countdown, and Force-Heal control stay intact. Row order is unchanged across refreshes (alphabetical by account), so rows no longer appear to re-sort.

### Fixed — Power Mode banner and pool-runout wording

- The Power Mode banner no longer shows a misleading "~1× throughput across 1 of N accounts" in least-busy mode; it now reads "smart routing across N healthy accounts," and the mode label no longer renders doubled parentheses.
- The offline-grace license banner drops the stray "What is this?" label (the explanation remains on hover).
- Pool-runout wording now agrees in number — e.g. "1 of 12 accounts still has capacity" and "… will exhaust before their windows reset."

### Fixed — "Resume session" never warned when a session was already being worked on

The double-launch guard — the modal that is supposed to stop two processes from driving the same Claude Code session at once — almost never fired. It relied solely on a heartbeat sidecar that a VS Code window writes only when it *explicitly claims* a session, so a session you were driving from a terminal (`claude --resume`), the `pc` CLI, or a sibling window that never claimed it was invisible to the guard. Worse, the single-session resume path would *silently skip* an already-running session — no new window, no warning — which is exactly the "I never get notified" report.

**Fix.** Liveness detection now combines the heartbeat sidecar with a live `claude --resume <id>` **process scan**, so a session being worked on anywhere on the machine is detected regardless of how it was launched. Resuming a busy session now shows an explicit modal — **Take over / Open anyway / Open read-only** — instead of silently racing or silently skipping. Both "resume an existing session" surfaces (the Session Explorer Resume action and the dashboard per-row Resume button) share the one guard, and the Session Explorer live dot now lights for terminal/CLI sessions too — not only windows that claimed a session.

### Added — Session concurrency on the `pc` CLI (`pc session live`, guarded `pc session recover`)

Everything the editor knows about "is this session being worked on?" is now available on the command line, for headless and terminal-only workflows:

- **`pc session live`** lists every session being driven right now — fresh heartbeat sidecars unioned with live `claude --resume` processes — with `--format=json`. It is the terminal-side equivalent of the Session Explorer live dot.
- **`pc session recover`** now runs the same concurrency guard before resuming: it refuses a session that is already in use, names who holds it (a VS Code window, or a terminal/CLI process), and exits non-zero unless you pass **`--force`**. `--dry-run` is never blocked.

### Added — More VS Code actions reach the `pc` CLI (stop, heal, throttle-only, token-refresh)

Closing the gap so headless / terminal-only workflows can do what the editor can. Each mirrors an existing VS Code command:

- **`pc stop`** (also **`pc proxy stop`**) — stop the background rotation proxy `pc serve` starts. It clears the respawn-intent marker first so the watchdog can't resurrect a deliberately-stopped proxy mid-kill. Previously the CLI could start the proxy but nothing could stop it.
- **`pc heal`** — full operational reset, then `pc fix`: drops the rotation kill-switch (canonical + legacy mirror), the throttle-only flag, and every per-account cooldown/lockout backoff file. The CLI mirror of the editor's **Force Heal** command.
- **`pc throttle-only [on|off|status]`** — toggle the rotation throttle-only sentinel (rotate only when an account is throttled), mirroring the dashboard toggle.
- **`pc relogin <name> --refresh-only`** — token-refresh-only path (no full OAuth re-login), the flag the extension's "Refresh account" button already invoked but the CLI silently ignored.

### Added — Full VS Code → CLI parity: settings, hooks, routing, reporting

The remaining editor-only actions now have headless `pc` equivalents, each consuming the **same vscode-free core** the extension uses (extracted to `source` where it lived inline) — no duplicated logic:

- **`pc permission-mode [get | set <mode>]`** — read/write Claude Code's `permissions.defaultMode` (default · acceptEdits · auto · bypassPermissions · plan · dontAsk), atomically under the cross-window settings lock. Mirrors the editor's set-permission-mode / toggle-auto-mode.
- **`pc hooks <install|uninstall> <watchdog|lifecycle|timeline>`** — manage Power Claude's Claude Code hook entries from the terminal: the self-heal watchdog tick, the session-lifecycle hooks, and the Timeline edit-logger.
- **`pc routing <smart|fallback|status>`** — switch routing between the always-on rotation **proxy** (smart) and reactive **bash-hook** rotation (fallback); persisted through the same `proxy-mode.last` signal the watchdog honors.
- **`pc switch --soonest`** — switch to the account that recovers soonest, ranked from `state/rate-limits.json` (parity with the editor's "switch to soonest").
- **`pc savings [--sessions N --hours H --accounts C] [--json]`** — the dashboard's subscription-savings estimate on the command line.
- **`pc insight-export [--window today|24h|7d|30d] [--output PATH] [--json]`** — aggregate sessions in a window into a markdown insight snapshot (standup / weekly review / PR description).
- **`pc logs export [--out DIR] [--no-rate-limit] [--no-handler] [--json]`** (also `pc logs-export`) — a sanitized log bundle (API keys, OAuth tokens, session secrets, home-dir PII redacted) ready for a support ticket.
- **`pc license refresh`** (alias `pc license validate`) — re-validate the activated license against the auth server and refresh cached state, instead of waiting for the background re-check.

### Fixed — Usage dashboard showed "0 tokens" for every account except the active one

The LLM Usage tab's plan-tier distribution and per-account cards read token totals from the ephemeral session logs, which can only attribute usage to whichever account is *currently* active. Every other account — including all your PRO accounts — showed **0 tokens**, making the plan distribution and per-account drill-down look broken.

**Fix.** Per-account token totals now come from the proxy's authoritative usage store, which records real cumulative tokens (uncached input + output — the limit-relevant tokens) for **every** account the proxy has ever served, regardless of which one is active right now. PRO and idle accounts now show their true totals.

### Fixed — "Daily token burn" chart was empty or wildly inflated

The 30-day chart was sourced from data that is pruned after ~2 days and cache-inflated, with no reliable per-account attribution — so it showed either nothing or numbers many times too large.

**Fix.** The proxy now keeps a small, forward-only **daily token ledger**: each day's per-account usage is derived from the authoritative cumulative counters, so the chart is accurate and reconciles with the per-account totals. It is honest about history — the chart fills forward from when collection began and shows a clear note rather than fabricating days that predate it. (No hot-path cost: the ledger piggybacks on the proxy's existing debounced state write.)

### Changed — Usage dashboard leads with subscription savings, not pay-as-you-go API pricing

Power Claude users rotate **subscription** accounts, so comparing usage to per-MTok pay-as-you-go API rates was misleading — it implied a "savings vs API" that nobody was ever going to pay. All pay-as-you-go API comparisons (the "API equivalent" cards, the "$/M tokens" and "vs API" columns, the per-MTok rate table) are now **hidden by default** and can be re-enabled with the `powerClaude.usage.showApiComparison` setting.

In their place, the Overview hero shows an honest, subscription-native figure: **how much your mixed fleet saves versus buying the same weekly token capacity entirely in Max-200 seats** — e.g. "your N accounts deliver M× Max-200 capacity for $X/mo."

### Changed — Exact counts now use thousands separators

Exact token counts, dollar amounts, and request/event counts across the dashboard now render with thousands separators (`1,234,567`) instead of running together. Compact `K`/`M`/`B` units are kept only where space is tight — chart axes and small summary chips.

### Added — Balanced-mode account highlighting

In full-rotation (single) mode the dashboard highlights the one active account in green. In **balanced/parallel** mode the dispatcher fans out across the whole healthy pool, so a single green row was misleading. The Accounts tab now reflects the actual routing: a **"⚖ Balanced · N in rotation"** header chip, a partial-green **"◐ in rotation"** treatment on every account currently being routed, and a **"★ PRIMARY"** marker on the dispatcher's home account. The solid-green single-active row is reserved for full-rotation mode.

### Fixed — Power Mode banner showed contradictory account counts (e.g. "~11× throughput across 7 accounts")

The Overview "Power Mode is ACTIVE" banner could report a throughput multiplier and a pool size that disagreed — "~11× throughput across 7 accounts" — while the accounts table below showed yet a third number (9 healthy). None of the figures were wrong on their own; they simply came from different places.

**Root cause.** The multiplier was read from the live proxy status, but the "across N accounts" count was recomputed separately from the dashboard's own account-scan results — a different data pipeline refreshed on a different cadence. When the two snapshots were momentarily out of sync, the banner showed two counts of the same thing that didn't match.

**Fix.** Both numbers now derive from a single proxy-status snapshot, so they can never contradict each other. The banner reads "~N× throughput across N of M accounts" — N usable accounts in the rotation pool out of M total — which also makes plain why the figure is what it is. The multiplier remains a simple per-account count (each account counts once, regardless of plan tier). The Power Mode card on the same tab was corrected the same way.

### Changed — "Your Accounts" is now one stable, filterable list instead of state-grouped sections

The accounts table previously split accounts into collapsible **Throttled / Healthy / Needs-action / Idle** sections. When an account changed state it jumped from one section to another, so the list re-ordered itself underneath you — hard to follow at a glance.

It is now a **single list in a fixed alphabetical order** (by account email), so a row never moves when its status changes. A row of **status filter chips** sits above the table — Healthy, Throttled, Needs-action, Idle, each with a live count — and you can toggle any combination on or off to focus the list. Filtering hides and shows rows in place (no re-ordering), and your selection persists across the dashboard's automatic refreshes. The filter is a reusable control any future dashboard table can adopt.

### Fixed — "Your Request" banner sat mid-screen over the conversation and covered the first reply

The pinned recap of a session's original ask (the "THIS SESSION" band) could appear a quarter of the way down the conversation pane — floating over live content, and on a phone-sized viewport landing in the middle of the screen. Early in a session it also showed immediately, duplicating the still-visible first message and covering the assistant's first "thinking" block.

**Root cause.** The band positioned itself just below Claude Code's header by probing broad CSS-class fragments (`header_`, `toolbar_`, …) and taking the lowest match. Those fragments also matched *per-message* elements, so the computed offset drifted with message length and viewport size, parking the band wherever that element happened to be. And it had no notion of "is the original message still on screen?" — it rendered the moment the text was readable.

**Fix.** The band now anchors to the **top edge of the conversation's own scroll container** (a stable position regardless of message length, scroll, or viewport) instead of guessing the header height. It stays hidden while the session's original message is still visible — so it never covers the first reply or thinking block — and reveals only once that message has scrolled up out of view. When shown, it reserves its own height at the top of the scroll area so it never overlaps a message (zero content-hiding), and restores that space the moment it hides or is dismissed. Scroll/resize are tracked so reveal/hide feel instant. Verified in a browser harness across the scrolled-away, scrolled-back, steady-state (no flicker), and dismiss cases.

### Fixed — Chat input box could disappear during a usage-limit warning (recoverable only by reloading the window)

On some sessions the Claude Code message input box vanished and did not return until the VS Code window was reloaded. It happened specifically when Claude Code surfaced its native "You've used N% of your weekly limit" usage banner.

**Root cause.** Power Claude replaces that single-account banner with a pool-aware message (one account's percentage is misleading when Power Claude rotates across many accounts). The replacement located the banner by its text — but matching on text also matched the *outer* container that wraps the banner, the conversation, and the input box together, and the rewrite then collapsed that container's contents into a single plain-text line, deleting the input box along with it. Because the change mutated the live page, the input stayed gone until the editor reloaded and rebuilt the view.

**Fix.** The banner replacement is now surgical. It narrows from any matched container down to the smallest element that actually holds the banner text, hard-refuses to touch any element that contains the message input (or other interactive content), and only ever rewrites the banner's own text — leaving sibling controls such as "View usage" intact. If it cannot isolate the banner safely it leaves the page untouched rather than risk the input box. Verified across the all-healthy, partially-limited, and fully-exhausted pool states.

### Changed — Pool status banner now explains itself in plain language

The message that replaces Claude Code's single-account usage warning previously read "Power Claude: 3 of 12 accounts healthy · best weekly 0% — still routing", which didn't convey what it meant or why it appeared. It now leads with its purpose — for example, "⚡ Power Claude is spreading work across your 12 accounts, so Claude Code's single-account limit warning doesn't apply. 3 accounts still have room (lowest weekly use: 0%)." — with matching plain-language wording for the all-healthy and fully-exhausted states.

### Fixed — Chat sessions appeared to be "processing/thinking" forever after a turn finished

When a chat turn completed and the assistant went idle, the session's tab icon and status dot kept showing the "running" (processing) state indefinitely, so it looked like Power Claude was still working on a conversation that was actually done.

**Root cause.** The icon state conflated two unrelated signals. A session carries a "live" flag — a heartbeat that stays on the whole time the session is *open in a window* (used to detect the same session being driven from two windows at once). The icon logic treated "live" as if it meant "processing", so any open-but-idle session rendered as running and never returned to idle. The genuine processing signal (a recent transcript append, which auto-expires a few seconds after the turn ends) was being masked by the ever-on "live" flag.

**Fix.** The running/processing icon is now driven ONLY by the genuine processing signal, which clears on its own shortly after a turn ends. The "live" ownership flag is still tracked for double-launch detection but no longer forces a processing appearance. A finished turn now shows idle/complete as it should.

### Added — Malformed-request (HTTP 400 / 4xx) failures are now visible in the event feed

Client-side request errors (HTTP 400 and other 4xx — e.g. an empty messages array, a too-large prompt, an invalid parameter) were never recorded anywhere: the failure feed only captured rotation-recoverable statuses (rate-limit, auth, server errors), so a malformed request that the editor or a tool produced returned an error to you with no trace to diagnose from. These now land in the recoverable-failures event feed as `kind: "client-error"`, including a truncated copy of the upstream error body so the exact reason is visible (for example, "messages: at least one message is required"). They are recorded for visibility only — a 4xx is not rotation-recoverable and explicitly never triggers an account rotation or an auto-resume, so the new logging adds zero behavioral risk.

### Fixed — Extension drifted out of sync across editor environments (VS Code, code-server, Cursor, containers)

On a machine running more than one editor environment — desktop VS Code, a VS Code Remote server, a local code-server, and code-server instances running inside containers (each with its own extensions directory, some in separate mount namespaces) — Power Claude could be current in one environment and stale or missing in another. The editor you were actually using might run an old build of the rotation engine while a different environment had the fix, so rotation/auto-resume behaved inconsistently and "it's installed" was only true in some windows.

**Root cause.** The hot-deploy step enumerated a hardcoded list of extension directories and copied files into them. That list used a literal `/config/extensions` path that does not resolve to a containerized editor's real directory (containers run in a separate mount namespace; their directory is only reachable from the host via `/proc/<pid>/root/...`). Containers were therefore never reached, and copies could diverge from the installed manifest.

**Fix — one drift-proof sync path.** A single editor-sync engine now DISCOVERS every editor environment on the machine — by scanning running editor processes (including namespaced containers, resolved through `/proc`) and globbing well-known install locations — de-duplicates them by real directory identity, and reconciles each one to the freshly built bundle. Staleness is detected by content hash (every copy reports the same version, so version is not a reliable signal), so re-runs only touch environments that actually drifted. The sync runs as the final step of `pc install` and again on every session start, so no environment can silently fall behind. Containers are updated by a safe atomic directory swap plus a corruption-resistant manifest merge; the editor's own install command is used where it can be invoked directly. When a refreshed environment needs a window reload to pick up a new UI bundle, that is surfaced rather than forced.

### Changed — Extension ↔ CLI ↔ background-service lifecycle is now consistent (no orphaned services, no silent drift)

The extension, the `pc` CLI, and the background services (rotation proxy + watchdog) are three separate install surfaces that could previously drift out of sync. Tightened all three transitions:

- **`pc uninstall` now tears down the background services.** Previously it removed the `pc` shim + PATH entry but left the systemd units running — after a `--purge` they pointed at deleted scripts and restart-looped forever. Uninstall now stops, disables, and removes the proxy + watchdog units first (best-effort; a no-op on hosts without systemd).
- **The runtime stands down when the extension is uninstalled.** Editors fire no uninstall event for extensions, so the services would otherwise run forever after the extension was removed. The watchdog now detects a removed extension (its install marker pointing at a missing directory for ~30 minutes straight, with no upgraded copy present) and stops the proxy + disables itself. Reinstalling the extension re-enables everything automatically — nothing to do by hand.
- **The extension offers to repair a missing runtime.** If `~/.power-claude` or the rotation engine is gone while the extension is still installed, the extension now surfaces a one-click "Reinstall runtime" action (from its own bundled CLI) instead of silently failing to rotate. Offer-only and dismissible — it never re-creates files behind your back.

### Fixed — Rotation could wedge into a permanent "All N accounts exhausted" state that burned usage

Under sustained load the proxy could enter a state where it returned `All N accounts exhausted. Retry in Ns.` on every request — even though accounts had real capacity left. Once wedged it stayed wedged for the proxy's whole lifetime (only a restart cleared it), and because each rejected request triggered an automatic session-resume, the resume loop quietly consumed real usage.

**Root cause.** Account selection made its "everything is exhausted" decision from in-memory quota readings that are only refreshed by a live upstream call — but the exhaustion path returned *before* making any upstream call. That made it self-latching: no upstream call → the stale "exhausted" reading never refreshed → still looks exhausted. A transient spike in measured utilization could therefore lock the whole pool until the process restarted.

**Fix (defence in depth):**

- **Last-resort selection.** When every account scores as unusable, the proxy now forwards the least-bad account upstream anyway instead of fabricating a rejection. The upstream response is the source of truth: success immediately marks the account healthy and clears the wedge; a genuine rate-limit sets a real cooldown from the server's own retry-after. A synthetic "all exhausted" is now only possible when every account is truly credential-dead or under a real, server-confirmed cooldown.
- **Stale readings are probed, not excluded.** A quota reading older than 15 minutes is treated as "unknown, worth a probe" rather than "exhausted", so an account can never be locked out on evidence that nothing is refreshing.
- **Resume-loop circuit breaker.** Auto-resume now stops after 3 consecutive "all exhausted" resumes within 10 minutes and surfaces a single notice instead of looping — so a wedge can never silently burn usage again.
- **Self-healing watchdog.** The background watchdog now detects the wedge signature (sustained synthetic rejections while the saved state shows healthy capacity) and restarts the proxy, with anti-flap guards (sustained across ≥2 ticks, ≤3 restarts/hour, ≥10 min apart) that escalate instead of restart-looping.
- **Deterministic classification.** Rate-limit handling now trusts the proxy's structured HTTP-status/header signal over free-text error matching, so a wording change upstream can't misclassify a limit.

### Fixed — `pc rotate` (and every rotation/score/classify call) took ~21 seconds to start

The rotation engine binary in the runtime tree could become stale on upgrade — only first-time setup ever refreshed it, so reinstalls and hot-reloads left an old, oversized build in place that took ~21 seconds of pure startup cost on every invocation. `pc install` now redeploys the rotation engine binary on every run, so rotation commands start in well under a second.

### Fixed — Per-message session-state dot stopped rendering on Claude Code 2.1.153/154 installs (v3↔v6 sentinel drift)

The colored dot that decorates each chat row to show the live state of the session (processing / completed / incomplete / active) silently disappeared on any Claude Code install where the v3 message-time IIFE had been bumped to v6 (every install dated after 2026-05-28). The IIFE itself was emitting correctly — the body-level `data-pc-session-state` attribute was being set on every tick — but the brand-stamp badge IIFE that anchors the colored dot to each `.pc-msg-meta` span was never reaching the bundle.

**Root cause.** Three consumers of the message-time sentinel were left at the v3 string when `patch.sh` was bumped to v6:

**Fix.** Bumped all three to v6 in lockstep with the patcher. Added v3/v4/v5 to `revert.sh`'s legacy strip list so an upgrade-window revert still cleans up regardless of which generation last patched. The brand-stamp gate now opens on next orchestrator run, `reconcileForeignStamp()` injects the badge into every host bundle, and the per-row state dot returns.

### Fixed — `Your Request Banner` had wasted vertical space and a too-faint hairline border

The `THIS SESSION` label was rendered on its own line above the request text, doubling the banner's height for zero information benefit. The visual separator between the banner and the rest of the chat chrome was a single 1px purple hairline at 35% opacity — which read as "no border" against Claude Code's dark background.

**Fix** (`related module`, CSS section):

- Label is now inline with the text via a flex body with `align-items:baseline` — drops banner height ~40% on short asks.
- **3px solid purple top + bottom borders** (`rgba(124,58,237,0.85)`) replace the 1px hairline, plus a **4px solid bright-purple left accent** (`rgba(167,139,250,1)`) as a section-break cue.
- Label color brightened to `#c4b5fd` and weight bumped to `700` so the inline `THIS SESSION` prefix reads cleanly.
- Padding tightened to `6px 14px 6px 10px`.

No new feature surface — same single fixed-position banner, same DOM-only data source, same dismiss button. Future work toward inline-per-prompt scope and a session-recap accordion (sketched in the related `your-request-banner.md` doc) is unchanged and not part of this fix.

### Changed — Dashboard tooltip pass: every badge, chip, and stat tile now self-explains on hover

The dashboard had a class of small status indicators ("API", "EST", colour dots, the routing strip's request counter, the per-account fairness KPIs, the cooling/healthy metric tiles) where the meaning was implicit — readable to anyone who built the feature, opaque to a new user staring at the panel. We swept every one and attached a verbose `data-pc-tip` tooltip that explains:

- **what** the indicator represents,
- **what data** drives it,
- **what action** (if any) you should take when it changes colour or value.

The biggest legibility win was the **calibration-source pill** on the "Next account available in" card. It used to read **`API`** or **`EST`** — labels that, in isolation, read like "this is an API account vs an estimate account." That's not what the badge means: it tells you whether the recovery countdown was *calibrated from a real Anthropic rate-limit reset header* (we know exactly) or *projected from the published 5h-window heuristic* (we're estimating). The pill is now labelled **`✓ EXACT`** / **`≈ EST`** with rich markdown tooltips, and the same calibration-source helper is reused across the soonest-available card, the upcoming-recovery rows, and the rank chip.

Other surfaces touched (all in `related module`):

- **Routing strip** — `Routing →`, `via <account>`, `N req`, `Switch to Smart`, `Settings →` all upgraded from sparse `title=` to wide `data-pc-tip` with explanations of what each action does and what the counter means.
- **Soonest-available card** — every account-color dot and the queue-rank chips (`#2`, `#3`) explain themselves; the active-credential `▶` marker now distinguishes between *primary dispatcher account* (Power Mode) and *single bound account* (Single mode).
- **Status legend pills** — each pill in the Status Reference accordion carries the same tooltip as the matching dashboard pill, so hovering anywhere in the dashboard yields the same explanation.
- **Pool-count metric tiles** (`Healthy`, `Cooling`, `Blocked`, `Expired`, plus the `Rate Limits` / `Rotations` counters) — each tile explains what its number means and (for state tiles) whether it's a permanent or recoverable state.
- **Fairness KPI tiles** (Pool Utilization, Active Capacity, Load Concentration, Idle Accounts, Recovery ETA) — each carries its own definition, threshold guidance, and Gini-basis note for the load-concentration metric.

The tooltip engine (`related module`) already supported `**bold**`, `*italic*`, `` `code` `` and `\n` linebreaks via `data-pc-tip`; this pass just connects more elements to it. No changes to the rendering engine or settings surface.

**Why this matters.** The dashboard's information density was an accessibility tax for new users — the colours and acronyms encoded a model that lived in the developer's head, not on the screen. Tooltips bring the model to the screen without spending pixels on it. They also seed the equivalent public docs on neural-llm.com (badge glossary) so the same words live in both places.

**Files**: `related module` (renderSoonestAvailable, renderRoutingStrip, renderMetrics, renderStatusLegend, fairnessTile).

### Fixed — Preserve-Focus Fix: terminal `show()` was still yanking the cursor on Bash tool calls

The v1 patch covered six autonomous-focus-steal sites (panel reveal, sidebar show, two `showTextDocument` paths). Users running with the patch enabled still saw cursor focus leave the editor mid-typing — the window stayed put, but the keyboard cursor jumped. Two unpatched `Terminal.show()` call sites were the residual cause.

- **Patch 7 — transient terminal `show()` on every Bash tool call**. Claude Code creates a transient terminal for each Bash invocation and shows it without `preserveFocus`. On every bash command in an agent turn, this stole focus from whatever editor you were typing in. Now patched to `Terminal.show(true)` — terminal still appears, editor cursor stays put.
- **Patch 8 — `getTerminalContents` `show()`**. When the agent reads terminal output, the extension programmatically shows the terminal before running select-all + copy-selection. Same fix — `Terminal.show(true)` preserves editor focus.
- **Expected sentinel count bumped 7 → 9** (`/*preserve-focus-v1*/`). Idempotency check updated; partial-patch detection (e.g. mid-upgrade) still falls back to the `.preserve-focus.orig` backup and re-applies cleanly.
- **No setting change.** Existing `powerClaude.preserveFocusFix.enabled` users get the additional patches on the next extension activation (or via the manual `Power Claude: Re-apply Preserve-Focus Patch` command).
- **Files**: `related module` (added 2 patches, bumped `EXPECTED_SENTINELS`, expanded size-delta budget), `related module` (docstring count).

### Added — Your Request Banner: original ask pinned to every session via DOM injection

Power Claude reads the first user message directly from the session JSONL transcript and injects a slim banner into Claude Code's chat DOM — no LLM instructions, no context tokens consumed, fully deterministic. The Power Claude bolt badge appears as a tooltip-only stamp (`title="Power Claude feature"`); nothing is written as AI output.

Designed for users running many concurrent Claude Code sessions: ten windows open, one glance to know what each one is doing.

- **Zero context tokens.** The banner is a DOM element injected by `related module` IIFE. It reads session data from the Power Claude proxy (`GET /v1/sessions/:id/request`) — no prompt instructions to the model, no transcript entries.
- **Self-heals across Claude Code updates** — the IIFE is re-applied by `requestAnchorPatch.ts` on every extension `activate()`.
- **Default ON.** Disable via `powerClaude.yourRequestBanner.enabled = false`, the Command Palette entry **Power Claude: Toggle Your Request Banner**, or `~/.power-claude/state/your-request-banner.disabled`.

**Files**:

- `package.json` (`powerClaude.yourRequestBanner.enabled` setting + `powerClaude.toggleYourRequestBanner`)
- `data/brand-stamp/feature-matrix.json` (row `pc-your-request-banner`, surface `vscode-webview-bundle`)
- product docs (feature spec)

### Added — Dashboard expansion: rotation lane graph, account drill-down, per-row context menus

The VS Code sidebar dashboard gained a class of features inspired by GitLens and Git Graph — turning the panel from a status report into a hub you can act from.

- **Rotation handoff lane graph (Overview)**: a 60-minute timeline above the accounts table showing every rotation as a curved handoff between account lanes, with shape-encoded dots for state (filled = healthy, ring = throttled, × = error). Hand-rolled SVG; no chart libraries; theme-token coloured.
- **Status-bucket grouping (Overview)**: the flat accounts table now groups into "Needs action", "Throttled", "Healthy", and "Idle" sections you can collapse. Empty buckets are hidden, and your open/closed state persists per bucket across reloads.
- **Tree decorators (Overview)**: each account row carries inline status icons — 🔔 for recent events in the last hour (click to deep-link into Events filtered to that account), `!` for an error-grade event in the last 24h, 🔒 for currently throttled.
- **Account drill-down drawer**: click an account row (or its name) to slide a 320 px detail drawer in from the right showing a 24-hour activity sparkline, the last 10 rotations involving that account, and quick-action buttons (open log, activate).
- **Universal event Account column with autoFilter chips (Events)**: every handler event now exposes its target account as a discrete column with a clickable filter chip strip — combining it with the existing phase/component/level chips. Clicking 🔔 on Overview deep-links the events search to the matching account.
- **Hover action cards**: hovering an account row for 250 ms surfaces a compact card with the status summary and primary actions (open log, activate) — fewer clicks for the workflow you use most.
- **State-as-shape glyphs on status pills**: every account status pill now carries a leading glyph (●/◌/×/◇) in addition to colour, so the column is readable at a glance even on monochrome displays or for users with reduced colour vision.
- **Ctrl/Cmd-click compare (Events)**: select an event row by clicking it, then Ctrl/Cmd-click a second event to open a side-by-side JSON diff modal. Useful for diffing two ROTATED events to see how the rotator's reasoning changed.
- **Right-click context menus**: account rows expose Activate / Re-login / Refresh / Open log / Open claude.ai / Remove; event rows expose Copy JSON / Filter to account / Open log file. The native context menu is suppressed in favour of a dashboard-styled menu.

All rendering is hand-rolled SVG + CSS using VS Code theme tokens — no external chart or UI libraries. The expansion stays inside the existing 7-tab IA; nothing was renamed or moved.

**Files**:

### Added — Premium Trial callouts in the extension, CLI, and README

Free-trial users now see a consistent nudge toward the website's longer **14-day Premium Trial** (card-on-file, $0 today) that locks founder pricing for 2 years. The same URL and copy drive every surface from one shared source, so they never drift:

- **Extension dashboard**: free-trial users get a "Lock founder pricing" button in the dashboard that opens the Premium Trial signup. It is shown only on the no-card free trial — paid and Premium-Trial users never see it.
- **`pc` CLI**: `pc license info` / `pc license status` print a suppressible Premium-Trial banner when you are on the free trial. Silence it with `POWER_CLAUDE_NO_TRIAL_BANNER=1`.
- **Marketplace listing**: the README and `package.json` description now mention the free tier's no time limit alongside the Premium Trial's founder-pricing lock.

The callouts are gated on trial state — they appear for free-trial users and stay hidden for Premium-Trial and paid users.

**Files**:

- `README.md`, `package.json` (marketplace callouts)

### Fixed — "Connection refused" no longer needs a manual restart to recover

The rotation proxy used to run as a child of the VS Code / code-server extension host. When the editor recycled a stale extension host, it killed that host's entire process group — and the proxy went down with it, because a detached child still lives inside the host's control group. The port unbound, every request returned `API Error: Connection refused`, and nothing brought the proxy back until you manually restarted the editor.

The proxy now runs as a dedicated **systemd user service** (`power-claude-proxy.service`) in its own control group, fully decoupled from any editor process:

- **Survives editor restarts**: killing or recycling the extension host no longer touches the proxy — it lives in its own slice, not the host's.
- **Self-heals on crash**: `Restart=always` (with a 5-crashes-in-60s backoff budget) brings the proxy straight back. The 30-second watchdog is now a second layer that delegates to the service instead of spawning its own copy.
- **Respects the emergency-off switch natively**: when the kill-switch sentinel exists, systemd skips the start (recorded as a skipped condition, not a failure, so the restart loop stays quiet) and the session hook stops + disables the service.
- **Adopts an existing proxy** rather than fighting it: the extension probes the port and delegates to the running service when one is present, so there is never a duplicate on the port.
- **Self-registers on install**: `pc install` now wires the proxy / watchdog / pending-recovery hooks into `SessionStart` automatically. Previously the hooks were deployed to the runtime tree but never registered, so a fresh install never actually self-healed until the entries were hand-added to settings. Registration is idempotent — re-running refreshes the entries and migrates any earlier hand-added ones, so it never duplicates.

On hosts without systemd (minimal containers), the extension and watchdog fall back to the previous direct-spawn behavior automatically.

**Files**:

### Changed — Auto-open of session tabs is now dev-only (default off)

Power Claude no longer automatically opens Claude Code session tabs in production. Auto-open shipped buggy — it opened tabs in the wrong workspace context, and the rate-limit recovery loop ("accounts recover → `pending-recovery.json` → tab pops → user closes → handler rewrites → tab pops again") was hard to escape without disabling the extension.

A single master gate now controls every auto-open code path:

- **`powerClaude.devMode.autoOpenSessions`** (new, default `false`). When OFF (the new production default), Power Claude will NEVER auto-open a tab — not on startup, not after rate-limit recovery, and not when the watchdog detects a stalled session. The watchdog and rate-limit handler still run and still surface UI signals (badges, status-bar messages, `pending-recovery.json`); only the tab pop is suppressed.
- **Manual resume is unchanged**: dashboard "Resume Claude Sessions" buttons, Session Explorer right-click → Resume, and the `Power Claude: Resume Saved Sessions` command all still work as before.
- Three pre-existing settings (`autoResumeOnRateLimit`, `autoResumeSessions`, `watchdog.compactThrashAutoRecover`) had their defaults flipped from `true` to `false` to match this posture. They are now subordinate to the master gate — even when individually enabled, they no-op unless the master gate is ON.

Turn the master gate ON only when developing the extension and intentionally exercising the auto-open code paths. The detection logic stays exercised under normal use; production users get a quiet, manual-only resume flow until the underlying context-detection is reworked.

**Files**:

- `package.json` (`powerClaude.devMode.autoOpenSessions` setting + flipped defaults)

### Added — Session Awareness: see what every session is doing at a glance

Four small chat- and Session-Explorer patches that share one thesis — you can finally read your session state without opening anything.

- **Per-message timestamps.** Each chat bubble is stamped with your local HH:MM as it renders. Pure client-side via a MutationObserver, so the value never enters the JSONL transcript and is invisible to the model (zero token cost). Self-heals across Claude Code auto-updates.
- **Lifecycle status badge.** Every Session Explorer row is prefixed with a glyph for its classified state — 🟢 active, ✅ completed, 🟡 stale, ⚠️ abandoned, 📦 archived — so a long session list reads at a glance. Badge map and classifier live in `related module`; classification rules in `related module`.
- **Live-running overlay.** A 🟢 dot is layered onto the status badge when a session's heartbeat sidecar in `~/.power-claude/state/session-live/` is less than 10 seconds old, so you can tell which session is being driven right now versus idle between turns.
- **Double-launch guard.** Clicking Resume on a session another VS Code window is already driving pops a modal — Take over, or Open read-only — instead of silently racing the JSONL writer and corrupting session history.

Surfaced as a feature in `pc doctor` (CLI) and gated by the `powerClaude.sessionAwareness.statusBadge.enabled` setting (VS Code). Marketing tile + changelog on neural-llm.com updated in lockstep.

**Files**:

### Added — Session Recovery (Pro): rescue lost work when sessions fail

A first-class recovery system for the failure modes that previously meant losing your work entirely.

**Detection (9 failure scopes)** — the SessionIndexer now classifies each session against:

- `compact-thrash` (autocompact filled the window within a few turns, repeatedly)
- `tool-loop` (last N tool calls share an identical signature)
- `context-overflow` (API rejected the request as too long)
- `crashed` (truncated JSONL tail + no `session_ended` marker)
- `rate-limit-stuck` (auto-rewake stuck in retry state)
- `tool-truncated`, `heartbeat-stale`, `ended-with-pending`, `manual-stop` (existing/refined)

Scopes appear as red pills in the Sessions tab status column (severity-graded color, evidence visible on hover) and as `scope:*` auto-tags.

**Recovery (6 strategies)** — each scope maps to a default strategy:

- `context-trim-resume` (the fix for thrash/overflow): exports a trimmed summary, opens a fresh Claude session pre-seeded with it
- `fork-from-checkpoint`: truncates the JSONL at the last clean assistant `end_turn` under 140K prompt tokens, preserves the original as `.bak`, then resumes
- `tool-rerun`, `pending-task-injection`, `naive-resume`, `manual-export`

A new **Recover ▾** button appears in the actions column when failure scopes are detected. Click opens a strategy chooser with per-strategy cost-vs-rescue dollar estimates.

**Snapshot safety net** — every recovery creates `refs/power-claude/sessions/<id>/pre-recovery-<n>` (and `post-recovery-<n>` on success) so a bad recovery is one click to undo. Reuses the same drift-free git refs the Session Trail feature depends on.

**Recovery history** — a per-session record of every attempt. The engine consults this to avoid retry loops and to auto-escalate from naive-resume to context-trim-resume after 2 failed attempts.

**CLI surface (`pc session <subcommand>`)** — 7 new subcommands, all 60 commands now in `data/cli-manifest.json`:

- `pc session list [--failed] [--scope=<scope>] [--tag=<tag>] [--format=json]`
- `pc session recover <id> [--strategy=<id>] [--no-snapshot] [--dry-run]`
- `pc session export <id>` — trimmed-context markdown
- `pc session bundle <id>` — tarball with JSONL + recovery.json + git ref bundle for cross-machine resume
- `pc session restore <bundle>` — unpack + register on another machine
- `pc session rollback <id> [--attempt=N]` — `git reset --hard` to pre-recovery snapshot
- `pc session history <id>`

**Telemetry** — token-at-risk per session computed against per-model rate table; surfaces as "$X rescuable" inline on the Recover button.

**Files**:

- product docs (NEW)

### Added — Preserve-Focus Fix: stop Claude Code from yanking your cursor

- **Two new settings — `powerClaude.preserveFocusFix.enabled` (default OFF) and `powerClaude.preserveFocusFix.autoRunOnUpgrade` (default ON)** — patch the installed Claude Code VS Code extension to pass `preserveFocus:true` on every autonomous reveal/show/showTextDocument call. Without the patch, the Claude Code panel yanks editor focus whenever output arrives, a session reopens, or a file gets shown. The fix is the upstream change Anthropic hasn't shipped yet — tracked at [anthropics/claude-code#32726](https://github.com/anthropics/claude-code/issues/32726) (OPEN, no shipping fix as of 2026-05-20).
- **Six surgical patches** at the autonomous-focus-steal call sites: at-mention reveal, session-already-open reveal, makeVisible reveal/show callbacks (×3), and two `showTextDocument` calls. Idempotent via the sentinel `/*preserve-focus-v1*/` (expected 7 sentinels per file — one site appears twice). One-shot `.preserve-focus.orig` backup beside each patched `extension.js`.
- **Survives version drift** — anchors key on stable string literals (property names, the VS Code command literal `"revealInExplorer"`, the user-facing string `"Session is already open"`) rather than minified identifiers. Same drift-resistance strategy as the chip patcher.
- **Self-healing upgrade detection** — on each activation Power Claude compares the on-disk `extension.js` mtime against the last-applied record in globalState. On mismatch (an extension auto-update overwrote the patched file), the patcher re-runs automatically. Per-extension records keyed by absolute path, so users with multiple Claude Code installs (remote / Insiders / native) are covered independently.
- **Manual command** — `Power Claude: Re-apply Preserve-Focus Patch to Claude Code Extension` (`powerClaude.preserveFocusFix.apply`) — force-runs the patcher regardless of upgrade state. Use after editing the bundled `related module` or to recover from a failed apply.
- **Reload prompt** — after a fresh apply Power Claude shows a one-time `Reload Window` toast so the patched extension host code takes effect.
- **Opt-in by default** — the patch modifies a sibling extension. Safe and well-tested, but Power Claude doesn't touch another vendor's bytes without explicit consent. Flip `powerClaude.preserveFocusFix.enabled` to `true` in settings, then reload.
- **Files**: `related module` (bundled patcher), `related module` (lifecycle + globalState + settings listener + command), `package.json` configuration section 1 and command entry, `related module` wiring under the auto-nudge block.

### Added — Host Tuning (`pc tune`): stop Claude Code sessions dying en masse (exit 143)

- **New `pc tune` command fixes the bug where many Claude Code sessions die at once** with `Claude Code process exited with code 143`. Claude Code runs as a child process of the VS Code / code-server remote extension host. When the browser disconnects past a reconnection grace period, the extension host is disposed and **every** child `claude` process is SIGTERM-killed together — which is why dozens of sessions appear to die simultaneously. It is not a memory problem.
- **Two grace timers govern teardown.** The long grace is the `VSCODE_RECONNECTION_GRACE_TIME` env var (default 3h). The short grace is hard-capped at 5 minutes inside the bundled server JS (`Math.min(<5min>, n)`) — an env var cannot raise it, and on a phone over cellular 5 minutes of unbroken websocket is effectively impossible. The short-grace path accounted for ~70% of observed kills.
- **`pc tune` applies a durable, self-healing fix:** (1) writes a systemd drop-in for the code-server user service raising the long grace to 24h; (2) writes a marked `VSCODE_RECONNECTION_GRACE_TIME` block into `~/.vscode-server/server-env-setup` for desktop VS Code Remote; (3) patches the bundled server JS to remove the 5-minute short-grace cap. The JS files are vendored Microsoft code overwritten on every code-server / VS Code update — so the extension re-applies the patch automatically on each activation when it detects drift (`ensureTuningCurrent()`), and `.pcbak` backups make every change reversible.
- **Modes**: `pc tune` (apply, idempotent), `pc tune --status` (report applied state + live hosts + drift), `pc tune --revert` (restore `.pcbak` backups, remove env config). `--grace-hours N` overrides the 24h default (clamped 1–168); `--quiet` prints a one-line summary.
- **`pc doctor`** gains a 15th check — "Host tuning (exit-143)" — surfacing whether tuning is applied and whether a code-server / VS Code update has reintroduced the cap.
- **Wired into first-run setup** — `first-run-setup.sh` runs `pc tune --quiet` after hook registration (skippable with `--no-tune`); the extension's `activate()` runs `ensureTuningCurrent()` best-effort so the fix lands even for users who never run the CLI.
- **Files**: `related module` (CPU/RAM detection), `related module` (the tuning engine — host detection, systemd/env config, vendored-JS patch, drift self-heal, marker at `~/.power-claude/state/tuning-applied.json`), `related module`. Unit tests: `related module`, `related module`, `related module`. Takes effect after `systemctl --user restart code-server`.

### Added — Runout Forecaster

- **New "Runout Forecast" panel on the Overview tab** that projects, at your current burn rate, whether your pool will exhaust capacity before the 5-hour or 7-day windows reset. Three states drive a single color-coded banner: **green** when you're safe through the next reset, **amber** when some accounts will exhaust before reset, **red** when the pool is about to hit a wall. Each account row also gets a tiny ETA chip (`✓ safe` / `ETA 1h 47m` / `ETA 14m`) so you can spot the bottleneck without opening drawers.
- **Authoritative reset times** — pulled from Anthropic's `anthropic-ratelimit-unified-5h-reset` and `-7d-reset` headers (already persisted in `~/.power-claude/state/rate-limits.json`). The "will I make it before reset?" half of the math is exact; only burn rate is estimated.
- **Rolling sample buffer** — a tiny JSONL file at `~/.power-claude/state/usage-history.jsonl` stores per-account utilization samples (throttled to ≥30s gap per account, capped at 2 MB with oldest-half rotation). The estimator does a linear-regression fit over the last 30 min of samples and falls back to window-average growth when fewer than 3 samples are available.
- **Works in both Balanced and single-account modes.** Pool ETA is computed per-window (5h, 7d) and the tighter of the two drives the banner. A single hot account in a 12-account pool reads as `warn`, not `alert` — Balanced routes away from it. Pool only escalates to `alert` when the math itself says we'll hit the wall (ETA < 50% of earliest reset) or when a majority of accounts are individually at risk.
- **Cold-start affordance** — when there isn't yet enough data to project (first ~2 min after activation, or no account has sent traffic) the banner is suppressed; the per-account chips show `—`.
- **Files**: estimator at `related module`, sample writer at `related module` (both `vscode`-free so the proxy or CLI can consume the same code), UI in `related module` (`renderRunoutBanner` + `renderUsageCluster` ETA chip), styles in listing media. Unit tests: `related module` (16 tests) + `related module` (9 tests).
- **No vscode dependency in the estimator** — placed under `source` per the extension's TypeScript layout philosophy. Reuses the existing `formatDuration` from `related module` for the human-readable ETA strings.

### Added — Auto-Resume Nudges (Pro)

- **New Stop-hook layer that detects "trivial stops" and auto-resumes.** Sessions that pause to ask "want me to continue?", offer a multi-choice menu when one option is obvious, tell *you* to run a command Claude could run itself, or declare a "good stopping point" with no real reason now get a targeted re-injection prompt and exit-2 resume — reusing the same mechanism the rate-limit auto-resume has proven reliable.
- **8 nudges in the default catalog**, 4 enabled by default (`ask-permission-to-continue`, `offer-multi-choice`, `tell-user-to-do-work`, `pseudo-checkpoint`) and 4 opt-in (`multi-session-defer`, `ask-to-verify`, `sample-instead-of-all`, `restate-then-stop`). Each nudge is an independent toggle in VS Code settings; the catalog itself lives at `~/.power-claude/config/nudges.json` and is user-editable for custom patterns.
- **Hard-stop veto list** — auth failure, missing credential, destructive op pending approval, `/approve-sensitive-edit` style gates, and genuine spec ambiguity always win, even if a lazy-stop pattern also matches.
- **Per-session loop guard** (default 3) prevents nudge/stop ping-pong.
- **Shadow mode** — `powerClaude.autoNudge.shadowMode=true` logs every would-fire decision without resuming, so you can audit the catalog on real sessions before going live.
- **Optional LLM fallback** for ambiguous stops the deterministic catalog missed. Off by default; uses Haiku 4.5 + a ~128-token classifier call when enabled. Requires `ANTHROPIC_API_KEY`.
- **Pro-gated** via `~/.power-claude/state/pro-active` sentinel written by the extension on license validation. Free users see the hook exit 0 silently.
- **Telemetry**: every decision (`fired`, `vetoed`, `loop-guard-exceeded`, `no-match`, `fallback-fired`, `shadow-would-fire`) lands as a JSON line in `~/.power-claude/logs/events.jsonl` tagged `kind=auto-nudge` and `resume_source=trivial-stop-exit-2`.
- **Settings**: `powerClaude.autoNudge.enabled` / `.loopGuardMax` / `.shadowMode` / `.nudges.<id>` / `.fallback.enabled|model|effort`.
- **Bug fix (on-touch)**: `installLifecycleHooks()` and the install-prompt path previously read bundled hook scripts from `${extensionPath}/release tooling`, but the vsix packages them at `release tooling` (per `.vscodeignore`). Both call sites now read from the correct path. Hook install was previously silently failing on fresh installs that relied on the install prompt — now works.

### Added — CLI unification + UI overhaul (the `pc` migration)

- **Single-binary CLI.** All commands now live under one Node binary: `power-claude <cmd>` (canonical) and `pc <cmd>` (short alias, declared in `package.json` `bin`). The dispatcher routes to per-command TypeScript modules in `source`.
- **New commands** ported from the deleted bash bins, each as its own TS module + co-located vitest test:
 - `pc rotate [name]` — auto-rotate or specific rotation
 - `pc remove <name>` — delete a profile (refuses active unless `--force`)
 - `pc save-profile <name>` — save current credentials; `--stdin` reads JSON
 - `pc enable` / `pc disable [--strip-profiles]` — rotation kill switch
 - `pc fix` — clear stuck locks, restart watchers
 - `pc health [--account NAME]` — probe accounts and render
 - `pc doctor` — structured diagnostic checklist
 - `pc install [--no-path]` — first-time setup, wires PATH into shell rc
 - `pc uninstall [--purge]` — reverse install
 - `pc migrate` — copy legacy Claude Code data into `~/.power-claude/`
 - `pc logs [-f] [--level …] [--grep …]` — merged logs + tail with filters
 - `pc run [-- claude args]` — launches `claude` with auto-rotation
 - `pc relogin <name>` / `pc relogin --all` — re-auth via OAuth
 - `pc config get|set|list` — persisted CLI config
 - `pc watch` — **NEW** live TUI: account table + activity stream + modal hotkeys (`s`/`r`/`R`/`q`). Built on shared CLI library shared TUI primitives.
- **shared CLI library shared library** (`shared library/js/cli/`). Reusable Node CLI primitives: ANSI-aware width helpers, threshold-coded utilization bars, status badges, Unicode box-drawing tables, Braille spinner, modal-TUI scaffolding. 201 vitest assertions, 1:1 source-to-test mirror enforcement.
- **Teamclaude-style quota bars.** Threshold colors (green < 70% < yellow < 90% < red) with reset countdown overlaid centered on the bar.
- **First-run CLI nudge.** Extension activation shows a one-time toast offering to run `power-claude install` if `pc` isn't on PATH.

### Removed — BREAKING

The 12 standalone bash CLI scripts are gone. Migration table:

| Old bash command | New equivalent |
|---|---|
| `claude-rotate [name]` | `pc rotate [name]` |
| `claude-health` | `pc health` |
| `claude-relogin <name>` | `pc relogin <name>` |
| `claude-profiles` | `pc list` |
| `claude-watchdog` (manual) | runs only via systemd timer; no CLI surface |
| `claude-auto <args>` | `pc run -- <args>` |
| `claude-save-profile <name>` | `pc save-profile <name>` |
| `claude-rl-logs --grep X` | `pc logs --grep X` |
| `claude-rl-tail` | `pc logs --follow` |
| `claude-dashboard-serve` | `pc serve` |
| `disable-rotation` | `pc disable --strip-profiles` |
| `rate-limit-debug.sh` | internal-only (no PATH entry) |
| `power-claude <subcmd>` (bash) | `power-claude <subcmd>` (TS) — same surface, new implementation |

The bash `bin/power-claude` (1166-line dispatcher) and all 12 standalone bash sources in `release tooling` are deleted. The `package.json` `bin` map exposes only `power-claude` and `pc`.

## [1.0.0] — 2026-03-10

First public release.

### Added
- **Legacy → canonical migration.** First activation after install moves any leftover Power Claude data from older legacy locations into `~/.power-claude/` and deletes the legacy copies. Idempotent; guarded by `~/.power-claude/state/migration-done`.
- **Stale-state cleanup** (`related module`). Removes orphaned `*.tmp.*`, `*.init.*`, dead `proxy.pid`, expired `auto-rewake/*.json` on every activation.
- **Proxy multi-window reference counting** (`related module`). N VS Code windows share a single proxy; the proxy only dies when the LAST window unregisters. Fixes the bug where closing one window broke rotation for every other window.
- **Settings.json cross-window mutation lock** (`related module`, `related module`). Concurrent windows installing hooks no longer clobber each others' edits.
- **First-run setup for npm users** (`related module`). `npm install -g power-claude` followed by any CLI invocation triggers automatic deployment of `~/.power-claude/`, migration, and (optional) hook registration. No manual `power-claude install` required.
- **Version single-source-of-truth** (`related module`). `bin/power-claude:VERSION` is now sed-injected from `package.json` on every build. Pre-publish check fails if the two drift.
- **`Power Claude: Uninstall Everything` command**. Strips every `_powerClaude`-tagged hook from Claude Code's settings file, kills the proxy, deletes `~/.power-claude/`. Two-step confirmation; Claude Code's credentials file and other Claude Code state untouched.
- **9 new npm `bin` entries** so `npm install -g power-claude` puts `claude-rotate`, `claude-health`, `claude-relogin`, `claude-profiles`, `claude-watchdog`, `claude-auto`, `claude-rl-logs`, `claude-save-profile`, `disable-rotation` in PATH automatically alongside `power-claude`.

### Changed
- **Single canonical runtime directory**: `~/.power-claude/`. Only Claude Code's own credentials file and settings file stay under the `~/.claude` directory — those are owned by Claude Code itself. README has a dedicated "What Power Claude writes to disk" section disclosing every path.
- **Lifecycle hook filter widened**. Re-install/uninstall now sweep ALL `_powerClaude` markers starting with `lifecycle-`, not just the exact-marker match. Stale entries from prior versions get swept up automatically.
- **Log rotation in `related module`**. Inline 5 MB rotation per log file — `events.jsonl` no longer grows unbounded.
- **Window registry write-back on prune** (`related module`). Stale `vscode-windows.json` entries get cleaned to disk instead of pruning-in-memory forever.
- **Debounce timers tracked in disposables** (`related module`). Pending timeouts can't fire on a torn-down DataSource.

### Removed
- `installedBy` dual-write to a legacy install marker. Migration removes the legacy marker; activate() writes only the canonical one.

### Fixed
- Rotation died with "no eligible account" when 6/12 accounts were healthy. Root cause: `overageStatus=rejected` (a billing-feature flag, not a rate-limit signal) was treated as an unconditional blocker. Now `overageStatus=rejected` only demotes when `unifiedStatus != "allowed"` (the account is genuinely at quota and has no overage budget). Affects `score.sh:_score_apply_overage_override()` and both cached + live probe paths in `related module`.

### Known limitations (deferred to 1.0.1)
- 28 `fs.watch` calls in `source` are not coalesced across watchers — N windows × 28 file descriptors. Not a correctness issue but resource-heavy under heavy fan-out.

---

## Older releases

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
 `fmt.duration()`, `fmt.bytes()` in `related module`.
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
- **Render pipeline**: `related module` discovers a
 local Playwright install (repo / global / npx cache), launches headless
 Chromium, and screenshots each SVG at 2× pixel density. Run once before
 `vsce publish`; commits PNGs alongside SVGs.

### Payment / licensing (E-14) — confirmed already shipped

The extension does NOT integrate with Stripe / Paddle / FastSpring. License
`https://api.neural-llm.com/license/validate`, which resolves your
subscription state server-side. No additional payment-processor work
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

### Mission expansion

The first paid release. Power Claude moves from reactive (hook-based) to
**pre-emptive** rotation via a local HTTP proxy that intercepts every
Claude Code request, reads `anthropic-ratelimit-unified-*` headers in
real time, and rotates accounts BEFORE quota is hit. Parallel account
mode delivers the long-requested throughput multiplier: with N healthy
accounts, effective ITPM is Nx single-account. Subscription enforcement

### Added

- **Proxy core** (`source`) — Node.js HTTP server (port 3456, no
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
 issues short-lived (1hr) signed JWTs per machine fingerprint. Heartbeat
 refuses to start without a valid license (30-min offline grace period).
 Forced version updates via server-side `minVersion`.
 integrity-verified against tampering, with signed-response verification
 securing communication with the license service.
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
- **Hook fallback** — `related module` now detects
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

 signature using the embedded public key. Tampered or replayed responses
 are rejected.
- JWT session tokens are never written to disk and are cryptographically
 bound to the machine fingerprint (`vscode.env.machineId` + OS
 identifiers).
- Max 2 concurrent sessions per license (home + work). The third
 activation terminates the oldest session.

## [0.14.0-dev] — 2026-02-05 — Insight Graph

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
 session (when auto-resumed). Live under `source`.
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

- Power Claude is now a standalone product, packaged independently for
 clean marketplace shipping.

## [0.13.1] — 2026-01-21 — Watchdog hotfix

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

## [0.13.0] — 2026-01-20 — Continuous Automation

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
- **Inline JSONL lifecycle markers.** Three new session-start, heartbeat,
 and session-end hooks installed into Claude Code's config directory
 append `{"type":"lifecycle",...}` records to each session's JSONL.
 Heartbeats are sampled (every 5th tool call by default) to keep
 transcript size bounded; `session_ended` includes the final TodoWrite
 status snapshot. Idempotent, exit-0-always, line-atomic via O_APPEND
 under PIPE_BUF.
- **Deterministic task-bundle completion.** New
 `related module` exposes `readTaskBundleStatus(jsonlPath)`
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

- **Auto-resume event history was never populated.** The
 Self-Diagnostics reader looked for auto-resume events in a different
 location and field schema than the rotator actually wrote them to, so
 every Power Claude Self-Diagnostics report surfaced an empty array.
 The reader now reads the rotator's actual event log and adapts the
 schema, mapping each rotator event kind (rate-limit-detected,
 rotated, opportunistic-rotate, etc.) to the typed event union;
 unknown kinds map to `system_error` with the original kind preserved.
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
 hooks (bundled inside the .vsix at `related module`).
 Accept once; the extension copies the scripts into Claude Code's
 config directory and registers them in Claude Code's settings file
 (atomic read-modify-write, idempotent,
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

## [0.12.0] — 2026-01-06

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
 reader extracted into shared session snapshot helpers. No
 new instrumentation in Claude Code itself.

### Implementation notes

- New power-claude feature module: `source` (tree
 providers, three webviews, command handlers, vendored Cytoscape +
 fcose + dagre layouts under listing media).
- Pre-existing duplicate-case warnings in `related module` are
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

## [0.11.3] — 2025-12-23 — second bug-hunt pass

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

## [0.11.2] — 2025-12-21 — bug-hunt fixes

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
- **Refresh storm from Claude Code state-directory writes.** The home-dir
 `fs.watch` callback called `refresh()` synchronously, but the state
 dir holds many unrelated files (`vscode-windows.json` heartbeat
 every 15s from every VS Code window, `rate-limits.json`, cooldown
 sentinels, lockout files). Routed the home-dir watcher through the
 same `debouncedRefresh(200ms)` already used for the workspace
 watcher.

## [0.11.1] — 2025-12-20 — extension-host freeze fix

### Fixed
- **Extension-host freeze on activate against a large Claude Code session-transcripts directory**
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
- **`related module`**: defers the JSONL bucket read by 5 s on
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

## [0.11.0] — 2025-12-19 — recursive cleanup pass

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
 falls back to direct read of Claude Code's session transcripts. Source badge
 in the LLM Usage header tells the user which path is providing numbers.
- Background freshness loop — periodically refreshes when data is stale.
- One-time, dismissible prompt to install the rate-limit anchor hook when
 Claude Code's rate-limit handler is missing the marker. Per-day
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
- esbuild bundling — `related module` is a single self-contained CJS
 bundle (`vscode` is the only external).

## [0.10.1] — 2025-12-08

### Added
- Account rotation dashboard (accounts / sessions / history tabs).
- Cross-system links (git ↔ session refs ↔ events).
- Auto-deploy watcher — sentinel-based zero-friction "edit src → live
 extension" reload (opt-out via the auto-reload configuration key).
- LLM usage analytics sub-module.
