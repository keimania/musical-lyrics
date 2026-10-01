import json

def build_six_readme():
    with open('six/data/six_skeletons.json', 'r', encoding='utf-8') as f:
        skeletons = json.load(f)

    readme = []
    readme.append("# 👑 뮤지컬 <식스(SIX: The Musical)> 전 11곡 공식 원본 가사 및 한국어 전곡 완역 대역집\n\n")
    readme.append("> **\"Divorced, beheaded, died, divorced, beheaded, survived.\"**  \n")
    readme.append("> \"이혼, 참수, 사망, 이혼, 참수, 생존.\"  \n")
    readme.append("> **\"Historemix: We're one of a kind, no category, too many years lost in his-story!\"**  \n")
    readme.append("> \"역사를 새로 써라! 우린 분류 불가한 유일무이한 존재, 그의 역사(his-story) 속에서 너무 많은 세월을 잃었어!\"\n\n")
    readme.append("영국 튜더 왕조 헨리 8세의 여섯 왕비가 팝 콘서트 디바로 부활하여 펼치는 전 세계적인 메가 히트 뮤지컬, **<식스(SIX)>** 전 11곡(오프닝, 6인의 솔로, 테크노 클럽 앙상블, 피날레 및 커튼콜 메가식스, 총 986행)의 브로드웨이/웨스트엔드 오리지널 영문 가사 전수 조사 및 한국어 완역 대역집입니다.\n\n")
    readme.append("---\n\n")

    readme.append("## 📌 주요 특징 및 문서 구성\n\n")
    readme.append("1. **행별 1:1 영한 대역 (Bilingual Line-by-Line)**: 980여 행에 달하는 팝 앤섬 원문 가사와 라임, 펀치라인, 현대 팝스타의 플로우를 살린 고품질 한국어 대역.\n")
    readme.append("2. **6인의 퀸(Queens) 팝 디바 모티브 및 역사적 고증**: 비욘세, 에이브릴 라빈, 아델, 니키 미나즈, 아리아나 그란데, 알리샤 키스 등 팝스타의 음악 스타일과 16세기 튜더 왕조의 실제 역사적 사료(이혼 소송, 레위기 논쟁, 불린의 처형, 홀바인의 초상화 사기극, 하워드의 그루밍 성착취, 파의 저작권)를 밀도 높게 주석화.\n")
    readme.append("3. **개별 넘버별 상세 문서 (`songs/`)**: 11곡 전편에 대한 곡 배경, 인물 프로필, 주석 및 가사 대역 수록.\n")
    readme.append("4. **통합 완본 문서 ([six_complete.md](./six_complete.md))**: 11곡 전체를 한눈에 통독 및 검색할 수 있는 단일 마크다운 문서.\n")
    readme.append("5. **인터랙티브 웹 뷰어 ([index.html](./index.html))**: 네온 팝 콘서트 테마, 퀸별 상징색 뱃지, 영한 대역/한글 전용/영문 전용 뷰 모드 지원.\n\n")
    readme.append("---\n\n")

    readme.append("## 👑 6인의 왕비(The Six Queens) 심층 프로필 및 팝스타 매핑\n\n")
    readme.append("| 번호 | 왕비 (Queen) | 역사적 결말 | 상징색 | 모티브 팝 디바 (Inspirations) | 대표 솔로 넘버 |\n")
    readme.append("|:---:|:---|:---:|:---:|:---|:---|\n")
    readme.append("| 1 | **아라곤의 캐서린**<br>(Catherine of Aragon) | **이혼**<br>(Divorced) | 🟡 골드<br>(Gold) | **비욘세 (Beyoncé)**, 제니퍼 로페즈, 샤키라 | [03. No Way](./songs/03_no_way.md) |\n")
    readme.append("| 2 | **앤 불린**<br>(Anne Boleyn) | **참수**<br>(Beheaded) | 🟢 그린<br>(Green) | **에이브릴 라빈**, 릴리 알렌, 마일리 사이러스 | [04. Don't Lose Ur Head](./songs/04_dont_lose_ur_head.md) |\n")
    readme.append("| 3 | **제인 시모어**<br>(Jane Seymour) | **사망**<br>(Died) | ⚪ 화이트/실버<br>(White) | **아델 (Adele)**, 시아 (Sia), 셀린 디옹 | [05. Heart of Stone](./songs/05_heart_of_stone.md) |\n")
    readme.append("| 4 | **클레페의 앤**<br>(Anna of Cleves) | **이혼**<br>(Divorced) | 🔴 레드<br>(Red) | **니키 미나즈 (Nicki Minaj)**, 리한나 (Rihanna) | [07. Get Down](./songs/07_get_down.md) |\n")
    readme.append("| 5 | **캐서린 하워드**<br>(Katherine Howard) | **참수**<br>(Beheaded) | 🟣 핑크<br>(Pink) | **아리아나 그란데**, 브리트니 스피어스 | [08. All You Wanna Do](./songs/08_all_you_wanna_do.md) |\n")
    readme.append("| 6 | **캐서린 파**<br>(Catherine Parr) | **생존**<br>(Survived) | 🔵 블루<br>(Blue) | **알리샤 키스 (Alicia Keys)**, 에밀리 산데 | [09. I Don't Need Your Love](./songs/09_i_dont_need_your_love.md) |\n\n")
    readme.append("---\n\n")

    readme.append("## 📑 전 11곡 수록 목록 (Full Tracklist)\n\n")
    readme.append("| 트랙 | 영문 제목 | 한국어 제목 | 주요 가창자 | 바로가기 |\n")
    readme.append("|:---:|:---|:---|:---|:---:|\n")
    for i in range(1, 12):
        s = skeletons[str(i)]
        readme.append(f"| {i:02d} | **{s['title']}** | {s['title_kr']} | {s['stanzas'][0]['speaker_kr']} | [문서 열기]({s['file_rel_path']}) |\n")

    readme.append("\n---\n\n")
    readme.append("## 🔍 무결성 검증 안내\n\n")
    readme.append("전 11곡 986행에 대한 가사 누락 및 대역 매칭 무결성은 아래 명령어로 언제든지 재검증할 수 있습니다:\n\n")
    readme.append("```bash\n")
    readme.append("python3 six/scripts/verify_six.py\n")
    readme.append("```\n\n")
    readme.append("---\n\n")
    readme.append("*본 자료는 학술 연구 및 감상 목적의 비상업적 대역·주석 해설집입니다.*  \n")
    readme.append("*Music & Lyrics by Toby Marlow & Lucy Moss © Ex-Wives Ltd.*\n")

    with open('six/README.md', 'w', encoding='utf-8') as rf:
        rf.writelines(readme)

    print("Successfully built six/README.md!")

if __name__ == '__main__':
    build_six_readme()
