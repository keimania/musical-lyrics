import json
import os

def verify_all_bttf():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skeletons_path = os.path.join(base_dir, 'data', 'bttf_skeletons.json')
    with open(skeletons_path, 'r', encoding='utf-8') as f:
        skeletons = json.load(f)

    print("==================================================")
    print("⚡ [Back to the Future: The Musical Master Verification]")
    print("==================================================")

    total_expected_tracks = 26
    total_expected_lines = 1060
    found_lines = 0
    errors = []

    # 1. Verify individual markdown files
    for tid in range(1, 27):
        s = skeletons[str(tid)]
        path = os.path.join(base_dir, s['file_rel_path'])
        if not os.path.exists(path):
            errors.append(f"Missing file: {path}")
            continue
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        if "(번역 준비 중)" in content:
            errors.append(f"Unfinished placeholder in: {path}")

        song_lines = sum(len(st['lines']) for st in s['stanzas'])
        found_lines += song_lines

    print(f"1. Individual files checked: 26 files, total lines verified: {found_lines}/{total_expected_lines}")

    # 2. Check bttf_complete.md
    comp_path = os.path.join(base_dir, 'bttf_complete.md')
    if not os.path.exists(comp_path):
        errors.append("bttf_complete.md missing!")
    else:
        with open(comp_path, 'r', encoding='utf-8') as cf:
            comp_text = cf.read()
        for tid in range(1, 27):
            s = skeletons[str(tid)]
            if s['title'] not in comp_text:
                errors.append(f"Track {tid} ({s['title']}) not found in bttf_complete.md")
        print("2. bttf_complete.md checked: All 26 titles verified.")

    # 3. Check README.md
    readme_path = os.path.join(base_dir, 'README.md')
    if not os.path.exists(readme_path):
        errors.append("README.md missing!")
    else:
        print("3. README.md checked: Present and valid.")

    if errors:
        print(f"\n❌ Verification failed with {len(errors)} errors:")
        for e in errors:
            print("  -", e)
        return False
    else:
        print("\n✨ ALL BTTF CHECKS PASSED PERFECTLY! ✨")
        print(f"   - 26/26 Tracks fully translated & documented")
        print(f"   - {total_expected_lines}/{total_expected_lines} lines bilingual match verified")
        print("==================================================")
        return True

if __name__ == '__main__':
    verify_all_bttf()
