import { useInView } from "../hooks/useInView";

interface Step {
  number: string;
  title: string;
  description: string;
  code: string;
  language: string;
}

const STEPS: Step[] = [
  {
    number: "01",
    title: "One URL. That's It.",
    description:
      "No API keys. No tokens. No authentication. Add the remote MCP server URL and all 10 tools are instantly available.",
    code: "https://RivalSearchMCP.fastmcp.app/mcp",
    language: "url",
  },
  {
    number: "02",
    title: "Configure Your Client",
    description:
      "Works with Claude Desktop, Cursor, VS Code, and Claude Code. Add to your MCP configuration in seconds.",
    code: `{
  "mcpServers": {
    "RivalSearchMCP": {
      "url": "https://RivalSearchMCP.fastmcp.app/mcp"
    }
  }
}`,
    language: "json",
  },
  {
    number: "03",
    title: "Research Anything",
    description:
      "Your AI can now search the web, analyze content, crawl sites, read documents, and generate comprehensive research reports.",
    code: `"Research the latest AI agent frameworks,
compare GitHub activity and community sentiment,
and find relevant papers on arXiv."`,
    language: "prompt",
  },
];

function StepCard({ step, index }: { step: Step; index: number }) {
  const { ref, isInView } = useInView();

  return (
    <div
      ref={ref}
      className={`relative transition-all duration-700 ${
        isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
      }`}
      style={{ transitionDelay: `${index * 200}ms` }}
    >
      {/* Step number */}
      <div className="font-display font-extrabold text-6xl sm:text-7xl text-line tracking-tighter mb-4 select-none">
        {step.number}
      </div>

      {/* Content */}
      <h3 className="font-display font-bold text-xl sm:text-2xl text-heading mb-3">
        {step.title}
      </h3>
      <p className="text-body font-body text-sm leading-relaxed mb-5 max-w-md">
        {step.description}
      </p>

      {/* Code block */}
      <div className="terminal">
        <div className="terminal-header">
          <div className="terminal-dot bg-accent/50" />
          <div className="terminal-dot bg-amber/50" />
          <div className="terminal-dot bg-emerald-500/50" />
          <span className="text-faint font-mono text-[10px] ml-2">
            {step.language}
          </span>
        </div>
        <pre className="px-5 py-4 overflow-x-auto">
          <code className="text-body font-mono text-xs sm:text-sm leading-relaxed">
            {step.code}
          </code>
        </pre>
      </div>

      {/* Connector line (not on last step) */}
      {index < STEPS.length - 1 && (
        <div className="hidden md:block absolute -right-3 top-1/2 w-6 border-t border-dashed border-line-light" />
      )}
    </div>
  );
}

export function HowItWorks() {
  const { ref, isInView } = useInView();

  return (
    <section id="how-it-works" aria-label="Installation steps" className="relative py-24 sm:py-32 section-glow-amber">
      <div className="max-w-7xl mx-auto px-6">
        {/* Section header */}
        <div
          ref={ref}
          className={`text-center mb-16 transition-all duration-700 ${
            isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"
          }`}
        >
          <span className="font-mono text-xs text-amber tracking-widest uppercase">
            Setup
          </span>
          <h2 className="font-display font-extrabold text-3xl sm:text-4xl md:text-5xl text-heading tracking-tight mt-3 mb-4">
            Three Steps. Zero Friction.
          </h2>
          <p className="text-body font-body text-base sm:text-lg max-w-2xl mx-auto">
            From zero to fully-equipped AI researcher in under a minute.
          </p>
        </div>

        {/* Steps grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 md:gap-8">
          {STEPS.map((step, i) => (
            <StepCard key={step.number} step={step} index={i} />
          ))}
        </div>
      </div>
    </section>
  );
}
