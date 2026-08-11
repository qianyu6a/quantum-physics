import re

path = "D:/知识库/quantum-physics/static/index.html"
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

# ═══════════════════════════════════════
# 1. Add CSS for home page + light theme + search + cards
# ═══════════════════════════════════════
extra_css = '''
/* ══ Light Theme ══ */
body.light { --bg: #f0f4f8; --surface: #ffffff; --surface2: #e8ecf1; --fg: #1a1a2e; --muted: #555; --faint: #bbb; --border: rgba(0,0,0,0.1); }
body.light .sidebar { background: var(--surface); }
body.light .controls { background: var(--surface2); }
body.light .callout { background: var(--surface); }
body.light .canvas-container { background: var(--surface); }

/* ══ Top Nav Bar ══ */
.topnav {
  position:fixed; top:0; left:0; right:0; z-index:100; height:44px;
  background:var(--surface); border-bottom:1px solid var(--border);
  display:flex; align-items:center; justify-content:space-between; padding:0 16px;
  backdrop-filter:blur(10px);
}
.topnav .logo { font-size:14px; color:var(--accent); font-weight:700; cursor:pointer; letter-spacing:1px; }
.topnav .nav-btns { display:flex; gap:8px; align-items:center; }
.topnav .nav-btn {
  padding:4px 10px; border-radius:6px; border:1px solid var(--border);
  background:transparent; color:var(--muted); font-size:11px; cursor:pointer;
  font-family:var(--font); transition:all .2s;
}
.topnav .nav-btn:hover { border-color:var(--accent); color:var(--accent); }
.topnav .nav-btn.active { background:rgba(0,180,216,0.15); border-color:var(--accent); color:var(--accent); }

/* ══ Home View ══ */
#home-view { padding-top:44px; display:none; }
#home-view.active { display:block; }
.home-hero {
  text-align:center; padding:60px 20px 40px;
  background:linear-gradient(180deg, rgba(0,180,216,0.08) 0%, transparent 100%);
}
.home-hero h1 { font-size:32px; color:var(--fg); margin-bottom:8px; }
.home-hero .subtitle { font-size:14px; color:var(--muted); max-width:600px; margin:0 auto; line-height:1.8; }
.home-hero .stats { display:flex; justify-content:center; gap:32px; margin-top:24px; }
.home-hero .stat { text-align:center; }
.home-hero .stat-num { font-size:28px; font-weight:700; color:var(--accent); }
.home-hero .stat-label { font-size:10px; color:var(--muted); letter-spacing:1px; text-transform:uppercase; }

/* Timeline */
.timeline-section { padding:32px 20px; max-width:800px; margin:0 auto; }
.timeline-section h2 { font-size:18px; color:var(--accent); margin-bottom:20px; text-align:center; }
.timeline { position:relative; padding-left:24px; border-left:2px solid var(--border); }
.timeline-item { margin-bottom:24px; position:relative; }
.timeline-item::before {
  content:''; position:absolute; left:-30px; top:4px; width:10px; height:10px;
  border-radius:50%; background:var(--accent); border:2px solid var(--surface);
}
.timeline-year { font-size:11px; color:var(--accent); font-weight:700; letter-spacing:1px; }
.timeline-text { font-size:13px; color:var(--muted); line-height:1.7; margin-top:4px; }

/* Concept Cards Grid */
.cards-section { padding:20px; max-width:1000px; margin:0 auto; }
.cards-section h2 { font-size:18px; color:var(--accent); margin-bottom:16px; text-align:center; }
.search-bar {
  display:flex; justify-content:center; margin-bottom:20px;
}
.search-bar input {
  background:var(--surface2); border:1px solid var(--border); border-radius:20px;
  padding:8px 20px; color:var(--fg); font-size:13px; width:280px; max-width:90%;
  outline:none; font-family:var(--font);
}
.search-bar input:focus { border-color:var(--accent); }
.cards-grid { display:grid; grid-template-columns:repeat(auto-fill, minmax(260px,1fr)); gap:14px; }
.concept-card {
  background:var(--surface); border:1px solid var(--border); border-radius:var(--radius);
  padding:20px; cursor:pointer; transition:all .2s;
}
.concept-card:hover { border-color:var(--accent); transform:translateY(-2px); box-shadow:0 4px 20px rgba(0,180,216,0.1); }
.concept-card .card-icon { font-size:24px; margin-bottom:8px; }
.concept-card .card-num { font-size:10px; color:var(--faint); letter-spacing:1px; }
.concept-card .card-title { font-size:15px; color:var(--fg); margin:4px 0; font-weight:600; }
.concept-card .card-desc { font-size:12px; color:var(--muted); line-height:1.6; }
.concept-card.hidden { display:none; }

/* ══ Detail View ══ */
#detail-view { padding-top:44px; display:none; }
#detail-view.active { display:flex; }
.no-results { text-align:center; color:var(--muted); padding:40px; font-size:14px; display:none; }

/* Mobile topnav */
@media (max-width:768px) {
  .home-hero h1 { font-size:24px; }
  .cards-grid { grid-template-columns:1fr; }
  .timeline-section { padding:20px 12px; }
  #detail-view.active { flex-direction:column; }
}
'''

# Inject CSS before </style>
html = html.replace('</style>', extra_css + '\n</style>', 1)

# ═══════════════════════════════════════
# 2. Add HTML: topnav + home view + wrap detail view
# ═══════════════════════════════════════

# Build timeline HTML
timeline_html = '''
    <div class="timeline-section">
      <h2>📜 近代物理编年史</h2>
      <div class="timeline" id="timeline"></div>
    </div>
'''

# Build concept cards (generated by JS from data)
cards_html = '''
    <div class="cards-section">
      <h2>🧭 探索量子世界</h2>
      <div class="search-bar"><input type="text" id="searchInput" placeholder="搜索概念... (如: 波粒二象性, 量子纠缠)" oninput="filterCards()"></div>
      <div class="cards-grid" id="cardsGrid"></div>
      <div class="no-results" id="noResults">未找到匹配的概念 🔍</div>
    </div>
'''

home_html = f'''
  <div id="home-view" class="active">
    <div class="home-hero">
      <h1>⚛️ 量子物理交互科普</h1>
      <p class="subtitle" id="heroSubtitle">从1900年普朗克的"绝望之举"，到2020年代的量子计算——这是一场人类对宇宙最底层规则的探索。这里没有公式堆砌，只有故事、动画和你能亲手操作的交互实验。</p>
      <div class="stats">
        <div class="stat"><div class="stat-num">15</div><div class="stat-label">核心概念</div></div>
        <div class="stat"><div class="stat-num">125</div><div class="stat-label">年物理学史</div></div>
        <div class="stat"><div class="stat-num">17</div><div class="stat-label">基本粒子</div></div>
      </div>
    </div>
    {timeline_html}
    {cards_html}
  </div>
'''

# Build topnav
topnav_html = '''
  <div class="topnav">
    <span class="logo" onclick="showView('home')">⚛️ 量子物理</span>
    <div class="nav-btns">
      <button class="nav-btn active" id="navHome" onclick="showView('home')">🏠 首页</button>
      <button class="nav-btn" id="navDetail" onclick="showView('detail')">📚 知识库</button>
      <button class="nav-btn" onclick="toggleTheme()" id="themeBtn">🌙</button>
      <button class="nav-btn" onclick="toggleLang()" id="langBtn">EN</button>
    </div>
  </div>
'''

# Insert topnav after <body>
html = html.replace('<body>', '<body>\n' + topnav_html, 1)

# Insert home view after topnav
html = html.replace(topnav_html, topnav_html + '\n' + home_html, 1)

# Wrap existing content in detail view
# Find <nav class="sidebar" and wrap everything from there to </body> in detail-view
body_start = html.find('<body>') + len('<body>')
nav_start = html.find('<nav class="sidebar"', body_start)
body_end = html.find('</body>', nav_start)

existing_content = html[nav_start:body_end]

detail_wrap = f'<div id="detail-view">\n{existing_content}\n</div>\n'
html = html[:nav_start] + detail_wrap + html[body_end:]

# ═══════════════════════════════════════
# 3. Add JS functions (view switching, theme, search, language)
# ═══════════════════════════════════════

extra_js = '''
// ══ View Switching ══
let currentLang = 'zh';
let isDark = true;

function showView(view) {
  document.getElementById('home-view').classList.toggle('active', view === 'home');
  document.getElementById('detail-view').classList.toggle('active', view === 'detail');
  document.getElementById('navHome').classList.toggle('active', view === 'home');
  document.getElementById('navDetail').classList.toggle('active', view === 'detail');
  if (view === 'detail') {
    activeId = activeId || 'planck';
    setTimeout(() => { showConcept(activeId); }, 100);
  }
  window.scrollTo(0, 0);
}

// ══ Theme Toggle ══
function toggleTheme() {
  isDark = !isDark;
  document.body.classList.toggle('light', !isDark);
  document.getElementById('themeBtn').textContent = isDark ? '☀️' : '🌙';
  localStorage.setItem('quantum-theme', isDark ? 'dark' : 'light');
}
// Load saved theme
if (localStorage.getItem('quantum-theme') === 'light') { isDark = false; toggleTheme(); }

// ══ Search ══
function filterCards() {
  const q = document.getElementById('searchInput').value.toLowerCase();
  let found = false;
  document.querySelectorAll('.concept-card').forEach(card => {
    const title = (card.dataset.title || '').toLowerCase();
    const desc = (card.dataset.desc || '').toLowerCase();
    const match = !q || title.includes(q) || desc.includes(q);
    card.classList.toggle('hidden', !match);
    if (match) found = true;
  });
  document.getElementById('noResults').style.display = found ? 'none' : 'block';
}

// ══ Language Toggle ══
function toggleLang() {
  currentLang = currentLang === 'zh' ? 'en' : 'zh';
  document.getElementById('langBtn').textContent = currentLang === 'zh' ? 'EN' : '中文';
  updateLanguage();
}
function updateLanguage() {
  // Will be populated when translations are ready
  if (currentLang === 'en' && translations) {
    concepts.forEach(c => {
      if (translations[c.id]) {
        c.title = translations[c.id].title || c.title;
        c.tagline = translations[c.id].tagline || c.tagline;
        c.problem = translations[c.id].problem || c.problem;
        c.insight = translations[c.id].insight || c.insight;
        c.bigpic = translations[c.id].bigpic || c.bigpic;
      }
    });
    rebuildUI();
  }
}
let translations = null;

// ══ Build Home Page ══
function buildHomePage() {
  // Concept cards
  const grid = document.getElementById('cardsGrid');
  concepts.forEach(c => {
    const card = document.createElement('div');
    card.className = 'concept-card';
    card.dataset.title = c.title;
    card.dataset.desc = c.tagline;
    card.innerHTML = `
      <div class="card-icon">${c.icon}</div>
      <div class="card-num">${c.year}</div>
      <div class="card-title">${c.num}. ${c.title}</div>
      <div class="card-desc">${c.tagline}</div>
    `;
    card.onclick = () => { activeId = c.id; showView('detail'); };
    grid.appendChild(card);
  });

  // Timeline
  const timeline = document.getElementById('timeline');
  const events = [
    {year:'1895', text:'伦琴发现X射线——人类第一次看到体内的骨骼。这不仅是一项医学革命，更标志着物理学开始深入原子世界。'},
    {year:'1900', text:'普朗克引入能量量子化概念，E=hν。"这是绝望之举"——他自己都不信。量子物理的诞生日。'},
    {year:'1905', text:'爱因斯坦奇迹年：光电效应（光量子）、布朗运动（原子存在证据）、狭义相对论（E=mc²）。26岁的专利局职员改写了物理学。'},
    {year:'1911-1913', text:'卢瑟福发现原子核，玻尔提出量子轨道模型。电子"住楼房"——只允许特定轨道，解释了为什么元素有独特的光谱。'},
    {year:'1924-1927', text:'量子力学的黄金时代：德布罗意提出波粒二象性，海森堡发现不确定性原理，薛定谔写出波动方程。玻尔和海森堡在哥本哈根激烈争论——量子世界的哲学基础在此奠基。'},
    {year:'1928-1932', text:'狄拉克方程统一了量子力学和相对论，预言了反物质。安德森在宇宙射线中发现正电子——数学之美被实验证实。'},
    {year:'1940s-1950s', text:'量子电动力学（QED）完成：费曼、施温格、朝永振一郎解决了"无穷大"问题。QED成为人类最精确的物理理论——精确到小数点后12位。'},
    {year:'1960s-1970s', text:'标准模型成形：盖尔曼提出夸克模型，格拉肖-温伯格-萨拉姆统一了电磁力和弱力。所有预言的粒子被逐一发现。'},
    {year:'1964-2012', text:'希格斯机制预言了赋予万物质量的场。希格斯的论文最初被拒稿，但他等了48年。2012年CERN宣布发现希格斯玻色子——83岁的他在发布会上哭了。'},
    {year:'1980s-1990s', text:'量子纠缠被实验证实违反贝尔不等式——爱因斯坦错了。量子计算从费曼的构想走向实验：肖尔算法证明量子计算机能破解RSA加密。'},
    {year:'2000s-2020s', text:'量子技术爆发：中国发射"墨子号"量子卫星，Google实现量子霸权，IBM部署千比特级处理器。量子计算机正在从实验室走向数据中心。'}
  ];
  events.forEach(e => {
    const item = document.createElement('div');
    item.className = 'timeline-item';
    item.innerHTML = `<div class="timeline-year">${e.year}</div><div class="timeline-text">${e.text}</div>`;
    timeline.appendChild(item);
  });
}

// ══ Init ══
document.addEventListener('DOMContentLoaded', () => {
  buildHomePage();
});
''';

# Inject JS before </script> at end
html = html.replace('</script>\n</body>', extra_js + '\n</script>\n</body>', 1)

# Fix the initCanvas call at the bottom
html = html.replace("setTimeout(() => initCanvas('planck'), 200);", "// initCanvas handled by showConcept now")

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Done. File size: {len(html)} bytes")
print("Added: home view, detail view, topnav, theme toggle, search, timeline, cards grid")
