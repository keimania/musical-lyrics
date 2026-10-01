# -*- coding: utf-8 -*-
import json
import os
import sys

# Ensure current workspace is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.songs_24_25 import get_song_24, get_song_25
from scripts.songs_26_27 import get_song_26, get_song_27
from scripts.song_28 import get_song_28
from scripts.songs_29_30_31 import get_song_29, get_song_30, get_song_31

def build_trans_part4():
    trans_data = {
        "24": get_song_24(),
        "25": get_song_25(),
        "26": get_song_26(),
        "27": get_song_27(),
        "28": get_song_28(),
        "29": get_song_29(),
        "30": get_song_30(),
        "31": get_song_31(),
    }
    
    output_path = 'data/trans_part4.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(trans_data, f, ensure_ascii=False, indent=2)
    print(f"Successfully wrote {output_path} with {len(trans_data)} songs!")

if __name__ == '__main__':
    build_trans_part4()
