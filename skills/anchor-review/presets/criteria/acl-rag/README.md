# acl-rag 심사 기준 파일

- 생성일: 2026-11-12
- 대상: ACL 2027 목표, RAG·검색 문맥 선택·압축 분야
- 등급 정의: `presets/tiers.json`의 "ACL" 항목

## 파일
- `tier_target_ACL.md`: ACL 2027 (4 = 본회의, 3 = Findings)
- `tier_peer_EMNLP.md`: EMNLP 2027 (같은 척도, 강건성을 강조)
- `tier_lower_COLING.md`: COLING 2027 (4 = 채택, Findings 없음)

## 근거
결과가 알려진 같은 분야 논문을 묶음별로 분석한 4개 파일을 썼다.

| 묶음 | 편수 | 결과 |
|---|---|---|
| analysis_MAIN | 12 | ACL·EMNLP·NAACL 본회의 채택 |
| analysis_FINDINGS | 12 | Findings 채택 |
| analysis_COLING | 6 | COLING 2025 본회의 채택 |
| analysis_ARXIV-ONLY | 12 | arXiv 게시 후 14개월 이상 미게재 |

- 공식 규칙과 채택률은 `reference/arr_criteria.md`(접근일 2026-11-11)에서 가져왔다.
- COLING 채택률은 `tiers.json`의 note(COLING 2025 공식 front matter)에서 가져왔다.

기준 파일에는 논문 제목, ID, 저자, 시스템 이름이 없다. 특징과 편수만 적었다.

## 한계
- 묶음당 표본이 12편(COLING 6편)으로 작다.
- MAIN 묶음은 세 학회 본회의가 섞여 있어, ACL과 EMNLP의 차이는 CFP 문구에 근거한다.
- ARXIV-ONLY에는 제출하지 않은 논문이 있을 수 있다.
- 모든 대응은 상관 관찰이다.

## 갱신
이 파일들은 결과가 알려진 논문에서 만든 것이다. 다음 경우에는 새 분석으로 다시 만든다.
- 목표 학회나 등급 구성이 바뀔 때
- 분야(주제)가 바뀔 때
- 채택률이나 ARR 지침이 바뀔 때
