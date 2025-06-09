import json
import re
from openai import OpenAI

client = OpenAI(
    api_key=''
)

with open('../MCQ5_choices_wrong_reference2.json', 'r', encoding="utf-8") as file:
    mcq_dataset = json.load(file)

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


def extract_choice(text):
    text = text.strip().replace("\u00a0", " ").replace("\xa0", " ")

    patterns = [
        r"the answer is\s*\(?([A-E])\)?",
        r"answer\s*[:\-]?\s*\(?([A-E])\)?",
        r"correct option is\s*\(?([A-E])\)?",
        r"selected option is\s*\(?([A-E])\)?",
        r"option\s*\(?([A-E])\)?\s*is correct",
        r"\(\s*([A-E])\s*\)",  
    ]

    matches = []
    for pat in patterns:
        found = re.findall(pat, text, re.IGNORECASE)
        if found:
            matches.extend(found)

    if matches:
        return matches[-1].upper()  

    return None


results = []

for data in mcq_dataset:
    id = data["id"]
    question = data["question"]
    answer = data["answer"]
    choice_A = data["mcq_choices"]["A"]
    choice_B = data["mcq_choices"]["B"]
    choice_C = data["mcq_choices"]["C"]
    choice_D = data["mcq_choices"]["D"]
    choice_E = data["mcq_choices"]["E"]
    document = get_document(documents, id, question)
    
    system_input = """You are a scientific assistant. You are supposed to answer the following multiple-choice question based on the provided scientific document context. 

First, carefully read the document and think through the problem step by step, documenting each necessary step in your reasoning. After the reasoning process, conclude your response with the correct answer choice. 

Your final sentence must be in the format: \"Therefore, the answer is (X).\", where X is A, B, C, D or E."""

    user_input = f"""{document}

Question: {question}

Choices:
(A) {choice_A}
(B) {choice_B}
(C) {choice_C}
(D) {choice_D}
(E) {choice_E}

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

        #match = re.search(r"(?:Therefore, the answer is|Among them,|Answer:|correct answer is)\s*(?:[0-9.]+\s*)?([A-E])\b", content)
        #selected_choice = match.group(1) if match else None
        selected_choice = extract_choice(content)

        results.append({
            "id": id,
            "question": question,
            "answer" : answer,
            "response": content,
            "prediction": selected_choice
        })
        print(f"ID: {id}\nSelected: {selected_choice}\n")

    except Exception as e:
        results.append({"id": id, "question": question, "answer": answer, "error": str(e)})
        print(f"Error processing ID {id}: {e}")


with open('mcqa5_wrong_reference_results_cot2.json', 'w', encoding="utf-8") as outfile:
    json.dump(results, outfile, ensure_ascii=False, indent=2)

    