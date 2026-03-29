import React from "react";

interface RedditPost {
  id?: string | number;
  url: string;
  title: string;
  author?: string;
  subreddit?: string;
  text?: string;
  score?: number;
  nb_upvote?: number;
  nb_comment?: number;
  date?: number;
}

interface RedditPostCardProps {
  post: RedditPost;
}

export default function RedditPostCard({ post }: RedditPostCardProps) {
  return (
    <div className="reddit-post-card w-full bg-[#23272f] border border-[#444851] rounded-2xl shadow p-4 flex flex-col gap-2 mb-4">
      <div className="reddit-post-header flex flex-col md:flex-row md:items-center md:justify-between gap-1 mb-2">
        <a
          href={post.url}
          target="_blank"
          rel="noopener noreferrer"
          className="reddit-post-title text-lg md:text-xl font-bold text-[#ff7849] hover:underline"
        >
          {post.title}
        </a>
        <span className="reddit-post-author text-xs text-[#bcbfc4] md:ml-2">
          par {post.author || "[unknown]"} • r/{post.subreddit}
        </span>
      </div>
      <div className="reddit-post-body text-[#e0e2e6] text-sm mb-2">
        {post.text && post.text.length > 0
          ? post.text.slice(0, 180) + (post.text.length > 180 ? "..." : "")
          : <span className="italic text-[#bcbfc4]">(Pas de texte)</span>}
      </div>
      <div className="reddit-post-footer flex flex-wrap items-center gap-4 text-xs text-[#bcbfc4] mt-2">
        <span className="reddit-post-score bg-[#353a43] rounded px-2 py-1 text-[#ff7849] font-semibold">Score: {post.score?.toFixed(3)}</span>
        <span className="reddit-post-upvotes">⬆️ {post.nb_upvote}</span>
        <span className="reddit-post-comments">💬 {post.nb_comment}</span>
        <span className="reddit-post-date ml-auto md:ml-0">{post.date ? new Date(post.date * 1000).toLocaleDateString() : ""}</span>
      </div>
    </div>
  );
}
