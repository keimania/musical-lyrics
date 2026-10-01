import json
import os

def build_six_web_viewer():
    with open('six/data/six_skeletons.json', 'r', encoding='utf-8') as f:
        skeletons = json.load(f)

    all_trans = {}
    for p in [1, 2]:
        p_path = f'six/data/trans_part{p}.json'
        if os.path.exists(p_path):
            with open(p_path, 'r', encoding='utf-8') as pf:
                all_trans.update(json.load(pf))

    web_songs = []
    for i in range(1, 12):
        sid = str(i)
        s = skeletons[sid]
        t = all_trans.get(sid, {})
        synopsis = t.get('synopsis', '곡 개요가 준비 중입니다.')
        notes = t.get('notes', [])
        trans_dict = t.get('translations', {})

        stanzas_data = []
        for st in s['stanzas']:
            key = st['key']
            orig = st['lines']
            translated = trans_dict.get(key, [])
            stanzas_data.append({
                'key': key,
                'speaker_kr': st['speaker_kr'],
                'speaker_en': st['speaker_en'],
                'lines_en': orig,
                'lines_kr': translated if translated else ['(번역 준비 중)' for _ in orig]
            })

        web_songs.append({
            'id': i,
            'title': s['title'],
            'title_kr': s['title_kr'],
            'synopsis': synopsis,
            'notes': notes,
            'stanzas': stanzas_data
        })

    json_str = json.dumps(web_songs, ensure_ascii=False)

    html_content = f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>뮤지컬 식스(SIX) 전 11곡 영한 대역 콘서트 뷰어</title>
  <style>
    :root {{
      --bg: #0c0914;
      --card-bg: #151124;
      --neon-pink: #ff1493;
      --neon-gold: #ffd700;
      --neon-green: #00ff7f;
      --neon-blue: #00bfff;
      --neon-red: #ff3366;
      --neon-silver: #e6e6fa;
      --purple-accent: #9b51e0;
      --text: #f5f5f7;
      --text-muted: #a39eb8;
      --border: #292042;
      --hover: #221a38;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Apple SD Gothic Neo", "Noto Sans KR", sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      display: flex;
      height: 100vh;
      overflow: hidden;
    }}
    /* Sidebar */
    #sidebar {{
      width: 320px;
      background: #110d1c;
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
    }}
    .sidebar-header {{
      padding: 20px 16px;
      border-bottom: 1px solid var(--border);
      background: #0d0a17;
      text-align: center;
    }}
    .sidebar-header h1 {{
      font-size: 1.4rem;
      background: linear-gradient(45deg, #ff1493, #ffd700, #00bfff);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      font-weight: 900;
      letter-spacing: 2px;
    }}
    .sidebar-header p {{
      font-size: 0.8rem;
      color: var(--text-muted);
      margin-top: 4px;
    }}
    .search-box {{
      padding: 12px 16px;
      border-bottom: 1px solid var(--border);
    }}
    .search-box input {{
      width: 100%;
      padding: 8px 12px;
      background: #1b152b;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: #fff;
      font-size: 0.85rem;
      outline: none;
    }}
    .search-box input:focus {{ border-color: var(--neon-pink); }}
    .song-list {{
      flex: 1;
      overflow-y: auto;
      padding: 8px;
    }}
    .song-item {{
      padding: 10px 12px;
      margin-bottom: 6px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s;
      border: 1px solid transparent;
      background: #161224;
    }}
    .song-item:hover {{
      background: var(--hover);
      border-color: rgba(255, 20, 147, 0.3);
    }}
    .song-item.active {{
      background: rgba(255, 20, 147, 0.15);
      border-color: var(--neon-pink);
    }}
    .song-num {{
      font-size: 0.75rem;
      color: var(--neon-gold);
      font-weight: 700;
    }}
    .song-title {{
      font-size: 0.92rem;
      font-weight: 700;
      color: #fff;
    }}
    .song-title-kr {{
      font-size: 0.8rem;
      color: var(--text-muted);
    }}

    /* Main Content */
    #main {{
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      background: var(--bg);
    }}
    .top-bar {{
      padding: 14px 24px;
      border-bottom: 1px solid var(--border);
      background: #110d1c;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .view-toggles {{
      display: flex;
      gap: 8px;
    }}
    .view-btn {{
      padding: 6px 14px;
      background: #1d172e;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: var(--text-muted);
      font-size: 0.8rem;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .view-btn.active {{
      background: var(--neon-pink);
      color: #fff;
      font-weight: 700;
      border-color: var(--neon-pink);
      box-shadow: 0 0 10px rgba(255, 20, 147, 0.4);
    }}
    .song-content {{
      flex: 1;
      overflow-y: auto;
      padding: 32px 48px;
      max-width: 960px;
      margin: 0 auto;
      width: 100%;
    }}
    .song-header {{
      margin-bottom: 24px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--border);
    }}
    .song-header h2 {{
      font-size: 1.8rem;
      color: #fff;
      font-weight: 800;
    }}
    .song-header h2 .kr-title {{
      color: var(--neon-gold);
      margin-left: 10px;
      font-size: 1.3rem;
      font-weight: 600;
    }}
    .synopsis-box {{
      background: var(--card-bg);
      border-left: 4px solid var(--neon-pink);
      padding: 16px 20px;
      border-radius: 0 8px 8px 0;
      margin-bottom: 24px;
      font-size: 0.95rem;
      line-height: 1.7;
    }}
    .notes-box {{
      background: #140e24;
      border: 1px solid #332057;
      border-radius: 8px;
      padding: 16px 20px;
      margin-bottom: 32px;
    }}
    .notes-box h4 {{
      font-size: 0.9rem;
      color: #00bfff;
      margin-bottom: 10px;
    }}
    .notes-box ul {{
      padding-left: 20px;
      font-size: 0.86rem;
      color: #c4bfd6;
    }}
    .notes-box li {{
      margin-bottom: 6px;
    }}
    /* Stanzas */
    .stanza-block {{
      margin-bottom: 24px;
      background: rgba(255,255,255,0.02);
      border-radius: 8px;
      padding: 16px 20px;
      border: 1px solid rgba(255,255,255,0.05);
    }}
    .speaker-tag {{
      display: inline-block;
      font-size: 0.8rem;
      font-weight: 700;
      color: #ff69b4;
      background: rgba(255, 105, 180, 0.15);
      padding: 3px 10px;
      border-radius: 4px;
      margin-bottom: 12px;
      border: 1px solid rgba(255, 105, 180, 0.3);
    }}
    .lyric-pair {{
      margin-bottom: 10px;
      line-height: 1.5;
    }}
    .lyric-en {{
      font-weight: 700;
      color: #ffffff;
      font-size: 0.96rem;
    }}
    .lyric-kr {{
      color: #8be9fd;
      font-size: 0.92rem;
      margin-top: 2px;
    }}
    .mode-kr-only .lyric-en {{ display: none; }}
    .mode-en-only .lyric-kr {{ display: none; }}
  </style>
</head>
<body>
  <div id="sidebar">
    <div class="sidebar-header">
      <h1>★ SIX ★</h1>
      <p>전 11곡 영한 대역 콘서트 뷰어</p>
    </div>
    <div class="search-box">
      <input type="text" id="searchInput" placeholder="곡 제목, 왕비, 가사 검색..." oninput="renderSongList()">
    </div>
    <div class="song-list" id="songListContainer"></div>
  </div>

  <div id="main">
    <div class="top-bar">
      <div style="font-size: 0.85rem; color: var(--neon-gold);" id="topBarTrackInfo">Track 01 of 11</div>
      <div class="view-toggles">
        <button class="view-btn active" id="btnBilingual" onclick="setViewMode('bilingual')">영한 대역</button>
        <button class="view-btn" id="btnKr" onclick="setViewMode('kr')">한국어만</button>
        <button class="view-btn" id="btnEn" onclick="setViewMode('en')">English Only</button>
      </div>
    </div>
    <div class="song-content" id="songContent"></div>
  </div>

  <script>
    const songsData = {json_str};
    let currentSongId = 1;
    let currentMode = 'bilingual';

    function init() {{
      renderSongList();
      loadSong(1);
    }}

    function setViewMode(mode) {{
      currentMode = mode;
      document.getElementById('btnBilingual').classList.toggle('active', mode === 'bilingual');
      document.getElementById('btnKr').classList.toggle('active', mode === 'kr');
      document.getElementById('btnEn').classList.toggle('active', mode === 'en');
      
      const content = document.getElementById('songContent');
      content.className = 'song-content';
      if (mode === 'kr') content.classList.add('mode-kr-only');
      if (mode === 'en') content.classList.add('mode-en-only');
    }}

    function renderSongList() {{
      const query = document.getElementById('searchInput').value.toLowerCase().trim();
      const container = document.getElementById('songListContainer');
      container.innerHTML = '';

      songsData.forEach(s => {{
        if (query) {{
          const matchTitle = s.title.toLowerCase().includes(query) || s.title_kr.toLowerCase().includes(query);
          const matchLyric = s.stanzas.some(st => st.lines_en.some(l => l.toLowerCase().includes(query)) || st.lines_kr.some(l => l.toLowerCase().includes(query)));
          if (!matchTitle && !matchLyric) return;
        }}

        const item = document.createElement('div');
        item.className = 'song-item' + (s.id === currentSongId ? ' active' : '');
        item.onclick = () => loadSong(s.id);
        item.innerHTML = `
          <div class="song-num">SIX · Track ${{String(s.id).padStart(2, '0')}}</div>
          <div class="song-title">${{s.title}}</div>
          <div class="song-title-kr">${{s.title_kr}}</div>
        `;
        container.appendChild(item);
      }});
    }}

    function loadSong(id) {{
      currentSongId = id;
      document.querySelectorAll('.song-item').forEach(el => el.classList.remove('active'));
      renderSongList();

      const song = songsData.find(s => s.id === id);
      if (!song) return;

      document.getElementById('topBarTrackInfo').textContent = `Track ${{String(song.id).padStart(2, '0')}} / 11`;

      let notesHtml = '';
      if (song.notes && song.notes.length > 0) {{
        notesHtml = `
          <div class="notes-box">
            <h4>💡 감상 포인트 및 주석 (Key Notes & Pop Motifs)</h4>
            <ul>
              ${{song.notes.map(n => `<li>${{n}}</li>`).join('')}}
            </ul>
          </div>
        `;
      }}

      let stanzasHtml = '';
      song.stanzas.forEach(st => {{
        let linesHtml = '';
        for (let idx = 0; idx < st.lines_en.length; idx++) {{
          const en = st.lines_en[idx] || '';
          const kr = st.lines_kr[idx] || '';
          linesHtml += `
            <div class="lyric-pair">
              <div class="lyric-en">${{en}}</div>
              <div class="lyric-kr">${{kr}}</div>
            </div>
          `;
        }}

        stanzasHtml += `
          <div class="stanza-block">
            <div class="speaker-tag">${{st.speaker_kr}} (${{st.speaker_en}})</div>
            ${{linesHtml}}
          </div>
        `;
      }});

      const html = `
        <div class="song-header">
          <h2>${{String(song.id).padStart(2, '0')}}. ${{song.title}} <span class="kr-title">${{song.title_kr}}</span></h2>
        </div>
        <div class="synopsis-box">
          <strong>📖 장면 및 역사적 배경:</strong> ${{song.synopsis}}
        </div>
        ${{notesHtml}}
        <div class="lyrics-section">
          ${{stanzasHtml}}
        </div>
      `;

      const content = document.getElementById('songContent');
      content.innerHTML = html;
      content.scrollTop = 0;
    }}

    window.onload = init;
  </script>
</body>
</html>
'''

    with open('six/index.html', 'w', encoding='utf-8') as hf:
        hf.write(html_content)

    print("Successfully built six/index.html!")

if __name__ == '__main__':
    build_six_web_viewer()
