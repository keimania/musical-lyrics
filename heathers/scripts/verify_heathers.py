# -*- coding: utf-8 -*-
"""
Verification Script for Heathers Lyrics Integrity & Line Matching
"""

import os
import sys
import json

def verify_heathers():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "data", "heathers_songs.json")

    if not os.path.exists(json_path):
        print(f"Error: Database not found at {json_path}")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        songs = json.load(f)

    assert len(songs) == 21, f"Expected 21 songs, got {len(songs)}"

    total_lines = 0
    total_stanzas = 0
    mismatches = 0

    for song in songs:
        sid = song["id"]
        title = song["title"]
        act = song["act"]
        stanzas = song["stanzas"]

        for s_idx, st in enumerate(stanzas):
            total_stanzas += 1
            l_en = len(st["lines_en"])
            l_kr = len(st["lines_kr"])
            total_lines += l_en

            if l_en != l_kr:
                print(f"[MISMATCH] Act {act} Track {sid:02d} ({title}) Stanza #{s_idx+1}: EN({l_en}) != KR({l_kr})")
                mismatches += 1

        rel_path = song.get("rel_path")
        if rel_path:
            full_path = os.path.join(base_dir, rel_path)
            if not os.path.exists(full_path):
                print(f"[MISSING FILE] {full_path}")
                mismatches += 1

    print("\n" + "=" * 50)
    print(f"Total Songs Verified   : {len(songs)} (Act 1: 9 / Act 2: 12)")
    print(f"Total Stanzas Verified : {total_stanzas}")
    print(f"Total Lyric Lines (EN) : {total_lines}")
    print(f"Total Mismatches       : {mismatches}")
    print("=" * 50)

    if mismatches == 0:
        print("✅ SUCCESS: All Heathers tracks verified 100% 1:1 aligned!")
        return 0
    else:
        print(f"❌ FAILED: Found {mismatches} issues.")
        return 1

if __name__ == "__main__":
    sys.exit(verify_heathers())
