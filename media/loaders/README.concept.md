# [grok:grok-4.5][client:0.2.93][hurc:v0.12.940] Power Claude Loader Screens (concept package notes)

Four real CSS/SVG animated loading screens based on the Power Claude neural-node
and lightning-bolt identity.

## Open immediately

Open `gallery.html` in the **public** pack:

`power-claude-public/media/loaders/gallery.html`

(Open in Chrome, Edge, Firefox, or a VS Code webview. Fully self-contained.)

Standalone screens (in the original zip under `neural-llm.com/tmp/`):

- `energy-pulse.html`
- `data-stream.html`
- `circuit-sync.html`
- `neural-scan.html`

## Add to Power Claude

Copy `power-claude-loaders.js` into webview assets and load as a classic script:

```html
<script src="power-claude-loaders.js"></script>
<power-claude-loader
  variant="neural"
  message="INITIALIZING AGENT"
  detail="RESTORING SESSION"
  size="420"
  speed="1">
</power-claude-loader>
```

Variants: `energy`, `data`, `circuit`, `neural`.

No external images, fonts, modules, CDN, framework, or build step required.

## Production note

Dashboard busy states should keep using the injectable Neural Core template
(`src/extension/webview/neuralLoader.ts` + `window.__pcLoader`). These full-screen
variants and `power-claude-neural-ignition.gif` are for splash / marketing / optional
agent-boot screens — not a second spinner library.
