import { useState, useCallback } from "react";
import { useInView } from "../hooks/useInView";

const INSTALL_URL = "https://RivalSearchMCP.fastmcp.app/mcp";

export function CallToAction() {
  const { ref, isInView } = useInView();
  const [copied, setCopied] = useState(false);

  const handleCopy = useCallback(async () => {
    await navigator.clipboard.writeText(INSTALL_URL);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }, []);

  return (
    <section aria-label="Get started with Rival Search MCP" className="relative py-24 sm:py-32 overflow-hidden">
      {/* Background glow */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-accent/[0.03] to-transparent" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full bg-accent/[0.04] blur-[120px]" />

      <div
        ref={ref}
        className={`relative z-10 max-w-3xl mx-auto px-6 text-center transition-all duration-700 ${
          isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
        }`}
      >
        <h2 className="font-display font-extrabold text-3xl sm:text-4xl md:text-5xl text-heading tracking-tight mb-5">
          Ready to Give Your AI
          <br />
          <span className="gradient-text">Superpowers?</span>
        </h2>
        <p className="text-body font-body text-base sm:text-lg mb-10 max-w-xl mx-auto">
          One URL. Ten tools. Twenty sources. Zero configuration.
          <br />
          Start researching in seconds.
        </p>

        {/* URL copy block */}
        <div className="terminal max-w-xl mx-auto mb-8">
          <div className="flex items-center gap-3 px-5 py-4">
            <span className="text-accent font-mono text-sm shrink-0">
              URL
            </span>
            <code className="text-body font-mono text-xs sm:text-sm flex-1 overflow-x-auto whitespace-nowrap text-left">
              {INSTALL_URL}
            </code>
            <button
              onClick={handleCopy}
              className="shrink-0 text-faint hover:text-heading transition-colors p-1.5 rounded-md hover:bg-elevated"
              aria-label="Copy URL"
            >
              {copied ? (
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="text-emerald-400">
                  <polyline points="20 6 9 17 4 12" />
                </svg>
              ) : (
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <rect x="9" y="9" width="13" height="13" rx="2" />
                  <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" />
                </svg>
              )}
            </button>
          </div>
        </div>

        {/* Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <a
            href="https://github.com/damionrashford/RivalSearchMCP"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2.5 bg-accent hover:bg-accent-light text-white font-body font-semibold text-sm px-8 py-3.5 rounded-xl transition-all duration-300 hover:shadow-xl hover:shadow-accent/25 hover:scale-[1.02]"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
            </svg>
            Star on GitHub
          </a>
          <a
            href="https://github.com/damionrashford/RivalSearchMCP#readme"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2 border border-line-light text-heading font-body font-medium text-sm px-8 py-3.5 rounded-xl transition-all duration-300 hover:border-amber/30 hover:bg-amber/5"
          >
            Read Documentation
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M7 17l9.2-9.2M17 17V8H8" />
            </svg>
          </a>
        </div>
      </div>
    </section>
  );
}
