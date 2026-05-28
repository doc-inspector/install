/**
 * hero-office.js v6 — Chibi office scene for hero section
 * 3 throw types: distant hand throw, distant kick, carry to bin
 * Docs land at varying depths (Y), chibi moves in depth too
 * Bin always visible, desks on both sides
 */
(function(){
'use strict';

const CYAN = [6, 182, 212];
const c = (a) => `rgba(${CYAN[0]},${CYAN[1]},${CYAN[2]},${a})`;
const IS_MOBILE = () => window.innerWidth < 900;

/* ─── TIMING ─────────────────────────────────────────── */
const ACTIVE_DURATION = 30000;
const HAPPY_DURATION  = 15000;
const CHIBI_SPEED     = 0.22;

/* ─── GLOBAL STATE ───────────────────────────────────── */
let canvas, ctx, cssW, cssH, heroEl, floorY, floorBottom;
let chibi, trashBin;
let desks = [];
let currentDoc = null;
let flyingDoc = null;
let animFrame, prevTime = 0;

let phase = 'first_idle';
let phaseStart = 0;
let docsThrown = 0;

// throw pattern: 0=distant hand, 1=distant kick, 2=carry to bin
const THROW_PATTERN = [2, 0, 1, 2, 0, 2, 1, 0];

let mouseX = 0.5, mouseY = 0.5;

function lerp(a,b,t){ return a+(b-a)*t; }
function rand(a,b){ return a+Math.random()*(b-a); }
function clamp(v,lo,hi){ return Math.max(lo,Math.min(hi,v)); }

/* ─── PSEUDO-3D DEPTH HELPERS ────────────────────────── */
// depth: 0 = floor line (near), 1 = bottom of hero (far)
// Objects deeper → lower Y, smaller scale, lower alpha
function depthToY(depth){
  return floorY + depth * (floorBottom - floorY);
}
function yToDepth(y){
  return (y - floorY) / (floorBottom - floorY);
}
function depthScale(depth){
  return lerp(1, 0.6, depth);
}

/* ─── INIT ───────────────────────────────────────────── */
function init(){
  heroEl = document.querySelector('.hero');
  if(!heroEl) return;
  
  const rain = document.querySelector('.doc-rain');
  if(rain) rain.style.display = 'none';
  
  canvas = document.createElement('canvas');
  canvas.id = 'hero-office-canvas';
  canvas.style.cssText = 'position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:1;';
  heroEl.style.position = 'relative';
  const cont = heroEl.querySelector('.container');
  if(cont) heroEl.insertBefore(canvas, cont);
  else heroEl.insertBefore(canvas, heroEl.firstChild);
  ctx = canvas.getContext('2d');

  resize();
  initChibi();
  initTrashBin();
  if(!IS_MOBILE()) initDesks();

  window.addEventListener('resize', onResize);
  heroEl.addEventListener('mousemove', e => {
    const r = heroEl.getBoundingClientRect();
    mouseX = (e.clientX - r.left)/r.width;
    mouseY = (e.clientY - r.top)/r.height;
  });

  phase = 'first_idle';
  phaseStart = performance.now();
  animFrame = requestAnimationFrame(loop);
}

function resize(){
  const r = heroEl.getBoundingClientRect();
  const dpr = window.devicePixelRatio||1;
  cssW = r.width; cssH = r.height;
  canvas.width = cssW*dpr; canvas.height = cssH*dpr;
  canvas.style.width = cssW+'px'; canvas.style.height = cssH+'px';
  ctx.setTransform(dpr,0,0,dpr,0,0);
  floorY = cssH * 0.62;
  floorBottom = cssH * 0.92;
}

let resizeTimer;
function onResize(){
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(()=>{
    resize();
    if(!IS_MOBILE()){ desks=[]; initDesks(); } else desks=[];
    initTrashBin();
    positionChibiOnImage();
  },200);
}

/* ─── 3D GRID ────────────────────────────────────────── */
function drawGrid(){
  const w = cssW, h = cssH;
  const vanishX = w*0.5 + (mouseX-0.5)*30;
  const vanishY = h*0.18;
  const alpha = 0.06;

  const rows = 28;
  for(let i=0;i<=rows;i++){
    const t2 = i/rows;
    const y = vanishY + t2*t2*(h - vanishY)*1.1;
    const squeeze = 1 - t2*0.45;
    const lx = vanishX - (w*0.85)*squeeze;
    const rx = vanishX + (w*0.85)*squeeze;
    ctx.beginPath();
    ctx.moveTo(lx,y); ctx.lineTo(rx,y);
    ctx.strokeStyle = c(alpha * (0.3 + t2*0.7));
    ctx.lineWidth = 0.5 + t2*0.3;
    ctx.stroke();
  }

  const cols = 24, sp = 50;
  for(let i=-cols/2;i<=cols/2;i++){
    const baseX = vanishX + i*sp;
    const farX = vanishX + i*sp*0.03;
    ctx.beginPath();
    ctx.moveTo(baseX, h+20);
    ctx.lineTo(lerp(baseX,farX,0.95), vanishY);
    ctx.strokeStyle = c(alpha*0.5);
    ctx.lineWidth = 0.4;
    ctx.stroke();
  }
}

/* ─── CHIBI ──────────────────────────────────────────── */
function getImagePos(){
  const vis = document.querySelector('.hero-visual');
  if(!vis) return { x: cssW*0.35, y: floorY - 40 };
  const vr = vis.getBoundingClientRect();
  const hr = heroEl.getBoundingClientRect();
  return {
    x: (vr.left-hr.left) + vr.width*0.45,
    y: (vr.top-hr.top) - 4,
  };
}

function initChibi(){
  const pos = getImagePos();
  chibi = {
    x: pos.x, y: pos.y,
    size: IS_MOBILE()?36:46,
    state: 'on_image',
    stateTime: 0,
    headTilt: 0, headPhase: 0,
    legPhase: 0,
    facingRight: true,
    emotion: 'annoyed',
    fallVY: 0,
    blinkTimer: rand(2000,4000), isBlinking: false,
    throwAnim: 0,
    throwMode: 2, // 0=distant hand, 1=distant kick, 2=carry
    holdingDoc: false,
    holdDocType: 0,
    depth: 0, // current depth on floor
  };
}

function positionChibiOnImage(){
  const pos = getImagePos();
  if(chibi.state==='on_image' || chibi.state==='happy_on_image'){
    chibi.x = pos.x; chibi.y = pos.y;
  }
}

function setChibiState(newState){
  chibi.state = newState;
  chibi.stateTime = 0;

  // Dynamic slider interaction
  try {
    const btnOnline = document.querySelector('.slider-btn[data-slide="0"]');
    const btnDesktop = document.querySelector('.slider-btn[data-slide="1"]');
    
    if(['on_image', 'happy_on_image'].includes(newState)) {
      // Show Desktop App (Slide 1) only when chibi is resting/happy on top of the frame
      if(btnDesktop && !btnDesktop.classList.contains('active')) {
        btnDesktop.click();
      }
    } else {
      // Show Online Tools (Slide 0) most of the time when chibi is processing files on the floor
      if(btnOnline && !btnOnline.classList.contains('active')) {
        btnOnline.click();
      }
    }
  } catch(e){}
}

function getFloorRestX(){ return cssW * (IS_MOBILE() ? 0.4 : 0.42); }

/* ─── chibi size scaled by depth ─── */
function getChibiDrawSize(){
  const base = IS_MOBILE() ? 36 : 46;
  if(['on_image','looking_down','happy_on_image'].includes(chibi.state)) return base;
  return base * depthScale(chibi.depth);
}

function updateChibi(dt){
  const ch = chibi;
  ch.stateTime += dt;

  ch.blinkTimer -= dt;
  if(ch.blinkTimer<=0){
    if(!ch.isBlinking){ ch.isBlinking=true; ch.blinkTimer=130; }
    else { ch.isBlinking=false; ch.blinkTimer=rand(2500,5000); }
  }

  switch(ch.state){

    case 'on_image': {
      const pos = getImagePos();
      ch.x = pos.x; ch.y = pos.y;
      ch.headPhase += dt*0.003;
      ch.headTilt = Math.sin(ch.headPhase)*0.8;
      ch.emotion = 'annoyed';
      break;
    }

    case 'looking_down': {
      const pos = getImagePos();
      ch.x = pos.x; ch.y = pos.y;
      ch.emotion = 'shocked';
      if(currentDoc){
        ch.headTilt = clamp((currentDoc.x - ch.x)/200, -1.2, 1.2);
        ch.facingRight = currentDoc.x > ch.x;
      }
      if(ch.stateTime > 800){
        setChibiState('falling_off');
        ch.fallVY = 0;
      }
      break;
    }

    case 'falling_off': {
      ch.emotion = 'shocked';
      ch.fallVY += dt * 0.001;
      ch.y += ch.fallVY * dt;
      if(currentDoc) ch.x += (currentDoc.x > ch.x ? 0.04 : -0.04) * dt;
      
      if(ch.y >= floorY + 8){
        ch.y = floorY + 8;
        ch.depth = 0;
        setChibiState('wait_for_land');
        ch.emotion = 'annoyed';
      }
      break;
    }

    case 'wait_for_land': {
      ch.emotion = 'annoyed';
      ch.headPhase += dt*0.004;
      if(currentDoc){
        ch.facingRight = currentDoc.x > ch.x;
        ch.headTilt = clamp((currentDoc.x - ch.x)/300, -0.8, 0.8);
        if(currentDoc.state === 'falling'){
          ch.headTilt += -0.2;
        }
      }
      if(currentDoc && currentDoc.state === 'landed'){
        setChibiState('running_to_doc');
      }
      if(!currentDoc){
        setChibiState('idle_on_floor');
      }
      break;
    }

    case 'running_to_doc': {
      ch.legPhase += dt*0.02;
      ch.emotion = 'annoyed';
      if(!currentDoc){ setChibiState('idle_on_floor'); break; }

      const tx = currentDoc.x;
      const ty = currentDoc.y;
      const dx = tx - ch.x;
      const dy = ty - ch.y;
      const dist = Math.sqrt(dx*dx + dy*dy);
      ch.facingRight = dx > 0;
      ch.headTilt = clamp(dx*0.004, -0.6, 0.6);

      if(dist < 14){
        // Arrived at doc
        ch.depth = yToDepth(ch.y);
        setChibiState('picking_up');
      } else {
        const step = Math.min(dist, CHIBI_SPEED * dt);
        ch.x += (dx/dist)*step;
        ch.y += (dy/dist)*step;
        ch.depth = yToDepth(ch.y);
      }
      break;
    }

    case 'picking_up': {
      ch.emotion = 'annoyed';
      if(ch.stateTime > 350){
        ch.holdingDoc = true;
        ch.holdDocType = currentDoc ? currentDoc.type : 0;
        currentDoc = null;

        // Decide throw mode
        ch.throwMode = THROW_PATTERN[docsThrown % THROW_PATTERN.length];

        if(ch.throwMode === 2){
          // Carry to bin
          setChibiState('running_to_bin');
          ch.facingRight = trashBin.x > ch.x;
        } else {
          // Distant throw (hand=0) or kick (1) from current position
          setChibiState('throwing');
          ch.throwAnim = 0;
          ch.facingRight = trashBin.x > ch.x;
        }
      }
      break;
    }

    case 'running_to_bin': {
      ch.legPhase += dt*0.02;
      ch.emotion = 'annoyed';
      // Walk to near the bin (bin is at floor+12, depth≈0)
      const stopX = trashBin.x - trashBin.w * 0.8;
      const stopY = trashBin.y + 5;
      const dx = stopX - ch.x;
      const dy = stopY - ch.y;
      const dist = Math.sqrt(dx*dx + dy*dy);
      ch.facingRight = dx > 0;
      ch.headTilt = clamp(dx*0.003, -0.5, 0.5);

      if(dist < 14){
        ch.depth = yToDepth(ch.y);
        setChibiState('throwing');
        ch.throwAnim = 0;
        ch.facingRight = true;
      } else {
        const step = Math.min(dist, CHIBI_SPEED * dt);
        ch.x += (dx/dist)*step;
        ch.y += (dy/dist)*step;
        ch.depth = yToDepth(ch.y);
      }
      break;
    }

    case 'throwing': {
      ch.emotion = 'annoyed';
      ch.throwAnim = Math.min(ch.throwAnim + dt*0.003, 1);

      // Launch flying doc at animation peak
      if(ch.throwAnim > 0.4 && ch.holdingDoc && !flyingDoc){
        ch.holdingDoc = false;
        const sc = getChibiDrawSize();
        const dir = ch.facingRight ? 1 : -1;
        let handX, handY;

        if(ch.throwMode === 1){
          // kick — doc launches from foot area
          handX = ch.x + dir * sc * 0.5;
          handY = ch.y + sc * 0.15;
        } else {
          // hand throw
          handX = ch.x + dir * sc * 0.45;
          handY = ch.y - sc * 0.3;
        }

        const dist = Math.abs(trashBin.x - ch.x);
        flyingDoc = {
          x: handX, y: handY,
          startX: handX, startY: handY,
          targetX: trashBin.x,
          targetY: trashBin.y - trashBin.h * 0.1,
          t: 0,
          type: ch.holdDocType,
          size: 18,
          rotation: 0,
          // Bigger arc for distant throws, shorter for close
          arcHeight: ch.throwMode === 2 ? 40 : 60 + dist * 0.2,
          speed: ch.throwMode === 2 ? 0.004 : 0.0022,
        };
      }

      if(ch.throwAnim >= 1){
        setChibiState('wait_for_arc');
      }
      break;
    }

    case 'wait_for_arc': {
      ch.emotion = 'annoyed';
      if(flyingDoc){
        ch.headTilt = clamp((flyingDoc.x - ch.x)*0.005, -0.8, 0.8);
      }
      if(!flyingDoc){
        docsThrown++;
        setChibiState('walking_back');
      }
      break;
    }

    case 'walking_back': {
      ch.legPhase += dt*0.015;
      ch.emotion = 'annoyed';
      // Walk back to center at floor level (depth=0)
      const restX = getFloorRestX();
      const restY = floorY + 8;
      const dx = restX - ch.x;
      const dy = restY - ch.y;
      const dist = Math.sqrt(dx*dx + dy*dy);
      ch.facingRight = dx > 0;

      if(dist < 20){
        ch.depth = 0;
        ch.y = floorY + 8;
        setChibiState('idle_on_floor');
      } else {
        const step = Math.min(dist, CHIBI_SPEED * 0.7 * dt);
        ch.x += (dx/dist)*step;
        ch.y += (dy/dist)*step;
        ch.depth = yToDepth(ch.y);
      }
      break;
    }

    case 'idle_on_floor': {
      ch.y = floorY + 8;
      ch.depth = 0;
      ch.headPhase += dt*0.004;
      ch.headTilt = Math.sin(ch.headPhase)*0.7;
      ch.emotion = 'annoyed';
      break;
    }

    case 'climbing': {
      ch.emotion = 'happy';
      ch.legPhase += dt*0.015;
      const pos = getImagePos();
      const dx = pos.x - ch.x;
      const dy = pos.y - ch.y;
      const dist = Math.sqrt(dx*dx + dy*dy);
      ch.facingRight = dx > 0;

      if(dist < 8){
        ch.x = pos.x; ch.y = pos.y;
        setChibiState('happy_on_image');
      } else {
        const step = Math.min(dist, CHIBI_SPEED*0.7*dt);
        ch.x += (dx/dist)*step;
        ch.y += (dy/dist)*step;
      }
      break;
    }

    case 'happy_on_image': {
      const pos = getImagePos();
      ch.x = pos.x; ch.y = pos.y;
      ch.emotion = 'happy';
      ch.headPhase += dt*0.002;
      ch.headTilt = Math.sin(ch.headPhase)*0.3;
      break;
    }
  }
}

/* ─── DRAW CHIBI ─────────────────────────────────────── */
function drawChibi(t){
  const ch = chibi;
  const s = getChibiDrawSize();
  const x = ch.x, y = ch.y;

  ctx.save();
  ctx.translate(x, y);
  if(!ch.facingRight) ctx.scale(-1,1);

  const alpha = 0.35;
  const headR = s*0.38;
  const bodyH = s*0.34;
  const bodyW = s*0.42;

  // Shadow
  ctx.beginPath();
  ctx.ellipse(0, s*0.2, s*0.32, s*0.05, 0, 0, Math.PI*2);
  ctx.fillStyle = c(0.06);
  ctx.fill();

  // Legs
  const legSp = s*0.14;
  const legLen = s*0.25;
  let la1=0, la2=0;
  if(['running_to_doc','running_to_bin','climbing','walking_back'].includes(ch.state)){
    la1 = Math.sin(ch.legPhase)*0.65;
    la2 = Math.sin(ch.legPhase+Math.PI)*0.65;
  } else if(ch.state==='throwing' && ch.throwMode===1){
    // kick animation — big leg swing
    la1=-0.2;
    la2 = Math.sin(clamp(ch.throwAnim*1.5,0,1)*Math.PI)*1.4;
  } else if(ch.state==='picking_up'){
    la1 = -0.15; la2 = 0.15;
  }
  ctx.strokeStyle = c(alpha);
  ctx.lineWidth = s*0.065;
  ctx.lineCap = 'round';
  [[-1,la1],[1,la2]].forEach(([side,ang])=>{
    const ox = side*legSp;
    const ex = ox + Math.sin(ang)*legLen;
    const ey = bodyH*0.32 + Math.cos(ang)*legLen;
    ctx.beginPath(); ctx.moveTo(ox,bodyH*0.32); ctx.lineTo(ex,ey); ctx.stroke();
    ctx.beginPath(); ctx.arc(ex+1.5,ey,s*0.035,0,Math.PI*2);
    ctx.fillStyle=c(alpha); ctx.fill();
  });

  // Body
  ctx.beginPath();
  roundRect(ctx, -bodyW/2, -bodyH/2, bodyW, bodyH, s*0.09);
  ctx.fillStyle = c(0.09);
  ctx.fill();
  ctx.strokeStyle = c(alpha);
  ctx.lineWidth = s*0.04;
  ctx.stroke();

  // Arms
  const armLen = s*0.32;
  let aL=-0.3, aR=0.3;
  if(ch.state==='on_image'||ch.state==='happy_on_image'){
    aL = -0.5 + Math.sin(t*0.001)*0.06;
    aR = -0.4 + Math.sin(t*0.001+1.5)*0.06;
  } else if(ch.state==='picking_up'){
    aL = 1.0; aR = 1.0;
  } else if(ch.state==='running_to_bin' && ch.holdingDoc){
    aL = 0.3; aR = -0.8;
  } else if(ch.state==='throwing'){
    if(ch.throwMode===0){
      // distant hand throw — big wind-up arc
      aR = -1.8 + ch.throwAnim*3.6; aL=0.3;
    } else if(ch.throwMode===1){
      // distant kick — arms out for balance
      aL=-0.7; aR=0.7;
    } else {
      // carry throw near bin — quick toss
      aR = -1.2 + ch.throwAnim*2.8; aL=0.2;
    }
  } else if(ch.state==='looking_down'||ch.state==='falling_off'){
    aL = 0.8; aR = 0.8;
  } else if(['running_to_doc','climbing','walking_back'].includes(ch.state)){
    aL = Math.sin(ch.legPhase+Math.PI)*0.5;
    aR = Math.sin(ch.legPhase)*0.5;
  }

  ctx.strokeStyle = c(alpha);
  ctx.lineWidth = s*0.055;
  [[-1,aL,-bodyW*0.42],[1,aR,bodyW*0.42]].forEach(([side,ang,ox])=>{
    const ex = ox + Math.sin(ang)*armLen;
    const ey = -bodyH*0.1 + Math.cos(ang)*armLen;
    ctx.beginPath(); ctx.moveTo(ox,-bodyH*0.1); ctx.lineTo(ex,ey); ctx.stroke();
    ctx.beginPath(); ctx.arc(ex,ey,s*0.03,0,Math.PI*2);
    ctx.fillStyle=c(alpha); ctx.fill();
  });

  // Doc in hand
  if(ch.holdingDoc){
    let dx2, dy2;
    if(ch.state==='running_to_bin'){
      dx2 = bodyW*0.42 + Math.sin(-0.8)*armLen;
      dy2 = -bodyH*0.1 + Math.cos(-0.8)*armLen;
    } else if(ch.state==='throwing' && ch.throwAnim <= 0.4){
      if(ch.throwMode===1){
        // kick — doc at foot level
        dx2 = s*0.3;
        dy2 = bodyH*0.32 + legLen*0.6;
      } else {
        dx2 = bodyW*0.42 + Math.sin(aR)*armLen;
        dy2 = -bodyH*0.1 + Math.cos(aR)*armLen;
      }
    }
    if(dx2 !== undefined){
      drawMiniDoc(dx2, dy2, s*0.24, ch.holdDocType);
    }
  }

  // Head
  const headY = -bodyH*0.52 - headR*0.7;
  ctx.save();
  ctx.translate(0, headY);
  ctx.rotate(ch.headTilt*0.16);

  ctx.beginPath(); ctx.arc(0,0,headR*1.1,0,Math.PI*2);
  ctx.fillStyle=c(0.025); ctx.fill();

  ctx.beginPath(); ctx.arc(0,0,headR,0,Math.PI*2);
  ctx.fillStyle=c(0.08); ctx.fill();
  ctx.strokeStyle=c(alpha); ctx.lineWidth=s*0.04; ctx.stroke();

  // Eyes
  const eyeY = -headR*0.05;
  const eyeSp = headR*0.36;
  const eyeR = headR*0.11;

  if(ch.isBlinking){
    ctx.strokeStyle=c(0.55); ctx.lineWidth=1.3;
    ctx.beginPath(); ctx.moveTo(-eyeSp-eyeR,eyeY); ctx.lineTo(-eyeSp+eyeR,eyeY); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(eyeSp-eyeR,eyeY); ctx.lineTo(eyeSp+eyeR,eyeY); ctx.stroke();
  } else {
    const eR = ch.emotion==='shocked' ? eyeR*1.3 : eyeR;
    ctx.fillStyle = c(ch.emotion==='shocked' ? 0.8 : 0.6);
    ctx.beginPath(); ctx.arc(-eyeSp,eyeY,eR,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.arc(eyeSp,eyeY,eR,0,Math.PI*2); ctx.fill();
    ctx.fillStyle='rgba(255,255,255,0.2)';
    ctx.beginPath(); ctx.arc(-eyeSp-eyeR*0.3,eyeY-eyeR*0.3,eyeR*0.3,0,Math.PI*2); ctx.fill();
    ctx.beginPath(); ctx.arc(eyeSp-eyeR*0.3,eyeY-eyeR*0.3,eyeR*0.3,0,Math.PI*2); ctx.fill();
  }

  // Mouth
  if(ch.emotion==='happy'){
    ctx.beginPath();
    ctx.arc(0, headR*0.3, headR*0.2, 0.1*Math.PI, 0.9*Math.PI);
    ctx.strokeStyle=c(0.45); ctx.lineWidth=s*0.03; ctx.stroke();
  } else if(ch.emotion==='shocked'){
    ctx.beginPath();
    ctx.arc(0, headR*0.38, headR*0.1, 0, Math.PI*2);
    ctx.strokeStyle=c(0.4); ctx.lineWidth=s*0.025; ctx.stroke();
  } else {
    ctx.beginPath();
    ctx.arc(0, headR*0.42, headR*0.17, Math.PI*0.15, Math.PI*0.85, true);
    ctx.strokeStyle=c(0.4); ctx.lineWidth=s*0.03; ctx.stroke();
  }

  // Eyebrows
  if(ch.emotion==='annoyed'){
    ctx.strokeStyle=c(0.35); ctx.lineWidth=s*0.025;
    ctx.beginPath(); ctx.moveTo(-eyeSp-eyeR,eyeY-eyeR*1.7); ctx.lineTo(-eyeSp+eyeR*0.5,eyeY-eyeR*2.1); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(eyeSp+eyeR,eyeY-eyeR*1.7); ctx.lineTo(eyeSp-eyeR*0.5,eyeY-eyeR*2.1); ctx.stroke();
  } else if(ch.emotion==='shocked'){
    ctx.strokeStyle=c(0.35); ctx.lineWidth=s*0.025;
    ctx.beginPath(); ctx.moveTo(-eyeSp-eyeR,eyeY-eyeR*2.3); ctx.lineTo(-eyeSp+eyeR,eyeY-eyeR*2.3); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(eyeSp-eyeR,eyeY-eyeR*2.3); ctx.lineTo(eyeSp+eyeR,eyeY-eyeR*2.3); ctx.stroke();
  }

  ctx.restore(); // head
  ctx.restore(); // body
}

function roundRect(ctx,x,y,w,h,r){
  ctx.moveTo(x+r,y); ctx.lineTo(x+w-r,y);
  ctx.quadraticCurveTo(x+w,y,x+w,y+r); ctx.lineTo(x+w,y+h-r);
  ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h); ctx.lineTo(x+r,y+h);
  ctx.quadraticCurveTo(x,y+h,x,y+h-r); ctx.lineTo(x,y+r);
  ctx.quadraticCurveTo(x,y,x+r,y);
}

/* ─── TRASH BIN ──────────────────────────────────────── */
function initTrashBin(){
  // Always visible — on mobile push it more toward center
  const mobile = IS_MOBILE();
  trashBin = {
    x: cssW * (mobile ? 0.75 : 0.86),
    y: floorY + 12,
    w: mobile ? 28 : 42,
    h: mobile ? 35 : 52,
  };
}

function drawTrashBin(){
  const tb=trashBin, x=tb.x, y=tb.y, w=tb.w, h=tb.h;
  ctx.save(); ctx.translate(x,y);

  ctx.beginPath();
  ctx.moveTo(-w*0.5,0); ctx.lineTo(-w*0.38,h); ctx.lineTo(w*0.38,h); ctx.lineTo(w*0.5,0);
  ctx.closePath();
  ctx.fillStyle=c(0.07); ctx.fill();
  ctx.strokeStyle=c(0.25); ctx.lineWidth=1.3; ctx.stroke();

  for(let i=-1;i<=1;i++){
    ctx.beginPath();
    ctx.moveTo(i*w*0.14,h*0.1); ctx.lineTo(i*w*0.11,h*0.88);
    ctx.strokeStyle=c(0.1); ctx.lineWidth=0.6; ctx.stroke();
  }

  ctx.beginPath();
  ctx.moveTo(-w*0.56,0); ctx.lineTo(w*0.56,0);
  ctx.lineTo(w*0.5,-h*0.1); ctx.lineTo(-w*0.5,-h*0.1); ctx.closePath();
  ctx.fillStyle=c(0.1); ctx.fill();
  ctx.strokeStyle=c(0.25); ctx.lineWidth=1.2; ctx.stroke();

  ctx.beginPath();
  ctx.moveTo(-w*0.1,-h*0.1); ctx.lineTo(-w*0.07,-h*0.18);
  ctx.lineTo(w*0.07,-h*0.18); ctx.lineTo(w*0.1,-h*0.1);
  ctx.strokeStyle=c(0.25); ctx.lineWidth=1.2; ctx.stroke();

  for(let i=0;i<3;i++){
    ctx.save();
    ctx.translate(i*5-5, -h*0.06-i*3);
    ctx.rotate((i-1)*0.3);
    drawMiniDoc(0,0,13,i%3);
    ctx.restore();
  }

  ctx.save(); ctx.translate(w*0.7,h*0.75); ctx.rotate(0.3); drawMiniDoc(0,0,10,0); ctx.restore();
  ctx.save(); ctx.translate(-w*0.6,h*0.9); ctx.rotate(-0.2); drawMiniDoc(0,0,10,2); ctx.restore();

  ctx.restore();
}

/* ─── MINI DOCUMENT ──────────────────────────────────── */
function drawMiniDoc(x,y,size,type){
  const colors = ['rgba(220,38,38,0.45)','rgba(37,99,235,0.45)','rgba(22,163,74,0.45)'];
  ctx.save(); ctx.translate(x,y);

  ctx.beginPath(); ctx.rect(-size*0.4,-size*0.5,size*0.8,size);
  ctx.fillStyle='rgba(241,245,249,0.1)'; ctx.fill();
  ctx.strokeStyle=c(0.2); ctx.lineWidth=0.7; ctx.stroke();

  const cs=size*0.18;
  ctx.beginPath();
  ctx.moveTo(size*0.4-cs,-size*0.5); ctx.lineTo(size*0.4,-size*0.5+cs);
  ctx.lineTo(size*0.4-cs,-size*0.5+cs); ctx.closePath();
  ctx.fillStyle=c(0.1); ctx.fill();

  ctx.fillStyle=colors[type]||colors[0];
  ctx.fillRect(-size*0.4,size*0.28,size*0.8,size*0.22);

  ctx.strokeStyle=c(0.08); ctx.lineWidth=0.4;
  for(let i=0;i<3;i++){
    const ly = -size*0.25+i*size*0.17;
    ctx.beginPath(); ctx.moveTo(-size*0.22,ly); ctx.lineTo(size*0.12+i*1.5,ly); ctx.stroke();
  }
  ctx.restore();
}

/* ─── FALLING DOC ────────────────────────────────────── */
function getDocFallSpeed(){
  const fallDist = floorY + 30;
  return fallDist / 3000;
}

function spawnDoc(){
  const speed = getDocFallSpeed();
  // Vary landing depth — some near (floorY+8), some far (floorY + 60% of zone)
  const zone = floorBottom - floorY;
  const landDepth = rand(0.02, 0.55); // 0=near, 0.55=deep
  const landY = floorY + landDepth * zone;

  currentDoc = {
    x: rand(cssW*0.12, cssW*0.58),
    y: -30,
    vy: speed,
    vx: rand(-0.01,0.01),
    rotation: rand(-0.3,0.3),
    rotSpeed: rand(-0.002,0.002),
    size: rand(20,26),
    type: Math.floor(rand(0,3)),
    state: 'falling',
    landY: landY,
    sway: rand(0,100),
    depth: landDepth,
  };
}

function updateDoc(t,dt){
  if(!currentDoc || currentDoc.state!=='falling') return;
  const d = currentDoc;
  d.y += d.vy*dt;
  d.x += d.vx*dt;
  d.rotation += d.rotSpeed*dt;
  d.x += Math.sin(t*0.0007+d.sway)*0.05;

  if(d.y >= d.landY){
    d.y = d.landY;
    d.state = 'landed';
  }
}

function drawDoc(){
  if(!currentDoc) return;
  const sc = depthScale(currentDoc.depth || 0);
  ctx.save();
  ctx.translate(currentDoc.x, currentDoc.y);
  ctx.rotate(currentDoc.rotation);
  drawMiniDoc(0,0, currentDoc.size * sc, currentDoc.type);
  ctx.restore();
}

/* ─── FLYING DOC (arc to bin) ────────────────────────── */
function updateFlyingDoc(dt){
  if(!flyingDoc) return;
  const spd = flyingDoc.speed || 0.003;
  flyingDoc.t += dt * spd;
  flyingDoc.rotation += dt*0.012;

  const t2 = clamp(flyingDoc.t,0,1);
  const ease = t2<0.5 ? 2*t2*t2 : 1-Math.pow(-2*t2+2,2)/2;
  flyingDoc.x = lerp(flyingDoc.startX, flyingDoc.targetX, ease);
  const arcH = flyingDoc.arcHeight || 90;
  flyingDoc.y = lerp(flyingDoc.startY, flyingDoc.targetY, ease) - Math.sin(t2*Math.PI)*arcH;

  // Scale shrinks as doc approaches bin (depth changes)
  flyingDoc.drawScale = lerp(1, 0.85, ease);

  if(flyingDoc.t >= 1){
    flyingDoc = null;
  }
}

function drawFlyingDoc(){
  if(!flyingDoc) return;
  const sc = flyingDoc.drawScale || 1;
  ctx.save();
  ctx.translate(flyingDoc.x, flyingDoc.y);
  ctx.rotate(flyingDoc.rotation);
  drawMiniDoc(0,0, flyingDoc.size * sc, flyingDoc.type);
  ctx.restore();
}

/* ─── DESKS ──────────────────────────────────────────── */
function initDesks(){
  const w=cssW, zone=floorBottom-floorY;
  desks=[];
  const positions=[
    // Left side
    {x:w*0.06, y:floorY+zone*0.10},
    {x:w*0.20, y:floorY+zone*0.38},
    {x:w*0.10, y:floorY+zone*0.62},
    // Right side
    {x:w*0.70, y:floorY+zone*0.12},
    {x:w*0.60, y:floorY+zone*0.44},
    {x:w*0.75, y:floorY+zone*0.68},
  ];
  for(const pos of positions){
    const dr = (pos.y-floorY)/zone;
    desks.push({x:pos.x, y:pos.y, scale:0.5+dr*0.5});
  }
}

function drawDesks(){
  // Sort by Y so far desks drawn first (painter's algo)
  const sorted = [...desks].sort((a,b) => a.y - b.y);
  for(const desk of sorted){
    ctx.save(); ctx.translate(desk.x,desk.y);
    const sc=desk.scale;
    const dw=70*sc, dh=9*sc, legH=28*sc;
    const alph = 0.12;

    ctx.beginPath(); ctx.rect(-dw/2,0,dw,dh);
    ctx.fillStyle=c(0.04); ctx.fill();
    ctx.strokeStyle=c(alph); ctx.lineWidth=0.9; ctx.stroke();

    ctx.strokeStyle=c(alph*0.8); ctx.lineWidth=1.5*sc;
    ctx.beginPath();
    ctx.moveTo(-dw/2+4*sc,dh); ctx.lineTo(-dw/2+4*sc,dh+legH);
    ctx.moveTo(dw/2-4*sc,dh); ctx.lineTo(dw/2-4*sc,dh+legH);
    ctx.stroke();

    const mw=20*sc, mh=15*sc;
    ctx.beginPath(); ctx.rect(-mw/2,-mh,mw,mh);
    ctx.fillStyle=c(0.03); ctx.fill();
    ctx.strokeStyle=c(alph); ctx.lineWidth=0.7; ctx.stroke();

    ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(0,-2);
    ctx.strokeStyle=c(alph*0.8); ctx.lineWidth=2*sc; ctx.stroke();

    const cx2=dw*0.3;
    ctx.beginPath();
    ctx.ellipse(cx2,dh+legH*0.35,9*sc,2.5*sc,0,0,Math.PI*2);
    ctx.fillStyle=c(0.03); ctx.fill();
    ctx.strokeStyle=c(alph*0.7); ctx.lineWidth=0.8; ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(cx2-7*sc,dh+legH*0.35-2*sc);
    ctx.quadraticCurveTo(cx2,dh+legH*0.35-18*sc,cx2+7*sc,dh+legH*0.35-2*sc);
    ctx.strokeStyle=c(alph*0.7); ctx.lineWidth=1; ctx.stroke();

    ctx.restore();
  }
}

/* ─── PHASE MANAGEMENT ───────────────────────────────── */
function updatePhase(now, dt){
  const elapsed = now - phaseStart;

  switch(phase){
    case 'first_idle':
      if(elapsed > 2000){
        phase = 'active'; phaseStart = now; docsThrown = 0;
        spawnDoc();
        setChibiState('looking_down');
      }
      break;

    case 'active': {
      const ready = !currentDoc && !flyingDoc && chibi.state === 'idle_on_floor';
      if(ready){
        if(elapsed > ACTIVE_DURATION){
          phase = 'climbing'; phaseStart = now;
          setChibiState('climbing');
          break;
        }
        if(chibi.stateTime > 1500){
          spawnDoc();
          setChibiState('wait_for_land');
        }
      }
      break;
    }

    case 'climbing':
      if(chibi.state === 'happy_on_image'){
        phase = 'happy'; phaseStart = now;
      }
      break;

    case 'happy':
      if(elapsed > HAPPY_DURATION){
        phase = 'active'; phaseStart = now; docsThrown = 0;
        spawnDoc();
        setChibiState('looking_down');
      }
      break;
  }
}

/* ─── MAIN LOOP ──────────────────────────────────────── */
function loop(t){
  const dt = prevTime ? Math.min(t-prevTime,50) : 16;
  prevTime = t;
  ctx.clearRect(0,0,cssW,cssH);

  drawGrid();
  if(!IS_MOBILE()) drawDesks();
  drawDoc();
  drawFlyingDoc();
  drawTrashBin();
  drawChibi(t);

  updateDoc(t,dt);
  updateFlyingDoc(dt);
  updateChibi(dt);
  updatePhase(t,dt);

  animFrame = requestAnimationFrame(loop);
}

/* ─── DEBUG ─────────────────────────────────────────── */
window._heroDebug = () => ({
  phase, elapsed: (performance.now()-phaseStart).toFixed(0),
  st: chibi?.state, stT: chibi?.stateTime?.toFixed(0),
  cx: chibi?.x?.toFixed(0), cy: chibi?.y?.toFixed(0),
  cDepth: chibi?.depth?.toFixed(2),
  hold: chibi?.holdingDoc, mode: chibi?.throwMode,
  doc: !!currentDoc, docSt: currentDoc?.state,
  docY: currentDoc?.y?.toFixed(0), docLandY: currentDoc?.landY?.toFixed(0),
  fly: !!flyingDoc,
  flY: floorY?.toFixed(0), flB: floorBottom?.toFixed(0),
  thrown: docsThrown,
});

/* ─── START ──────────────────────────────────────────── */
if(document.readyState==='loading')
  document.addEventListener('DOMContentLoaded',()=>setTimeout(init,500));
else setTimeout(init,500);

})();
