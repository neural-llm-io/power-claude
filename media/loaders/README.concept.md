# Power Claude Loader Screens

Four real CSS/SVG animated loading screens based on the Power Claude neural-node and lightning-bolt identity.

## Open immediately

Open `gallery.html` directly in Chrome, Edge, Firefox, or a VS Code webview. It has all JavaScript embedded and does not need a local server.

Standalone screens:

- `energy-pulse.html`
- `data-stream.html`
- `circuit-sync.html`
- `neural-scan.html`

## Add to Power Claude

Copy `power-claude-loaders.js` into the extension/webview assets and load it as a normal classic script:

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

No external images, fonts, modules, CDN calls, framework, or build step are required.
