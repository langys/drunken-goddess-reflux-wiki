/**
 * Root layout.
 *
 * It intentionally renders children without <html>/<body>: the real document
 * shell lives in app/[locale]/layout.tsx so that `lang` reflects the active
 * locale. Next.js still requires a layout at the root segment, and the bare `/`
 * request is handed to the [locale] tree by the middleware rewrite.
 */
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return children;
}
