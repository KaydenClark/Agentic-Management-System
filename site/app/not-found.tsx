import Link from "next/link";

export default function NotFound() {
  return (
    <>
      <h1>Page not found</h1>
      <p>
        There is no page at this address. <Link href="/">Go to the home page</Link>.
      </p>
    </>
  );
}
