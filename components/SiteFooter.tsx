import Link from 'next/link';
import { useTranslations } from 'next-intl';
import { siteConfig } from '@/config/site.config';
import { getAllGuides } from '@/lib/content';

export function SiteFooter({ locale }: { locale: string }) {
  const t = useTranslations();
  const prefix = locale === siteConfig.defaultLocale ? '' : `/${locale}`;
  const year = new Date().getFullYear();
  // Hubs without a single article in this locale are empty pages; leaving them
  // out of the footer keeps a partial translation from linking to dead sections.
  const guides = getAllGuides(locale);
  const footerHubs = (Object.keys(siteConfig.hubs) as Array<keyof typeof siteConfig.hubs>).filter((key) =>
    guides.some((guide) => guide.hub === key),
  );

  const legal = [
    { href: '/about', label: 'About' },
    { href: '/contact', label: 'Contact' },
    { href: '/privacy', label: 'Privacy Policy' },
    { href: '/terms', label: 'Terms of Use' },
  ];

  const tagline = t.has('hero.tagline') ? t('hero.tagline') : siteConfig.tagline;

  return (
    <footer data-site-footer="" className="mt-16 border-t border-border bg-muted/30">
      <div className="mx-auto max-w-4xl px-4 py-10">
        <div className="grid gap-8 sm:grid-cols-3">
          <div>
            <p className="mb-3 font-semibold">{siteConfig.fullName}</p>
            <p className="text-sm text-muted-foreground">{tagline}</p>
            {siteConfig.external.store && (
              <p className="mt-4">
                <a
                  href={siteConfig.external.store}
                  target="_blank"
                  rel="noopener nofollow"
                  className="inline-flex items-center gap-1.5 text-xs font-medium text-muted-foreground underline underline-offset-4 transition hover:text-foreground"
                >
                  <span>{siteConfig.external.storeLabel || 'Official Store'}</span>
                  <svg
                    className="h-3.5 w-3.5 opacity-70"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    aria-hidden="true"
                  >
                    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                    <polyline points="15 3 21 3 21 9" />
                    <line x1="10" y1="14" x2="21" y2="3" />
                  </svg>
                </a>
              </p>
            )}
          </div>

          <div>
            <p className="mb-3 text-sm font-semibold">{t.has('nav.guides') ? t('nav.guides') : 'Guides'}</p>
            <ul className="space-y-2 text-sm text-muted-foreground">
              {footerHubs.map((key) => {
                const hubLabel = t.has(`hubs.${key}.label`) ? t(`hubs.${key}.label`) : siteConfig.hubs[key].label;
                return (
                  <li key={key}>
                    <Link href={`${prefix}${siteConfig.hubs[key].href}`} className="hover:text-primary">
                      {hubLabel}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </div>

          <div>
            <p className="mb-3 text-sm font-semibold">Site</p>
            <ul className="space-y-2 text-sm text-muted-foreground">
              {legal.map((item) => (
                <li key={item.href}>
                  {/* Legal boilerplate exists only in English, so these links stay
                      unprefixed on every locale: a translated prefix would serve
                      the same English text at a second URL and split the canonical. */}
                  <Link href={item.href} className="hover:text-primary">
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-8 space-y-2 border-t border-border pt-6 text-xs text-muted-foreground">
          <p>
            © {year} {siteConfig.fullName}. All rights reserved.
          </p>
          <p>
            {siteConfig.name} is a trademark of its respective owner. This site is an unofficial fan
            resource and is not affiliated with, endorsed by, or sponsored by the developer or publisher.
            Game names, logos and screenshots remain the property of their respective owners.
          </p>
        </div>
      </div>
    </footer>
  );
}
