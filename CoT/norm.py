import json

with open("test_for_CoT_updated.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

new_results = []
print(len(dataset))

for sample in dataset:
    doc_id = sample["id"]
    ques = sample["question"]
    ground_truth = sample["ground_truth"]
    prediction = sample["prediction"]
    
    new_results.append({
        "id": doc_id,
        "ques": ques,
        "ground_truth": ground_truth,
        "prediction": prediction, 
    })
    
print(len(new_results))
with open("normalized_predictions_cot.json", "w", encoding="utf-8") as f:
    json.dump(new_results, f, ensure_ascii=False, indent=2)

print("저장 완료: normalized_predictions_cot.json")