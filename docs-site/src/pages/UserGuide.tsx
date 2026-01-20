import { motion } from 'framer-motion'
import { ArrowRight, BookOpen, Lightbulb, Sparkles } from 'lucide-react'
import { Link } from 'react-router-dom'
import Callout from '../components/ui/Callout'

export default function UserGuide() {
  const workflows = [
    {
      title: 'Quick Research',
      steps: ['web_search → Find sources', 'content_operations → Extract content', 'social_search → Check discussions'],
      time: '2-3 min',
      color: '#3b82f6',
    },
    {
      title: 'Deep Dive',
      steps: ['research_agent → AI orchestrates all tools', 'Generates 4000-6000+ char report', 'Cites all sources'],
      time: '5-8 min',
      color: '#dc2626',
    },
    {
      title: 'Academic',
      steps: ['scientific_research → Find papers', 'document_analysis → Analyze PDFs', 'research_agent → Synthesize findings'],
      time: '10-15 min',
      color: '#22c55e',
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
          <BookOpen className="w-6 h-6 text-[var(--color-rival-amber)]" />
          <span className="text-sm font-bold uppercase tracking-[0.2em] text-[var(--color-rival-amber)]">
            Comprehensive Guide
          </span>
          <div className="flex-1 h-px bg-gradient-to-r from-[var(--color-rival-amber)]/30 to-transparent" />
        </div>

        <h1 className="text-5xl sm:text-6xl font-black tracking-tight text-[var(--color-text-primary)] mb-6 leading-tight">
          User Guide
        </h1>

        <p className="text-xl text-[var(--color-text-muted)] leading-relaxed max-w-3xl">
          Master RivalSearchMCP with proven workflows, best practices, and pro tips.
        </p>
      </motion.div>

      {/* Overview */}
      <motion.section
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
        id="overview"
        className="mb-20"
      >
        <h2 className="text-3xl font-black text-[var(--color-text-primary)] mb-8 flex items-center gap-3">
          <div className="w-1 h-8 bg-[var(--color-rival-red)] rounded-full" />
          Overview
        </h2>

        <div className="p-8 rounded-2xl bg-[var(--color-surface-2)] border border-[var(--color-border-subtle)] mb-8">
          <p className="text-lg text-[var(--color-text-secondary)] leading-relaxed mb-6">
            RivalSearchMCP provides <strong className="text-[var(--color-text-primary)]">10 specialized tools</strong> organized into three categories:
          </p>

          <div className="grid gap-5">
            {[
              { 
                title: 'Search & Discovery', 
                tools: ['web_search', 'social_search', 'news_aggregation', 'github_search', 'scientific_research'],
                desc: 'Find information across web, social, news, GitHub, and academic sources'
              },
              { 
                title: 'Content Analysis', 
                tools: ['content_operations', 'map_website', 'document_analysis'],
                desc: 'Extract, analyze, and process content from URLs and documents'
              },
              { 
                title: 'AI-Powered Research', 
                tools: ['research_topic', 'research_agent'],
                desc: 'Automated research workflows with AI orchestration'
              },
            ].map((category) => (
              <div key={category.title} className="p-5 rounded-xl bg-[var(--color-surface-3)]/50 border border-[var(--color-border-subtle)]">
                <h4 className="font-bold text-[var(--color-rival-red)] mb-2">{category.title}</h4>
                <p className="text-sm text-[var(--color-text-muted)] mb-3">{category.desc}</p>
                <div className="flex flex-wrap gap-2">
                  {category.tools.map(tool => (
                    <code key={tool} className="text-xs font-mono bg-[var(--color-surface-4)] px-2 py-1 rounded text-[var(--color-rival-amber)]">
                      {tool}
                    </code>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>

        <Callout type="tip" title="Smart Tool Hints">
          Every tool response includes "Next Steps" suggestions, guiding you to the logical next tool in your workflow.
        </Callout>
      </motion.section>

      {/* Common Workflows */}
      <motion.section
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        id="research-workflows"
        className="mb-20"
      >
        <h2 className="text-3xl font-black text-[var(--color-text-primary)] mb-8 flex items-center gap-3">
          <div className="w-1 h-8 bg-[var(--color-rival-red)] rounded-full" />
          Common Workflows
        </h2>

        <div className="grid gap-6 mb-10">
          {workflows.map((workflow) => (
            <div
              key={workflow.title}
              className="relative p-6 sm:p-8 rounded-2xl bg-[var(--color-surface-2)] border border-[var(--color-border-subtle)] hover:border-[var(--color-border-default)] transition-all duration-300 overflow-hidden group"
            >
              {/* Accent bar */}
              <div className="absolute left-0 top-0 bottom-0 w-1 rounded-l-2xl" style={{ background: workflow.color }} />
              
              <div className="flex flex-col sm:flex-row sm:items-start gap-6">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-4">
                    <h3 className="text-2xl font-bold text-[var(--color-text-primary)]">
                      {workflow.title}
                    </h3>
                    <span 
                      className="px-3 py-1 text-xs font-black uppercase tracking-wider rounded-full"
                      style={{ 
                        backgroundColor: `${workflow.color}15`,
                        color: workflow.color
                      }}
                    >
                      {workflow.time}
                    </span>
                  </div>

                  <div className="space-y-2.5">
                    {workflow.steps.map((step, stepIndex) => (
                      <div key={stepIndex} className="flex items-start gap-3">
                        <div 
                          className="w-6 h-6 rounded-lg flex items-center justify-center shrink-0 font-bold text-xs mt-0.5"
                          style={{ 
                            backgroundColor: `${workflow.color}20`,
                            color: workflow.color
                          }}
                        >
                          {stepIndex + 1}
                        </div>
                        <p className="text-sm text-[var(--color-text-muted)] leading-relaxed pt-1">
                          {step}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </motion.section>

      {/* Web Search section */}
      <motion.section
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.3 }}
        id="web-search"
        className="mb-20"
      >
        <h2 className="text-3xl font-black text-[var(--color-text-primary)] mb-8 flex items-center gap-3">
          <div className="w-1 h-8 bg-[var(--color-rival-red)] rounded-full" />
          Web Search Mastery
        </h2>

        <div className="space-y-8">
          <div>
            <h3 className="text-xl font-bold text-[var(--color-text-primary)] mb-4">
              Basic Search
            </h3>
            <div className="p-5 rounded-xl bg-[var(--color-surface-2)] border border-[var(--color-border-subtle)] mb-4">
              <p className="text-base text-[var(--color-text-secondary)] italic font-medium">
                "Search the web for React server components best practices"
              </p>
            </div>
            <p className="text-base text-[var(--color-text-muted)] leading-relaxed">
              The AI automatically uses <code>web_search</code> to query all 3 engines concurrently.
            </p>
          </div>

          <div>
            <h3 className="text-xl font-bold text-[var(--color-text-primary)] mb-4">
              Pro Tips for Better Results
            </h3>
            <div className="grid sm:grid-cols-2 gap-4">
              {[
                { tip: 'Be Specific', example: '"Python web scraping BeautifulSoup" vs "web scraping"' },
                { tip: 'Add Context', example: '"AI news 2024" to get recent content' },
                { tip: 'Use Quotes', example: 'Exact phrase matching with "quoted text"' },
                { tip: 'Combine Tools', example: 'Search → Extract → Analyze workflow' },
              ].map((item) => (
                <div key={item.tip} className="p-4 rounded-xl bg-[var(--color-surface-3)]/50">
                  <div className="font-bold text-[var(--color-rival-amber)] mb-2 text-sm">{item.tip}</div>
                  <div className="text-sm text-[var(--color-text-muted)]">{item.example}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </motion.section>

      {/* Content Extraction */}
      <motion.section
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.4 }}
        id="content-extraction"
        className="mb-20"
      >
        <h2 className="text-3xl font-black text-[var(--color-text-primary)] mb-8 flex items-center gap-3">
          <div className="w-1 h-8 bg-[var(--color-rival-red)] rounded-full" />
          Content Extraction
        </h2>

        <Callout type="tip" title="Two-Step Workflow">
          First use <code>web_search</code> to find URLs, then <code>content_operations</code> to extract full content.
        </Callout>

        <div className="mt-8 p-6 rounded-2xl bg-[var(--color-surface-2)] border border-[var(--color-border-subtle)]">
          <h3 className="text-lg font-bold text-[var(--color-text-primary)] mb-6">Typical Flow</h3>
          <div className="space-y-5">
            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-lg bg-blue-500/10 flex items-center justify-center shrink-0 font-bold text-sm text-blue-400">
                1
              </div>
              <div>
                <div className="font-semibold text-[var(--color-text-primary)] mb-1">Search</div>
                <div className="p-4 rounded-lg bg-[var(--color-surface-3)] border border-[var(--color-border-subtle)] mb-2">
                  <p className="text-sm text-[var(--color-text-secondary)] italic">
                    "Search for FastAPI async tutorial"
                  </p>
                </div>
                <p className="text-sm text-[var(--color-text-muted)]">Returns URLs from 3 engines</p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-lg bg-amber-500/10 flex items-center justify-center shrink-0 font-bold text-sm text-amber-400">
                2
              </div>
              <div>
                <div className="font-semibold text-[var(--color-text-primary)] mb-1">Extract</div>
                <div className="p-4 rounded-lg bg-[var(--color-surface-3)] border border-[var(--color-border-subtle)] mb-2">
                  <p className="text-sm text-[var(--color-text-secondary)] italic">
                    "Get the content from https://fastapi.tiangolo.com/async/"
                  </p>
                </div>
                <p className="text-sm text-[var(--color-text-muted)]">Retrieves full page as clean markdown</p>
              </div>
            </div>

            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-lg bg-green-500/10 flex items-center justify-center shrink-0 font-bold text-sm text-green-400">
                ✓
              </div>
              <div>
                <div className="font-semibold text-[var(--color-text-primary)] mb-1">Result</div>
                <p className="text-sm text-[var(--color-text-muted)]">
                  AI now has full tutorial content and can answer questions
                </p>
              </div>
            </div>
          </div>
        </div>
      </motion.section>

      {/* Research with Agent */}
      <motion.section
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.5 }}
        className="mb-20"
      >
        <h2 className="text-3xl font-black text-[var(--color-text-primary)] mb-8 flex items-center gap-3">
          <div className="w-1 h-8 bg-[var(--color-rival-red)] rounded-full" />
          AI-Powered Research
        </h2>

        <div className="p-8 rounded-2xl bg-gradient-to-br from-[var(--color-rival-red)]/5 via-[var(--color-surface-2)] to-[var(--color-rival-amber)]/5 border border-[var(--color-rival-red)]/20 mb-6">
          <div className="flex items-start gap-4 mb-6">
            <div className="w-12 h-12 rounded-2xl bg-[var(--color-rival-red)]/20 flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-[var(--color-rival-red)]" />
            </div>
            <div>
              <h3 className="text-2xl font-bold text-[var(--color-text-primary)] mb-2">
                research_agent
              </h3>
              <p className="text-base text-[var(--color-text-muted)] leading-relaxed">
                The most powerful tool — AI orchestrates all other tools to generate comprehensive 4000-6000+ character reports.
              </p>
            </div>
          </div>

          <div className="p-5 rounded-xl bg-[var(--color-surface-3)]/80 border border-[var(--color-border-subtle)] mb-4">
            <p className="text-base text-[var(--color-text-secondary)] italic font-medium">
              "Research the current state of quantum computing using all available sources and create a detailed report"
            </p>
          </div>

          <div className="flex items-start gap-3">
            <Lightbulb className="w-5 h-5 text-[var(--color-rival-amber)] shrink-0 mt-0.5" />
            <p className="text-sm text-[var(--color-text-muted)] leading-relaxed">
              The agent will search web, social media, news, GitHub, and academic databases, then synthesize findings with citations.
            </p>
          </div>
        </div>

        <Callout type="info" title="API Key Required">
          The research agent requires <code>OPENROUTER_API_KEY</code> to power AI orchestration. All other 9 tools work without any API keys.
        </Callout>
      </motion.section>

      {/* Continue Learning */}
      <motion.section
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.6 }}
      >
        <h2 className="text-3xl font-black text-[var(--color-text-primary)] mb-8 flex items-center gap-3">
          <div className="w-1 h-8 bg-[var(--color-rival-red)] rounded-full" />
          Continue Learning
        </h2>

        <div className="grid sm:grid-cols-2 gap-4">
          <Link
            to="/tools"
            className="group p-6 rounded-2xl bg-[var(--color-surface-2)] border border-[var(--color-border-subtle)] hover:border-[var(--color-rival-red)]/40 transition-all duration-300 hover:shadow-lg"
          >
            <h3 className="font-bold text-[var(--color-text-primary)] mb-2 group-hover:text-[var(--color-rival-red)] transition-colors duration-300">
              Tool Reference
            </h3>
            <p className="text-sm text-[var(--color-text-muted)] mb-4">
              Detailed documentation for all 10 tools
            </p>
            <div className="flex items-center gap-2 text-sm text-[var(--color-rival-red)] font-semibold">
              Explore tools
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-300" />
            </div>
          </Link>

          <Link
            to="/examples"
            className="group p-6 rounded-2xl bg-[var(--color-surface-2)] border border-[var(--color-border-subtle)] hover:border-[var(--color-rival-red)]/40 transition-all duration-300 hover:shadow-lg"
          >
            <h3 className="font-bold text-[var(--color-text-primary)] mb-2 group-hover:text-[var(--color-rival-red)] transition-colors duration-300">
              Real Examples
            </h3>
            <p className="text-sm text-[var(--color-text-muted)] mb-4">
              See RivalSearchMCP in action
            </p>
            <div className="flex items-center gap-2 text-sm text-[var(--color-rival-red)] font-semibold">
              View examples
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-300" />
            </div>
          </Link>
        </div>
      </motion.section>
    </div>
  )
}
