// 모든 페이지에 공통으로 적용되는 태그 관리 (aroundtool.com)
(function(){
  const head = document.head;

  const charsetEl = document.createElement('meta');
  charsetEl.charset = 'UTF-8';
  head.appendChild(charsetEl);

  const metaTags = [
    { name: 'naver-site-verification', content: '819ae10e3fae28782afbbbbc248f8423b816872b' },
    { name: 'google-adsense-account', content: 'ca-pub-7089972708901760' },
    { name: 'viewport', content: 'width=device-width, initial-scale=1.0' }
  ];

  metaTags.forEach(tag => {
    if (!head.querySelector('meta[name="' + tag.name + '"]')) {
      const el = document.createElement('meta');
      el.name = tag.name;
      el.content = tag.content;
      head.appendChild(el);
    }
  });

  // AdSense는 공통 헤더에서 한 번만 로드합니다.
  if (!head.querySelector('script[data-aroundtool-adsense]')) {
    const adsScript = document.createElement('script');
    adsScript.async = true;
    adsScript.dataset.aroundtoolAdsense = 'true';
    adsScript.src = 'https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-7089972708901760';
    adsScript.crossOrigin = 'anonymous';
    head.appendChild(adsScript);
  }

  // Google Analytics는 방문 분석을 위한 최소 설정만 사용합니다.
  const gaId = 'G-2LK65NYW74';
  if (!head.querySelector('script[data-aroundtool-ga]')) {
    const gaScript = document.createElement('script');
    gaScript.async = true;
    gaScript.dataset.aroundtoolGa = 'true';
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
  }

  const faviconPC = document.createElement('link');
  faviconPC.rel = 'icon';
  faviconPC.type = 'image/png';
  faviconPC.sizes = '32x32';
  faviconPC.href = '/favicon-32x32.png';
  head.appendChild(faviconPC);

  const faviconMobile = document.createElement('link');
  faviconMobile.rel = 'apple-touch-icon';
  faviconMobile.sizes = '180x180';
  faviconMobile.href = '/apple-touch-icon.png';
  head.appendChild(faviconMobile);
})();
