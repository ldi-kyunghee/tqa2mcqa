import json
import re
from datasets import load_dataset
from openai import OpenAI

client = OpenAI(
    api_key=''
)

'''
def is_float(val):
    try:
        float(val)
        return True
    except:
        return False
'''

with open("Dataset/test.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

results = []


for sample in dataset:
    doc_id = sample["id"]
    caption = sample.get("caption", "")
    description = sample.get("description", "")
    table = sample.get("table", [])

    table_str = "\n".join(["\t".join(row) for row in table])

    document = f"{caption}\n\n{description}\n\nTable:\n{table_str}"

    for i, qa in enumerate(sample.get("qa", [])):
        question = qa["ques"]
        ground_truth = qa["ans"]
        tag = qa["tag"]
        qid = f"{doc_id}_q{i}"
    
        system_input = """You are a scientific assistant. You are supposed to generate a Python program to answer the given question.The answer may be either a number or a short descriptive phrase, depending on the question type. Here is an example of the Python program:
    ```python
    def solution():
        # Define variables and values based on the given context
        ...
        # Do computation to get the answer
        ...
        # return answer
        return answer
    ```"""

        user_input = f"""{document}

    Question: {question}

    Continue the program to answer the question. The returned value of the program is supposed to be the answer:
    ```python
    def solution():
        # Define variables name and value based on the given context
    """

        prediction = None
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=1.8,
                max_tokens=512,
                messages=[
                    {"role": "system", "content": system_input},
                    {"role": "user", "content": user_input}
                ]
            )
            content = response.choices[0].message.content
            match = re.search(r"```python(.*?)```", content, re.DOTALL)
            code_block = match.group(1).strip() if match else content
            prediction = content.strip()
            
            '''
            if is_float(ground_truth): 
                exec_globals = {}
                exec(code_block, exec_globals)
                prediction = exec_globals["solution"]()
            else: 
                prediction = content.strip()
            '''

        except Exception as e:
            prediction = None
            print(f"[{qid}] 처리 오류: {e}")

        results.append({
            "id": qid,
            "ques": question,
            "ground_truth": ground_truth,
            "prediction": prediction,
        })

with open("test_temp(1.8).json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
