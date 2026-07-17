# Power Claude branded loaders (media)

## Injectable loader contract (product code)

Power Claude **already** has an injectable loader package:

| Layer | Location |
|-------|----------|
| Shared contract | `@cj-hurc/webview-ui` → `Loader.ts` (`renderLoaderTemplate`, `__pcLoader.show/hide`) |
| PC brand markup | `power-claude/src/extension/webview/neuralLoader.ts` (`PC_NEURAL_LOADER_HTML`) |
| PC brand CSS | `power-claude/media/dashboard.css` (Neural Core) |
| Claude Code chat | `powerClaude.animatedLoader.mode` + `animatedLoaderPatch.ts` |

Consumers register **one** `<template data-pc-loader-template>` per webview; every table/page/busy state clones it. Custom spinners are injected by swapping that template HTML (and CSS), not by hardcoding a spinner in each component.

## Assets in this folder

| File | Role |
|------|------|
| `power-claude-neural-ignition.gif` | Full-screen / splash-style neural ignition concept (420×420). Unique brand motion — preferred for site splash / first-paint / marketing. |
| `power-claude-loaders.js` | Concept package: four CSS/SVG web-component variants (`energy`, `data`, `circuit`, `neural`) for future site/extension full-screen loaders. |
| `gallery.html` | Open locally to preview all four variants. |
| `previews/*` | GIF/PNG previews of each variant + combined board. |
| `README.concept.md` | Upstream concept notes from the design package. |

These media files are **brand assets / concepts**. Wiring a site-wide page loader should use the injectable contract above and can point at `power-claude-neural-ignition.gif` or a slim CSS clone of Neural Core for production (prefer CSS for small UI chrome; GIF for splash).

## Suggested product wiring (not all done here)

1. **Marketing site (neural-llm.com):** optional first-paint overlay using ignition GIF or a CSS Neural Core, max ~1.2s, `prefers-reduced-motion: reduce` → static frame.
2. **Extension dashboard:** keep CSS Neural Core via `renderLoaderTemplate("pc", PC_NEURAL_LOADER_HTML)`.
3. **Full-screen agent boot:** evaluate `power-claude-loaders.js` variants as optional splash; do not replace the injectable template contract.

