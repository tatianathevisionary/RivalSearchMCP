import { motion } from 'framer-motion'
import { Check, Zap, Terminal, Download, Sparkles, ArrowRight } from 'lucide-react'
import { Link } from 'react-router-dom'
import CodeBlock from '../components/ui/CodeBlock'
import Callout from '../components/ui/Callout'

export default function GettingStarted() {
  const cursorConfig = `{
  "mcpServers": {
    "RivalSearchMCP": {
      "url": "https://RivalSearchMCP.fastmcp.app/mcp"
    }
  }
}`

  const claudeConfig = `{
  "mcpServers": {
    "RivalSearchMCP": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/damionrashford/RivalSearchMCP",
        "rivalsearchmcp"
      ]
    }
  }
}`

  const localInstall = `# Clone the repository
git clone https://github.com/damionrashford/RivalSearchMCP
cd RivalSearchMCP

# Install dependencies with uv
uv sync

# Run the server (stdio mode)
uv run python server.py`

  const verificationSteps = [
    { step: 'Ask your AI', text: '"Search the web for the latest AI news"' },
    { step: 'Tool called', text: 'web_search with query parameter' },
    { step: 'Results returned', text: 'Articles from DuckDuckGo, Yahoo, and Wikipedia' },
    { step: 'Success!', text: 'Your AI can now access current information' },
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
          <Zap className="w-6 h-6 text-[var(--color-rival-amber)]" />
          <span className="text-sm font-bold uppercase tracking-[0.2em] text-[var(--color-rival-amber)]">
            Installation Guide
          </span>
          <div className="flex-1 h-px bg-gradient-to-r from-[var(--color-rival-amber)]/30 to-transparent" />
        </div>

        <h1 className="text-5xl sm:text-6xl font-black tracking-tight text-[var(--color-text-primary)] mb-6 leading-tight">
          Getting Started
        </h1>

        <p className="text-xl text-[var(--color-text-muted)] leading-relaxed max-w-3xl">
          Get RivalSearchMCP running in your AI client in under 60 seconds.
          <span className="block mt-2 text-[var(--color-text-secondary)] font-semibold">
            Zero configuration. Zero API keys. Zero friction.
          </span>
        </p>
      </motion.div>

      {/* Instant setup - featured */}
      <motion.section
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.1 }}
        id="quick-start"
        className="mb-20"
      >
        <div className="relative p-10 rounded-3xl bg-gradient-to-br from-[var(--color-rival-red)]/10 via-[var(--color-surface-2)] to-[var(--color-rival-amber)]/5 border-2 border-[var(--color-rival-red)]/30 overflow-hidden">
          {/* Background glow */}
          <div className="absolute top-0 right-0 w-96 h-96 bg-[var(--color-rival-red)] rounded-full blur-[200px] opacity-[0.08]" />
          
          <div className="relative">
            <div className="flex items-start gap-4 mb-6">
              <div className="w-14 h-14 rounded-2xl bg-[var(--color-rival-red)]/20 border border-[var(--color-rival-red)]/40 flex items-center justify-center shrink-0">
                <Zap className="w-7 h-7 text-[var(--color-rival-red)]" />
              </div>
              <div>
                <span className="inline-block px-3 py-1 text-xs font-black uppercase tracking-wider text-[var(--color-rival-red)] bg-[var(--color-rival-red)]/10 rounded-full mb-3">
                  Recommended
                </span>
                <h2 className="text-3xl font-black text-[var(--color-text-primary)] mb-2">
                  Instant Setup for Cursor
                </h2>
                <p className="text-base text-[var(--color-text-muted)]">
                  One-click installation. No manual configuration needed.
                </p>
              </div>
            </div>

            <a
              href="cursor://anysphere.cursor-deeplink/mcp/install?name=RivalSearchMCP&config=eyJ1cmwiOiJodHRwczovL1JpdmFsU2VhcmNoTUNQLmZhc3RtY3AuYXBwL21jcCJ9"
              className="inline-flex items-center gap-3 px-8 py-4 text-lg font-black text-white bg-gradient-to-r from-[var(--color-rival-red)] to-[var(--color-rival-red-dark)] rounded-2xl transition-all duration-300 hover:shadow-[0_0_40px_rgba(220,38,38,0.5)] hover:scale-[1.02] mb-6"
            >
              <Zap className="w-6 h-6" />
              Open in Cursor
              <ArrowRight className="w-5 h-5" />
            </a>

            <div className="flex items-center gap-2 text-sm text-[var(--color-text-muted)]">
              <Check className="w-4 h-4 text-[var(--color-rival-green)]" />
              Installs in &lt;5 seconds • Works immediately
            </div>
          </div>
        </div>
      </motion.section>

      {/* Alternative methods */}
      <motion.section
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        id="installation"
        className="mb-20"
      >
        <h2 className="text-3xl font-black text-[var(--color-text-primary)] mb-10 flex items-center gap-3">
          <div className="w-1 h-8 bg-[var(--color-rival-red)] rounded-full" />
          Alternative Installation Methods
        </h2>

        <div className="space-y-8">
          {/* Cursor manual */}
          <div id="cursor-installation" className="scroll-mt-24">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-xl bg-blue-500/10 flex items-center justify-center">
                <Terminal className="w-5 h-5 text-blue-400" />
              </div>
              <h3 className="text-2xl font-bold text-[var(--color-text-primary)]">
                Cursor (Manual)
              </h3>
            </div>
            <p className="text-base text-[var(--color-text-muted)] mb-4 leading-relaxed">
              Add to your Cursor settings configuration file:
            </p>
            <CodeBlock code={cursorConfig} language="json" filename="settings.json" />
          </div>

          {/* Claude Desktop */}
          <div id="claude-installation" className="scroll-mt-24">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-xl bg-purple-500/10 flex items-center justify-center">
                <Download className="w-5 h-5 text-purple-400" />
              </div>
              <h3 className="text-2xl font-bold text-[var(--color-text-primary)]">
                Claude Desktop
              </h3>
            </div>
            <p className="text-base text-[var(--color-text-muted)] mb-4 leading-relaxed">
              Add to <code>claude_desktop_config.json</code>:
            </p>
            <CodeBlock code={claudeConfig} language="json" filename="claude_desktop_config.json" />
          </div>

          {/* Local Development */}
          <div id="local-installation" className="scroll-mt-24">
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-xl bg-amber-500/10 flex items-center justify-center">
                <Terminal className="w-5 h-5 text-amber-400" />
              </div>
              <h3 className="text-2xl font-bold text-[var(--color-text-primary)]">
                Local Development
              </h3>
            </div>
            <p className="text-base text-[var(--color-text-muted)] mb-4 leading-relaxed">
              For local development or self-hosting:
            </p>
            <CodeBlock code={localInstall} language="bash" filename="terminal" />
            <div className="mt-4">
              <Callout type="info" title="Requirements">
                Requires Python 3.10+ and{' '}
                <a
                  href="https://docs.astral.sh/uv/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="font-semibold"
                >
                  uv package manager
                </a>
                . The server runs in stdio mode by default for MCP compatibility.
              </Callout>
            </div>
          </div>
        </div>
      </motion.section>

      {/* Configuration */}
      <motion.section
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.3 }}
        id="configuration"
        className="mb-20"
      >
        <h2 className="text-3xl font-black text-[var(--color-text-primary)] mb-8 flex items-center gap-3">
          <div className="w-1 h-8 bg-[var(--color-rival-red)] rounded-full" />
          Configuration
        </h2>

        <Callout type="success" title="Zero Configuration Required">
          RivalSearchMCP works out of the box with <strong>no API keys or additional setup</strong> needed for all core functionality.
        </Callout>

        <div className="mt-8 p-6 rounded-2xl bg-[var(--color-surface-2)] border border-[var(--color-border-subtle)]">
          <h3 className="text-xl font-bold text-[var(--color-text-primary)] mb-4">What's Included</h3>
          <div className="grid sm:grid-cols-2 gap-4">
            {[
              { name: 'Web Search', detail: 'DuckDuckGo, Yahoo, Wikipedia' },
              { name: 'Social Search', detail: 'Reddit, HN, Dev.to, Product Hunt, Medium' },
              { name: 'News', detail: 'Google News, DDG News, Yahoo News' },
              { name: 'GitHub', detail: 'Public API (60 req/hr)' },
              { name: 'Scientific', detail: 'arXiv, Semantic Scholar, PubMed' },
              { name: 'Documents', detail: 'PDF, Word, Images with OCR' },
            ].map((item) => (
              <div key={item.name} className="flex items-start gap-3 p-4 rounded-xl bg-[var(--color-surface-3)]/50">
                <Check className="w-5 h-5 text-[var(--color-rival-green)] shrink-0 mt-0.5" />
                <div>
                  <div className="font-semibold text-[var(--color-text-primary)] mb-1">{item.name}</div>
                  <div className="text-sm text-[var(--color-text-muted)]">{item.detail}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-6">
          <Callout type="info" title="Optional: Research Agent">
            The <code>research_agent</code> tool uses AI to orchestrate multiple tools. This requires setting{' '}
            <code>OPENROUTER_API_KEY</code> as an environment variable. All other 9 tools work without any configuration.
          </Callout>
        </div>
      </motion.section>

      {/* Verification */}
      <motion.section
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.4 }}
        className="mb-20"
      >
        <h2 className="text-3xl font-black text-[var(--color-text-primary)] mb-8 flex items-center gap-3">
          <div className="w-1 h-8 bg-[var(--color-rival-red)] rounded-full" />
          Verify Installation
        </h2>

        <div className="space-y-6">
          <div className="p-6 rounded-2xl bg-[var(--color-surface-2)] border border-[var(--color-border-subtle)]">
            <h3 className="text-lg font-bold text-[var(--color-text-primary)] mb-4">
              Test Query
            </h3>
            <div className="p-5 rounded-xl bg-[var(--color-surface-3)] border border-[var(--color-border-subtle)]">
              <p className="text-base text-[var(--color-text-secondary)] font-medium italic">
                "Search the web for the latest AI developments"
              </p>
            </div>
          </div>

          <div className="p-6 rounded-2xl bg-gradient-to-br from-green-500/5 to-transparent border border-green-500/20">
            <h3 className="text-lg font-bold text-green-300 mb-5 flex items-center gap-2">
              <Check className="w-5 h-5" />
              Expected Response
            </h3>
            <div className="space-y-3">
              {verificationSteps.map((item, index) => (
                <div key={index} className="flex items-start gap-3">
                  <div className="w-6 h-6 rounded-full bg-green-500/20 border border-green-500/40 flex items-center justify-center shrink-0 mt-0.5">
                    <span className="text-xs font-bold text-green-400">{index + 1}</span>
                  </div>
                  <div>
                    <div className="text-sm font-semibold text-green-300 mb-1">{item.step}</div>
                    <div className="text-sm text-green-200/70">{item.text}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </motion.section>

      {/* Next steps */}
      <motion.section
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.5 }}
      >
        <h2 className="text-3xl font-black text-[var(--color-text-primary)] mb-8 flex items-center gap-3">
          <div className="w-1 h-8 bg-[var(--color-rival-red)] rounded-full" />
          Next Steps
        </h2>

        <div className="grid sm:grid-cols-3 gap-4">
          {[
            { title: 'Explore Tools', desc: 'Learn what each tool can do', href: '/tools', icon: Sparkles },
            { title: 'User Guide', desc: 'Understand common workflows', href: '/guide', icon: Terminal },
            { title: 'See Examples', desc: 'Real-world usage patterns', href: '/examples', icon: Download },
          ].map((item) => {
            const Icon = item.icon
            return (
              <Link
                key={item.href}
                to={item.href}
                className="group p-6 rounded-2xl bg-[var(--color-surface-2)] border border-[var(--color-border-subtle)] hover:border-[var(--color-rival-red)]/40 transition-all duration-300 hover:shadow-lg"
              >
                <Icon className="w-6 h-6 text-[var(--color-rival-red)] mb-4 group-hover:scale-110 transition-transform duration-300" />
                <h3 className="font-bold text-[var(--color-text-primary)] mb-2 group-hover:text-[var(--color-rival-red)] transition-colors duration-300">
                  {item.title}
                </h3>
                <p className="text-sm text-[var(--color-text-muted)] mb-3">
                  {item.desc}
                </p>
                <div className="flex items-center gap-2 text-sm text-[var(--color-rival-red)] font-semibold">
                  Learn more
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform duration-300" />
                </div>
              </Link>
            )
          })}
        </div>
      </motion.section>
    </div>
  )
}
