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
  var showThirds = store.get('pose-thirds', true) !== false;

  function esc(s){ return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
  var THIRDS = '<g class="thirds-g" stroke="#fff" stroke-width="1.25" opacity=".8" aria-hidden="true"><line x1="200" y1="0" x2="200" y2="800"/><line x1="400" y1="0" x2="400" y2="800"/><line x1="0" y1="266.7" x2="600" y2="266.7"/><line x1="0" y1="533.3" x2="600" y2="533.3"/></g>';
  function svg(c){ return '<svg viewBox="0 0 600 800" preserveAspectRatio="xMidYMid slice" role="img" aria-label="' + esc('Pose ' + c.n + ', ' + c.t) + '">' + c.a + THIRDS + '</svg>'; }
  function applyThirds(){
    document.body.classList.toggle('thirds', showThirds);
    $('gridToggle').setAttribute('aria-checked', showThirds ? 'true' : 'false');
    $('vGrid').setAttribute('aria-checked', showThirds ? 'true' : 'false');
  }
  function lower(tags){ return tags.slice(0, 3).map(function(t, i){ return i ? t.toLowerCase() : t; }).join(', '); }

  // filter chips
  var counts = {};
  CARDS.forEach(function(c){ c.g.forEach(function(t){ counts[t] = (counts[t] || 0) + 1; }); });
  $('groups').innerHTML = GROUPS.map(function(g){
    return '<div class="group"><h2>' + esc(g[0]) + '</h2><div class="chips">' + g[1].map(function(t){
      return '<button class="chip" type="button" aria-pressed="false" data-tag="' + esc(t) + '">' + esc(t) + '<span class="n">' + (counts[t] || 0) + '</span></button>';
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
  $('clear').addEventListener('click', clearAll);
  $('clear2').addEventListener('click', clearAll);

  // pills for the applied filters, visible even when the filter panel is closed
  var MAX_PILLS = 3;
  function renderActive(){
    var items = [];
    GROUPS.forEach(function(g){ g[1].forEach(function(t){ if (sel[t]) items.push({ tag: t, label: t }); }); });
    if (query) items.push({ q: true, label: '“' + $('q').value.trim() + '”' });
    var shown = items.slice(0, MAX_PILLS), rest = items.length - shown.length;
    $('active').hidden = !items.length;
    $('active').innerHTML = shown.map(function(it){
      return '<button class="apill" type="button" ' + (it.q ? 'data-q="1"' : 'data-tag="' + esc(it.tag) + '"') +
        ' aria-label="' + esc('Remove filter ' + it.label) + '">' + esc(it.label) + '<span class="x" aria-hidden="true">×</span></button>';
    }).join('');
    // total applied filters, counted on the Filter poses button
    var badge = $('moreBadge'), total = items.length;
    badge.hidden = total <= 0;
    badge.textContent = total > 0 ? '+' + total : '';
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
    var next = $('active').querySelector('.apill'); (next || $('filterBtn')).focus();
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

  function render(){
    if (io) io.disconnect();
    list = [];
    CARDS.forEach(function(c, i){ if (matches(c)) list.push(i); });
    var filtered = Object.keys(sel).some(function(k){ return sel[k]; }) || query || savedOnly;
    $('count').textContent = filtered ? ('Showing ' + list.length + ' of ' + CARDS.length + ' poses') : (CARDS.length + ' poses');
    $('clear').hidden = !filtered;
    renderActive();
    updateCounts();
    $('grid').innerHTML = list.map(function(i){
      var c = CARDS[i];
      return '<li><button class="pose" type="button" data-i="' + i + '" aria-label="' + esc('Open pose ' + c.n + ', ' + c.t) + '">' +
        '<span class="frame" data-i="' + i + '"></span>' +
        '<span class="cap"><span class="num">' + c.n + '</span><span class="name">' + esc(c.t) + '</span>' +
        (saved[c.n] ? '<span class="saved-mark" title="Saved"><svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/></svg></span>' : '') + '</span>' +
        '<span class="meta">' + esc(lower(c.g)) + '</span></button></li>';
    }).join('');
    var frames = document.querySelectorAll('.frame');
    Array.prototype.forEach.call(frames, function(f){ if (io) io.observe(f); else f.innerHTML = svg(CARDS[+f.getAttribute('data-i')]); });
    var none = !list.length;
    $('empty').hidden = !none; $('grid').hidden = none;
    if (none) $('emptyText').textContent = savedOnly && !Object.keys(saved).length
      ? 'You haven’t saved any poses yet. Open a pose and choose “Save pose” to start a shortlist.'
      : 'No poses match these filters. Remove a tag, change the search, or clear everything.';
  }
  $('grid').addEventListener('click', function(e){
    var b = e.target.closest('.pose'); if (!b) return;
    location.hash = 'pose-' + CARDS[+b.getAttribute('data-i')].n;
  });

  // viewer
  var dlg = $('viewer');
  function show(i){
    var c = CARDS[i]; openIdx = i;
    $('vArt').innerHTML = svg(c);
    var at = list.indexOf(i);
    $('vPos').textContent = 'Pose ' + c.n + (at >= 0 && list.length < CARDS.length ? ', ' + (at + 1) + ' of ' + list.length + ' shown' : ' of ' + CARDS.length);
    $('vTitle').textContent = c.t;
    $('vTags').innerHTML = c.g.map(function(t){ return '<li>' + esc(t) + '</li>'; }).join('');
    $('vPose').textContent = c.p; $('vFrame').textContent = c.f;
    var on = !!saved[c.n];
    $('vSave').setAttribute('aria-pressed', on ? 'true' : 'false');
    $('vSaveLabel').textContent = on ? 'Saved' : 'Save pose';
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
  }
  function step(d){
    var pool = list.length ? list : CARDS.map(function(_, i){ return i; });
    var at = pool.indexOf(openIdx); if (at < 0) at = 0;
    location.hash = 'pose-' + CARDS[pool[(at + d + pool.length) % pool.length]].n;
  }
  function route(){
    var m = /^#pose-(\d+)$/.exec(location.hash);
    var idx = -1;
    if (m) CARDS.forEach(function(c, i){ if (c.n === +m[1]) idx = i; });
    if (idx >= 0) show(idx);
    else if (dlg.open) { openIdx = -1; dlg.close(); }
  }
  $('vPrev').addEventListener('click', function(){ step(-1); });
  $('vNext').addEventListener('click', function(){ step(1); });
  $('vClose').addEventListener('click', function(){ location.hash = 'all'; });
  dlg.addEventListener('close', function(){ if (/^#pose-/.test(location.hash)) location.hash = 'all'; render(); });
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
    $('vSaveLabel').textContent = on ? 'Saved' : 'Save pose';
  });
  function setThirds(on){ showThirds = on; store.set('pose-thirds', showThirds); applyThirds(); }
  $('vGrid').addEventListener('click', function(){ setThirds(!showThirds); });
  $('gridToggle').addEventListener('click', function(){ setThirds(!showThirds); });
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
  render();
  window.addEventListener('hashchange', route);
  route();
})();
