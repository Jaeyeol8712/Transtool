// 모든 페이지에 공통으로 적용되는 태그 관리 (aroundtool.com)
(function(){
  const head = document.head;
  // 1. 메타태그 추가 (네이버 서치어드바이저, 구글 애드센스)
  const metaTags = [
    { name: 'naver-site-verification', content: 'b49199b17146051daa9c8f8eba5053a31708444c' },
    { name: 'google-adsense-account', content: 'ca-pub-7089972708901760' }
  ];
  metaTags.forEach(tag => {
    const el = document.createElement('meta');
    el.name = tag.name;
    el.content = tag.content;
    head.appendChild(el);
  });
  // 2. 구글 애널리틱스(GA4) 적용
  const gaId = 'G-2LK65NYW74';
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
})();
