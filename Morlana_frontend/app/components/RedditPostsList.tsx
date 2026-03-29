import React from "react";
import RedditPostCard from "./RedditPostCard";

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

interface RedditPostsListProps {
  posts: RedditPost[];
}

export default function RedditPostsList({ posts }: RedditPostsListProps) {
  if (!Array.isArray(posts) || posts.length === 0) return null;
  return (
    <div className="w-full flex flex-col gap-4 mt-2">
      <h4 className="text-lg font-bold text-[#ff7849] mb-2">Similar posts</h4>
      {posts.map((post) => (
        <RedditPostCard key={post.id} post={post} />
      ))}
    </div>
  );
}
