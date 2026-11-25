(function(){
  var DATA = JSON.parse(document.getElementById('poses').textContent);
  var CARDS = DATA.cards, GROUPS = DATA.groups;
  var $ = function(id){ return document.getElementById(id); };
  var store = {
    get: function(k, d){ try { var v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch (e) { return d; } },
    set: function(k, v){ try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  };
  var sel = {}, query = '', savedOnly = false, list = [], openIdx = -1;
  var saved = {}; (store.get('pose-saved', []) || []).forEach(function(n){ saved[n] = true; });
  var showThirds = store.get('pose-thirds', false) === true;
  var showTags = store.get('pose-tags', true) !== false;

  // motion: everything below is skipped when the visitor asks for reduced motion
  var EASE = 'cubic-bezier(.2,.7,.2,1)';
  function calm(){ return !document.documentElement.animate || !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches); }
  // run fn once when the animation ends; the timer covers tabs where finish events never arrive
  function done(anim, ms, fn){ var ran = false; function go(){ if (ran) return; ran = true; fn(); } anim.onfinish = go; setTimeout(go, ms + 150); }

  // show or hide a pill by growing it from nothing (or shrinking it back), so its neighbours glide instead of jumping
  function reveal(el, on){
    var cur = el._want === undefined ? !el.hidden : el._want;
    if (cur === on) return;
    el._want = on;
    if (el._rv) { el._rv.cancel(); el._rv = null; }
    if (calm()) { el.hidden = !on; return; }
    el.hidden = false; el.classList.add('rv');
    var cs = getComputedStyle(el), gap = parseFloat(getComputedStyle(el.parentNode).columnGap) || 0;
    var full = { width: el.getBoundingClientRect().width + 'px', minWidth: '0px', paddingLeft: cs.paddingLeft, paddingRight: cs.paddingRight,
                 borderLeftWidth: cs.borderLeftWidth, borderRightWidth: cs.borderRightWidth, marginLeft: cs.marginLeft, opacity: 1, transform: 'none' };
    // the negative margin cancels the flex gap, so a fully shrunk pill takes no room at all
    var small = { width: '0px', minWidth: '0px', paddingLeft: '0px', paddingRight: '0px', borderLeftWidth: '0px', borderRightWidth: '0px',
                  marginLeft: -gap + 'px', opacity: 0, transform: 'scale(.6)' };
    var anim = el._rv = el.animate(on ? [small, full] : [full, small], { duration: 240, easing: EASE, fill: 'forwards' });
    done(anim, 240, function(){
      if (el._rv !== anim) return;
      el._rv = null; el.hidden = !on; el.classList.remove('rv'); anim.cancel();
    });
  }

  function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
  var THIRDS = '<g class="thirds-g" stroke="#fff" stroke-width="1.25" opacity=".8" aria-hidden="true"><line x1="200" y1="0" x2="200" y2="800"/><line x1="400" y1="0" x2="400" y2="800"/><line x1="0" y1="266.7" x2="600" y2="266.7"/><line x1="0" y1="533.3" x2="600" y2="533.3"/></g>';
  function svg(c){ return '<svg viewBox="0 0 600 800" preserveAspectRatio="xMidYMid slice" role="img" aria-label="' + esc('Pose ' + c.n + ', ' + c.t) + '">' + c.a + THIRDS + '</svg>'; }
  function applyThirds(){
    document.body.classList.toggle('thirds', showThirds);
    $('gridToggle').setAttribute('aria-checked', showThirds ? 'true' : 'false');
    $('vGrid').setAttribute('aria-checked', showThirds ? 'true' : 'false');
  }
  function pills(tags){ return tags.slice(0, 3).map(function(t){ return '<span class="mp">' + esc(t) + '</span>'; }).join(''); }
  function applyTags(){
    document.body.classList.toggle('notags', !showTags);
    $('tagToggle').setAttribute('aria-checked', showTags ? 'true' : 'false');
  }

  // filter chips
  var counts = {};
  CARDS.forEach(function(c){ c.g.forEach(function(t){ counts[t] = (counts[t] || 0) + 1; }); });
  // line icons (24px grid, drawn in currentColor); dots use fill="currentColor"
  function icon(cls, d){
    return '<svg class="' + cls + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + d + '</svg>';
  }
  var DOT = ' r="1.3" fill="currentColor" stroke="none"/>';
  var FRAME = '<rect x="5" y="3" width="14" height="18" rx="1.5"/>';
  var GROUP_ICONS = {
    'People': '<circle cx="9" cy="8" r="3"/><path d="M3 20a6 6 0 0 1 12 0"/><path d="M16 5.2a3 3 0 0 1 0 5.6M18 14.5a6 6 0 0 1 3 5.5"/>',
    'Pose': '<circle cx="12" cy="4.5" r="2"/><path d="M12 8v6M7 10.5l5-2 5 2M9 21l3-7 3 7"/>',
    'Shot': '<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
    'Setting': '<path d="M12 21s-6-5.5-6-11a6 6 0 0 1 12 0c0 5.5-6 11-6 11z"/><circle cx="12" cy="10" r="2"/>',
    'Angle': '<path d="M20 12a8 8 0 1 1-2.3-5.7"/><path d="M20 4v4h-4"/>'
  };
  // only where a picture says more than the word: head counts, crop size, facing direction
  var TAG_ICONS = {
    'Solo': '<circle cx="12" cy="8" r="3.2"/><path d="M5.5 20a6.5 6.5 0 0 1 13 0"/>',
    'Partner': '<circle cx="7.5" cy="9" r="2.6"/><path d="M2.5 20a5 5 0 0 1 10 0"/><circle cx="16.5" cy="9" r="2.6"/><path d="M11.5 20a5 5 0 0 1 10 0"/>',
    'Group': '<circle cx="5" cy="10" r="2.1"/><circle cx="12" cy="7.5" r="2.4"/><circle cx="19" cy="10" r="2.1"/><path d="M1.5 20a3.5 3.5 0 0 1 7 0M7 20a5 5 0 0 1 10 0M15.5 20a3.5 3.5 0 0 1 7 0"/>',
    'Wide': FRAME + '<circle cx="12" cy="13.6" r=".9" fill="currentColor" stroke="none"/><path d="M12 15.2v2.8M8 18h8"/>',
    'Full Length': FRAME + '<circle cx="12" cy="7" r="1.7"/><path d="M12 9.5v5.5l-2 3.5M12 15l2 3.5"/>',
    'Three-Quarter': FRAME + '<circle cx="12" cy="8.5" r="2.3"/><path d="M8.5 21v-5a3.5 3.5 0 0 1 7 0v5"/>',
    'Waist Up': FRAME + '<circle cx="12" cy="9.5" r="3"/><path d="M6.5 21a5.5 5.5 0 0 1 11 0"/>',
    'Close-Up': FRAME + '<circle cx="12" cy="11" r="4.6"/><path d="M8 21a4 2.4 0 0 1 8 0"/>',
    'Facing Camera': '<circle cx="12" cy="12" r="8"/><circle cx="9.3" cy="11"' + DOT + '<circle cx="14.7" cy="11"' + DOT,
    'Side-On': '<circle cx="12" cy="12" r="8"/><circle cx="16.4" cy="11"' + DOT + '<path d="M20 12.2l1.6 1.3-1.8.4"/>',
    'Back to Camera': '<circle cx="12" cy="12" r="8"/><path d="M7 8.2a6.5 6.5 0 0 1 10 0"/>'
  };
  $('groups').innerHTML = GROUPS.map(function(g){
    var gi = GROUP_ICONS[g[0]] ? icon('gi', GROUP_ICONS[g[0]]) : '';
    return '<div class="group"><h2>' + gi + esc(g[0]) + '</h2><div class="chips">' + g[1].map(function(t){
      var ci = TAG_ICONS[t] ? icon('ci', TAG_ICONS[t]) : '';
      return '<button class="chip" type="button" aria-pressed="false" data-tag="' + esc(t) + '">' + ci + esc(t) + '<span class="n">' + (counts[t] || 0) + '</span></button>';
    }).join('') + '</div></div>';
  }).join('');
  $('groups').addEventListener('click', function(e){
    var b = e.target.closest('.chip'); if (!b) return;
    var t = b.getAttribute('data-tag'); sel[t] = !sel[t];
    b.setAttribute('aria-pressed', sel[t] ? 'true' : 'false');
    render();
  });
  $('q').addEventListener('input', function(){ query = this.value.trim().toLowerCase(); render(); });
  $('savedOnly').addEventListener('click', function(){ savedOnly = !savedOnly; this.setAttribute('aria-pressed', savedOnly ? 'true' : 'false'); render(); });
  function clearAll(){
    sel = {}; query = ''; savedOnly = false; $('q').value = '';
    $('savedOnly').setAttribute('aria-pressed', 'false');
    Array.prototype.forEach.call(document.querySelectorAll('.chip'), function(b){ b.setAttribute('aria-pressed', 'false'); });
    render();
  }
  // Home: soft reset to the starting view (no reload, so saved poses and the grid setting are untouched)
  function goHome(){
    clearAll();
    setFilterOpen(false);
    window.scrollTo({ top: 0, behavior: calm() ? 'auto' : 'smooth' });
  }
  $('homeBar').addEventListener('click', goHome);
  $('clear').addEventListener('click', clearAll);
  $('clear2').addEventListener('click', clearAll);

  // pills for the applied filters, visible even when the filter panel is closed
  var pillSeen = {}, badgeN = 0;
  function renderActive(){
    var items = [], seen = {};
    GROUPS.forEach(function(g){ g[1].forEach(function(t){ if (sel[t]) items.push({ tag: t, label: t }); }); });
    if (query) items.push({ q: true, label: '“' + $('q').value.trim() + '”' });
    $('active').hidden = !items.length;
    $('active').innerHTML = items.map(function(it){
      seen[it.label] = true;
      return '<button class="apill' + (pillSeen[it.label] ? '' : ' in') + '" type="button" ' + (it.q ? 'data-q="1"' : 'data-tag="' + esc(it.tag) + '"') +
        ' aria-label="' + esc('Remove filter ' + it.label) + '">' + esc(it.label) + '<span class="x" aria-hidden="true">×</span></button>';
    }).join('');
    pillSeen = seen;
    // total applied filters, counted on the Filter poses button
    var badge = $('moreBadge'), total = items.length;
    // the old number stays in place while the badge shrinks away
    if (total > 0) badge.textContent = '+' + total;
    if (total > 0 && badgeN > 0 && total !== badgeN && !calm()) badge.animate([{ transform: 'scale(.8)' }, { transform: 'scale(1.18)', offset: .55 }, { transform: 'none' }], { duration: 280, easing: 'ease-out' });
    badgeN = total;
    reveal(badge, total > 0);
    if (total > 0) badge.setAttribute('aria-label', total + ' applied filter' + (total > 1 ? 's' : ''));
  }
  $('active').addEventListener('click', function(e){
    var b = e.target.closest('.apill'); if (!b) return;
    if (b.hasAttribute('data-q')) { query = ''; $('q').value = ''; }
    else {
      var t = b.getAttribute('data-tag'); sel[t] = false;
      Array.prototype.forEach.call(document.querySelectorAll('.chip'), function(c){ if (c.getAttribute('data-tag') === t) c.setAttribute('aria-pressed', 'false'); });
    }
    render();
    var next = $('active').querySelector('.apill'); (next || $('filterBtn')).focus({ preventScroll: true });
  });

  // does the card pass saved, search and every group's selection except group `skip` (-1 = none skipped)
  function matchesExcept(c, skip){
    if (savedOnly && !saved[c.n]) return false;
    if (query && (c.t + ' ' + c.p + ' ' + c.f + ' ' + c.g.join(' ')).toLowerCase().indexOf(query) < 0) return false;
    return GROUPS.every(function(g, gi){
      if (gi === skip) return true;
      var on = g[1].filter(function(t){ return sel[t]; });
      return !on.length || on.some(function(t){ return c.g.indexOf(t) >= 0; });
    });
  }
  function matches(c){ return matchesExcept(c, -1); }

  // chip counts show how many poses each tag would give with the other filters applied
  var chipN = {};
  Array.prototype.forEach.call(document.querySelectorAll('.chip'), function(b){
    chipN[b.getAttribute('data-tag')] = { chip: b, n: b.querySelector('.n') };
  });
  function updateCounts(){
    GROUPS.forEach(function(g, gi){
      var base = CARDS.filter(function(c){ return matchesExcept(c, gi); });
      g[1].forEach(function(t){
        var k = base.filter(function(c){ return c.g.indexOf(t) >= 0; }).length, r = chipN[t];
        r.n.textContent = k;
        r.chip.classList.toggle('zero', k === 0);
      });
    });
  }

  // thumbnails are drawn only while near the viewport
  var io = ('IntersectionObserver' in window) ? new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      var f = en.target, c = CARDS[+f.getAttribute('data-i')];
      if (en.isIntersecting) { if (!f.firstChild) f.innerHTML = svg(c); }
      else if (f.firstChild) f.innerHTML = '';
    });
  }, { rootMargin: '700px 0px' }) : null;

  // one <li> per pose, built once and reused, so cards can slide to their new place when the filters change
  var HEART = '<span class="saved-mark" title="Saved"><svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/></svg></span>';
  var frames = [], caps = [];
  var items = CARDS.map(function(c, i){
    var li = document.createElement('li'); li._i = i;
    li.innerHTML = '<button class="pose" type="button" data-i="' + i + '" aria-label="' + esc('Open pose ' + c.n + ', ' + c.t) + '">' +
      '<span class="frame" data-i="' + i + '"></span>' +
      '<span class="cap"><span class="num">' + c.n + '</span><span class="name">' + esc(c.t) + '</span></span>' +
      '<span class="meta" aria-hidden="true">' + pills(c.g) + '</span></button>';
    frames[i] = li.querySelector('.frame'); caps[i] = li.querySelector('.cap');
    if (io) io.observe(frames[i]); else frames[i].innerHTML = svg(c);
    return li;
  });
  function syncSaved(i){
    var m = caps[i].querySelector('.saved-mark'), on = !!saved[CARDS[i].n];
    if (on && !m) caps[i].insertAdjacentHTML('beforeend', HEART); else if (!on && m) caps[i].removeChild(m);
  }

  var ready = false, shownKey = null, seq = 0;
  function near(r){ return r.bottom > -80 && r.top < window.innerHeight + 80; }
  function unleave(li){
    li._leaving = 0; if (li._anim) li._anim.cancel(); li._anim = null;
    li.className = ''; li.removeAttribute('style'); li.inert = false;
  }
  // fade a filtered-out card away from where it stood, without it taking a grid cell
  function leave(li, r, g){
    var grid = $('grid'), tok = li._leaving = ++seq;
    li.className = 'leaving'; li.inert = true;
    li.style.cssText = 'left:' + (r.left - g.left) + 'px;top:' + (r.top - g.top) + 'px;width:' + r.width + 'px';
    grid.appendChild(li);
    li._anim = li.animate([{ opacity: 1, transform: 'none' }, { opacity: 0, transform: 'scale(.9)' }], { duration: 200, easing: 'ease-out', fill: 'forwards' });
    done(li._anim, 200, function(){
      if (li._leaving !== tok) return;
      unleave(li); if (li.parentNode === grid) grid.removeChild(li);
    });
  }
  // put the matching cards in the grid; cards that stay slide (FLIP), new ones fade in, removed ones fade out
  function layout(){
    var grid = $('grid'), none = !list.length, motion = ready && !calm(), measure = motion && !grid.hidden;
    var g = measure ? grid.getBoundingClientRect() : null, keep = {}, first = {}, ghosts = [];
    list.forEach(function(i){ keep[i] = true; });
    var old = Array.prototype.slice.call(grid.children);
    // read every position before touching the DOM (a card mid-slide reports where it currently looks)
    if (measure) old.forEach(function(li){
      if (li._leaving) return;
      var r = li.getBoundingClientRect();
      if (keep[li._i]) first[li._i] = r; else if (near(r)) ghosts.push({ li: li, r: r });
    });
    old.forEach(function(li){
      if (li._leaving) { if (keep[li._i]) unleave(li); return; }
      if (li._anim) { li._anim.cancel(); li._anim = null; }
      if (!keep[li._i]) grid.removeChild(li);
    });
    ghosts.forEach(function(o){ leave(o.li, o.r, g); });
    list.forEach(function(i){ grid.appendChild(items[i]); });
    $('empty').hidden = !none; grid.hidden = none;
    if (!motion || none) return;
    var last = list.map(function(i){ return items[i].getBoundingClientRect(); });
    list.forEach(function(i, k){
      var li = items[i], a = first[i], b = last[k];
      if (a) {
        var dx = a.left - b.left, dy = a.top - b.top;
        if ((dx || dy) && (near(a) || near(b))) li._anim = li.animate([{ transform: 'translate(' + dx + 'px,' + dy + 'px)' }, { transform: 'none' }], { duration: 340, easing: EASE });
      } else if (near(b)) {
        li._anim = li.animate([{ opacity: 0, transform: 'scale(.9)' }, { opacity: 1, transform: 'none' }], { duration: 260, easing: EASE });
      }
    });
  }

  function render(){
    list = [];
    CARDS.forEach(function(c, i){ if (matches(c)) list.push(i); syncSaved(i); });
    var filtered = Object.keys(sel).some(function(k){ return sel[k]; }) || query || savedOnly;
    $('count').textContent = filtered ? ('Showing ' + list.length + ' of ' + CARDS.length + ' poses') : (CARDS.length + ' poses');
    reveal($('clear'), !!filtered);
    renderActive();
    updateCounts();
    // an unchanged list leaves the grid alone, which also keeps keyboard focus on the card after the viewer closes
    var key = list.join(',');
    if (key !== shownKey) { layout(); shownKey = key; }
    ready = true;
    if (!list.length) $('emptyText').textContent = savedOnly && !Object.keys(saved).length
      ? 'You haven’t saved any poses yet. Open a pose and choose “Save Pose” to start a shortlist.'
      : 'No poses match these filters. Remove a tag, change the search, or clear everything.';
  }
  $('grid').addEventListener('click', function(e){
    var b = e.target.closest('.pose'); if (!b) return;
    location.hash = 'pose-' + CARDS[+b.getAttribute('data-i')].n;
  });

  // viewer
  var dlg = $('viewer'), closing = false, closeTok = 0, dlgAnim = null, navDir = 0;
  // the small end of the open/close animation: the viewer shrunk so its drawing sits exactly on the pose's thumbnail.
  // With no thumbnail on screen (deep link, or stepped away from it) it is a plain fade and slight scale.
  function heroPair(i){
    var li = items[i], t = null;
    if (li && li.parentNode === $('grid') && !li._leaving) { t = frames[i].getBoundingClientRect(); if (!t.width || !near(t)) t = null; }
    var d = dlg.getBoundingClientRect(), s = $('vShot').getBoundingClientRect();
    if (!t || !s.width) return [{ opacity: 0, transform: 'scale(.96)' }, { opacity: 1, transform: 'none' }];
    var k = t.width / s.width;
    return [{ opacity: 0, transformOrigin: '0 0', transform: 'translate(' + (t.left - d.left - (s.left - d.left) * k) + 'px,' + (t.top - d.top - (s.top - d.top) * k) + 'px) scale(' + k + ')' },
            { opacity: 1, transformOrigin: '0 0', transform: 'none' }];
  }
  function closeViewer(){
    var i = openIdx; openIdx = -1;
    if (calm() || i < 0) { dlg.close(); return; }
    closing = true; var tok = ++closeTok, p = heroPair(i);
    dlg.classList.add('closing');
    dlgAnim = dlg.animate([p[1], { opacity: 1, offset: .55 }, p[0]], { duration: 260, easing: EASE, fill: 'forwards' });
    done(dlgAnim, 260, function(){
      if (tok !== closeTok) return;
      closing = false; dlg.close(); dlg.classList.remove('closing'); dlgAnim.cancel();
    });
  }
  function show(i){
    var c = CARDS[i]; openIdx = i;
    var fresh = !dlg.open || closing, dir = navDir, art = $('vArt'); navDir = 0;
    if (closing) { closeTok++; closing = false; dlg.classList.remove('closing'); if (dlgAnim) dlgAnim.cancel(); }
    Array.prototype.forEach.call($('vShot').querySelectorAll('.art-ghost'), function(n){ n.parentNode.removeChild(n); });
    if (!fresh && dir && !calm() && art.firstChild) {
      // Previous/Next: the old drawing slides out one way while the new one follows it in
      var ghost = document.createElement('div'); ghost.className = 'art-ghost';
      ghost.appendChild(art.firstChild); $('vShot').appendChild(ghost);
      art.innerHTML = svg(c);
      var ga = ghost.animate([{ transform: 'none' }, { transform: 'translateX(' + (-dir * 100) + '%)' }], { duration: 300, easing: EASE, fill: 'forwards' });
      art.animate([{ transform: 'translateX(' + (dir * 100) + '%)' }, { transform: 'none' }], { duration: 300, easing: EASE });
      done(ga, 300, function(){ if (ghost.parentNode) ghost.parentNode.removeChild(ghost); });
      ['vPos', 'vTitle', 'vTags', 'vPose', 'vFrame'].forEach(function(id){
        $(id).animate([{ opacity: 0, transform: 'translateX(' + (dir * 14) + 'px)' }, { opacity: 1, transform: 'none' }], { duration: 260, easing: EASE });
      });
    } else art.innerHTML = svg(c);
    var at = list.indexOf(i);
    $('vPos').textContent = 'Pose ' + c.n + (at >= 0 && list.length < CARDS.length ? ', ' + (at + 1) + ' of ' + list.length + ' shown' : ' of ' + CARDS.length);
    $('vTitle').textContent = c.t;
    $('vTags').innerHTML = c.g.map(function(t){ return '<li>' + esc(t) + '</li>'; }).join('');
    $('vPose').textContent = c.p; $('vFrame').textContent = c.f;
    var on = !!saved[c.n];
    $('vSave').setAttribute('aria-pressed', on ? 'true' : 'false');
    $('vSaveLabel').textContent = on ? 'Saved' : 'Save Pose';
    if (!dlg.open) { if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', ''); }
    // showModal focuses the first control (Save, below the drawing) and scrolls to it, so move focus without scrolling and reset to the top
    try { $('vClose').focus({ preventScroll: true }); } catch (e) {}
    function top(){
      var info = dlg.querySelector('.info'); if (info) info.scrollTop = 0;
      var vw = dlg.querySelector('.viewer'); if (vw) vw.scrollTop = 0;
      dlg.scrollTop = 0;
    }
    top();
    if (window.requestAnimationFrame) requestAnimationFrame(top);
    if (fresh && !calm()) {
      var p = heroPair(i);
      dlgAnim = dlg.animate([p[0], { opacity: 1, offset: .4 }, p[1]], { duration: 320, easing: EASE });
    }
  }
  function step(d){
    var pool = list.length ? list : CARDS.map(function(_, i){ return i; });
    var at = pool.indexOf(openIdx); if (at < 0) at = 0;
    navDir = d;
    location.hash = 'pose-' + CARDS[pool[(at + d + pool.length) % pool.length]].n;
  }
  function route(){
    var m = /^#pose-(\d+)$/.exec(location.hash);
    var idx = -1;
    if (m) CARDS.forEach(function(c, i){ if (c.n === +m[1]) idx = i; });
    if (idx >= 0) show(idx);
    else if (dlg.open && !closing) closeViewer();
  }
  $('vPrev').addEventListener('click', function(){ step(-1); });
  $('vNext').addEventListener('click', function(){ step(1); });
  $('vClose').addEventListener('click', function(){ location.hash = 'all'; });
  dlg.addEventListener('close', function(){ if (/^#pose-/.test(location.hash)) location.hash = 'all'; render(); });
  // Escape goes through the hash too, so the viewer animates shut instead of vanishing
  dlg.addEventListener('cancel', function(e){ e.preventDefault(); location.hash = 'all'; });
  dlg.addEventListener('click', function(e){ if (e.target === dlg) location.hash = 'all'; });
  dlg.addEventListener('keydown', function(e){
    if (e.key === 'ArrowLeft') { e.preventDefault(); step(-1); }
    if (e.key === 'ArrowRight') { e.preventDefault(); step(1); }
  });
  $('vSave').addEventListener('click', function(){
    var c = CARDS[openIdx]; if (!c) return;
    if (saved[c.n]) delete saved[c.n]; else saved[c.n] = true;
    store.set('pose-saved', Object.keys(saved).map(Number));
    var on = !!saved[c.n];
    this.setAttribute('aria-pressed', on ? 'true' : 'false');
    $('vSaveLabel').textContent = on ? 'Saved' : 'Save Pose';
    if (!calm()) {
      // the new label rises into place (drops in when un-saving) and the heart pops when a pose is saved
      $('vSaveLabel').animate([{ opacity: 0, transform: 'translateY(' + (on ? 60 : -60) + '%)' }, { opacity: 1, transform: 'none' }], { duration: 240, easing: EASE });
      if (on) this.querySelector('.sv-live .ico').animate([{ transform: 'scale(.7)' }, { transform: 'scale(1.3)', offset: .55 }, { transform: 'none' }], { duration: 320, easing: 'ease-out' });
    }
  });
  function setThirds(on){ showThirds = on; store.set('pose-thirds', showThirds); applyThirds(); }
  $('vGrid').addEventListener('click', function(){ setThirds(!showThirds); });
  $('gridToggle').addEventListener('click', function(){ setThirds(!showThirds); });
  $('tagToggle').addEventListener('click', function(){ showTags = !showTags; store.set('pose-tags', showTags); applyTags(); });
  var sx = null;
  $('vShot').addEventListener('touchstart', function(e){ sx = e.touches[0].clientX; }, { passive: true });
  $('vShot').addEventListener('touchend', function(e){
    if (sx === null) return;
    var dx = e.changedTouches[0].clientX - sx; sx = null;
    if (Math.abs(dx) > 50) step(dx < 0 ? 1 : -1);
  }, { passive: true });

  function setFilterOpen(on){
    $('filterPanel').hidden = !on;
    $('filterBtn').setAttribute('aria-expanded', on ? 'true' : 'false');
    $('filters').classList.toggle('open', on);
  }
  $('filterBtn').addEventListener('click', function(){ setFilterOpen($('filterPanel').hidden); });
  setFilterOpen(false);
  applyThirds();
  applyTags();
  render();
  window.addEventListener('hashchange', route);
  route();
})();
