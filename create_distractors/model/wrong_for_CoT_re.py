import json
import re
from openai import OpenAI

client = OpenAI(
    api_key='sk-cNbZsZKsbfChfSKMUj66LdWoYqTm2A_FZPojkPQV7rT3BlbkFJIPk6gOBzIfG1yGjNUa1N2-HiNaM2ihDYb72evtpUQA'
)

def extract_answer(text):
    match = re.search(r"Therefore, the answer is\s+([^\n\.]+(?:\.\d+)?)(?:\.|\n|$)", text)
    return match.group(1).strip() if match else None

# Load distractors
with open("model_distractors_re.json", "r", encoding="utf-8") as f:
    distractor_map = {
        (item["id"], item["ques"]): {
            "ground_truth": item["ground_truth"],
            "model_distractors": item["model_distractors"]
        }
        for item in json.load(f)
    }

# Load dataset
with open("../../Dataset/test.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

results = []

for sample in dataset:
    doc_id = sample["id"]
    caption = sample.get("caption", "")
    description = sample.get("description", "")
    table = sample.get("table", [])

    table_str = ""
    if table:
        header = " | ".join(table[0])
        divider = " | ".join(["---"] * len(table[0]))
        rows = [" | ".join(row) for row in table[1:]]
        table_str = "\n".join([header, divider] + rows)

    document = f"{caption}\n\n{description}\n\n{table_str}"

    for i, qa in enumerate(sample.get("qa", [])):
        question = qa["ques"]
        ground_truth = qa["ans"]
        tag = qa["tag"]
        qid = f"{doc_id}_q{i}"

        entry = distractor_map.get((qid, question), {"ground_truth": ground_truth, "model_distractors": []})
        distractors = entry["model_distractors"]

        attempts = 0
        max_attempts = 3
        content = ""
        parsed_answer = None

        while len(set(map(str, distractors))) < 3 and attempts < max_attempts:
            attempts += 1

            system_input = """You are a scientific assistant, you are supposed to answer the given question based on the provided scientific document context. You need to first think through the problem step by step. documenting each necessary step. Then you are required to conclude your response with the final answer in your last sentence as "Therefore, the answer is {final answer}". The final answer should be either a numeric value or a short textual phrase, directly inferred from the table."""

            user_input = f"""{document}

Question: {question}

Let's think step by step to answer the given question."""

            try:
                response = client.chat.completions.create(
                    model="gpt-4.1-nano",
                    max_tokens=512,
                    temperature=1.5,
                    messages=[
                        {"role": "system", "content": system_input},
                        {"role": "user", "content": user_input}
                    ]
                )
                content = response.choices[0].message.content.strip()
                parsed_answer = extract_answer(content)

                print(f"[{qid}] Attempt {attempts} - prediction: {parsed_answer}")

                if parsed_answer is None:
                    print(f"[{qid}] 파싱 실패 (content 미포함)")
                    continue

                if parsed_answer != ground_truth and parsed_answer not in distractors and parsed_answer != "EXECUTION_ERROR":
                    distractors.append(parsed_answer)

            except Exception as e:
                print(f"[{qid}] 처리 오류: {e}")
                break

        if attempts >= max_attempts and len(set(map(str, distractors))) < 3:
            print(f"[{qid}] 최대 시도 초과로 패스 (생성된 distractor {len(distractors)}개)")

        results.append({
            "id": qid,
            "question": question,
            "ground_truth": ground_truth,
            "raw_output": content,
            "prediction": parsed_answer,
        })

        distractor_map[(qid, question)] = {"ground_truth": ground_truth, "model_distractors": distractors}

        print(f"[{len(results)}] {qid} - 최종 distractors: {len(distractors)}개")

        if len(results) % 10 == 0:
            with open("temp_results.json", "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

            with open("temp_distractors.json", "w", encoding="utf-8") as f:
                json.dump([
                    {"id": id_, "ques": ques, "ground_truth": ground_truth, "model_distractors": dist}
                    for (id_, ques), dist in distractor_map.items()
                ], f, ensure_ascii=False, indent=2)

            print(f"[임시 저장] {len(results)}개 완료")


with open("wrong_for_CoT_re.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

distractor_list = [
    {
        "id": id_,
        "ques": ques,
        "ground_truth": entry["ground_truth"],
        "model_distractors": entry["model_distractors"]
    }
    for (id_, ques), entry in distractor_map.items()
]

with open("model_distractors_re.json", "w", encoding="utf-8") as f:
    json.dump(distractor_list, f, ensure_ascii=False, indent=2)

print("최종 저장 완료: wrong_for_CoT_re.json, model_distractors_re.json")