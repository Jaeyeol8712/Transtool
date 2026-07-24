// 모든 페이지에 공통으로 적용되는 태그 관리 (aroundtool.com)
(function(){
    const head = document.head;

    // 1. 공통 메타태그 추가 (문자셋, 네이버 소유확인, 애드센스, 반응형 뷰포트)
    const charsetEl = document.createElement('meta');
    charsetEl.charset = 'UTF-8';
    head.appendChild(charsetEl);

    const metaTags = [
        { name: 'naver-site-verification', content: '819ae10e3fae28782afbbbbc248f8423b816872b' },
        { name: 'google-adsense-account', content: 'ca-pub-7089972708901760' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }
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
