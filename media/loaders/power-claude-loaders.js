(() => {
  const template = document.createElement('template');
  template.innerHTML = `
<style>
  :host {
    --pc-size: 420px;
    --pc-speed: 1;
    --pc-cyan: #29dcff;
    --pc-blue: #3b82f6;
    --pc-violet: #8b5cf6;
    --pc-pink: #e879f9;
    --pc-ink: #050817;
    --pc-panel: #071126;
    --pc-text: #d9ecff;
    display: inline-block;
    width: min(var(--pc-size), 100%);
    color: var(--pc-text);
    font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  }
  * { box-sizing: border-box; }
  .screen {
    position: relative;
    width: 100%;
    aspect-ratio: 1;
    overflow: hidden;
    display: grid;
    grid-template-rows: 1fr auto;
    border: 1px solid rgba(113, 181, 255, .13);
    border-radius: 13.5%;
    background:
      radial-gradient(circle at 50% 44%, rgba(34, 211, 238, .075), transparent 35%),
      radial-gradient(circle at 64% 25%, rgba(139, 92, 246, .095), transparent 29%),
      linear-gradient(145deg, #071024 0%, #081328 50%, #040817 100%);
    box-shadow:
      inset 0 1px 0 rgba(255,255,255,.035),
      inset 0 0 80px rgba(3,7,18,.72),
      0 24px 80px rgba(0,0,0,.34);
    isolation: isolate;
  }
  .screen::before {
    content: "";
    position: absolute;
    inset: 0;
    z-index: -1;
    background:
      linear-gradient(135deg, transparent 0 20%, rgba(58, 91, 153, .07) 20% 27%, transparent 27% 73%, rgba(58, 91, 153, .07) 73% 80%, transparent 80%),
      repeating-linear-gradient(0deg, transparent 0 23px, rgba(106, 189, 255, .021) 24px),
      repeating-linear-gradient(90deg, transparent 0 23px, rgba(106, 189, 255, .018) 24px);
    mask-image: radial-gradient(circle at center, black, transparent 78%);
  }
  .visual { position: relative; min-height: 0; display: grid; place-items: center; }
  svg { width: 100%; height: 100%; overflow: visible; }
  .caption {
    position: relative;
    padding: 0 28px 26px;
    text-align: center;
    letter-spacing: .28em;
    text-transform: uppercase;
    font-size: clamp(10px, 2.8vw, 13px);
    font-weight: 750;
    color: #cce4fa;
    text-shadow: 0 0 18px rgba(34, 211, 238, .35);
  }
  .caption::after {
    content: "";
    position: absolute;
    left: 32%; right: 32%; bottom: 17px;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(41,220,255,.72), rgba(232,121,249,.7), transparent);
    transform-origin: center;
    animation: caption-line calc(1.8s / var(--pc-speed)) ease-in-out infinite;
  }
  .detail {
    display: block;
    margin-top: 7px;
    font-size: .68em;
    letter-spacing: .17em;
    font-weight: 580;
    color: #6f89a8;
  }
  .grid-dot { fill: #67dffc; opacity: .14; }
  .mesh, .spoke, .ring, .trace, .tick, .stream, .beam {
    fill: none; vector-effect: non-scaling-stroke; stroke-linecap: round; stroke-linejoin: round;
  }
  .mesh { stroke: url(#meshGrad); stroke-width: 3; opacity: .66; }
  .spoke { stroke: url(#meshGrad); stroke-width: 2.5; opacity: .58; }
  .node-shell { fill: #0d2040; stroke: #68eaff; stroke-width: 2; }
  .node-core { fill: url(#nodeGrad); filter: url(#nodeGlow); }
  .core-disc { fill: url(#coreGrad); opacity: .9; filter: url(#coreGlow); }
  .core-ring { fill: none; stroke: url(#meshGrad); stroke-width: 2; opacity: .5; }
  .bolt { fill: url(#boltGrad); filter: url(#boltGlow); }
  .logo { transform-origin: 210px 190px; }
  .node { transform-box: fill-box; transform-origin: center; }
  .ambient-orbit { fill: none; stroke: url(#meshGrad); stroke-width: 1.2; opacity: .18; stroke-dasharray: 5 10; transform-origin: 210px 190px; }

  /* ENERGY PULSE */
  .energy .logo { animation: energy-logo calc(2.2s / var(--pc-speed)) cubic-bezier(.4,0,.2,1) infinite; }
  .energy .pulse-ring { fill: none; stroke: url(#meshGrad); stroke-width: 2; opacity: 0; transform-origin: 210px 190px; animation: energy-ring calc(2.2s / var(--pc-speed)) ease-out infinite; }
  .energy .pulse-ring.r2 { animation-delay: calc(-.73s / var(--pc-speed)); }
  .energy .pulse-ring.r3 { animation-delay: calc(-1.46s / var(--pc-speed)); }
  .energy .beam { stroke: url(#beamGrad); stroke-width: 3; stroke-dasharray: 24 190; filter: url(#beamGlow); animation: beam-run calc(1.4s / var(--pc-speed)) linear infinite; }
  .energy .beam-soft { stroke-width: 12; opacity: .12; }
  .energy .node { animation: node-pop calc(2.2s / var(--pc-speed)) ease-in-out infinite; }
  .energy .node.n2 { animation-delay: calc(-.36s / var(--pc-speed)); }
  .energy .node.n3 { animation-delay: calc(-.72s / var(--pc-speed)); }
  .energy .node.n4 { animation-delay: calc(-1.08s / var(--pc-speed)); }
  .energy .node.n5 { animation-delay: calc(-1.44s / var(--pc-speed)); }
  .energy .node.n6 { animation-delay: calc(-1.80s / var(--pc-speed)); }
  .energy .bolt { animation: bolt-flare calc(2.2s / var(--pc-speed)) ease-in-out infinite; transform-origin: 210px 190px; }

  /* DATA STREAM */
  .data .stream { stroke: url(#streamGrad); stroke-width: 2; opacity: .48; stroke-dasharray: 5 14 22 16; animation: stream-fall calc(1.65s / var(--pc-speed)) linear infinite; }
  .data .stream.s2 { animation-duration: calc(2.05s / var(--pc-speed)); animation-delay: calc(-.5s / var(--pc-speed)); opacity: .30; }
  .data .stream.s3 { animation-duration: calc(1.35s / var(--pc-speed)); animation-delay: calc(-.9s / var(--pc-speed)); opacity: .38; }
  .data .stream.s4 { animation-duration: calc(2.4s / var(--pc-speed)); animation-delay: calc(-1.2s / var(--pc-speed)); opacity: .28; }
  .data .logo { animation: data-float calc(2.5s / var(--pc-speed)) ease-in-out infinite; }
  .data .mesh, .data .spoke { stroke-dasharray: 10 8; animation: mesh-flow calc(1.1s / var(--pc-speed)) linear infinite; }
  .data .node { animation: data-node calc(1.8s / var(--pc-speed)) steps(2,end) infinite; }
  .data .node.n2 { animation-delay: calc(-.3s / var(--pc-speed)); }
  .data .node.n3 { animation-delay: calc(-.6s / var(--pc-speed)); }
  .data .node.n4 { animation-delay: calc(-.9s / var(--pc-speed)); }
  .data .node.n5 { animation-delay: calc(-1.2s / var(--pc-speed)); }
  .data .node.n6 { animation-delay: calc(-1.5s / var(--pc-speed)); }
  .data .packet { fill: #eafbff; filter: url(#nodeGlow); animation: packet-blink calc(.72s / var(--pc-speed)) linear infinite; }
  .data .scanline { fill: url(#scanlineGrad); opacity: .22; animation: scanline-down calc(2.1s / var(--pc-speed)) linear infinite; }

  /* CIRCUIT SYNC */
  .circuit .trace { stroke: url(#meshGrad); stroke-width: 2; stroke-dasharray: 220; stroke-dashoffset: 220; filter: url(#softGlow); animation: trace-draw calc(2.4s / var(--pc-speed)) cubic-bezier(.65,0,.2,1) infinite; }
  .circuit .trace.t2 { animation-delay: calc(-.4s / var(--pc-speed)); }
  .circuit .trace.t3 { animation-delay: calc(-.8s / var(--pc-speed)); }
  .circuit .trace.t4 { animation-delay: calc(-1.2s / var(--pc-speed)); }
  .circuit .trace.t5 { animation-delay: calc(-1.6s / var(--pc-speed)); }
  .circuit .trace.t6 { animation-delay: calc(-2.0s / var(--pc-speed)); }
  .circuit .tick { stroke: #8feaff; stroke-width: 2; opacity: .18; animation: tick-lock calc(1.8s / var(--pc-speed)) ease-in-out infinite; }
  .circuit .logo { animation: sync-lock calc(2.4s / var(--pc-speed)) cubic-bezier(.22,1,.36,1) infinite; }
  .circuit .mesh { stroke-dasharray: 14 6; animation: mesh-flow calc(1.4s / var(--pc-speed)) linear infinite; }
  .circuit .spoke { animation: spoke-flash calc(1.2s / var(--pc-speed)) ease-in-out infinite; }
  .circuit .bolt { animation: sync-bolt calc(2.4s / var(--pc-speed)) ease-in-out infinite; }
  .circuit .sync-ring { fill: none; stroke: url(#meshGrad); stroke-width: 2; stroke-dasharray: 4 9; opacity: .38; transform-origin: 210px 190px; animation: rotate calc(5s / var(--pc-speed)) linear infinite; }

  /* NEURAL SCAN */
  .neural .scan-ring { fill: none; stroke: url(#meshGrad); stroke-width: 1.7; stroke-dasharray: 8 14; opacity: .4; transform-origin: 210px 190px; animation: rotate calc(5.4s / var(--pc-speed)) linear infinite; }
  .neural .scan-ring.r2 { animation-direction: reverse; animation-duration: calc(3.4s / var(--pc-speed)); opacity: .24; }
  .neural .scanner { transform-origin: 210px 190px; animation: rotate calc(2.25s / var(--pc-speed)) linear infinite; }
  .neural .scanner-wedge { fill: url(#scannerGrad); opacity: .52; filter: url(#softGlow); }
  .neural .scanner-line { stroke: #bff7ff; stroke-width: 2; filter: url(#beamGlow); }
  .neural .logo { animation: neural-breathe calc(2.25s / var(--pc-speed)) ease-in-out infinite; }
  .neural .node { animation: neural-node calc(2.25s / var(--pc-speed)) ease-in-out infinite; }
  .neural .node.n2 { animation-delay: calc(-.375s / var(--pc-speed)); }
  .neural .node.n3 { animation-delay: calc(-.75s / var(--pc-speed)); }
  .neural .node.n4 { animation-delay: calc(-1.125s / var(--pc-speed)); }
  .neural .node.n5 { animation-delay: calc(-1.5s / var(--pc-speed)); }
  .neural .node.n6 { animation-delay: calc(-1.875s / var(--pc-speed)); }
  .neural .ambient-orbit { animation: rotate calc(8s / var(--pc-speed)) linear infinite; }
  .neural .bolt { animation: neural-bolt calc(1.15s / var(--pc-speed)) ease-in-out infinite; }

  @keyframes caption-line { 0%,100% { transform: scaleX(.28); opacity:.28 } 50% { transform: scaleX(1); opacity:.9 } }
  @keyframes rotate { to { transform: rotate(360deg); } }
  @keyframes energy-logo { 0%,100% { transform: scale(.95); filter: brightness(.9) } 48% { transform: scale(1.035); filter: brightness(1.25) } 58% { transform: scale(1.01); } }
  @keyframes energy-ring { 0% { transform: scale(.45); opacity:0 } 14% { opacity:.7 } 85%,100% { transform: scale(1.25); opacity:0 } }
  @keyframes beam-run { to { stroke-dashoffset: -214; } }
  @keyframes node-pop { 0%,65%,100% { transform: scale(.92); opacity:.62 } 18%,36% { transform: scale(1.16); opacity:1 } }
  @keyframes bolt-flare { 0%,65%,100% { transform: scale(.94); opacity:.72 } 43%,55% { transform: scale(1.08); opacity:1; filter: url(#boltGlow) brightness(1.5) } }
  @keyframes stream-fall { to { stroke-dashoffset: -180; } }
  @keyframes data-float { 0%,100% { transform: translateY(3px) scale(.98) } 50% { transform: translateY(-4px) scale(1.015) } }
  @keyframes mesh-flow { to { stroke-dashoffset: -36; } }
  @keyframes data-node { 0%,72%,100% { opacity:.55; transform: scale(.94) } 74%,86% { opacity:1; transform: scale(1.12) } }
  @keyframes packet-blink { 0%,48% { opacity:.2 } 50%,100% { opacity:1 } }
  @keyframes scanline-down { 0% { transform: translateY(-170px) } 100% { transform: translateY(210px) } }
  @keyframes trace-draw { 0% { stroke-dashoffset:220; opacity:0 } 20% { opacity:.85 } 52% { stroke-dashoffset:0; opacity:.95 } 80%,100% { stroke-dashoffset:-220; opacity:0 } }
  @keyframes tick-lock { 0%,100% { opacity:.08 } 45%,60% { opacity:.8 } }
  @keyframes sync-lock { 0%,26%,100% { transform: scale(.94); filter: blur(.25px) brightness(.85) } 38% { transform: scale(1.04) rotate(-1.2deg); filter: brightness(1.28) } 48% { transform: scale(1.015) rotate(.7deg) } 58%,72% { transform: scale(1); filter: brightness(1.05) } }
  @keyframes spoke-flash { 0%,100% { opacity:.28 } 50% { opacity:.95 } }
  @keyframes sync-bolt { 0%,28%,100% { opacity:.6; transform:scale(.94) } 42%,70% { opacity:1; transform:scale(1.06) } }
  @keyframes neural-breathe { 0%,100% { transform:scale(.97); opacity:.82 } 50% { transform:scale(1.02); opacity:1 } }
  @keyframes neural-node { 0%,74%,100% { opacity:.46; transform:scale(.91) } 12%,30% { opacity:1; transform:scale(1.18) } }
  @keyframes neural-bolt { 0%,100% { opacity:.68; filter:url(#boltGlow) brightness(.85) } 50% { opacity:1; filter:url(#boltGlow) brightness(1.45) } }

  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { animation-duration: 1ms !important; animation-iteration-count: 1 !important; }
  }
</style>
<div class="screen" role="status" aria-live="polite">
  <div class="visual">
    <svg viewBox="0 0 420 340" aria-hidden="true">
      <defs>
        <linearGradient id="meshGrad" x1="110" y1="95" x2="310" y2="270" gradientUnits="userSpaceOnUse">
          <stop stop-color="#22d3ee"/><stop offset=".5" stop-color="#60a5fa"/><stop offset="1" stop-color="#c084fc"/>
        </linearGradient>
        <radialGradient id="nodeGrad"><stop stop-color="#effcff"/><stop offset=".32" stop-color="#56ddff"/><stop offset="1" stop-color="#4f46e5"/></radialGradient>
        <radialGradient id="coreGrad"><stop stop-color="#e0fbff"/><stop offset=".24" stop-color="#36d7ff"/><stop offset=".62" stop-color="#7348ff"/><stop offset="1" stop-color="#101b4c"/></radialGradient>
        <linearGradient id="boltGrad" x1="175" y1="125" x2="245" y2="255" gradientUnits="userSpaceOnUse"><stop stop-color="#fff"/><stop offset=".2" stop-color="#7de8ff"/><stop offset=".55" stop-color="#b56cff"/><stop offset="1" stop-color="#ff72cf"/></linearGradient>
        <linearGradient id="beamGrad"><stop stop-color="#22d3ee" stop-opacity="0"/><stop offset=".45" stop-color="#a7f3ff"/><stop offset=".55" stop-color="#fff"/><stop offset="1" stop-color="#e879f9" stop-opacity="0"/></linearGradient>
        <linearGradient id="streamGrad" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#22d3ee" stop-opacity="0"/><stop offset=".35" stop-color="#22d3ee"/><stop offset=".72" stop-color="#a855f7"/><stop offset="1" stop-color="#e879f9" stop-opacity="0"/></linearGradient>
        <linearGradient id="scanlineGrad" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#22d3ee" stop-opacity="0"/><stop offset=".55" stop-color="#a7f3ff"/><stop offset="1" stop-color="#22d3ee" stop-opacity="0"/></linearGradient>
        <radialGradient id="scannerGrad" cx="0" cy="1" r="1"><stop stop-color="#80f3ff" stop-opacity=".7"/><stop offset="1" stop-color="#6d5dfc" stop-opacity="0"/></radialGradient>
        <filter id="nodeGlow" x="-150%" y="-150%" width="400%" height="400%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        <filter id="coreGlow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="11" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        <filter id="boltGlow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        <filter id="beamGlow" x="-50%" y="-200%" width="200%" height="500%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
        <filter id="softGlow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
      </defs>

      <g class="background-dots" opacity=".8">
        <circle class="grid-dot" cx="48" cy="55" r="1"/><circle class="grid-dot" cx="73" cy="93" r="1.2"/><circle class="grid-dot" cx="355" cy="62" r="1"/><circle class="grid-dot" cx="327" cy="108" r="1.2"/><circle class="grid-dot" cx="53" cy="257" r="1.1"/><circle class="grid-dot" cx="354" cy="251" r="1"/><circle class="grid-dot" cx="315" cy="287" r="1.2"/><circle class="grid-dot" cx="100" cy="301" r="1"/>
      </g>

      <g class="energy-only">
        <circle class="pulse-ring r1" cx="210" cy="190" r="78"/><circle class="pulse-ring r2" cx="210" cy="190" r="78"/><circle class="pulse-ring r3" cx="210" cy="190" r="78"/>
        <line class="beam beam-soft" x1="38" y1="190" x2="382" y2="190"/><line class="beam" x1="38" y1="190" x2="382" y2="190"/>
      </g>

      <g class="data-only">
        <path class="stream s1" d="M75 -20V330 M94 -20V330 M112 -20V330 M322 -20V330 M340 -20V330"/>
        <path class="stream s2" d="M130 -20V330 M148 -20V330 M288 -20V330 M306 -20V330"/>
        <path class="stream s3" d="M52 -20V330 M166 -20V330 M252 -20V330 M365 -20V330"/>
        <path class="stream s4" d="M184 -20V330 M235 -20V330"/>
        <rect class="scanline" x="28" y="30" width="364" height="24" rx="12"/>
      </g>

      <g class="circuit-only">
        <path class="trace t1" d="M135 145H91L75 129H33"/><path class="trace t2" d="M135 230H86L68 248H29"/>
        <path class="trace t3" d="M210 105V64L191 45V16"/><path class="trace t4" d="M285 145H328L346 127H390"/>
        <path class="trace t5" d="M285 230H332L350 248H392"/><path class="trace t6" d="M210 270V301"/>
        <path class="tick" d="M58 119h12m-6-6v12 M54 251h12m-6-6v12 M352 117h12m-6-6v12 M354 252h12m-6-6v12"/>
        <circle class="sync-ring" cx="210" cy="190" r="112"/>
      </g>

      <g class="neural-only">
        <circle class="ambient-orbit" cx="210" cy="190" r="138"/>
        <circle class="scan-ring r1" cx="210" cy="190" r="111"/><circle class="scan-ring r2" cx="210" cy="190" r="130"/>
        <g class="scanner"><path class="scanner-wedge" d="M210 190 L210 62 A128 128 0 0 1 315 117 Z"/><line class="scanner-line" x1="210" y1="190" x2="315" y2="117"/></g>
      </g>

      <g class="logo">
        <path class="mesh" d="M210 105L285 145L285 230L210 270L135 230L135 145Z"/>
        <path class="spoke" d="M210 105L210 190M285 145L210 190M285 230L210 190M210 270L210 190M135 230L210 190M135 145L210 190"/>
        <circle class="core-disc" cx="210" cy="190" r="38"/><circle class="core-ring" cx="210" cy="190" r="47"/>
        <g class="node n1" transform="translate(210 105)"><circle class="node-shell" r="14"/><circle class="node-core" r="8"/></g>
        <g class="node n2" transform="translate(285 145)"><circle class="node-shell" r="14"/><circle class="node-core" r="8"/></g>
        <g class="node n3" transform="translate(285 230)"><circle class="node-shell" r="14"/><circle class="node-core" r="8"/></g>
        <g class="node n4" transform="translate(210 270)"><circle class="node-shell" r="14"/><circle class="node-core" r="8"/></g>
        <g class="node n5" transform="translate(135 230)"><circle class="node-shell" r="14"/><circle class="node-core" r="8"/></g>
        <g class="node n6" transform="translate(135 145)"><circle class="node-shell" r="14"/><circle class="node-core" r="8"/></g>
        <path class="bolt" d="M218 119L174 199H207L190 263L250 173H216Z"/>
        <g class="data-packets data-only"><circle class="packet" cx="210" cy="105" r="3"/><circle class="packet" cx="285" cy="230" r="3"/><circle class="packet" cx="135" cy="145" r="3"/></g>
      </g>
    </svg>
  </div>
  <div class="caption"><span class="message"></span><span class="detail"></span></div>
</div>`;

  class PowerClaudeLoader extends HTMLElement {
    static get observedAttributes() { return ['variant', 'message', 'detail', 'size', 'speed']; }
    constructor() { super(); this.attachShadow({mode:'open'}); }
    connectedCallback() { this.render(); }
    attributeChangedCallback() { if (this.isConnected) this.render(); }
    render() {
      const valid = new Set(['energy','data','circuit','neural']);
      const variant = valid.has(this.getAttribute('variant')) ? this.getAttribute('variant') : 'energy';
      const defaults = {
        energy: ['ENERGY PULSE', 'POWERING CLAUDE CORE'],
        data: ['DATA STREAM', 'SYNCHRONIZING CONTEXT'],
        circuit: ['CIRCUIT SYNC', 'LINKING AGENT SYSTEMS'],
        neural: ['NEURAL SCAN', 'INITIALIZING AGENT']
      };
      const size = Math.max(180, Math.min(760, Number(this.getAttribute('size')) || 420));
      const speed = Math.max(.25, Math.min(3, Number(this.getAttribute('speed')) || 1));
      this.shadowRoot.replaceChildren(template.content.cloneNode(true));
      const root = this.shadowRoot;
      root.host.style.setProperty('--pc-size', `${size}px`);
      root.host.style.setProperty('--pc-speed', speed);
      root.querySelector('.screen').classList.add(variant);
      root.querySelector('.message').textContent = this.getAttribute('message') || defaults[variant][0];
      root.querySelector('.detail').textContent = this.getAttribute('detail') || defaults[variant][1];
      ['energy','data','circuit','neural'].forEach(name => {
        root.querySelectorAll(`.${name}-only`).forEach(el => { if (name !== variant) el.style.display = 'none'; });
      });
    }
  }
  if (!customElements.get('power-claude-loader')) customElements.define('power-claude-loader', PowerClaudeLoader);
})();
