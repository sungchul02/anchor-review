# *ACL(ACL/EMNLP/NAACL, ARR) 모의 심사 루브릭 근거 자료

- 접근일: 2026-11-11 (모든 URL 공통)
- 표기: **[공식]** = ARR/ACL/학회 공식 문서, **[경험]** = 공식 보고서 속 통계나 논문·블로그·커뮤니티의 경험적 경향. 인용문은 원문 짧은 구절이다.
- 주의: 일부 인용은 웹 페이지 요약 도구를 거쳐 받은 것이다. 최종 문구를 쓰기 전에 원문 페이지에서 한 번 더 대조하는 편이 안전하다.

---

## 1. 현재 ARR 심사자 지침과 심사 양식 [공식]

출처:
- ARR Review Form: https://aclrollingreview.org/reviewform
- ARR Reviewer Guidelines: https://aclrollingreview.org/reviewerguidelines (페이지에 "updated for the October 2026 review cycle"라고 적혀 있음)

### 1.1 심사 양식 필드 (순서대로)
1. Paper Summary: "Describe what this paper is about."
2. Summary of Strengths
3. Summary of Weaknesses: 이 논문을 다른 강한 제출물보다 낮게 둘 우려 사항을 묻는다. 결과·논증의 정확성, 영향 범위가 좁음, 서술 불명확 같은 예를 들고, 저자가 하나씩 답할 수 있도록 번호를 붙이라고 한다.
4. Comments/Suggestions/Typos
5. Reviewer Confidence (1–5)
6. Soundness (1–5, 0.5 단위)
7. Excitement (1–5, 0.5 단위)
8. Overall Assessment (1–5, 0.5 단위)
9. Best paper justification (수상 수준 점수를 줄 때 필수)
10. Limitations and Societal Impact
11. Ethical Concerns / Needs Ethics Review
12. Reproducibility (1–5)
13. Datasets (1–5): 5 Enabling, 4 Useful, 3 Potentially useful, 2 Documentary, 1 No usable datasets submitted
14. Software (1–5): 같은 척도
15. Knowledge of / educated guess at author identity (1–5), 선택 사항으로 저자 추정 메모(저자에게는 보이지 않음)

### 1.2 Soundness
도입 질문: "Does it clearly state scientific claims and provide adequate support for them?"
| 점수 | 원문 |
|---|---|
| 5 | "Excellent: This study is one of the most thorough I have seen, given its type." |
| 4 | "Strong: This study provides sufficient support for all of its claims." "Some extra experiments could be nice, but not essential." |
| 3 | "Acceptable: This study provides sufficient support for its main claims." "Some minor points may need extra support or details." |
| 2 | "Poor: Some of the main claims are not sufficiently supported. There are major technical/methodological problems." |
| 1 | "Major Issues: This study is not yet sufficiently thorough to warrant publication or is not relevant to ACL." |

지침 I3: soundness 점수는 "must be justified by the text of the review". 큰 결함을 짚지 않은 채 낮은 점수를 주면 심사평을 고쳐야 한다.

### 1.3 Excitement
도입: "Excitement is _subjective_, and does not necessarily follow what is popular in the field."
| 점수 | 원문 |
|---|---|
| 5 | "Highly Exciting: I would recommend this paper to others and/or attend its presentation in a conference." |
| 4 | "Exciting: I would mention this paper to others and/or make an effort to attend its presentation in a conference." |
| 3 | "Interesting: I might mention some points of this paper to others and/or attend its presentation in a conference if there's time." |
| 2 | "Potentially Interesting: this paper does not resonate with me, but it might with others in the *ACL community." |
| 1 | "Not Exciting: this paper does not resonate with me, and I don't think it would with others in the *ACL community" |

지침상 excitement는 soundness와 직교하며, 명시적 이유를 붙이지 않아도 된다.

### 1.4 Overall Assessment (핵심)
도입: "If this paper was committed to an *ACL conference, do you believe it should be accepted?"
- "Outstanding papers should be either fascinating, controversial, surprising, impressive, or potentially field-changing."
- "Main vs Findings papers: the main criteria for Findings are soundness and reproducibility."
- "Conference recommendations may also consider novelty, impact and other factors."

| 점수 | 라벨 | 원문 정의 |
|---|---|---|
| 5 | Consider for Award | "I think this paper could be considered for an outstanding paper award at an *ACL conference" |
| 4.5 | Borderline Award | 라벨만 있음 |
| 4 | Conference | "I think this paper could be accepted to an *ACL conference." |
| 3.5 | Borderline Conference | 라벨만 있음 |
| 3 | Findings | "I think this paper could be accepted to the Findings of the ACL." |
| 2.5 | Borderline Findings | 라벨만 있음 |
| 2 | Resubmit next cycle | "I think this paper needs substantial revisions that can be completed by the next ARR cycle." |
| 1.5 | Resubmit after next cycle | "...substantial revisions that cannot be completed by the next ARR cycle." |
| 1 | Do not resubmit | "This paper has to be fully redone, or it is not relevant to the *ACL community (e.g. it is in no way related to computational processing of language)." |

정리하면 **2 이하는 사실상 '이번 사이클 불가(재제출)'**이고, 3은 Findings, 4는 본회의다. 심사자 지침 5절: "All papers recommended for Findings and main conferences are expected to be sufficiently sound and reproducible, but you may consider a paper worthy of the main conference even if you personally are not excited about it."

### 1.5 Reviewer Confidence
- 5: 매우 확신. 논문을 꼼꼼히 읽었고 관련 연구도 잘 앎
- 4: 상당히 확신. 핵심 사항을 확인함
- 3: 꽤 확신. 수식이나 실험 설계 같은 세부는 꼼꼼히 확인하지 않음
- 2: 평가를 방어할 의향은 있으나 세부를 놓쳤을 수 있음
- 1: "Not my area, or paper is very hard to understand."

### 1.6 Reproducibility
5 Easily reproducible / 4 Mostly / 3 With difficulty / 2 Hard pressed / 1 Not reproducible. 지침 M2: 결과가 실제로 재현되는지가 아니라, 다시 돌릴 수 있을 만큼 세부와 코드가 제공됐는지를 본다.

### 1.7 "피해야 할 심사 휴리스틱" H1–H17 (지침 Task 3 §3)
| ID | 휴리스틱 | ARR의 처리 지시 (원문 구절) |
|---|---|---|
| H1 | 결과가 놀랍지 않다 | "Many findings seem obvious in retrospect, but this does not mean that the community is already aware of them" |
| H2 | 기대와 반대다 | 확증 편향일 수 있음 |
| H3 | 새롭지 않다 | "you need to provide a reference". 재현·재구현·분석은 "in scope of the CFP and deserve a fair hearing." |
| H4 | 선례가 없다 | 새로운 연구일수록 불리해질 수 있음 |
| H5 | SOTA를 못 넘었다 | "SOTA results are neither necessary nor sufficient for a scientific contribution." "If the authors do not claim that their contribution achieves SOTA status, the lack thereof is not an issue." |
| H6 | 부정적 결과다 | "If something systematically does not work where it could be expected to, the community does need to know about it." |
| H7 | 너무 단순하다 | "The goal is to solve the problem, not to solve it in a complex way." "Simpler solutions are in fact preferable" |
| H8 | 내가 선호하는 방법론이 아니다 | NLP는 다양한 기여 유형을 받는다 |
| H9 | 주제가 너무 좁다 | 좁은 분야에서도 의미 있는 기여가 가능 |
| H10 | 영어 외 언어만 다뤘다 | 영어만 다룬 연구도 같은 문제를 가짐 |
| H11 | 영어 표현 오류 | 이해 가능하면 충분 |
| H12 | 참고문헌 누락 | 마감 "3+ months before" 출판된 연구만 필수. 프리프린트는 제안 사항 |
| H13 | 추가 실험 X도 해야 한다 | "a paper only needs to present sufficient evidence for the claim that the authors are making." 나머지는 "nice-to-have"로 reasons to reject가 아니라 suggestions에 둔다 |
| H14 | 폐쇄형 모델과 비교하라 | 주장과 직접 관련될 때만 합당 |
| H15 | 저자는 X를 했어야 했다 | 그 선택 때문에 연구 질문에 답할 수 없거나 프레이밍이 오도할 때만 유효 |
| H16 | 한계 = 약점 | "A good review should not just take the limitations and list them as weaknesses or reasons to reject." 한계가 연구를 무효화한다면 그 논증을 해야 함 |
| H17 | 인용 수 | 타당성의 지표가 아님 |

### 1.8 정당한 감점 사유: NLP 논문의 흔한 문제 (지침 Task 3 §4, R/M 목록)
- R1 분석 문제: "presenting the 'best' results out of an unknown number of trials", p-hacking, 튜닝이 덜 된 베이스라인
- R2 주장 범위: "a sample that does not represent the population about which the claim is made"
- R3 추측을 결론처럼 씀: 근거가 없으면 "clearly marked as conjecture/speculation"이어야 함
- R4 "Misleading or inappropriate framing, overclaiming": 벤치마크 결과를 검증 없이 더 넓은 구성 개념으로 일반화
- R5 "Inappropriate or missing statistical significance assessment": 주요 결과에 오차 막대, 신뢰구간, 검정을 붙이고 효과 크기도 권장
- M1 LLM-as-judge의 신뢰성을 해당 맥락에서 검증했는가
- M2 재현 가능성(세부와 코드)
- M4 모델과 벤치마크 선택의 동기, 주장과의 적합성
- M5 가정을 명시하고 증명을 완결했는가

### 1.9 2024–2026 변경 사항 (보이는 범위)
- 심사자 지침 changelog: 2024-05-15 익명성 / **2024-10-21 대개편(Anna Rogers 외; NLP 문제 목록 R/M 신설, H14 추가)** / 2025-05-01 인센티브 정책 / 2025-10-22 sustainable reviewing / 2026-05 secondary reviewer 기능 / 2026-10 사이클용 갱신. 출처: https://aclrollingreview.org/reviewerguidelines
- AC 지침: **2025년 2월 meta-review 점수 척도를 심사자 Overall 척도에 맞춤**(같은 9단계 라벨). 출처: https://aclrollingreview.org/acguidelines
- Soundness/Excitement 2축 점수는 ACL 2023에서 처음 도입됐다. "neither score is functionally equivalent to the traditional 'overall recommendation' score"(https://2023.aclweb.org/blog/overall-recommendation/). 현재 ARR 양식은 Soundness·Excitement·Overall을 함께 쓴다.
- 2026년 10월부터 sustainable reviewing policy가 적용된다. "Submissions will now be capped to reviewer capacity", 단일 저자 최대 20편(제1저자 5편) 제출 상한. 출처: https://aclrollingreview.org/authors
- 생성형 AI: 심사평 초안을 생성형 AI로 쓰는 것은 금지되고, 가벼운 문장 보조만 허용된다. AI 심사자를 노린 숨은 프롬프트가 있으면 데스크 리젝트. 출처: 심사자 지침
- 미확인: 9단계 Overall 라벨(Conference/Findings/Resubmit…)이 처음 도입된 정확한 시점은 공식 문서에서 찾지 못했다.

---

## 2. 메타리뷰(AC) 지침과 채택 결정 과정

### 2.1 AC 지침 [공식] — https://aclrollingreview.org/acguidelines
- 메타리뷰 필드: 점수(심사자와 같은 9단계, 본문으로 뒷받침해야 함), "Summary of reasons to publish", "Summary of suggested revisions", 저자가 신고한 review issue 처리 체크, 심사평 무시(disregard) 필드, 윤리·수상 추천.
- 집계: ACs "do not have to simply average across reviewer scores". soundness는 심사자들이 일치하면 "mostly follow the soundness assessment of the reviewers". 새 비판은 심사자들이 결정적인 것을 놓쳤다고 "strongly believe"할 때만, AC 의견으로 표시해 제기한다.
- 잘못된 휴리스틱 처리: "this is a resource paper", "results are not sota" 같은 논거, 한 줄 심사평, 무례하거나 막연한 비판을 점검하고 심사자에게 먼저 제기한다. 심각하면 "This review does not meet the ARR quality standards, and will be disregarded in the assessment".
- **본회의 vs Findings**: 둘 다 "expected to be sound and reproducible". Findings는 어떤 면에서 돋보이고 다른 문제가 없는 좋은 논문을 고른다. 본회의는 excitement, novelty, impact 등으로 사례별로 구분하며, **excitement는 필요조건도 충분조건도 아니다**. 효율 개선이나 고품질 자원처럼 덜 "흥미로운" 논문도 본회의에 갈 수 있다. 판단은 해당 학회 제출 풀 대비 상대적이다.

### 2.2 SAC/PC 결정 [공식]
- SAC 지침 (https://aclrollingreview.org/sacguidelines): 최종 결정은 각 학회 PC가 한다. SAC는 리뷰, 메타리뷰, 저자 응답, issue report를 보고 추천한다. 점수와 인기만 보지 말고 "encouraging a diversity of perspectives, methodology, reporting of negative results"를 고려하라고 한다. 경계선 논문은 심사 기간 중 프리프린트를 공개하지 않은 쪽이 유리하다. **공개된 점수 컷오프는 없다.**
- ARR authors 페이지 (https://aclrollingreview.org/authors): "a 'high' AC recommendation does not guarantee acceptance." 결정은 커밋된 논문 풀, PC의 전문성과 편집 선호도에 달려 있다. 메타리뷰 1.5점이면 다음 사이클 재제출이 막히고, 1점이면 영구히 막힌다(https://aclrollingreview.org/cfp).
- ACL 2026 PC: SAC 추천을 바탕으로 결정하되 "with a view to obtaining a balanced program and prioritizing work at a mature state of development" (ACL 2026 front matter, https://aclanthology.org/2026.acl-long.0.pdf).
- ACL 2021 FAQ (https://2021.aclweb.org/blog/faq-decision/): P1 본회의 / P2 Findings / P3 reject. "Going-to-finding decisions are made by SACs and PCs, not by reviewers/ACs." 당시 목표 채택률은 본회의 21–24%, Findings 약 15%.
- COPR 보고서 (2025-01, https://aclweb.org/adminwiki/images/9/9e/COPR-5-cycle-report-to-publish.pdf): "about 35-40% of the papers in major conferences are accepted to either the main conference or Findings". 저자들이 "receive a high score in their ARR meta review, but end up getting their paper rejected"하는 불만이 있어, ARR이 Findings 결정을 직접 내리는 실험을 제안했다. 실제 시행 여부는 확인하지 못했다.

### 2.3 채택률
| 학회 | 제출(분모) | 본회의 | Findings | 출처 |
|---|---|---|---|---|
| NAACL 2025 | 10월 ARR 중 NAACL 희망 3,099편(추정) | 약 22% (719편) | 약 15% (477편) | 공식 front matter https://aclanthology.org/2025.naacl-long.0.pdf |
| ACL 2025 | 고유 제출 8,360편 | 20.3% (1,699편) | 16.7% (1,392편) | 공식 PC 보고서 https://www.aclweb.org/adminwiki/index.php/2025Q3_Reports:_Program_Chairs |
| EMNLP 2025 | 8,174편 | 22.16% (1,811편) | 17.34% (1,417편) | 공식 front matter https://aclanthology.org/2025.emnlp-main.0.pdf |
| ACL 2026 | 고유 제출 12,148편 | 18.9% (2,296편) | 17.8% (2,163편) | 공식 front matter https://aclanthology.org/2026.acl-long.0.pdf |
| EMNLP 2026 | 약 17,669편 (비공식) | 약 15% (2,700편 이상) | 약 14% (2,500편 이상), 총 5,252편 | **비공식 2차 보도**: https://digg.com/tech/5xgwr5hu, https://kr.linkedin.com/in/bcj1210/en. 공식 PC 보고서는 확인하지 못함 |

정리: 본회의 약 19–22%(2026년에는 15–19%로 하락), Findings 약 15–18%, 합계 약 35–40%. 제출이 급증하면서 2026년 본회의 비율이 낮아졌다.

### 2.4 점수와 결정의 관계 [경험]
- ACL 2023 보고서 (https://2023.aclweb.org/blog/review-report/): 결정에 미치는 영향은 점수 < AC < SAC 순이다. 할당량은 SAC만 적용하므로 "possible for papers to be rejected with high scores and positive meta-reviews". 세 심사자 간 Krippendorff α는 약 0.3이고, Soundness가 Excitement보다 일치도가 높다.
- ARR-Dv2 (AACL 2026, https://aclanthology.org/2026.aacl-long.17/): EMNLP 2024와 NAACL 2025의 메타리뷰 점수는 "primarily at 4, with some at 3"이다. 심사자 Overall 평균은 EMNLP 2024 약 3.23, NAACL 2025 약 3.25. Overall과 Soundness의 상관은 r=0.78 (NAACL, EMNLP)이고, 신뢰도와 점수의 상관은 0에 가깝다. 메타리뷰 2점인데도 채택된 사례가 있다(EMNLP 2024: 본회의 2편, Findings 9편). 단, 이 데이터는 저자가 기부한 논문만 담고 있어 채택 논문 쪽으로 편향돼 있다.
- 커뮤니티 통념 (비공식, https://cspaper.org/post/50): 심사자 OA 평균 3.5 이상이면 본회의 가능, 3.0 이상이면 Findings 경계. 메타 3.5를 받고도 reject된 사례와 Findings가 된 사례가 모두 보고된다. 일화로만 취급할 것.
- SAC 경험담 (Antonis Anastasopoulos, EMNLP 2023 SAC, https://gist.github.com/antonisa/2158dee79179c7c49304ef353887bfa0): SAC는 논문을 Accept-Main / Borderline-Main-Findings / Accept-Findings / Borderline-Findings-Reject / Reject로 순위화한다. 점수로 정렬해 이상치를 재검토하고, 점수는 "a grain of salt"로 본다. 쉬운 사례는 심사자와 AC가 일치하는 경우이고 나머지는 경계선이다.

---

## 3. 학회 목표와 CFP [공식]

### 3.1 ACL 2026 — https://2026.aclweb.org/calls/main_conference_papers/
- "substantial, original, and unpublished research". 다양한 프로그램을 지향한다.
- 기여 유형: "negative findings", 서베이, "the creation of a new resource", 입장(position), "novel linguistic insights derived using existing computational techniques", 재현 연구("fail to reproduce" 포함).
- 특별 주제: Explainability of NLP Models (124편 제출, 본회의 29편, Findings 27편).
- Findings: 본회의에 선정되지 않은 제출은 "automatically considered for publication in the Findings".
- 효율은 기여 유형이 아니라 주제(LLM Efficiency)로 등장한다.

### 3.2 EMNLP 2026 — https://2026.emnlp.org/calls/main_conference_papers/
- "substantial, original, and unpublished research on empirical methods for Natural Language Processing".
- 기여 유형: "may contribute negative findings", 서베이, 자원, 입장, 언어학적 통찰, "reproduce (or fail to reproduce) previous results".
- 특별 주제: New Missions for NLP Research. 진보는 "can no longer be measured only by fractional improvements in benchmark scores". 평가에서 "trustworthiness, robustness, and longitudinal behavior"를 요구하고 "clear claims, strong evidence, and actionable insights"를 요구한다.

### 3.3 NAACL 2027 (최신) — https://2027.naacl.org/calls/main_conference_papers/
- "a clear and substantive contribution to the field of NLP". 방법론, 실증, 이론, 언어학, 자원 연구와 "evaluation methods and reproducibility" 연구를 받는다. 서베이와 입장 논문은 "a substantial original synthesis, perspective, insight, or argument"가 있어야 한다.
- 특별 주제: Language as a Medium for Agentic Communication. "The use of multiple agents alone is not sufficient for relevance to the theme."
- ARR 2026년 10월 사이클을 COLING 2027과 공유한다. CFP 본문에는 Findings 언급이 없다.

### 3.4 ARR 공통 CFP — https://aclrollingreview.org/cfp
- 기여 유형 체크 항목: low-resource, **low-compute/efficiency**, data resources, data analysis, model analysis & interpretability, NLP engineering experiments, software/pre-trained models, position, **reproduction studies**, surveys, theory.
- 부정적 결과: "Both positive and negative results for experimental studies are welcome". 저자는 그 결과가 왜 중요한지 정당화해야 한다(예: 재현 불가, "right for the wrong reasons", 동기가 좋았지만 작동하지 않은 아이디어).
- Short paper: "a small, focused contribution", "a short paper is not a shortened long paper". (비)재현 보고, 부정적 결과, 의견, 응용 사례가 예로 들어진다.
- Limitations 섹션 필수: "Papers without a limitations section will be desk rejected." Responsible NLP checklist도 필수다.

### 3.5 Findings의 정의
- [공식] 현재 문서상 정의: Findings 추천의 "main criteria ... are soundness and reproducibility"(심사 양식). AC 지침은 어떤 면에서 돋보이고 다른 문제가 없는 좋은 논문이라고 설명한다.
- [공식, 2021] ACL 2021 FAQ: "solid work but cannot make it to the main conference due to the low acceptance rate" (https://2021.aclweb.org/blog/faq-decision/).
- [공식, 2020] Findings of EMNLP 2020 서문: 본회의에 오르지 못했지만 출판 가치가 있는 강한 연구, ACL 학회들의 "companion" 출판물. 당시 PC는 특정 하위 커뮤니티에 관심 있는 논문이 Findings에 맞는다고 했고, 이에 대한 비판이 있었다(Yoav Artzi 공개서한, https://yoavartzi.com/2020/04/26/findings-letter.html). 원 PC 공지문은 확인하지 못했다.
- [경험] Findings는 발표 슬롯이 없고 "not considered a top-tier publication by many" (Anastasopoulos gist).

---

## 4. 채택을 예측하는 요인에 대한 경험적 분석 [경험, 공식 규칙과 분리]

| 출처 | 핵심 내용 |
|---|---|
| ACL 2023 PC 보고서 (Rogers, Karpinska, Boyd-Graber, Okazaki), https://2023.aclweb.org/blog/review-report/ , https://aclanthology.org/2023.acl-long.911 | 영향 순서는 점수 < AC < SAC. 심사자 간 α≈0.3. 저자가 가장 많이 신고한 이슈는 "too simple", "not SOTA" 같은 'lazy thinking' 휴리스틱(신고 이슈의 약 24.3%, LazyReview 논문 인용). 저자는 점수가 낮고 거절 이유가 긴 심사평을 주로 신고한다. 비주류 기여 유형은 "NLP engineering"보다 채택률이 높았다(수치는 블로그에 없음). 프리프린트가 있는 논문은 Soundness·Excitement 점수가 유의하게 높았다. 신뢰도 점수는 실제 경험을 반영하지 않았다. |
| ARR-Dv2 (Tonja et al., AACL 2026), https://aclanthology.org/2026.aacl-long.17/ | Overall과 Soundness의 상관 0.78–0.80. 신뢰도와는 거의 무상관(NAACL, EMNLP). 점수는 대부분 3–4에 몰리고 5는 드물다. 메타 점수는 주로 4. Overall 3은 경계선, 1–2는 명확한 reject로 해석. 심사평이 가장 자주 다루는 측면은 Methodology, Result, Data/Task, Presentation이며, NLPeer ARR-22 이후 거의 변하지 않았다. |
| NLPeer (Dycke et al., ACL 2023) | ARR 2022 심사평 데이터셋. LazyReview와 ARR-Dv2의 기반 데이터로 쓰였다. |
| LazyReview (Purkayastha et al., ACL 2025), https://arxiv.org/abs/2504.11042 | NLPeer ARR-22 심사평 500개 구간에 전문가 주석. 가장 흔한 lazy thinking은 "Extra Experiments"(정당화 없는 추가 실험 요구), 그다음이 "Not Enough Novelty"와 "Language Errors". zero-shot LLM은 이를 잘 탐지하지 못한다. |
| ACL 2023 Acceptance Recommendations 블로그, https://2023.aclweb.org/blog/overall-recommendation/ | "non-scientifically-sound papers should not be published anywhere". soundness가 높고 excitement가 낮으면 어딘가에는 채택돼야 하고, soundness가 낮고 일부 심사자만 흥미를 보이면 더 발전시켜야 한다. |
| COPR 2025-01 보고서 | 본회의와 Findings를 합친 채택률 35–40%. 메타 점수가 높아도 reject되는 괴리가 존재한다. |
| Antonis Anastasopoulos SAC gist (2023) | 5단계 순위화. 점수 정렬로 이상치를 찾는다. 주니어 심사자일수록 엄격한 경향이 있다. 경계선 판정은 사실상 확률적이다. |
| 커뮤니티 (cspaper, Reddit) | OA 평균 3.5 이상이면 본회의 가능권, 3.0이면 Findings 경계, 메타 3.0이면 Findings 약 40%. 일화 수준이며 신뢰도가 낮다. |

---

## 5. 부정적 결과, "방법이 이기지 못하는" 결과, 분석 논문의 처리 [공식 + 경험]

- [공식] H5: "SOTA results are neither necessary nor sufficient for a scientific contribution." "An engineering paper could also offer improvements on other dimensions"(효율, 공정성 등). **저자가 SOTA를 주장하지 않았다면 SOTA가 아니라는 점은 문제가 되지 않는다.**
- [공식] H6: "The bias towards publishing only positive results is a known problem". "If something systematically does not work where it could be expected to, the community does need to know about it."
- [공식] H3·1절: 재현, 재구현, 체계적 분석은 "should be encouraged" / "in scope of the CFP and deserve a fair hearing".
- [공식] 1절, 주장 범위: 논문은 "a proof of concept, an interesting finding, a convincing point, a negative result"를 제시할 수 있다. 심사는 저자가 실제로 한 주장의 범위 안에서 한다.
- [공식] ARR CFP: 긍정·부정 결과를 모두 환영하되, 저자가 그 부정적 결과의 중요성을 정당화해야 한다. Short paper의 대표 유형이 negative result와 (non-)reproduction이다.
- [공식] AC 지침: "results are not sota", "this is a resource paper"는 AC가 걸러야 할 문제 논거다. 덜 흥미로운 효율 개선이나 자원 논문도 본회의 자격이 있다.
- [공식] SAC 지침: "reporting of negative results"를 다양성 차원에서 고려한다.
- [공식] EMNLP 2026 주제: 진보를 "fractional improvements in benchmark scores"만으로 잴 수 없다.
- [경험] ACL 2023: 비주류 기여 유형의 채택률이 엔지니어링 논문보다 높았다. 그래도 "not SOTA"와 "too simple"은 여전히 가장 많이 신고되는 심사 문제다. 실제 심사자들은 이 휴리스틱을 자주 쓰므로, 모의 심사에서도 나올 가능성은 있다. 다만 공식 규칙상 유효한 감점 사유는 아니다.
- 한계: 부정적 결과 논문의 실제 채택률을 따로 집계한 공식 통계는 찾지 못했다.

---

## 6. Rubric implications (모의 심사 루브릭 항목)

표기: **[R]** 공식 규칙, **[T]** 경험적 경향. 각 항목은 예/아니오나 점수로 점검할 수 있게 썼다.

### A. 점수 산정 규칙
1. **[R]** Overall은 9단계 라벨로 낸다: 5 Award / 4.5 / **4 Conference** / 3.5 / **3 Findings** / 2.5 / **2 Resubmit next cycle** / 1.5 / 1 Do not resubmit. 점수마다 라벨 문장이 붙는다. (reviewform)
2. **[R]** Findings 판정(3)의 최소 조건은 soundness와 reproducibility가 충분한가이다. 새로움과 영향은 본회의(4)를 판단할 때 추가로 본다. (reviewform, reviewerguidelines §5, acguidelines)
3. **[R]** Soundness 3 = 주요 주장이 충분히 뒷받침됨, 4 = 모든 주장이 뒷받침됨, 2 = 일부 주요 주장이 근거 부족이거나 큰 방법론 문제가 있음. Soundness 2 이하이면 Findings 이상을 추천하지 않는다. (reviewform, ACL 2023 블로그)
4. **[R]** Soundness 점수는 심사평 본문의 구체적 결함으로 뒷받침되어야 한다. 결함을 적지 않고 낮은 점수를 주면 무효다. (지침 I3)
5. **[R]** Excitement는 주관적이고 soundness와 독립적이다. Excitement가 낮다는 이유만으로 Overall을 2 이하로 내리지 않는다. 본회의에서도 excitement는 "neither necessary nor sufficient"이다. (reviewform, acguidelines)
6. **[R]** Confidence 1–5를 함께 낸다. (reviewform) **[T]** 실제 신뢰도와 점수는 거의 무상관이니 보정 변수로 쓰지 않는다. (ARR-Dv2, ACL 2023)
7. **[R]** Reproducibility, Datasets, Software 점수를 따로 매긴다. (reviewform)

### B. 유효한 감점 사유 (soundness 점검표)
8. **[R]** R1: 최고 시도만 보고했는가, 베이스라인 튜닝이 부족한가.
9. **[R]** R2: 표본이 주장 대상 모집단을 대표하는가(주장 범위와 데이터 범위가 맞는가).
10. **[R]** R3: 추측을 결론처럼 썼는가.
11. **[R]** R4: 과장 주장(overclaiming)이나 벤치마크에서 구성 개념으로 과도하게 일반화했는가.
12. **[R]** R5: 주요 결과에 유의성 검정, 신뢰구간, 오차 막대가 있는가.
13. **[R]** M1: LLM 평가자를 쓴다면 해당 맥락에서 신뢰성을 검증했는가.
14. **[R]** M4: 모델과 벤치마크 선택의 동기가 주장과 맞는가.
15. **[R]** 필수 Limitations 섹션이 있는가(없으면 데스크 리젝트). (ARR CFP)

### C. 금지된 감점 사유 (모의 심사자가 이를 근거로 점수를 내리면 무효)
16. **[R]** H5: 저자가 SOTA를 주장하지 않았는데 "SOTA가 아니다"를 이유로 감점.
17. **[R]** H6: 부정적 결과라는 이유로 감점. 체계적으로 작동하지 않는다는 결과는 그 자체로 기여다.
18. **[R]** H7: 방법이 단순하다는 이유로 감점.
19. **[R]** H3: 구체적 선행 문헌 없이 "새롭지 않다"고 감점. 분석이나 재현 논문에 새로움 부족을 적용.
20. **[R]** H13: 주장을 뒷받침하는 데 필요하지 않은 추가 실험 요구를 reasons to reject에 넣음. suggestions로 옮긴다.
21. **[R]** H16: 저자가 Limitations에 적은 항목을 그대로 약점으로 나열. 무효화 논증이 있을 때만 허용.
22. **[R]** H14: 주장과 무관하게 폐쇄형 모델 비교를 요구.
23. **[R]** H12: 마감 3개월 이내 문헌이나 프리프린트 누락을 약점으로 지적.
24. **[R]** H1, H9: "놀랍지 않다", "주제가 좁다"를 근거로 감점.
25. **[R]** AC 지침: "this is a resource paper", "results are not sota"는 AC가 걸러내야 할 논거다.

### D. 본회의(4)와 Findings(3)를 가르는 질문
26. **[R]** sound하고 재현 가능하며 다른 문제가 없으면 3 이상이다. (acguidelines, reviewform)
27. **[R]** 본회의 4는 novelty, impact, excitement 등 "other factors"로 사례별로 판단하고, 해당 학회 제출 풀 대비 상대적으로 본다. 효율 개선이나 고품질 자원도 4가 될 수 있다. (acguidelines)
28. **[R]** 학회 CFP 목표와의 적합성: EMNLP 2026은 벤치마크 소폭 향상 이상의 증거(신뢰성, 강건성)를 요구하고, NAACL 2027은 "clear and substantive contribution"을 요구한다. 해당 학회의 특별 주제에 부합하면 가점 요인이다. (각 CFP)
29. **[T]** PC는 "mature state of development"인 연구를 우선한다(ACL 2026). 미완성 인상을 주는 논문은 본회의에서 밀리기 쉽다.
30. **[T]** 채택 분포를 보정 기준으로 삼는다. 본회의 약 15–22%, Findings 약 14–18%, 합계 약 35–40%. 모의 심사자가 무작위 제출물의 절반 이상에 4를 준다면 지나치게 관대한 것이다. (PC 보고서, COPR)
31. **[T]** 심사자 Overall 평균은 약 3.2이고 3–4에 몰린다. 메타 점수는 주로 4다(커밋된 논문 기준). 5는 드물다. (ARR-Dv2)
32. **[T]** Overall은 Soundness와 r≈0.78로 강하게 연동된다. 모의 심사자의 Overall과 Soundness가 크게 어긋나면(예: S 4, O 2) 근거를 다시 점검한다. (ARR-Dv2)
33. **[T]** 커뮤니티 통념: 심사자 OA 평균 3.5 이상이면 본회의 가능권, 3.0 근처면 Findings 경계. 메타 점수가 높아도 SAC 할당량 때문에 reject될 수 있으므로 점수에서 결과로 가는 확률을 단정하지 않는다. (cspaper, ACL 2023, COPR. 일화 수준)
34. **[T]** 실제 심사자는 "Extra Experiments", "Not Enough Novelty", "too simple", "not SOTA"를 자주 쓴다(LazyReview, ACL 2023). 실전 대비용 '적대적 심사자' 모드에서는 이런 비판이 나올 가능성을 예고하되, 공식 점수 산정에서는 C항 규칙으로 배제한다.

### E. 부정적 결과와 분석 논문 전용 점검
35. **[R]** 저자가 실제로 한 주장의 범위로 평가한다. SOTA를 주장하지 않았다면 승패표는 감점 근거가 아니다. (H5, §1)
36. **[R]** 부정적이거나 혼재된 결과라면, 기대할 만한 상황에서 체계적으로 작동하지 않는다는 점과 그 이유가 근거와 함께 제시됐는지 본다(soundness 문제). 결과의 방향 자체는 평가 대상이 아니다. (H6, ARR CFP)
37. **[R]** 분석 논문이라면 R2(표본 대표성), R4(일반화 범위), R5(유의성)가 핵심 soundness 축이다. 새로움은 "구체적 선행 문헌 제시" 원칙으로만 다룬다. (H3, R목록)
38. **[R]** 효율, 공정성 같은 다른 차원의 개선이 주장된다면 그 차원으로 평가한다. (H5, ARR CFP 기여 유형)
39. **[T]** 비주류 기여 유형은 엔지니어링 논문보다 채택률이 높았다(ACL 2023). 이것이 부정적 결과 논문에 유리하다는 직접 통계는 없다.

---

## 부록: 주요 URL 목록 (접근일 2026-11-11)
- https://aclrollingreview.org/reviewform
- https://aclrollingreview.org/reviewerguidelines
- https://aclrollingreview.org/acguidelines
- https://aclrollingreview.org/sacguidelines
- https://aclrollingreview.org/authors
- https://aclrollingreview.org/cfp
- https://aclrollingreview.org/may26-cycle-letter
- https://2026.aclweb.org/calls/main_conference_papers/
- https://2026.emnlp.org/calls/main_conference_papers/
- https://2027.naacl.org/calls/main_conference_papers/
- https://www.aclweb.org/adminwiki/index.php/2025Q3_Reports:_Program_Chairs
- https://aclanthology.org/2025.emnlp-main.0.pdf
- https://aclanthology.org/2025.naacl-long.0.pdf
- https://aclanthology.org/2026.acl-long.0.pdf
- https://2021.aclweb.org/blog/faq-decision/
- https://2023.aclweb.org/blog/review-report/
- https://2023.aclweb.org/blog/overall-recommendation/
- https://aclweb.org/adminwiki/images/9/9e/COPR-5-cycle-report-to-publish.pdf
- https://aclanthology.org/2026.aacl-long.17/
- https://arxiv.org/abs/2504.11042
- https://gist.github.com/antonisa/2158dee79179c7c49304ef353887bfa0
- https://yoavartzi.com/2020/04/26/findings-letter.html
- (비공식) https://cspaper.org/post/50 , https://digg.com/tech/5xgwr5hu
