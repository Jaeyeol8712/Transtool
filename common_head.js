// 모든 페이지에 공통으로 들어가는 애널리틱스 및 메타태그 관리
(function() {
 const head = document.head;

 // 1. 구글 서치콘솔 / 네이버 서치어드바이저 인증태그 (코드 입력 부분)
 const metaTags = [
 { name: 'google-site-verification', content: 'google-site-verification=PomvSVjqf2y59zGMvY-9VAVV4vf07mF1uXXZ9L3cTHQ' },
 { name: 'naver-site-verification', content: '여기에_네이버_인증코드_입력' }
 ];
 
 metaTags.forEach(tag => {
 const el = document.createElement('meta');
 el.name = tag.name;
 el.content = tag.content;
 head.appendChild(el);
 });

 // 2. 구글 애널리틱스 (GA4)
 const gaId = 'G-XXXXXXXXXX'; // GA4 측정 ID로 변경
 const gaScript = document.createElement('script');
 gaScript.async = true;
 gaScript.src = `https://www.googletagmanager.com/gtag/js?id=${gaId}`;
 head.appendChild(gaScript);

 const gaInit = document.createElement('script');
 gaInit.innerHTML = `
 window.dataLayer = window.dataLayer || [];
 function gtag(){dataLayer.push(arguments);}
 gtag('js', new Date());
 gtag('config', '${gaId}');
 `;
 head.appendChild(gaInit);

 // 3. 구글 애드센스 자동광고 스크립트
 const adClientId = 'ca-pub-XXXXXXXXXXXXXXXX'; // 애드센스 펍ID로 변경
 const adScript = document.createElement('script');
 adScript.async = true;
 adScript.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${adClientId}`;
 adScript.crossOrigin = 'anonymous';
 head.appendChild(adScript);
})();
