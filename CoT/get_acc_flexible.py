import json
import math

def within_eps(pred, gt, eps=1e-3):
    try:
        return abs(float(pred) - float(gt)) < eps
    except:
        return False

def round_up_to_decimal(x, dec=3):
    return round(x, dec)

def compare_two_numbers(p, gt):
    try:
        p = float(p)
        gt = float(gt)
    except:
        return False

    v1, v2 = max(abs(gt), abs(p)), min(abs(gt), abs(p))

    try:
        if (v1 != 0 and v2 != 0) and int(math.log10(v1 / v2)) == math.log10(v1 / v2):
            return True
    except:
        pass

    if v2 <= v1 / 50 and within_eps(v2 * 100, v1):
        return True
    elif v2 <= v1 / 500 and within_eps(v2 * 1000, v1):
        return True
    elif v2 <= v1 / 50000 and within_eps(v2 * 100000, v1):
        return True

    if round_up_to_decimal(v1, 3) == round_up_to_decimal(v2, 3):
        return True

    return within_eps(p, gt)

def get_acc_flexible(prediction, gt):
    try:
        try:
            pred_float = float(prediction)
            gt_float = float(gt)
            return int(compare_two_numbers(pred_float, gt_float))
        except:
            pass

        pred_str = str(prediction).strip().lower()
        gt_str = str(gt).strip().lower()
        return int(pred_str == gt_str)

    except Exception:
        return 0

file_path = "num_test_data_cot.json"
with open(file_path, 'r', encoding="utf-8") as f:
    num_data = json.load(f)

wrong_num_data = []
correct = 0

for item in num_data:
    acc = get_acc_flexible(item["prediction"], item["ans"])
    if acc == 1:
        correct += 1
    else:
        wrong_num_data.append(item)

total = len(num_data)
print(f"num_CoT Accuracy: {correct / total:.2%} ({correct}/{total})")

with open("wrong_num_data_cot.json", "w", encoding="utf-8") as f:
    json.dump(wrong_num_data, f, ensure_ascii=False, indent=2)


file_path = "text_test_data_cot.json"
with open(file_path, 'r', encoding="utf-8") as f:
    text_data = json.load(f)

wrong_text_data = []
correct = 0

for item in text_data:
    acc = get_acc_flexible(item["prediction"], item["ans"])
    if acc == 1:
        correct += 1
    else:
        wrong_text_data.append(item)

total = len(text_data)
print(f"text_CoT Accuracy: {correct / total:.2%} ({correct}/{total})")

with open("wrong_text_data_cot.json", "w", encoding="utf-8") as f:
    json.dump(wrong_text_data, f, ensure_ascii=False, indent=2)


