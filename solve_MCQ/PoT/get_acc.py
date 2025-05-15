import json


# random gaussian noise
with open('mcqa_random_noise_results_cot_re.json', 'r', encoding="utf-8") as file:
    mcqa_results = json.load(file)
    
total = len(mcqa_results)  
correct = 0

for result in mcqa_results:
    answer = result["answer"]
    prediction = result["prediction"]
    
    if answer == prediction:
        correct += 1
        
print(f"random gaussian noise CoT Accuracy : {correct / total:.2%} ({correct}/{total})")


# wrong_row
with open('mcqa_wrong_row_results_cot_re.json', 'r', encoding="utf-8") as file:
    mcqa_results = json.load(file)
    
total = len(mcqa_results)  
correct = 0

for result in mcqa_results:
    answer = result["answer"]
    prediction = result["prediction"]
    
    if answer == prediction:
        correct += 1

print(f"wrong row CoT Accuracy : {correct / total:.2%} ({correct}/{total})")


# wrong_column
with open('mcqa_wrong_column_results_cot_re.json', 'r', encoding="utf-8") as file:
    mcqa_results = json.load(file)
    
total = len(mcqa_results)  
correct = 0

for result in mcqa_results:
    answer = result["answer"]
    prediction = result["prediction"]
    
    if answer == prediction:
        correct += 1
        
print(f"wrong column CoT Accuracy : {correct / total:.2%} ({correct}/{total})")

