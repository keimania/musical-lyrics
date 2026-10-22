# -*- coding: utf-8 -*-
"""
Hadestown Musical Archive & Web Viewer Builder
Generates:
- hadestown/data/hadestown_songs.json
- hadestown/act1/*.md (16 tracks)
- hadestown/act2/*.md (17 tracks)
- hadestown/hadestown_complete.md
- hadestown/README.md
- hadestown/index.html (Interactive Web Viewer)
"""

import os
import json
import re
import sys

from build_hadestown_data import HADESTOWN_SONGS

FILE_SLUGS = [
    # Act 1 (1-16)
    "01_road_to_hell",
    "02_any_way_the_wind_blows",
    "03_come_home_with_me",
    "04_wedding_song",
    "05_epic_i",
    "06_livin_it_up_on_top",
    "07_all_ive_ever_known",
    "08_way_down_hadestown",
    "09_a_gathering_storm",
    "10_epic_ii",
    "11_chant",
    "12_hey_little_songbird",
    "13_when_the_chips_are_down",
    "14_gone_im_gone",
    "15_wait_for_me",
    "16_why_we_build_the_wall",
    # Act 2 (17-33)
    "17_our_lady_of_the_underground",
    "18_way_down_hadestown_reprise",
    "19_flowers",
    "20_come_home_with_me_reprise",
    "21_papers",
    "22_nothing_changes",
    "23_if_its_true",
    "24_how_long",
    "25_chant_reprise",
    "26_epic_iii",
    "27_promises",
    "28_word_to_the_wise",
    "29_his_kiss_the_riot",
    "30_wait_for_me_reprise",
    "31_doubt_comes_in",
    "32_road_to_hell_reprise",
    "33_we_raise_our_cups"
]

def slugify_anchor(title):
    cleaned = re.sub(r'[^a-zA-Z0-9\s-]', '', title).lower()
    return re.sub(r'[\s_]+', '-', cleaned).strip('-')

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assert len(HADESTOWN_SONGS) == 33, f"Expected 33 songs, got {len(HADESTOWN_SONGS)}"

    for idx, song in enumerate(HADESTOWN_SONGS):
        slug = FILE_SLUGS[idx]
        act_dir = f"act{song['act']}"
        song["slug"] = slug
        song["filename"] = f"{slug}.md"
        song["rel_path"] = f"{act_dir}/{slug}.md"

    # 1. Verify 1:1 Line Matching
    print("=== [1/6] Verifying 1:1 Line Matching ===")
    total_lines = 0
    mismatches = 0
    for song in HADESTOWN_SONGS:
        for s_idx, st in enumerate(song["stanzas"]):
            len_en = len(st["lines_en"])
            len_kr = len(st["lines_kr"])
            total_lines += len_en
            if len_en != len_kr:
                print(f"[MISMATCH] Song #{song['id']} ({song['title']}) Stanza #{s_idx+1}: EN({len_en}) != KR({len_kr})")
                mismatches += 1

    if mismatches > 0:
        raise ValueError(f"Found {mismatches} stanza mismatches! Aborting build.")
    print(f"Verification Passed! 33 songs, {total_lines} lines verified 100% aligned 1:1.\n")

    # 2. Save JSON Database
    print("=== [2/6] Writing hadestown/data/hadestown_songs.json ===")
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    json_path = os.path.join(data_dir, "hadestown_songs.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(HADESTOWN_SONGS, f, ensure_ascii=False, indent=2)
    print(f"Saved: {json_path}\n")

    # 3. Generate Individual Markdown Track Files
    print("=== [3/6] Generating Individual Markdown Track Files ===")
    os.makedirs(os.path.join(base_dir, "act1"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "act2"), exist_ok=True)

    for idx, song in enumerate(HADESTOWN_SONGS):
        file_path = os.path.join(base_dir, song["rel_path"])
        act = song["act"]
        act_label = f"제{act}막 (Act {act})"

        prev_song = HADESTOWN_SONGS[idx - 1] if idx > 0 else None
        next_song = HADESTOWN_SONGS[idx + 1] if idx < len(HADESTOWN_SONGS) - 1 else None

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
            md.append("## 💡 감상 포인트 및 주석 (Key Notes & Mythology)\n\n")
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

    print(f"Generated 33 individual markdown files in hadestown/act1/ and hadestown/act2/\n")

    # 4. Generate Master Complete Document
    print("=== [4/6] Generating hadestown/hadestown_complete.md ===")
    comp = []
    comp.append("# 🪕 뮤지컬 《하데스타운 (Hadestown)》 전 33곡 공식 원본 가사 및 한국어 전곡 대역·해설집\n\n")
    comp.append("**작사/작곡/극본**: 아나이스 미첼 (Anaïs Mitchell)\n")
    comp.append("**연출**: 레이첼 차브킨 (Rachel Chavkin)\n")
    comp.append("**초연 주연**: 리브 카니 (오르페우스), 에바 노블자다 (에우리디케), 패트릭 페이지 (하데스), 앰버 그레이 (페르세포네), 앙드레 드 실즈 (헤르메스)\n")
    comp.append("**수상 이력**: 제73회 토니상 8관왕 (최우수 작품상, 연출상, 오리지널 스코어상, 남우조연상 등), 그래미 어워드 최우수 뮤지컬 앨범상 수상\n")
    comp.append("**특징**: 그리스 신화를 뉴올리언스 재즈와 포크 블루스로 재해석한 브로드웨이 불멸의 걸작. 전 33곡 전수 1:1 대역 및 신화/사회학적 해설 수록.\n\n")
    comp.append("---\n\n")

    comp.append("## 📜 전곡 목차 (Table of Contents)\n\n")
    comp.append("### 제1막 (Act I: 지상에서의 사랑과 지옥으로의 여정)\n\n")
    for s in HADESTOWN_SONGS[:16]:
        anchor = f"{s['id']:02d}-{slugify_anchor(s['title'])}"
        comp.append(f"{s['id']:02d}. [{s['title']} ({s['title_kr']})](#{anchor})\n")

    comp.append("\n### 제2막 (Act II: 지하의 혁명과 의심의 시련, 그리고 영원한 노래)\n\n")
    for s in HADESTOWN_SONGS[16:]:
        anchor = f"{s['id']:02d}-{slugify_anchor(s['title'])}"
        comp.append(f"{s['id']:02d}. [{s['title']} ({s['title_kr']})](#{anchor})\n")

    comp.append("\n---\n\n")

    for s in HADESTOWN_SONGS:
        anchor = f"{s['id']:02d}-{slugify_anchor(s['title'])}"
        comp.append(f"## <a id=\"{anchor}\"></a>{s['id']:02d}. {s['title']} ({s['title_kr']})\n\n")
        comp.append(f"- **막**: Act {s['act']} · Track {s['id']:02d}\n")
        chars_en = ", ".join(s.get("characters_en", []))
        chars_kr = ", ".join(s.get("characters_kr", []))
        comp.append(f"- **등장인물/보컬**: {chars_kr} ({chars_en})\n\n")
        comp.append(f"**신화적·드라마적 배경**: {s['synopsis']}\n\n")

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

    complete_path = os.path.join(base_dir, "hadestown_complete.md")
    with open(complete_path, "w", encoding="utf-8") as f:
        f.writelines(comp)
    print(f"Generated: {complete_path}\n")

    # 5. Generate README.md
    print("=== [5/6] Generating hadestown/README.md ===")
    readme = []
    readme.append("# 🪕 뮤지컬 《하데스타운 (Hadestown)》 공식 전곡 가사 및 영한 대역 아카이브\n\n")
    readme.append("> **\"Wait for me, I'm comin'!\"**\n")
    readme.append("> 제73회 토니상 8관왕 & 그래미 어워드 최우수 뮤지컬 앨범상 수상작!\n")
    readme.append("> 그리스 신화 속 오르페우스와 에우리디케의 사랑, 하데스와 페르세포네의 계절을 뉴올리언스 재즈와 포크 블루스로 빚어낸 현대 브로드웨이 최고의 시적 명작.\n\n")
    readme.append("## 🌟 웹 뷰어 바로가기\n\n")
    readme.append("- 📱 **인터랙티브 웹 뷰어 (GitHub Pages)**: [하데스타운 뷰어 바로가기](./index.html)\n")
    readme.append("- 📖 **전곡 단일 통합 완본 (Single Document)**: [`hadestown_complete.md`](./hadestown_complete.md)\n")
    readme.append("- 🏠 **뮤지컬 라이브러리 홈**: [전체 라이브러리 포털](../index.html)\n\n")
    readme.append("---\n\n")

    readme.append("## 🎭 주요 등장인물 및 캐스트 (Original Broadway Cast)\n\n")
    readme.append("- **오르페우스 (Orpheus)**: 리브 카니 (Reeve Carney) — 봄을 되돌릴 노래를 짓는 가난한 순수 예술가, 뤼라를 든 청년\n")
    readme.append("- **에우리디케 (Eurydice)**: 에바 노블자다 (Eva Noblezada) — 혹독한 추위와 배고픔 속에서 생존을 위해 지하로 내려간 방랑자\n")
    readme.append("- **하데스 (Hades)**: 패트릭 페이지 (Patrick Page) — 저승과 지하 광산을 통치하는 동굴 같은 초저음의 군주\n")
    readme.append("- **페르세포네 (Persephone)**: 앰버 그레이 (Amber Gray) — 여름과 봄의 여신이자 지하 세계의 자유분방한 안주인\n")
    readme.append("- **헤르메스 (Hermes)**: 앙드레 드 실즈 (André De Shields) — 옛이야기를 이끄는 전령의 신이자 인도자 (토니상 남우조연상 수상)\n")
    readme.append("- **운명의 세 여신 (The Fates)**: 주엘 블랙맨, 이베트 곤잘레스-나세르, 케이 트리니다드 — 인간의 귓가에 불안과 의심을 속삭이는 세 자매\n\n")
    readme.append("---\n\n")

    readme.append("## 📜 전곡 트랙리스트 (Tracklist)\n\n")
    readme.append("### 🍂 제1막 (Act I)\n\n")
    for s in HADESTOWN_SONGS[:16]:
        chars = ", ".join(s.get("characters_kr", []))
        readme.append(f"- **{s['id']:02d}. [{s['title']} ({s['title_kr']})](./act1/{s['filename']})** — *{chars}*\n")

    readme.append("\n### 🌿 제2막 (Act II)\n\n")
    for s in HADESTOWN_SONGS[16:]:
        chars = ", ".join(s.get("characters_kr", []))
        readme.append(f"- **{s['id']:02d}. [{s['title']} ({s['title_kr']})](./act2/{s['filename']})** — *{chars}*\n")

    readme_path = os.path.join(base_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.writelines(readme)
    print(f"Generated: {readme_path}\n")

    # 6. Generate Standalone Interactive Web Viewer (hadestown/index.html)
    print("=== [6/6] Generating hadestown/index.html ===")
    json_data_for_web = json.dumps(HADESTOWN_SONGS, ensure_ascii=False)

    html_content = f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>뮤지컬 《하데스타운 (Hadestown)》 전곡 영한 대역 뷰어</title>
  <style>
    :root {{
      --bg: #0e0a07;
      --sidebar-bg: #16100c;
      --card-bg: #201712;
      --hadestown-amber: #ff9f1a;
      --hadestown-amber-glow: rgba(255, 159, 26, 0.4);
      --hadestown-red: #e55039;
      --hadestown-bronze: #cd6133;
      --carnation-red: #ff3838;
      --text: #fbede4;
      --text-muted: #bda293;
      --border: #38251b;
      --hover: #291c15;
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
      background: #120b08;
      text-align: center;
      position: relative;
    }}
    .sidebar-header .home-link {{
      display: inline-block;
      margin-bottom: 8px;
      font-size: 0.75rem;
      color: var(--hadestown-amber);
      text-decoration: none;
      padding: 3px 8px;
      background: rgba(255, 159, 26, 0.1);
      border-radius: 4px;
      border: 1px solid rgba(255, 159, 26, 0.25);
      transition: all 0.2s;
    }}
    .sidebar-header .home-link:hover {{
      background: var(--hadestown-amber);
      color: #000;
    }}
    .sidebar-header h1 {{
      font-size: 1.25rem;
      background: linear-gradient(135deg, #ff9f1a 0%, #e55039 100%);
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
      background: #1c130e;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: #fff;
      font-size: 0.85rem;
      outline: none;
      transition: border-color 0.2s;
    }}
    .search-box input:focus {{
      border-color: var(--hadestown-amber);
      box-shadow: 0 0 8px var(--hadestown-amber-glow);
    }}
    .act-tabs {{
      display: flex;
      padding: 6px 10px;
      gap: 6px;
      background: #120b08;
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
      background: rgba(255, 159, 26, 0.15);
      color: var(--hadestown-amber);
      border-color: rgba(255, 159, 26, 0.4);
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
      background: #1a120c;
    }}
    .song-item:hover {{
      background: var(--hover);
      border-color: rgba(255, 159, 26, 0.3);
    }}
    .song-item.active {{
      background: rgba(255, 159, 26, 0.15);
      border-color: var(--hadestown-amber);
      box-shadow: 0 0 10px rgba(255, 159, 26, 0.2);
    }}
    .song-badge-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 3px;
    }}
    .song-num {{
      font-size: 0.72rem;
      color: var(--hadestown-amber);
      font-weight: 700;
    }}
    .song-act-tag {{
      font-size: 0.65rem;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 600;
      background: rgba(255, 159, 26, 0.12);
      color: var(--hadestown-amber);
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
      background: #16100c;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .mobile-menu-btn {{
      display: none;
      background: transparent;
      border: 1px solid var(--border);
      color: var(--hadestown-amber);
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
      background: #201712;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: var(--text-muted);
      font-size: 0.8rem;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .view-btn.active {{
      background: var(--hadestown-amber);
      color: #000;
      font-weight: 700;
      border-color: var(--hadestown-amber);
      box-shadow: 0 0 10px var(--hadestown-amber-glow);
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
      color: var(--hadestown-amber);
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
      border-left: 4px solid var(--hadestown-amber);
      padding: 16px 20px;
      border-radius: 0 8px 8px 0;
      margin-bottom: 20px;
      font-size: 0.95rem;
      line-height: 1.7;
      color: #f7e6dc;
    }}
    .notes-box {{
      background: #1c130e;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px 20px;
      margin-bottom: 30px;
    }}
    .notes-box h4 {{
      font-size: 0.9rem;
      color: var(--hadestown-amber);
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .notes-box ul {{
      padding-left: 18px;
      font-size: 0.88rem;
      color: #d1b8ab;
      line-height: 1.65;
    }}
    .notes-box li {{
      margin-bottom: 6px;
    }}
    .stanza-block {{
      background: #1a120c;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px 24px;
      margin-bottom: 24px;
    }}
    .speaker-tag {{
      display: inline-block;
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--hadestown-amber);
      background: rgba(255, 159, 26, 0.1);
      padding: 4px 10px;
      border-radius: 4px;
      margin-bottom: 16px;
      border: 1px solid rgba(255, 159, 26, 0.25);
    }}
    .lyric-pair {{
      margin-bottom: 14px;
      padding-bottom: 10px;
      border-bottom: 1px dashed rgba(56, 37, 27, 0.7);
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
      color: #cbb4a6;
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
      <h1>HADESTOWN</h1>
      <p>전 33곡 공식 가사 & 영한 대역 뷰어</p>
    </div>
    <div class="search-box">
      <input type="text" id="searchInput" placeholder="곡 제목, 가사, 등장인물 검색..." oninput="renderSongList()">
    </div>
    <div class="act-tabs">
      <button class="act-tab active" id="tabAll" onclick="setActFilter('all')">전체 (33)</button>
      <button class="act-tab" id="tabAct1" onclick="setActFilter(1)">1막 (16)</button>
      <button class="act-tab" id="tabAct2" onclick="setActFilter(2)">2막 (17)</button>
    </div>
    <div class="song-list" id="songListContainer"></div>
  </div>

  <!-- Main Content -->
  <div id="main">
    <div class="top-bar">
      <div style="display: flex; align-items: center; gap: 12px;">
        <button class="mobile-menu-btn" onclick="openSidebar()">☰ 목록</button>
        <div style="font-size: 0.85rem; color: var(--hadestown-amber); font-weight: 700;" id="topBarTrackInfo">Act 1 · Track 01 / 33</div>
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

      document.getElementById('topBarTrackInfo').textContent = `Act ${{song.act}} · Track ${{String(song.id).padStart(2, '0')}} / 33`;

      let notesHtml = '';
      if (song.notes && song.notes.length > 0) {{
        notesHtml = `
          <div class="notes-box">
            <h4>💡 감상 포인트 및 주석 (Key Notes & Mythology)</h4>
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
          <strong>📖 신화적·드라마적 배경:</strong> ${{song.synopsis}}
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
    print("=== Hadestown Build Complete! ===")

if __name__ == "__main__":
    main()
