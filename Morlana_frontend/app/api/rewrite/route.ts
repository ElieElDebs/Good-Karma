import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);

  const subreddit = searchParams.get("subreddit") || "";
  const draft_title = searchParams.get("draft_title") || "";
  const draft_body = searchParams.get("draft_body") || "";
  const weakness_and_strength = searchParams.get("weakness_and_strength") || "";
  const advices = searchParams.get("advices") || "";
  const examples = searchParams.get("examples") || "";
  const ideal_title_length = searchParams.get("ideal_title_length") || "";
  const ideal_words_to_use = searchParams.get("ideal_words_to_use") || "";

  const params = new URLSearchParams({
    subreddit,
    draft_title,
    draft_body,
    weakness_and_strength,
    advices,
    examples,
    ideal_title_length,
    ideal_words_to_use,
  });

  const url = `${process.env.NEXT_PUBLIC_API_URL}rewrite?${params.toString()}`;

  try {
    const apiRes = await fetch(url, {
      method: "GET",
      headers: { "X-API-KEY": process.env.API_KEY ?? "" },
    });

    if (!apiRes.ok) {
      return NextResponse.json(
        { error: "Erreur API backend" },
        { status: apiRes.status }
      );
    }

    const data = await apiRes.json();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: "Erreur lors de la connexion à l'API" },
      { status: 500 }
    );
  }
}
