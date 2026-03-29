import { NextResponse } from "next/server";

export async function GET() {
  const url = `${process.env.NEXT_PUBLIC_API_URL}subreddits`;
  const apiRes = await fetch(url, { method: "GET" });
  if (!apiRes.ok) {
    return NextResponse.json({ error: "Erreur API" }, { status: 500 });
  }
  const data = await apiRes.json();
  return NextResponse.json(data);
}
