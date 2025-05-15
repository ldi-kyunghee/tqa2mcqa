import json
import re
from openai import OpenAI

client = OpenAI(
    api_key='sk-cNbZsZKsbfChfSKMUj66LdWoYqTm2A_FZPojkPQV7rT3BlbkFJIPk6gOBzIfG1yGjNUa1N2-HiNaM2ihDYb72evtpUQA'
)

# MCQ 데이터셋 로드
with open('../MCQ_choices_wrong_column.json', 'r', encoding="utf-8") as file:
    mcq_dataset = json.load(file)

# 문서 데이터 로드
with open('../../Dataset/test.json', 'r', encoding="utf-8") as file:
    documents = json.load(file)

def get_document(documents, target_id, target_ques):
    for sample in documents:
        if sample["id"] == target_id and sample["question"] == target_ques:
            caption = sample.get("caption", "")
            description = sample.get("description", "")
            table = sample.get("table", [])

            if table:
                header = " | ".join(table[0])
                divider = " | ".join(["---"] * len(table[0]))
                rows = [" | ".join(row) for row in table[1:]]
                table_str = "\n".join([header, divider] + rows)
            else:
                table_str = ""

            document = f"{caption}\n\n{description}\n\n{table_str}"
            return document
    return ""

results = []

for data in mcq_dataset:
    id = data["id"]
    question = data["question"]
    answer = data["answer"]
    mcq_choices = data["mcq_choices"]
    document = get_document(documents, id, question)

    system_input = """You are a scientific assistant. You are supposed to generate a Python program to answer the given multiple-choice question. The question provides a set of choices as a dictionary, where keys are "A", "B", "C", "D", and values are the answer options.

Your task is to compute the correct answer based on the given context and return the correct choice key (e.g., "A", "B", "C", or "D").

Here is an example of the Python program structure:
```python
def solution():
    choices = {
        "A": "...",
        "B": "...",
        "C": "...",
        "D": "..."
    }
    # Perform computations based on the context
    return answer  # return the correct key
```"""


    user_input = f"""{document}

Question: {question}

Continue the program to answer the question. Return the correct choice key:
```python
def solution():
    choices = {mcq_choices}
    # Perform computation to select the correct answer
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=512,
            messages=[
                {"role": "system", "content": system_input},
                {"role": "user", "content": user_input}
            ]
        )
        content = response.choices[0].message.content or ""


        code_match = re.search(r"```python(.*?)```", content, re.DOTALL)
        code_block = code_match.group(1).strip() if code_match else ""


        local_vars = {}
        exec(code_block, {}, local_vars)  
        predicted_choice = local_vars['solution']() 

        results.append({
            "id": id,
            "question": question,
            "answer": answer,
            "response": content,
            "prediction": predicted_choice
        })
        print(f"ID: {id}\nSelected: {predicted_choice}\n")

    except Exception as e:
        results.append({"id": id, "question": question, "error": str(e)})
        print(f"Error processing ID {id}: {e}")


with open('mcqa_wrong_column_results_pot.json', 'w', encoding="utf-8") as outfile:
    json.dump(results, outfile, ensure_ascii=False, indent=2)
    

