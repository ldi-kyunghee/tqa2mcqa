import json
import re

def extract_answer_from_raw(text):
    # 정규식: "Therefore, the answer is 37.5." 또는 "Therefore, the answer is 37.5\n"
    match = re.search(r"Therefore, the answer is\s+([^\n\.]+(?:\.\d+)?)(?:\.|\n|$)", text)
    return match.group(1).strip() if match else None

# Load original file
with open("wrong_for_CoT.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Update predictions
skipped = 0
for entry in data:
    raw = entry.get("raw_output", "")
    parsed = extract_answer_from_raw(raw)

    if parsed is not None:
        entry["prediction"] = parsed
    else:
        skipped += 1
        # 기존 prediction 유지
        print(f"[SKIPPED] id: {entry['id']} → 기존 prediction 유지")

# Save updated version
with open("wrong_for_CoT_updated.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"완료: 총 {len(data)}개 중 {skipped}개는 기존 prediction 유지됨.")

