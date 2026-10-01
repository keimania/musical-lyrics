import json
import os

def build_bttf_readme():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skeletons_path = os.path.join(base_dir, 'data', 'bttf_skeletons.json')
    with open(skeletons_path, 'r', encoding='utf-8') as f:
        skeletons = json.load(f)

    readme = []
    readme.append("# ⚡ 뮤지컬 <백 투 더 퓨처(Back to the Future: The Musical)> 전 26곡 공식 원본 가사 및 한국어 전곡 완역 대역집\n\n")
    readme.append("> **\"Your future is whatever you make it, so make it a good one!\"**  \n")
    readme.append("> 당신의 미래는 스스로 만들어가는 것입니다, 그러니 멋진 미래를 만드세요!\n\n")
    readme.append("로버트 저메키스 감독과 밥 게일 각본의 1985년 전설적인 SF 영화를 원작으로, 런던 웨스트엔드 올리비에상(Laurence Olivier Awards) 최우수 신작 뮤지컬상을 수상하고 브로드웨이 무대를 뒤흔든 블록버스터 SF 록 뮤지컬, **<백 투 더 퓨처: 더 뮤지컬(Back to the Future: The Musical)>** 전 26개 트랙(1막 13곡, 2막 13곡, 총 1,060행)의 공식 영문 가사 전수 조사 및 한국어 완역 대역집입니다.\n\n")
    readme.append("---\n\n")

    readme.append("## 📌 주요 특징 및 문서 구성\n\n")
    readme.append("1. **행별 1:1 영한 대역 (Bilingual Line-by-Line)**: 1,060행에 달하는 원문 가사와 대사를 즉시 대조할 수 있도록 완벽하게 매칭하여 배치하였습니다.\n")
    readme.append("2. **영화 오리지널 음악과 브로드웨이 록/쇼튠의 완벽한 융합**: 영화의 음악감독 앨런 실베스트리(Alan Silvestri)와 팝 거장 글렌 발라드(Glen Ballard)가 새로 쓴 신곡들과 함께, 전설적인 명곡 휴이 루이스 앤 더 뉴스의 **\"The Power of Love\"**, **\"Back in Time\"**, 척 베리의 **\"Johnny B. Goode\"**, 펭귄스의 **\"Earth Angel\"**을 전곡 수록하였습니다.\n")
    readme.append("3. **개별 넘버별 상세 문서 (`act1/`, `act2/`)**: 26곡 전편에 대한 곡 배경 시놉시스, 1985년 vs 1955년 문화 차이, 50년대 두왑과 80년대 신스록, 타임 패러독스 사료 고증 주석 수록.\n")
    readme.append("4. **통합 완본 문서 ([bttf_complete.md](./bttf_complete.md))**: 26곡 전체를 한 번에 연속 통독 및 검색할 수 있는 단일 마크다운 문서.\n")
    readme.append("5. **인터랙티브 웹 뷰어 ([index.html](./index.html))**: 드로리안 계기판 & 80년대 레트로 SF 테마, 막별 필터, 실시간 검색, 영한 대역/한글/영문 뷰 모드 지원.\n\n")
    readme.append("---\n\n")

    readme.append("## 👥 주요 등장인물 및 캐릭터 가이드\n\n")
    readme.append("| 인물 (한국어) | Character (English) | 특징 및 음악적 스타일 | 대표 넘버 |\n")
    readme.append("|:---|:---|:---|:---|\n")
    readme.append("| **마티 맥플라이** | Marty McFly | 1985년 힐밸리의 평범하지만 록스타를 꿈꾸는 고교생. 80년대 신스록/팝록 보컬 | [It's Only a Matter of Time](./act1/02_its_only_a_matter_of_time.md), [Johnny B. Goode](./act2/21_johnny_b_goode.md) |\n")
    readme.append("| **에밋 \"닥\" 브라운 박사** | Doc Emmett Brown | 괴짜 천재 과학자이자 드로리안 타임머신의 발명가. 브로드웨이 정통 쇼튠 & 스윙 | [It Works](./act1/06_it_works.md), [For the Dreamers](./act2/16_for_the_dreamers.md) |\n")
    readme.append("| **조지 맥플라이** | George McFly | 마티의 소심하고 유약한 아버지. SF 소설을 좋아하며 50년대 두왑 & 팝 보컬 | [My Myopia](./act1/10_my_myopia.md), [Put Your Mind to It](./act2/15_put_your_mind_to_it.md) |\n")
    readme.append("| **로레인 베인스** | Lorraine Baines | 마티의 1955년 10대 어머니. 당돌하고 로맨스를 갈망하는 50년대 벨팅 보컬 | [Pretty Baby](./act1/11_pretty_baby.md), [Something About That Boy](./act1/13_something_about_that_boy.md) |\n")
    readme.append("| **비프 태넌** | Biff Tannen | 조지를 괴롭히는 마을의 불량배 골목대장. 거친 록 & 블루스 보컬 | [Teach Him a Lesson](./act2/17_teach_him_a_lesson.md) |\n")
    readme.append("| **골디 윌슨** | Goldie Wilson | 1955년 카페 청소부에서 1985년 힐밸리 시장으로 자수성가하는 인물. 모타운 소울 | [Gotta Start Somewhere](./act1/09_gotta_start_somewhere.md) |\n")
    readme.append("| **제니퍼 파커** | Jennifer Parker | 마티의 다정하고 응원해주는 여자친구. 서정적인 팝 듀엣 | [Wherever We're Going](./act1/04_wherever_were_going.md) |\n")
    readme.append("| **마빈 베리** | Marvin Berry | '해저의 환상' 무도회 밴드 리더. 정통 50년대 R&B 및 블루스 보컬 | [Deep Divin'](./act2/19_deep_divin.md), [Earth Angel](./act2/20_earth_angel.md) |\n\n")
    readme.append("---\n\n")

    readme.append("## 📑 전 26곡 수록 목록 (Full Tracklist)\n\n")
    readme.append("### 제1막 (Act I: 1985년에서 1955년으로)\n\n")
    readme.append("| 트랙 | 영문 제목 | 한국어 제목 | 주요 가창자 | 바로가기 |\n")
    readme.append("|:---:|:---|:---|:---|:---:|\n")
    for i in range(1, 14):
        s = skeletons[str(i)]
        readme.append(f"| {i:02d} | **{s['title']}** | {s['title_kr']} | {s['stanzas'][0]['speaker_kr']} | [문서 열기]({s['file_rel_path']}) |\n")

    readme.append("\n### 제2막 (Act II: 과거를 바로잡고 미래로 돌아가라!)\n\n")
    readme.append("| 트랙 | 영문 제목 | 한국어 제목 | 주요 가창자 | 바로가기 |\n")
    readme.append("|:---:|:---|:---|:---|:---:|\n")
    for i in range(14, 27):
        s = skeletons[str(i)]
        readme.append(f"| {i:02d} | **{s['title']}** | {s['title_kr']} | {s['stanzas'][0]['speaker_kr']} | [문서 열기]({s['file_rel_path']}) |\n")

    readme.append("\n---\n\n")
    readme.append("## 🔍 무결성 검증 안내\n\n")
    readme.append("전 26개 트랙 1,060행에 대한 가사 누락 및 대역 매칭 무결성은 아래 명령어로 언제든지 재검증할 수 있습니다:\n\n")
    readme.append("```bash\n")
    readme.append("python3 back_to_the_future/scripts/verify_bttf.py\n")
    readme.append("```\n\n")
    readme.append("---\n\n")
    readme.append("*본 자료는 학술 연구 및 감상 목적의 비상업적 대역·주석 해설집입니다.*  \n")
    readme.append("*Music & Lyrics by Alan Silvestri, Glen Ballard, Huey Lewis, Chuck Berry © Universal Theatrical Group.*\n")

    readme_path = os.path.join(base_dir, 'README.md')
    with open(readme_path, 'w', encoding='utf-8') as rf:
        rf.writelines(readme)

    print("Successfully built back_to_the_future/README.md!")

if __name__ == '__main__':
    build_bttf_readme()
