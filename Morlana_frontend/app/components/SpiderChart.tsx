"use client";
import React from "react";
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
  Tooltip,
} from "recharts";

const FACTOR_LABELS: Record<string, string> = {
  "F_Titre": "Title",
  "F_Lisibilité": "Readability",
  "F_Longueur": "Substance",
  "F_Sémantique": "Relevance",
  "F_Lexical": "Vocabulary",
};

interface SpiderChartProps {
  factors: Record<string, number>;
  color: string;
}

interface TooltipPayloadItem {
  value?: number;
  stroke?: string;
  payload?: { subject?: string };
}

function ChartTooltip({
  active,
  payload,
}: {
  active?: boolean;
  payload?: TooltipPayloadItem[];
}) {
  if (!active || !payload?.length) return null;
  const item = payload[0];
  return (
    <div
      style={{
        background: "var(--color-bg-section, #23272f)",
        border: "1px solid var(--color-border, #444851)",
        borderRadius: 8,
        padding: "6px 12px",
        fontSize: 13,
      }}
    >
      <span style={{ color: "var(--color-light, #e0e2e6)", fontWeight: 500 }}>
        {item.payload?.subject}:{" "}
      </span>
      <span style={{ color: item.stroke, fontWeight: 700 }}>
        {item.value}/10
      </span>
    </div>
  );
}

export default function SpiderChart({ factors, color }: SpiderChartProps) {
  const data = Object.entries(factors).map(([key, value]) => ({
    subject: FACTOR_LABELS[key] ?? key,
    value: Math.round(Math.min(10, value > 1 ? value : value * 10)),
    fullMark: 10,
  }));

  return (
    <ResponsiveContainer width="100%" height={240}>
      <RadarChart outerRadius="62%" data={data}>
        <PolarGrid stroke="#444851" strokeDasharray="3 3" />
        <PolarRadiusAxis domain={[0, 10]} tick={false} axisLine={false} />
        <PolarAngleAxis
          dataKey="subject"
          tick={{ fill: "#bcbfc4", fontSize: 12, fontWeight: 500 }}
        />
        <Radar
          dataKey="value"
          stroke={color}
          fill={color}
          fillOpacity={0.18}
          strokeWidth={2}
        />
        <Tooltip content={<ChartTooltip />} />
      </RadarChart>
    </ResponsiveContainer>
  );
}
