import json
import random
import string

def prepare_mcq(sample):
    correct_answer = sample["ground_truth"]
    distractors = sample["wrong_row_distractors"]
    
    unknown_choice = "I don't know"
    
    all_choices = distractors + [correct_answer, unknown_choice]
    random.shuffle(all_choices)

    choice_labels = list(string.ascii_uppercase[:len(all_choices)])
    #labeled_choices = {label: choice for label, choice in zip(choice_labels, all_choices)}
    labeled_choices = {label: str(choice) for label, choice in zip(choice_labels, all_choices)}
    
    correct_label = next(label for label, val in labeled_choices.items() if val == correct_answer)
    return labeled_choices, correct_label

with open("../create_distractors/rule/wrong_row_distractors.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

results = []
for data in dataset:
    mcq_choices, answer = prepare_mcq(data)
    results.append({
        "id": data["id"],
        "question": data["question"],
        "mcq_choices": mcq_choices,
        "answer": answer  
    })

with open("MCQ5_choices_wrong_row.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("저장 완료")
