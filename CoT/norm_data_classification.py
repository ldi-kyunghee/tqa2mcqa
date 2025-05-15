import json

def is_float(val):
    try:
        float(val)
        return True
    except (ValueError, TypeError):
        return False

with open('normalized_predictions_cot.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

num_data = []
text_data = []
print(len(data))

for item in data:
    entry = {
        "id": item.get("id"),
        "ques": item.get("ques"),
        "ans": item.get("ground_truth"),
        "prediction" : item.get("prediction")
    }
    if is_float(entry["ans"]):
        num_data.append(entry)
    else:
        text_data.append(entry)

total_ans_count = len(num_data) + len(text_data)

with open("num_test_data_cot.json", "w", encoding="utf-8") as f:
    json.dump(num_data, f, ensure_ascii=False, indent=2)

with open("text_test_data_cot.json", "w", encoding="utf-8") as f:
    json.dump(text_data, f, ensure_ascii=False, indent=2)

print(f"총 ans 개수: {total_ans_count}개")
print(f"숫자형 ans 개수: {len(num_data)}개")
print(f"문자형 ans 개수: {len(text_data)}개")

