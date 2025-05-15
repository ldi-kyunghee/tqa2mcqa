import json

# 1. 전체 QA 기준 (test.json)
with open("../../Dataset/test.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

all_keys = []
for sample in dataset:
    doc_id = sample["id"]
    for i, qa in enumerate(sample.get("qa", [])):
        qid = f"{doc_id}_q{i}"
        question = qa["ques"]
        all_keys.append((qid, question))

print(f"📌 test.json 기준 전체 QA 수: {len(all_keys)}개")

# 2. distractor 생성된 결과 (model_distractors.json)
with open("model_distractors_re_with_gt.json", "r", encoding="utf-8") as f:
    distractor_data = json.load(f)

existing_keys = set((item["id"], item["ques"]) for item in distractor_data)

# 3. 누락된 QA 찾기
missing_keys = [key for key in all_keys if key not in existing_keys]

print(f"🚨 누락된 (id, ques) 수: {len(missing_keys)}개")

# 4. 결과 일부 출력
for key in missing_keys[:5]:
    print("누락된 QA:", key)

# 5. 원하면 파일로 저장
with open("missing_distractor_keys.json", "w", encoding="utf-8") as f:
    json.dump([{"id": id_, "ques": ques} for (id_, ques) in missing_keys], f, ensure_ascii=False, indent=2)

