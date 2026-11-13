'use strict';
function safeStage() { try { renderStage(); } catch (e) { console.error(e); const s = document.getElementById('mapbox'); if (s && !window.d3) s.innerHTML = `<div class="empty" style="padding-top:30vh">${esc(T.noMap || 'Map unavailable')}</div>`; } }
function init() {
  let l = S.lang;
  if (!l || !I18N[l]) { const n = (navigator.language || 'en').toLowerCase(); l = n.startsWith('zh') ? 'zh' : n.startsWith('ja') ? 'ja' : n.startsWith('ko') ? 'ko' : 'en'; }
  let h = (location.hash || '').slice(1), course = null;
  { const m = /^course-(.+)-(\d+)$/.exec(h); if (m && REGIONS[m[1]]) { h = m[1]; course = `${m[1]}:${m[2]}`; } }   // 여행 가이드 'K링크에서 이 코스 담기'(i261113-01)
  if (course) { if (!S.lang) l = 'ko'; if (!S.trip.kind && !isOv(h)) S.trip.kind = 'kr'; }   // 한국어 여행 가이드에서 왔으면 한국어 · 국내 여행으로 시작
  if ((REGIONS[h] && isOv(h)) || h === 'overseas' || (PBY[h] && isOv(PBY[h].r))) S.trip.kind = 'ov';
  if (REGIONS[h]) { S.seenIntro = true; S.ui.lvl = 'region'; S.ui.r = h; S.ui.scope = isOv(h) ? 'ov' : 'kr'; }
  else if (h === 'overseas') { S.seenIntro = true; S.ui.scope = 'ov'; }
  else if (PBY[h]) { S.seenIntro = true; S.ui.lvl = 'region'; S.ui.r = PBY[h].r; S.ui.scope = isOv(PBY[h].r) ? 'ov' : 'kr'; S.ui.sel = h; }   // 여행 가이드 '명소 안내'에서 바로 이 장소로
  setLang(l); setKindTimes(S.trip, tripKind()); buildShell();
  loadAround(() => { if (S.ui.tab !== 'saved') renderPanel(); });
  renderChrome(); renderPanel(); safeStage();
  if (course) { try { loadCourse(course); } catch (e) { console.error(e); } try { history.replaceState(null, '', '#' + h); } catch (e) {} }
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
