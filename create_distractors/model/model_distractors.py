import json

with open("../../PoT/normalized_predictions_pot.json", "r", encoding="utf-8") as f:
    pot_dataset = json.load(f)
    
with open("../../CoT/normalized_predictions_cot.json", "r", encoding="utf-8") as f:
    cot_dataset = json.load(f)


def is_correct(gold, pred):
    try:
        return float(gold) == float(pred)
    except (ValueError, TypeError):
        return str(gold).strip().lower() == str(pred).strip().lower()

    

def model_distractors(pot_dataset, cot_dataset):
    cot_dict = {(item['id'], item['ques']): item for item in cot_dataset}
    
    result = []

    for pot_item in pot_dataset:
        key = (pot_item['id'], pot_item['ques'])
        cot_item = cot_dict.get(key)

        if cot_item is None:
            continue  

        pot_pred = pot_item['prediction']
        cot_pred = cot_item['prediction']
        gold = pot_item['ground_truth'] 

        distractors = []
        if(pot_pred == cot_pred):
            if not is_correct(gold, pot_pred):
                distractors.append(pot_pred)
        else:
            if (pot_pred != "EXECUTION_ERROR") and (not is_correct(gold, pot_pred)):
                distractors.append(pot_pred)
            if (cot_pred is not None) and (not is_correct(gold, cot_pred)):
                distractors.append(cot_pred)


        result.append({
            "id": pot_item['id'],
            "ques": pot_item['ques'], 
            "ground_truth": pot_item['ground_truth'],
            "model_distractors": distractors
        })

    return result

md = model_distractors(pot_dataset, cot_dataset)

with open("model_distractors.json", "w", encoding="utf-8") as f:
    json.dump(md, f, indent=2, ensure_ascii=False)
    