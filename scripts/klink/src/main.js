'use strict';
function safeStage() { try { renderStage(); } catch (e) { console.error(e); const s = document.getElementById('mapbox'); if (s && !window.d3) s.innerHTML = `<div class="empty" style="padding-top:30vh">${esc(T.noMap || 'Map unavailable')}</div>`; } }
function init() {
  let l = S.lang;
  if (!l || !I18N[l]) { const n = (navigator.language || 'en').toLowerCase(); l = n.startsWith('zh') ? 'zh' : n.startsWith('ja') ? 'ja' : n.startsWith('ko') ? 'ko' : 'en'; }
  const h = (location.hash || '').slice(1);
  if (REGIONS[h]) { S.seenIntro = true; S.ui.lvl = 'region'; S.ui.r = h; S.ui.scope = isOv(h) ? 'ov' : 'kr'; }
  else if (h === 'overseas') { S.seenIntro = true; S.ui.scope = 'ov'; }
  else if (PBY[h]) { S.seenIntro = true; S.ui.lvl = 'region'; S.ui.r = PBY[h].r; S.ui.scope = isOv(PBY[h].r) ? 'ov' : 'kr'; S.ui.sel = h; }   // 여행 가이드 '명소 안내'에서 바로 이 장소로
  setLang(l); buildShell();
  loadAround(() => { if (S.ui.tab !== 'saved') renderPanel(); });
  renderChrome(); renderPanel(); safeStage();
  if (!S.seenIntro) showIntro();
}
document.addEventListener('click', e => {
  const a = e.target.closest && e.target.closest('a[href]'); if (!a) return;
  let u; try { u = new URL(a.getAttribute('href'), location.href); } catch (x) { return; }
  if (!/(^|\.)aroundtool\.com$/.test(u.hostname) || u.pathname.startsWith('/klink/')) return;
  const f = u.pathname.replace(/^\//, ''), kind = /_calculator\.html$/.test(f) || f === 'tools.html' ? 'calculator' : /^guide[-_]/.test(f) ? 'guide' : /^travel[-.]/.test(f) ? 'travel' : /^season/.test(f) ? 'season' : /^(shop|connect)/.test(f) ? 'recommend' : /\.html$/.test(f) ? 'food' : 'other';
  track('klink_out', { kind });
}, true);
const _renderAll0 = renderAll;
renderAll = function (keep) { renderChrome(); renderPanel(); safeStage(); };
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
