import json
import numpy as np

def generate_gaussian_distractors(answer, num_distractors=3, std_ratio=0.1):
    std_dev = abs(answer) * std_ratio if answer != 0 else 1.0
    distractors = set()
    while len(distractors) < num_distractors:
        noise = np.random.normal(0, std_dev)
        distractor = round(answer + noise, 2)
        if distractor != answer:
            distractors.add(distractor)
    return list(distractors)

def convert_to_mcqa_with_noise(data, num_distractors=3, std_ratio=0.1):
    result = []
    for item in data:
        try:
            ans = float(item["ans"])
        except ValueError:
            continue  # 수치형이 아닌 경우 건너뜀
        distractors = generate_gaussian_distractors(ans, num_distractors, std_ratio)
        result.append({
            "id": item["id"],
            "ques": item["ques"],
            "noise_distractors": distractors
        })
    return result


with open("num_test_data_cot.json", "r", encoding="utf-8") as f:
    data = json.load(f)

mcqa_data = convert_to_mcqa_with_noise(data)

with open("num_noise_distractors_cot.json", "w") as f:
    json.dump(mcqa_data, f, indent=2)

