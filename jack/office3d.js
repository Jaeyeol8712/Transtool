/* 어라운드툴 오피스 3D 장면 (Three.js r149 UMD 필요: window.THREE)
   createOffice(container, {rooms, onPick}) → API
   rooms: [{id, name, kind, x, z, w, d, tint, people:[{name, role}]}]
   kind: team | boss | meet | sched | lounge */
(function (global) {
"use strict";
const T = () => global.THREE;

function createOffice(container, opt) {
  const THREE = T();
  const rooms = opt.rooms;
  const W0 = 40, D0 = 30, CX = W0 / 2, CZ = D0 / 2;

  /* ── 렌더러 · 카메라 · 빛 ── */
  if (THREE.ColorManagement) THREE.ColorManagement.legacyMode = false;
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(2, global.devicePixelRatio || 1));
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.outputEncoding = THREE.sRGBEncoding;
  renderer.toneMapping = THREE.NoToneMapping;
  container.appendChild(renderer.domElement);
  renderer.domElement.style.cssText = "display:block;width:100%;height:100%";

  const scene = new THREE.Scene();
  const cam = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.1, 400);
  let az = Math.PI * 0.25, tAz = az, zoom = 1, tZoom = 1, panX = 0, panZ = 0;
  const EL = 0.62; /* 카메라 높이 각도(라디안) */

  scene.add(new THREE.HemisphereLight(0xffffff, 0xcfc8b8, 0.62));
  const sun = new THREE.DirectionalLight(0xfff6e8, 0.85);
  sun.position.set(CX + 22, 38, CZ + 14); sun.target.position.set(CX, 0, CZ);
  sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -34, right: 34, top: 30, bottom: -30, near: 1, far: 120 });
  sun.shadow.bias = -0.0004; sun.shadow.radius = 4;
  scene.add(sun, sun.target);

  /* ── 재질 ── */
  const M = {};
  const mat = (k, c, o = {}) => (M[k] = M[k] || new THREE.MeshStandardMaterial(Object.assign({ color: c, roughness: 0.82, metalness: 0.02 }, o)));
  const box = (w, h, d, m, x, y, z, parent, cast = true) => {
    const g = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), m);
    g.position.set(x, y, z); g.castShadow = cast; g.receiveShadow = true; (parent || scene).add(g); return g;
  };
  const tex = (draw, s = 256) => { const c = document.createElement("canvas"); c.width = c.height = s; draw(c.getContext("2d"), s);
    const t = new THREE.CanvasTexture(c); t.encoding = THREE.sRGBEncoding; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.anisotropy = 4; return t; };

  /* 바닥: 테라조(잔점) */
  const terrazzo = tex((g, s) => { g.fillStyle = "#f4f2ec"; g.fillRect(0, 0, s, s);
    for (let i = 0; i < 1400; i++) { g.fillStyle = ["#d9d5cb", "#c9c3b6", "#e7e3da", "#bdb6a7"][i % 4]; g.globalAlpha = 0.55; g.beginPath(); g.arc(Math.random() * s, Math.random() * s, Math.random() * 1.6 + 0.3, 0, 7); g.fill(); } g.globalAlpha = 1; });
  terrazzo.repeat.set(10, 8);
  const slab = box(W0, 0.6, D0, new THREE.MeshStandardMaterial({ map: terrazzo, roughness: 0.9 }), CX, -0.3, CZ, scene, false);
  box(W0 + 0.6, 0.9, D0 + 0.6, mat("slabside", 0xe2ded5), CX, -0.75, CZ, scene, false);

  /* 나무 바닥(헤링본) */
  const wood = tex((g, s) => { g.fillStyle = "#8a5a36"; g.fillRect(0, 0, s, s); const u = s / 8;
    for (let y = -1; y < 10; y++) for (let x = -1; x < 10; x++) { g.save(); g.translate(x * u, y * u); g.rotate(((x + y) % 2 ? 1 : -1) * Math.PI / 4);
      g.fillStyle = ["#9b6a41", "#86552f", "#a87548", "#7c4e2c"][(x * 3 + y) & 3]; g.fillRect(-u * 0.7, -u * 0.18, u * 1.4, u * 0.34); g.restore(); } });
  wood.repeat.set(3, 3);

  /* ── 유리 외벽(뒤쪽 두 면) ── */
  const glass = new THREE.MeshStandardMaterial({ color: 0xcfe6ee, transparent: true, opacity: 0.22, roughness: 0.1, metalness: 0.1, depthWrite: false });
  const frame = mat("frame", 0x3b4248, { roughness: 0.5 });
  function wall(ax, len, fixed) {
    for (let i = 0; i <= len; i += 2) {
      if (ax === "x") box(0.1, 3.2, 0.1, frame, i, 1.6, fixed); else box(0.1, 3.2, 0.1, frame, fixed, 1.6, i);
    }
    if (ax === "x") { const g = box(len, 3.1, 0.04, glass, len / 2, 1.6, fixed, scene, false); g.receiveShadow = false;
      box(len, 0.12, 0.14, frame, len / 2, 3.2, fixed); box(len, 0.1, 0.14, frame, len / 2, 0.05, fixed); }
    else { const g = box(0.04, 3.1, len, glass, fixed, 1.6, len / 2, scene, false); g.receiveShadow = false;
      box(0.14, 0.12, len, frame, fixed, 3.2, len / 2); box(0.14, 0.1, len, frame, fixed, 0.05, len / 2); }
  }
  wall("x", W0, 0.05); wall("z", D0, 0.05);

  /* ── 가구 ── */
  const C = { desk: mat("desk", 0xf3f2ee), leg: mat("leg", 0x9aa0a6, { metalness: 0.4, roughness: 0.4 }), screen: mat("screen", 0x1c2126, { roughness: 0.35 }),
    chair: mat("chair", 0x3a3f45), planter: mat("planter", 0xb99a73), leaf: mat("leaf", 0x4f7f43), leaf2: mat("leaf2", 0x5f9550), leaf3: mat("leaf3", 0x3e6b37),
    trunk: mat("trunk", 0x6e4f35), wood: mat("woodm", 0xa77a4f), board: mat("board", 0x2f4a3a), moss: mat("moss", 0x3f6b3a), rack: mat("rack", 0x16191c, { roughness: 0.4 }),
    white: mat("white", 0xfafaf7), sofa: mat("sofa", 0xd8d1c4), lamp: mat("lamp", 0xe9d9a8, { emissive: 0x3a2f10 }) };
  const shrubGeo = new THREE.IcosahedronGeometry(0.32, 0);
  function shrub(x, y, z, s = 1, parent) { const m = new THREE.Mesh(shrubGeo, [C.leaf, C.leaf2, C.leaf3][Math.floor(Math.random() * 3)]);
    m.position.set(x, y, z); m.scale.setScalar(s); m.rotation.set(Math.random() * 3, Math.random() * 3, 0); m.castShadow = true; (parent || scene).add(m); return m; }
  function planterRow(x, z, len) { box(len, 0.5, 0.5, C.planter, x + len / 2, 0.25, z); for (let i = 0.3; i < len; i += 0.45) shrub(x + i, 0.62 + Math.random() * 0.1, z + (Math.random() - 0.5) * 0.15, 0.8 + Math.random() * 0.4); }
  function potPlant(x, z, s = 1) { const g = new THREE.Mesh(new THREE.CylinderGeometry(0.25 * s, 0.2 * s, 0.45 * s, 10), C.planter); g.position.set(x, 0.22 * s, z); g.castShadow = true; scene.add(g);
    for (let i = 0; i < 5; i++) shrub(x + (Math.random() - 0.5) * 0.3 * s, 0.6 * s + i * 0.22 * s, z + (Math.random() - 0.5) * 0.3 * s, (0.9 - i * 0.12) * s); }
  function tree(x, z) { const t = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.18, 2.2, 8), C.trunk); t.position.set(x, 1.1, z); t.castShadow = true; scene.add(t);
    box(1.1, 0.5, 1.1, C.planter, x, 0.25, z); for (let i = 0; i < 14; i++) shrub(x + (Math.random() - 0.5) * 1.6, 2.1 + Math.random() * 1.0, z + (Math.random() - 0.5) * 1.6, 1.4 + Math.random() * 0.6); }
  function desk(x, z, face = -1) { /* face: 모니터가 향하는 z 방향(−1 = 뒤쪽 벽) */
    box(1.4, 0.05, 0.7, C.desk, x, 0.74, z); for (const [dx, dz] of [[-0.65, -0.3], [0.65, -0.3], [-0.65, 0.3], [0.65, 0.3]]) box(0.04, 0.72, 0.04, C.leg, x + dx, 0.36, z + dz, scene, false);
    box(0.62, 0.38, 0.04, C.screen, x, 1.05, z + face * 0.2); box(0.06, 0.18, 0.06, C.leg, x, 0.85, z + face * 0.22, scene, false);
    box(0.4, 0.02, 0.14, C.screen, x, 0.78, z + 0.05, scene, false);
    const cz = z - face * 0.62; box(0.5, 0.08, 0.5, C.chair, x, 0.46, cz); box(0.5, 0.55, 0.07, C.chair, x, 0.78, cz - face * 0.24); box(0.06, 0.42, 0.06, C.leg, x, 0.21, cz, scene, false);
    return { sx: x, sz: cz };
  }
  function standee(x, z) { box(0.9, 1.3, 0.05, C.white, x, 1.0, z); box(0.04, 0.4, 0.04, C.leg, x - 0.35, 0.2, z, scene, false); box(0.04, 0.4, 0.04, C.leg, x + 0.35, 0.2, z, scene, false);
    const cols = [0xf6d365, 0xf7a1a1, 0x9fd8a8, 0x9ec7f0]; for (let i = 0; i < 9; i++) box(0.16, 0.16, 0.01, mat("note" + (i % 4), cols[i % 4]), x - 0.3 + (i % 3) * 0.3, 1.3 - Math.floor(i / 3) * 0.3, z + 0.035, scene, false); }

  /* ── 사람 ── */
  const SKIN = mat("skin", 0xf0c7a0), HAIR = mat("hair", 0x2a2420), PANTS = mat("pants", 0x2f3438), SHOE = mat("shoe", 0x1b1d1f), HELMET = mat("helmet", 0xf2c230);
  const SHIRTS = [0x3d6fb6, 0xc2563a, 0x2f8f6a, 0x8a4fb0, 0xd39b2a, 0x50606e, 0xb83b5e, 0x2b7a8c, 0x6b8e23, 0xd9734a];
  const people = [], pickables = [];
  function person(colorIdx, opt2 = {}) {
    const g = new THREE.Group(); const shirt = mat("shirt" + colorIdx, SHIRTS[colorIdx % SHIRTS.length]);
    const legL = box(0.16, 0.72, 0.2, PANTS, -0.11, 0.36, 0, g), legR = box(0.16, 0.72, 0.2, PANTS, 0.11, 0.36, 0, g);
    const shoeL = box(0.17, 0.08, 0.26, SHOE, -0.11, 0.04, 0.03, g), shoeR = box(0.17, 0.08, 0.26, SHOE, 0.11, 0.04, 0.03, g);
    const body = box(0.46, 0.6, 0.26, shirt, 0, 1.02, 0, g);
    const armL = box(0.12, 0.56, 0.16, shirt, -0.3, 1.02, 0, g), armR = box(0.12, 0.56, 0.16, shirt, 0.3, 1.02, 0, g);
    const head = box(0.32, 0.32, 0.3, SKIN, 0, 1.52, 0, g);
    const hairs = [box(0.34, 0.12, 0.32, opt2.helmet ? HELMET : HAIR, 0, 1.71, 0, g)]; if (!opt2.helmet) hairs.push(box(0.34, 0.2, 0.08, HAIR, 0, 1.6, -0.13, g));
    g.userData = { legL, legR, armL, armR, body, head, shoeL, shoeR, hairs }; g.traverse(m => { if (m.isMesh) m.userData.owner = g; });
    return g;
  }
  function sit(p) { const u = p.userData; const drop = 0.12;
    for (const [l, sh, x] of [[u.legL, u.shoeL, -0.11], [u.legR, u.shoeR, 0.11]]) { l.rotation.x = -Math.PI / 2; l.position.set(x, 0.5, 0.3); sh.position.set(x, 0.2, 0.62); sh.rotation.x = 0; }
    u.legL.scale.y = u.legR.scale.y = 0.75;
    for (const m of [u.body, u.armL, u.armR, u.head, ...u.hairs]) m.position.y -= drop; }

  /* ── HTML 이름표 ── */
  const overlay = document.createElement("div");
  overlay.style.cssText = "position:absolute;inset:0;pointer-events:none;overflow:hidden";
  if (getComputedStyle(container).position === "static") container.style.position = "relative"; container.appendChild(overlay);
  const labels = [];
  function addLabel(html, pos, cls, clickData) { const el = document.createElement("div"); el.className = "o3-l " + (cls || ""); el.innerHTML = html; overlay.appendChild(el);
    if (clickData) { el.style.pointerEvents = "auto"; el.style.cursor = "pointer"; el.addEventListener("click", e => { e.stopPropagation(); opt.onPick && opt.onPick(clickData, e); }); }
    const L = { el, pos, cls }; labels.push(L); return L; }

  /* ── 방 만들기 ── */
  const roomObjs = {};
  let ci = 0;
  for (const r of rooms) {
    const floorMat = r.kind === "boss" ? new THREE.MeshStandardMaterial({ map: wood, roughness: 0.7 }) : new THREE.MeshStandardMaterial({ color: r.tint, roughness: 0.95, transparent: true, opacity: 0.6 });
    const fl = new THREE.Mesh(new THREE.PlaneGeometry(r.w, r.d), floorMat); fl.rotation.x = -Math.PI / 2; fl.position.set(r.x + r.w / 2, 0.012, r.z + r.d / 2); fl.receiveShadow = true; fl.userData.room = r; scene.add(fl); pickables.push(fl);
    const R = roomObjs[r.id] = { r, people: [], dot: null };
    const seats = [];
    if (r.kind === "team") {
      planterRow(r.x + 0.3, r.z + 0.45, r.w - 0.6);
      const cols = Math.max(1, Math.floor((r.w - 0.8) / 1.9)), rows = Math.max(1, Math.floor((r.d - 1.6) / 2.6));
      const need = Math.max(r.people.length, Math.min(cols * rows, r.people.length + 2));
      for (let i = 0; i < need; i++) { const c = i % cols, rw = Math.floor(i / cols); if (rw >= rows) break;
        const x = r.x + 0.4 + (r.w - 0.8) * (c + 0.5) / cols, z = r.z + 1.6 + rw * 2.6; seats.push(desk(x, z, -1)); }
      standee(r.x + 0.35, r.z + r.d - 1.0);
    } else if (r.kind === "boss") {
      box(2.2, 0.06, 1.0, C.wood, r.x + r.w / 2, 0.76, r.z + 2.0); box(0.1, 0.74, 0.9, C.wood, r.x + r.w / 2 - 1.0, 0.37, r.z + 2.0); box(0.1, 0.74, 0.9, C.wood, r.x + r.w / 2 + 1.0, 0.37, r.z + 2.0);
      box(0.7, 0.42, 0.05, C.screen, r.x + r.w / 2 - 0.4, 1.0, r.z + 1.65); box(0.7, 0.42, 0.05, C.screen, r.x + r.w / 2 + 0.4, 1.0, r.z + 1.65);
      const cz = r.z + 2.75; box(0.6, 0.1, 0.6, C.chair, r.x + r.w / 2, 0.48, cz); box(0.6, 0.8, 0.08, C.chair, r.x + r.w / 2, 0.9, cz + 0.28); seats.push({ sx: r.x + r.w / 2, sz: cz, face: -1 });
      box(2.4, 1.8, 0.4, C.wood, r.x + 1.6, 0.9, r.z + 0.4); for (let i = 0; i < 4; i++) box(2.2, 0.03, 0.36, C.white, r.x + 1.6, 0.35 + i * 0.45, r.z + 0.42, scene, false);
      const tb = new THREE.Mesh(new THREE.CylinderGeometry(0.7, 0.7, 0.05, 24), C.white); tb.position.set(r.x + r.w - 2.0, 0.72, r.z + r.d - 1.8); tb.castShadow = true; scene.add(tb);
      box(0.08, 0.7, 0.08, C.leg, r.x + r.w - 2.0, 0.35, r.z + r.d - 1.8, scene, false);
      box(2.2, 0.45, 0.8, C.sofa, r.x + 1.6, 0.22, r.z + r.d - 1.0); box(2.2, 0.5, 0.2, C.sofa, r.x + 1.6, 0.6, r.z + r.d - 0.55);
      potPlant(r.x + r.w - 0.5, r.z + 0.5, 1.1);
    } else if (r.kind === "meet") {
      box(r.w - 2.4, 1.6, 0.25, C.moss, r.x + r.w / 2 - 0.8, 1.2, r.z + 0.25); box(2.0, 1.1, 0.06, C.board, r.x + r.w - 2.2, 1.35, r.z + 0.3);
      box(r.w - 3, 0.08, 1.4, C.wood, r.x + r.w / 2, 0.74, r.z + r.d / 2 + 0.3); for (const dx of [-1, 1]) box(0.1, 0.72, 1.2, C.wood, r.x + r.w / 2 + dx * (r.w - 3.4) / 2, 0.36, r.z + r.d / 2 + 0.3);
      for (const dz of [-1.05, 1.05]) box(r.w - 3.4, 0.4, 0.4, C.wood, r.x + r.w / 2, 0.22, r.z + r.d / 2 + 0.3 + dz);
      const cols2 = [0xf6d365, 0xf7a1a1, 0x9fd8a8, 0xbfa5e6]; for (let i = 0; i < 6; i++) box(0.35, 0.05, 0.25, mat("pad" + (i % 4), cols2[i % 4]), r.x + 2.2 + i * 0.9, 0.81, r.z + r.d / 2 + 0.3 + (i % 2 ? 0.3 : -0.3), scene, false);
      tree(r.x + 1.1, r.z + r.d - 1.2); seats.push({ sx: r.x + r.w - 2.2, sz: r.z + 1.3, stand: true, face: -1 });
    } else if (r.kind === "sched") {
      for (const [a, b, c2, d2] of [[r.x, r.z, r.w, 0], [r.x, r.z, 0, r.d], [r.x, r.z + r.d, r.w, 0], [r.x + r.w, r.z, 0, r.d]]) {
        if (c2) box(c2, 2.4, 0.04, glass, a + c2 / 2, 1.2, b, scene, false); else box(0.04, 2.4, d2, glass, a, 1.2, b + d2 / 2, scene, false);
        if (c2) box(c2, 0.06, 0.08, frame, a + c2 / 2, 2.4, b); else box(0.08, 0.06, d2, frame, a, 2.4, b + d2 / 2); }
      for (let i = 0; i < 4; i++) { const rx = r.x + 1.0 + i * 0.9; box(0.75, 2.0, 0.9, C.rack, rx, 1.0, r.z + 1.2);
        for (let j = 0; j < 6; j++) box(0.05, 0.03, 0.01, mat("led" + (j % 2), j % 2 ? 0x46e07a : 0x4aa3ff, { emissive: j % 2 ? 0x1f9d55 : 0x2f6fd6, emissiveIntensity: 1.2 }), rx - 0.22, 0.4 + j * 0.27, r.z + 1.66, scene, false); }
      box(0.75, 2.0, 0.9, C.rack, r.x + r.w - 1.0, 1.0, r.z + r.d - 1.4);
    } else if (r.kind === "lounge") {
      box(r.w - 2, 1.0, 0.6, C.wood, r.x + r.w / 2, 0.5, r.z + 1.2); box(r.w - 1.8, 0.06, 0.8, C.white, r.x + r.w / 2, 1.03, r.z + 1.2);
      for (let i = 0; i < 4; i++) { const sx = r.x + 1.6 + i * 1.1; const st = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.06, 14), C.chair); st.position.set(sx, 0.72, r.z + 2.0); st.castShadow = true; scene.add(st); box(0.05, 0.7, 0.05, C.leg, sx, 0.35, r.z + 2.0, scene, false); }
      box(0.8, 1.9, 0.7, C.white, r.x + r.w - 0.7, 0.95, r.z + 0.6); potPlant(r.x + 0.6, r.z + r.d - 0.6, 1.2); potPlant(r.x + r.w - 0.6, r.z + r.d - 0.6, 1.0);
      box(1.6, 0.06, 0.8, C.white, r.x + r.w / 2, 0.74, r.z + r.d - 2.2); box(0.06, 0.72, 0.06, C.leg, r.x + r.w / 2, 0.36, r.z + r.d - 2.2, scene, false);
    }
    /* 사람 앉히기 */
    r.people.forEach((pp, i) => {
      const s = seats[i] || { sx: r.x + 1 + i * 1.2, sz: r.z + r.d - 1.5, stand: true };
      const p = person(r.kind === "boss" ? 3 : ci++, { helmet: r.kind === "sched" });
      if (r.kind === "sched") { p.position.set(r.x + 1.0 + (i % 4) * 0.9, 0, r.z + 2.3 + Math.floor(i / 4) * 0.9); p.rotation.y = Math.PI; }
      else { p.position.set(s.sx, 0, s.sz); p.rotation.y = Math.PI; if (!s.stand) sit(p); }
      p.userData.pick = { room: r, idx: i, person: pp }; scene.add(p); people.push(p);
      p.traverse(m => { if (m.isMesh) pickables.push(m); });
      const head = new THREE.Vector3(p.position.x, s.stand || r.kind === "sched" ? 2.05 : 1.95, p.position.z);
      const badge = addLabel('<i class="o3-b">–</i>', head, "o3-badge", { room: r, idx: i, person: pp });
      const tag = addLabel(pp.name, new THREE.Vector3(p.position.x, 0.05, p.position.z + 0.5), "o3-tag", { room: r, idx: i, person: pp });
      const bub = addLabel("", new THREE.Vector3(p.position.x, 2.75, p.position.z), "o3-bub"); bub.el.style.display = "none";
      R.people.push({ p, badge, tag, bub, status: "idle", base: p.position.clone() });
    });
    R.dot = addLabel('<i class="o3-dot"></i>' + r.name, new THREE.Vector3(r.x + r.w / 2, 0.05, r.z + r.d - 0.35), "o3-room", { room: r });
  }
  /* 복도 장식 */
  potPlant(18.7, 10.6, 1.0); potPlant(29.2, 10.4, 0.9); potPlant(10.4, 18.6, 1.0); potPlant(23.3, 20.2, 0.9); potPlant(14.6, 27.5, 1.1);

  /* 돌아다니는 사람 2명 */
  const walkers = [];
  [[[9.4, 10.2], [18.8, 10.2], [18.8, 19.6], [9.4, 19.6]], [[23.0, 19.8], [38.5, 19.8], [38.5, 10.2], [29.0, 10.2]]].forEach((path, k) => {
    const p = person(7 + k); scene.add(p); walkers.push({ p, path, t: k * 0.37 }); });

  /* ── 투영 · 리사이즈 ── */
  let Wd = 1, Hd = 1;
  function resize() { Wd = Math.max(1, container.clientWidth); Hd = Math.max(1, container.clientHeight); renderer.setSize(Wd, Hd, false); }
  /* 사무실 전체가 화면에 딱 맞게: 바닥 모서리와 벽 윗부분을 카메라 좌표로 투영해 범위를 잡음 */
  const corners = []; for (const x of [0, W0]) for (const z of [0, D0]) for (const y of [-1.2, 3.4]) corners.push(new THREE.Vector3(x, y, z));
  const tmp = new THREE.Vector3();
  function place() {
    const aspect = Wd / Hd, base = Math.max(17.5, 23 / aspect), span = base / zoom;
    const lim = base - span; panX = Math.max(-lim * aspect, Math.min(lim * aspect, panX)); panZ = Math.max(-lim, Math.min(lim, panZ));
    cam.left = -span * aspect + panX; cam.right = span * aspect + panX; cam.top = span + panZ; cam.bottom = -span + panZ; cam.updateProjectionMatrix();
    const dist = 80;
    cam.position.set(CX + Math.sin(az) * Math.cos(EL) * dist, Math.sin(EL) * dist, CZ + Math.cos(az) * Math.cos(EL) * dist); cam.lookAt(CX, 0, CZ);
  }
  const v = new THREE.Vector3();
  function updLabels() {
    const showTags = false, showBub = true; for (const L of labels) { if (L.cls === "o3-tag") L.el.style.visibility = showTags ? "visible" : "hidden"; if (L.cls === "o3-bub") L.el.style.visibility = showBub ? "visible" : "hidden"; if (L.el.style.display === "none") continue; v.copy(L.pos).project(cam);
      const x = (v.x + 1) / 2 * Wd, y = (1 - v.y) / 2 * Hd; L.el.style.transform = `translate(${x.toFixed(1)}px,${y.toFixed(1)}px) translate(-50%,-50%)`; L.el.style.zIndex = String(1000 - Math.round(v.z * 500)); }
  }

  /* ── 애니메이션 ── */
  const clock = new THREE.Clock();
  function tick() {
    const t = clock.getElapsedTime(), dt = Math.min(0.05, clock.getDelta() || 0.016);
    az += (tAz - az) * 0.12; zoom += (tZoom - zoom) * 0.15; place();
    for (const id in roomObjs) for (const P of roomObjs[id].people) { const u = P.p.userData;
      if (P.status === "run") { u.armL.rotation.x = -1.1 + Math.sin(t * 14) * 0.2; u.armR.rotation.x = -1.1 + Math.cos(t * 14) * 0.2; P.p.position.y = Math.abs(Math.sin(t * 7)) * 0.02; }
      else if (P.status === "err") { P.p.rotation.z = Math.sin(t * 3) * 0.06; u.armL.rotation.x = u.armR.rotation.x = 0; }
      else if (P.status === "think") { u.head.rotation.y = Math.sin(t * 1.3) * 0.5; u.armR.rotation.x = -0.6; }
      else { u.armL.rotation.x = u.armR.rotation.x = -0.25; P.p.position.y = Math.sin(t * 1.6 + P.base.x) * 0.008; P.p.rotation.z = 0; u.head.rotation.y = 0; } }
    for (const w of walkers) { w.t += 0.0009; const n = w.path.length, f = (w.t % 1) * n, i = Math.floor(f), a = w.path[i], b = w.path[(i + 1) % n], k = f - i;
      const x = a[0] + (b[0] - a[0]) * k, z = a[1] + (b[1] - a[1]) * k; w.p.position.set(x, 0, z); w.p.rotation.y = Math.atan2(b[0] - a[0], b[1] - a[1]);
      const s = Math.sin(t * 8); w.p.userData.legL.rotation.x = s * 0.5; w.p.userData.legR.rotation.x = -s * 0.5; w.p.userData.armL.rotation.x = -s * 0.4; w.p.userData.armR.rotation.x = s * 0.4; }
    renderer.render(scene, cam); updLabels(); requestAnimationFrame(tick);
  }

  /* ── 조작: 끌어서 회전, 휠·핀치 확대, 클릭 선택 ── */
  const el = renderer.domElement; el.style.cursor = "default"; let drag = null;
  function touchMode() { el.style.touchAction = tZoom > 1.01 ? "none" : "pan-y"; el.style.cursor = tZoom > 1.01 ? "grab" : "default"; }
  el.addEventListener("pointerdown", e => { drag = { x: e.clientX, y: e.clientY, px: panX, pz: panZ, moved: false }; if (tZoom > 1.01) el.setPointerCapture(e.pointerId); });
  el.addEventListener("pointermove", e => { if (!drag) return; const dx = e.clientX - drag.x, dy = e.clientY - drag.y; if (Math.abs(dx) + Math.abs(dy) > 5) drag.moved = true;
    if (tZoom > 1.01 && drag.moved) { const r = el.getBoundingClientRect(), k = (cam.right - cam.left) / r.width; panX = drag.px - dx * k; panZ = drag.pz + dy * k; } });
  el.addEventListener("pointerup", e => { const d = drag; drag = null; if (d && !d.moved) pick(e); });
  el.addEventListener("pointercancel", () => { drag = null; });
  touchMode();
  const ray = new THREE.Raycaster(), ndc = new THREE.Vector2();
  function pick(e) { const r = el.getBoundingClientRect(); ndc.set((e.clientX - r.left) / r.width * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1); ray.setFromCamera(ndc, cam);
    const hit = ray.intersectObjects(pickables, false)[0]; if (!hit) { opt.onPick && opt.onPick(null, e); return; }
    const o = hit.object.userData.owner; if (o && o.userData.pick) opt.onPick && opt.onPick({ room: o.userData.pick.room, idx: o.userData.pick.idx, person: o.userData.pick.person }, e);
    else if (hit.object.userData.room) opt.onPick && opt.onPick({ room: hit.object.userData.room }, e); }

  resize(); new ResizeObserver(resize).observe(container); place(); tick();

  const ICON = { run: "▶", think: "…", turn: "!", err: "×", idle: "–" };
  return {
    setStatus(roomId, idx, st) { const R = roomObjs[roomId]; if (!R || !R.people[idx]) return; const P = R.people[idx]; P.status = st; P.badge.el.className = "o3-l o3-badge s-" + st; P.badge.el.innerHTML = `<i class="o3-b">${ICON[st] || "–"}</i>`; },
    setRoom(roomId, st) { const R = roomObjs[roomId]; if (R) R.dot.el.className = "o3-l o3-room s-" + st; },
    setBubble(roomId, idx, text) { const R = roomObjs[roomId]; if (!R || !R.people[idx]) return; const b = R.people[idx].bub; if (!text) { b.el.style.display = "none"; return; } b.el.textContent = text; b.el.style.display = ""; },
    setName(roomId, idx, text) { const R = roomObjs[roomId]; if (R && R.people[idx]) R.people[idx].tag.el.textContent = text; },
    rotate(d) { tAz += d; }, zoomBy(f) { tZoom = Math.max(1, Math.min(3.5, tZoom * f)); touchMode(); }, zoomReset() { tZoom = 1; panX = 0; panZ = 0; touchMode(); },
  };
}
global.createOffice = createOffice;
})(window);
