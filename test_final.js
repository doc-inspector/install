
if (typeof gsap !== 'undefined') {
  if (typeof ScrollTrigger !== 'undefined') {
    gsap.registerPlugin(ScrollTrigger);
  }

  // Entrance animations
  gsap.from('.gsap-fade', { opacity:0, y:30, stagger:.15, duration:.9, ease:'power3.out' });

  // Disable CSS transitions during animation to prevent rendering conflicts
  gsap.set('.gsap-card', { transition: 'none' });
  gsap.from('.gsap-card', {
    opacity:0,
    y:40,
    stagger:.1,
    duration:.7,
    ease:'power3.out',
    delay:.4,
    onComplete: function() {
      // Restore CSS transitions after animation finishes
      gsap.set('.gsap-card', { clearProps: 'transition' });
    }
  });

  // Scroll animations for security items
  if (typeof ScrollTrigger !== 'undefined') {
    gsap.utils.toArray('.sec-item.reveal').forEach((el, i) => {
      gsap.fromTo(el,
        { opacity:0, y:30 },
        { opacity:1, y:0, duration:.7, ease:'power3.out', delay:i*.08,
          scrollTrigger:{ trigger:el, start:'top 85%' }
        }
      );
    });
  }
}

// Tool metadata
const TOOLS = {
  sanitize : { label:'Sanitize Metadata',      emoji:'🧹' },
  watermark: { label:'Add Watermark',           emoji:'💧' },
  encrypt  : { label:'Encrypt PDF',             emoji:'🔐 ' },
  redact   : { label:'Find & Redact',           emoji:'⬛' },
  flatten  : { label:'Flatten to Image PDF',    emoji:'🖼️ ' },
  rebuild  : { label:'Rebuild & Repair PDF',    emoji:'🛠️ ' },
  bundle   : { label:'PDF Bundle Summary',      emoji:'📋' },
};
const selectedOps = new Set();
let files = [];
const MAX = 100;

// License & Limit state
let currentTier = "Free";
let currentLimit = 100;
let currentUsed = 0;

async function fetchStatus() {
  try {
    const res = await fetch('https://deeper-passage-rotation-universities.trycloudflare.com/api/auth/status', { headers: {'Bypass-Tunnel-Reminder': 'true'} });
    if (res.ok) {
      const data = await res.json();
      currentTier = data.tier;
      currentUsed = data.used_today;
      currentLimit = data.limit_today;
      updateUI();
      if(data.kicked_out) alert("License activated on another device. This session has been downgraded to Free.");
      if(data.revoked) alert("License revoked or expired. Downgraded to Free.");
    }
  } catch(e) {}
}

function updateUI() {
  const tb = document.getElementById('tier-badge');
  const dCnt = document.getElementById('dailyCnt');
  const dFill = document.getElementById('dailyFill');
  const lForm = document.getElementById('license-activate-form');
  const lInfo = document.getElementById('license-active-info');
  
  tb.textContent = currentTier;
  if (currentTier === "Free") {
    tb.style.color = "var(--text-muted)";
    tb.style.borderColor = "rgba(255,255,255,0.1)";
    tb.style.background = "rgba(255,255,255,0.05)";
    lForm.style.display = "block";
    lInfo.style.display = "none";
    const ub = document.getElementById("upsell-box");
    if(ub) ub.style.display = "block";
  } else if (currentTier === "Basic") {
    tb.style.color = "#34d399";
    tb.style.borderColor = "rgba(16,185,129,0.3)";
    tb.style.background = "rgba(16,185,129,0.1)";
    lForm.style.display = "none";
    lInfo.style.display = "block";
    const ub = document.getElementById("upsell-box");
    if(ub) ub.style.display = "none";
  } else {
    tb.style.color = "#f59e0b";
    tb.style.borderColor = "rgba(245,158,11,0.3)";
    tb.style.background = "rgba(245,158,11,0.1)";
    lForm.style.display = "none";
    lInfo.style.display = "block";
    const ub = document.getElementById("upsell-box");
    if(ub) ub.style.display = "none";
  }
  
  if (currentLimit === "unlimited") {
    dCnt.textContent = currentUsed + " / ∞";
    dFill.style.width = "0%";
  } else {
    dCnt.textContent = currentUsed + " / " + currentLimit + " files";
    dFill.style.width = Math.min((currentUsed / currentLimit) * 100, 100) + '%';
  }
  
  // Update visually locked cards
  const proFeatures = ['redact', 'flatten'];
  proFeatures.forEach(op => {
    const card = document.getElementById('card-' + op);
    if (!card) return;
    if (currentTier === "Free") {
      if (!card.querySelector('.pro-lock')) {
        const lock = document.createElement('div');
        lock.className = 'pro-lock';
        lock.innerHTML = '<span style="background:rgba(239,68,68,.15);border:1px solid rgba(239,68,68,.3);color:#f87171;font-size:.65rem;font-weight:800;padding:.2rem .45rem;border-radius:4px;position:absolute;top:12px;right:12px;letter-spacing:.05em">PRO</span>';
        card.appendChild(lock);
      }
      card.style.opacity = "0.6";
      card.style.pointerEvents = "none";
    } else {
      const lock = card.querySelector('.pro-lock');
      if (lock) lock.remove();
      card.style.opacity = "1";
      card.style.pointerEvents = "auto";
    }
  });
}

async function activateLicense() {
  const key = document.getElementById('license-key-input').value.trim();
  const msg = document.getElementById('license-msg');
  const btn = document.getElementById('activate-btn');
  if (!key) return;
  
  btn.disabled = true;
  btn.innerHTML = '<div class="spin" style="width:16px;height:16px;border-width:2px;margin:0"></div> Activating...';
  msg.style.display = "none";
  
  const fd = new FormData();
  fd.append("license_key", key);
  
  try {
    const res = await fetch('https://deeper-passage-rotation-universities.trycloudflare.com/api/auth/activate', { method: 'POST', body: fd, headers: {'Bypass-Tunnel-Reminder': 'true'} });
    const data = await res.json();
    if (res.ok) {
      msg.style.display = "block";
      msg.style.color = "#34d399";
      msg.textContent = "Activated successfully!";
      await fetchStatus();
    } else {
      msg.style.display = "block";
      msg.style.color = "#f87171";
      msg.textContent = data.error || "Invalid key.";
    }
  } catch(e) {
    msg.style.display = "block";
    msg.style.color = "#f87171";
    msg.textContent = "Network error. Is the backend running?";
  }
  
  btn.disabled = false;
  btn.textContent = "Activate Key";
}

async function logoutLicense() {
  await fetch('https://deeper-passage-rotation-universities.trycloudflare.com/api/auth/logout', { headers: {'Bypass-Tunnel-Reminder': 'true'}, method: 'POST' });
  await fetchStatus();
}

// Initial fetch on load
fetchStatus();

// Ripple effect
function addRipple(e, el) {
  const r = document.createElement('span');
  r.className = 'ripple';
  const rect = el.getBoundingClientRect();
  const s = Math.max(rect.width, rect.height) * 2;
  r.style.cssText = 'width:'+s+'px;height:'+s+'px;left:'+(e.clientX-rect.left-s/2)+'px;top:'+(e.clientY-rect.top-s/2)+'px';
  el.appendChild(r);
  setTimeout(() => r.remove(), 600);
}

function toggleTool(e, name) {
  const card = document.getElementById('card-' + name);
  addRipple(e, card);
  const opts = document.getElementById('opts-' + name);

  // Bundle is exclusive — deselect other tools
  if (name === 'bundle') {
    if (selectedOps.has('bundle')) {
      selectedOps.delete('bundle');
      card.classList.remove('selected');
    } else {
      // Deselect everything else first
      selectedOps.forEach(op => {
        const c = document.getElementById('card-' + op);
        if (c) c.classList.remove('selected');
        const o = document.getElementById('opts-' + op);
        if (o) o.classList.remove('open');
      });
      selectedOps.clear();
      selectedOps.add('bundle');
      card.classList.add('selected');
      gsap.from('#card-bundle', { scale:.97, duration:.3, ease:'back.out(2)' });
    }
  } else {
    // Deselect bundle if switching to regular tools
    if (selectedOps.has('bundle')) {
      selectedOps.delete('bundle');
      const bc = document.getElementById('card-bundle');
      if (bc) bc.classList.remove('selected');
    }
    if (selectedOps.has(name)) {
      selectedOps.delete(name);
      card.classList.remove('selected');
      if (opts) opts.classList.remove('open');
    } else {
      selectedOps.add(name);
      card.classList.add('selected');
      if (opts) opts.classList.add('open');
      gsap.from('#card-' + name, { scale:.97, duration:.3, ease:'back.out(2)' });
    }
  }

    if (selectedOps.has('bundle')) {
      // Remove PRO lock for bundle since we allow bundle with Free (it is max 15MB)
      fi.setAttribute('webkitdirectory', '');
      fi.setAttribute('multiple', '');
      fi.removeAttribute('accept');
      dzIcon.textContent  = '📁';
      dzTitle.textContent = 'Drag a FOLDER here (up to 100 PDFs)';
      dzSub.textContent   = 'or click to browse folder — max 100 files — 15 MB each';
      dz.style.borderColor = 'rgba(245,158,11,.4)';
      dz.style.background  = 'rgba(245,158,11,.02)';
    } else {
      fi.removeAttribute('webkitdirectory');
      fi.setAttribute('accept', '.pdf');
      dzIcon.textContent  = '📂';
      dzTitle.textContent = 'Drag & Drop PDF files here';
      const maxSz = currentTier === "Free" ? "15" : "50";
      dzSub.textContent   = 'or click to browse — max ' + currentLimit + ' files per day — ' + maxSz + ' MB each';
      dz.style.borderColor = '';
      dz.style.background  = '';
    }
    // Clear file list when switching modes
    // files = []; renderFiles();

  updateSidebar();
  updateBtn();
}

function updateSidebar() {
  const list = document.getElementById('opsList');
  const ps   = document.getElementById('pipelineSection');
  const pf   = document.getElementById('pipelineFlow');
  if (!selectedOps.size) {
    list.innerHTML = '<div class="ops-empty">No operations selected yet.<br>Pick tools from the left.</div>';
    ps.style.display = 'none';
    return;
  }
  list.innerHTML = [...selectedOps].map(op => {
    const m = TOOLS[op];
    return '<div class="op-chip"><span>'+m.emoji+'</span><span class="op-chip-name">'+m.label+'</span>'
      + '<button class="op-chip-remove" onclick="toggleTool(event,\''+op+'\')" title="Remove">✕</button></div>';
  }).join('');
  ps.style.display = 'block';
  
  // Construct a premium vertical pipeline tree instead of messy horizontal tags
  const nodes = [
    { label: 'Input PDF Files', emoji: '📄', desc: 'Uploaded & ready' },
    ...[...selectedOps].map(op => ({
      label: TOOLS[op].label,
      emoji: TOOLS[op].emoji,
      desc: 'Pipeline active stage'
    })),
    { label: 'Ready for Download', emoji: '✅', desc: 'Processed output package' }
  ];

  const stepsHTML = nodes.map((node, i) => {
    let stateClass = 'pending';
    if (i === 0) {
      stateClass = 'completed';
    } else if (i === nodes.length - 1) {
      stateClass = 'pending';
    } else {
      stateClass = 'active';
    }

    return '<div class="pt-step ' + stateClass + '">'
      + '<div class="pt-icon-wrap">'
      + '<div class="pt-icon">' + node.emoji + '</div>'
      + (i < nodes.length - 1 ? '<div class="pt-line"></div>' : '')
      + '</div>'
      + '<div class="pt-content">'
      + '<div class="pt-label">' + node.label + '</div>'
      + '<div class="pt-desc">' + node.desc + '</div>'
      + '</div>'
      + '</div>';
  }).join('');
  
  pf.innerHTML = '<div class="pipeline-tree">' + stepsHTML + '</div>';
}


function updateBtn() {
  document.getElementById('processBtn').disabled = !(files.length > 0 && selectedOps.size > 0);
}

// Drop zone
const dz = document.getElementById('dropZone');
const fi = document.getElementById('fileInput');
dz.addEventListener('dragover',  e => { e.preventDefault(); dz.classList.add('over'); });
dz.addEventListener('dragleave', ()  => dz.classList.remove('over'));
dz.addEventListener('drop', async e => {
  e.preventDefault(); dz.classList.remove('over');
  if (e.dataTransfer.items) {
    const newFiles = await getFilesFromDataTransferItems(e.dataTransfer.items);
    addFiles(newFiles);
  } else {
    addFiles([...e.dataTransfer.files]);
  }
});
fi.addEventListener('change', () => { addFiles([...fi.files]); fi.value = ''; });


async function getFilesFromDataTransferItems(items) {
  const promises = [];
  for (let i = 0; i < items.length; i++) {
    const item = items[i];
    if (item.kind === 'file') {
      const entry = item.webkitGetAsEntry();
      if (entry) promises.push(traverseFileTree(entry));
    }
  }
  const nestedArrays = await Promise.all(promises);
  return nestedArrays.flat();
}
function traverseFileTree(item) {
  return new Promise((resolve) => {
    if (item.isFile) {
      item.file(file => resolve([file]));
    } else if (item.isDirectory) {
      const dirReader = item.createReader();
      dirReader.readEntries(async entries => {
        const promises = entries.map(entry => traverseFileTree(entry));
        const nestedFiles = await Promise.all(promises);
        resolve(nestedFiles.flat());
      });
    } else resolve([]);
  });
}

function addFiles(newFiles) {
  const CURRENT_MAX = currentTier === "Free" ? 100 : 1000;
  const maxSz = currentTier === "Free" ? 15 * 1024 * 1024 : 50 * 1024 * 1024;
  let skippedLimit = 0; let skippedSize = 0;
  
  newFiles.filter(f => f.name.toLowerCase().endsWith('.pdf')).forEach(f => {
    if (f.size > maxSz) { skippedSize++; return; }
    if (files.length >= CURRENT_MAX) { skippedLimit++; return; }
    if (!files.find(x => x.name === f.name && x.size === f.size)) files.push(f);
  });
  
  let msg = [];
  if (skippedLimit) msg.push(skippedLimit + " files ignored (max " + CURRENT_MAX + " reached).");
  if (skippedSize) msg.push(skippedSize + " files ignored (exceeded " + (maxSz/1024/1024) + "MB limit).");
  if (msg.length) alert(msg.join("\\n"));
  
  renderFiles(); updateBtn();
}
function removeFile(i) { files.splice(i, 1); renderFiles(); updateBtn(); }
function renderFiles() {
  const list  = document.getElementById('fileList');
  const icon  = document.getElementById('dzIcon');
  const title = document.getElementById('dzTitle');
  const sub   = document.getElementById('dzSub');
  if (!files.length) {
    list.innerHTML = '';
    icon.textContent  = '📂';
    title.textContent = 'Drag & Drop PDF files here';
    const maxSz = currentTier === "Free" ? "15" : "50";
    sub.textContent   = 'or click to browse — max ' + currentLimit + ' files per day — ' + maxSz + ' MB each';
    return;
  }
  icon.textContent  = '📋';
  title.textContent = files.length + ' file' + (files.length > 1 ? 's' : '') + ' selected';
  sub.textContent   = files.length >= MAX ? 'Maximum reached' : 'Click to add more';
  list.innerHTML = files.map((f, i) =>
    '<div class="file-item">📄 <span class="fi-name" title="'+f.name+'">'+f.name+'</span>'
    + '<span class="fi-size">'+(f.size/1024).toFixed(0)+' KB</span>'
    + '<button class="fi-remove" onclick="removeFile('+i+')" title="Remove">✕</button></div>'
  ).join('');
}

function gatherOptions() {
  return {
    watermarkText:    document.getElementById('wm-text')?.value    || 'CONFIDENTIAL',
    watermarkFont:    document.getElementById('wm-font')?.value    || 'Helvetica-Bold',
    watermarkSize:    document.getElementById('wm-size')?.value    || 60,
    watermarkOpacity: (parseInt(document.getElementById('wm-opacity')?.value || 15) / 100).toFixed(2),
    encryptUserPw:    document.getElementById('enc-pw')?.value     || '',
    encryptOwnerPw:   document.getElementById('enc-owner')?.value  || '',
    encryptNoPrint:   document.getElementById('enc-no-print')?.checked || false,
    encryptNoCopy:    document.getElementById('enc-no-copy')?.checked || false,
    encryptNoEdit:    document.getElementById('enc-no-edit')?.checked || false,
    encryptBits:      '256',
    redactKeywords:   document.getElementById('redact-kw')?.value  || '',
    sanitizeAuthor:   document.getElementById('san-author') ? document.getElementById('san-author').checked : true,
    sanitizeTime:     document.getElementById('san-time')   ? document.getElementById('san-time').checked   : true,
    sanitizeGps:      document.getElementById('san-gps')    ? document.getElementById('san-gps').checked    : true,
    sanitizeSoftware: document.getElementById('san-software')? document.getElementById('san-software').checked: true,
  };
}

async function startProcessing() {
  if (!files.length || !selectedOps.size) return;

  // Route bundle summary to its own endpoint
  if (selectedOps.has('bundle')) {
    await startBundleSummary();
    return;
  }

  // Validate encrypt
  if (selectedOps.has('encrypt')) {
    const pw  = document.getElementById('enc-pw').value;
    const pw2 = document.getElementById('enc-pw2').value;
    if (!pw)       { alert('Please enter an encryption password.'); return; }
    if (pw !== pw2){ alert('Passwords do not match.');              return; }
  }
  const ra = document.getElementById('resultArea');
  ra.classList.add('show');
  document.getElementById('rSpin').style.display  = 'block';
  document.getElementById('rIcon').style.display  = 'none';
  document.getElementById('rTitle').textContent   = 'Processing your files…';
  document.getElementById('rSub').textContent     = 'Pipeline: ' + [...selectedOps].join(' → ');
  document.getElementById('rDlBtn').style.display = 'none';
  document.getElementById('rDlBtn').textContent   = '';
  document.getElementById('rDlBtn').innerHTML     = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg> Download Results (.zip)';
  document.getElementById('rResetBtn').style.display = 'none';
  document.getElementById('processBtn').disabled  = true;
  ra.scrollIntoView({ behavior:'smooth', block:'center' });
  const fd = new FormData();
  files.forEach(f => fd.append('files[]', f));
  fd.append('operations', JSON.stringify([...selectedOps]));
  fd.append('options',    JSON.stringify(gatherOptions()));
  try {
    const resp = await fetch('https://deeper-passage-rotation-universities.trycloudflare.com/api/process', { method:'POST', body:fd, headers: {'Bypass-Tunnel-Reminder': 'true'} });
    if (!resp.ok) {
      let m = 'Server error.';
      try { const j = await resp.json(); m = j.error || m; } catch(_) {}
      throw new Error(m);
    }
    const blob = await resp.blob();
    const url  = URL.createObjectURL(blob);
    await fetchStatus(); // Refresh limit from server
    document.getElementById('rSpin').style.display   = 'none';
    document.getElementById('rIcon').style.display   = 'block';
    document.getElementById('rIcon').textContent     = '✅';
    document.getElementById('rTitle').textContent    = 'Processing Complete!';
    document.getElementById('rSub').textContent      = files.length + ' file' + (files.length > 1 ? 's' : '') + ' processed successfully';
    const dl = document.getElementById('rDlBtn');
    dl.download = 'DocInspector_Processed.zip'; dl.href = url; dl.style.display = 'inline-flex'; dl.click();
    document.getElementById('rResetBtn').style.display = 'inline-block';
  } catch(err) {
    document.getElementById('rSpin').style.display   = 'none';
    document.getElementById('rIcon').style.display   = 'block';
    document.getElementById('rIcon').textContent     = '❌';
    document.getElementById('rTitle').textContent    = 'Processing Failed';
    document.getElementById('rSub').textContent      = err.message || 'Make sure the local server is running (python server.py)';
    document.getElementById('processBtn').disabled   = false;
    document.getElementById('rResetBtn').style.display = 'inline-block';
  }
}

// Bundle Summary — calls /api/bundle-summary, returns ZIP with Excel+PDF+TXT
async function startBundleSummary() {
  const ra = document.getElementById('resultArea');
  ra.classList.add('show');
  document.getElementById('rSpin').style.display  = 'block';
  document.getElementById('rIcon').style.display  = 'none';
  document.getElementById('rTitle').textContent   = 'Generating Bundle Summary…';
  document.getElementById('rSub').textContent     = 'Extracting metadata, page counts & SHA-256 for each file';
  document.getElementById('rDlBtn').style.display = 'none';
  document.getElementById('rResetBtn').style.display = 'none';
  document.getElementById('processBtn').disabled  = true;
  ra.scrollIntoView({ behavior:'smooth', block:'center' });
  const fd = new FormData();
  files.forEach(f => fd.append('files[]', f));
  try {
    const resp = await fetch('https://deeper-passage-rotation-universities.trycloudflare.com/api/bundle-summary', { method:'POST', body:fd, headers: {'Bypass-Tunnel-Reminder': 'true'} });
    if (!resp.ok) {
      let m = 'Server error.';
      try { const j = await resp.json(); m = j.error || m; } catch(_) {}
      throw new Error(m);
    }
    const blob = await resp.blob();
    const url  = URL.createObjectURL(blob);
    await fetchStatus(); // Refresh limit from server
    document.getElementById('rSpin').style.display   = 'none';
    document.getElementById('rIcon').style.display   = 'block';
    document.getElementById('rIcon').textContent     = '📊';
    document.getElementById('rTitle').textContent    = 'Bundle Summary Ready!';
    document.getElementById('rSub').textContent      = 'Your ZIP contains: Excel report (2 sheets) + PDF + text summary';
    const dl = document.getElementById('rDlBtn');
    dl.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg> Download Bundle Summary (.zip)';
    dl.download = 'DocInspector_Processed.zip'; dl.href = url; dl.style.display = 'inline-flex'; dl.click();
    document.getElementById('rResetBtn').style.display = 'inline-block';
  } catch(err) {
    document.getElementById('rSpin').style.display   = 'none';
    document.getElementById('rIcon').style.display   = 'block';
    document.getElementById('rIcon').textContent     = '❌';
    document.getElementById('rTitle').textContent    = 'Bundle Summary Failed';
    document.getElementById('rSub').textContent      = err.message || 'Make sure the local server is running (python server.py)';
    document.getElementById('processBtn').disabled   = false;
    document.getElementById('rResetBtn').style.display = 'inline-block';
  }
}

function resetTool() {
  files = [];
  renderFiles(); updateBtn();
  document.getElementById('resultArea').classList.remove('show');
  document.getElementById('processBtn').disabled = false;
}

// Progress bar on scroll
window.addEventListener('scroll', () => {
  const el = document.getElementById('progress-bar');
  if (!el) return;
  const p = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;
  el.style.cssText = 'position:fixed;top:0;left:0;z-index:9999;height:2px;background:linear-gradient(90deg,var(--cyan),#818cf8);width:'+p+'%;transition:width .1s';
});

// Redact keyword tags manager
const redactKeywordsSet = new Set();
function updateRedactKeywordsHidden() {
  const hiddenInput = document.getElementById('redact-kw');
  if (hiddenInput) {
    hiddenInput.value = [...redactKeywordsSet].join(', ');
  }
  renderRedactTags();
}

function renderRedactTags() {
  const container = document.getElementById('kwTagsContainer');
  if (!container) return;
  if (redactKeywordsSet.size === 0) {
    container.innerHTML = '<span style="font-size:.78rem;color:var(--text-muted)">No keywords added yet. Search matches exact phrases.</span>';
    return;
  }
  container.innerHTML = [...redactKeywordsSet].map((kw, i) => {
    return '<span class="kw-tag" style="display:inline-flex;align-items:center;gap:.35rem;background:rgba(6,182,212,.12);border:1px solid rgba(6,182,212,.4);border-radius:6px;padding:.2rem .5rem;font-size:.78rem;color:#38bdf8;animation:ptFadeIn .2s ease">'
      + kw
      + '<button type="button" onclick="removeRedactKeyword(\'' + kw.replace(/'/g, "\\'") + '\')" style="background:none;border:none;color:#94a3b8;cursor:pointer;font-size:.8rem;padding:0;line-height:1" onmouseover="this.style.color=\'#f87171\'" onmouseout="this.style.color=\'#94a3b8\'">✕</button>'
      + '</span>';
  }).join('');
}

function addRedactKeywords() {
  const input = document.getElementById('redact-kw-input');
  if (!input) return;
  const val = input.value.trim();
  if (!val) return;
  
  // Split by comma in case they copy-paste a list
  val.split(',').forEach(item => {
    const clean = item.trim();
    if (clean) redactKeywordsSet.add(clean);
  });
  
  input.value = '';
  updateRedactKeywordsHidden();
}

function removeRedactKeyword(kw) {
  redactKeywordsSet.delete(kw);
  updateRedactKeywordsHidden();
}

document.addEventListener('DOMContentLoaded', () => {
  const addBtn = document.getElementById('btn-add-kw');
  const input = document.getElementById('redact-kw-input');
  if (addBtn && input) {
    addBtn.addEventListener('click', addRedactKeywords);
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        addRedactKeywords();
      }
    });
  }
  renderRedactTags();
});
