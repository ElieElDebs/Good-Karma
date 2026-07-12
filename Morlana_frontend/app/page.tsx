"use client";
import React, { useState, useTransition, useEffect } from "react";
import dynamic from "next/dynamic";
import { ActionMeta } from "react-select";
import ScoreGauge from "./components/ScoreGauge";
import KpiBar from "./components/KpiBar";

const SpiderChart = dynamic(() => import("./components/SpiderChart"), { ssr: false });

// Utilise le composant Select en dynamique côté client pour éviter le mismatch SSR/hydration
const Select = dynamic(() => import("react-select"), { ssr: false });

function getGESColor(label: string) {
  switch (label) {
    case "Bad":
      return "var(--color-danger)";
    case "Medium":
      return "var(--color-warning)";
    case "Good":
      return "var(--color-primary)";
    case "Really Good":
      return "var(--color-success)";
    default:
      return "var(--color-muted)";
  }
}

function getSemanticConfidenceColor(score: number) {
  if (score < 30) return "var(--color-danger)";
  if (score < 50) return "var(--color-warning)";
  if (score < 70) return "var(--color-primary)";
  return "var(--color-success)";
}

function getSemanticConfidenceLabel(score: number) {
  if (score < 30) return "Poor";
  if (score < 50) return "Fair";
  if (score < 70) return "Good";
  return "Excellent";
}

// Tooltip component
function Tooltip({ content, children }: { content: React.ReactNode; children: React.ReactNode }) {
  const [visible, setVisible] = useState(false);
  return (
    <span
      style={{ position: "relative", display: "inline-block" }}
      onMouseEnter={() => setVisible(true)}
      onMouseLeave={() => setVisible(false)}
    >
      {children}
      {visible && (
        <div
          style={{
            position: "absolute",
            left: "110%",
            top: "50%",
            transform: "translateY(-50%)",
            background: "var(--color-bg-section)",
            color: "var(--color-light)",
            border: "1px solid var(--color-border)",
            borderRadius: 8,
            boxShadow: "0 2px 8px rgba(0,0,0,0.18)",
            padding: "12px 16px",
            minWidth: 220,
            zIndex: 100,
            fontSize: 14,
            whiteSpace: "normal",
            fontWeight: 400,
          }}
        >
          {content}
        </div>
      )}
    </span>
  );
}


function SemanticRangeBar({
  min, avg, max, draftScore,
}: {
  min: number; avg: number; max: number; draftScore?: number;
}) {
  const scale = (v: number) => `${Math.min(97, Math.max(3, v * 100)).toFixed(1)}%`;
  const draftPct = draftScore !== undefined ? Math.min(97, Math.max(3, draftScore * 100)) : undefined;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
      <span style={{ fontSize: 11, fontWeight: 600, color: "var(--color-gray)", textTransform: "uppercase", letterSpacing: "0.04em" }}>
        Relevance Score
      </span>

      <div style={{ position: "relative", height: 24 }}>
        {/* Track */}
        <div style={{ position: "absolute", top: "50%", left: 0, right: 0, height: 6, transform: "translateY(-50%)", borderRadius: 99, background: "var(--color-bg-input)" }} />

        {/* Community range band */}
        <div style={{
          position: "absolute",
          top: "50%",
          left: scale(min),
          width: `${(max - min) * 100}%`,
          height: 6,
          transform: "translateY(-50%)",
          background: "var(--color-orange)",
          opacity: 0.2,
          borderRadius: 99,
        }} />

        {/* Min dot */}
        <div style={{ position: "absolute", top: "50%", left: scale(min), width: 8, height: 8, borderRadius: "50%", background: "var(--color-orange)", opacity: 0.5, transform: "translate(-50%, -50%)" }} />

        {/* Avg dot (larger, full opacity) */}
        <div style={{ position: "absolute", top: "50%", left: scale(avg), width: 14, height: 14, borderRadius: "50%", background: "var(--color-orange)", transform: "translate(-50%, -50%)" }} />

        {/* Max dot */}
        <div style={{ position: "absolute", top: "50%", left: scale(max), width: 8, height: 8, borderRadius: "50%", background: "var(--color-orange)", opacity: 0.5, transform: "translate(-50%, -50%)" }} />

        {/* Draft dot */}
        {draftPct !== undefined && (
          <div style={{
            position: "absolute",
            top: "50%",
            left: `${draftPct}%`,
            width: 14,
            height: 14,
            borderRadius: "50%",
            background: "var(--color-blue)",
            border: "2.5px solid var(--color-bg-section)",
            transform: "translate(-50%, -50%)",
            boxSizing: "border-box",
          }} />
        )}
      </div>

      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11 }}>
        <span><span style={{ color: "var(--color-orange)", fontWeight: 600 }}>{min.toFixed(2)}</span><span style={{ color: "var(--color-gray)", marginLeft: 3 }}>min</span></span>
        <span><span style={{ color: "var(--color-orange)", fontWeight: 700 }}>{avg.toFixed(2)}</span><span style={{ color: "var(--color-gray)", marginLeft: 3 }}>avg</span></span>
        <span><span style={{ color: "var(--color-orange)", fontWeight: 600 }}>{max.toFixed(2)}</span><span style={{ color: "var(--color-gray)", marginLeft: 3 }}>max</span></span>
        {draftScore !== undefined && (
          <span><span style={{ color: "var(--color-blue)", fontWeight: 700 }}>{draftScore.toFixed(2)}</span><span style={{ color: "var(--color-gray)", marginLeft: 3 }}>draft</span></span>
        )}
      </div>
    </div>
  );
}

const titleKpiTooltips: Record<string, React.ReactNode> = {
  "average_title_length": "Number of characters in the title. Too short and it lacks context; too long and it may get cut off. Compare with the average of top-performing posts in this subreddit.",
  "average_title_word_count": "Number of words in the title. Titles with too few words feel vague; too many and they become hard to scan at a glance. Aim for the sweet spot this community responds to.",
  "average_title_question_count": "Number of question marks in the title. Question-based titles invite interaction and tend to generate more comments — but overusing them can feel clickbait-y.",
  "average_title_exclamation_count": "Number of exclamation points. A touch of enthusiasm grabs attention, but too many can come across as shouting or spam. Check what successful posts in this subreddit do.",
  "average_title_polarity": "Emotional tone of the title, from -1 (very negative) to +1 (very positive). Some communities respond better to a positive framing, others to a neutral or critical one.",
  "average_title_subjectivity": "How opinion-based the title is, from 0 (purely factual) to 1 (highly subjective). News subreddits favour factual titles; debate-focused ones expect opinions.",
  "average_title_uppercase_word_count": "Number of fully ALL-CAPS words. Used sparingly, they emphasise a key term. Overused, they signal shouting and may trigger spam filters.",
};

const bodyKpiTooltips: Record<string, React.ReactNode> = {
  "average_word_count": "Total word count of the post body. Too short feels low-effort; too long and readers drop off. Align with the length of posts that performed well here.",
  "average_sentence_count": "Number of sentences. More sentences means the text is broken into digestible ideas. A high word-to-sentence ratio indicates long, dense sentences.",
  "average_readability_score": "Flesch Reading Ease score (0–100). Higher = easier to read. Above 60 is accessible to most readers; below 30 is very technical. Match the level your audience expects.",
  "average_polarity": "Average emotional tone of the body (-1 very negative → +1 very positive). Helps you understand whether this community responds better to positive, neutral, or critical content.",
  "average_subjectivity": "How opinionated the body is (0 = factual, 1 = fully subjective). Compare your writing style with what resonates in this subreddit.",
  "total_posts_with_links": "Number of reference posts that include an external link. If most do, adding a link may help your post fit the community norm.",
  "percentage_posts_with_links": "Percentage of reference posts that contain a link. A high rate means links are expected here; a low rate suggests plain-text posts tend to do better.",
};

// Tooltip contents for each factor
const factorTooltips: Record<string, React.ReactNode> = {
  "title_score": (
    <>
      <strong>Title Impact</strong><br />
      Measures the alignment of your title's polarity (emotional tone) with posts that generated the most clicks in this subreddit. A high score means your title uses a similar emotional charge to the community standard.
    </>
  ),
  "body_score": (
    <>
      <strong>Body Score</strong><br />
      Analyzes your text's complexity using the Flesch Reading Ease index. The score is optimal if your text is as simple or more accessible than successful posts; it only decreases if your writing is too complex for the audience.
    </>
  ),
  "substance_score": (
    <>
      <strong>Substance</strong><br />
      Evaluates your word count against the average of viral posts using a logarithmic curve. You gain points quickly at first, but reaching the maximum requires closely matching the "ideal length" found for this subreddit.
    </>
  ),
  "semantic_score": (
    <>
      <strong>Semantic Component</strong><br />
      Measures how closely your topic aligns with historically successful themes. This is separate from the Semantic Alignment score above—it's one input to the Structure Score calculation.
    </>
  )
};

export default function Home() {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [subreddits, setSubreddits] = useState<any[]>([]);
  const [result, setResult] = useState<any>(null);
  const [isPending, startTransition] = useTransition();
  const [error, setError] = useState("");
  const [subredditOptions, setSubredditOptions] = useState<{ value: string; label: string }[]>([]);
  const [showPosts, setShowPosts] = useState<{ [subreddit: string]: boolean }>({});

  // Fetch subreddits from API on mount
  useEffect(() => {
    async function fetchSubreddits() {
      try {
        const res = await fetch("/api/subreddits");
        const data = await res.json();
        if (data?.data?.subreddits) {
          setSubredditOptions(
            data.data.subreddits.map((s: string) => ({ value: s, label: s }))
          );
        }
      } catch (err) {
        setSubredditOptions([]);
      }
    }
    fetchSubreddits();
  }, []);

  
  async function handleSearch(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setError("");
    setResult(null);
    if (!title.trim() || !content.trim() || subreddits.length === 0) {
      setError("Please fill in the post title, content, and select at least one subreddit.");
      return;
    }
    startTransition(async () => {
      try {
        // Correction : appel GET avec query params
        const params = new URLSearchParams({
          title: title,
          body: content,
        });
        subreddits.forEach((s) => params.append("subreddits", s.value));
        const res = await fetch(`/api/search?${params.toString()}`, {
          method: "GET"
        });
        const data = await res.json();
        if (data.error) throw new Error(data.error);
        setResult(data.data || data); // selon structure retour API
      } catch (err) {
        setError("An error occurred during the search.");
      }
    });
  }

  // Correction: Adapter la fonction onChange pour react-select
  function handleSubredditsChange(
    newValue: any,
    _actionMeta: ActionMeta<any>
  ) {
    setSubreddits(newValue || []);
  }

  function toggleShowPosts(subreddit: string) {
    setShowPosts(prev => ({
      ...prev,
      [subreddit]: !prev[subreddit]
    }));
  }

  // Helper pour afficher le meilleur moment à poster
  function renderBestTimeToPost(subreddit: string) {
    const bestTimes = result?.best_times_to_post?.[subreddit];
    if (!bestTimes) return <span className="text-gray">No data</span>;
    return (
      <div className="flex flex-col items-center">
        <span className="text-lg font-bold text-orange text-center">
          {bestTimes.best_day} at {bestTimes.best_hour}:00
        </span>
      </div>
    );
  }

  return (
    <main className="flex min-h-screen flex-col items-center bg-section px-2 md:px-6 py-8 gap-4">
      {/* Card d'intro */}
      <section className="w-full max-w-7xl bg-card shadow-xl rounded-2xl px-4 md:px-8 py-4 md:py-8 flex flex-col gap-2 border border-border mb-2">
        <h1 className="text-3xl md:text-4xl font-extrabold text-orange mb-1">Good Karma</h1>
        <p className="text-light text-base md:text-lg">
          Good Karma helps you optimize your Reddit posts for maximum engagement and visibility.
          Enter your post draft and instantly compare its key metrics (KPIs) with successful posts from the community.
          The tool analyzes your title and body, provides actionable advice, and highlights the most relevant keywords.
          <br /><br />
          <span className="font-semibold text-orange">Structure Score:</span>
          This score evaluates the quality and potential of your post based on title impact, readability, word count, and substance.
          <br />
          <span className="font-semibold text-orange">Semantic Alignment:</span>
          This score measures how well your topic aligns with successful posts in the community (0–100%).
          <br />
          <span className="font-semibold">Score scale:</span>
          <span className="ml-2">Bad (≤ 45) | Medium (≤ 65) | Good (≤ 85) | Really Good (&gt; 85)</span>
          <br />
          Use Good Karma to quickly see how your draft compares, understand what works, and improve your chances of success on Reddit.
        </p>
      </section>
      {/* Card principale */}
      <section className="w-full max-w-7xl bg-card shadow-2xl rounded-2xl px-4 md:px-10 py-4 md:py-10 flex flex-col gap-6 relative border border-border">
        <form className="flex flex-col gap-6" onSubmit={handleSearch}>
          <div>
            <h2 className="text-2xl md:text-3xl font-bold text-orange mb-2">Create a Reddit post</h2>
            <p className="text-light text-base md:text-lg mb-4">Fill in the title and content of your Reddit post, select one or more subreddits, then click "Search" to generate or find similar posts.</p>
          </div>
          <div className="flex flex-col gap-4">
            {/* Subreddit Selector */}
            <label className="text-sm font-medium text-lightest" htmlFor="subreddit-select">Subreddit(s)</label>
            <Select
              id="subreddit-select"
              options={subredditOptions}
              value={subreddits}
              onChange={handleSubredditsChange}
              isMulti
              placeholder="Select subreddit(s)..."
              className="react-select-container"
              classNamePrefix="react-select"
              styles={{
                control: (base) => ({
                  ...base,
                  backgroundColor: "var(--color-bg-input)",
                  borderColor: "var(--color-border)",
                  color: "var(--color-lightest)",
                  minHeight: "44px",
                  boxShadow: "none",
                }),
                menu: (base) => ({
                  ...base,
                  backgroundColor: "var(--color-bg-section)",
                  color: "var(--color-lightest)",
                }),
                option: (base, state) => ({
                  ...base,
                  backgroundColor: state.isSelected ? "var(--color-orange)" : "var(--color-bg-section)",
                  color: state.isSelected ? "#fff" : "var(--color-lightest)",
                  cursor: "pointer",
                }),
                multiValue: (base) => ({
                  ...base,
                  backgroundColor: "var(--color-orange)",
                  color: "#fff",
                }),
                multiValueLabel: (base) => ({
                  ...base,
                  color: "#fff",
                }),
                multiValueRemove: (base) => ({
                  ...base,
                  color: "#fff",
                  ':hover': { backgroundColor: "var(--color-orange-hover)", color: "#fff" },
                }),
                placeholder: (base) => ({
                  ...base,
                  color: "var(--color-gray)",
                }),
                singleValue: (base) => ({
                  ...base,
                  color: "var(--color-lightest)",
                }),
                input: (base) => ({
                  ...base,
                  color: "var(--color-lightest)",
                }),
              }}
              isDisabled={subredditOptions.length === 0}
              noOptionsMessage={() => "No subreddits available"}
            />
            <label className="text-sm font-medium text-lightest" htmlFor="post-title">Post title</label>
            <input
              id="post-title"
              type="text"
              placeholder="Title..."
              value={title}
              onChange={e => setTitle(e.target.value)}
              className="w-full rounded-lg border border-border bg-input px-4 py-2 text-lightest focus:outline-none focus:ring-2 focus:ring-orange transition"
            />
            <label className="text-sm font-medium text-lightest mt-2" htmlFor="post-content">Post content</label>
            <textarea
              id="post-content"
              placeholder="Write your Reddit post here (can be long)..."
              rows={6}
              value={content}
              onChange={e => setContent(e.target.value)}
              className="w-full rounded-lg border border-border bg-input px-4 py-2 text-lightest focus:outline-none focus:ring-2 focus:ring-orange transition resize-y min-h-[120px]"
            />
          </div>
          <div className="flex justify-end mt-2">
            <button
              type="submit"
              disabled={isPending}
              className="bg-orange hover:bg-orange-hover text-white font-semibold px-6 py-2 rounded-lg shadow-md transition-all focus:outline-none focus:ring-2 focus:ring-orange/50 disabled:opacity-60 disabled:cursor-not-allowed"
            >
              {isPending ? "Searching..." : "Search"}
            </button>
          </div>
          {error && <div className="text-danger text-sm mt-2">{error}</div>}
        </form>
      </section>

      {/* Card résultat API */}
      {result && (
        <>
          {Object.keys(result.kpi_by_subreddit || {}).map((subreddit) => (
            <section
              key={subreddit}
              className="w-full max-w-7xl bg-card shadow-2xl rounded-2xl px-4 md:px-10 py-6 md:py-10 flex flex-col gap-8 border border-border mt-2 animate-fade-in"
            >
              <h2 className="text-2xl md:text-3xl font-bold text-orange mb-2">
                Analysis results for <span className="text-blue">{subreddit}</span>
              </h2>
              {/* Structure Score & Semantic Confidence */}
              {result.ges_results?.[subreddit]?.GES && (() => {
                const ges = result.ges_results[subreddit].GES;
                const gesColor = getGESColor(ges.label);
                const semanticConfidence = ges.semantic_confidence ?? 0;
                const semanticColor = getSemanticConfidenceColor(semanticConfidence);
                const semanticLabel = getSemanticConfidenceLabel(semanticConfidence);

                return (
                  <>
                    {/* Three-column score cards with flex-wrap */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                      {/* Structure Score Card */}
                      <div
                        className="flex flex-col p-6 rounded-xl"
                        style={{ background: gesColor + "18" }}
                      >
                        <div className="flex flex-col items-center justify-center h-full">
                          <span style={{ fontSize: 11, fontWeight: 600, color: "var(--color-gray)", textTransform: "uppercase", letterSpacing: "0.04em", marginBottom: 6 }}>
                            Structure Score
                          </span>
                          <ScoreGauge
                            score={ges.score ?? 0}
                            label={ges.label ?? ""}
                            color={gesColor}
                          />
                          <p style={{ fontSize: 12, color: "var(--color-light)", marginTop: 12, textAlign: "center", fontStyle: "italic" }}>
                            Measures title, body, and substance quality
                          </p>
                        </div>
                      </div>

                      {/* Semantic Confidence Card */}
                      <div
                        className="flex flex-col p-6 rounded-xl"
                        style={{ background: semanticColor + "18" }}
                      >
                        <div className="flex flex-col items-center justify-center h-full">
                          <span style={{ fontSize: 11, fontWeight: 600, color: "var(--color-gray)", textTransform: "uppercase", letterSpacing: "0.04em", marginBottom: 6 }}>
                            Semantic Alignment
                          </span>
                          <div style={{ position: "relative", width: 160, height: 160, marginBottom: 16 }}>
                            <svg viewBox="0 0 160 160" style={{ width: "100%", height: "100%" }}>
                              {/* Background circle */}
                              <circle cx="80" cy="80" r="75" fill="none" stroke="var(--color-bg-input)" strokeWidth="8" />
                              {/* Progress circle */}
                              <circle
                                cx="80"
                                cy="80"
                                r="75"
                                fill="none"
                                stroke={semanticColor}
                                strokeWidth="8"
                                strokeDasharray={`${(semanticConfidence / 100) * 471} 471`}
                                strokeLinecap="round"
                                style={{ transformOrigin: "80px 80px", transform: "rotate(-90deg)", transition: "stroke-dasharray 0.6s ease" }}
                              />
                            </svg>
                            <div style={{
                              position: "absolute",
                              top: "50%",
                              left: "50%",
                              transform: "translate(-50%, -50%)",
                              textAlign: "center"
                            }}>
                              <div style={{
                                fontSize: 32,
                                fontWeight: 700,
                                color: semanticColor
                              }}>
                                {semanticConfidence.toFixed(0)}%
                              </div>
                              <div style={{
                                fontSize: 11,
                                fontWeight: 600,
                                color: "var(--color-gray)",
                                marginTop: 4,
                                textTransform: "uppercase"
                              }}>
                                {semanticLabel}
                              </div>
                            </div>
                          </div>
                          <p style={{ fontSize: 12, color: "var(--color-light)", marginTop: 12, textAlign: "center", fontStyle: "italic" }}>
                            How aligned with successful topics here
                          </p>
                        </div>
                      </div>

                      {/* Spider chart – same level as scores */}
                      {ges.factors && (
                        <div className="flex flex-col p-6 rounded-xl" style={{ background: gesColor + "18" }}>
                          <span style={{ display: "block", fontSize: 11, fontWeight: 600, color: "var(--color-gray)", textTransform: "uppercase", letterSpacing: "0.04em", marginBottom: 6 }}>
                            Score Breakdown
                          </span>
                          <div style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center" }}>
                            <SpiderChart factors={ges.factors} color={gesColor} />
                          </div>
                        </div>
                      )}
                    </div>
                  </>
                );
              })()}

              {/* Advice */}
              {result.ges_results?.[subreddit]?.advice && (
                <div className="w-full bg-section rounded-xl p-4 shadow flex flex-col gap-2 border border-border">
                  <h4 className="text-lg font-bold text-orange mb-2">Advice</h4>
                  <ul className="list-disc pl-6 text-light">
                    {result.ges_results[subreddit].advice.map(
                      (a: string, idx: number) => (
                        <li key={idx}>{a}</li>
                      )
                    )}
                  </ul>
                </div>
              )}

              {/* Context: best time + semantic range */}
              {result.kpi_by_subreddit?.[subreddit]?.global_body_kpi && (
                <div className="flex flex-col sm:flex-row gap-4">
                  {/* Best time to post */}
                  <div className="flex flex-col items-center bg-section border border-orange rounded-xl px-5 py-4 shadow min-w-[180px]">
                    <span className="text-xs font-semibold text-gray mb-1 flex items-center gap-2 justify-center">
                      <svg className="w-4 h-4 text-orange" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" /><path d="M12 6v6l4 2" /></svg>
                      Best time to post
                    </span>
                    {renderBestTimeToPost(subreddit)}
                  </div>

                  {/* Semantic range bar */}
                  {result.kpi_by_subreddit[subreddit].global_body_kpi.scores && (
                    <div className="flex-1 bg-section border border-border rounded-xl px-5 py-4 shadow">
                      <SemanticRangeBar
                        min={result.kpi_by_subreddit[subreddit].global_body_kpi.scores.min_score ?? 0}
                        avg={result.kpi_by_subreddit[subreddit].global_body_kpi.scores.average_score ?? 0}
                        max={result.kpi_by_subreddit[subreddit].global_body_kpi.scores.max_score ?? 0}
                        draftScore={result.draft_post_kpi?.body_kpi?.scores?.average_score}
                      />
                    </div>
                  )}
                </div>
              )}

              {/* Title KPI Comparison */}
              {result.kpi_by_subreddit?.[subreddit]?.global_title_kpi && (
                <div className="w-full bg-section rounded-xl px-5 py-4 shadow flex flex-col gap-2 border border-border">
                  <div className="flex items-center gap-3 mb-1">
                    <h4 className="text-base font-bold text-orange">Title KPIs</h4>
                    <span className="flex items-center gap-1 text-xs text-gray">
                      <span style={{ display: "inline-block", width: 10, height: 10, borderRadius: "50%", background: "var(--color-orange)" }} /> Posts
                      <span style={{ display: "inline-block", width: 10, height: 10, borderRadius: "50%", background: "var(--color-blue)", marginLeft: 8 }} /> Draft
                    </span>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-x-8 divide-y divide-[var(--color-border)]">
                    {[
                      { key: "average_title_length", label: "Title Length" },
                      { key: "average_title_word_count", label: "Word Count" },
                      { key: "average_title_question_count", label: "Questions" },
                      { key: "average_title_exclamation_count", label: "Exclamations" },
                      { key: "average_title_polarity", label: "Polarity", min: -1, max: 1, fmt: (v: number) => v.toFixed(2) },
                      { key: "average_title_subjectivity", label: "Subjectivity", min: 0, max: 1, fmt: (v: number) => v.toFixed(2) },
                      { key: "average_title_uppercase_word_count", label: "Uppercase Words" },
                    ].map(({ key, label, min, max, fmt }) => (
                      <KpiBar
                        key={key}
                        label={label}
                        postsValue={result.kpi_by_subreddit[subreddit].global_title_kpi[key]}
                        draftValue={result.draft_post_kpi?.title_kpi?.[key]}
                        min={min}
                        max={max}
                        format={fmt}
                        tooltip={titleKpiTooltips[key]}
                      />
                    ))}
                  </div>

                  {/* Most used words in titles */}
                  {result.kpi_by_subreddit[subreddit].global_title_kpi.most_used_title_words && (
                    <div className="pt-2 border-t border-[var(--color-border)] mt-1">
                      <strong className="text-orange text-sm">Most used words in similar titles:</strong>
                      <ul className="flex flex-wrap gap-2 mt-2">
                        {result.kpi_by_subreddit[subreddit].global_title_kpi.most_used_title_words.map(
                          ([word, count]: [string, number]) => (
                            <li key={word} className="bg-input px-2 py-1 rounded text-light text-sm">
                              {word} <span className="text-orange">({count})</span>
                            </li>
                          )
                        )}
                      </ul>
                    </div>
                  )}
                </div>
              )}

              {/* Body KPI Comparison */}
              {result.kpi_by_subreddit?.[subreddit]?.global_body_kpi && (
                <div className="w-full bg-section rounded-xl px-5 py-4 shadow flex flex-col gap-2 border border-border">
                  <div className="flex items-center gap-3 mb-1">
                    <h4 className="text-base font-bold text-orange">Body KPIs</h4>
                    <span className="flex items-center gap-1 text-xs text-gray">
                      <span style={{ display: "inline-block", width: 10, height: 10, borderRadius: "50%", background: "var(--color-orange)" }} /> Posts
                      <span style={{ display: "inline-block", width: 10, height: 10, borderRadius: "50%", background: "var(--color-blue)", marginLeft: 8 }} /> Draft
                    </span>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-x-8 divide-y divide-[var(--color-border)]">
                    {[
                      { key: "average_word_count", label: "Word Count", section: "words_and_sentences", fmt: (v: number) => Math.round(v).toString() },
                      { key: "average_sentence_count", label: "Sentence Count", section: "words_and_sentences", fmt: (v: number) => Math.round(v).toString() },
                      { key: "average_readability_score", label: "Readability", section: "polarity_and_readability_subjectivity", min: 0, max: 100, fmt: (v: number) => v.toFixed(1) },
                      { key: "average_polarity", label: "Polarity", section: "polarity_and_readability_subjectivity", min: -1, max: 1, fmt: (v: number) => v.toFixed(2) },
                      { key: "average_subjectivity", label: "Subjectivity", section: "polarity_and_readability_subjectivity", min: 0, max: 1, fmt: (v: number) => v.toFixed(2) },
                      { key: "total_posts_with_links", label: "Posts with Links", section: "links_and_time", fmt: (v: number) => Math.round(v).toString() },
                      { key: "percentage_posts_with_links", label: "Links (%)", section: "links_and_time", min: 0, max: 100, fmt: (v: number) => v.toFixed(0) + "%" },
                    ].map(({ key, label, section, min, max, fmt }) => (
                      <KpiBar
                        key={key}
                        label={label}
                        postsValue={result.kpi_by_subreddit[subreddit].global_body_kpi[section]?.[key]}
                        draftValue={result.draft_post_kpi?.body_kpi?.[section]?.[key]}
                        min={min}
                        max={max}
                        format={fmt}
                        tooltip={bodyKpiTooltips[key]}
                      />
                    ))}
                  </div>

                  {/* Most used words */}
                  {result.kpi_by_subreddit[subreddit].global_body_kpi.words_and_sentences?.most_used_words && (
                    <div className="pt-2 border-t border-[var(--color-border)] mt-1">
                      <strong className="text-orange text-sm">Most used words in similar posts:</strong>
                      <ul className="flex flex-wrap gap-2 mt-2">
                        {result.kpi_by_subreddit[subreddit].global_body_kpi.words_and_sentences.most_used_words.map(
                          ([word, count]: [string, number]) => (
                            <li key={word} className="bg-input px-2 py-1 rounded text-light text-sm">
                              {word} <span className="text-orange">({count})</span>
                            </li>
                          )
                        )}
                      </ul>
                    </div>
                  )}
                </div>
              )}

              {/* Posts à succès */}
              {result.posts_by_subreddit?.[subreddit] && (
                <div className="w-full">
                  <div
                    className="flex items-center cursor-pointer select-none mb-4 group"
                    onClick={() => toggleShowPosts(subreddit)}
                    tabIndex={0}
                    role="button"
                    aria-expanded={!!showPosts[subreddit]}
                    aria-label="Afficher les posts à succès"
                    onKeyDown={e => {
                      if (e.key === "Enter" || e.key === " ") toggleShowPosts(subreddit);
                    }}
                  >
                    <h4 className="text-lg font-bold text-orange mr-2">Successful Posts</h4>
                    <span className="text-xs text-gray mr-2">
                      ({result.posts_by_subreddit[subreddit].length})
                    </span>
                    <svg
                      className={`w-5 h-5 text-orange transition-transform duration-200 group-hover:scale-125 ${showPosts[subreddit] ? "rotate-90" : ""}`}
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      viewBox="0 0 24 24"
                      style={{ cursor: "pointer" }}
                    >
                      <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                  <div
                    style={{
                      maxHeight: showPosts[subreddit] ? "5000px" : "0px",
                      overflow: "hidden",
                      transition: "max-height 0.4s cubic-bezier(.4,0,.2,1)"
                    }}
                  >
                    {showPosts[subreddit] && (
                      <div className="flex flex-col gap-4">
                        {result.posts_by_subreddit[subreddit].length === 0 ? (
                          <div className="text-gray italic text-sm px-2 py-2">
                            Aucun post à succès trouvé.
                          </div>
                        ) : (
                          result.posts_by_subreddit[subreddit].map((post: any) => (
                            <div key={post.id} className="reddit-post-card w-full bg-section border border-border rounded-2xl shadow p-4 flex flex-col gap-2 mb-4">
                              <div className="reddit-post-header flex flex-col md:flex-row md:items-center md:justify-between gap-1 mb-2">
                                <a
                                  href={post.url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="reddit-post-title text-lg md:text-xl font-bold text-orange hover:underline"
                                >
                                  {post.title}
                                </a>
                                <span className="reddit-post-author text-xs text-gray md:ml-2">
                                  par {post.author || "[unknown]"} • r/{post.subreddit}
                                </span>
                              </div>
                              <div className="reddit-post-body text-light text-sm mb-2">
                                {post.text && post.text.length > 0
                                  ? post.text.slice(0, 180) + (post.text.length > 180 ? "..." : "")
                                  : <span className="italic text-gray">(Pas de texte)</span>}
                              </div>
                              <div className="reddit-post-footer flex flex-wrap items-center gap-4 text-xs text-gray mt-2">
                                <span className="reddit-post-score bg-input rounded px-2 py-1 text-orange font-semibold">Score: {post.score?.toFixed(3)}</span>
                                <span className="reddit-post-upvotes">⬆️ {post.nb_upvote}</span>
                                <span className="reddit-post-comments">💬 {post.nb_comment}</span>
                                <span className="reddit-post-date ml-auto md:ml-0">{post.date ? new Date(post.date * 1000).toLocaleDateString() : ""}</span>
                              </div>
                            </div>
                          ))
                        )}
                      </div>
                    )}
                  </div>
                </div>
              )}
            </section>
          ))}
        </>
      )}
    </main>
  );
}
