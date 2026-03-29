import React from "react";

interface WordsToAddSectionProps {
  words: string[];
}

export default function WordsToAddSection({ words }: WordsToAddSectionProps) {
  if (!words || words.length === 0) return null;
  return (
    <div className="w-full bg-[#23272f] rounded-xl p-4 shadow flex flex-col gap-2 border border-[#444851] mb-4">
      <h4 className="text-lg font-bold text-[#ff7849] mb-2">Words to add</h4>
      <div className="flex flex-wrap gap-2">
        {words.map((word, idx) => (
          <span key={idx} className="bg-[#353a43] text-[#ff7849] px-3 py-1 rounded-full text-xs font-semibold border border-[#444851]">{word}</span>
        ))}
      </div>
    </div>
  );
}
