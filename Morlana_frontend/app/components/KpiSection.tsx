import React from "react";

type KpiFormat = (v: any, kpi?: any) => React.ReactNode;

const kpiList: Array<{
  key: string;
  label: string;
  icon: React.ReactNode;
  format: KpiFormat;
}> = [
  {
    key: "average_word_count",
    label: "Avg. Words",
    icon: (
      <svg className="w-5 h-5 text-[#ff7849]" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M4 17h16M4 12h16M4 7h16" /></svg>
    ),
    format: (v) => Math.round(v),
  },
  {
    key: "median_word_count",
    label: "Median Words",
    icon: (
      <svg className="w-5 h-5 text-[#ff7849]" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" /><path d="M12 8v4l3 3" /></svg>
    ),
    format: (v) => v,
  },
  {
    key: "average_score",
    label: "Avg. Score",
    icon: (
      <svg className="w-5 h-5 text-[#ff7849]" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M5 12l5 5L20 7" /></svg>
    ),
    format: (v) => v.toFixed(2),
  },
  {
    key: "median_score",
    label: "Median Score",
    icon: (
      <svg className="w-5 h-5 text-[#ff7849]" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M5 12l5 5L20 7" /></svg>
    ),
    format: (v) => v.toFixed(2),
  },
  {
    key: "average_upvotes",
    label: "Avg. Upvotes",
    icon: (
      <svg className="w-5 h-5 text-[#ff7849]" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M12 4v16m8-8H4" /></svg>
    ),
    format: (v) => Math.round(v),
  },
  {
    key: "median_upvotes",
    label: "Median Upvotes",
    icon: (
      <svg className="w-5 h-5 text-[#ff7849]" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M12 4v16m8-8H4" /></svg>
    ),
    format: (v) => v,
  },
  {
    key: "average_readability_score",
    label: "Avg. Readability",
    icon: (
      <svg className="w-5 h-5 text-[#ff7849]" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="2" /></svg>
    ),
    format: (v) => v.toFixed(1),
  },
  {
    key: "average_polarity",
    label: "Avg. Polarity",
    icon: (
      <svg className="w-5 h-5 text-[#ff7849]" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M12 20l9-5-9-5-9 5 9 5z" /></svg>
    ),
    format: (v) => v.toFixed(2),
  },
  {
    key: "average_subjectivity",
    label: "Avg. Subjectivity",
    icon: (
      <svg className="w-5 h-5 text-[#ff7849]" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" /></svg>
    ),
    format: (v) => v.toFixed(2),
  },
  {
    key: "total_posts_with_links",
    label: "Posts with links",
    icon: (
      <svg className="w-5 h-5 text-[#ff7849]" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 1 7 7l-1.5 1.5a5 5 0 0 1-7-7" /></svg>
    ),
    format: (v, kpi) => `${v} (${kpi.percentage_posts_with_links?.toFixed(0) || 0}%)`,
  },
  {
    key: "optimal_date_to_post",
    label: "Best time to post",
    icon: (
      <svg className="w-5 h-5 text-[#ff7849]" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" /><path d="M12 6v6l4 2" /></svg>
    ),
    format: (v) => v,
  },
];

interface KpiSectionProps {
  kpi: Record<string, any>;
}

export default function KpiSection({ kpi }: KpiSectionProps) {
  return (
    <div className="w-full bg-[#23272f] rounded-xl p-4 shadow flex flex-col gap-4 border border-[#444851] mb-4">
      <h4 className="text-lg font-bold text-[#ff7849] mb-4">Key Performance Indicators</h4>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {kpiList.map(({ key, label, icon, format }) =>
          kpi[key] !== undefined && (
            <div key={key} className="flex items-center gap-3 bg-[#2d323b] rounded-lg px-4 py-3 shadow border border-[#353a43]">
              {icon}
              <div className="flex flex-col">
                <span className="text-2xl text-[#ff7849] font-extrabold leading-tight">
                  {typeof format === "function" ? format(kpi[key], kpi) : kpi[key]}
                </span>
                <span className="text-xs text-[#e0e2e6] font-semibold">{label}</span>
              </div>
            </div>
          )
        )}
      </div>
    </div>
  );
}
