# -*- coding: utf-8 -*-
"""
Les Misérables Musical Archive & Web Viewer Builder
Generates:
- les_miserables/data/lesmis_songs.json
- les_miserables/act1/*.md (18 tracks)
- les_miserables/act2/*.md (16 tracks)
- les_miserables/lesmis_complete.md
- les_miserables/README.md
- les_miserables/index.html (Interactive Web Viewer)
"""

import os
import json
import re
import sys

from build_lesmis_data import LESMIS_SONGS

FILE_SLUGS = [
    # Act 1 (1-18)
    "01_prologue_look_down",
    "02_valjeans_soliloquy",
    "03_at_the_end_of_the_day",
    "04_i_dreamed_a_dream",
    "05_lovely_ladies",
    "06_who_am_i",
    "07_come_to_me_fantines_death",
    "08_the_confrontation",
    "09_castle_on_a_cloud",
    "10_master_of_the_house",
    "11_the_bargain_waltz",
    "12_look_down_paris",
    "13_stars",
    "14_red_and_black",
    "15_do_you_hear_the_people_sing",
    "16_in_my_life_a_heart_full_of_love",
    "17_the_attack_on_rue_plumet",
    "18_one_day_more",
    # Act 2 (19-34)
    "19_building_the_barricade_on_my_own",
    "20_at_the_barricade",
    "21_a_little_fall_of_rain",
    "22_night_of_anguish",
    "23_first_attack",
    "24_drink_with_me",
    "25_bring_him_home",
    "26_dawn_of_anguish",
    "27_death_of_gavroche",
    "28_the_final_battle",
    "29_the_sewers_dog_eats_dog",
    "30_javerts_suicide",
    "31_turning_empty_chairs",
    "32_every_day_wedding_chorale",
    "33_valjeans_death",
    "34_finale_do_you_hear_the_people_sing"
]

def slugify_anchor(title):
    cleaned = re.sub(r'[^a-zA-Z0-9\s-]', '', title).lower()
    return re.sub(r'[\s_]+', '-', cleaned).strip('-')

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assert len(LESMIS_SONGS) == 34, f"Expected 34 songs, got {len(LESMIS_SONGS)}"

    for idx, song in enumerate(LESMIS_SONGS):
        slug = FILE_SLUGS[idx]
        act_dir = f"act{song['act']}"
        song["slug"] = slug
        song["filename"] = f"{slug}.md"
        song["rel_path"] = f"{act_dir}/{slug}.md"

    # 1. Verify 1:1 Line Matching
    print("=== [1/6] Verifying 1:1 Line Matching ===")
    total_lines = 0
    mismatches = 0
    for song in LESMIS_SONGS:
        for s_idx, st in enumerate(song["stanzas"]):
            len_en = len(st["lines_en"])
            len_kr = len(st["lines_kr"])
            total_lines += len_en
            if len_en != len_kr:
                print(f"[MISMATCH] Song #{song['id']} ({song['title']}) Stanza #{s_idx+1}: EN({len_en}) != KR({len_kr})")
                mismatches += 1

    if mismatches > 0:
        raise ValueError(f"Found {mismatches} stanza mismatches! Aborting build.")
    print(f"Verification Passed! 34 songs, {total_lines} lines verified 100% aligned 1:1.\n")

    # 2. Save JSON Database
    print("=== [2/6] Writing les_miserables/data/lesmis_songs.json ===")
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    json_path = os.path.join(data_dir, "lesmis_songs.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(LESMIS_SONGS, f, ensure_ascii=False, indent=2)
    print(f"Saved: {json_path}\n")

    # 3. Generate Individual Markdown Track Files
    print("=== [3/6] Generating Individual Markdown Track Files ===")
    os.makedirs(os.path.join(base_dir, "act1"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "act2"), exist_ok=True)

    for idx, song in enumerate(LESMIS_SONGS):
        file_path = os.path.join(base_dir, song["rel_path"])
        act = song["act"]
        act_label = f"제{act}막 (Act {act})"

        prev_song = LESMIS_SONGS[idx - 1] if idx > 0 else None
        next_song = LESMIS_SONGS[idx + 1] if idx < len(LESMIS_SONGS) - 1 else None

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

        md.append("## 📖 곡 개요 및 역사적 배경 (Historical & Dramatic Synopsis)\n\n")
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

    print(f"Generated 34 individual markdown files in les_miserables/act1/ and les_miserables/act2/\n")

    # 4. Generate Master Complete Document
    print("=== [4/6] Generating les_miserables/lesmis_complete.md ===")
    comp = []
    comp.append("# 🇫🇷 뮤지컬 《레미제라블 (Les Misérables)》 전 34곡 공식 원본 가사 및 한국어 전곡 대역·해설집\n\n")
    comp.append("**작곡**: 클로드미셸 쇤베르그 (Claude-Michel Schönberg)\n")
    comp.append("**작사**: 알랭 부블릴 & 장마르크 나텔 (영어 가사: 허버트 크레츠머)\n")
    comp.append("**기반 원작**: 빅토르 위고의 1862년 불멸의 대하소설 《레 미제라블 (Les Misérables)》\n")
    comp.append("**제작**: 카메론 매킨토시 (Cameron Mackintosh)\n")
    comp.append("**초연 주연**: 콜름 윌킨슨 (장발장), 필립 퀘스트 (자베르), 패티 루폰 (팡틴), 레아 살롱가 (에포닌), 마이클 볼 (마리우스)\n")
    comp.append("**수상 이력**: 토니상 8관왕 (최우수 작품상, 음악상, 연출상 등), 전 세계 44개국 1억 3천만 명 관람 불멸의 뮤지컬\n")
    comp.append("**특징**: 대사 없이 전곡이 노래로 이어지는 풀 성스루(Sung-through) 심포닉 오케스트라 명작. 전 34곡 전수 1:1 대역 수록.\n\n")
    comp.append("---\n\n")

    comp.append("## 📜 전곡 목차 (Table of Contents)\n\n")
    comp.append("### 제1막 (Act I: 툴롱에서 파리까지, 은혜와 갈등, 그리고 혁명의 전야)\n\n")
    for s in LESMIS_SONGS[:18]:
        anchor = f"{s['id']:02d}-{slugify_anchor(s['title'])}"
        comp.append(f"{s['id']:02d}. [{s['title']} ({s['title_kr']})](#{anchor})\n")

    comp.append("\n### 제2막 (Act II: 바리케이드의 피와 눈물, 하수도의 구원, 그리고 영원한 승리)\n\n")
    for s in LESMIS_SONGS[18:]:
        anchor = f"{s['id']:02d}-{slugify_anchor(s['title'])}"
        comp.append(f"{s['id']:02d}. [{s['title']} ({s['title_kr']})](#{anchor})\n")

    comp.append("\n---\n\n")

    for s in LESMIS_SONGS:
        anchor = f"{s['id']:02d}-{slugify_anchor(s['title'])}"
        comp.append(f"## <a id=\"{anchor}\"></a>{s['id']:02d}. {s['title']} ({s['title_kr']})\n\n")
        comp.append(f"- **막**: Act {s['act']} · Track {s['id']:02d}\n")
        chars_en = ", ".join(s.get("characters_en", []))
        chars_kr = ", ".join(s.get("characters_kr", []))
        comp.append(f"- **등장인물/보컬**: {chars_kr} ({chars_en})\n\n")
        comp.append(f"**역사적·드라마적 배경**: {s['synopsis']}\n\n")

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

    complete_path = os.path.join(base_dir, "lesmis_complete.md")
    with open(complete_path, "w", encoding="utf-8") as f:
        f.writelines(comp)
    print(f"Generated: {complete_path}\n")

    # 5. Generate README.md
    print("=== [5/6] Generating les_miserables/README.md ===")
    readme = []
    readme.append("# 🇫🇷 뮤지컬 《레미제라블 (Les Misérables)》 공식 전곡 가사 및 영한 대역 아카이브\n\n")
    readme.append("> **\"Do you hear the people sing? Singing a song of angry men!\"**\n")
    readme.append("> **\"To love another person is to see the face of God!\"**\n")
    readme.append("> 전 세계 1억 3천만 명을 울린 인류 역사상 가장 위대한 뮤지컬의 정점!\n")
    readme.append("> 빅토르 위고의 원작 대하소설을 웅장한 풀 성스루 심포닉 오케스트라로 구현한 브로드웨이/웨스트엔드 전 34곡 전수 완역 아카이브.\n\n")
    readme.append("## 🌟 웹 뷰어 바로가기\n\n")
    readme.append("- 📱 **인터랙티브 웹 뷰어 (GitHub Pages)**: [레미제라블 뷰어 바로가기](./index.html)\n")
    readme.append("- 📖 **전곡 단일 통합 완본 (Single Document)**: [`lesmis_complete.md`](./lesmis_complete.md)\n")
    readme.append("- 🏠 **뮤지컬 라이브러리 홈**: [전체 라이브러리 포털](../index.html)\n\n")
    readme.append("---\n\n")

    readme.append("## 🎭 주요 등장인물 및 배역 (Characters)\n\n")
    readme.append("- **장발장 (Jean Valjean)**: 빵 한 조각을 훔쳐 19년간 복역한 죄수에서 미리엘 주교의 자비로 거듭나 평생을 헌신하는 주인공\n")
    readme.append("- **자베르 경감 (Inspector Javert)**: 오직 법과 질서만이 정의라고 맹신하며 평생 장발장을 쫓는 냉혹한 법 집행관\n")
    readme.append("- **팡틴 (Fantine)**: 딸 코제트를 위해 모든 것을 희생하고 비극적으로 숨져간 가련한 어머니\n")
    readme.append("- **코제트 (Cosette)**: 팡틴의 딸이자 장발장이 목숨 바쳐 키워낸 순수와 희망의 상징\n")
    readme.append("- **마리우스 퐁메르시 (Marius Pontmercy)**: 귀족 가문을 박차고 공화국 혁명에 뛰어든 청년, 코제트와의 진실한 사랑\n")
    readme.append("- **에포닌 (Éponine)**: 테나르디에 부부의 딸, 마리우스를 향한 짝사랑을 위해 바리케이드에서 목숨을 바치는 비련의 여주인공\n")
    readme.append("- **앙졸라 (Enjolras)**: 1832년 6월 봉기를 이끄는 순결하고 불꽃같은 혁명 청년단의 지도자\n")
    readme.append("- **가브로슈 (Gavroche)**: 파리 뒷골목의 용감하고 당돌한 꼬마 영웅\n")
    readme.append("- **테나르디에 부부 (The Thénardiers)**: 여관을 운영하며 손님들을 등쳐먹고 시체를 터는 탐욕과 야합의 화신들\n\n")
    readme.append("---\n\n")

    readme.append("## 📜 전곡 트랙리스트 (Tracklist)\n\n")
    readme.append("### 🔵 제1막 (Act I)\n\n")
    for s in LESMIS_SONGS[:18]:
        chars = ", ".join(s.get("characters_kr", []))
        readme.append(f"- **{s['id']:02d}. [{s['title']} ({s['title_kr']})](./act1/{s['filename']})** — *{chars}*\n")

    readme.append("\n### 🔴 제2막 (Act II)\n\n")
    for s in LESMIS_SONGS[18:]:
        chars = ", ".join(s.get("characters_kr", []))
        readme.append(f"- **{s['id']:02d}. [{s['title']} ({s['title_kr']})](./act2/{s['filename']})** — *{chars}*\n")

    readme_path = os.path.join(base_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.writelines(readme)
    print(f"Generated: {readme_path}\n")

    # 6. Generate Standalone Interactive Web Viewer (les_miserables/index.html)
    print("=== [6/6] Generating les_miserables/index.html ===")
    json_data_for_web = json.dumps(LESMIS_SONGS, ensure_ascii=False)

    html_content = f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>뮤지컬 《레미제라블 (Les Misérables)》 전곡 영한 대역 뷰어</title>
  <style>
    :root {{
      --bg: #090b12;
      --sidebar-bg: #0f121d;
      --card-bg: #151a29;
      --france-blue: #3867d6;
      --france-blue-glow: rgba(56, 103, 214, 0.4);
      --france-red: #eb3b5a;
      --rebel-gold: #fed330;
      --text: #edf2f7;
      --text-muted: #8b98aa;
      --border: #232a3d;
      --hover: #1c2234;
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
      background: #0b0e17;
      text-align: center;
      position: relative;
    }}
    .sidebar-header .home-link {{
      display: inline-block;
      margin-bottom: 8px;
      font-size: 0.75rem;
      color: var(--france-blue);
      text-decoration: none;
      padding: 3px 8px;
      background: rgba(56, 103, 214, 0.1);
      border-radius: 4px;
      border: 1px solid rgba(56, 103, 214, 0.25);
      transition: all 0.2s;
    }}
    .sidebar-header .home-link:hover {{
      background: var(--france-blue);
      color: #fff;
    }}
    .sidebar-header h1 {{
      font-size: 1.25rem;
      background: linear-gradient(135deg, #3867d6 0%, #eb3b5a 100%);
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
      background: #141926;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: #fff;
      font-size: 0.85rem;
      outline: none;
      transition: border-color 0.2s;
    }}
    .search-box input:focus {{
      border-color: var(--france-blue);
      box-shadow: 0 0 8px var(--france-blue-glow);
    }}
    .act-tabs {{
      display: flex;
      padding: 6px 10px;
      gap: 6px;
      background: #0b0e17;
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
      background: rgba(56, 103, 214, 0.15);
      color: var(--france-blue);
      border-color: rgba(56, 103, 214, 0.4);
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
      background: #131724;
    }}
    .song-item:hover {{
      background: var(--hover);
      border-color: rgba(56, 103, 214, 0.3);
    }}
    .song-item.active {{
      background: rgba(56, 103, 214, 0.15);
      border-color: var(--france-blue);
      box-shadow: 0 0 10px rgba(56, 103, 214, 0.2);
    }}
    .song-badge-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 3px;
    }}
    .song-num {{
      font-size: 0.72rem;
      color: var(--rebel-gold);
      font-weight: 700;
    }}
    .song-act-tag {{
      font-size: 0.65rem;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 600;
      background: rgba(56, 103, 214, 0.12);
      color: var(--france-blue);
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
      background: #0f121d;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .mobile-menu-btn {{
      display: none;
      background: transparent;
      border: 1px solid var(--border);
      color: var(--france-blue);
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
      background: #151a29;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: var(--text-muted);
      font-size: 0.8rem;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .view-btn.active {{
      background: var(--france-blue);
      color: #fff;
      font-weight: 700;
      border-color: var(--france-blue);
      box-shadow: 0 0 10px var(--france-blue-glow);
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
      color: var(--france-blue);
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
      border-left: 4px solid var(--france-blue);
      padding: 16px 20px;
      border-radius: 0 8px 8px 0;
      margin-bottom: 20px;
      font-size: 0.95rem;
      line-height: 1.7;
      color: #e5ecf6;
    }}
    .notes-box {{
      background: #121624;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px 20px;
      margin-bottom: 30px;
    }}
    .notes-box h4 {{
      font-size: 0.9rem;
      color: var(--rebel-gold);
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .notes-box ul {{
      padding-left: 18px;
      font-size: 0.88rem;
      color: #bac7d5;
      line-height: 1.65;
    }}
    .notes-box li {{
      margin-bottom: 6px;
    }}
    .stanza-block {{
      background: #111522;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px 24px;
      margin-bottom: 24px;
    }}
    .speaker-tag {{
      display: inline-block;
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--france-blue);
      background: rgba(56, 103, 214, 0.1);
      padding: 4px 10px;
      border-radius: 4px;
      margin-bottom: 16px;
      border: 1px solid rgba(56, 103, 214, 0.25);
    }}
    .lyric-pair {{
      margin-bottom: 14px;
      padding-bottom: 10px;
      border-bottom: 1px dashed rgba(35, 42, 61, 0.7);
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
      color: #afbdd0;
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
      <h1>LES MISÉRABLES</h1>
      <p>전 34곡 공식 가사 & 영한 대역 뷰어</p>
    </div>
    <div class="search-box">
      <input type="text" id="searchInput" placeholder="곡 제목, 가사, 등장인물 검색..." oninput="renderSongList()">
    </div>
    <div class="act-tabs">
      <button class="act-tab active" id="tabAll" onclick="setActFilter('all')">전체 (34)</button>
      <button class="act-tab" id="tabAct1" onclick="setActFilter(1)">1막 (18)</button>
      <button class="act-tab" id="tabAct2" onclick="setActFilter(2)">2막 (16)</button>
    </div>
    <div class="song-list" id="songListContainer"></div>
  </div>

  <!-- Main Content -->
  <div id="main">
    <div class="top-bar">
      <div style="display: flex; align-items: center; gap: 12px;">
        <button class="mobile-menu-btn" onclick="openSidebar()">☰ 목록</button>
        <div style="font-size: 0.85rem; color: var(--rebel-gold); font-weight: 700;" id="topBarTrackInfo">Act 1 · Track 01 / 34</div>
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

      document.getElementById('topBarTrackInfo').textContent = `Act ${{song.act}} · Track ${{String(song.id).padStart(2, '0')}} / 34`;

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
          <strong>📖 역사적·드라마적 배경:</strong> ${{song.synopsis}}
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
    print("=== Les Misérables Build Complete! ===")

if __name__ == "__main__":
    main()
