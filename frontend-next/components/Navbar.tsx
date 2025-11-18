import Link from "next/link";

export default function Navbar() {
  return (
    <nav>
      <Link href="/">Dashboard</Link>
      <Link href="/users">Users</Link>
      <Link href="/reports">Reports</Link>
    </nav>
  );
}
