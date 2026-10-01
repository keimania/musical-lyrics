import json
import os
import re

def build_bttf_markdown():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skeletons_path = os.path.join(base_dir, 'data', 'bttf_skeletons.json')
    with open(skeletons_path, 'r', encoding='utf-8') as f:
        skeletons = json.load(f)

    all_trans = {}
    for p in [1, 2]:
        p_path = os.path.join(base_dir, 'data', f'trans_part{p}.json')
        if os.path.exists(p_path):
            with open(p_path, 'r', encoding='utf-8') as pf:
                all_trans.update(json.load(pf))

    print(f"Loaded translations for {len(all_trans)}/26 tracks.")

    # Master complete document
    complete_doc = []
    complete_doc.append("# ⚡ 뮤지컬 <백 투 더 퓨처(Back to the Future: The Musical)> 전 26곡 공식 원본 가사 및 한국어 전곡 대역·해설집\n\n")
    complete_doc.append("**작사/작곡**: 앨런 실베스트리 & 글렌 발라드 (Alan Silvestri & Glen Ballard)\n")
    complete_doc.append("**추가 명곡**: 휴이 루이스 앤 더 뉴스, 척 베리, 펭귄스\n")
    complete_doc.append("**대본**: 밥 게일 (Bob Gale, 영화 원작 각본가)\n")
    complete_doc.append("**기반 원작**: 로버트 저메키스 & 밥 게일의 1985년 영화 《백 투 더 퓨처》\n")
    complete_doc.append("**총 수록 수**: 총 26개 트랙 (1막 13곡 / 2막 13곡, 보컬 넘버 및 스코어 전수 수록)\n\n")
    complete_doc.append("---\n\n")

    complete_doc.append("## 📜 전곡 목차 (Table of Contents)\n\n")
    complete_doc.append("### 제1막 (Act I: 1985년에서 1955년으로)\n")
    for i in range(1, 14):
        s = skeletons[str(i)]
        complete_doc.append(f"{i:02d}. [{s['title']} ({s['title_kr']})](#{i:02d}-{slugify_anchor(s['title'])})\n")
    complete_doc.append("\n### 제2막 (Act II: 과거를 바로잡고 미래로 돌아가라!)\n")
    for i in range(14, 27):
        s = skeletons[str(i)]
        complete_doc.append(f"{i:02d}. [{s['title']} ({s['title_kr']})](#{i:02d}-{slugify_anchor(s['title'])})\n")
    complete_doc.append("\n---\n\n")

    for i in range(1, 27):
        sid = str(i)
        s = skeletons[sid]
        t = all_trans.get(sid, {})
        
        synopsis = t.get('synopsis', '곡 개요가 준비 중입니다.')
        notes = t.get('notes', [])
        trans_dict = t.get('translations', {})

        file_path = os.path.join(base_dir, s['file_rel_path'])
        act = s['act']
        
        md_lines = []
        md_lines.append(f"# {i:02d}. {s['title']} ({s['title_kr']})\n\n")
        md_lines.append(f"- **막(Act)**: Act {act}, Track {i:02d}\n")
        
        prev_link = f"[{skeletons[str(i-1)]['title']}](./{os.path.basename(skeletons[str(i-1)]['file_rel_path'])})" if i > 1 else "시작"
        next_link = f"[{skeletons[str(i+1)]['title']}](./{os.path.basename(skeletons[str(i+1)]['file_rel_path'])})" if i < 26 else "끝"
        md_lines.append(f"- **넘버 이동**: [◀ 이전 곡: {prev_link}] | [목차](../README.md) | [다음 곡: {next_link} ▶]\n\n")
        md_lines.append("---\n\n")

        md_lines.append("## 📖 곡 개요 및 드라마적 배경\n\n")
        md_lines.append(f"{synopsis}\n\n")

        if notes:
            md_lines.append("## 💡 감상 포인트 및 주석 (Key Notes & 80s Pop Culture)\n\n")
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
        complete_doc.append(f"- **막(Act)**: Act {act}, Track {i:02d}\n\n")
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

    comp_file = os.path.join(base_dir, 'bttf_complete.md')
    with open(comp_file, 'w', encoding='utf-8') as cf:
        cf.writelines(complete_doc)

    print("Successfully built all BTTF individual markdown files and bttf_complete.md!")

def slugify_anchor(title):
    title = title.lower()
    title = re.sub(r'[\'\?\(\)\!\,\#\/\.]', '', title)
    title = re.sub(r'\s+', '-', title)
    return title.strip('-')

if __name__ == '__main__':
    build_bttf_markdown()
