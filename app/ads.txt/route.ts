export const dynamic = 'force-static';

/**
 * ads.txt — served at /ads.txt.
 *
 * Publishing this lets AdSense verify that you (your publisher ID) are authorised
 * to sell your inventory, which is a hard requirement for AdSense. Submit it at
 * the same time as the AdSense application, not after approval.
 */
export function GET() {
  const publisherId = process.env.NEXT_PUBLIC_ADSENSE_PUB_ID ?? 'pub-XXXXXXXXXXXXXXXX';

  const body = `google.com, ${publisherId}, DIRECT, f08c47fec0942fa0\n`;

  return new Response(body, {
    headers: {
      'content-type': 'text/plain; charset=utf-8',
      'cache-control': 'public, max-age=3600, s-maxage=86400',
    },
  });
}
