<!-- [claude:sonnet-4-6][stack:v0.2.0] v1.0.0 marketing-grade README rewrite for marketplace launch -->

# Power Claude — AI Session Insights

> GitLens for your AI sessions. See what every Claude session changed — commits, files, models, costs, hooks, sub-agents — in one connected graph.

Built on three pillars: multi-account rotation keeps Claude flowing through rate limits, a resilience watchdog recovers crashes and incomplete runs, and the Insight Graph turns every session's raw history into a navigable, linked audit trail.

![Power Claude Insight Graph](docs/marketplace/screenshots/hero-insight-graph.png)

[![Marketplace](https://img.shields.io/badge/marketplace-neural--llm.power--claude-2b6cb0.svg)](https://marketplace.visualstudio.com/items?itemName=neural-llm.power-claude)
[![Homepage](https://img.shields.io/badge/homepage-neural--llm.com-1a73e8.svg)](https://neural-llm.com/power-claude)

---

## The Insight Graph

Every developer who uses Claude Code asks the same questions after a long session: *What did it actually change? Which files did it touch? What model did it use and what did that cost me? Did it finish, or did it quietly stop mid-task?* Today you answer those by hunting through JSONL transcripts and git diffs. Power Claude answers them in one click.

### What you see

The Insight Graph renders your Claude session history as a commit-graph-style lane view — the same visual language GitLens made familiar for git, applied to AI coding sessions. Each row is a session. Each session carries:

- **Model badge** — which Claude model (Sonnet, Opus, Haiku) ran in this session, with version
- **Cost** — total dollars spent, broken down by model if it switched mid-session
- **Files-changed badge** — how many files were read, written, or edited
- **Account** — which of your accounts handled this session
- **Completion status** — green check (every TodoWrite item completed), yellow warning (pending tasks remain), or neutral (agent never called TodoWrite)

### Click any session, see everything it touched

Selecting a session expands the full detail view without leaving VS Code:

- **Files panel** — every file the agent read, wrote, or edited, with per-file diff vs the session's git snapshot, op-type counts, and last-touched timestamps
- **Sub-agents spawned** — if the session forked sub-agents, they appear as child lanes in the graph, linked back to the parent session
- **Hooks fired** — which `~/.claude/hooks/` scripts ran during this session, with exit codes and timing
- **Rate-limit events** — when the session hit a cap, which account it rotated to, and how long the cooldown lasted
- **Plans drafted** — plan-mode artifacts the agent created, linked to the session that authored them
- **Commits authored** — every `git commit` the session produced, clickable to open the diff

This is the session history Claude Code has always been generating — Power Claude makes it navigable.

### Inline session blame in the editor gutter

Open any file and Power Claude annotates each region with the Claude session that last touched it — exactly like git blame, but for AI editing activity. Hover a blame annotation to see the session summary (date, model, cost, completion status) without switching panels. Click to jump to that session's full detail view.

Works alongside GitLens. The two annotations occupy separate gutter columns and use distinct visual language so they never conflict.

### Hover cards everywhere

Every element in the Insight Graph carries a hover card. Hover an account chip to see its current rate-limit state, today's spend, and which cooldown window it is in. Hover a model badge to see token counts and what the same work would have cost on a different tier. Hover a files-changed badge to see the top-touched files without opening the detail view. No jumping context.

### Multi-track timeline

The session detail Timeline tab shows tool calls, hook firings, model switches, and rate-limit events on a synchronized horizontal timeline — the same time axis, rendered as swim lanes. You can see that the session switched from Sonnet to Opus at minute 4, hit a rate limit at minute 9, rotated to a second account at minute 9.3, and resumed at minute 9.5. Each event is clickable.

### Cost breakdown with subscription savings

The cost panel shows what each session cost you under your current subscription tier and what the equivalent API calls would have cost at pay-per-token rates. If you are on the Max plan, Power Claude surfaces the effective cost of each session in both terms. If you are on a lower tier and regularly hitting rate limits during high-Opus sessions, the recommender flags when upgrading would eliminate cap hits that currently stall your workflow.

---

## The three pillars

The Insight Graph is powered by session data that Power Claude collects through three underlying capabilities. Understanding them helps you get the most out of the graph.

### Multi-account rotation

Connect personal, team, and project-specific Claude accounts. Power Claude watches rate limits in real time via the `~/.claude/` state directory that Claude Code writes itself. When the active account hits a cap:

1. The Stop hook fires and Power Claude detects the rate-limit signal
2. The soonest-recovering account is activated automatically
3. The interrupted session resumes in the same VS Code tab — same context, same conversation, no retyping

The status bar shows a live count of healthy / cooling / blocked accounts. The accounts dashboard shows cooldown ETAs and lets you manually activate, refresh, or re-authenticate any account. Throttle-only mode and a master rotation switch are available from the command palette without leaving your editor.

**What this means for the Insight Graph**: rate-limit events appear as annotations on the session lane, with the exact rotation timestamp and which account took over. You can see whether a session's model quality degraded when it rotated from a Max account to a Pro account.

### ⚡ Balanced Mode — N× throughput + smart 429 routing

Multi-account rotation reacts to exhaustion. Balanced Mode is proactive: every request is routed to the **least-busy account simultaneously**, so all your accounts fill in parallel instead of draining one before moving to the next.

Each Claude.ai account has independent **5-hour, 7-day, per-minute token (TPM), and per-minute request (RPM)** rate-limit windows. With three accounts in Balanced Mode you get an effective **~3× ceiling on every one of them** — heavy Opus sessions that used to stall every 30 minutes run uninterrupted, and the per-minute throttling that sometimes choked single-account streaming during heavy sub-agent fan-out simply doesn't happen.

| Mode | How it works | Best for |
|------|-------------|----------|
| **Standard rotation** | Stays on one account until it exhausts, then switches | Light to moderate usage |
| **Balanced Mode** | Every request goes to the least-loaded account | Heavy / continuous coding sessions |

**Smart 429 routing** is the second half of the multiplier. When an account returns 429 (whether it's a per-minute throttle or a hard quota signal), the proxy used to sleep `Retry-After` seconds and retry the same account. Now it tries a healthy alternate first — flipping to another account in your pool instead of waiting up to 120 seconds. The throttled account is put in cooldown so the selector can't pick it again until Anthropic says it's ready. **Anti-ping-pong is structural, not a heuristic**: each 429 marks its account out for `Retry-After` seconds, so the proxy can't bounce between two throttled accounts. If the entire pool is throttled at the same time, the proxy falls back to the existing wait-and-retry path on the least-bad account — so you never end up in a worse state than before.

The status bar shows `⚡ Balanced [3] ~3×` while active so you can see the multiplier at a glance. The dashboard also tracks `N throttle waits avoided` cumulatively so you can see the smart 429 router doing its job. Enable from the **Power Claude Settings** panel in one click — no CLI, no config files. Or via CLI: `power-claude balanced on`.

> **Why it works**: Claude.ai Pro and Max subscriptions each carry their own 5-hour, 7-day, TPM, and RPM rate-limit windows. Accounts are completely independent organizations on Anthropic's side — there is no shared pool. Balanced Mode + smart 429 routing simply uses them all, all the time.

### Session-resilience watchdog

Rate limits are not the only thing that kills a Claude session. Process kills, OOM events, IDE crashes, network drops mid-tool-call, and sessions that ended cleanly but left work unfinished all used to leave you with a stale tab and a manual recovery.

The watchdog polls every 30 seconds and applies four detection rules:

| Trigger | Signal | What it means |
|---------|--------|---------------|
| **Heartbeat-stale** | No `lifecycle:heartbeat` in N seconds AND JSONL idle | Process kill, OOM, IDE crash, or network drop |
| **Tool-truncation** | Last assistant record is `stop_reason: tool_use` with no follow-up | Died mid-tool-call |
| **Ended with pending tasks** | Stopped cleanly but TodoWrite items still pending | Session said "done" but work remains |
| **Rate-limit** | `pending-recovery.json` written by Stop hook | Standard rate-limit rotation |

When the watchdog fires, Power Claude surfaces a one-click QuickPick with a reason-aware resume prompt — heartbeat-stale, tool-truncation, and unfinished-task cases each get tailored wording so the agent picks up with the right context.

**What this means for the Insight Graph**: recovered sessions show the recovery event in their timeline. You can see the gap between the last heartbeat and the resume, what type of death occurred, and which resume prompt was injected.

### LLM usage analytics

Power Claude tracks token consumption and dollar cost per session, per account, and per model with plan-tier-aware cost math:

- **Per-account breakdown** by model (Sonnet, Opus, Haiku) with daily / weekly / monthly rollups
- **Anchor markers** showing exactly when rate-limit caps were reached in your session history
- **Cap-hit recommender** that surfaces when upgrading your plan would eliminate throttling that regularly stalls your workflow
- **Subscription savings** showing your effective cost under your current tier versus pay-per-token API rates

All analytics run locally. Power Claude reads from `~/.claude/state/` and `~/.claude/projects/*.jsonl` — the same files Claude Code writes. No token counts, transcripts, or usage data leave your machine.

---

## Quickstart

**Install from the Marketplace:**

```bash
code --install-extension neural-llm.power-claude
```

Or search "Power Claude" in the VS Code Extensions panel.

**First launch:**

1. Click the Power Claude icon in the activity bar (the graph icon)
2. The extension reads your existing `~/.claude/` state and surfaces every account you have already authenticated
3. The Insight Graph populates immediately — no configuration required

**Add more accounts:**

Click **Link Account** in the accounts tree to walk through `claude login` for a new account profile. Multiple accounts enable rotation.

**Enable the full watchdog:**

Run "Power Claude: Install Session Lifecycle Hooks" from the command palette. This installs three lightweight hooks into `~/.claude/hooks/lifecycle/` that emit heartbeat and session-end markers — the watchdog's precision detection depends on these. Opt-in; the extension never modifies your Claude home directory without explicit consent.

**Enable editor gutter blame:**

Timeline tracking is opt-in. Run "Power Claude: Install Timeline Hook" from the command palette to enable AI-edit annotations in VS Code's Timeline view and the editor gutter.

**Pro features:**

Enter your license key in `Settings > Power Claude > License Key`. The free tier activates automatically on install. See [Free vs Pro](#free-vs-pro) for what each tier includes.

---

## Free vs Pro

See [docs/PRICING.md](docs/PRICING.md) for current pricing and tier details.

The free tier gives you the Insight Graph (read-only), multi-account rotation for up to two accounts, basic LLM usage analytics, and session history for the last 7 days.

Pro unlocks unlimited accounts, the full watchdog with all four detection rules, the editor gutter blame annotations, the session graph view (Cytoscape.js force-directed and hierarchical layouts), pre-commit review, advanced search with field filters, and session history with no day limit.

---

## FAQ

**Does this work with the Anthropic API directly, or only with Claude Code?**

Power Claude is built specifically for Claude Code — the CLI and IDE tool at `claude.ai/code`. It reads from `~/.claude/` which is written by Claude Code itself. It does not work with raw Anthropic API calls or with Claude.ai in the browser.

**What data leaves my machine?**

Only your license key, a hashed machine identifier, and the extension version are transmitted — to `api.neural-llm.com` during license validation. That validation is cached locally for 24 hours; no call is made on every keystroke. No prompts, no file contents, no transcripts, no usage data, no authentication tokens. Full details at [neural-llm.com/privacy](https://neural-llm.com/privacy).

**Can I use multiple Claude accounts?**

Yes. This is one of Power Claude's core capabilities. Add as many accounts as you have. Power Claude tracks health, cooldown state, and spend per account, and rotates automatically when the active account hits a rate limit. The Insight Graph annotates which account handled each part of a session.

**What happens when I hit a Claude rate limit?**

If you have a second healthy account, Power Claude rotates to it automatically and resumes your session — usually within a few seconds. If all accounts are in cooldown, Power Claude displays the soonest-recovering countdown and optionally (`powerClaude.autoSelectSoonest`) activates the first account whose cooldown clears.

**How is this different from GitLens?**

GitLens maps your git history to your code. Power Claude maps your *AI session history* to your code. The two are complementary and designed to coexist — each annotates a different dimension of how your codebase changed. GitLens tells you which commit introduced a line. Power Claude tells you which Claude session wrote that commit, what it cost, which model it used, and whether it finished what it started.

**How much does Pro cost?**

See [neural-llm.com/power-claude](https://neural-llm.com/power-claude) for current pricing. A free tier with no time limit is available.

**What is the refund policy?**

Full refund within 14 days of purchase, no questions asked. Contact [support@neural-llm.com](mailto:support@neural-llm.com) with your order details.

---

## Extending Power Claude

Power Claude exposes a stable public API for other VS Code extensions to read session data, contribute custom tabs to the Session Detail webview, and enrich the Insight Graph with domain-specific data.

```ts
// In your extension's activate():
const powerClaude = vscode.extensions.getExtension("neural-llm.power-claude");
const api = await powerClaude.activate();   // PowerClaudePublicApi

// Read the live session index.
const sessions = api.sessions.list({ limit: 20 });
api.sessions.onDidChange(() => /* re-read */);

// Contribute a new tab to the Session Detail webview.
api.contributeSessionDetailTab({
  id:    "myExt.audit",
  label: "Audit",
  render(ctx) {
    return {
      html: `<p>Audit findings for ${ctx.sessionId}</p>`,
      messageHandlers: {
        "myExt.audit.openTrace": (payload) => /* … */,
      },
    };
  },
});

// Contribute a session enricher (lightweight read-only augmentation).
api.contributeSessionEnricher({
  id: "myExt.severityScore",
  label: "Severity Score",
  enrich(session) { return { score: 0.42 }; },
});
```

Full API surface in [src/extension/api/types.ts](src/extension/api/types.ts). Contracts under the `PowerClaudePublicApi` interface follow semver — breaking changes are rare and announced in the changelog.

---

## What Power Claude does NOT do

- Does not make API calls to Anthropic on your behalf
- Does not transmit your prompts, code, transcripts, or authentication tokens off your machine
- Does not modify your global Claude Code config without explicit consent (all hook installers are opt-in command-palette invocations)
- Does not require any VS Code workspace to be open — the extension activates on `~/.claude/` state changes regardless

---

## Privacy

Local-first. Power Claude reads from:

- `~/.claude/state/` — your Claude Code state, written by Claude Code itself
- `~/.claude/profiles/` — your account profile JSONs, written by `claude login`
- `~/.claude/projects/` — your transcripts, used only for token-bucket counts and session indexing
- `~/.claude/state/ai-edits.jsonl` — only if you opt in to Timeline tracking

No file outside `~/.claude/` is read without explicit user action. Full privacy policy at [neural-llm.com/privacy](https://neural-llm.com/privacy).

---

## Support

- Bug reports: [github.com/neural-llm-io/power-claude/issues](https://github.com/neural-llm-io/power-claude/issues)
- Email: [support@neural-llm.com](mailto:support@neural-llm.com)
- Sales / licensing: [legal@neural-llm.com](mailto:legal@neural-llm.com)

---

## License

Neural-LLM commercial EULA — see [LICENSE](LICENSE) and [neural-llm.com/power-claude/license](https://neural-llm.com/power-claude/license). Copyright (c) 2026 Neural-LLM.

---

## Trademarks

Claude and Claude Code are trademarks of Anthropic PBC. Visual Studio Code is a trademark of Microsoft Corporation. Cursor is a trademark of Anysphere Inc. Neural-LLM is not affiliated with, endorsed by, or sponsored by Anthropic, Microsoft, or Anysphere. Power Claude is an independent third-party tool that interoperates with the public file outputs of Claude Code.
