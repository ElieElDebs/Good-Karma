import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();

    const url = `${process.env.NEXT_PUBLIC_API_URL}rewrite`;

    const apiRes = await fetch(url, {
      method: "POST",
      headers: {
        "X-API-KEY": process.env.API_KEY ?? "",
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (!apiRes.ok) {
      const errorData = await apiRes.text();
      console.error(`Backend error: ${apiRes.status} - ${errorData}`);
      return NextResponse.json(
        { error: `Backend API error: ${apiRes.statusText}` },
        { status: apiRes.status }
      );
    }

    const data = await apiRes.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error("Rewrite API error:", error);
    return NextResponse.json(
      { error: "Erreur lors de la connexion à l'API" },
      { status: 500 }
    );
  }
}
