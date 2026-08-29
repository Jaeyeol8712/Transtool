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

  // 답변엔진(AEO)·생성엔진(GEO)이 스니펫과 이미지를 충분히 인용할 수 있도록 명시적으로 허용
  if (!head.querySelector('meta[name="robots"]')) {
    const robotsEl = document.createElement('meta');
    robotsEl.name = 'robots';
    robotsEl.content = 'index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1';
    head.appendChild(robotsEl);
  }

  // Open Graph / Twitter Card / 구조화 데이터는 <title>, <meta description>, canonical이
  // 파싱된 뒤에 채워야 하므로 DOMContentLoaded 시점에 실행합니다.
  function enhanceSEO(){
    const siteName = '어라운드툴';
    const siteUrl = 'https://www.aroundtool.com/';
    const defaultImage = 'https://www.aroundtool.com/apple-touch-icon.png';

    const titleEl = document.querySelector('title');
    const descEl = document.querySelector('meta[name="description"]');
    const canonicalEl = document.querySelector('link[rel="canonical"]');
    const pageTitle = titleEl ? titleEl.textContent.trim() : siteName;
    const pageDesc = descEl ? (descEl.getAttribute('content') || '') : '';
    const pageUrl = canonicalEl ? canonicalEl.getAttribute('href') : location.href;
    const isHome = pageUrl === siteUrl || pageUrl === siteUrl.replace(/\/$/, '');

    const ogTags = [
      ['og:site_name', siteName],
      ['og:locale', 'ko_KR'],
      ['og:type', 'website'],
      ['og:title', pageTitle],
      ['og:description', pageDesc],
      ['og:url', pageUrl],
      ['og:image', defaultImage]
    ];
    ogTags.forEach(function(pair){
      var prop = pair[0], content = pair[1];
      if (content && !head.querySelector('meta[property="' + prop + '"]')) {
        var el = document.createElement('meta');
        el.setAttribute('property', prop);
        el.setAttribute('content', content);
        head.appendChild(el);
      }
    });

    const twitterTags = [
      ['twitter:card', 'summary'],
      ['twitter:title', pageTitle],
      ['twitter:description', pageDesc],
      ['twitter:image', defaultImage]
    ];
    twitterTags.forEach(function(pair){
      var name = pair[0], content = pair[1];
      if (content && !head.querySelector('meta[name="' + name + '"]')) {
        var el = document.createElement('meta');
        el.name = name;
        el.content = content;
        head.appendChild(el);
      }
    });

    // 계산기/도구 페이지 전용: 상단 브레드크럼이 있는 페이지에서만
    // BreadcrumbList + WebApplication 구조화 데이터를 자동 생성합니다.
    const crumbNav = document.querySelector('.site-breadcrumb');
    if (crumbNav && !isHome) {
      const parts = Array.prototype.slice.call(crumbNav.querySelectorAll('a, span'))
        .map(function(el){ return el.textContent.replace(/^\s*🏠\s*/, '').trim(); })
        .filter(function(t){ return t && t !== '/'; });

      if (parts.length >= 2 && !document.getElementById('ld-breadcrumb')) {
        const breadcrumbList = {
          '@context': 'https://schema.org',
          '@type': 'BreadcrumbList',
          itemListElement: parts.map(function(name, i){
            const item = { '@type': 'ListItem', position: i + 1, name: name };
            if (i === 0) item.item = siteUrl;
            else if (i === parts.length - 1) item.item = pageUrl;
            return item;
          })
        };
        const bcScript = document.createElement('script');
        bcScript.type = 'application/ld+json';
        bcScript.id = 'ld-breadcrumb';
        bcScript.textContent = JSON.stringify(breadcrumbList);
        head.appendChild(bcScript);
      }

      if (!document.getElementById('ld-webapp')) {
        const toolName = pageTitle.split(' - ')[0].split(' | ')[0].trim();
        const webApp = {
          '@context': 'https://schema.org',
          '@type': 'WebApplication',
          name: toolName,
          headline: pageTitle,
          description: pageDesc,
          url: pageUrl,
          applicationCategory: 'UtilitiesApplication',
          operatingSystem: 'Any',
          inLanguage: 'ko',
          isAccessibleForFree: true,
          offers: { '@type': 'Offer', price: '0', priceCurrency: 'KRW' },
          publisher: { '@type': 'Organization', name: siteName, url: siteUrl }
        };
        const appScript = document.createElement('script');
        appScript.type = 'application/ld+json';
        appScript.id = 'ld-webapp';
        appScript.textContent = JSON.stringify(webApp);
        head.appendChild(appScript);
      }
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', enhanceSEO);
  } else {
    enhanceSEO();
  }
})();
