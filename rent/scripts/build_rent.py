# -*- coding: utf-8 -*-
"""
RENT Musical Archive & Web Viewer Builder
Generates:
- rent/data/rent_songs.json
- rent/act1/*.md (18 tracks)
- rent/act2/*.md (14 tracks)
- rent/rent_complete.md
- rent/README.md
- rent/index.html (Interactive Web Viewer)
"""

import os
import json
import re
import sys

from build_rent_data import RENT_SONGS

FILE_SLUGS = [
    # Act 1 (1-18)
    "01_tune_up_a_rent",
    "02_youll_see",
    "03_one_song_glory",
    "04_light_my_candle",
    "05_today_4_u",
    "06_youll_see_boys",
    "07_tango_maureen",
    "08_life_support",
    "09_out_tonight",
    "10_another_day",
    "11_will_i",
    "12_on_the_street",
    "13_santa_fe",
    "14_ill_cover_you",
    "15_we_re_okay",
    "16_christmas_bells",
    "17_over_the_moon",
    "18_la_vie_boheme",
    # Act 2 (19-32)
    "19_seasons_of_love",
    "20_happy_new_year",
    "21_take_me_or_leave_me",
    "22_without_you",
    "23_seasons_of_love_b",
    "24_ill_cover_you_reprise",
    "25_halloween",
    "26_goodbye_love",
    "27_what_you_own",
    "28_finale_a",
    "29_your_eyes",
    "30_finale_b",
    "31_love_heals",
    "32_seasons_of_love_reprise"
]

def slugify_anchor(title):
    cleaned = re.sub(r'[^a-zA-Z0-9\s-]', '', title).lower()
    return re.sub(r'[\s_]+', '-', cleaned).strip('-')

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assert len(RENT_SONGS) == 32, f"Expected 32 songs, got {len(RENT_SONGS)}"

    for idx, song in enumerate(RENT_SONGS):
        slug = FILE_SLUGS[idx]
        act_dir = f"act{song['act']}"
        song["slug"] = slug
        song["filename"] = f"{slug}.md"
        song["rel_path"] = f"{act_dir}/{slug}.md"

    # 1. Verify 1:1 Line Matching
    print("=== [1/6] Verifying 1:1 Line Matching ===")
    total_lines = 0
    mismatches = 0
    for song in RENT_SONGS:
        for s_idx, st in enumerate(song["stanzas"]):
            len_en = len(st["lines_en"])
            len_kr = len(st["lines_kr"])
            total_lines += len_en
            if len_en != len_kr:
                print(f"[MISMATCH] Song #{song['id']} ({song['title']}) Stanza #{s_idx+1}: EN({len_en}) != KR({len_kr})")
                mismatches += 1

    if mismatches > 0:
        raise ValueError(f"Found {mismatches} stanza mismatches! Aborting build.")
    print(f"Verification Passed! 32 songs, {total_lines} lines verified 100% aligned 1:1.\n")

    # 2. Save JSON Database
    print("=== [2/6] Writing rent/data/rent_songs.json ===")
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    json_path = os.path.join(data_dir, "rent_songs.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(RENT_SONGS, f, ensure_ascii=False, indent=2)
    print(f"Saved: {json_path}\n")

    # 3. Generate Individual Markdown Track Files
    print("=== [3/6] Generating Individual Markdown Track Files ===")
    os.makedirs(os.path.join(base_dir, "act1"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "act2"), exist_ok=True)

    for idx, song in enumerate(RENT_SONGS):
        file_path = os.path.join(base_dir, song["rel_path"])
        act = song["act"]
        act_label = f"제{act}막 (Act {act})"

        prev_song = RENT_SONGS[idx - 1] if idx > 0 else None
        next_song = RENT_SONGS[idx + 1] if idx < len(RENT_SONGS) - 1 else None

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
            md.append("## 💡 감상 포인트 및 주석 (Key Notes & 90s NYC Culture)\n\n")
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

    print(f"Generated 32 individual markdown files in rent/act1/ and rent/act2/\n")

    # 4. Generate Master Complete Document
    print("=== [4/6] Generating rent/rent_complete.md ===")
    comp = []
    comp.append("# 🎸 뮤지컬 《렌트 (RENT)》 전 32곡 공식 원본 가사 및 한국어 전곡 대역·해설집\n\n")
    comp.append("**작사/작곡/극본**: 조나단 라슨 (Jonathan Larson)\n")
    comp.append("**기반 원작**: 자코모 푸치니의 오페라 《라 보엠 (La Bohème)》\n")
    comp.append("**초연 주연**: 앤서니 랩 (마크), 아담 파스칼 (로저), 다프네 루빈-베가 (미미), 제시 L. 마틴 (콜린스), 윌슨 저메인 에레디아 (엔젤), 이디나 멘젤 (모린)\n")
    comp.append("**수상 이력**: 퓰리처상 드라마 부문 수상, 제50회 토니상 4관왕 (최우수 작품상, 각본상, 작곡상, 남우조연상)\n")
    comp.append("**특징**: 90년대 뉴욕 이스트 빌리지 청춘들의 사랑과 예술, 에이즈의 비극을 록 오페라로 승화시킨 현대 뮤지컬의 혁명작. 전 32곡 전수 1:1 대역 수록.\n\n")
    comp.append("---\n\n")

    comp.append("## 📜 전곡 목차 (Table of Contents)\n\n")
    comp.append("### 제1막 (Act I: 크리스마스 이브와 보헤미안의 연대)\n\n")
    for s in RENT_SONGS[:18]:
        anchor = f"{s['id']:02d}-{slugify_anchor(s['title'])}"
        comp.append(f"{s['id']:02d}. [{s['title']} ({s['title_kr']})](#{anchor})\n")

    comp.append("\n### 제2막 (Act II: 52만 5천 6백 분의 사랑과 이별, 그리고 생명의 부활)\n\n")
    for s in RENT_SONGS[18:]:
        anchor = f"{s['id']:02d}-{slugify_anchor(s['title'])}"
        comp.append(f"{s['id']:02d}. [{s['title']} ({s['title_kr']})](#{anchor})\n")

    comp.append("\n---\n\n")

    for s in RENT_SONGS:
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

    complete_path = os.path.join(base_dir, "rent_complete.md")
    with open(complete_path, "w", encoding="utf-8") as f:
        f.writelines(comp)
    print(f"Generated: {complete_path}\n")

    # 5. Generate README.md
    print("=== [5/6] Generating rent/README.md ===")
    readme = []
    readme.append("# 🎸 뮤지컬 《렌트 (RENT)》 공식 전곡 가사 및 영한 대역 아카이브\n\n")
    readme.append("> **\"No day but today!\"**\n")
    readme.append("> **\"How do you measure a year in the life? Measure in love!\"**\n")
    readme.append("> 퓰리처상 드라마 부문 & 토니상 4관왕에 빛나는 90년대 브로드웨이 불멸의 혁명작!\n")
    readme.append("> 작곡가 조나단 라슨이 목숨과 맞바꾸어 탄생시킨 세기말 뉴욕 청춘들의 가난과 열정, 에이즈와 사랑의 대서사시 전 32곡 전수 완역 아카이브.\n\n")
    readme.append("## 🌟 웹 뷰어 바로가기\n\n")
    readme.append("- 📱 **인터랙티브 웹 뷰어 (GitHub Pages)**: [렌트 뷰어 바로가기](./index.html)\n")
    readme.append("- 📖 **전곡 단일 통합 완본 (Single Document)**: [`rent_complete.md`](./rent_complete.md)\n")
    readme.append("- 🏠 **뮤지컬 라이브러리 홈**: [전체 라이브러리 포털](../index.html)\n\n")
    readme.append("---\n\n")

    readme.append("## 🎭 주요 등장인물 및 배역 (Characters)\n\n")
    readme.append("- **마크 코헨 (Mark Cohen)**: 다큐멘터리 영화를 찍는 가난한 유대인 영화감독, 보헤미안 친구들의 삶을 기록하는 관찰자이자 화자\n")
    readme.append("- **로저 데이비스 (Roger Davis)**: 전직 록밴드 프론트맨이자 기타리스트, 에이즈 진단 후 세상과 단절했다가 미미를 만나 다시 사랑을 배운다\n")
    readme.append("- **미미 마르케즈 (Mimi Marquez)**: 클럽 댄서이자 에이즈 환자, 삶의 마지막 순간까지 열정적으로 오늘을 살아가는 열아홉 살 소녀\n")
    readme.append("- **톰 콜린스 (Tom Collins)**: 컴퓨터 천재이자 철학 교수, 길거리에서 엔젤을 만나 운명적인 사랑을 나눈다\n")
    readme.append("- **엔젤 듀못 슈나드 (Angel Dumott Schunard)**: 거리의 드랙퀸 드러머이자 친구들에게 무한한 사랑과 온기를 베푸는 수호천사\n")
    readme.append("- **모린 존슨 (Maureen Johnson)**: 전위 예술가이자 마크의 전 여친, 자유분방하고 매혹적인 퍼포먼스 아티스트\n")
    readme.append("- **조앤 제퍼슨 (Joanne Jefferson)**: 하버드 로스쿨 출신의 인권 변호사, 모린의 현 여친\n")
    readme.append("- **베니 (Benjamin Coffin III)**: 마크와 로저의 옛 룸메이트였으나 부잣집 사위가 되어 건물을 매입한 집주인\n\n")
    readme.append("---\n\n")

    readme.append("## 📜 전곡 트랙리스트 (Tracklist)\n\n")
    readme.append("### 🔥 제1막 (Act I)\n\n")
    for s in RENT_SONGS[:18]:
        chars = ", ".join(s.get("characters_kr", []))
        readme.append(f"- **{s['id']:02d}. [{s['title']} ({s['title_kr']})](./act1/{s['filename']})** — *{chars}*\n")

    readme.append("\n### 💖 제2막 (Act II)\n\n")
    for s in RENT_SONGS[18:]:
        chars = ", ".join(s.get("characters_kr", []))
        readme.append(f"- **{s['id']:02d}. [{s['title']} ({s['title_kr']})](./act2/{s['filename']})** — *{chars}*\n")

    readme_path = os.path.join(base_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.writelines(readme)
    print(f"Generated: {readme_path}\n")

    # 6. Generate Standalone Interactive Web Viewer (rent/index.html)
    print("=== [6/6] Generating rent/index.html ===")
    json_data_for_web = json.dumps(RENT_SONGS, ensure_ascii=False)

    html_content = f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>뮤지컬 《렌트 (RENT)》 전곡 영한 대역 뷰어</title>
  <style>
    :root {{
      --bg: #100808;
      --sidebar-bg: #180c0c;
      --card-bg: #221212;
      --rent-red: #eb2f06;
      --rent-red-glow: rgba(235, 47, 6, 0.4);
      --rent-purple: #9b59b6;
      --rent-yellow: #f1c40f;
      --text: #fae8e8;
      --text-muted: #b89898;
      --border: #3d1c1c;
      --hover: #2d1616;
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
      background: #120606;
      text-align: center;
      position: relative;
    }}
    .sidebar-header .home-link {{
      display: inline-block;
      margin-bottom: 8px;
      font-size: 0.75rem;
      color: var(--rent-red);
      text-decoration: none;
      padding: 3px 8px;
      background: rgba(235, 47, 6, 0.1);
      border-radius: 4px;
      border: 1px solid rgba(235, 47, 6, 0.25);
      transition: all 0.2s;
    }}
    .sidebar-header .home-link:hover {{
      background: var(--rent-red);
      color: #fff;
    }}
    .sidebar-header h1 {{
      font-size: 1.25rem;
      background: linear-gradient(135deg, #eb2f06 0%, #9b59b6 100%);
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
      background: #1e0e0e;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: #fff;
      font-size: 0.85rem;
      outline: none;
      transition: border-color 0.2s;
    }}
    .search-box input:focus {{
      border-color: var(--rent-red);
      box-shadow: 0 0 8px var(--rent-red-glow);
    }}
    .act-tabs {{
      display: flex;
      padding: 6px 10px;
      gap: 6px;
      background: #120606;
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
      background: rgba(235, 47, 6, 0.15);
      color: var(--rent-red);
      border-color: rgba(235, 47, 6, 0.4);
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
      background: #1c0e0e;
    }}
    .song-item:hover {{
      background: var(--hover);
      border-color: rgba(235, 47, 6, 0.3);
    }}
    .song-item.active {{
      background: rgba(235, 47, 6, 0.15);
      border-color: var(--rent-red);
      box-shadow: 0 0 10px rgba(235, 47, 6, 0.2);
    }}
    .song-badge-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 3px;
    }}
    .song-num {{
      font-size: 0.72rem;
      color: var(--rent-yellow);
      font-weight: 700;
    }}
    .song-act-tag {{
      font-size: 0.65rem;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 600;
      background: rgba(235, 47, 6, 0.12);
      color: var(--rent-red);
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
      background: #180c0c;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .mobile-menu-btn {{
      display: none;
      background: transparent;
      border: 1px solid var(--border);
      color: var(--rent-red);
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
      background: #221212;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: var(--text-muted);
      font-size: 0.8rem;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .view-btn.active {{
      background: var(--rent-red);
      color: #fff;
      font-weight: 700;
      border-color: var(--rent-red);
      box-shadow: 0 0 10px var(--rent-red-glow);
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
      color: var(--rent-red);
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
      border-left: 4px solid var(--rent-red);
      padding: 16px 20px;
      border-radius: 0 8px 8px 0;
      margin-bottom: 20px;
      font-size: 0.95rem;
      line-height: 1.7;
      color: #fae1e1;
    }}
    .notes-box {{
      background: #1e0f0f;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px 20px;
      margin-bottom: 30px;
    }}
    .notes-box h4 {{
      font-size: 0.9rem;
      color: var(--rent-yellow);
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .notes-box ul {{
      padding-left: 18px;
      font-size: 0.88rem;
      color: #d1b4b4;
      line-height: 1.65;
    }}
    .notes-box li {{
      margin-bottom: 6px;
    }}
    .stanza-block {{
      background: #1a0d0d;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px 24px;
      margin-bottom: 24px;
    }}
    .speaker-tag {{
      display: inline-block;
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--rent-purple);
      background: rgba(155, 89, 182, 0.1);
      padding: 4px 10px;
      border-radius: 4px;
      margin-bottom: 16px;
      border: 1px solid rgba(155, 89, 182, 0.25);
    }}
    .lyric-pair {{
      margin-bottom: 14px;
      padding-bottom: 10px;
      border-bottom: 1px dashed rgba(61, 28, 28, 0.7);
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
      color: #cdaaaa;
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
      <h1>RENT</h1>
      <p>전 32곡 공식 가사 & 영한 대역 뷰어</p>
    </div>
    <div class="search-box">
      <input type="text" id="searchInput" placeholder="곡 제목, 가사, 등장인물 검색..." oninput="renderSongList()">
    </div>
    <div class="act-tabs">
      <button class="act-tab active" id="tabAll" onclick="setActFilter('all')">전체 (32)</button>
      <button class="act-tab" id="tabAct1" onclick="setActFilter(1)">1막 (18)</button>
      <button class="act-tab" id="tabAct2" onclick="setActFilter(2)">2막 (14)</button>
    </div>
    <div class="song-list" id="songListContainer"></div>
  </div>

  <!-- Main Content -->
  <div id="main">
    <div class="top-bar">
      <div style="display: flex; align-items: center; gap: 12px;">
        <button class="mobile-menu-btn" onclick="openSidebar()">☰ 목록</button>
        <div style="font-size: 0.85rem; color: var(--rent-yellow); font-weight: 700;" id="topBarTrackInfo">Act 1 · Track 01 / 32</div>
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

      document.getElementById('topBarTrackInfo').textContent = `Act ${{song.act}} · Track ${{String(song.id).padStart(2, '0')}} / 32`;

      let notesHtml = '';
      if (song.notes && song.notes.length > 0) {{
        notesHtml = `
          <div class="notes-box">
            <h4>💡 감상 포인트 및 주석 (Key Notes & 90s NYC Culture)</h4>
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
    print("=== RENT Build Complete! ===")

if __name__ == "__main__":
    main()
