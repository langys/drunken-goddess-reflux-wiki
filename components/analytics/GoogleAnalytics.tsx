import Script from 'next/script';
import { siteConfig } from '@/config/site.config';

/** Validates that a measurement id is a real GA4 ID ('G-' followed by alphanumeric).
 *  Placeholders like 'G-XXXXXXXXXX' must never trigger requests or render scripts. */
function isValidGaId(id: string): boolean {
  return /^G-[A-Z0-9]+$/.test(id) && id !== 'G-XXXXXXXXXX';
}

export function GoogleAnalytics() {
  const gaId = process.env.NEXT_PUBLIC_GA_ID || siteConfig.analytics.gaId;

  if (!siteConfig.analytics.enabled || !gaId || !isValidGaId(gaId)) {
    return null;
  }

  return (
    <Script id="google-analytics" strategy="afterInteractive">
      {`
        if (window.location.hostname === '${siteConfig.domain}' || window.location.hostname === 'www.${siteConfig.domain}') {
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());
          gtag('config', '${gaId}');
          var script = document.createElement('script');
          script.async = true;
          script.src = 'https://www.googletagmanager.com/gtag/js?id=${gaId}';
          document.head.appendChild(script);
        }
      `}
    </Script>
  );
}
