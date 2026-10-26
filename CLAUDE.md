# Agent Guidelines

See [AGENTS.md](AGENTS.md) for full project standards.

## Mandatory Invariant: HTML Google Tag
Whenever creating or editing any `.html` page, you MUST insert the Google tag (`gtag.js`, `G-Z56XV344LR`) immediately following `<head>`:

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-Z56XV344LR"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-Z56XV344LR');
</script>
```

Always verify with `python3 scripts/verify-pages.py`.
