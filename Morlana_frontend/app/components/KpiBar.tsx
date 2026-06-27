"use client";
import React, { useState } from "react";

interface KpiBarProps {
  label: string;
  postsValue: number | undefined;
  draftValue: number | undefined;
  min?: number;
  max?: number;
  format?: (v: number) => string;
  tooltip?: React.ReactNode;
}

function autoFormat(v: number): string {
  if (Math.abs(v) >= 1000) return Math.round(v).toLocaleString();
  if (Math.abs(v) >= 100) return Math.round(v).toString();
  if (Math.abs(v) >= 10) return v.toFixed(1);
  return v.toFixed(2);
}

function InfoTooltip({ content }: { content: React.ReactNode }) {
  const [visible, setVisible] = useState(false);
  return (
    <span
      style={{ position: "relative", display: "inline-flex", alignItems: "center", marginLeft: 5, cursor: "default" }}
      onMouseEnter={() => setVisible(true)}
      onMouseLeave={() => setVisible(false)}
    >
      <svg width="13" height="13" viewBox="0 0 13 13" fill="none" style={{ verticalAlign: "middle", flexShrink: 0, color: "var(--color-orange)" }}>
        <circle cx="6.5" cy="6.5" r="6" stroke="currentColor" strokeWidth="1.5" />
        <rect x="6" y="5.5" width="1" height="4" rx="0.5" fill="currentColor" />
        <rect x="6" y="3.5" width="1" height="1.2" rx="0.5" fill="currentColor" />
      </svg>
      {visible && (
        <div style={{
          position: "absolute",
          bottom: "calc(100% + 8px)",
          left: 0,
          background: "var(--color-bg-section, #23272f)",
          color: "var(--color-light, #e0e2e6)",
          border: "1px solid var(--color-border, #444851)",
          borderRadius: 8,
          boxShadow: "0 4px 20px rgba(0,0,0,0.3)",
          padding: "10px 14px",
          minWidth: 220,
          maxWidth: 300,
          zIndex: 200,
          fontSize: 12,
          fontWeight: 400,
          lineHeight: 1.55,
          whiteSpace: "normal",
          pointerEvents: "none",
        }}>
          {content}
        </div>
      )}
    </span>
  );
}

export default function KpiBar({
  label,
  postsValue,
  draftValue,
  min = 0,
  max,
  format = autoFormat,
  tooltip,
}: KpiBarProps) {
  if (postsValue === undefined || postsValue === null || draftValue === undefined || draftValue === null) {
    return null;
  }

  const topVal = Math.max(Math.abs(postsValue), Math.abs(draftValue));
  const effectiveMax = max !== undefined ? max : topVal * 1.35 || 1;
  const range = (effectiveMax - min) || 1;

  const toPercent = (v: number) =>
    Math.min(97, Math.max(3, ((v - min) / range) * 100));

  const postsLeft = toPercent(postsValue);
  const draftLeft = toPercent(draftValue);

  const relDiff =
    postsValue !== 0
      ? Math.abs(draftValue - postsValue) / Math.abs(postsValue)
      : draftValue === 0 ? 0 : 1;

  const gapColor =
    relDiff < 0.12 ? "#22c55e" : relDiff < 0.30 ? "#fbbf24" : "#ef4444";

  const gapLeft = Math.min(postsLeft, draftLeft);
  const gapWidth = Math.abs(postsLeft - draftLeft);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 5, padding: "10px 0" }}>
      <span style={{ display: "inline-flex", alignItems: "center" }}>
        <span
          style={{
            fontSize: 11,
            fontWeight: 600,
            color: "var(--color-gray)",
            textTransform: "uppercase",
            letterSpacing: "0.04em",
          }}
        >
          {label}
        </span>
        {tooltip && <InfoTooltip content={tooltip} />}
      </span>

      <div style={{ position: "relative", height: 22 }}>
        {/* Track */}
        <div
          style={{
            position: "absolute",
            top: "50%",
            left: 0,
            right: 0,
            height: 6,
            transform: "translateY(-50%)",
            borderRadius: 99,
            background: "var(--color-bg-input)",
          }}
        />

        {/* Gap highlight */}
        {gapWidth > 1 && (
          <div
            style={{
              position: "absolute",
              top: "50%",
              left: `${gapLeft}%`,
              width: `${gapWidth}%`,
              height: 6,
              transform: "translateY(-50%)",
              background: gapColor,
              opacity: 0.25,
              borderRadius: 99,
            }}
          />
        )}

        {/* Posts dot (orange) */}
        <div
          style={{
            position: "absolute",
            top: "50%",
            left: `${postsLeft}%`,
            width: 14,
            height: 14,
            borderRadius: "50%",
            background: "var(--color-orange)",
            transform: "translate(-50%, -50%)",
            boxShadow: "0 0 0 3px rgba(255,107,53,0.15)",
          }}
        />

        {/* Draft dot (blue) */}
        <div
          style={{
            position: "absolute",
            top: "50%",
            left: `${draftLeft}%`,
            width: 14,
            height: 14,
            borderRadius: "50%",
            background: "var(--color-blue)",
            border: "2.5px solid var(--color-bg-card)",
            transform: "translate(-50%, -50%)",
            boxSizing: "border-box",
            boxShadow: "0 0 0 3px rgba(52,152,219,0.15)",
          }}
        />
      </div>

      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          fontSize: 12,
          marginTop: 1,
        }}
      >
        <span>
          <span style={{ color: "var(--color-orange)", fontWeight: 700 }}>
            {format(postsValue)}
          </span>
          <span style={{ color: "var(--color-gray)", marginLeft: 4 }}>Posts</span>
        </span>
        <span>
          <span style={{ color: "var(--color-blue)", fontWeight: 700 }}>
            {format(draftValue)}
          </span>
          <span style={{ color: "var(--color-gray)", marginLeft: 4 }}>Draft</span>
        </span>
      </div>
    </div>
  );
}
