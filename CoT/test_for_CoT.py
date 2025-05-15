import json
import re
from datasets import load_dataset
from openai import OpenAI

client = OpenAI(
    api_key='sk-cNbZsZKsbfChfSKMUj66LdWoYqTm2A_FZPojkPQV7rT3BlbkFJIPk6gOBzIfG1yGjNUa1N2-HiNaM2ihDYb72evtpUQA'
)


with open("Dataset/test.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

results = []


def extract_answer(text):
    match = re.search(r"Therefore, the answer is (.+?)(\.|\n|$)", text)
    return match.group(1).strip() if match else None

for sample in dataset:
    doc_id = sample["id"]
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

    for i, qa in enumerate(sample.get("qa", [])):
        question = qa["ques"]
        ground_truth = qa["ans"]
        tag = qa["tag"]
        qid = f"{doc_id}_q{i}"

        system_input = """You are a scientific assistant, you are supposed to answer the given question based on the provided scientific document context. You need to first think through the problem step by step. documenting each necessary step. Then you are required to conclude your response with the final answer in your last sentence as "Therefore, the answer is {final answer}". The final answer should be either a numeric value or a short textual phrase, directly inferred from the table."""

        user_input = f"""{document}

Question: {question}

Let's think step by step to answer the given question."""

        prediction_text = ""
        parsed_answer = None

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                max_tokens=512,
                messages=[
                    {"role": "system", "content": system_input},
                    {"role": "user", "content": user_input}
                ]
            )
            content = response.choices[0].message.content
            prediction_text = content.strip()
            parsed_answer = extract_answer(prediction_text)

        except Exception as e:
            print(f"[{qid}] 처리 오류: {e}")

        results.append({
            "id": qid,
            "question": question,
            "ground_truth": ground_truth,
            "raw_output": prediction_text,
            "prediction": parsed_answer,
        })

with open("test_for_CoT.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("저장 완료: test_for_CoT.json")