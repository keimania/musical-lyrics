import json
import os
import re

def build_all_markdown():
    with open('data/song_skeletons.json', 'r', encoding='utf-8') as f:
        skeletons = json.load(f)

    # Merge translations from trans_part1.json to trans_part6.json
    all_trans = {}
    for p in range(1, 7):
        p_path = f'data/trans_part{p}.json'
        if os.path.exists(p_path):
            with open(p_path, 'r', encoding='utf-8') as pf:
                part_dict = json.load(pf)
                all_trans.update(part_dict)
        else:
            print(f"Warning: {p_path} not found.")

    print(f"Loaded translations for {len(all_trans)}/46 songs.")

    # Master complete document lines
    complete_doc = []
    complete_doc.append("# 🎭 뮤지컬 <해밀턴(Hamilton)> 전 46곡 공식 원본 가사 및 한국어 전곡 대역·해설집\n")
    complete_doc.append("**작사/작곡**: 린마누엘 미란다 (Lin-Manuel Miranda)\n")
    complete_doc.append("**기반 원작**: 론 처노(Ron Chernow) 저 《알렉산더 해밀턴(Alexander Hamilton)》\n")
    complete_doc.append("**총 곡 수**: 총 46곡 (1막 23곡 / 2막 23곡, 전곡 완역 대역)\n\n")
    complete_doc.append("---\n\n")

    # Table of Contents for complete doc
    complete_doc.append("## 📜 전곡 목차 (Table of Contents)\n\n")
    complete_doc.append("### 제1막 (Act I)\n")
    for i in range(1, 24):
        s = skeletons[str(i)]
        complete_doc.append(f"{i:02d}. [{s['title']} ({s['title_kr']})](#{i:02d}-{slugify_anchor(s['title'])})\n")
    complete_doc.append("\n### 제2막 (Act II)\n")
    for i in range(24, 47):
        s = skeletons[str(i)]
        complete_doc.append(f"{i:02d}. [{s['title']} ({s['title_kr']})](#{i:02d}-{slugify_anchor(s['title'])})\n")
    complete_doc.append("\n---\n\n")

    for i in range(1, 47):
        sid = str(i)
        s = skeletons[sid]
        t = all_trans.get(sid, {})
        
        synopsis = t.get('synopsis', '곡 개요가 준비 중입니다.')
        notes = t.get('notes', [])
        trans_dict = t.get('translations', {})

        act = s['act']
        file_path = s['file_rel_path']
        
        # Prepare individual markdown
        md_lines = []
        md_lines.append(f"# {i:02d}. {s['title']} ({s['title_kr']})\n\n")
        md_lines.append(f"- **막(Act)**: Act {act}, Track {i:02d}\n")
        chars_str = ", ".join([f"{kr} ({en})" for kr, en in zip(s['characters_kr'], s['characters_en'])])
        md_lines.append(f"- **등장인물/가창자**: {chars_str if chars_str else '앙상블 전체 (Company)'}\n")
        
        prev_link = f"[{skeletons[str(i-1)]['title']}](./{os.path.basename(skeletons[str(i-1)]['file_rel_path'])})" if i > 1 else "시작"
        next_link = f"[{skeletons[str(i+1)]['title']}](./{os.path.basename(skeletons[str(i+1)]['file_rel_path'])})" if i < 46 else "끝"
        md_lines.append(f"- **넘버 이동**: [◀ 이전 곡: {prev_link}] | [목차](../README.md) | [다음 곡: {next_link} ▶]\n\n")
        md_lines.append("---\n\n")

        md_lines.append("## 📖 곡 개요 및 드라마적 배경\n\n")
        md_lines.append(f"{synopsis}\n\n")

        if notes:
            md_lines.append("## 💡 감상 포인트 및 주석 (Notes & Rhymes)\n\n")
            for n in notes:
                md_lines.append(f"- {n}\n")
            md_lines.append("\n")

        md_lines.append("---\n\n")
        md_lines.append("## 🎵 가사 대역 (Bilingual Lyrics)\n\n")

        for stanza in s['stanzas']:
            key = stanza['key']
            speaker_kr = stanza['speaker_kr']
            speaker_en = stanza['speaker_en']
            orig_lines = stanza['lines']
            translated = trans_dict.get(key, [])

            md_lines.append(f"### [{speaker_kr} / {speaker_en}]\n\n")
            md_lines.append("> \n")
            for line_idx, o_line in enumerate(orig_lines):
                t_line = translated[line_idx] if line_idx < len(translated) else ""
                md_lines.append(f"> **{o_line}**  \n")
                if t_line:
                    md_lines.append(f"> {t_line}  \n")
                else:
                    md_lines.append(f"> (번역 준비 중)  \n")
                md_lines.append("> \n")
            md_lines.append("\n")

        # Save individual file
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as out_f:
            out_f.writelines(md_lines)

        # Append to complete doc
        complete_doc.append(f"## <a id=\"{i:02d}-{slugify_anchor(s['title'])}\"></a>{i:02d}. {s['title']} ({s['title_kr']})\n\n")
        complete_doc.append(f"- **막(Act)**: Act {act}, Track {i:02d}\n")
        complete_doc.append(f"- **등장인물**: {chars_str}\n\n")
        complete_doc.append(f"**배경**: {synopsis}\n\n")
        if notes:
            complete_doc.append("**주요 감상 포인트**:\n")
            for n in notes:
                complete_doc.append(f"- {n}\n")
            complete_doc.append("\n")

        for stanza in s['stanzas']:
            key = stanza['key']
            speaker_kr = stanza['speaker_kr']
            speaker_en = stanza['speaker_en']
            orig_lines = stanza['lines']
            translated = trans_dict.get(key, [])

            complete_doc.append(f"**[{speaker_kr} / {speaker_en}]**  \n")
            for line_idx, o_line in enumerate(orig_lines):
                t_line = translated[line_idx] if line_idx < len(translated) else ""
                complete_doc.append(f"> **{o_line}**  \n")
                complete_doc.append(f"> {t_line}  \n>\n")
            complete_doc.append("\n")

        complete_doc.append("\n[맨 위로 이동 ↑](#-전곡-목차-table-of-contents)\n\n---\n\n")

    # Save complete markdown
    with open('hamilton_complete.md', 'w', encoding='utf-8') as cf:
        cf.writelines(complete_doc)

    print("Successfully built all individual markdown files and hamilton_complete.md!")

def slugify_anchor(title):
    title = title.lower()
    title = re.sub(r'[\'\?\(\)\!\,\#]', '', title)
    title = re.sub(r'\s+', '-', title)
    return title.strip('-')

if __name__ == '__main__':
    build_all_markdown()
