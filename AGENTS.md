# Project Standards & Agent Guidelines

## 1. HTML Page Standards (Mandatory Invariant)

Every HTML page created, modified, or scaffolded in this website MUST include the Google tag (`gtag.js`) **immediately following the `<head>` opening element**.

### Requirements
1. **Placement**: Place directly after `<head>` before any `<meta>`, `<title>`, or stylesheet links.
2. **Cardinality**: Never include more than one Google tag snippet on any page.
3. **Exact Code Snippet**:
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

4. **Verification**:
   Whenever an HTML file is created or edited, run the verification script:
   ```bash
   python3 scripts/verify-pages.py
   ```
   All checks must pass with exit code 0.

---

## 2. Page Structure & Design Conventions
- **Header & Navigation**: Use the standard 5-item navbar (`Governance`, `Architecture`, `Dilemmas`, `Flashcards`, `Reference`) with the vector `[g˙]` logo.
- **Relative Linking**: All user-facing links must point to valid `.html` routes with appropriate relative depth (`../index.html` or `index.html`). Zero raw `.md` links in user-facing UI.
- **Tag Integrity**: Keep all `<details>`, `<article>`, `<section>`, and `<fieldset>` tags strictly balanced and valid.
