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

  /* ---------- 방문자 수 (GA4 기준, 매시간 갱신) ---------- */
  var vBoxes = document.querySelectorAll('[data-visitors]');
  if (vBoxes.length && window.fetch) {
    var bust = Math.floor(Date.now() / 600000);
    var show = function (d) {
      if (!d || typeof d.total !== 'number' || d.total <= 0) return;
      vBoxes.forEach(function (box) {
        box.querySelectorAll('[data-v]').forEach(function (el) {
          var v = d[el.getAttribute('data-v')];
          if (typeof v === 'number') el.textContent = v.toLocaleString('ko-KR');
        });
        box.hidden = false;
      });
    };
    fetch('https://raw.githubusercontent.com/Jaeyeol8712/Transtool/main/assets/visitors.json?t=' + bust)
      .then(function (r) { if (!r.ok) throw 0; return r.json(); })
      .catch(function () { return fetch('/assets/visitors.json?t=' + bust).then(function (r) { return r.ok ? r.json() : null; }); })
      .then(show).catch(function () {});
  }

  /* ---------- 휴대폰: 제휴 버튼은 같은 탭에서 열기 ----------
     새 탭으로 열면 일부 안드로이드 브라우저가 '어떤 앱으로 열기' 선택창을 띄우는 경우가 있어
     터치 기기에서는 현재 탭에서 바로 이동합니다. (뒤로 가기로 글에 돌아올 수 있음) */
  if (window.matchMedia && matchMedia('(hover: none) and (pointer: coarse)').matches) {
    document.querySelectorAll('a[rel~="sponsored"][target="_blank"]').forEach(function (a) { a.removeAttribute('target'); });
  }

  /* ---------- 휴대폰: 네이버 제휴 링크는 웹 주소로 바로 ----------
     브랜드 커넥트 연결 페이지는 휴대폰에서 네이버 앱을 열려고 해서 '열기 — 삼성 브라우저 / NAVER'
     선택창이 뜹니다. 연결 페이지의 '웹으로 보기'와 같은 주소(data-web, 제휴 추적 포함)로 같은 탭에서
     바로 이동해 선택창 없이 상품 페이지를 엽니다. PC는 기존 주소 그대로(선택창 없음). */
  var mobile = /android|iphone|ipad|ipod/i.test(navigator.userAgent || '') ||
    (window.matchMedia && matchMedia('(hover: none) and (pointer: coarse)').matches);
  if (mobile) {
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a[data-web]');
      if (!a) return;
      e.preventDefault();
      var w = a.getAttribute('data-web');
      if (window.gtag) gtag('event', 'affiliate_click', { link_url: w, method: 'mobile_web', transport_type: 'beacon' });
      window.location.href = w;
    }, true);
  }

  /* ---------- 유료 광고로 들어온 방문 ----------
     구글 애즈·네이버·카카오 키워드 광고 랜딩은 광고 정책(Better Ads Standards의 팝업·깜빡이는 광고 금지,
     이용자 의도와 무관한 화면 변화 금지)에 맞춰 팝업을 띄우지 않고 버튼 깜빡임도 멈춥니다.
     광고 클릭 주소의 gclid·gad_source·n_media·utm_medium=cpc 등으로 판별하고, 같은 방문(세션) 동안 유지합니다. */
  var adVisit = /[?&](gclid|gbraid|wbraid|gad_source|n_media|n_query|n_ad|napm|kakao_ad|ad)=|[?&]utm_medium=(cpc|ppc|paid|paidsearch|ad|ads|display|keyword)/i.test(location.search);
  try {
    if (adVisit) sessionStorage.setItem('at_ad_visit', '1');
    else adVisit = sessionStorage.getItem('at_ad_visit') === '1';
  } catch (e) {}
  if (adVisit) document.documentElement.classList.add('at-ad-visit');

  /* ---------- 추천 글: 6초 이상 읽으면 '자세히 알아보기' 팝업 ---------- */
  var pop = document.querySelector('[data-at-popup]');
  if (pop && !adVisit) {
    /* 글을 열 때마다(페이지를 볼 때마다) 한 번 뜹니다. 닫으면 그 화면에서는 다시 뜨지 않습니다. */
    var seen = false;
    var openPop = function () {
      if (seen) return; seen = true;
      pop.hidden = false; document.documentElement.classList.add('at-pop-open');
      var go = pop.querySelector('[data-pop-go]'); if (go) go.focus();
      if (window.gtag) gtag('event', 'popup_view', { post: pop.getAttribute('data-at-popup') });
    };
    var closePop = function () { pop.hidden = true; document.documentElement.classList.remove('at-pop-open'); };
    pop.querySelectorAll('[data-pop-close]').forEach(function (b) { b.addEventListener('click', closePop); });
    var goBtn = pop.querySelector('[data-pop-go]');
    if (goBtn) goBtn.addEventListener('click', function () {
      if (window.gtag) gtag('event', 'popup_click', { post: pop.getAttribute('data-at-popup'), transport_type: 'beacon' });
      closePop();
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !pop.hidden) closePop(); });
    /* 탭이 보이는 동안만 6초를 셉니다 (다른 탭에 가 있던 시간은 제외) */
    var shown = 0, last = Date.now();
    var tick = setInterval(function () {
      var now = Date.now();
      if (document.visibilityState === 'visible') shown += now - last;
      last = now;
      if (shown >= 6000) { clearInterval(tick); openPop(); }
    }, 500);
  }


  /* ---------- 목록 5개씩 페이지 나누기 (data-paginate) ---------- */
  document.querySelectorAll('[data-paginate]').forEach(function (list) {
    var per = +list.getAttribute('data-paginate') || 5, items = Array.prototype.slice.call(list.children);
    if (items.length <= per) return;
    var pages = Math.ceil(items.length / per), nav = document.createElement('nav');
    nav.className = 'at-pager'; nav.setAttribute('aria-label', '페이지');
    var show = function (n, scroll) {
      items.forEach(function (li, i) { li.hidden = Math.floor(i / per) !== n; });
      nav.querySelectorAll('button').forEach(function (b, i) {
        if (i === n) b.setAttribute('aria-current', 'page'); else b.removeAttribute('aria-current');
      });
      if (scroll) { var top = list.getBoundingClientRect().top + window.pageYOffset - 120; window.scrollTo({ top: top, behavior: 'smooth' }); }
    };
    for (var i = 0; i < pages; i++) {
      var b = document.createElement('button'); b.type = 'button'; b.textContent = i + 1;
      (function (n) { b.addEventListener('click', function () { show(n, true); }); })(i);
      nav.appendChild(b);
    }
    list.parentNode.insertBefore(nav, list.nextSibling);
    show(0, false);
  });

  /* ---------- 코드 복사 ---------- */
  document.querySelectorAll('[data-copy]').forEach(function (b) {
    b.addEventListener('click', function () {
      var t = document.getElementById(b.getAttribute('data-copy'));
      if (!t) return;
      var done = function () { b.textContent = '복사했습니다'; setTimeout(function () { b.textContent = '코드 복사'; }, 2000); };
      if (navigator.clipboard) navigator.clipboard.writeText(t.value).then(done, function () { t.select(); document.execCommand('copy'); done(); });
      else { t.select(); document.execCommand('copy'); done(); }
    });
  });

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
