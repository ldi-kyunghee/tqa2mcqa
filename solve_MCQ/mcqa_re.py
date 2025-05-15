import re
import json

with open("PoT/mcqa_wrong_column_results_pot.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

results = []

def extract_choice(text):
    match = re.search(r"\(\s*([A-D])\s*\)", text)
    if match:
        return match.group(1)
    
    match = re.search(
        r"(?:Therefore, the answer is|Among them,|Answer:|correct answer is)\s*(?:[0-9.]+\s*)?([A-D])\b",
        text
    )
    if match:
        return match.group(1)

    return None


for data in dataset:
    if data["prediction"] == None:
        raw_response = data["response"]
        selected_choice = extract_choice(raw_response)
        results.append({
        "id": data["id"],
        "question": data["question"],
        "answer": data["answer"],
        "response": data["response"],
        "prediction": selected_choice
        })
    else:
        results.append(data)

    

with open("PoT/mcqa_wrong_column_results_pot_re.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
