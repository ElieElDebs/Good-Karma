import { NextResponse } from "next/server";

export async function GET() {
  const url = `${process.env.NEXT_PUBLIC_API_URL}subreddits`;
  console.log("Above the API Key")
  console.log(process.env.API_KEY)
  const apiRes = await fetch(url, {
    method: "GET",
    headers: { "X-API-KEY": process.env.API_KEY ?? "" },
  });
  if (!apiRes.ok) {
    return NextResponse.json({ error: "Erreur API" }, { status: 500 });
  }
  const data = await apiRes.json();
  return NextResponse.json(data);
}
