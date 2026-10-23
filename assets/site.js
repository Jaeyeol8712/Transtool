/* 어라운드툴 공통 스크립트 (assets/site.js)
   - 탭 전환 (홈 지역별 맛집)
   - 게시판 목록 필터 (생활툴 · 맛집 허브)
   - 사이트 검색 (search.html)
   스크립트가 없어도 모든 링크와 목록은 그대로 보입니다. */
(function () {
  'use strict';

  /* ---------- 현재 게시판 탭을 보이게 ---------- */
  document.querySelectorAll('.at-board-tabs [aria-current="page"]').forEach(function (a) {
    var ul = a.closest('.at-board-tabs');
    if (ul && ul.scrollWidth > ul.clientWidth) ul.scrollLeft = a.parentNode.offsetLeft - ul.offsetLeft - 16;
  });

  /* ---------- 탭 ---------- */
  document.querySelectorAll('[data-at-tabs]').forEach(function (list) {
    var tabs = list.querySelectorAll('[role="tab"]');
    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        tabs.forEach(function (t) {
          var on = t === tab;
          t.setAttribute('aria-selected', on ? 'true' : 'false');
          t.tabIndex = on ? 0 : -1;
          var pane = document.getElementById(t.getAttribute('aria-controls'));
          if (pane) pane.hidden = !on;
        });
      });
      tab.addEventListener('keydown', function (e) {
        var i = Array.prototype.indexOf.call(tabs, tab);
        if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
          var next = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length];
          next.focus(); next.click(); e.preventDefault();
        }
      });
    });
  });

  /* 주소의 #id 로 해당 탭 열기 (예: /connect.html#travel) */
  var openHash = function () {
    var t = location.hash && document.querySelector('[role="tab"][aria-controls="' + location.hash.slice(1) + '"]');
    if (t) { t.click(); var l = t.closest('[role="tablist"]'); if (l) setTimeout(function () { l.scrollIntoView({ block: 'start' }); }, 0); }
  };
  openHash();
  window.addEventListener('hashchange', openHash);

  /* ---------- 목록 필터 ---------- */
  var norm = function (s) { return (s || '').toLowerCase().replace(/\s+/g, ''); };
  document.querySelectorAll('[data-at-filter]').forEach(function (input) {
    var target = document.getElementById(input.getAttribute('data-at-filter'));
    if (!target) return;
    var rows = target.querySelectorAll('tbody tr:not(.at-gr)');
    var groups = target.querySelectorAll('tbody tr.at-gr');
    var empty = document.getElementById(input.getAttribute('data-at-empty'));
    input.addEventListener('input', function () {
      var q = norm(input.value), shown = 0;
      rows.forEach(function (r) {
        var hit = !q || norm(r.textContent).indexOf(q) > -1 || norm(r.getAttribute('data-k')).indexOf(q) > -1;
        r.hidden = !hit; if (hit) shown++;
      });
      groups.forEach(function (g) {
        var n = g.nextElementSibling, any = false;
        while (n && !n.classList.contains('at-gr')) { if (!n.hidden) any = true; n = n.nextElementSibling; }
        g.hidden = !any;
      });
      if (empty) empty.hidden = shown > 0;
    });
  });

  /* ---------- 사이트 검색 ---------- */
  var box = document.getElementById('at-search-results');
  if (!box) return;
  var params = new URLSearchParams(location.search);
  var q = (params.get('q') || '').trim();
  var field = document.getElementById('at-search-page-q');
  if (field) field.value = q;
  document.querySelectorAll('.at-search input[name="q"]').forEach(function (i) { i.value = q; });
  var info = document.getElementById('at-search-info');
  if (!q) { info.textContent = '찾고 싶은 계산기나 지역, 음식 이름을 입력하세요.'; return; }

  var esc = function (s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  };
  var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
  var mark = function (text) {
    var out = esc(text);
    terms.forEach(function (t) {
      var re = new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
      out = out.replace(re, '<mark>$1</mark>');
    });
    return out;
  };

  fetch('/assets/search-index.json').then(function (r) { return r.json(); }).then(function (items) {
    var scored = items.map(function (it) {
      var title = it.t.toLowerCase(), body = (it.d + ' ' + it.k + ' ' + it.s).toLowerCase(), score = 0;
      terms.forEach(function (t) {
        if (title.indexOf(t) > -1) score += 10;
        else if (body.indexOf(t) > -1) score += 3;
        else score -= 100;
      });
      return { it: it, score: score };
    }).filter(function (x) { return x.score > 0; })
      .sort(function (a, b) { return b.score - a.score; });

    info.textContent = '‘' + q + '’ 검색 결과 ' + scored.length + '건';
    if (!scored.length) {
      box.innerHTML = '<li class="at-empty">일치하는 페이지가 없습니다. 지역명(예: 해운대)이나 계산기 이름(예: 퇴직금)처럼 짧게 입력해 보세요.</li>';
      return;
    }
    box.innerHTML = scored.slice(0, 60).map(function (x) {
      return '<li><span class="u">' + esc(x.it.s) + '</span><br><a href="' + esc(x.it.u) + '">' + mark(x.it.t) +
        '</a><p>' + mark(x.it.d) + '</p></li>';
    }).join('');
  }).catch(function () {
    info.textContent = '검색 색인을 불러오지 못했습니다. 잠시 후 다시 시도하거나 사이트맵을 이용하세요.';
  });
})();
