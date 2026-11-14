import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/** Builds `/<Game-Name>-<intent>` style slugs from a game name and intent. */
export function buildSlug(gameName: string, intent: string) {
  const base = gameName
    .replace(/['’]/g, '')
    .replace(/[^a-zA-Z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
  const tail = intent.replace(/^-+/, '');
  return `${base}-${tail}`;
}

export function formatDate(iso: string, locale = 'en') {
  return new Date(iso).toLocaleDateString(locale, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}
