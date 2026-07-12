import { useEffect, useState } from "react";

interface ParsedData {
  title?: string;
  body?: string;
}

interface RewriteModalProps {
  isOpen: boolean;
  isLoading: boolean;
  subreddit: string;
  rewriteResult: string | null;
  onClose: () => void;
  onAccept?: (result: ParsedData) => void;
}

interface ParsedResult {
  title?: string;
  body?: string;
  text?: string;
  raw: string;
}

export default function RewriteModal({
  isOpen,
  isLoading,
  subreddit,
  rewriteResult,
  onClose,
  onAccept,
}: RewriteModalProps) {
  const [displayedText, setDisplayedText] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [parsedResult, setParsedResult] = useState<ParsedResult | null>(null);

  useEffect(() => {
    if (rewriteResult && !isLoading) {
      // Try to parse as JSON
      let parsed: ParsedResult = { raw: rewriteResult };

      try {
        // First try to parse the entire result as JSON
        const parsed_obj = JSON.parse(rewriteResult);
        parsed = {
          title: parsed_obj.title || "",
          body: parsed_obj.body || "",
          raw: rewriteResult
        };
      } catch (e) {
        // If that fails, try to extract JSON from the text
        try {
          const jsonMatch = rewriteResult.match(/\{[\s\S]*\}/);
          if (jsonMatch) {
            const parsed_obj = JSON.parse(jsonMatch[0]);
            parsed = {
              title: parsed_obj.title || "",
              body: parsed_obj.body || "",
              raw: rewriteResult
            };
          } else {
            throw new Error("No JSON found");
          }
        } catch (extractError) {
          // If JSON parsing fails, treat as plain text
          parsed = { text: rewriteResult, raw: rewriteResult };
        }
      }

      setParsedResult(parsed);

      // Typewriter effect for body only
      setIsTyping(true);
      setDisplayedText("");
      let index = 0;
      const fullText = parsed.body || parsed.text || "";

      if (fullText) {
        const typeInterval = setInterval(() => {
          if (index < fullText.length) {
            setDisplayedText((prev) => prev + fullText[index]);
            index++;
          } else {
            setIsTyping(false);
            clearInterval(typeInterval);
          }
        }, 2); // Faster typewriter effect

        return () => clearInterval(typeInterval);
      } else {
        setIsTyping(false);
      }
    }
  }, [rewriteResult, isLoading]);

  if (!isOpen) return null;

  return (
    <div
      style={{
        position: "fixed",
        inset: 0,
        backgroundColor: "rgba(0, 0, 0, 0.7)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
        backdropFilter: "blur(4px)",
      }}
      onClick={onClose}
    >
      <div
        className="w-full max-w-3xl mx-4 bg-card rounded-2xl shadow-2xl border border-border"
        style={{
          maxHeight: "90vh",
          display: "flex",
          flexDirection: "column",
          animation: "slideUp 0.3s ease-out",
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-border">
          <h2 className="text-2xl font-bold text-orange">
            ✨ Rewrite Preview for <span className="text-blue">{subreddit}</span>
          </h2>
          <button
            onClick={onClose}
            className="text-gray hover:text-lightest transition-colors focus:outline-none"
            aria-label="Close modal"
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto px-6 py-6">
          {isLoading ? (
            <div className="flex flex-col items-center justify-center py-12 gap-4">
              <div className="relative w-12 h-12">
                <div
                  style={{
                    position: "absolute",
                    inset: 0,
                    borderRadius: "50%",
                    border: "3px solid var(--color-bg-input)",
                    borderTopColor: "var(--color-orange)",
                    animation: "spin 1s linear infinite",
                  }}
                />
              </div>
              <p className="text-light text-lg font-medium">
                Rewriting your post for r/{subreddit}...
              </p>
              <p className="text-gray text-sm italic">
                Our AI is analyzing your content and generating improvements
              </p>
            </div>
          ) : rewriteResult ? (
            <div className="space-y-6">
              {/* Title Section */}
              {parsedResult?.title && (
                <div className="bg-section rounded-lg p-4 border border-border">
                  <p className="text-xs font-semibold text-orange uppercase tracking-wider mb-2">
                    📌 Rewritten Title
                  </p>
                  <h3 className="text-xl font-bold text-lightest leading-tight break-words">
                    {parsedResult.title}
                  </h3>
                  <p className="text-xs text-gray mt-2">
                    {parsedResult.title.length} characters
                  </p>
                </div>
              )}

              {/* Body Section */}
              <div className="bg-section rounded-lg p-4 border border-border">
                <p className="text-xs font-semibold text-orange uppercase tracking-wider mb-2">
                  📝 Rewritten Body
                </p>
                {/* TEMP: Show without typewriter effect to debug */}
                <div
                  style={{
                    fontSize: "15px",
                    lineHeight: "1.7",
                    color: "var(--color-light)",
                    minHeight: "150px",
                    maxHeight: "400px",
                    overflowY: "auto",
                    whiteSpace: "pre-wrap",
                    wordBreak: "break-word",
                    fontFamily: "monospace",
                  }}
                  className="text-light"
                >
                  {parsedResult?.body || parsedResult?.text || "Pas de contenu"}
                </div>
                <p className="text-xs text-gray mt-2">
                  {(parsedResult?.body || parsedResult?.text || "").length} characters
                </p>
              </div>

              <div className="bg-blue/10 rounded-lg p-4 border border-blue/30">
                <p className="text-sm text-light">
                  <span className="font-semibold text-blue">💡 Tip:</span> Review
                  the rewritten content. Click "Accept" to use it, or "Copy" to
                  adjust manually before using.
                </p>
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-12">
              <svg
                className="w-12 h-12 text-gray mb-4"
                fill="none"
                stroke="currentColor"
                strokeWidth="1.5"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
              <p className="text-gray text-center">No rewrite result available</p>
            </div>
          )}
        </div>

        {/* Footer with Actions */}
        {!isLoading && rewriteResult && (
          <div className="border-t border-border px-6 py-4 flex gap-3 justify-end">
            <button
              onClick={() => {
                const textToCopy = parsedResult?.title
                  ? `${parsedResult.title}\n\n${displayedText}`
                  : displayedText;
                navigator.clipboard.writeText(textToCopy);
              }}
              className="px-4 py-2 rounded-lg bg-section hover:bg-border text-lightest font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-orange/50"
              title="Copy rewritten post to clipboard"
            >
              📋 Copy
            </button>
            <button
              onClick={onClose}
              className="px-4 py-2 rounded-lg bg-section hover:bg-border text-lightest font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-orange/50"
            >
              Close
            </button>
            {onAccept && (
              <button
                onClick={() => onAccept({
                  title: parsedResult?.title || "",
                  body: parsedResult?.body || parsedResult?.text || ""
                })}
                className="px-6 py-2 rounded-lg bg-orange hover:bg-orange-hover text-white font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-orange/50"
              >
                ✅ Accept
              </button>
            )}
          </div>
        )}

        {/* Loading Footer */}
        {isLoading && (
          <div className="border-t border-border px-6 py-4 flex justify-end">
            <button
              onClick={onClose}
              className="px-4 py-2 rounded-lg bg-section hover:bg-border text-lightest font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-orange/50"
            >
              Cancel
            </button>
          </div>
        )}
      </div>

      <style>{`
        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes spin {
          to {
            transform: rotate(360deg);
          }
        }

        @keyframes blink {
          0%, 49% {
            opacity: 1;
          }
          50%, 100% {
            opacity: 0;
          }
        }
      `}</style>
    </div>
  );
}
