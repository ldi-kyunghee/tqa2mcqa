import json

def is_float(val):
    try:
        float(val)
        return True
    except (ValueError, TypeError):
        return False

with open('normalized_predictions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

num_data = []
text_data = []
total_ans_count = 0

for item in data:
    for qa in item.get("qa", []):
        total_ans_count += 1
        qa_entry = {
            "id": item.get("id"),
            "ques": qa.get("ques"),
            "ans": qa.get("ans"),
            "tag": qa.get("tag")
        }
        if is_float(qa.get("ans")):
            num_data.append(qa_entry)
        else:
            text_data.append(qa_entry)

with open("num_test_data.json", "w", encoding="utf-8") as f:
    json.dump(num_data, f, ensure_ascii=False, indent=2)

with open("text_test_data.json", "w", encoding="utf-8") as f:
    json.dump(text_data, f, ensure_ascii=False, indent=2)

print(f"총 ans 개수: {total_ans_count}개")
print(f"숫자형 ans 개수: {len(num_data)}개")
print(f"문자형 ans 개수: {len(text_data)}개")


