// Native keyboard reachability and visible-focus detector shared by browser checks.
export async function keyboardProblems(page) {
  const atStart = await page.evaluate(() => {
    // Blurring a middle control preserves its sequential Tab starting point.
    // Focus the document itself, restoring its original attribute immediately;
    // native Tab then starts before the first control without reloading faults.
    const body = document.body;
    const original = body.getAttribute('tabindex');
    body.setAttribute('tabindex', '-1');
    body.focus({ preventScroll: true });
    const focused = document.activeElement === body;
    if (original === null) body.removeAttribute('tabindex');
    else body.setAttribute('tabindex', original);
    window.scrollTo(0, 0);
    return focused;
  });
  if (!atStart) return ['could not establish document-start keyboard traversal'];
  const total = await page.evaluate(() => {
    const native = 'a[href], area[href], button, input:not([type="hidden"]), select, textarea, summary, iframe, audio[controls], video[controls], [contenteditable=""], [contenteditable="true"]';
    // Closed <details> descendants can retain client rects despite not being painted.
    const visible = (el) => el.getClientRects().length > 0 && el.checkVisibility({ visibilityProperty: true });
    document.querySelectorAll('[data-qa-i]').forEach(el => el.removeAttribute('data-qa-i'));
    const els = [...document.querySelectorAll(`${native}, [tabindex]`)]
      .filter((el) => !el.disabled && !el.closest('[inert]') && visible(el))
      // tabindex="-1" on a non-interactive element (a skip-link target) is a
      // focus target, not a control.
      .filter((el) => el.matches(native) || el.tabIndex >= 0);
    els.forEach((el, i) => el.setAttribute('data-qa-i', String(i)));
    // The look of a control: what a focus indicator can change. Recorded for
    // every control now, while nothing is focused, as its baseline.
    window.__qaLook = (el) => {
      const s = getComputedStyle(el);
      const sides = ['Top', 'Right', 'Bottom', 'Left'];
      return {
        outline: { style: s.outlineStyle, width: parseFloat(s.outlineWidth) || 0, color: s.outlineColor },
        shadow: s.boxShadow,
        border: sides.map((d) => `${s[`border${d}Style`]} ${parseFloat(s[`border${d}Width`]) || 0} ${s[`border${d}Color`]}`),
        background: s.backgroundColor,
      };
    };
    window.__qaBaseline = Object.fromEntries(els.map((el, i) => [String(i), window.__qaLook(el)]));
    return els.length;
  });
  const reached = new Set();
  const noIndicator = [];
  const clipped = [];
  for (let step = 0; step < total * 2 + 5; step += 1) {
    await page.keyboard.press('Tab');
    const f = await page.evaluate(() => {
      const el = document.activeElement;
      if (!el || el === document.body) return null;
      const i = el.getAttribute('data-qa-i');
      // Alpha of a computed color: 0 for transparent or a zero-alpha value.
      const alpha = (c) => {
        if (!c || c === 'transparent') return 0;
        const slash = c.match(/\/\s*([\d.]+)(%?)\s*\)\s*$/);
        if (slash) return parseFloat(slash[1]) / (slash[2] ? 100 : 1);
        const rgba = c.match(/^rgba\([^,]+,[^,]+,[^,]+,\s*([\d.]+)\s*\)$/);
        return rgba ? parseFloat(rgba[1]) : 1;
      };
      const colorsIn = (v) => v.match(/(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch|color)\([^)]*\)|transparent/g) ?? [];
      const now = window.__qaLook(el);
      const was = window.__qaBaseline[i] ?? { outline: { style: 'none', width: 0, color: '' }, shadow: 'none', border: [], background: '' };
      const outlineSeen = (o) => o.style !== 'none' && o.width > 0 && alpha(o.color) > 0;
      const shadowSeen = (v) => v !== 'none' && colorsIn(v).some((c) => alpha(c) > 0);
      const changes = [];
      if (outlineSeen(now.outline) && JSON.stringify(now.outline) !== JSON.stringify(was.outline)) changes.push('outline');
      if (shadowSeen(now.shadow) && now.shadow !== was.shadow) changes.push('box-shadow');
      if (now.border.some((b, k) => b !== was.border[k] && !b.startsWith('none') && parseFloat(b.split(' ')[1]) > 0 && alpha(b.split(' ').slice(2).join(' ')) > 0)) changes.push('border');
      if (now.background !== was.background && alpha(now.background) > 0) changes.push('background');
      const nav = el.closest('.topnav');
      const rect = el.getBoundingClientRect();
      const viewport = nav?.getBoundingClientRect();
      const fullyVisible = !viewport || (rect.left >= viewport.left - 1 && rect.right <= viewport.right + 1);
      return { i, label: `${el.tagName.toLowerCase()}${el.className ? `.${String(el.className).split(' ')[0]}` : ''} "${(el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 30)}"`, indicator: changes.length > 0, fullyVisible };
    });
    if (!f) break;
    if (f.i !== null && reached.has(f.i)) break;
    if (f.i !== null) reached.add(f.i);
    if (!f.indicator) noIndicator.push(f.label);
    if (!f.fullyVisible) clipped.push(f.label);
  }
  const missed = await page.evaluate((got) => [...document.querySelectorAll('[data-qa-i]')]
    .filter((el) => !got.includes(el.getAttribute('data-qa-i')))
    .map((el) => `${el.tagName.toLowerCase()} "${(el.textContent || el.getAttribute('aria-label') || '').trim().slice(0, 30)}"`), [...reached]);
  return [
    ...(total === 0 ? ['no interactive element found'] : []),
    ...missed.map((m) => `not reachable by Tab: ${m}`),
    ...noIndicator.map((m) => `no visible focus indicator: ${m}`),
    ...clipped.map((m) => `focused navigation link clipped: ${m}`),
  ];
}
