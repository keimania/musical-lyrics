# -*- coding: utf-8 -*-
"""
Dear Evan Hansen Musical Archive & Web Viewer Builder
Generates:
- dear_evan_hansen/data/deh_songs.json
- dear_evan_hansen/act1/*.md (8 tracks)
- dear_evan_hansen/act2/*.md (6 tracks)
- dear_evan_hansen/deh_complete.md
- dear_evan_hansen/README.md
- dear_evan_hansen/index.html (Interactive Web Viewer)
"""

import os
import json
import re
import sys

from build_deh_data import DEH_SONGS

FILE_SLUGS = [
    # Act 1 (1-8)
    "01_anybody_have_a_map",
    "02_waving_through_a_window",
    "03_for_forever",
    "04_sincerely_me",
    "05_requiem",
    "06_if_i_could_tell_her",
    "07_disappear",
    "08_you_will_be_found",
    # Act 2 (9-14)
    "09_to_break_in_a_glove",
    "10_only_us",
    "11_good_for_you",
    "12_words_fail",
    "13_so_big_so_small",
    "14_finale"
]

def slugify_anchor(title):
    cleaned = re.sub(r'[^a-zA-Z0-9\s-]', '', title).lower()
    return re.sub(r'[\s_]+', '-', cleaned).strip('-')

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assert len(DEH_SONGS) == 14, f"Expected 14 songs, got {len(DEH_SONGS)}"

    for idx, song in enumerate(DEH_SONGS):
        slug = FILE_SLUGS[idx]
        act_dir = f"act{song['act']}"
        song["slug"] = slug
        song["filename"] = f"{slug}.md"
        song["rel_path"] = f"{act_dir}/{slug}.md"

    # 1. Verify 1:1 Line Matching
    print("=== [1/6] Verifying 1:1 Line Matching ===")
    total_lines = 0
    mismatches = 0
    for song in DEH_SONGS:
        for s_idx, st in enumerate(song["stanzas"]):
            len_en = len(st["lines_en"])
            len_kr = len(st["lines_kr"])
            total_lines += len_en
            if len_en != len_kr:
                print(f"[MISMATCH] Song #{song['id']} ({song['title']}) Stanza #{s_idx+1}: EN({len_en}) != KR({len_kr})")
                mismatches += 1

    if mismatches > 0:
        raise ValueError(f"Found {mismatches} stanza mismatches! Aborting build.")
    print(f"Verification Passed! 14 songs, {total_lines} lines verified 100% aligned 1:1.\n")

    # 2. Save JSON Database
    print("=== [2/6] Writing dear_evan_hansen/data/deh_songs.json ===")
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    json_path = os.path.join(data_dir, "deh_songs.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(DEH_SONGS, f, ensure_ascii=False, indent=2)
    print(f"Saved: {json_path}\n")

    # 3. Generate Individual Markdown Track Files
    print("=== [3/6] Generating Individual Markdown Track Files ===")
    os.makedirs(os.path.join(base_dir, "act1"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "act2"), exist_ok=True)

    for idx, song in enumerate(DEH_SONGS):
        file_path = os.path.join(base_dir, song["rel_path"])
        act = song["act"]
        act_label = f"제{act}막 (Act {act})"

        prev_song = DEH_SONGS[idx - 1] if idx > 0 else None
        next_song = DEH_SONGS[idx + 1] if idx < len(DEH_SONGS) - 1 else None

        if prev_song:
            p_dir = f"act{prev_song['act']}"
            c_dir = f"act{act}"
            p_prefix = "./" if p_dir == c_dir else f"../{p_dir}/"
            prev_link = f"[{prev_song['id']:02d}. {prev_song['title']}]({p_prefix}{prev_song['filename']})"
        else:
            prev_link = "시작"

        if next_song:
            n_dir = f"act{next_song['act']}"
            c_dir = f"act{act}"
            n_prefix = "./" if n_dir == c_dir else f"../{n_dir}/"
            next_link = f"[{next_song['id']:02d}. {next_song['title']}]({n_prefix}{next_song['filename']})"
        else:
            next_link = "끝"

        md = []
        md.append(f"# {song['id']:02d}. {song['title']} ({song['title_kr']})\n\n")
        md.append(f"- **막(Act)**: {act_label} · Track {song['id']:02d}\n")
        chars_en = ", ".join(song.get("characters_en", []))
        chars_kr = ", ".join(song.get("characters_kr", []))
        md.append(f"- **등장인물/보컬**: {chars_kr} ({chars_en})\n")
        md.append(f"- **넘버 이동**: [◀ 이전 곡: {prev_link}] | [전체 목차](../README.md) | [다음 곡: {next_link} ▶]\n\n")
        md.append("---\n\n")

        md.append("## 📖 곡 개요 및 드라마적 배경 (Dramatic Synopsis)\n\n")
        md.append(f"{song['synopsis']}\n\n")

        if song.get("notes"):
            md.append("## 💡 감상 포인트 및 주석 (Key Notes & Themes)\n\n")
            for note in song["notes"]:
                md.append(f"- {note}\n")
            md.append("\n")

        md.append("---\n\n")
        md.append("## 🎵 가사 대역 (Bilingual Lyrics)\n\n")

        for stanza in song["stanzas"]:
            spk_kr = stanza.get("speaker_kr", "등장인물")
            spk_en = stanza.get("speaker_en", "Character")
            md.append(f"### [{spk_kr} / {spk_en}]\n\n")
            md.append("> \n")
            for l_en, l_kr in zip(stanza["lines_en"], stanza["lines_kr"]):
                md.append(f"> **{l_en}**  \n")
                md.append(f"> {l_kr}  \n")
                md.append("> \n")
            md.append("\n")

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(md)

    print(f"Generated 14 individual markdown files in dear_evan_hansen/act1/ and dear_evan_hansen/act2/\n")

    # 4. Generate Master Complete Document
    print("=== [4/6] Generating dear_evan_hansen/deh_complete.md ===")
    comp = []
    comp.append("# 💌 뮤지컬 《디어 에반 핸슨 (Dear Evan Hansen)》 전 14곡 공식 원본 가사 및 한국어 전곡 대역·해설집\n\n")
    comp.append("**작사/작곡**: 벤지 파섹 & 저스틴 폴 (Benj Pasek & Justin Paul)\n")
    comp.append("**극본**: 스티븐 레븐슨 (Steven Levenson)\n")
    comp.append("**초연 주연**: 벤 플랫 (에반 핸슨), 로라 드레이퍼스 (조에 머피), 레이첼 베이 존스 (하이디 핸슨), 마이크 파이스트 (코너 머피), 윌 롤랜드 (재러드 클라인먼)\n")
    comp.append("**수상 이력**: 제71회 토니상 6관왕 (작품상, 극본상, 작곡/작사상, 남우주연상, 여우조연상, 편곡상), 그래미 어워드 최우수 뮤지컬 앨범상 수상\n")
    comp.append("**총 수록 수**: 총 14개 넘버 (1막 8곡 / 2막 6곡 전수 수록 및 100% 1:1 대역)\n\n")
    comp.append("---\n\n")

    comp.append("## 📜 전곡 목차 (Table of Contents)\n\n")
    comp.append("### 제1막 (Act I: 거짓말의 시작과 코너 프로젝트의 탄생)\n\n")
    for s in DEH_SONGS[:8]:
        anchor = f"{s['id']:02d}-{slugify_anchor(s['title'])}"
        comp.append(f"{s['id']:02d}. [{s['title']} ({s['title_kr']})](#{anchor})\n")

    comp.append("\n### 제2막 (Act II: 환상의 절정과 진실의 고백, 그리고 치유)\n\n")
    for s in DEH_SONGS[8:]:
        anchor = f"{s['id']:02d}-{slugify_anchor(s['title'])}"
        comp.append(f"{s['id']:02d}. [{s['title']} ({s['title_kr']})](#{anchor})\n")

    comp.append("\n---\n\n")

    for s in DEH_SONGS:
        anchor = f"{s['id']:02d}-{slugify_anchor(s['title'])}"
        comp.append(f"## <a id=\"{anchor}\"></a>{s['id']:02d}. {s['title']} ({s['title_kr']})\n\n")
        comp.append(f"- **막**: Act {s['act']} · Track {s['id']:02d}\n")
        chars_en = ", ".join(s.get("characters_en", []))
        chars_kr = ", ".join(s.get("characters_kr", []))
        comp.append(f"- **등장인물/보컬**: {chars_kr} ({chars_en})\n\n")
        comp.append(f"**드라마적 배경**: {s['synopsis']}\n\n")

        if s.get("notes"):
            comp.append("**감상 포인트 & 해설**:\n")
            for n in s["notes"]:
                comp.append(f"- {n}\n")
            comp.append("\n")

        comp.append("### 가사 대역\n\n")
        for stanza in s["stanzas"]:
            spk_kr = stanza.get("speaker_kr", "등장인물")
            spk_en = stanza.get("speaker_en", "Character")
            comp.append(f"**[{spk_kr} / {spk_en}]**\n\n")
            for l_en, l_kr in zip(stanza["lines_en"], stanza["lines_kr"]):
                comp.append(f"> **{l_en}**  \n")
                comp.append(f"> {l_kr}  \n")
                comp.append("> \n")
            comp.append("\n")

        comp.append("---\n\n")

    complete_path = os.path.join(base_dir, "deh_complete.md")
    with open(complete_path, "w", encoding="utf-8") as f:
        f.writelines(comp)
    print(f"Generated: {complete_path}\n")

    # 5. Generate README.md
    print("=== [5/6] Generating dear_evan_hansen/README.md ===")
    readme = []
    readme.append("# 💌 뮤지컬 《디어 에반 핸슨 (Dear Evan Hansen)》 공식 전곡 가사 및 영한 대역 아카이브\n\n")
    readme.append("> **\"You Will Be Found.\"**\n")
    readme.append("> 제71회 토니상 6관왕(작품상·남우주연상 등) & 그래미 어워드 수상작!\n")
    readme.append("> 《위대한 쇼맨》, 《라라랜드》의 천재 듀오 **파섹 & 폴(Pasek & Paul)**이 선사하는 가슴 시린 치유와 연대의 마스터피스.\n\n")
    readme.append("## 🌟 웹 뷰어 바로가기\n\n")
    readme.append("- 📱 **인터랙티브 웹 뷰어 (GitHub Pages)**: [디어 에반 핸슨 뷰어 바로가기](./index.html)\n")
    readme.append("- 📖 **전곡 단일 통합 완본 (Single Document)**: [`deh_complete.md`](./deh_complete.md)\n")
    readme.append("- 🏠 **뮤지컬 라이브러리 홈**: [전체 라이브러리 포털](../index.html)\n\n")
    readme.append("---\n\n")

    readme.append("## 🎭 주요 등장인물 및 캐스트 (Original Broadway Cast)\n\n")
    readme.append("- **에반 핸슨 (Evan Hansen)**: 벤 플랫 (Ben Platt) — 극심한 불안장애와 소외감을 겪는 고등학생, 토니상 남우주연상 수상\n")
    readme.append("- **조에 머피 (Zoe Murphy)**: 로라 드레이퍼스 (Laura Dreyfuss) — 오빠 코너의 폭력에 상처받은 여동생이자 에반의 첫사랑\n")
    readme.append("- **하이디 핸슨 (Heidi Hansen)**: 레이첼 베이 존스 (Rachel Bay Jones) — 아들을 홀로 키우며 헌신하는 싱글맘, 토니상 여우조연상 수상\n")
    readme.append("- **코너 머피 (Connor Murphy)**: 마이크 파이스트 (Mike Faist) — 분노와 약물로 방황하다 극단적 선택을 한 소년\n")
    readme.append("- **신시아 머피 (Cynthia Murphy)**: 제니퍼 로라 톰슨 (Jennifer Laura Thompson) — 아들의 죽음 후 에반의 편지에서 위로를 찾는 엄마\n")
    readme.append("- **래리 머피 (Larry Murphy)**: 마이클 박 (Michael Park) — 슬픔을 억누르며 가족을 지키려는 무뚝뚝한 아버지\n")
    readme.append("- **재러드 클라인먼 (Jared Kleinman)**: 윌 롤랜드 (Will Roland) — 에반의 가짜 이메일 조작을 돕는 유쾌한 패밀리 프렌드\n")
    readme.append("- **알라나 벡 (Alana Beck)**: 크리스톨린 로이드 (Kristolyn Lloyd) — 코너 프로젝트를 조직하는 열정적인 모범생\n\n")
    readme.append("---\n\n")

    readme.append("## 📜 전곡 트랙리스트 (Tracklist)\n\n")
    readme.append("### 🔵 제1막 (Act I)\n\n")
    for s in DEH_SONGS[:8]:
        chars = ", ".join(s.get("characters_kr", []))
        readme.append(f"- **{s['id']:02d}. [{s['title']} ({s['title_kr']})](./act1/{s['filename']})** — *{chars}*\n")

    readme.append("\n### 🔷 제2막 (Act II)\n\n")
    for s in DEH_SONGS[8:]:
        chars = ", ".join(s.get("characters_kr", []))
        readme.append(f"- **{s['id']:02d}. [{s['title']} ({s['title_kr']})](./act2/{s['filename']})** — *{chars}*\n")

    readme_path = os.path.join(base_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.writelines(readme)
    print(f"Generated: {readme_path}\n")

    # 6. Generate Standalone Interactive Web Viewer (dear_evan_hansen/index.html)
    print("=== [6/6] Generating dear_evan_hansen/index.html ===")
    json_data_for_web = json.dumps(DEH_SONGS, ensure_ascii=False)

    html_content = f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>뮤지컬 《디어 에반 핸슨 (Dear Evan Hansen)》 전곡 영한 대역 뷰어</title>
  <style>
    :root {{
      --bg: #090e17;
      --sidebar-bg: #0d1522;
      --card-bg: #121c2c;
      --sky-blue: #00a8ff;
      --sky-blue-glow: rgba(0, 168, 255, 0.35);
      --soft-cyan: #4cd137;
      --accent-yellow: #fbc531;
      --accent-coral: #e84118;
      --text: #e6edf8;
      --text-muted: #8395a7;
      --border: #1e2d42;
      --hover: #172437;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Apple SD Gothic Neo", sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
      display: flex;
      height: 100vh;
      overflow: hidden;
    }}

    /* Mobile Drawer Overlay */
    .drawer-overlay {{
      display: none;
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(4px);
      z-index: 998;
    }}

    /* Sidebar */
    #sidebar {{
      width: 340px;
      background: var(--sidebar-bg);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      z-index: 999;
      transition: transform 0.3s ease;
    }}
    .sidebar-header {{
      padding: 18px 16px;
      border-bottom: 1px solid var(--border);
      background: #090f1a;
      text-align: center;
      position: relative;
    }}
    .sidebar-header .home-link {{
      display: inline-block;
      margin-bottom: 8px;
      font-size: 0.75rem;
      color: var(--sky-blue);
      text-decoration: none;
      padding: 3px 8px;
      background: rgba(0, 168, 255, 0.1);
      border-radius: 4px;
      border: 1px solid rgba(0, 168, 255, 0.25);
      transition: all 0.2s;
    }}
    .sidebar-header .home-link:hover {{
      background: var(--sky-blue);
      color: #000;
    }}
    .sidebar-header h1 {{
      font-size: 1.25rem;
      background: linear-gradient(135deg, #00a8ff 0%, #00d2d3 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      font-weight: 900;
      letter-spacing: 0.5px;
    }}
    .sidebar-header p {{
      font-size: 0.78rem;
      color: var(--text-muted);
      margin-top: 4px;
    }}
    .close-drawer-btn {{
      display: none;
      position: absolute;
      top: 14px;
      right: 14px;
      background: transparent;
      border: none;
      color: #fff;
      font-size: 1.5rem;
      cursor: pointer;
    }}
    .search-box {{
      padding: 12px 14px;
      border-bottom: 1px solid var(--border);
    }}
    .search-box input {{
      width: 100%;
      padding: 8px 12px;
      background: #111b2b;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: #fff;
      font-size: 0.85rem;
      outline: none;
      transition: border-color 0.2s;
    }}
    .search-box input:focus {{
      border-color: var(--sky-blue);
      box-shadow: 0 0 8px var(--sky-blue-glow);
    }}
    .act-tabs {{
      display: flex;
      padding: 6px 10px;
      gap: 6px;
      background: #090f1a;
      border-bottom: 1px solid var(--border);
    }}
    .act-tab {{
      flex: 1;
      padding: 7px 4px;
      background: transparent;
      border: 1px solid transparent;
      border-radius: 6px;
      color: var(--text-muted);
      font-size: 0.74rem;
      cursor: pointer;
      text-align: center;
      transition: all 0.2s;
      white-space: nowrap;
    }}
    .act-tab.active {{
      background: rgba(0, 168, 255, 0.15);
      color: var(--sky-blue);
      border-color: rgba(0, 168, 255, 0.4);
      font-weight: 700;
    }}
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
      background: #0f1826;
    }}
    .song-item:hover {{
      background: var(--hover);
      border-color: rgba(0, 168, 255, 0.3);
    }}
    .song-item.active {{
      background: rgba(0, 168, 255, 0.15);
      border-color: var(--sky-blue);
      box-shadow: 0 0 10px rgba(0, 168, 255, 0.2);
    }}
    .song-badge-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 3px;
    }}
    .song-num {{
      font-size: 0.72rem;
      color: var(--accent-yellow);
      font-weight: 700;
    }}
    .song-act-tag {{
      font-size: 0.65rem;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 600;
      background: rgba(0, 168, 255, 0.12);
      color: var(--sky-blue);
    }}
    .song-title {{
      font-size: 0.88rem;
      font-weight: 700;
      color: #fff;
    }}
    .song-title-kr {{
      font-size: 0.78rem;
      color: var(--text-muted);
    }}

    /* Main Content Area */
    #main {{
      flex: 1;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      background: var(--bg);
      position: relative;
    }}
    .top-bar {{
      padding: 12px 24px;
      border-bottom: 1px solid var(--border);
      background: #0d1522;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .mobile-menu-btn {{
      display: none;
      background: transparent;
      border: 1px solid var(--border);
      color: var(--sky-blue);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 1.1rem;
      cursor: pointer;
    }}
    .view-toggles {{
      display: flex;
      gap: 8px;
    }}
    .view-btn {{
      padding: 6px 14px;
      background: #121c2c;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: var(--text-muted);
      font-size: 0.8rem;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .view-btn.active {{
      background: var(--sky-blue);
      color: #000;
      font-weight: 700;
      border-color: var(--sky-blue);
      box-shadow: 0 0 10px var(--sky-blue-glow);
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
      color: var(--sky-blue);
      margin-left: 10px;
      font-size: 1.3rem;
      font-weight: 600;
    }}
    .song-meta-box {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 10px;
      font-size: 0.82rem;
      color: var(--text-muted);
    }}
    .song-meta-item strong {{
      color: #fff;
    }}
    .synopsis-box {{
      background: var(--card-bg);
      border-left: 4px solid var(--sky-blue);
      padding: 16px 20px;
      border-radius: 0 8px 8px 0;
      margin-bottom: 20px;
      font-size: 0.95rem;
      line-height: 1.7;
      color: #d1dcf0;
    }}
    .notes-box {{
      background: #0f1927;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px 20px;
      margin-bottom: 30px;
    }}
    .notes-box h4 {{
      font-size: 0.9rem;
      color: var(--accent-yellow);
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .notes-box ul {{
      padding-left: 18px;
      font-size: 0.88rem;
      color: #a4b4cc;
      line-height: 1.65;
    }}
    .notes-box li {{
      margin-bottom: 6px;
    }}
    .stanza-block {{
      background: #0e1724;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px 24px;
      margin-bottom: 24px;
    }}
    .speaker-tag {{
      display: inline-block;
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--sky-blue);
      background: rgba(0, 168, 255, 0.1);
      padding: 4px 10px;
      border-radius: 4px;
      margin-bottom: 16px;
      border: 1px solid rgba(0, 168, 255, 0.25);
    }}
    .lyric-pair {{
      margin-bottom: 14px;
      padding-bottom: 10px;
      border-bottom: 1px dashed rgba(30, 45, 66, 0.7);
    }}
    .lyric-pair:last-child {{
      margin-bottom: 0;
      padding-bottom: 0;
      border-bottom: none;
    }}
    .lyric-en {{
      font-size: 1.02rem;
      font-weight: 600;
      color: #ffffff;
      margin-bottom: 4px;
      letter-spacing: 0.2px;
    }}
    .lyric-kr {{
      font-size: 0.95rem;
      color: #9cb1ce;
      line-height: 1.55;
    }}

    /* View modes */
    .mode-kr-only .lyric-en {{ display: none; }}
    .mode-en-only .lyric-kr {{ display: none; }}

    /* Responsive Design */
    @media (max-width: 768px) {{
      #sidebar {{
        position: fixed;
        top: 0;
        bottom: 0;
        left: 0;
        transform: translateX(-100%);
        width: 82%;
        max-width: 320px;
        box-shadow: 10px 0 30px rgba(0, 0, 0, 0.7);
      }}
      #sidebar.open {{
        transform: translateX(0);
      }}
      .drawer-overlay.active {{
        display: block;
      }}
      .mobile-menu-btn {{
        display: inline-block;
      }}
      .close-drawer-btn {{
        display: block;
      }}
      .top-bar {{
        padding: 10px 16px;
      }}
      .song-content {{
        padding: 20px 16px;
      }}
      .song-header h2 {{
        font-size: 1.35rem;
      }}
      .song-header h2 .kr-title {{
        display: block;
        margin-left: 0;
        margin-top: 4px;
        font-size: 1.05rem;
      }}
      .stanza-block {{
        padding: 16px;
      }}
      .lyric-en {{
        font-size: 0.95rem;
      }}
      .lyric-kr {{
        font-size: 0.88rem;
      }}
    }}
  </style>
</head>
<body>

  <!-- Mobile Drawer Overlay -->
  <div class="drawer-overlay" id="drawerOverlay" onclick="closeSidebar()"></div>

  <!-- Sidebar -->
  <div id="sidebar">
    <div class="sidebar-header">
      <a href="../index.html" class="home-link">◀ 뮤지컬 도서관 홈</a>
      <button class="close-drawer-btn" onclick="closeSidebar()">✕</button>
      <h1>DEAR EVAN HANSEN</h1>
      <p>전 14곡 공식 가사 & 영한 대역 뷰어</p>
    </div>
    <div class="search-box">
      <input type="text" id="searchInput" placeholder="곡 제목, 가사, 등장인물 검색..." oninput="renderSongList()">
    </div>
    <div class="act-tabs">
      <button class="act-tab active" id="tabAll" onclick="setActFilter('all')">전체 (14)</button>
      <button class="act-tab" id="tabAct1" onclick="setActFilter(1)">1막 (8)</button>
      <button class="act-tab" id="tabAct2" onclick="setActFilter(2)">2막 (6)</button>
    </div>
    <div class="song-list" id="songListContainer"></div>
  </div>

  <!-- Main Content -->
  <div id="main">
    <div class="top-bar">
      <div style="display: flex; align-items: center; gap: 12px;">
        <button class="mobile-menu-btn" onclick="openSidebar()">☰ 목록</button>
        <div style="font-size: 0.85rem; color: var(--accent-yellow); font-weight: 700;" id="topBarTrackInfo">Act 1 · Track 01 / 14</div>
      </div>
      <div class="view-toggles">
        <button class="view-btn active" id="btnBilingual" onclick="setViewMode('bilingual')">영한 대역</button>
        <button class="view-btn" id="btnKr" onclick="setViewMode('kr')">한국어만</button>
        <button class="view-btn" id="btnEn" onclick="setViewMode('en')">English Only</button>
      </div>
    </div>
    <div class="song-content" id="songContent"></div>
  </div>

  <script>
    const songsData = {json_data_for_web};
    let currentSongId = 1;
    let currentAct = 'all';
    let currentMode = 'bilingual';

    function init() {{
      renderSongList();
      loadSong(1);
    }}

    function openSidebar() {{
      document.getElementById('sidebar').classList.add('open');
      document.getElementById('drawerOverlay').classList.add('active');
    }}

    function closeSidebar() {{
      document.getElementById('sidebar').classList.remove('open');
      document.getElementById('drawerOverlay').classList.remove('active');
    }}

    function setActFilter(act) {{
      currentAct = act;
      document.getElementById('tabAll').classList.toggle('active', act === 'all');
      document.getElementById('tabAct1').classList.toggle('active', act === 1);
      document.getElementById('tabAct2').classList.toggle('active', act === 2);
      renderSongList();
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
        if (currentAct !== 'all' && s.act !== currentAct) return;
        if (query) {{
          const matchTitle = s.title.toLowerCase().includes(query) || s.title_kr.toLowerCase().includes(query);
          const matchChar = (s.characters_en || []).some(c => c.toLowerCase().includes(query)) ||
                            (s.characters_kr || []).some(c => c.toLowerCase().includes(query));
          const matchLyric = s.stanzas.some(st => 
            st.lines_en.some(l => l.toLowerCase().includes(query)) || 
            st.lines_kr.some(l => l.toLowerCase().includes(query))
          );
          if (!matchTitle && !matchChar && !matchLyric) return;
        }}

        const item = document.createElement('div');
        item.className = 'song-item' + (s.id === currentSongId ? ' active' : '');
        item.onclick = () => {{
          loadSong(s.id);
          closeSidebar();
        }};

        item.innerHTML = `
          <div class="song-badge-row">
            <span class="song-num">Track ${{String(s.id).padStart(2, '0')}}</span>
            <span class="song-act-tag">${{s.act}}막</span>
          </div>
          <div class="song-title">${{s.title}}</div>
          <div class="song-title-kr">${{s.title_kr}}</div>
        `;
        container.appendChild(item);
      }});
    }}

    function loadSong(id) {{
      currentSongId = id;
      renderSongList();

      const song = songsData.find(s => s.id === id);
      if (!song) return;

      document.getElementById('topBarTrackInfo').textContent = `Act ${{song.act}} · Track ${{String(song.id).padStart(2, '0')}} / 14`;

      let notesHtml = '';
      if (song.notes && song.notes.length > 0) {{
        notesHtml = `
          <div class="notes-box">
            <h4>💡 감상 포인트 및 주석 (Key Notes & Themes)</h4>
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

      const charsKr = (song.characters_kr || []).join(', ');
      const charsEn = (song.characters_en || []).join(', ');

      const html = `
        <div class="song-header">
          <h2>${{String(song.id).padStart(2, '0')}}. ${{song.title}} <span class="kr-title">${{song.title_kr}}</span></h2>
          <div class="song-meta-box">
            <div class="song-meta-item"><strong>막(Act):</strong> 제${{song.act}}막</div>
            <div class="song-meta-item"><strong>등장인물/보컬:</strong> ${{charsKr}} (${{charsEn}})</div>
          </div>
        </div>
        <div class="synopsis-box">
          <strong>📖 드라마적 배경:</strong> ${{song.synopsis}}
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

    web_file = os.path.join(base_dir, "index.html")
    with open(web_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated: {web_file}\n")
    print("=== Dear Evan Hansen Build Complete! ===")

if __name__ == "__main__":
    main()
