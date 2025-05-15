import json
import re
from openai import OpenAI

client = OpenAI(
    api_key='sk-cNbZsZKsbfChfSKMUj66LdWoYqTm2A_FZPojkPQV7rT3BlbkFJIPk6gOBzIfG1yGjNUa1N2-HiNaM2ihDYb72evtpUQA'
)

# MCQ 데이터셋 로드
with open('MCQ_choices_random_noise.json', 'r', encoding="utf-8") as file:
    mcq_dataset = json.load(file)

# 문서 데이터 로드
with open('../Dataset/test.json', 'r', encoding="utf-8") as file:
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
    choice_A = data["mcq_choices"]["A"]
    choice_B = data["mcq_choices"]["B"]
    choice_C = data["mcq_choices"]["C"]
    choice_D = data["mcq_choices"]["D"]
    document = get_document(documents, id, question)
    
    system_input = """You are a scientific assistant. You are supposed to answer the following multiple-choice question based on the provided scientific document context. 

First, carefully read the document and think through the problem step by step, documenting each necessary step in your reasoning. After the reasoning process, conclude your response with the correct answer choice.

Your final sentence must be in the format: \"Therefore, the answer is (X).\", where X is A, B, C, or D."""

    user_input = f"""{document}

Question: {question}

Choices:
(A) {choice_A}
(B) {choice_B}
(C) {choice_C}
(D) {choice_D}

Let's think step by step to answer the given question."""

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

        match = re.search(r"(?:Therefore, the answer is|Among them,|Answer:|correct answer is)\s*(?:[0-9.]+\s*)?([A-D])\b", content)
        selected_choice = match.group(1) if match else None

        results.append({
            "id": id,
            "question": question,
            "answer" : answer,
            "response": content,
            "prediction": selected_choice
        })
        print(f"ID: {id}\nSelected: {selected_choice}\n")

    except Exception as e:
        results.append({"id": id, "question": question, "error": str(e)})
        print(f"Error processing ID {id}: {e}")

# 결과를 JSON 파일로 저장
with open('mcqa_random_noise_results_cot.json', 'w', encoding="utf-8") as outfile:
    json.dump(results, outfile, ensure_ascii=False, indent=2)

    