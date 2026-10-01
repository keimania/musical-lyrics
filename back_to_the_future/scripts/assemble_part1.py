import json
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(base_dir, 'scripts'))

from build_part1_tracks1_5 import part1_data as p1
from build_part1_tracks6_9 import part1_data as p2
from build_part1_tracks10_13 import part1_data as p3

merged_data = {}
merged_data.update(p1)
merged_data.update(p2)
merged_data.update(p3)

output_path = os.path.join(base_dir, 'data', 'trans_part1.json')

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {output_path} with {len(merged_data)} tracks.")
