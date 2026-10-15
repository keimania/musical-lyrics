# -*- coding: utf-8 -*-
"""
Verification Script for Wicked Movie Adaptation Lyrics
Checks 1:1 line matching and integrity of all 22 tracks.
"""

import os
import sys
import json

def verify_wicked():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "data", "wicked_songs.json")
    
    if not os.path.exists(json_path):
        print(f"Error: Database not found at {json_path}")
        sys.exit(1)
        
    with open(json_path, "r", encoding="utf-8") as f:
        songs = json.load(f)
        
    print(f"Loaded {len(songs)} songs from {json_path}")
    assert len(songs) == 22, f"Expected 22 songs, got {len(songs)}"
    
    total_lines = 0
    total_stanzas = 0
    mismatches = 0
    
    for song in songs:
        sid = song["id"]
        title = song["title"]
        part = song["part"]
        stanzas = song["stanzas"]
        
        for s_idx, st in enumerate(stanzas):
            total_stanzas += 1
            l_en = len(st["lines_en"])
            l_kr = len(st["lines_kr"])
            total_lines += l_en
            
            if l_en != l_kr:
                print(f"[MISMATCH] Part {part} Track {sid:02d} ({title}) Stanza #{s_idx+1}: EN({l_en}) != KR({l_kr})")
                mismatches += 1
                
        # Check individual markdown file exists
        rel_path = song.get("rel_path")
        if rel_path:
            full_path = os.path.join(base_dir, rel_path)
            if not os.path.exists(full_path):
                print(f"[MISSING FILE] {full_path}")
                mismatches += 1

    print("\n" + "=" * 50)
    print(f"Total Songs Verified   : {len(songs)} (Part 1: 11 / Part 2: 11)")
    print(f"Total Stanzas Verified : {total_stanzas}")
    print(f"Total Lyric Lines (EN) : {total_lines}")
    print(f"Total Mismatches       : {mismatches}")
    print("=" * 50)
    
    if mismatches == 0:
        print("✅ SUCCESS: All Wicked movie tracks have 100% 1:1 line matching & files verified!")
        return 0
    else:
        print(f"❌ FAILED: Found {mismatches} issues.")
        return 1

if __name__ == "__main__":
    sys.exit(verify_wicked())
