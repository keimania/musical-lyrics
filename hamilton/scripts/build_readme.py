import json

def build_readme():
    with open('data/song_skeletons.json', 'r', encoding='utf-8') as f:
        skeletons = json.load(f)

    readme = []
    readme.append("# 🌟 뮤지컬 <해밀턴(Hamilton)> 전 곡(46곡) 원본 가사 및 한국어 전곡 완역 대역집\n\n")
    readme.append("> **\"History has its eyes on you.\"**  \n")
    readme.append("> 역사는 당신을 지켜보고 있다.\n\n")
    readme.append("미국 브로드웨이 뮤지컬 역사를 새로 쓴 **린마누엘 미란다(Lin-Manuel Miranda)**의 불멸의 명작, 뮤지컬 **<해밀턴(Hamilton)>** 전 46곡(1막 23곡, 2막 23곡, 총 3,258행)의 브로드웨이 오리지널 영문 가사 전수 조사 및 한국어 완역 대역집입니다.\n\n")
    readme.append("---\n\n")

    readme.append("## 📌 주요 특징 및 문서 구성\n\n")
    readme.append("1. **행별 1:1 영한 대역 (Bilingual Line-by-Line)**: 3,250여 행에 달하는 원문 가사와 번역을 바로 맞비교할 수 있도록 배치하였습니다.\n")
    readme.append("2. **캐릭터별 보이스 및 힙합 라임 완벽 구현**: 90년대 황금기 힙합(노토리어스 B.I.G., 라킴, 에미넴 등)의 오마주와 펀치라인, 라임 구조, 18세기 미국 독립전쟁과 건국기의 역사적 사료(연방주의자 보고서, 내각 논쟁, 결투 규칙)를 고증하여 번역하였습니다.\n")
    readme.append("3. **개별 곡별 상세 문서 (`act1/`, `act2/`)**: 각 넘버마다 곡의 극적 배경(시놉시스), 등장인물, 주요 감상 포인트 및 주석을 수록하였습니다.\n")
    readme.append("4. **통합 완본 문서 ([hamilton_complete.md](./hamilton_complete.md))**: 46곡 전체를 단 하나의 마크다운 문서로 엮어 전문 검색 및 연속 감상이 가능합니다.\n")
    readme.append("5. **인터랙티브 웹 뷰어 ([index.html](./index.html))**: 브라우저에서 편리하게 넘버를 검색하고, 영한 대역/한글 전용/영문 전용 뷰 모드를 전환할 수 있는 웹 뷰어를 제공합니다.\n\n")
    readme.append("---\n\n")

    readme.append("## 👥 브로드웨이 오리지널 1인 2역 (Dual Roles) 및 주요 인물 가이드\n\n")
    readme.append("| 인물 (한국어) | Character (English) | 브로드웨이 초연 캐스트 | 1막 역할 (Act I) | 2막 역할 (Act II) |\n")
    readme.append("|:---|:---|:---|:---|:---|\n")
    readme.append("| **알렉산더 해밀턴** | Alexander Hamilton | Lin-Manuel Miranda | 초대 재무장관, 대륙군 중령, 독립전쟁 영웅 | 연방주의자 보고서 집필, 첫 국가 금융체계 수립 |\n")
    readme.append("| **아론 버** | Aaron Burr | Leslie Odom Jr. | 해밀턴의 평생의 라이벌, 신중한 기회주의자 | 뉴욕주 상원의원, 제3대 부통령, 결투의 당사자 |\n")
    readme.append("| **조지 워싱턴** | George Washington | Christopher Jackson | 대륙군 총사령관, 해밀턴의 멘토이자 후원자 | 미국의 초대 대통령, 평화적 정권 이양의 선구자 |\n")
    readme.append("| **일라이자 스카일러** | Eliza Schuyler | Phillipa Soo | 해밀턴의 아내, 스카일러 가문의 둘째 딸 | 남편 사후 50년간 그의 업적과 고아원을 지킨 자 |\n")
    readme.append("| **안젤리카 스카일러** | Angelica Schuyler | Renée Elise Goldsberry | 스카일러 가문의 장녀, 지성과 기품을 겸비한 여성 | 해밀턴과 정신적 교감을 나누며 일라이자를 지킨 누이 |\n")
    readme.append("| **라파예트 / 제퍼슨** | Lafayette / Jefferson | Daveed Diggs | 프랑스 귀족 출신 독립전쟁 혁명군 참모 | 제3대 대통령, 해밀턴의 최대 정적 (민주공화당) |\n")
    readme.append("| **멀리건 / 매디슨** | Mulligan / Madison | Okieriete Onaodowan | 재단사 도제 출신 독립군 스파이 | '헌법의 아버지', 제4대 대통령, 제퍼슨의 동맹 |\n")
    readme.append("| **로런스 / 필립** | Laurens / Philip | Anthony Ramos | 해밀턴의 절친, 흑인 노예해방대대 추진자 | 해밀턴의 장남, 아버지를 지키려다 결투로 요절 |\n")
    readme.append("| **페기 / 마리아** | Peggy / Maria | Jasmine Cephas Jones | 스카일러 가문의 셋째 딸 | 해밀턴을 스캔들에 빠뜨린 마리아 레이놀즈 |\n")
    readme.append("| **조지 3세** | King George III | Jonathan Groff | 대영제국의 국왕, 식민지를 향한 집착과 풍자 | 미국의 혼란을 조소하는 브리티시 팝의 상징 |\n\n")
    readme.append("---\n\n")

    readme.append("## 📑 전 46곡 수록 목록 (Full Tracklist)\n\n")
    readme.append("### 제1막 (Act I: 1776 ~ 1789) - 청춘, 혁명, 그리고 새로운 국가의 시작\n\n")
    readme.append("| 번호 | 영문 제목 | 한국어 제목 | 주요 등장인물 | 바로가기 |\n")
    readme.append("|:---:|:---|:---|:---|:---:|\n")
    for i in range(1, 24):
        s = skeletons[str(i)]
        chars_kr = ", ".join(s['characters_kr'][:3]) + (" 등" if len(s['characters_kr']) > 3 else "")
        readme.append(f"| {i:02d} | **{s['title']}** | {s['title_kr']} | {chars_kr} | [문서 열기]({s['file_rel_path']}) |\n")

    readme.append("\n### 제2막 (Act II: 1789 ~ 1854) - 내각 논쟁, 비극적 스캔들, 그리고 불멸의 유산\n\n")
    readme.append("| 번호 | 영문 제목 | 한국어 제목 | 주요 등장인물 | 바로가기 |\n")
    readme.append("|:---:|:---|:---|:---|:---:|\n")
    for i in range(24, 47):
        s = skeletons[str(i)]
        chars_kr = ", ".join(s['characters_kr'][:3]) + (" 등" if len(s['characters_kr']) > 3 else "")
        readme.append(f"| {i:02d} | **{s['title']}** | {s['title_kr']} | {chars_kr} | [문서 열기]({s['file_rel_path']}) |\n")

    readme.append("\n---\n\n")
    readme.append("## 🔍 무결성 검증 안내\n\n")
    readme.append("전 46곡 3,258행 전량에 대한 가사 누락 및 대역 매칭 무결성은 아래 명령어로 언제든지 재검증할 수 있습니다:\n\n")
    readme.append("```bash\n")
    readme.append("python3 scripts/verify_lyrics.py\n")
    readme.append("```\n\n")
    readme.append("---\n\n")
    readme.append("*본 자료는 학술 연구 및 감상 목적의 비상업적 대역·주석 해설집입니다.*  \n")
    readme.append("*Music & Lyrics by Lin-Manuel Miranda © Hamilton Uptown LLC.*\n")

    with open('README.md', 'w', encoding='utf-8') as rf:
        rf.writelines(readme)

    print("Successfully built README.md!")

if __name__ == '__main__':
    build_readme()
