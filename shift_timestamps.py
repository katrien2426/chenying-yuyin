#!/usr/bin/env python3
# 从 Track04 (トリッチ·トラッチ· ポルカ) 起，每句时间减 1 秒
# 若减后出现重复，后者加 1 秒递推

import re

MD = "汉化.md"

with open(MD, encoding="utf-8") as f:
    lines = f.readlines()

# 找 Track04 起始行（0-indexed）
start_line = None
track_count = 0
for i, line in enumerate(lines):
    if line.startswith("## "):
        if track_count == 4:
            start_line = i
            break
        track_count += 1

print(f"Track04 starts at line {start_line+1}")

def to_sec(m, s):
    return int(m)*60 + int(s)

def to_ts(sec):
    return f"{sec//60:02d}:{sec%60:02d}"

TIMESTAMP_RE = re.compile(r'^(\d{1,2}):(\d{2})(\s+.*)')

changed = 0
# track seen timestamps per-track to detect duplicates
seen = set()
prev_section = False

for i in range(len(lines)):
    if i < start_line:
        continue
    line = lines[i]
    if line.startswith("## ") and i > start_line:
        seen = set()  # reset per track
    if line.startswith("## "):
        seen = set()
        continue
    m = TIMESTAMP_RE.match(line.rstrip('\n'))
    if m:
        sec = to_sec(m.group(1), m.group(2)) - 1
        if sec < 0:
            sec = 0
        # resolve duplicate
        while sec in seen:
            sec += 1
        seen.add(sec)
        new_line = to_ts(sec) + m.group(3) + '\n'
        if new_line != line:
            changed += 1
        lines[i] = new_line

print(f"Modified {changed} timestamps")

with open(MD, "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Done")
