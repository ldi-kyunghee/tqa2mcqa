import json
"""
with open("wrong_for_CoT_updated.json", "r", encoding="utf-8") as f:
    new_pred = json.load(f)
    
with open("model_distractors.json", "r", encoding="utf-8") as f:
    distractors_data = json.load(f)
    

def is_correct(gold, pred):
    try:
        return float(gold) == float(pred)
    except (ValueError, TypeError):
        return str(gold).strip().lower() == str(pred).strip().lower()
    

def model_distractors_update(new_pred):
    new_dict = {(item['id'], item['question']): item for item in new_pred}
    
    result = []

    for org_data in distractors_data:
        key = (org_data['id'], org_data['ques'])
        new_item = new_dict.get(key)

        if new_item is None:
            result.append(org_data)
            continue  

        distractors = org_data["model_distractors"]
        new_pred = new_item['prediction']
        gold = new_item['ground_truth'] 


        if not is_correct(gold, new_pred) and new_pred not in distractors:
            if new_pred is not None:
                distractors.append(new_pred)

        # 결과 누적
        result.append({
            "id": org_data["id"],
            "ques": org_data["ques"],
            "ground_truth": gold,
            "model_distractors": distractors
        })

    return result
        
updated_data = model_distractors_update(new_pred)

with open("model_distractors.json", "w", encoding="utf-8") as f:
    json.dump(updated_data, f, ensure_ascii=False, indent=2)
"""

with open("model_distractors_re.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("데이터 개수:", len(data))  
