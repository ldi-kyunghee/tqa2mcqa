import json
import re
from openai import OpenAI

client = OpenAI(
    api_key='sk-cNbZsZKsbfChfSKMUj66LdWoYqTm2A_FZPojkPQV7rT3BlbkFJIPk6gOBzIfG1yGjNUa1N2-HiNaM2ihDYb72evtpUQA'
)


with open("../../Dataset/test.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

# 기존 distractor 결과 불러오기
try:
    with open("wrong_row_distractors.json", "r", encoding="utf-8") as f:
        existing_results = {item["id"]: item for item in json.load(f)}
except FileNotFoundError:
    existing_results = {}

results = []

# 무조건 distractor 재생성할 대상
selected_pairs = {
    ("1911.03905v1_q0", "What is the disfluency for original training data?")
}

def clean_json_string(text):
    if text.startswith("```json") or text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    text = re.sub(r"//.*", "", text)
    return text.strip()

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

        parsed_answer = []

        if (qid, question) in selected_pairs:
            print(f"[{qid}] distractor 재생성 중...")

            system_input = """You are a distractor generator for generating plausible but incorrect answer choices for table-based QA problems

Your task is to generate 3 plausible but incorrect answer choices based on a wrong row reference — referencing or selecting a value from the correct column but a wrong row. Use the question and table context to guide your choices.

Return your result in the following JSON format:
{
  "id": "example_id",
  "ques": "example question",
  "ground_truth": "correct answer",
  "wrong_row_distractors": [
    "distractor 1",
    "distractor 2",
    "distractor 3"
  ]
}
Return only valid JSON. It must be directly parsable using json.loads() in Python. Do not include markdown, code fences, or comments."""

            user_input = f"""Table and Caption: {document}

Question: {question}

Ground truth: {ground_truth}"""

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    max_tokens=512,
                    temperature = 1.2,
                    messages=[
                        {"role": "system", "content": system_input},
                        {"role": "user", "content": user_input}
                    ]
                )
                content = response.choices[0].message.content or ""
                cleaned = clean_json_string(content.strip())
                parsed_json = json.loads(cleaned)
                parsed_answer = parsed_json.get("wrong_row_distractors", [])
            except Exception as e:
                print(f"[{qid}] 생성 오류: {e}")
                parsed_answer = []

        else:
            # 기존 결과가 있으면 유지
            parsed_answer = existing_results.get(qid, {}).get("wrong_row_distractors", [])

        results.append({
            "id": qid,
            "question": question,
            "ground_truth": ground_truth,
            "wrong_row_distractors": parsed_answer,
        })

with open("wrong_row_distractors.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("저장 완료: wrong_row_distractors.json")
