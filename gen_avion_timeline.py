import json
from pathlib import Path

with open("scratch/fenrir_caida_avion_words.json", encoding="utf-8") as f:
    data = json.load(f)

words = []
for segment in data["segments"]:
    for w in segment.get("words", []):
        w_text = w["word"].strip().upper()
        if w_text:
            words.append({
                "word": w_text,
                "start": round(w["start"], 2),
                "end": round(w["end"], 2)
            })

# Chunk into 2-3 word blocks
chunks = []
i = 0
while i < len(words):
    take = 3
    if i + take > len(words):
        take = len(words) - i
    elif i + take == len(words) - 1:
        take = 2
    
    group = words[i:i+take]
    start_t = group[0]["start"]
    end_t = group[-1]["end"]
    if end_t - start_t < 0.65:
        end_t = round(start_t + 0.65, 2)
    
    chunks.append({
        "start": start_t,
        "end": end_t,
        "words": [w["word"] for w in group]
    })
    i += take

ts_lines = [
    "export interface SubtitleChunk {",
    "  start: number;",
    "  end: number;",
    "  words: string[];",
    "}",
    "",
    f"export const AVION_HIELO_TOTAL_FRAMES = 1966; // 65.53s @ 30 FPS",
    "export const AVION_HIELO_FPS = 30;",
    "",
    "export const AVION_SUBTITLES: SubtitleChunk[] = ["
]

for c in chunks:
    words_str = json.dumps(c["words"], ensure_ascii=False)
    ts_lines.append(f'  {{ start: {c["start"]}, end: {c["end"]}, words: {words_str} }},')

ts_lines.append("];")

out_ts = Path("flows/image_content_generator/remotion/src/avion_hielo_timeline.ts")
with open(out_ts, "w", encoding="utf-8") as f:
    f.write("\n".join(ts_lines))

print(f"Generated {len(chunks)} subtitle chunks in {out_ts}")
