"use client";
import React from "react";

interface ScoreGaugeProps {
  score: number;
  label: string;
  color: string;
}

export default function ScoreGauge({ score, label, color }: ScoreGaugeProps) {
  const cx = 110, cy = 108, r = 85;

  function pt(pct: number) {
    const a = (1 - pct / 100) * Math.PI;
    return { x: cx + r * Math.cos(a), y: cy - r * Math.sin(a) };
  }

  function arc(from: number, to: number): string {
    const s = pt(from), e = pt(to);
    return `M ${s.x.toFixed(2)} ${s.y.toFixed(2)} A ${r} ${r} 0 0 1 ${e.x.toFixed(2)} ${e.y.toFixed(2)}`;
  }

  const zones = [
    { from: 0, to: 45, color: "#ef4444" },
    { from: 45, to: 65, color: "#fbbf24" },
    { from: 65, to: 85, color: "#2563eb" },
    { from: 85, to: 100, color: "#22c55e" },
  ];

  const clamped = Math.min(Math.max(score, 0.01), 99.99);

  return (
    <svg viewBox="0 0 220 120" style={{ width: "100%", maxWidth: 260, display: "block" }}>
      {/* Dim zone arcs as background context */}
      {zones.map((z) => (
        <path
          key={z.from}
          d={arc(z.from, z.to)}
          fill="none"
          stroke={z.color}
          strokeWidth="14"
          strokeLinecap="round"
          opacity="0.18"
        />
      ))}

      {/* Score fill arc */}
      {score > 0 && (
        <path
          d={arc(0, clamped)}
          fill="none"
          stroke={color}
          strokeWidth="14"
          strokeLinecap="round"
        />
      )}

      {/* Threshold dots at 45, 65, 85 */}
      {[45, 65, 85].map((t) => {
        const { x, y } = pt(t);
        return (
          <circle
            key={t}
            cx={x.toFixed(2)}
            cy={y.toFixed(2)}
            r="3.5"
            fill="var(--color-bg-card, #2d323b)"
            stroke="#444851"
            strokeWidth="1.5"
          />
        );
      })}

      {/* Score value */}
      <text
        x={cx}
        y={cy - 20}
        textAnchor="middle"
        fontSize="34"
        fontWeight="800"
        fill={color}
        fontFamily="system-ui,sans-serif"
      >
        {score.toFixed(1)}
      </text>

      {/* Label */}
      <text
        x={cx}
        y={cy + 4}
        textAnchor="middle"
        fontSize="13"
        fontWeight="600"
        fill={color}
        fontFamily="system-ui,sans-serif"
      >
        {label}
      </text>

      {/* Scale labels */}
      <text x="22" y="118" textAnchor="middle" fontSize="9" fill="#6b7280" fontFamily="system-ui,sans-serif">0</text>
      <text x="198" y="118" textAnchor="middle" fontSize="9" fill="#6b7280" fontFamily="system-ui,sans-serif">100</text>
    </svg>
  );
}
