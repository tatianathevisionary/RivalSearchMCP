import { useState, useCallback } from "react";
import { useTypewriter } from "../hooks/useTypewriter";

const ROTATING_WORDS = [
  "Deep Research",
  "Competitor Analysis",
  "Market Intelligence",
  "Academic Research",
  "OSINT",
];

const INSTALL_CMD =
  "claude mcp add RivalSearchMCP --url https://RivalSearchMCP.fastmcp.app/mcp";

export function Hero() {
  const rotatingText = useTypewriter(ROTATING_WORDS);
  const [copied, setCopied] = useState(false);

  const handleCopy = useCallback(async () => {
    await navigator.clipboard.writeText(INSTALL_CMD);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }, []);

  return (
    <section aria-label="Rival Search MCP overview" className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background layers */}
      <div className="absolute inset-0 hero-glow" />
      <div className="absolute inset-0 dot-grid opacity-60" />

      {/* Decorative accent line */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[400px] h-px bg-gradient-to-r from-transparent via-accent/40 to-transparent" />

      {/* Content */}
      <div className="relative z-10 max-w-5xl mx-auto px-6 pt-24 pb-16 text-center">
        {/* Badge */}
        <div
          className="inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full border border-line-light bg-surface/60 mb-10 opacity-0 animate-fade-in"
          style={{ animationDelay: "100ms" }}
        >
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse-glow" />
          <span className="text-dim font-mono text-xs tracking-wide">
            Open Source &middot; MIT License &middot; 39 Stars
          </span>
        </div>

        {/* Headline */}
        <h1 className="font-display font-extrabold tracking-tight leading-[1.05] mb-6">
          <span
            className="block text-4xl sm:text-5xl md:text-6xl lg:text-7xl text-heading opacity-0 animate-fade-in-up"
            style={{ animationDelay: "200ms" }}
          >
            Give Your AI
          </span>
          <span
            className="block text-4xl sm:text-5xl md:text-6xl lg:text-7xl text-heading opacity-0 animate-fade-in-up"
            style={{ animationDelay: "350ms" }}
          >
            Real-Time Web
          </span>
          <span
            className="block text-4xl sm:text-5xl md:text-6xl lg:text-7xl gradient-text opacity-0 animate-fade-in-up"
            style={{ animationDelay: "500ms" }}
          >
            Intelligence
          </span>
        </h1>

        {/* Subtitle */}
        <p
          className="text-body font-body text-base sm:text-lg max-w-2xl mx-auto mb-4 leading-relaxed opacity-0 animate-fade-in-up"
          style={{ animationDelay: "650ms" }}
        >
          10 specialized research tools. 20+ data sources.
          <br className="hidden sm:block" />
          Zero API keys required. One URL to install.
        </p>

        {/* Rotating text */}
        <div
          className="h-8 flex items-center justify-center mb-10 opacity-0 animate-fade-in"
          style={{ animationDelay: "800ms" }}
        >
          <span className="text-dim font-mono text-xs tracking-widest uppercase">
            Powering:{" "}
          </span>
          <span className="text-amber font-mono text-xs tracking-widest uppercase ml-2">
            {rotatingText}
          </span>
          <span className="w-0.5 h-4 bg-amber ml-0.5 animate-blink" />
        </div>

        {/* Terminal install block */}
        <div
          className="terminal max-w-2xl mx-auto mb-8 opacity-0 animate-fade-in-up"
          style={{ animationDelay: "900ms" }}
        >
          <div className="terminal-header">
            <div className="terminal-dot bg-accent/70" />
            <div className="terminal-dot bg-amber/70" />
            <div className="terminal-dot bg-emerald-500/70" />
            <span className="text-faint font-mono text-[11px] ml-2">
              Terminal
            </span>
          </div>
          <div className="flex items-center gap-3 px-5 py-4">
            <span className="text-amber font-mono text-sm shrink-0">$</span>
            <code className="text-body font-mono text-xs sm:text-sm flex-1 overflow-x-auto whitespace-nowrap text-left scrollbar-none">
              {INSTALL_CMD}
            </code>
            <button
              onClick={handleCopy}
              className="shrink-0 text-faint hover:text-heading transition-colors p-1.5 rounded-md hover:bg-elevated"
              aria-label="Copy command"
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

        {/* CTA Buttons */}
        <div
          className="flex flex-col sm:flex-row items-center justify-center gap-4 opacity-0 animate-fade-in-up"
          style={{ animationDelay: "1050ms" }}
        >
          <a
            href="https://github.com/damionrashford/RivalSearchMCP"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-2.5 bg-heading text-base font-body font-semibold text-sm px-7 py-3 rounded-xl transition-all duration-300 hover:bg-white hover:shadow-xl hover:shadow-white/10 hover:scale-[1.02]"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
            </svg>
            View on GitHub
          </a>
          <a
            href="#how-it-works"
            className="flex items-center gap-2 border border-line-light text-heading font-body font-medium text-sm px-7 py-3 rounded-xl transition-all duration-300 hover:border-accent/40 hover:bg-accent/5 hover:shadow-lg hover:shadow-accent/5"
          >
            Quick Setup
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M7 17l9.2-9.2M17 17V8H8" />
            </svg>
          </a>
        </div>

        {/* Scroll indicator */}
        <div
          className="mt-16 opacity-0 animate-fade-in animate-float"
          style={{ animationDelay: "1400ms" }}
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" className="text-faint mx-auto">
            <path d="M12 5v14M19 12l-7 7-7-7" />
          </svg>
        </div>
      </div>
    </section>
  );
}
