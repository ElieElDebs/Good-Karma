"use client";
import React, { useState, useTransition, useEffect } from "react";
import dynamic from "next/dynamic";
import { ActionMeta } from "react-select";

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
      <strong>Bordy Score</strong><br />
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
      <strong>Semantic</strong><br />
      Calculates semantic similarity between your topic and historically successful themes. This factor acts as a "gatekeeper": if alignment is below 0.7, it warns of a high risk of being off-topic.
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
          <span className="font-semibold text-orange">Global Score:</span> 
          This score summarizes the overall quality and potential of your post based on readability, length, semantics, and title impact.
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
              {/* GES Score & Label */}
              {result.ges_results?.[subreddit]?.GES && (
                <div
                  className="flex flex-col md:flex-row items-center gap-6 p-6 rounded-xl"
                  style={{
                    background:
                      getGESColor(result.ges_results[subreddit].GES.label) + "22",
                  }}
                >
                  <div className="flex flex-col items-center justify-center gap-2">
                    <span
                      className="text-4xl font-extrabold"
                      style={{
                        color: getGESColor(result.ges_results[subreddit].GES.label),
                      }}
                    >
                      {result.ges_results[subreddit].GES.score?.toFixed(2)}
                    </span>
                    <span
                      className="text-lg font-bold"
                      style={{
                        color: getGESColor(result.ges_results[subreddit].GES.label),
                      }}
                    >
                      {result.ges_results[subreddit].GES.label}
                    </span>
                  </div>
                  <div className="flex flex-col gap-2">
                    <span className="text-base font-semibold text-light">
                      Factors:
                    </span>
                    <div className="flex flex-wrap gap-3">
                      {result.ges_results[subreddit].GES.factors &&
                        Object.entries(result.ges_results[subreddit].GES.factors).map(
                          ([key, value]) => {
                            const factorLabels: Record<string, string> = {
                              "F_Titre": "Title",
                              "F_Lisibilité": "Readability",
                              "F_Longueur": "Substance",
                              "F_Sémantique": "Relevance",
                              "F_Lexical": "Vocabulary",
                            };
                            const label = factorLabels[key] || key;
                            return (
                              <span
                                key={key}
                                className="px-3 py-1 rounded bg-input text-orange font-semibold text-sm flex items-center gap-1"
                              >
                                {label}: {String(value)}
                                <Tooltip content={factorTooltips[key]}>
                                  <span style={{ marginLeft: 4, cursor: "pointer", display: "inline-flex", alignItems: "center" }}>
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                                      <circle cx="12" cy="12" r="10" stroke="var(--color-orange)" strokeWidth="2" fill="var(--color-bg-section)"/>
                                      <text x="12" y="16" textAnchor="middle" fontSize="13" fill="var(--color-orange)" fontWeight="bold">i</text>
                                    </svg>
                                  </span>
                                </Tooltip>
                              </span>
                            );
                          }
                        )}
                    </div>
                  </div>
                </div>
              )}

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

              {/* KPI & Info */}
              {result.kpi_by_subreddit?.[subreddit]?.global_body_kpi && (
                <div className="flex flex-col gap-4">
                  {/* Date optimale, score moyen, min/max semantic */}
                  <div className="flex flex-wrap gap-6 items-center justify-center">
                    <div className="flex flex-col items-center bg-section border border-orange rounded-xl px-5 py-4 shadow min-w-[220px]">
                      <span className="text-xs font-semibold text-gray mb-1 flex items-center gap-2 justify-center">
                        <svg className="w-5 h-5 text-orange" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" /><path d="M12 6v6l4 2" /></svg>
                        Best time to post
                      </span>
                      {renderBestTimeToPost(subreddit)}
                    </div>
                    {/* Semantic Score Min */}
                    <div className="flex flex-col items-center bg-section border border-green rounded-xl px-5 py-4 shadow min-w-[180px]">
                      <span className="text-xs font-semibold text-gray mb-1 flex items-center gap-2 justify-center">
                        <svg className="w-5 h-5 text-green" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                          <path d="M12 4v16" />
                        </svg>
                        Min Semantic Score
                      </span>
                      <span className="text-lg font-bold text-green text-center">
                        {result.kpi_by_subreddit[subreddit].global_body_kpi.scores.min_score?.toFixed(3)}
                      </span>
                    </div>
                    {/* Average Semantic Score */}
                    <div className="flex flex-col items-center bg-section border border-orange rounded-xl px-5 py-4 shadow min-w-[180px]">
                      <span className="text-xs font-semibold text-gray mb-1 flex items-center gap-2 justify-center">
                        <svg className="w-5 h-5 text-orange" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M5 12l5 5L20 7" /></svg>
                        Avg. relevance score
                      </span>
                      <span className="text-lg font-bold text-orange text-center">
                        {result.kpi_by_subreddit[subreddit].global_body_kpi.scores.average_score?.toFixed(2)}
                      </span>
                    </div>
                    {/* Semantic Score Max */}
                    <div className="flex flex-col items-center bg-section border border-yellow rounded-xl px-5 py-4 shadow min-w-[180px]">
                      <span className="text-xs font-semibold text-gray mb-1 flex items-center gap-2 justify-center">
                        <svg className="w-5 h-5 text-yellow" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
                          <path d="M12 4v16" />
                        </svg>
                        Max Semantic Score
                      </span>
                      <span className="text-lg font-bold text-yellow text-center">
                        {result.kpi_by_subreddit[subreddit].global_body_kpi.scores.max_score?.toFixed(3)}
                      </span>
                    </div>
                  </div>
                  {/* Mots les plus utilisés */}
                  <div className="flex flex-wrap gap-8">
                    <div>
                      <strong className="text-orange">Most used words in similar posts :</strong>
                      <ul className="flex flex-wrap gap-2 mt-1">
                        {result.kpi_by_subreddit[subreddit].global_body_kpi.words_and_sentences.most_used_words.map(
                          ([word, count]: [string, number]) => (
                            <li key={word} className="bg-input px-2 py-1 rounded text-light text-sm">
                              {word} <span className="text-orange">({count})</span>
                            </li>
                          )
                        )}
                      </ul>
                    </div>
                  </div>
                </div>
              )}

              {/* KPI Titres - Comparaison */}
              {result.kpi_by_subreddit?.[subreddit]?.global_title_kpi && (
                <div className="w-full bg-section rounded-xl p-4 shadow flex flex-col gap-6 border border-border">
                  <h4 className="text-lg font-bold text-orange mb-2">Title KPIs</h4>
                  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                    {[
                      { key: "average_title_length", label: "Avg. Title Length" },
                      { key: "average_title_word_count", label: "Avg. Title Word Count" },
                      { key: "average_title_question_count", label: "Avg. Questions" },
                      { key: "average_title_exclamation_count", label: "Avg. Exclamations" },
                      { key: "average_title_polarity", label: "Avg. Polarity" },
                      { key: "average_title_subjectivity", label: "Avg. Subjectivity" },
                      { key: "average_title_uppercase_word_count", label: "Avg. Uppercase Words" }
                    ].map(({ key, label }) => (
                      <div key={key} className="flex flex-col bg-card rounded-lg px-4 py-4 shadow border border-input items-center">
                        <span className="text-xs text-light font-semibold mb-2">{label}</span>
                        <div className="flex flex-row gap-2 items-end w-full justify-center">
                          <div className="flex flex-col items-center flex-1">
                            <span className="text-2xl text-orange font-extrabold leading-tight">
                              {result.kpi_by_subreddit[subreddit].global_title_kpi[key]}
                            </span>
                            <span className="text-xs text-gray">Posts</span>
                          </div>
                          <div className="flex flex-col items-center flex-1 border-l border-input pl-2">
                            <span className="text-2xl text-blue font-extrabold leading-tight">
                              {result.draft_post_kpi?.title_kpi[key]}
                            </span>
                            <span className="text-xs text-gray">Draft</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* KPI Body - Comparaison */}
              {result.kpi_by_subreddit?.[subreddit]?.global_body_kpi && (
                <div className="w-full bg-section rounded-xl p-4 shadow flex flex-col gap-6 border border-border">
                  <h4 className="text-lg font-bold text-orange mb-2">Body KPIs</h4>
                  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                    {[
                      { key: "average_word_count", label: "Avg. Word Count", section: "words_and_sentences" },
                      { key: "average_sentence_count", label: "Avg. Sentence Count", section: "words_and_sentences" },
                      { key: "average_readability_score", label: "Avg. Readability", section: "polarity_and_readability_subjectivity" },
                      { key: "average_polarity", label: "Avg. Polarity", section: "polarity_and_readability_subjectivity" },
                      { key: "average_subjectivity", label: "Avg. Subjectivity", section: "polarity_and_readability_subjectivity" },
                      { key: "average_score", label: "Avg. Score", section: "scores" },
                      { key: "average_upvotes", label: "Avg. Upvotes", section: "scores" },
                      { key: "total_posts_with_links", label: "Posts with Links", section: "links_and_time" },
                      { key: "percentage_posts_with_links", label: "Links (%)", section: "links_and_time" }
                    ].map(({ key, label, section }) => (
                      <div key={key} className="flex flex-col bg-card rounded-lg px-4 py-4 shadow border border-input items-center">
                        <span className="text-xs text-light font-semibold mb-2">{label}</span>
                        <div className="flex flex-row gap-2 items-end w-full justify-center">
                          <div className="flex flex-col items-center flex-1">
                            <span className="text-2xl text-orange font-extrabold leading-tight">
                              {result.kpi_by_subreddit[subreddit].global_body_kpi[section]?.[key]}
                            </span>
                            <span className="text-xs text-gray">Posts</span>
                          </div>
                          <div className="flex flex-col items-center flex-1 border-l border-input pl-2">
                            <span className="text-2xl text-blue font-extrabold leading-tight">
                              {result.draft_post_kpi?.body_kpi[section]?.[key]}
                            </span>
                            <span className="text-xs text-gray">Draft</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
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
                      maxHeight: showPosts[subreddit] ? "2000px" : "0px",
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
