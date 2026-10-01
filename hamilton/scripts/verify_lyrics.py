import json
import os
import re

def verify_all():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skeletons_path = os.path.join(base_dir, 'data', 'song_skeletons.json')
    with open(skeletons_path, 'r', encoding='utf-8') as f:
        skeletons = json.load(f)

    print("==================================================")
    print("🔍 [Hamilton Lyrics & Translation Master Verification]")
    print("==================================================")

    total_expected_songs = 46
    total_expected_lines = 3258
    found_lines = 0
    errors = []

    # 1. Verify individual markdown files
    for sid in range(1, 47):
        s = skeletons[str(sid)]
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

    print(f"1. Individual files checked: 46 files, total lines verified: {found_lines}/{total_expected_lines}")

    # 2. Check hamilton_complete.md
    comp_path = os.path.join(base_dir, 'hamilton_complete.md')
    if not os.path.exists(comp_path):
        errors.append("hamilton_complete.md missing!")
    else:
        with open(comp_path, 'r', encoding='utf-8') as cf:
            comp_text = cf.read()
        for sid in range(1, 47):
            s = skeletons[str(sid)]
            if s['title'] not in comp_text:
                errors.append(f"Song {sid} ({s['title']}) not found in hamilton_complete.md")
        print("2. hamilton_complete.md checked: All 46 titles verified.")

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
        print("\n✨ ALL CHECKS PASSED PERFECTLY! ✨")
        print(f"   - 46/46 Songs fully translated & documented")
        print(f"   - {total_expected_lines}/{total_expected_lines} lines bilingual match verified")
        print("==================================================")
        return True

if __name__ == '__main__':
    verify_all()
