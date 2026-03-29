import React from "react";

interface AdvicesSectionProps {
  advices: string[];
}

export default function AdvicesSection({ advices }: AdvicesSectionProps) {
  if (!advices || advices.length === 0) return null;
  return (
    <div className="w-full bg-[#2d323b] rounded-xl p-4 shadow flex flex-col gap-4 border border-[#444851] mb-4">
      <h4 className="text-lg font-bold text-[#ff7849] mb-4">Advices</h4>
      <ul className="flex flex-col gap-4">
        {advices.map((advice, idx) => (
          <li key={idx} className="flex items-center">
            <span className="h-full border-l-4 border-[#ff7849] bg-[#23272f] rounded-lg flex items-center px-4 py-3 w-full shadow-sm">
              <svg className="w-5 h-5 text-[#ff7849] mr-3 flex-shrink-0" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" /></svg>
              <span className="text-base text-[#e0e2e6] font-medium leading-relaxed">{advice}</span>
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}
