import { useState, useCallback } from "react";
import { useInView } from "../hooks/useInView";

interface FAQItem {
  question: string;
  answer: string;
}

const FAQS: FAQItem[] = [
  {
    question: "What is Rival Search MCP?",
    answer:
      "Rival Search MCP is an open-source Model Context Protocol (MCP) server that gives AI assistants like Claude, Cursor, and VS Code real-time web research capabilities. It provides 10 specialized tools that search across 20+ data sources including web search engines, social media, news, academic databases, and GitHub — all with zero API keys required.",
  },
  {
    question: "Does Rival Search MCP require API keys?",
    answer:
      "No. Rival Search MCP requires zero API keys, tokens, or authentication for all 10 tools. You only need to add one URL to your MCP client to get started immediately. An optional OpenRouter API key can be added to enable the autonomous AI research agent.",
  },
  {
    question: "How do I install Rival Search MCP?",
    answer:
      'Add the remote server URL (https://RivalSearchMCP.fastmcp.app/mcp) to your MCP client configuration. For Claude Code, run: claude mcp add RivalSearchMCP --url https://RivalSearchMCP.fastmcp.app/mcp. No local installation, cloning, or Python setup required.',
  },
  {
    question: "What AI clients does Rival Search MCP work with?",
    answer:
      "Rival Search MCP works with Claude Desktop, Cursor, VS Code, Claude Code, and any MCP-compatible AI client. Setup takes seconds — just add the remote server URL to your client's MCP configuration.",
  },
  {
    question: "Is Rival Search MCP free and open source?",
    answer:
      "Yes. Rival Search MCP is completely free and open-source under the MIT License. You can use the hosted remote server at no cost, or clone the repository and self-host it on your own infrastructure.",
  },
  {
    question: "What data sources does Rival Search MCP access?",
    answer:
      "Rival Search MCP accesses 20+ data sources: DuckDuckGo, Yahoo, Wikipedia, Reddit, Hacker News, Dev.to, ProductHunt, Medium, Google News RSS, DuckDuckGo News, Yahoo News, GitHub, arXiv, Semantic Scholar, Kaggle, HuggingFace, and any URL for content extraction and document analysis with OCR.",
  },
];

function FAQAccordion({ faq, index }: { faq: FAQItem; index: number }) {
  const [open, setOpen] = useState(false);
  const { ref, isInView } = useInView();

  const toggle = useCallback(() => setOpen((prev) => !prev), []);

  return (
    <div
      ref={ref}
      className={`border border-line rounded-xl overflow-hidden transition-all duration-700 ${
        isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"
      } ${open ? "bg-panel border-line-light" : "bg-transparent hover:bg-panel/50"}`}
      style={{ transitionDelay: `${index * 80}ms` }}
    >
      <button
        onClick={toggle}
        className="w-full flex items-center justify-between gap-4 px-6 py-5 text-left cursor-pointer"
        aria-expanded={open}
      >
        <h3 className="font-body font-semibold text-heading text-sm sm:text-base pr-4">
          {faq.question}
        </h3>
        <span
          className={`shrink-0 w-5 h-5 flex items-center justify-center text-dim transition-transform duration-300 ${
            open ? "rotate-45" : ""
          }`}
          aria-hidden="true"
        >
          <svg
            width="14"
            height="14"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
          >
            <line x1="12" y1="5" x2="12" y2="19" />
            <line x1="5" y1="12" x2="19" y2="12" />
          </svg>
        </span>
      </button>
      <div
        className={`overflow-hidden transition-all duration-300 ${
          open ? "max-h-96 pb-5" : "max-h-0"
        }`}
      >
        <p className="px-6 text-body font-body text-sm leading-relaxed">
          {faq.answer}
        </p>
      </div>
    </div>
  );
}

export function FAQ() {
  const { ref, isInView } = useInView();

  return (
    <section id="faq" aria-label="Frequently asked questions" className="relative py-24 sm:py-32">
      <div className="max-w-3xl mx-auto px-6">
        {/* Section header */}
        <div
          ref={ref}
          className={`text-center mb-12 transition-all duration-700 ${
            isInView ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"
          }`}
        >
          <span className="font-mono text-xs text-amber tracking-widest uppercase">
            FAQ
          </span>
          <h2 className="font-display font-extrabold text-3xl sm:text-4xl text-heading tracking-tight mt-3 mb-4">
            Common Questions
          </h2>
          <p className="text-body font-body text-base sm:text-lg">
            Everything you need to know about Rival Search MCP.
          </p>
        </div>

        {/* FAQ items */}
        <div className="flex flex-col gap-3">
          {FAQS.map((faq, i) => (
            <FAQAccordion key={faq.question} faq={faq} index={i} />
          ))}
        </div>
      </div>
    </section>
  );
}
