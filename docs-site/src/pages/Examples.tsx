import { motion } from 'framer-motion'
import { Code2, Terminal, Sparkles, FileCode } from 'lucide-react'
import CodeBlock from '../components/ui/CodeBlock'
import Callout from '../components/ui/Callout'

type UseCase = {
  title: string
  query: string
  response?: string
  workflow?: string
}

export default function Examples() {
  const examples: Array<{
    category: string
    icon: typeof Terminal
    color: string
    cases: UseCase[]
  }> = [
    {
      category: 'Basic Usage',
      icon: Terminal,
      color: '#3b82f6',
      cases: [
        {
          title: 'Simple Web Search',
          query: 'Search the web for the best JavaScript frameworks in 2026',
          response: 'Found 27 results across DuckDuckGo, Yahoo, and Wikipedia. Top results include React, Vue, Svelte...',
        },
        {
          title: 'Content Extraction',
          query: 'Get the full content from https://docs.python.org/3/tutorial/classes.html',
          response: 'Extracted 15,432 characters. The page covers Python classes including inheritance, private variables...',
        },
      ]
    },
    {
      category: 'Advanced Research',
      icon: Sparkles,
      color: '#dc2626',
      cases: [
        {
          title: 'Multi-Source Technology Research',
          query: 'Research microservices architecture — search web, check social discussions, find GitHub projects, and academic papers',
          workflow: `// AI orchestrates multiple tools:

1. web_search("microservices architecture best practices 2026")
   → 30 results from 3 engines

2. social_search("microservices", platforms=["reddit", "hackernews"])
   → Community discussions and sentiment

3. github_search("microservices template", sort="stars")
   → Top 10 repository implementations

4. scientific_research("microservices patterns")
   → Academic papers from arXiv, Semantic Scholar

Result: Comprehensive analysis with citations`,
        },
      ]
    },
    {
      category: 'Document Analysis',
      icon: FileCode,
      color: '#22c55e',
      cases: [
        {
          title: 'PDF Research Paper',
          query: 'Analyze this research paper and summarize key findings: https://arxiv.org/pdf/2312.12345.pdf',
          response: 'Document analyzed (23 pages, 45,321 characters). Uses OCR for scanned pages. Key findings: ...',
        },
      ]
    },
  ]

  return (
    <div className="max-w-4xl">
      {/* Hero header */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="mb-16"
      >
        <div className="flex items-center gap-4 mb-6">
          <Code2 className="w-6 h-6 text-[var(--color-rival-amber)]" />
          <span className="text-sm font-bold uppercase tracking-[0.2em] text-[var(--color-rival-amber)]">
            Real-World Examples
          </span>
          <div className="flex-1 h-px bg-gradient-to-r from-[var(--color-rival-amber)]/30 to-transparent" />
        </div>

        <h1 className="text-5xl sm:text-6xl font-black tracking-tight text-[var(--color-text-primary)] mb-6 leading-tight">
          Examples
        </h1>

        <p className="text-xl text-[var(--color-text-muted)] leading-relaxed max-w-3xl">
          See RivalSearchMCP in action with real-world use cases and workflows.
        </p>
      </motion.div>

      {/* Example categories */}
      <div className="space-y-16">
        {examples.map((category, categoryIndex) => {
          const Icon = category.icon
          
          return (
            <motion.section
              key={category.category}
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 + categoryIndex * 0.1 }}
              id={category.category.toLowerCase().replace(/\s+/g, '-')}
            >
              {/* Category header */}
              <div className="flex items-center gap-4 mb-8">
                <div 
                  className="w-12 h-12 rounded-2xl flex items-center justify-center"
                  style={{ backgroundColor: `${category.color}15`, border: `2px solid ${category.color}30` }}
                >
                  <Icon className="w-6 h-6" style={{ color: category.color }} />
                </div>
                <h2 className="text-3xl font-black text-[var(--color-text-primary)]">
                  {category.category}
                </h2>
              </div>

              {/* Use cases */}
              <div className="space-y-8">
                {category.cases.map((useCase, index) => (
                  <div
                    key={index}
                    className="p-6 sm:p-8 rounded-2xl bg-[var(--color-surface-2)] border border-[var(--color-border-subtle)] hover:border-[var(--color-border-default)] transition-all duration-300"
                  >
                    <h3 className="text-xl font-bold text-[var(--color-text-primary)] mb-6">
                      {useCase.title}
                    </h3>

                    {/* User query */}
                    <div className="mb-5">
                      <div className="text-sm font-bold text-[var(--color-text-dim)] uppercase tracking-wider mb-2">
                        You
                      </div>
                      <div className="p-5 rounded-xl bg-[var(--color-surface-3)] border border-[var(--color-border-subtle)]">
                        <p className="text-base text-[var(--color-text-secondary)] italic leading-relaxed">
                          "{useCase.query}"
                        </p>
                      </div>
                    </div>

                    {/* Workflow or Response */}
                    {useCase.workflow ? (
                      <div>
                        <div className="text-sm font-bold text-[var(--color-text-dim)] uppercase tracking-wider mb-2">
                          Workflow
                        </div>
                        <CodeBlock 
                          code={useCase.workflow} 
                          language="javascript" 
                          filename="orchestration.js"
                        />
                      </div>
                    ) : (
                      <div>
                        <div className="text-sm font-bold text-[var(--color-text-dim)] uppercase tracking-wider mb-2">
                          AI Response
                        </div>
                        <div className="p-5 rounded-xl bg-green-500/5 border border-green-500/20">
                          <p className="text-base text-[var(--color-text-secondary)] leading-relaxed">
                            {useCase.response}
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </motion.section>
          )
        })}
      </div>

      {/* Advanced Research Agent */}
      <motion.section
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.4 }}
        className="mt-20 mb-16"
      >
        <div className="p-10 rounded-3xl bg-gradient-to-br from-[var(--color-surface-2)] via-[var(--color-surface-3)] to-[var(--color-surface-2)] border-2 border-[var(--color-rival-red)]/30 overflow-hidden relative">
          <div className="absolute top-0 right-0 w-80 h-80 bg-[var(--color-rival-red)] rounded-full blur-[180px] opacity-[0.08]" />
          
          <div className="relative">
            <div className="flex items-center gap-3 mb-6">
              <Sparkles className="w-8 h-8 text-[var(--color-rival-red)]" />
              <h2 className="text-3xl font-black text-[var(--color-text-primary)]">
                Research Agent in Action
              </h2>
            </div>

            <div className="space-y-6">
              <div className="p-5 rounded-xl bg-[var(--color-surface-3)]/80">
                <p className="text-sm font-bold text-[var(--color-text-dim)] uppercase tracking-wider mb-2">Query</p>
                <p className="text-base text-[var(--color-text-secondary)] italic">
                  "Use the research agent to analyze the current state of large language models with depth=3"
                </p>
              </div>

              <CodeBlock
                code={`// The agent orchestrates:
{
  "tools_called": [
    "web_search",
    "social_search", 
    "news_aggregation",
    "github_search",
    "scientific_research"
  ],
  "sources_queried": 20+,
  "report_length": "6,247 characters",
  "sections": [
    "Executive Summary",
    "Current Developments",
    "Community Sentiment", 
    "Technical Implementations",
    "Academic Research",
    "Conclusions"
  ],
  "citations": 47
}`}
                language="json"
                filename="research_agent_output.json"
              />

              <Callout type="warning" title="API Key Required">
                Requires <code>OPENROUTER_API_KEY</code> environment variable.
              </Callout>
            </div>
          </div>
        </div>
      </motion.section>
    </div>
  )
}
