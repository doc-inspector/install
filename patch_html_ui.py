import re

files = [
    r"E:\Website online and local app new project\Public2\Public\en\tools-online.html",
    r"E:\Website online and local app new project\Public2\Public\ro\unelte-online.html",
    r"E:\Website online and local app new project\Public2\Public\ru\onlayn-instrumenty.html"
]

BRAND_COLORS = {
    'sanitize': '#f97316',
    'watermark': '#0ea5e9',
    'encrypt': '#8b5cf6',
    'redact': '#ef4444',
    'flatten': '#10b981',
    'rebuild': '#6366f1',
    'bundle': '#f59e0b'
}

PARTICLE_CSS = """
    #constellation-canvas {
      position: absolute; inset: 0; z-index: 0;
      pointer-events: none; opacity: 1; width: 100%; height: 100%;
    }
"""

PARTICLE_HTML_JS = """
  <!-- Constellation Particles -->
  <canvas id="constellation-canvas" aria-hidden="true"></canvas>
  <script>
  (function(){
    var c=document.getElementById('constellation-canvas');
    if(!c)return;
    var ctx=c.getContext('2d');
    var W,H,pts,RAF;
    var COLS=['6,182,212','99,102,241','16,185,129'];
    var N_BASE=55, CONNECT_DIST=160;
    var MOUSE={x:-999,y:-999};
    
    function resize(){
      var hero = document.querySelector('.tools-hero');
      W=c.width=hero ? hero.offsetWidth : window.innerWidth;
      H=c.height=hero ? hero.offsetHeight : 500;
      init();
    }
    
    function rand(a,b){return a+Math.random()*(b-a);}
    function init(){
      pts=[];
      var n=Math.round(N_BASE*(W*H)/(1440*900));
      n=Math.max(35,Math.min(90,n));
      for(var i=0;i<n;i++){
        var col=COLS[Math.floor(Math.random()*COLS.length)];
        pts.push({x:rand(0,W),y:rand(0,H),vx:rand(-.25,.25),vy:rand(-.18,.18),r:rand(.6,1.4),col:col,alpha:rand(.25,.55),z:rand(.3,1)});
      }
    }
    function draw(){
      ctx.clearRect(0,0,W,H);
      for(var i=0;i<pts.length;i++){
        var p=pts[i];
        for(var j=i+1;j<pts.length;j++){
          var q=pts[j],dx=p.x-q.x,dy=p.y-q.y,d=Math.sqrt(dx*dx+dy*dy);
          if(d<CONNECT_DIST){var fade=1-d/CONNECT_DIST,depth=(p.z+q.z)*.5;ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(q.x,q.y);ctx.strokeStyle='rgba('+p.col+','+(fade*.13*depth)+')';ctx.lineWidth=fade*1.1*depth;ctx.stroke();}
        }
        var mdx=p.x-MOUSE.x,mdy=p.y-MOUSE.y,md=Math.sqrt(mdx*mdx+mdy*mdy);
        if(md<140){var mf=1-md/140;ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(MOUSE.x,MOUSE.y);ctx.strokeStyle='rgba('+p.col+','+(mf*.22)+')';ctx.lineWidth=mf*1.4;ctx.stroke();}
      }
      for(var i=0;i<pts.length;i++){
        var p=pts[i];
        var grd=ctx.createRadialGradient(p.x,p.y,0,p.x,p.y,p.r*3.0*p.z);
        grd.addColorStop(0,'rgba('+p.col+','+(p.alpha*p.z)+')');
        grd.addColorStop(1,'rgba('+p.col+',0)');
        ctx.beginPath();ctx.arc(p.x,p.y,p.r*3.0*p.z,0,Math.PI*2);ctx.fillStyle=grd;ctx.fill();
        ctx.beginPath();ctx.arc(p.x,p.y,p.r*p.z,0,Math.PI*2);ctx.fillStyle='rgba('+p.col+','+(p.alpha*p.z)+')';ctx.fill();
        p.x+=p.vx;p.y+=p.vy;
        if(p.x<-20)p.x=W+20;if(p.x>W+20)p.x=-20;
        if(p.y<-20)p.y=H+20;if(p.y>H+20)p.y=-20;
      }
      RAF=requestAnimationFrame(draw);
    }
    
    // Position the canvas inside the hero section
    var hero = document.querySelector('.tools-hero');
    if (hero) {
      hero.style.position = 'relative';
      hero.insertBefore(c, hero.firstChild);
    }
    
    window.addEventListener('resize',resize);
    document.addEventListener('mousemove',function(e){
      var rect = c.getBoundingClientRect();
      MOUSE.x=e.clientX - rect.left;
      MOUSE.y=e.clientY - rect.top;
    });
    document.addEventListener('mouseleave',function(){MOUSE.x=-999;MOUSE.y=-999;});
    resize();draw();
  })();
  </script>
"""

def patch_html(content):
    # 1. Add style="--brand: #..." to the cards
    for tool_id, color in BRAND_COLORS.items():
        pattern = f'(<div class="tool-card gsap-card" id="card-{tool_id}")(?!(.*?style="--brand:))'
        # Only inject if style="--brand is not already there
        content = re.sub(pattern, f'\\1 style="--brand: {color};"', content)
        
    # 2. Remove cyber-grid and hex-particles
    content = content.replace('<div class="cyber-grid"></div>\n    <div class="hex-particles"></div>', '')
    content = content.replace('<div class="cyber-grid"></div>', '')
    content = content.replace('<div class="hex-particles"></div>', '')
    
    # 3. Inject CSS
    if '#constellation-canvas' not in content:
        content = content.replace('</style>', f'{PARTICLE_CSS}\n  </style>')
        
    # 4. Inject Canvas + JS
    if 'id="constellation-canvas"' not in content:
        # put it before </body>
        content = content.replace('</body>', f'{PARTICLE_HTML_JS}\n</body>')
        
    return content

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    html = patch_html(html)
    
    # Also to force cache bust, I can increment the version of style.css
    # But for now, they can just refresh.
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

print("UI successfully patched!")
