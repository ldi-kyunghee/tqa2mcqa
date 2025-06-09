#Short Answer QA to MCQA: LLM 평가 신뢰도 개선 프로젝트
프로젝트 소개
Short Answer QA to MCQA는 LLM(Large Language Model)의 Table 기반 질의응답(Table QA) 성능 평가에서 발생하는 정답 표현의 다양성 문제를 해결하기 위해, 기존 단답형 QA 데이터를 객관식(MCQA) 형식으로 전환하는 프로젝트입니다. 다양한 오답 생성 기법과 '모른다' 선택지 도입을 통해 LLM의 평가 신뢰도와 현실성을 높이는 것이 목표입니다.

목차
프로젝트 개요

데이터셋

오답(디스트랙터) 생성 방식

MCQA 데이터 구축 및 평가 방법

실험 결과

주요 결론 및 한계

참고 논문

프로젝트 개요
배경:
LLM 기반 Table QA 평가에서, 정답 표현이 다양해 실제 의미상 정답임에도 오답으로 처리되는 문제가 빈번하게 발생합니다. 이는 LLM의 실제 성능보다 낮은 평가로 이어집니다.

목표:
QA 데이터를 MCQA로 전환하여 정답 표현의 모호성을 줄이고, 평가 신뢰도를 높입니다. 다양한 오답 생성 방식과 '모른다' 선택지(5지선다형)를 실험하여 평가의 현실성과 신뢰성을 개선합니다.

데이터셋
SciTabQA
과학 논문에서 추출한 표(Table), 캡션, 설명이 결합된 하이브리드 데이터셋

QA 쌍: 199개

특징: 숫자/문자 혼합 정답, 다양한 테이블 구조, Table+Description 혼합 질문

TableBench
18개 분야, 4개 카테고리(사실 검증, 수치 추론, 데이터 분석, 시각화)로 구성된 대규모 Table QA 벤치마크 데이터셋

오답 생성 방식
Perturbation (수치형 오답)

정답이 숫자인 경우, random gaussian noise를 추가해 오답 생성

Hard Negative (약한 LLM 활용)

gpt-4.1-nano, gpt-3.5-turbo 등 약한 LLM의 답변을 오답으로 사용

다양한 temperature, top-p 조정 시도했으나 충분한 다양성 확보에 한계

Common Error Type (오류 유형 기반)

Table QA에서 자주 발생하는 오류 유형(wrong row/column reference, 문제 해석 오류 등) 기반 오답 생성

예시: 같은 열의 잘못된 행, 같은 행의 잘못된 열 등

MCQA 데이터 구축 및 평가 방법
MCQA 변환:
4지선다, 5지선다('I don't know' 포함) 객관식 문제로 변환

각 문제에 정답 및 3~4개의 오답 선택지 구성

5지선다에서는 "I don't know"를 E번에 고정

평가 방식:

Chain-of-Thought(CoT): 단계별 추론 과정을 명시적으로 기술

Program-of-Thought(PoT): 파이썬 코드 형태로 문제 풀이

주요 지표: Accuracy, F1 Score, Selective Accuracy(‘안다’고 판단한 문제 중 정답률)

실험 결과
주요 수치 (SciTabQA 기준, CoT/PoT)
평가 방식	QA F1	4-MCQA F1	5-MCQA(v1) F1	5-MCQA(v2) F1
CoT	0.558	0.561	0.552	0.590
PoT	0.515	0.589	0.597	0.587
평가 방식	QA Sel. Acc.	4-MCQA Sel. Acc.	5-MCQA(v1) Sel. Acc.	5-MCQA(v2) Sel. Acc.
CoT	36.18	39.38	42.04	48.25
PoT	34.67	41.71	51.82	52.68
MCQA 전환 시 F1 Score 및 Selective Accuracy가 전반적으로 향상

'모른다' 선택지(E고정) 도입(5-MCQA v2)에서 Selective Accuracy가 가장 높음

주요 결론 및 한계
MCQA 전환은 정답 표현의 모호성을 줄이고 평가 신뢰도를 높임

오답 생성 기법의 다양성 및 품질이 평가 신뢰도에 영향

'모른다' 선택지 도입 시, 모델이 불확실한 문제에서 추측(hallucination) 대신 회피 전략을 활용하여 평가의 현실성과 신뢰도를 높임

한계: 오답 생성 자동화, prompt 최적화, 다양한 도메인 확장 등 추가 연구 필요
