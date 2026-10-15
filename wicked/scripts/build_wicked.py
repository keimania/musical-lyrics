# -*- coding: utf-8 -*-
"""
Wicked 2-Part Movie Adaptation Builder
Builds:
- wicked/data/wicked_songs.json
- wicked/part1/*.md (11 songs)
- wicked/part2/*.md (11 songs)
- wicked/wicked_complete.md
- wicked/README.md
- wicked/index.html (Interactive Web Viewer with Emerald/Pink Dual Theme & Mobile Drawer)
"""

import os
import json
import re
import sys

# Import song definitions
from build_part1_data import PART1_SONGS
from build_part2_data import PART2_SONGS

FILE_SLUGS = [
    # Part 1 (1-11)
    "01_no_one_mourns_the_wicked",
    "02_dear_old_shiz",
    "03_the_wizard_and_i",
    "04_what_is_this_feeling",
    "05_something_bad",
    "06_dancing_through_life",
    "07_popular",
    "08_im_not_that_girl",
    "09_one_short_day",
    "10_a_sentimental_man",
    "11_defying_gravity",
    # Part 2 (12-22)
    "12_every_day_more_wicked",
    "13_thank_goodness",
    "14_no_place_like_home",
    "15_the_wicked_witch_of_the_east",
    "16_wonderful",
    "17_im_not_that_girl_reprise",
    "18_as_long_as_youre_mine",
    "19_no_good_deed",
    "20_march_of_the_witch_hunters",
    "21_the_girl_in_the_bubble",
    "22_for_good"
]

def slugify_anchor(title):
    cleaned = re.sub(r'[^a-zA-Z0-9\s-]', '', title).lower()
    return re.sub(r'[\s_]+', '-', cleaned).strip('-')

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    all_songs = PART1_SONGS + PART2_SONGS
    assert len(all_songs) == 22, f"Expected 22 songs, got {len(all_songs)}"

    # Attach file paths & metadata
    for idx, song in enumerate(all_songs):
        slug = FILE_SLUGS[idx]
        part_dir = "part1" if song["part"] == 1 else "part2"
        song["slug"] = slug
        song["filename"] = f"{slug}.md"
        song["rel_path"] = f"{part_dir}/{slug}.md"

    # 1. Strict Line Count Verification
    print("=== [1/6] Running 1:1 Line Matching Verification ===")
    mismatches = 0
    total_lines = 0
    for song in all_songs:
        for s_idx, st in enumerate(song["stanzas"]):
            l_en = len(st["lines_en"])
            l_kr = len(st["lines_kr"])
            total_lines += l_en
            if l_en != l_kr:
                print(f"Error in Song #{song['id']} ({song['title']}) Stanza #{s_idx+1}: EN({l_en}) != KR({l_kr})")
                mismatches += 1
    if mismatches > 0:
        raise ValueError(f"Found {mismatches} stanza mismatches! Aborting build.")
    print(f"Verification Passed! 22 songs, {total_lines} lines verified 100% aligned 1:1.\n")

    # 2. Save JSON Database
    print("=== [2/6] Writing wicked/data/wicked_songs.json ===")
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    json_path = os.path.join(data_dir, "wicked_songs.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_songs, f, ensure_ascii=False, indent=2)
    print(f"Saved: {json_path}\n")

    # 3. Generate Individual Markdown Track Files
    print("=== [3/6] Generating Individual Markdown Track Files ===")
    os.makedirs(os.path.join(base_dir, "part1"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "part2"), exist_ok=True)

    for idx, song in enumerate(all_songs):
        part = song["part"]
        part_name = "위키드: 파트 1 (Wicked, 2024)" if part == 1 else "위키드: 포 굿 (Wicked: For Good, 2025)"
        file_path = os.path.join(base_dir, song["rel_path"])

        prev_song = all_songs[idx - 1] if idx > 0 else None
        next_song = all_songs[idx + 1] if idx < len(all_songs) - 1 else None

        if prev_song:
            prev_dir = "part1" if prev_song["part"] == 1 else "part2"
            curr_dir = "part1" if part == 1 else "part2"
            rel_prefix = "./" if prev_dir == curr_dir else f"../{prev_dir}/"
            prev_link = f"[{prev_song['id']:02d}. {prev_song['title']}]({rel_prefix}{prev_song['filename']})"
        else:
            prev_link = "시작"

        if next_song:
            next_dir = "part1" if next_song["part"] == 1 else "part2"
            curr_dir = "part1" if part == 1 else "part2"
            rel_prefix = "./" if next_dir == curr_dir else f"../{next_dir}/"
            next_link = f"[{next_song['id']:02d}. {next_song['title']}]({rel_prefix}{next_song['filename']})"
        else:
            next_link = "끝"

        md = []
        md.append(f"# {song['id']:02d}. {song['title']} ({song['title_kr']})\n\n")
        md.append(f"- **영화 파트**: {part_name} · Track {song['id']:02d}\n")
        chars_en = ", ".join(song.get("characters_en", []))
        chars_kr = ", ".join(song.get("characters_kr", []))
        md.append(f"- **등장인물/보컬**: {chars_kr} ({chars_en})\n")
        md.append(f"- **넘버 이동**: [◀ 이전 곡: {prev_link}] | [전체 목차](../README.md) | [다음 곡: {next_link} ▶]\n\n")
        md.append("---\n\n")

        md.append("## 📖 곡 개요 및 영화적 연출 (Cinematic Synopsis)\n\n")
        md.append(f"{song['synopsis']}\n\n")

        if song.get("notes"):
            md.append("## 💡 감상 포인트 및 영화판 특징 (Key Notes & Film Highlights)\n\n")
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
            for line_en, line_kr in zip(stanza["lines_en"], stanza["lines_kr"]):
                md.append(f"> **{line_en}**  \n")
                md.append(f"> {line_kr}  \n")
                md.append("> \n")
            md.append("\n")

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(md)

    print(f"Generated 22 individual markdown files in wicked/part1/ and wicked/part2/\n")

    # 4. Generate Master Complete Document (wicked_complete.md)
    print("=== [4/6] Generating wicked/wicked_complete.md ===")
    comp = []
    comp.append("# 🧙‍♀️🧹 영화 《위키드 (Wicked 2부작)》 전 22곡 공식 원본 가사 및 한국어 전곡 대역·해설집\n\n")
    comp.append("**기반 원작**: 그레고리 맥과이어의 소설 《위키드: 사악한 서쪽 마녀의 삶과 시대》 & 브로드웨이 뮤지컬 《위키드》\n")
    comp.append("**영화 감독**: 존 M. 추 (Jon M. Chu)\n")
    comp.append("**음악/작사**: 스티븐 슈워츠 (Stephen Schwartz)\n")
    comp.append("**주연 배우**: 신시아 에리보 (엘파바), 아리아나 그란데 (글린다), 조나단 베일리 (피에로), 양자경 (마담 모리블), 제프 골드블룸 (마법사), 피터 딘클리지 (딜라몬드 교수), 이선 슬레이터 (보크), 마리사 보디 (네사로즈)\n")
    comp.append("**영화 구성**:\n")
    comp.append("  - **1부 (Part 1, 2024)**: 《위키드 (Wicked)》 - 11곡\n")
    comp.append("  - **2부 (Part 2, 2025)**: 《위키드: 포 굿 (Wicked: For Good)》 - 11곡 (★ 스티븐 슈워츠 작사/작곡 영화 오리지널 신곡 2곡 및 복원 넘버 포함)\n")
    comp.append("**총 수록 수**: 총 22개 영화 사운드트랙 전곡 (보컬 및 대사 전수 1:1 대역)\n\n")
    comp.append("---\n\n")

    comp.append("## 📜 전곡 목차 (Table of Contents)\n\n")
    comp.append("### 🌸 제1부: 위키드 (Wicked: Part One, 2024)\n\n")
    for s in all_songs[:11]:
        anchor = f"{s['id']:02d}-{slugify_anchor(s['title'])}"
        comp.append(f"{s['id']:02d}. [{s['title']} ({s['title_kr']})](#{anchor})\n")

    comp.append("\n### 💚 제2부: 위키드: 포 굿 (Wicked: For Good - Part Two, 2025)\n\n")
    for s in all_songs[11:]:
        anchor = f"{s['id']:02d}-{slugify_anchor(s['title'])}"
        comp.append(f"{s['id']:02d}. [{s['title']} ({s['title_kr']})](#{anchor})\n")

    comp.append("\n---\n\n")

    for s in all_songs:
        anchor = f"{s['id']:02d}-{slugify_anchor(s['title'])}"
        part_name = "제1부: 위키드 (2024)" if s["part"] == 1 else "제2부: 위키드: 포 굿 (2025)"
        comp.append(f"## <a id=\"{anchor}\"></a>{s['id']:02d}. {s['title']} ({s['title_kr']})\n\n")
        comp.append(f"- **파트**: {part_name} · Track {s['id']:02d}\n")
        chars_en = ", ".join(s.get("characters_en", []))
        chars_kr = ", ".join(s.get("characters_kr", []))
        comp.append(f"- **등장인물/보컬**: {chars_kr} ({chars_en})\n\n")
        comp.append(f"**영화적 배경 및 연출**: {s['synopsis']}\n\n")

        if s.get("notes"):
            comp.append("**감상 포인트 & 영화판 특징**:\n")
            for n in s["notes"]:
                comp.append(f"- {n}\n")
            comp.append("\n")

        comp.append("### 가사 대역\n\n")
        for stanza in s["stanzas"]:
            spk_kr = stanza.get("speaker_kr", "등장인물")
            spk_en = stanza.get("speaker_en", "Character")
            comp.append(f"**[{spk_kr} / {spk_en}]**\n\n")
            for line_en, line_kr in zip(stanza["lines_en"], stanza["lines_kr"]):
                comp.append(f"> **{line_en}**  \n")
                comp.append(f"> {line_kr}  \n")
                comp.append("> \n")
            comp.append("\n")

        comp.append("---\n\n")

    complete_path = os.path.join(base_dir, "wicked_complete.md")
    with open(complete_path, "w", encoding="utf-8") as f:
        f.writelines(comp)
    print(f"Generated: {complete_path}\n")

    # 5. Generate wicked/README.md
    print("=== [5/6] Generating wicked/README.md ===")
    readme = []
    readme.append("# 🧙‍♀️🧹 영화 《위키드 (Wicked 2부작)》 공식 전곡 가사 및 한국어 대역 아카이브\n\n")
    readme.append("> **존 M. 추(Jon M. Chu)** 감독 연출, **신시아 에리보(Cynthia Erivo)** & **아리아나 그란데(Ariana Grande)** 주연!\n")
    readme.append("> 유니버설 픽처스의 시네마틱 2부작 대작 영화 《위키드》(2024) 및 《위키드: 포 굿》(2025)에 수록된 전 22곡의 오리지널 사운드트랙 가사와 1:1 대역, 영화적 해설 아카이브입니다.\n\n")
    readme.append("## 🌟 웹 뷰어 바로가기\n\n")
    readme.append("- 📱 **인터랙티브 웹 뷰어 (GitHub Pages)**: [위키드 뷰어 바로가기](./index.html)\n")
    readme.append("- 📖 **전곡 통합 대역본 (Single Document)**: [`wicked_complete.md`](./wicked_complete.md)\n")
    readme.append("- 🏠 **뮤지컬 라이브러리 홈**: [전체 라이브러리 포털](../index.html)\n\n")
    readme.append("---\n\n")

    readme.append("## 🎬 영화 개요 (Film Overview)\n\n")
    readme.append("| 구분 | 1부: 《위키드 (Wicked)》 | 2부: 《위키드: 포 굿 (Wicked: For Good)》 |\n")
    readme.append("| :--- | :--- | :--- |\n")
    readme.append("| **개봉 연도** | 2024년 11월 | 2025년 11월 |\n")
    readme.append("| **원작 대응** | 브로드웨이 뮤지컬 제1막 (쉬즈 대학교 입학 ~ 중력을 벗어나) | 브로드웨이 뮤지컬 제2막 (도로시의 도착 ~ 에메랄드 시티의 진실) |\n")
    readme.append("| **수록 곡수** | 11곡 | 11곡 (★ 스티븐 슈워츠 작사/작곡 영화 오리지널 신곡 2곡 포함) |\n")
    readme.append("| **핵심 주제** | 다름에 대한 편견, 엘파바와 글린다의 깊은 우정의 태동 | 프로파간다와 권력의 실체, 선과 악의 진정한 의미, 영원한 작별과 구원 |\n\n")

    readme.append("## 🎭 주요 출연진 및 배역 (Cast)\n\n")
    readme.append("- **엘파바 트롭 (Elphaba Thropp)**: 신시아 에리보 (Cynthia Erivo) — 토니상, 그래미상, 에미상 수상의 독보적 가창력\n")
    readme.append("- **글린다 업랜드 (Glinda Upland)**: 아리아나 그란데 (Ariana Grande) — 4옥타브 음역의 팝 슈퍼스타 & 천상의 소프라노\n")
    readme.append("- **피에로 티겔라 (Fiyero Tigelaar)**: 조나단 베일리 (Jonathan Bailey) — 매혹적인 윙키 왕국의 왕자\n")
    readme.append("- **마담 모리블 (Madame Morrible)**: 양자경 (Michelle Yeoh) — 쉬즈 대학 학장이자 오즈의 실력자\n")
    readme.append("- **오즈의 마법사 (The Wonderful Wizard of Oz)**: 제프 골드블룸 (Jeff Goldblum) — 카리스마와 쓸쓸함을 지닌 통치자\n")
    readme.append("- **딜라몬드 교수 (Doctor Dillamond)**: 피터 딘클리지 (Peter Dinklage) — 말하는 동물 교수\n")
    readme.append("- **보크 (Boq)**: 이선 슬레이터 (Ethan Slater) — 글린다를 짝사랑하는 먼치킨\n")
    readme.append("- **네사로즈 트롭 (Nessarose Thropp)**: 마리사 보디 (Marissa Bode) — 휠체어를 타는 엘파바의 여동생\n\n")
    readme.append("---\n\n")

    readme.append("## 📜 전곡 트랙리스트 (Tracklist)\n\n")
    readme.append("### 🌸 제1부: 《위키드》(2024) - Part One\n\n")
    for s in all_songs[:11]:
        chars = ", ".join(s.get("characters_kr", []))
        readme.append(f"- **{s['id']:02d}. [{s['title']} ({s['title_kr']})](./part1/{s['filename']})** — *{chars}*\n")

    readme.append("\n### 💚 제2부: 《위키드: 포 굿》(2025) - Part Two\n\n")
    for s in all_songs[11:]:
        chars = ", ".join(s.get("characters_kr", []))
        extra = ""
        if s["id"] in [14, 21]:
            extra = " ★ [영화 오리지널 신곡]"
        elif s["id"] == 15:
            extra = " ★ [무대 복원 넘버]"
        readme.append(f"- **{s['id']:02d}. [{s['title']} ({s['title_kr']})](./part2/{s['filename']})**{extra} — *{chars}*\n")

    readme_path = os.path.join(base_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.writelines(readme)
    print(f"Generated: {readme_path}\n")

    # 6. Generate Standalone Interactive Web Viewer (wicked/index.html)
    print("=== [6/6] Generating wicked/index.html ===")
    json_data_for_web = json.dumps(all_songs, ensure_ascii=False)

    html_content = f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>영화 《위키드 (Wicked 2부작)》 전곡 원본 가사 & 영한 대역 뷰어</title>
  <style>
    :root {{
      --bg: #080d0b;
      --sidebar-bg: #0b1410;
      --card-bg: #111f18;
      --emerald: #00ff87;
      --emerald-glow: rgba(0, 255, 135, 0.35);
      --glinda-pink: #ff69b4;
      --glinda-pink-glow: rgba(255, 105, 180, 0.35);
      --gold: #ffdd55;
      --text: #eaf3ee;
      --text-muted: #8ca397;
      --border: #1a2d24;
      --hover: #15271e;
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
      background: #070e0b;
      text-align: center;
      position: relative;
    }}
    .sidebar-header .home-link {{
      display: inline-block;
      margin-bottom: 8px;
      font-size: 0.75rem;
      color: var(--emerald);
      text-decoration: none;
      padding: 3px 8px;
      background: rgba(0, 255, 135, 0.1);
      border-radius: 4px;
      border: 1px solid rgba(0, 255, 135, 0.25);
      transition: all 0.2s;
    }}
    .sidebar-header .home-link:hover {{
      background: var(--emerald);
      color: #000;
    }}
    .sidebar-header h1 {{
      font-size: 1.25rem;
      background: linear-gradient(135deg, var(--emerald) 0%, var(--glinda-pink) 100%);
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
      background: #101c16;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: #fff;
      font-size: 0.85rem;
      outline: none;
      transition: border-color 0.2s;
    }}
    .search-box input:focus {{
      border-color: var(--emerald);
      box-shadow: 0 0 8px var(--emerald-glow);
    }}
    .act-tabs {{
      display: flex;
      padding: 6px 10px;
      gap: 6px;
      background: #070e0b;
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
      background: rgba(0, 255, 135, 0.12);
      color: var(--emerald);
      border-color: rgba(0, 255, 135, 0.35);
      font-weight: 700;
    }}
    .act-tab.pink.active {{
      background: rgba(255, 105, 180, 0.12);
      color: var(--glinda-pink);
      border-color: rgba(255, 105, 180, 0.35);
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
      background: #0e1a14;
    }}
    .song-item:hover {{
      background: var(--hover);
      border-color: rgba(0, 255, 135, 0.3);
    }}
    .song-item.active {{
      background: rgba(0, 255, 135, 0.12);
      border-color: var(--emerald);
      box-shadow: 0 0 10px rgba(0, 255, 135, 0.15);
    }}
    .song-item.part2.active {{
      background: rgba(255, 105, 180, 0.12);
      border-color: var(--glinda-pink);
      box-shadow: 0 0 10px rgba(255, 105, 180, 0.15);
    }}
    .song-badge-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 3px;
    }}
    .song-num {{
      font-size: 0.72rem;
      color: var(--gold);
      font-weight: 700;
    }}
    .song-part-tag {{
      font-size: 0.65rem;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: 600;
    }}
    .song-part-tag.p1 {{
      background: rgba(0, 255, 135, 0.15);
      color: var(--emerald);
    }}
    .song-part-tag.p2 {{
      background: rgba(255, 105, 180, 0.15);
      color: var(--glinda-pink);
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
      background: #0b1410;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .mobile-menu-btn {{
      display: none;
      background: transparent;
      border: 1px solid var(--border);
      color: var(--emerald);
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
      background: #111e17;
      border: 1px solid var(--border);
      border-radius: 6px;
      color: var(--text-muted);
      font-size: 0.8rem;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .view-btn.active {{
      background: var(--emerald);
      color: #000;
      font-weight: 700;
      border-color: var(--emerald);
      box-shadow: 0 0 10px var(--emerald-glow);
    }}
    .view-btn.pink.active {{
      background: var(--glinda-pink);
      color: #fff;
      border-color: var(--glinda-pink);
      box-shadow: 0 0 10px var(--glinda-pink-glow);
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
      color: var(--emerald);
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
      border-left: 4px solid var(--emerald);
      padding: 16px 20px;
      border-radius: 0 8px 8px 0;
      margin-bottom: 20px;
      font-size: 0.95rem;
      line-height: 1.7;
      color: #d8e5de;
    }}
    .synopsis-box.part2 {{
      border-left-color: var(--glinda-pink);
    }}
    .notes-box {{
      background: #0f1c16;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px 20px;
      margin-bottom: 30px;
    }}
    .notes-box h4 {{
      font-size: 0.9rem;
      color: var(--gold);
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .notes-box ul {{
      padding-left: 18px;
      font-size: 0.88rem;
      color: #b2c4ba;
      line-height: 1.65;
    }}
    .notes-box li {{
      margin-bottom: 6px;
    }}
    .stanza-block {{
      background: #0d1712;
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px 24px;
      margin-bottom: 24px;
    }}
    .speaker-tag {{
      display: inline-block;
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--emerald);
      background: rgba(0, 255, 135, 0.1);
      padding: 4px 10px;
      border-radius: 4px;
      margin-bottom: 16px;
      border: 1px solid rgba(0, 255, 135, 0.25);
    }}
    .stanza-block.pink .speaker-tag {{
      color: var(--glinda-pink);
      background: rgba(255, 105, 180, 0.1);
      border-color: rgba(255, 105, 180, 0.25);
    }}
    .lyric-pair {{
      margin-bottom: 14px;
      padding-bottom: 10px;
      border-bottom: 1px dashed rgba(26, 45, 36, 0.7);
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
      color: #a4beaf;
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
      <h1>WICKED (위키드)</h1>
      <p>영화 2부작 전 22곡 영한 대역 뷰어</p>
    </div>
    <div class="search-box">
      <input type="text" id="searchInput" placeholder="곡 제목, 가사, 등장인물 검색..." oninput="renderSongList()">
    </div>
    <div class="act-tabs">
      <button class="act-tab active" id="tabAll" onclick="setActFilter('all')">전체 (22)</button>
      <button class="act-tab" id="tabPart1" onclick="setActFilter(1)">1부 (11)</button>
      <button class="act-tab pink" id="tabPart2" onclick="setActFilter(2)">2부 (11)</button>
    </div>
    <div class="song-list" id="songListContainer"></div>
  </div>

  <!-- Main Content -->
  <div id="main">
    <div class="top-bar">
      <div style="display: flex; align-items: center; gap: 12px;">
        <button class="mobile-menu-btn" onclick="openSidebar()">☰ 목록</button>
        <div style="font-size: 0.85rem; color: var(--gold); font-weight: 700;" id="topBarTrackInfo">Part 1 · Track 01 / 22</div>
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
      document.getElementById('tabPart1').classList.toggle('active', act === 1);
      document.getElementById('tabPart2').classList.toggle('active', act === 2);
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
        if (currentAct !== 'all' && s.part !== currentAct) return;
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
        const isPart2 = s.part === 2;
        item.className = 'song-item' + (isPart2 ? ' part2' : '') + (s.id === currentSongId ? ' active' : '');
        item.onclick = () => {{
          loadSong(s.id);
          closeSidebar();
        }};

        const partTag = isPart2 ? '<span class="song-part-tag p2">2부: 포 굿</span>' : '<span class="song-part-tag p1">1부: 위키드</span>';
        item.innerHTML = `
          <div class="song-badge-row">
            <span class="song-num">Track ${{String(s.id).padStart(2, '0')}}</span>
            ${{partTag}}
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

      const isPart2 = song.part === 2;
      const partLabel = isPart2 ? '제2부: 위키드 포 굿 (2025)' : '제1부: 위키드 (2024)';
      document.getElementById('topBarTrackInfo').textContent = `${{partLabel}} · Track ${{String(song.id).padStart(2, '0')}} / 22`;

      let notesHtml = '';
      if (song.notes && song.notes.length > 0) {{
        notesHtml = `
          <div class="notes-box">
            <h4>💡 감상 포인트 및 영화판 특징 (Key Notes & Film Highlights)</h4>
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
          <div class="stanza-block${{isPart2 ? ' pink' : ''}}">
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
            <div class="song-meta-item"><strong>영화 파트:</strong> ${{partLabel}}</div>
            <div class="song-meta-item"><strong>등장인물/보컬:</strong> ${{charsKr}} (${{charsEn}})</div>
          </div>
        </div>
        <div class="synopsis-box${{isPart2 ? ' part2' : ''}}">
          <strong>📖 영화적 배경 및 연출:</strong> ${{song.synopsis}}
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
    print("=== All Wicked Artifacts Successfully Built! ===")

if __name__ == "__main__":
    main()
