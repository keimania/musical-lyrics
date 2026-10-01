import json
import os
import re

def build_six_markdown():
    with open('six/data/six_skeletons.json', 'r', encoding='utf-8') as f:
        skeletons = json.load(f)

    all_trans = {}
    for p in [1, 2]:
        p_path = f'six/data/trans_part{p}.json'
        if os.path.exists(p_path):
            with open(p_path, 'r', encoding='utf-8') as pf:
                all_trans.update(json.load(pf))

    print(f"Loaded translations for {len(all_trans)}/11 songs.")

    # Master complete document
    complete_doc = []
    complete_doc.append("# 👑 뮤지컬 <식스(SIX)> 전 11곡 공식 원본 가사 및 한국어 전곡 대역·해설집\n\n")
    complete_doc.append("**작사/작곡**: 토비 말로 & 루시 모스 (Toby Marlow & Lucy Moss)\n")
    complete_doc.append("**작품 주제**: 헨리 8세의 여섯 왕비가 팝 디바로 환생하여 펼치는 역사 전복 팝 콘서트\n")
    complete_doc.append("**수록 곡 수**: 총 11곡 (오프닝, 6인의 솔로, 테크노 앙상블, 피날레 및 메가식스 전곡 완역)\n\n")
    complete_doc.append("---\n\n")

    complete_doc.append("## 📜 전곡 목차 (Table of Contents)\n\n")
    for i in range(1, 12):
        s = skeletons[str(i)]
        complete_doc.append(f"{i:02d}. [{s['title']} ({s['title_kr']})](#{i:02d}-{slugify_anchor(s['title'])})\n")
    complete_doc.append("\n---\n\n")

    for i in range(1, 12):
        sid = str(i)
        s = skeletons[sid]
        t = all_trans.get(sid, {})
        
        synopsis = t.get('synopsis', '곡 개요가 준비 중입니다.')
        notes = t.get('notes', [])
        trans_dict = t.get('translations', {})

        file_path = os.path.join('six', s['file_rel_path'])
        
        md_lines = []
        md_lines.append(f"# {i:02d}. {s['title']} ({s['title_kr']})\n\n")
        md_lines.append(f"- **트랙(Track)**: SIX Track {i:02d}\n")
        
        prev_link = f"[{skeletons[str(i-1)]['title']}](./{os.path.basename(skeletons[str(i-1)]['file_rel_path'])})" if i > 1 else "시작"
        next_link = f"[{skeletons[str(i+1)]['title']}](./{os.path.basename(skeletons[str(i+1)]['file_rel_path'])})" if i < 11 else "끝"
        md_lines.append(f"- **넘버 이동**: [◀ 이전 곡: {prev_link}] | [목차](../README.md) | [다음 곡: {next_link} ▶]\n\n")
        md_lines.append("---\n\n")

        md_lines.append("## 📖 곡 개요 및 역사적/드라마적 배경\n\n")
        md_lines.append(f"{synopsis}\n\n")

        if notes:
            md_lines.append("## 💡 감상 포인트 및 주석 (Key Notes & Pop Motifs)\n\n")
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

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as out_f:
            out_f.writelines(md_lines)

        # Append to complete doc
        complete_doc.append(f"## <a id=\"{i:02d}-{slugify_anchor(s['title'])}\"></a>{i:02d}. {s['title']} ({s['title_kr']})\n\n")
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

    with open('six/six_complete.md', 'w', encoding='utf-8') as cf:
        cf.writelines(complete_doc)

    print("Successfully built all SIX individual markdown files and six_complete.md!")

def slugify_anchor(title):
    title = title.lower()
    title = re.sub(r'[\'\?\(\)\!\,\#]', '', title)
    title = re.sub(r'\s+', '-', title)
    return title.strip('-')

if __name__ == '__main__':
    build_six_markdown()
