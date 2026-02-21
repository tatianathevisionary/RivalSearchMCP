import { useInView } from "../hooks/useInView";

interface Tool {
  name: string;
  label: string;
  desc: string;
  sources: string[];
}

interface Category {
  title: string;
  subtitle: string;
  accentClass: string;
  hoverClass: string;
  dotClass: string;
  tools: Tool[];
}

const CATEGORIES: Category[] = [
  {
    title: "Search Intelligence",
    subtitle: "Multi-source web discovery",
    accentClass: "text-amber",
    hoverClass: "card-hover card-hover-amber",
    dotClass: "bg-amber",
    tools: [
      {
        name: "web_search",
        label: "Web Search",
        desc: "Multi-engine search across DuckDuckGo, Yahoo & Wikipedia with automatic fallbacks",
        sources: ["DuckDuckGo", "Yahoo", "Wikipedia"],
      },
      {
        name: "social_search",
        label: "Social Search",
        desc: "Search Reddit, Hacker News, Dev.to, ProductHunt & Medium without auth",
        sources: ["Reddit", "HN", "Dev.to", "ProductHunt", "Medium"],
      },
      {
        name: "news_aggregation",
        label: "News Aggregation",
        desc: "Real-time news from Google News RSS, DuckDuckGo News & Yahoo News",
        sources: ["Google News", "DDG News", "Yahoo News"],
      },
      {
        name: "github_search",
        label: "GitHub Search",
        desc: "Search GitHub public repositories with rate-limited API access",
        sources: ["GitHub API"],
      },
      {
        name: "map_website",
        label: "Website Mapper",
        desc: "Intelligent website crawling with research, documentation & mapping modes",
        sources: ["Any URL"],
      },
    ],
  },
  {
    title: "Content Analysis",
    subtitle: "Deep content extraction",
    accentClass: "text-accent",
    hoverClass: "card-hover card-hover-red",
    dotClass: "bg-accent",
    tools: [
      {
        name: "content_operations",
        label: "Content Ops",
        desc: "Retrieve, stream, analyze & extract content from any URL with 5-tier fallback",
        sources: ["Any URL"],
      },
      {
        name: "research_topic",
        label: "Research Topic",
        desc: "End-to-end research workflow with source discovery & key finding extraction",
        sources: ["Multi-source"],
      },
      {
        name: "document_analysis",
        label: "Document Analysis",
        desc: "Extract text from PDF, Word, Text & Images with EasyOCR support",
        sources: ["PDF", "Word", "OCR"],
      },
    ],
  },
  {
    title: "Deep Research",
    subtitle: "AI-powered automation",
    accentClass: "gradient-text-subtle",
    hoverClass: "card-hover card-hover-gradient",
    dotClass: "bg-gradient-to-r from-accent to-amber",
    tools: [
      {
        name: "scientific_research",
        label: "Scientific Research",
        desc: "Academic paper search via arXiv & Semantic Scholar; dataset discovery via Kaggle & HuggingFace",
        sources: ["arXiv", "Semantic Scholar", "Kaggle", "HuggingFace"],
      },
      {
        name: "research_agent",
        label: "Research Agent",
        desc: "Autonomous AI agent with 7 internal tools generating comprehensive structured reports",
        sources: ["AI-Powered", "Autonomous"],
      },
    ],
  },
];

function CategoryColumn({ category, index }: { category: Category; index: number }) {
  const { ref, isInView } = useInView();

  return (
    <div
      ref={ref}
      className={`transition-all duration-700 ${
        isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
      }`}
      style={{ transitionDelay: `${index * 150}ms` }}
    >
      {/* Category header */}
      <div className="mb-6">
        <div className="flex items-center gap-2.5 mb-1.5">
          <div className={`w-2 h-2 rounded-full ${category.dotClass}`} />
          <h3 className={`font-display font-bold text-lg ${category.accentClass}`}>
            {category.title}
          </h3>
        </div>
        <p className="text-dim font-body text-sm pl-[18px]">
          {category.subtitle}
        </p>
      </div>

      {/* Tool cards */}
      <div className="flex flex-col gap-3">
        {category.tools.map((tool) => (
          <div
            key={tool.name}
            className={`${category.hoverClass} bg-panel border border-line rounded-xl p-5 cursor-default`}
          >
            <div className="flex items-start justify-between gap-3 mb-2">
              <h4 className="font-body font-semibold text-heading text-sm">
                {tool.label}
              </h4>
              <code className="text-faint font-mono text-[10px] shrink-0 bg-surface px-2 py-0.5 rounded-md">
                {tool.name}
              </code>
            </div>
            <p className="text-body font-body text-xs leading-relaxed mb-3">
              {tool.desc}
            </p>
            <div className="flex flex-wrap gap-1.5">
              {tool.sources.map((source) => (
                <span
                  key={source}
                  className="text-dim font-mono text-[10px] bg-surface border border-line px-2 py-0.5 rounded-md"
                >
                  {source}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export function Features() {
  const { ref, isInView } = useInView();

  return (
    <section id="features" aria-label="Research tools and capabilities" className="relative py-24 sm:py-32 section-glow-red">
      <div className="max-w-7xl mx-auto px-6">
        {/* Section header */}
        <div
          ref={ref}
          className={`text-center mb-16 transition-all duration-700 ${
            isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"
          }`}
        >
          <span className="font-mono text-xs text-accent tracking-widest uppercase">
            Capabilities
          </span>
          <h2 className="font-display font-extrabold text-3xl sm:text-4xl md:text-5xl text-heading tracking-tight mt-3 mb-4">
            10 Research Tools
          </h2>
          <p className="text-body font-body text-base sm:text-lg max-w-2xl mx-auto">
            Three categories of specialized tools that transform your AI
            assistant into a web-capable research engine.
          </p>
        </div>

        {/* Category columns */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 md:gap-6">
          {CATEGORIES.map((cat, i) => (
            <CategoryColumn key={cat.title} category={cat} index={i} />
          ))}
        </div>

        {/* Production callout */}
        <div className="mt-16 text-center">
          <div className="inline-flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-faint font-mono text-[11px] tracking-wide">
            {[
              "6-Layer Middleware",
              "Token-Bucket Rate Limiting",
              "Dual-Backend Cache",
              "Injection Prevention",
              "Performance Monitoring",
            ].map((item) => (
              <span key={item} className="flex items-center gap-1.5">
                <span className="w-1 h-1 rounded-full bg-faint" />
                {item}
              </span>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
