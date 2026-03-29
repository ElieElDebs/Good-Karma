import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const title = searchParams.get("title") || "";
  const body = searchParams.get("body") || "";
  const subreddits = searchParams.getAll("subreddits");
  const params = new URLSearchParams({
    title,
    body,
  });
  subreddits.forEach((s) => params.append("subreddits", s));
  const url = `${process.env.NEXT_PUBLIC_API_URL}search?${params.toString()}`;
  const apiRes = await fetch(url, { method: "GET" });
  if (!apiRes.ok) {
    return NextResponse.json({ error: "Erreur API" }, { status: 500 });
  }
  const data = await apiRes.json();
  return NextResponse.json(data);
}
