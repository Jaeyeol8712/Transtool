from preview import *
# 가이드
g='''<h2 class="q">영국 ETA란?</h2>
<p>비자 없이 영국에 가는 사람이 <b>출발 전에 받는 전자여행허가</b>예요. 비자는 아니고, 2026년 2월 25일부터 항공사가 탑승 전에 확인해요. 관광·가족 방문·출장으로 6개월 미만 머무는 한국인(아기 포함)은 받아야 하고, 영국 비자가 이미 있으면 필요 없어요.</p>
<div class="key"><p class="big">한 번 받으면 2년 동안 여러 번</p>
<div class="nums"><div><b>20</b><span>파운드</span></div><div><b>2년</b><span>유효</span></div><div><b>6개월</b><span>1회 최대 체류</span></div></div></div>
<h2 class="q">신청 방법</h2>
<div class="flow"><div><i></i>UK ETA<br>앱 설치</div><div><i></i>여권<br>칩 읽기</div><div><i></i>얼굴<br>사진</div><div><i></i>질문<br>답하기</div><div><i></i>20파운드<br>결제</div></div>
<p style="margin-top:10px!important">결과는 보통 <b>3영업일 안</b>에 이메일로 와요. 여권에 전자로 연결돼서 출력은 필요 없어요.</p>
<h2 class="q">쉽게 신청하는 법</h2>
<div class="tip"><p><b>공식 UK ETA 앱으로</b> — 여권 칩을 휴대폰으로 읽어 신청해요<br><b>출발 1주 전에</b> — 보통 3영업일 걸려 여유가 생겨요<br><b>대행 사이트는 피하기</b> — 빨라지지 않고 비용만 늘어요<br><b>여권 갱신 예정이면 새 여권으로</b> — 여권을 바꾸면 다시 신청해야 해요</p></div>
<h2 class="q">준비물</h2><div class="chips"><span>전자여권</span><span>스마트폰</span><span>해외결제 카드</span><span>이메일</span></div>
<h2 class="q">비용</h2>
<div class="rows"><div><b>수수료</b>20파운드 (2026.4.8부터, 이전 16파운드)</div><div><b>결제</b>신청할 때 카드로</div><div><b>대행</b>공식 수수료 외 추가 비용</div></div>
<details><summary>더 보기 · 유효기간 자세히·환승·출처</summary></details>'''+nxt(['환율 계산기','여권 유효기간 계산기','솅겐 90/180일'])+sim(['미국 ESTA 신청 방법','기내 액체 반입 규정','해외에서 여권 잃어버렸을 때'])
write('guide-uk-eta.html','_pv_guide.html',wrap('영국 ETA 신청 방법 — 앱 신청 순서, 이것만 보고 따라하세요','<span>가이드</span><span>2026.11.19 확인</span>',g,'가이드 예시'))
# 여행
t='''<div class="key"><p class="big">푸껫은 <em>11~4월 건기</em>에 가세요</p>
<div class="nums"><div><b>6.5시간</b><span>인천 직항(약)</span></div><div><b>90일</b><span>무비자</span></div><div><b>-2시간</b><span>시차</span></div></div>
<p class="s">입국 3일 전부터 TDAC(디지털 입국카드) 무료 작성</p></div>
<h2 class="q">✅ 4박 5일 코스</h2>
<div class="rows"><div><b>DAY 1</b>공항 → 빠통·까론 숙소</div><div><b>DAY 2</b>피피섬 투어</div><div><b>DAY 3</b>올드타운 → 빅붓다 → 프롬텝 곶 노을</div><div><b>DAY 4</b>해변 · 마사지 휴식</div><div><b>DAY 5</b>공항 출발</div></div>
<p class="yn" style="margin-top:8px!important">➕ 5박 6일이면 DAY 5에 팡아만·제임스본드섬 투어</p>
<h2 class="q">✅ 숙소는 어디에?</h2><div class="chips"><span>🌃 밤거리 → 빠통</span><span>🏖️ 조용히 → 까론·까따</span><span>🏛️ 구경 → 올드타운</span></div>
<div class="tip"><p>🌧️ <b>5~10월 우기</b>엔 파도로 섬 투어가 취소될 수 있어요<br>🚗 공항 → 빠통 차로 약 1시간</p></div>
<details><summary>더 보기 · 이동 시간표·입국 제도·출처</summary></details>'''+nxt(['호텔 총액 계산기','환율 계산기','무비자 마지막 날'])+sim(['🇹🇭 파타야 여행 코스','🇻🇳 달랏 여행 코스','🇵🇭 보라카이 여행 코스'])
write('travel-phuket.html','_pv_trip.html',wrap('푸껫 여행 코스 — 4박 5일 일정, 건기·입국 정리','<span>여행</span><span>2026.11.17 확인</span>',t,'여행 예시'))
# 맛집(시장)
m='''<div class="key"><p class="big">기장시장은 <em>미역·멸치·장어</em></p>
<div class="nums"><div><b>봄</b><span>미역·멸치장</span></div><div><b>가을</b><span>갈치장</span></div><div><b>사계절</b><span>건어물</span></div></div>
<p class="s">동해선 기장역에서 걸어서 · 가게 추천·후기 아님</p></div>
<h2 class="q">✅ 뭘 사고 먹을까?</h2><div class="chips"><span>🌿 미역·다시마</span><span>🐟 멸치</span><span>🐍 곰장어·붕장어</span><span>🦀 양념게장</span><span>🐠 생갈치</span></div>
<p class="yn" style="margin-top:8px!important">💰 보도 기준(2025) 양념게장 한 통 1만 원, 장어 회 한 팩 1만~1만 5천 원 선</p>
<h2 class="q">✅ 반나절 동선</h2>
<div class="flow" style="--n:3"><div><i>🛒</i>기장시장<br>장보기</div><div><i>⛪</i>죽성<br>드림세트장</div><div><i>🍲</i>대변항·해녀촌<br>전복죽</div></div>
<div class="tip"><p>⚖️ 건어물은 <b>무게 대비 가격</b>을 몇 집 비교<br>🧊 생물은 <b>아이스박스 포장</b> 부탁</p></div>
<details><summary>더 보기 · 멸치축제 일정·출처</summary></details>'''+nxt(['부산 여행','해운대 맛집','제철 음식·시장'])+sim(['🐟 해운대시장 먹거리','🦪 통영 중앙시장','🍊 서귀포 올레시장'])
write('season-gijang-market-food.html','_pv_market.html',wrap('부산 기장시장 먹거리 — 미역·멸치·곰장어, 철마다 장','<span>맛집</span><span>2026.11.17 확인</span>',m,'맛집 예시'))
# 계산기
c='''<div class="key"><p class="big">여권, <em>귀국일 + 6개월</em> 남았나요?</p>
<div class="nums"><div><b>6개월</b><span>동남아·중국·대만</span></div><div><b>3개월</b><span>솅겐 유럽</span></div><div><b>체류 중</b><span>일본·미국</span></div></div>
<p class="s">부족하면 항공사가 탑승을 거부할 수 있어요</p></div>
<h2 class="q">✅ 예시로 보면</h2>
<div class="ex">만료일 <b>2027.3.10</b>이면<br>6개월 기준 <b>2026.9.10까지</b> 돌아와야 해요</div>
<div class="tip"><p>🛂 재발급은 국내에서 보통 <b>근무일 8일 안팎</b><br>✈️ 경유지에서 공항 밖으로 나가면 그 나라 기준도 적용</p></div>
<details><summary>더 보기 · 계산 공식·나라별 기준표·출처</summary></details>
<details><summary>내 블로그에 이 계산기 넣기</summary></details>'''+nxt(['솅겐 90/180일','무비자 마지막 날','날짜 계산기'])+sim(['🛂 해외에서 여권 잃어버렸을 때','🇬🇧 영국 ETA 신청 방법','🇲🇾 말레이시아 MDAC 등록'])
write('passport_validity_calculator.html','_pv_calc.html','<div class="at-prose nt"><p class="lab">계산기 예시 — 계산기 아래 설명 부분, 미리보기</p>'+c+'</div>',keep_tool=True)
# 추천
r='''<p class="ad">이 글은 네이버 쇼핑 커넥트 활동의 일환으로 판매 발생 시 수수료를 받습니다.</p>
<img class="prod" src="/assets/shop/jmw-airjet-ultra-pro/product.jpg" alt="JMW 에어젯 울트라 PRO 드라이기">
<a class="btn" href="#">제품 가격 알아보기 >></a>
<div class="key"><p class="big"><em>JMW 드라이기</em> 에어젯 울트라 PRO</p>
<div class="nums"><div><b>1700W</b><span>소비전력</span></div><div><b>BLDC</b><span>터보 항공모터</span></div><div><b>전문가용</b><span>판매처 표기</span></div></div>
<p class="s">판매처 상품명 기준 · 직접 사용 후기 아님</p></div>
<p class="yn"><span class="m">잘 맞는 분</span> 머리숱이 많거나 길어 오래 말리는 분, 강한 바람을 원하는 분<br><span class="m">다시 생각할 분</span> 여행용 접이식·가벼운 무게가 1순위인 분</p>
<h2 class="q">✅ 결제 전 체크</h2><div class="chips"><span>⚡ 소비전력</span><span>⚖️ 무게</span><span>🧰 노즐·거치대</span><span>✅ KC 인증</span></div>
<div class="tip"><p>🔌 1700W라 멀티탭보다 <b>벽 콘센트</b>에 바로 꽂으세요<br>💰 가격은 <b>같은 모델명·구성끼리</b> 비교</p></div>
<details><summary>더 보기 · 일반 모터 vs BLDC·사양표·자주 묻는 질문</summary></details>
<a class="btn" href="#">제품 가격 알아보기 >></a>'''+sim(['🧊 삼성 비스포크 냉장고 4도어','📺 삼성 TV 50인치 비즈니스 TV','📱 갤럭시 S23 울트라 맥세이프 케이스'])
write('shop-jmw-airjet-ultra-pro.html' ,'_pv_shop.html',wrap('JMW 드라이기 에어젯 울트라 프로 가격','<span>추천</span><span>2026.11.19</span>',r,'추천 예시'))
