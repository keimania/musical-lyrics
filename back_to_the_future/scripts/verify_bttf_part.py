import json
import sys
import os

def verify_part(part_num):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    input_path = os.path.join(base_dir, 'data', f'part{part_num}_input.json')
    trans_path = os.path.join(base_dir, 'data', f'trans_part{part_num}.json')
    
    if not os.path.exists(trans_path):
        print(f"Error: {trans_path} does not exist.")
        return False
        
    with open(input_path, 'r', encoding='utf-8') as f:
        input_data = json.load(f)
    with open(trans_path, 'r', encoding='utf-8') as f:
        trans_data = json.load(f)
        
    errors = []
    total_stanzas = 0
    total_lines = 0
    
    for sid, sdata in input_data.items():
        if sid not in trans_data:
            errors.append(f"Track {sid} ({sdata['title']}) missing from translations.")
            continue
            
        st_trans = trans_data[sid]
        if not st_trans.get('synopsis'):
            errors.append(f"Track {sid} missing synopsis.")
        if not st_trans.get('notes') or len(st_trans.get('notes', [])) < 2:
            errors.append(f"Track {sid} has insufficient notes.")
            
        trans_dict = st_trans.get('translations', {})
        for stanza in sdata['stanzas']:
            key = stanza['key']
            total_stanzas += 1
            if key not in trans_dict:
                errors.append(f"Track {sid} missing translation for stanza key: {key}")
                continue
                
            orig_lines = stanza['lines']
            trans_lines = trans_dict[key]
            
            if len(orig_lines) != len(trans_lines):
                errors.append(f"Track {sid} stanza {key} line count mismatch: expected {len(orig_lines)}, got {len(trans_lines)}")
            else:
                for idx, (ol, tl) in enumerate(zip(orig_lines, trans_lines)):
                    total_lines += 1
                    if not tl or not tl.strip():
                        errors.append(f"Track {sid} stanza {key} line {idx} is empty.")
                    if tl.strip() == ol.strip() and len(tl.strip()) > 25 and not ol.startswith('('):
                        errors.append(f"Track {sid} stanza {key} line {idx} appears untranslated: '{tl}'")
                        
    if errors:
        print(f"❌ Part {part_num} verification failed with {len(errors)} errors:")
        for err in errors[:20]:
            print("  -", err)
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more errors.")
        return False
    else:
        print(f"✅ Part {part_num} verified successfully! ({len(input_data)} tracks, {total_stanzas} stanzas, {total_lines} lines translated)")
        return True

if __name__ == '__main__':
    if len(sys.argv) > 1:
        part_num = int(sys.argv[1])
        success = verify_part(part_num)
        sys.exit(0 if success else 1)
    else:
        all_ok = True
        for p in [1, 2]:
            if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', f'trans_part{p}.json')):
                ok = verify_part(p)
                if not ok: all_ok = False
            else:
                print(f"Part {p} not ready yet.")
                all_ok = False
        sys.exit(0 if all_ok else 1)
