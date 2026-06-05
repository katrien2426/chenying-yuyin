#!/usr/bin/env python3
import re, json

MD = "汉化.md"
HTML = "尘影余音.html"

with open(MD, encoding="utf-8") as f:
    content = f.read()

sections = re.split(r'^## ', content, flags=re.MULTILINE)
sections = [s for s in sections if s.strip()]

# audio file mapping: section title -> track filename
import os
mp3_files = sorted(os.listdir("mp3"))

tracks = []
for i, sec in enumerate(sections):
    lines = sec.split('\n')
    title = lines[0].strip()
    audio = mp3_files[i] if i < len(mp3_files) else ""

    entries = []
    # parse entries: line matching MM:SS or H:MM:SS speaker
    j = 1
    while j < len(lines):
        line = lines[j].strip()
        m = re.match(r'^(\d+):(\d{2})(?::(\d{2}))?\s+(.*)', line)
        if m:
            if m.group(3) is not None:
                t = int(m.group(1))*3600 + int(m.group(2))*60 + int(m.group(3))
            else:
                t = int(m.group(1))*60 + int(m.group(2))
            speaker = m.group(4).strip()
            ja = ""
            zh = ""
            j += 1
            while j < len(lines):
                l = lines[j].strip()
                if l.startswith("日文："):
                    ja = l[3:].strip()
                elif l.startswith("中文："):
                    zh = l[3:].strip()
                    break
                elif re.match(r'^\d+:\d{2}', l) or (l.startswith("##") ):
                    break
                j += 1
            if ja or zh:
                entries.append({"time": float(t), "speaker": speaker, "ja": ja, "zh": zh})
        j += 1

    tracks.append({"title": title, "audio": f"mp3/{audio}", "entries": entries})

tracks_json = json.dumps(tracks, ensure_ascii=False, separators=(',', ': '))

with open(HTML, encoding="utf-8") as f:
    html = f.read()

new_html = re.sub(r'var TRACKS=\[.*?\];', f'var TRACKS={tracks_json};', html, flags=re.DOTALL)

with open(HTML, "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"Done: {len(tracks)} tracks")
for t in tracks:
    print(f"  {t['title']}: {len(t['entries'])} entries, audio={t['audio']}")
