import { NextRequest, NextResponse } from 'next/server';
import createMiddleware from 'next-intl/middleware';
import { canonicalHost, routing } from './i18n/routing';

const handleI18n = createMiddleware(routing);

export default function middleware(request: NextRequest) {
  const { pathname, search } = request.nextUrl;

  // 1. Collapse both host variants onto the configured canonical host, so
  //    canonical / sitemap / hreflang never disagree about the origin.
  const host = request.headers.get('host') ?? '';
  const isWww = host.startsWith('www.');
  const wantWww = canonicalHost.startsWith('www.');
  const isLocalOrPreview =
    host.startsWith('localhost') || host.includes('vercel.app') || host.startsWith('127.0.0.1');

  if (host && isWww !== wantWww && !isLocalOrPreview) {
    const url = request.nextUrl.clone();
    url.host = canonicalHost;
    return NextResponse.redirect(url, 308);
  }

  // 2. `localePrefix: 'as-needed'` means the default locale is unprefixed, but
  //    next-intl still rewrites the bare root. Normalising `/en/...` to `/...`
  //    before that rewrite keeps one URL per page instead of two.
  const defaultPrefix = `/${routing.defaultLocale}`;
  if (pathname === defaultPrefix || pathname.startsWith(`${defaultPrefix}/`)) {
    const url = request.nextUrl.clone();
    url.pathname = pathname.slice(defaultPrefix.length) || '/';
    return NextResponse.redirect(url, 308);
  }

  return handleI18n(request);
}

export const config = {
  // Skip API routes, Next internals, and any path containing a dot (files).
  matcher: ['/((?!api|_next|_vercel|.*\\..*).*)'],
};
