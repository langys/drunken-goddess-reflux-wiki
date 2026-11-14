import Link from 'next/link';

export default function NotFound() {
  return (
    <div className="py-20 text-center">
      <h1 className="text-4xl font-extrabold tracking-tight">404</h1>
      <p className="mt-4 text-muted-foreground">That page does not exist yet.</p>
      <Link
        href="/"
        className="mt-8 inline-block rounded-lg bg-primary px-5 py-2.5 font-medium text-primary-foreground"
      >
        Back to home
      </Link>
    </div>
  );
}
