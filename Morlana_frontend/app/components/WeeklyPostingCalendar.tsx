"use client";

interface CalendarDay {
  day: string;
  dayIndex: number;
  engagementScore: number;
  isBestDay: boolean;
  bestHour: number | null;
  avgUpvotes: number;
  avgComments: number;
  rawEngagementScore: number;
}

interface CalendarData {
  calendar: CalendarDay[];
  bestDay: string;
  averageEngagement: {
    upvotes: number;
    comments: number;
  };
}

interface WeeklyPostingCalendarProps {
  data: CalendarData;
}

function getEngagementColor(score: number): string {
  if (score >= 1.0) return "var(--color-success)";
  if (score >= 0.8) return "var(--color-primary)";
  if (score >= 0.6) return "var(--color-orange)";
  if (score >= 0.4) return "var(--color-warning)";
  return "var(--color-danger)";
}

function getEngagementLabel(score: number): string {
  if (score >= 1.0) return "Optimal";
  if (score >= 0.8) return "Excellent";
  if (score >= 0.6) return "Good";
  if (score >= 0.4) return "Fair";
  return "Poor";
}

export default function WeeklyPostingCalendar({
  data,
}: WeeklyPostingCalendarProps) {
  const abbreviations: { [key: string]: string } = {
    Monday: "Mon",
    Tuesday: "Tue",
    Wednesday: "Wed",
    Thursday: "Thu",
    Friday: "Fri",
    Saturday: "Sat",
    Sunday: "Sun",
  };

  return (
    <div className="w-full bg-section rounded-xl px-5 py-4 shadow border border-border">
      <div className="flex items-center gap-3 mb-4">
        <h4 className="text-base font-bold text-orange">Weekly Posting Calendar</h4>
        <span className="flex items-center gap-1 text-xs text-gray">
          <svg
            className="w-4 h-4 text-orange"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            viewBox="0 0 24 24"
          >
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
            <path d="M16 2v4M8 2v4M3 10h18" />
          </svg>
          Optimal days highlighted
        </span>
      </div>

      {/* Calendar Grid */}
      <div className="grid grid-cols-7 gap-2 mb-6">
        {data.calendar.map((day: CalendarDay) => {
          const bgColor = getEngagementColor(day.engagementScore);
          const label = getEngagementLabel(day.engagementScore);

          return (
            <div
              key={day.dayIndex}
              className="flex flex-col items-center rounded-lg p-3 transition-all hover:scale-105 cursor-default"
              style={{
                background: bgColor + (day.isBestDay ? "33" : "18"),
                border: day.isBestDay ? `2px solid ${bgColor}` : `1px solid ${bgColor}33`,
              }}
            >
              {/* Day name */}
              <span className="text-xs font-semibold text-gray uppercase mb-1">
                {abbreviations[day.day]}
              </span>

              {/* Star icon for best day */}
              {day.isBestDay && (
                <span className="text-lg mb-1">⭐</span>
              )}

              {/* Best hour */}
              {day.bestHour !== null && (
                <div className="text-xs font-semibold text-light mb-1">
                  {String(day.bestHour).padStart(2, '0')}:00
                </div>
              )}

              {/* Engagement score */}
              <div className="text-center mb-2">
                <div
                  className="text-sm font-bold"
                  style={{ color: bgColor }}
                >
                  {(day.engagementScore * 100).toFixed(0)}%
                </div>
                <div
                  className="text-xs font-medium mt-0.5"
                  style={{ color: bgColor, opacity: 0.8 }}
                >
                  {label}
                </div>
              </div>

              {/* Quick stats */}
              <div className="text-xs text-gray text-center space-y-0.5">
                <div>↑ {day.avgUpvotes.toFixed(0)}</div>
                <div>💬 {day.avgComments.toFixed(0)}</div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Legend and stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-border">
        {/* Legend */}
        <div className="flex flex-col gap-2">
          <span className="text-xs font-semibold text-gray uppercase mb-1">Engagement Scale</span>
          <div className="flex flex-wrap gap-2">
            {[
              { label: "Optimal", score: 1.0 },
              { label: "Excellent", score: 0.8 },
              { label: "Good", score: 0.6 },
              { label: "Fair", score: 0.4 },
              { label: "Poor", score: 0.2 },
            ].map((item) => (
              <div key={item.label} className="flex items-center gap-2">
                <div
                  className="w-3 h-3 rounded"
                  style={{ background: getEngagementColor(item.score) }}
                />
                <span className="text-xs text-light">{item.label}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Engagement stats */}
        <div className="flex flex-col gap-2">
          <span className="text-xs font-semibold text-gray uppercase mb-1">
            Average Engagement
          </span>
          <div className="flex gap-4">
            <div>
              <span className="text-xs text-gray">Upvotes</span>
              <div className="text-lg font-bold text-orange">
                {data.averageEngagement.upvotes.toFixed(0)}
              </div>
            </div>
            <div>
              <span className="text-xs text-gray">Comments</span>
              <div className="text-lg font-bold text-orange">
                {data.averageEngagement.comments.toFixed(0)}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
