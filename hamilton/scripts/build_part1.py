# -*- coding: utf-8 -*-
import json
import os
import sys

from part1_data.song1 import song1_data
from part1_data.song2 import song2_data
from part1_data.song3 import song3_data
from part1_data.song4 import song4_data
from part1_data.song5 import song5_data
from part1_data.song6 import song6_data
from part1_data.song7 import song7_data
from part1_data.song8 import song8_data

def main():
    songs = {
        "1": song1_data,
        "2": song2_data,
        "3": song3_data,
        "4": song4_data,
        "5": song5_data,
        "6": song6_data,
        "7": song7_data,
        "8": song8_data
    }

    # Load input data
    with open('data/part1_input.json', 'r', encoding='utf-8') as f:
        input_data = json.load(f)

    # Validate before writing
    errors = []
    total_lines = 0
    total_stanzas = 0

    for sid, sdata in input_data.items():
        if sid not in songs:
            errors.append(f"Missing song {sid}")
            continue
        st_trans = songs[sid]
        if not st_trans.get('synopsis'):
            errors.append(f"Song {sid} missing synopsis")
        if len(st_trans.get('notes', [])) < 3:
            errors.append(f"Song {sid} has fewer than 3 notes (has {len(st_trans.get('notes', []))})")

        trans_dict = st_trans.get('translations', {})
        for stanza in sdata['stanzas']:
            key = stanza['key']
            total_stanzas += 1
            if key not in trans_dict:
                errors.append(f"Song {sid} missing stanza {key}")
                continue
            orig_lines = stanza['lines']
            trans_lines = trans_dict[key]
            if len(orig_lines) != len(trans_lines):
                errors.append(f"Song {sid} stanza {key} line mismatch: expected {len(orig_lines)}, got {len(trans_lines)}")
            else:
                for idx, (ol, tl) in enumerate(zip(orig_lines, trans_lines)):
                    total_lines += 1
                    if not tl or not tl.strip():
                        errors.append(f"Song {sid} stanza {key} line {idx} is empty.")
                    if tl.strip() == ol.strip() and len(tl.strip()) > 15:
                        errors.append(f"Song {sid} stanza {key} line {idx} appears untranslated: '{tl}'")

    if errors:
        print(f"Pre-validation failed with {len(errors)} errors:")
        for err in errors[:20]:
            print("  -", err)
        sys.exit(1)

    print(f"Pre-validation passed! Total stanzas: {total_stanzas}, Total lines: {total_lines}")

    # Write to data/trans_part1.json
    output_path = 'data/trans_part1.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(songs, f, ensure_ascii=False, indent=2)

    print(f"Wrote data to {output_path} successfully.")

if __name__ == '__main__':
    main()
