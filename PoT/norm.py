import re
import json
from evaluation_utils import normalize

def normalize_textual_answer(ans: str) -> str:
    if not isinstance(ans, str):
        ans = str(ans)
    
    # 1. 기본 정리
    #ans = ans.strip().upper()
    ans = ans.rstrip('.')  # 끝 마침표 제거
    ans = re.sub(r'\s+', ' ', ans)  # 여러 공백 → 하나

    # 2. 특수문자 제거
    ans = ans.replace('`', '')
    ans = ans.replace('"', '')
    ans = ans.replace("'", '')
    ans = ans.replace("–", "-")  # en dash
    ans = ans.replace("—", "-")  # em dash

    # 3. 의미적 매핑
    mapping = {
        "yes": "yes",
        "no": "no",
        "true": "yes",
        "false": "no",
        "n/a": "n/a",
        "not available": "n/a",
        "not applicable": "n/a",
        "greater than": "greater than",
        "less than": "less than",
        "equal": "equal",
        "none": "none"
    }

    # clean dash spacing (e.g., 'dataset - moderate' → 'dataset-moderate')
    ans = re.sub(r'\s*-\s*', '-', ans)

    if ans in mapping:
        return mapping[ans]

    # 4. fallback: 그대로 반환
    return ans


import re

def extract_python_code_block(prediction: str) -> str:
    match = re.search(r"```python(.*?)```", prediction, re.DOTALL)
    code_block = match.group(1).strip() if match else prediction.strip()
    
    code_block = re.sub(r'print\s*\(.*?\)', '', code_block)

    code_block = re.sub(r'^[ \t]*\)[ \t]*$', '', code_block, flags=re.MULTILINE)
    
    return code_block


def is_float(val):
    try:
        float(val)
        return True
    except:
        return False

with open("test_for_PoT.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

new_results = []
print(len(dataset))

for sample in dataset:
    doc_id = sample["id"]
    ques = sample["ques"]
    ground_truth = sample["ground_truth"]
    raw_prediction = sample["prediction"]
    
    prediction = extract_python_code_block(raw_prediction)
    try:
        exec_globals = {}
        exec(prediction, exec_globals)
        result = exec_globals["solution"]()
    except Exception as e:
        print(f"[{doc_id}] 실행 실패!\n에러: {e}\n예상 코드:\n{prediction}\n{'='*60}")
        result = "EXECUTION_ERROR"
        
    '''
    exec_globals = {}
    exec(prediction, exec_globals)
    result = exec_globals["solution"]() 
    '''
    if is_float(result):
        result = str(result)
        norm_result = normalize(result)
    else:
        norm_result = normalize_textual_answer(result)
    
    new_results.append({
        "id": doc_id,
        "ques": ques,
        "ground_truth": ground_truth,
        "prediction": str(norm_result), 
    })
    
print(len(new_results))
with open("normalized_predictions_pot.json", "w", encoding="utf-8") as f:
    json.dump(new_results, f, ensure_ascii=False, indent=2)

print("저장 완료: normalized_predictions_pot.json")


