'use strict';
/* =========================================================
   3D district world (three.js r128 + MapControls): diorama tile of the
   real district shape, landmark buildings at real coordinates, a walking avatar.
   ========================================================= */
const THREE_URL = 'https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js';
const CTRL_URL = 'https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js';
const World3D = (() => {
  let loading = null, W = null;
  function loadScript(src) { return new Promise((res, rej) => { const s = document.createElement('script'); s.src = src; s.async = true; s.onload = res; s.onerror = () => rej(new Error('load ' + src)); document.head.appendChild(s); }); }
  function load() {
    if (window.THREE && THREE.MapControls) return Promise.resolve();
    if (!loading) loading = Promise.race([(async () => { if (!window.THREE) await loadScript(THREE_URL); if (!THREE.MapControls) await loadScript(CTRL_URL); })(),
      new Promise((_, rej) => setTimeout(() => rej(new Error('timeout')), 20000))]).catch(e => { loading = null; throw e; });
    return loading;
  }
  function webglOK() { try { const c = document.createElement('canvas'); return !!(window.WebGLRenderingContext && (c.getContext('webgl') || c.getContext('experimental-webgl'))); } catch (e) { return false; } }
  // deterministic random
  function rng(seed) { let s = 0; for (const ch of seed) s = (s * 31 + ch.charCodeAt(0)) >>> 0; return () => { s ^= s << 13; s >>>= 0; s ^= s >> 17; s ^= s << 5; s >>>= 0; return (s % 100000) / 100000; }; }
  function pip(x, y, ring) { let ins = false; for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) { const xi = ring[i][0], yi = ring[i][1], xj = ring[j][0], yj = ring[j][1]; if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) ins = !ins; } return ins; }
  function inPolys(x, y, polys) { for (const poly of polys) { if (pip(x, y, poly[0])) { let hole = false; for (let k = 1; k < poly.length; k++) if (pip(x, y, poly[k])) { hole = true; break; } if (!hole) return true; } } return false; }

  async function enter(did, container, opts) {
    leave();
    const D = GEO.diorama[did]; if (!D) throw new Error('no diorama');
    if (!webglOK()) throw new Error('nowebgl');
    await load();
    const T3 = THREE, SC = 10, half = D.s / 2 / SC, dist = DISTRICTS[did], r = dist.r, urban = REGIONS[r].sub;
    const lat0 = D.c[0], lng0 = D.c[1], kx = Math.cos(lat0 * Math.PI / 180) * 111320, ky = 110574;
    const toXZ = (lat, lng) => [(lng - lng0) * kx / SC, -(lat - lat0) * ky / SC];
    const sc = s => s.map(poly => poly.map(ring => ring.map(([x, y]) => [x / SC, y / SC])));
    const land = sc(D.land), focus = sc(D.focus), water = sc(D.water);

    const wrap = document.createElement('div'); wrap.className = 'world'; container.appendChild(wrap);
    const labels = document.createElement('div'); labels.className = 'w-labels'; wrap.appendChild(labels);
    const rect = () => container.getBoundingClientRect();
    let renderer;
    try { renderer = new T3.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' }); } catch (e) { wrap.remove(); throw new Error('nowebgl'); }
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.shadowMap.enabled = true; renderer.shadowMap.type = T3.PCFSoftShadowMap;
    wrap.insertBefore(renderer.domElement, labels);
    const scene = new T3.Scene();
    const skyTop = new T3.Color('#DCE7FF');
    scene.fog = new T3.Fog(skyTop, half * 4.5, half * 10);
    const camera = new T3.PerspectiveCamera(38, 1, 1, half * 16);
    const hemi = new T3.HemisphereLight(0xffffff, 0xc3cde6, 0.56); scene.add(hemi);
    const sun = new T3.DirectionalLight(0xffffff, 0.5); sun.position.set(-half * 0.6, half * 1.3, half * 0.7); sun.castShadow = true;
    const sm = window.innerWidth >= 980 ? 2048 : 1536; sun.shadow.mapSize.set(sm, sm);
    Object.assign(sun.shadow.camera, { left: -half * 1.1, right: half * 1.1, top: half * 1.1, bottom: -half * 1.1, near: 1, far: half * 5 }); sun.shadow.bias = -0.0008;
    scene.add(sun); scene.add(sun.target);

    // base slab (sea on top, soil sides)
    const slabH = 16;
    const soil = new T3.MeshLambertMaterial({ color: '#C9B99D' }), soilD = new T3.MeshLambertMaterial({ color: '#B19F80' });
    const seaM = new T3.MeshLambertMaterial({ color: '#8FB8F2' });
    const slab = new T3.Mesh(new T3.BoxGeometry(half * 2, slabH, half * 2), [soil, soil, seaM, soilD, soilD, soil]);
    slab.position.y = -slabH / 2; slab.receiveShadow = true; scene.add(slab);
    const ground = [slab];
    function shapes(polys) { return polys.map(poly => { const sh = new T3.Shape(poly[0].map(([x, y]) => new T3.Vector2(x, y))); for (let k = 1; k < poly.length; k++) sh.holes.push(new T3.Path(poly[k].map(([x, y]) => new T3.Vector2(x, y)))); return sh; }); }
    const landH = 3;
    if (land.length) { const g = new T3.ExtrudeGeometry(shapes(land), { depth: landH, bevelEnabled: false }); g.rotateX(-Math.PI / 2);
      const m = new T3.Mesh(g, new T3.MeshLambertMaterial({ color: urban ? '#E9EDF3' : '#D9EACB' })); m.receiveShadow = true; scene.add(m); ground.push(m); }
    if (focus.length) { const g = new T3.ShapeGeometry(shapes(focus)); g.rotateX(-Math.PI / 2); const m = new T3.Mesh(g, new T3.MeshLambertMaterial({ color: urban ? '#F7F8FC' : '#E7F3DC' })); m.position.y = landH + 0.15; m.receiveShadow = true; scene.add(m); ground.push(m);
      for (const poly of focus) { const pts = poly[0].map(([x, y]) => new T3.Vector3(x, landH + 0.4, -y)); const lg = new T3.BufferGeometry().setFromPoints(pts); scene.add(new T3.Line(lg, new T3.LineBasicMaterial({ color: '#2443E8', transparent: true, opacity: .55 }))); } }
    if (water.length) { const g = new T3.ShapeGeometry(shapes(water)); g.rotateX(-Math.PI / 2); const m = new T3.Mesh(g, new T3.MeshLambertMaterial({ color: '#8FB8F2' })); m.position.y = landH + 0.25; scene.add(m); }

    // places & landmark positions
    const plist = dist.ids.map(id => PBY[id]);
    const LS = clamp(half / 170, 1, 2.6), edge = 20 * LS;
    const marks = plist.map(p => { const [x, z] = toXZ(p.lat, p.lng); return { p, x: clamp(x, -half + edge, half - edge), z: clamp(z, -half + edge, half - edge) }; });
    // keep landmarks from sitting on top of each other
    for (let it = 0; it < 60; it++) for (let i = 0; i < marks.length; i++) for (let j = i + 1; j < marks.length; j++) {
      const A = marks[i], B = marks[j]; let dx = B.x - A.x, dz = B.z - A.z, d = Math.hypot(dx, dz); const need = 40 * LS;
      if (d >= need) continue; if (d < .01) { dx = 1; dz = .3; d = 1.05; }
      const m = (need - d) / 2; A.x = clamp(A.x - dx / d * m, -half + edge, half - edge); A.z = clamp(A.z - dz / d * m, -half + edge, half - edge);
      B.x = clamp(B.x + dx / d * m, -half + edge, half - edge); B.z = clamp(B.z + dz / d * m, -half + edge, half - edge);
    }
    // city blocks + trees
    const rnd = rng(did);
    const step = Math.max(8, (half * 2) / 44);
    const bpos = [], tpos = [];
    for (let x = -half + step / 2; x < half; x += step) for (let z = -half + step / 2; z < half; z += step) {
      const gi = Math.round((x + half) / step), gj = Math.round((z + half) / step);
      if (urban && (gi % 5 === 0 || gj % 6 === 0)) continue;
      const jx = x + (rnd() - .5) * step * .3, jz = z + (rnd() - .5) * step * .3;
      if (!inPolys(jx, -jz, land) || inPolys(jx, -jz, water)) continue;
      if (marks.some(m => Math.hypot(m.x - jx, m.z - jz) < 20 * LS)) continue;
      const inF = focus.length && inPolys(jx, -jz, focus);
      const dens = urban ? (inF ? .7 : .4) : (inF ? .12 : .06);
      const v = rnd();
      if (v < dens) bpos.push([jx, jz, inF]); else if (v < dens + (urban ? .07 : .3)) tpos.push([jx, jz]);
    }
    const bm = new T3.InstancedMesh(new T3.BoxGeometry(1, 1, 1), new T3.MeshLambertMaterial({ color: '#ffffff' }), bpos.length || 1);
    const pal = urban ? ['#FFFFFF', '#F4F6FA', '#E6EBF5', '#DBE3F1', '#FBF1E2', '#E6F0EA', '#F2E8F1', '#EEF1F6'] : ['#FFFFFF', '#FBF1E2', '#F3E7D6', '#F4F4EF'];
    const dm = new T3.Object3D(), col = new T3.Color();
    bpos.forEach(([x, z, inF], i) => { const w = step * (urban ? .56 + rnd() * .22 : .3 + rnd() * .12), d = step * (urban ? .56 + rnd() * .22 : .3 + rnd() * .12);
      const h = urban ? step * (inF ? .3 + Math.pow(rnd(), 2.4) * 1.25 : .22 + Math.pow(rnd(), 3) * .7) : step * (.22 + rnd() * .12);
      dm.position.set(x, landH + h / 2, z); dm.scale.set(w, h, d); dm.rotation.y = (rnd() - .5) * .08; dm.updateMatrix(); bm.setMatrixAt(i, dm.matrix);
      bm.setColorAt(i, col.set(pal[Math.floor(rnd() * pal.length)])); });
    bm.castShadow = true; bm.receiveShadow = true; if (bm.instanceColor) bm.instanceColor.needsUpdate = true; scene.add(bm);
    const tm = new T3.InstancedMesh(new T3.ConeGeometry(1, 1, 6), new T3.MeshLambertMaterial({ color: '#ffffff' }), tpos.length || 1);
    const greens = ['#5DB37E', '#4AA56D', '#76C08E', '#3F9963'];
    tpos.forEach(([x, z], i) => { const s = step * (.2 + rnd() * .12), h = s * 2.3; dm.position.set(x, landH + h / 2, z); dm.scale.set(s, h, s); dm.rotation.y = 0; dm.updateMatrix(); tm.setMatrixAt(i, dm.matrix); tm.setColorAt(i, col.set(greens[Math.floor(rnd() * greens.length)])); });
    tm.castShadow = true; if (tm.instanceColor) tm.instanceColor.needsUpdate = true; scene.add(tm);

    // landmark models
    const M = c => new T3.MeshLambertMaterial({ color: c });
    const box = (w, h, d, c) => { const m = new T3.Mesh(new T3.BoxGeometry(w, h, d), M(c)); m.castShadow = true; m.receiveShadow = true; return m; };
    const cyl = (rt, rb, h, c, seg = 16) => { const m = new T3.Mesh(new T3.CylinderGeometry(rt, rb, h, seg), M(c)); m.castShadow = true; return m; };
    const animated = [];
    function model(p) {
      const g = new T3.Group(), c = CATS[p.c].col; let top = 10;
      const add = (m, x, y, z) => { m.position.set(x, y, z); g.add(m); return m; };
      switch (p.c) {
        case 'palace': { add(box(22, 2.4, 16, '#D9D0C2'), 0, 1.2, 0); add(box(16, 6, 10, '#F3E8D8'), 0, 5.4, 0);
          for (const dx of [-6.5, -2.2, 2.2, 6.5]) add(box(1, 6, 1, '#B23A2B'), dx, 5.4, 5.2);
          const roof = new T3.Mesh(new T3.ConeGeometry(14, 7, 4), M('#3F4A5E')); roof.rotation.y = Math.PI / 4; roof.scale.set(1.25, 1, .85); roof.castShadow = true; add(roof, 0, 11.9, 0);
          add(box(13, .8, 1.2, '#2E3646'), 0, 15.2, 0); top = 17; break; }
        case 'food': { add(box(12, 8, 10, '#FFF2E2'), 0, 4, 0); const aw = box(12.6, .6, 4, c); aw.rotation.x = .45; add(aw, 0, 6.6, 6.2);
          add(box(6, 2.4, .6, '#ffffff'), 0, 9.6, 3); add(box(12.4, .8, 10.4, '#E9DCC9'), 0, 8.4, 0); top = 12; break; }
        case 'skin': { add(box(13, 1.2, 13, '#E9EDF5'), 0, .6, 0); add(box(9, 22, 9, '#FFFFFF'), 0, 12, 0);
          add(box(1.2, 5, .4, c), 0, 18, 4.7); add(box(5, 1.2, .4, c), 0, 18, 4.7); top = 25; break; }
        case 'shop': { add(box(12, 26, 12, '#7ED6B4'), 0, 13, 0); add(box(8, 6, 8, '#A9E7CF'), 0, 29, 0); for (let y = 5; y < 26; y += 5) add(box(12.2, .5, 12.2, '#5FBF99'), 0, y, 0); top = 34; break; }
        case 'cafe': { add(box(10, 7, 10, '#DDB88E'), 0, 3.5, 0); add(box(11, 1, 11, '#8C6A4B'), 0, 7.5, 0); add(cyl(2.2, 1.8, 3, '#FFFFFF'), 0, 9.5, 0); const hd = new T3.Mesh(new T3.TorusGeometry(1, .35, 8, 16), M('#FFFFFF')); hd.position.set(2.4, 9.5, 0); g.add(hd); top = 13; break; }
        case 'kpop': { add(box(13, 10, 13, '#CDB7EE'), 0, 5, 0); add(box(13.4, 1, 13.4, c), 0, 10.4, 0); const st = new T3.Mesh(new T3.OctahedronGeometry(3.6), new T3.MeshLambertMaterial({ color: '#FFD166', emissive: '#7A5A00' })); st.castShadow = true; add(st, 0, 17, 0); animated.push(o => { st.rotation.y = o * 1.2; st.position.y = 17 + Math.sin(o * 2) * .8; }); top = 22; break; }
        case 'night': { add(cyl(3.5, 4.5, 3, '#D9DFF5'), 0, 1.5, 0); add(cyl(1.1, 1.6, 30, '#F0F3FF', 10), 0, 18, 0); add(cyl(4, 4, 2, '#3B3FB6'), 0, 31, 0); add(cyl(.4, .4, 7, '#F0F3FF', 6), 0, 35.5, 0);
          const glow = new T3.Mesh(new T3.SphereGeometry(1.4, 12, 12), new T3.MeshBasicMaterial({ color: '#FFD66B' })); add(glow, 0, 39.5, 0); top = 42; break; }
        case 'fun': { const wheel = new T3.Group(); const rim = new T3.Mesh(new T3.TorusGeometry(9, .6, 8, 40), M('#FFB703')); wheel.add(rim);
          for (let k = 0; k < 8; k++) { const sp = box(.4, 18, .4, '#FFFFFF'); sp.rotation.z = k * Math.PI / 8; wheel.add(sp); const cab = box(2, 2, 2, ['#FF4F7B', '#2443E8', '#0E9F8F', '#8E5BD8'][k % 4]); const a = k * Math.PI / 4; cab.position.set(Math.cos(a) * 9, Math.sin(a) * 9, 0); wheel.add(cab); }
          wheel.position.set(0, 12, 0); g.add(wheel); animated.push(o => { wheel.rotation.z = o * .25; });
          const l1 = box(.8, 13, .8, '#9AA3B8'); l1.rotation.z = .35; add(l1, -2.2, 6, 1.5); const l2 = box(.8, 13, .8, '#9AA3B8'); l2.rotation.z = -.35; add(l2, 2.2, 6, 1.5); top = 24; break; }
        case 'nature': default: {
          if (/halla|seongsan|taejongdae|yonggung|hyangil|seokguram/.test(p.id)) { const mt = new T3.Mesh(new T3.ConeGeometry(18, 22, 9), M('#5EA97A')); mt.castShadow = true; mt.receiveShadow = true; add(mt, 0, 11, 0);
            const cap = new T3.Mesh(new T3.ConeGeometry(6.2, 7.5, 9), M('#F1F5F2')); add(cap, 0, 18.4, 0); top = 25; }
          else if (/haeundae|hyeopjae|gyeongpo|gwangan|anmok|seopji/.test(p.id)) { add(cyl(14, 14, .6, '#F2E2BC', 24), 0, .3, 0);
            for (const [dx, dz, cc] of [[-5, 2, '#FF4F7B'], [4, -3, '#2443E8'], [5, 5, '#FFB703']]) { add(cyl(.3, .3, 6, '#FFFFFF', 6), dx, 3, dz); const um = new T3.Mesh(new T3.ConeGeometry(3.4, 1.6, 10), M(cc)); add(um, dx, 6.4, dz); } top = 10; }
          else { for (const [dx, dz, s] of [[0, 0, 1.4], [-6, 3, 1], [5, 4, 1.1], [3, -5, .9], [-4, -4, 1.05]]) { add(cyl(.5 * s, .6 * s, 3 * s, '#8A6A4A', 6), dx, 1.5 * s, dz); const cn = new T3.Mesh(new T3.ConeGeometry(3.6 * s, 9 * s, 7), M('#4AA56D')); cn.castShadow = true; add(cn, dx, 7.4 * s, dz); } top = 15; }
        }
      }
      const base = new T3.Mesh(new T3.CylinderGeometry(15, 15, .5, 32), new T3.MeshLambertMaterial({ color: c, transparent: true, opacity: .22 })); base.position.y = .3; g.add(base);
      const ring = new T3.Mesh(new T3.RingGeometry(15.5, 17.5, 40), new T3.MeshBasicMaterial({ color: '#2443E8', transparent: true, opacity: 0, side: T3.DoubleSide })); ring.rotation.x = -Math.PI / 2; ring.position.y = .7; g.add(ring);
      g.userData = { id: p.id, top, ring };
      return g;
    }
    const groups = [];
    for (const m of marks) { const g = model(m.p); g.scale.setScalar(LS); g.userData.top *= LS; g.position.set(m.x, landH, m.z); g.traverse(o => { o.userData.pid = m.p.id; }); scene.add(g); groups.push(g); m.g = g; }
    // avatar
    const av = new T3.Group();
    const body = new T3.Mesh(new T3.CylinderGeometry(1.25, 1.4, 3.4, 12), M('#2443E8')); body.position.y = 3.6; body.castShadow = true; av.add(body);
    const head = new T3.Mesh(new T3.SphereGeometry(1.25, 16, 12), M('#FFD9B8')); head.position.y = 6.3; head.castShadow = true; av.add(head);
    const hair = new T3.Mesh(new T3.SphereGeometry(1.32, 16, 12, 0, Math.PI * 2, 0, Math.PI / 2), M('#1E2333')); hair.position.y = 6.45; av.add(hair);
    const legL = box(.7, 2, .8, '#141A2E'), legR = box(.7, 2, .8, '#141A2E'); legL.geometry.translate(0, -1, 0); legR.geometry.translate(0, -1, 0); legL.position.set(-.55, 2, 0); legR.position.set(.55, 2, 0); av.add(legL); av.add(legR);
    const bag = box(1.6, 1.8, .7, '#FF4F7B'); bag.position.set(0, 3.8, -1.3); av.add(bag);
    av.scale.setScalar(1.5 * LS);
    const startM = marks[0] || { x: 0, z: 0 };
    av.position.set(startM.x + 20 * LS, landH, startM.z + 20 * LS); scene.add(av);
    let walkTo = null;

    // controls
    const controls = new T3.MapControls(camera, renderer.domElement);
    controls.enableDamping = true; controls.dampingFactor = .09; controls.screenSpacePanning = false;
    controls.minDistance = 60 * LS; controls.maxDistance = half * 3.4; controls.maxPolarAngle = 1.18; controls.minPolarAngle = .32;
    const cx0 = marks.length ? marks.reduce((a, m) => a + m.x, 0) / marks.length : 0, cz0 = marks.length ? marks.reduce((a, m) => a + m.z, 0) / marks.length : 0;
    const spread = marks.length ? Math.max(60, ...marks.map(m => Math.hypot(m.x - cx0, m.z - cz0))) : half * .5;
    const homeDist = clamp(spread * 2.3 + 150 * LS, 190 * LS, half * 3);
    function home(anim) { const tgt = new T3.Vector3(cx0, landH, cz0), pos = new T3.Vector3(cx0 + homeDist * .32, homeDist * .82, cz0 + homeDist * .78); if (anim) fly(tgt, pos); else { controls.target.copy(tgt); camera.position.copy(pos); } }
    home(false);
    let flyA = null;
    function fly(tgt, pos) { flyA = { t0: performance.now(), from: controls.target.clone(), to: tgt, pf: camera.position.clone(), pt: pos }; }
    controls.addEventListener('change', () => { controls.target.x = clamp(controls.target.x, -half, half); controls.target.z = clamp(controls.target.z, -half, half); controls.target.y = landH; });

    // labels
    const labs = marks.map(m => { const el = document.createElement('button'); el.className = 'w-label'; el.type = 'button';
      el.innerHTML = `<span class="cicon" style="background:${CATS[m.p.c].col}">${catIcon(m.p.c)}</span><span class="t">${esc(pn(m.p.id))}</span><span class="hrt"${isSaved(m.p.id) ? '' : ' hidden'}>♥</span>`;
      el.addEventListener('click', ev => { ev.stopPropagation(); select(m.p.id, true); }); labels.appendChild(el); return { m, el, w: 0, h: 0 }; });
    let sel = null;
    function select(id, notify) {
      sel = id; const m = marks.find(x => x.p.id === id);
      labs.forEach(L => L.el.classList.toggle('sel', L.m.p.id === id));
      if (m) { walkTo = new T3.Vector3(m.x + 19 * LS, landH, m.z + 19 * LS);
        const d = clamp(camera.position.distanceTo(controls.target), 150 * LS, 230 * LS), dir = camera.position.clone().sub(controls.target).normalize();
        const tgt = new T3.Vector3(m.x, landH, m.z); fly(tgt, tgt.clone().add(dir.multiplyScalar(d))); }
      if (notify && opts.onSelect) opts.onSelect(id);
    }
    function refreshSaved() { labs.forEach(L => { const h = L.el.querySelector('.hrt'); if (h) h.hidden = !isSaved(L.m.p.id); }); }
    // picking
    const ray = new T3.Raycaster(), ndc = new T3.Vector2(); let down = null;
    renderer.domElement.addEventListener('pointerdown', e => { down = { x: e.clientX, y: e.clientY, t: performance.now() }; if (opts.onInteract) opts.onInteract(); });
    renderer.domElement.addEventListener('pointerup', e => {
      if (!down || Math.hypot(e.clientX - down.x, e.clientY - down.y) > 6 || performance.now() - down.t > 500) { down = null; return; } down = null;
      const rc = renderer.domElement.getBoundingClientRect(); ndc.set(((e.clientX - rc.left) / rc.width) * 2 - 1, -((e.clientY - rc.top) / rc.height) * 2 + 1);
      ray.setFromCamera(ndc, camera);
      const hit = ray.intersectObjects(groups, true)[0];
      if (hit && hit.object.userData.pid) { select(hit.object.userData.pid, true); return; }
      const g2 = ray.intersectObjects(ground, false)[0]; if (g2) { walkTo = new T3.Vector3(clamp(g2.point.x, -half + 4, half - 4), landH, clamp(g2.point.z, -half + 4, half - 4)); }
    });
    // resize
    function resize() { const rc = rect(); const w = Math.max(100, rc.width), h = Math.max(100, rc.height); renderer.setSize(w, h, false); renderer.domElement.style.width = w + 'px'; renderer.domElement.style.height = h + 'px'; camera.aspect = w / h; camera.updateProjectionMatrix(); }
    const ro = new ResizeObserver(resize); ro.observe(container); resize();
    // loop
    const clock = new T3.Clock(); let raf = 0, alive = true; const v3 = new T3.Vector3();
    function frame() {
      if (!alive) return; raf = requestAnimationFrame(frame);
      const dt = Math.min(clock.getDelta(), .05), et = clock.elapsedTime;
      if (flyA) { const k = clamp((performance.now() - flyA.t0) / 700, 0, 1), e2 = 1 - Math.pow(1 - k, 3);
        controls.target.lerpVectors(flyA.from, flyA.to, e2); camera.position.lerpVectors(flyA.pf, flyA.pt, e2); if (k >= 1) flyA = null; }
      controls.update();
      if (walkTo) { const d = walkTo.clone().sub(av.position); d.y = 0; const L = d.length();
        if (L < 1.2 * LS) { walkTo = null; legL.rotation.x = legR.rotation.x = 0; }
        else { const sp = Math.min(L, 60 * LS * dt); d.normalize(); av.position.addScaledVector(d, sp); av.rotation.y = Math.atan2(d.x, d.z);
          const sw = Math.sin(et * 14) * .7; legL.rotation.x = sw; legR.rotation.x = -sw; av.position.y = landH + Math.abs(Math.sin(et * 14)) * .5 * LS; } }
      else { av.position.y = landH + Math.sin(et * 2.2) * .12; }
      animated.forEach(f => f(et));
      groups.forEach(g => { const rg = g.userData.ring, isSel = g.userData.id === sel, sv2 = isSaved(g.userData.id);
        rg.material.opacity = isSel ? .55 + Math.sin(et * 4) * .25 : sv2 ? .6 : 0; rg.material.color.set(isSel ? '#2443E8' : '#FF4F7B'); });
      renderer.render(scene, camera);
      // labels
      const rc = rect(), placed = [];
      const pri = L => (L.m.p.id === sel ? 3 : isSaved(L.m.p.id) ? 2 : 1);
      const items = labs.map(L => { v3.set(L.m.x, landH + L.m.g.userData.top + 4, L.m.z).project(camera); return { L, x: (v3.x + 1) / 2 * rc.width, y: (1 - v3.y) / 2 * rc.height, z: v3.z }; })
        .sort((a, b) => pri(b.L) - pri(a.L) || a.z - b.z);
      for (const it of items) { const L = it.L; if (!L.w) { L.w = L.el.offsetWidth; L.h = L.el.offsetHeight; }
        let ok = it.z < 1 && it.x > -20 && it.x < rc.width + 20 && it.y > 0 && it.y < rc.height;
        const rx = it.x - L.w / 2, ry = it.y - L.h;
        if (ok) for (const R of placed) if (rx < R.x + R.w + 3 && rx + L.w + 3 > R.x && ry < R.y + R.h + 2 && ry + L.h + 2 > R.y) { ok = false; break; }
        L.el.classList.toggle('hide', !ok); if (ok) { placed.push({ x: rx, y: ry, w: L.w, h: L.h }); L.el.style.transform = `translate(${rx}px,${ry}px)`; } }
    }
    frame();
    W = { did, alive: () => alive, select, refreshSaved, home: () => home(true), resize,
      zoomBy(f) { const dir = camera.position.clone().sub(controls.target); dir.multiplyScalar(1 / f); const L = clamp(dir.length(), controls.minDistance, controls.maxDistance); dir.setLength(L); fly(controls.target.clone(), controls.target.clone().add(dir)); },
      destroy() { alive = false; cancelAnimationFrame(raf); ro.disconnect(); controls.dispose(); scene.traverse(o => { if (o.geometry) o.geometry.dispose(); if (o.material) [].concat(o.material).forEach(mm => mm.dispose()); }); renderer.dispose(); try { renderer.forceContextLoss(); } catch (e) {} wrap.remove(); } };
    return W;
  }
  function leave() { if (W) { W.destroy(); W = null; } }
  return { enter, leave, get cur() { return W; }, load, webglOK };
})();
