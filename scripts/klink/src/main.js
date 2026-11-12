'use strict';
function safeStage() { try { renderStage(); } catch (e) { console.error(e); const s = document.getElementById('mapbox'); if (s && !window.d3) s.innerHTML = `<div class="empty" style="padding-top:30vh">${esc(T.noMap || 'Map unavailable')}</div>`; } }
function init() {
  let l = S.lang;
  if (!l || !I18N[l]) { const n = (navigator.language || 'en').toLowerCase(); l = n.startsWith('zh') ? 'zh' : n.startsWith('ja') ? 'ja' : n.startsWith('ko') ? 'ko' : 'en'; }
  const h = (location.hash || '').slice(1);
  if (REGIONS[h]) { S.seenIntro = true; S.ui.lvl = 'region'; S.ui.r = h; S.ui.scope = isOv(h) ? 'ov' : 'kr'; }
  else if (h === 'overseas') { S.seenIntro = true; S.ui.scope = 'ov'; }
  setLang(l); buildShell();
  loadAround(() => { if (S.ui.tab !== 'saved') renderPanel(); });
  renderChrome(); renderPanel(); safeStage();
  if (!S.seenIntro) showIntro();
}
const _renderAll0 = renderAll;
renderAll = function (keep) { renderChrome(); renderPanel(); safeStage(); };
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
