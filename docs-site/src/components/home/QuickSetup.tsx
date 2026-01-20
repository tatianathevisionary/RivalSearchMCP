import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Check, Copy, Download, Terminal, Zap } from 'lucide-react'
import CodeBlock from '../ui/CodeBlock'

type TabId = 'instant' | 'claude' | 'local'

const setupMethods = [
  { 
    id: 'instant' as TabId, 
    name: 'Instant Setup',
    icon: Zap,
    badge: 'Fastest',
    badgeColor: '#dc2626'
  },
  { 
    id: 'claude' as TabId, 
    name: 'Claude Desktop',
    icon: Download,
    badge: null,
    badgeColor: null 
  },
  { 
    id: 'local' as TabId, 
    name: 'Local Dev',
    icon: Terminal,
    badge: 'Advanced',
    badgeColor: '#f59e0b'
  },
]

const codeSnippets: Record<TabId, { code: string; language: string; filename?: string }> = {
  instant: {
    code: `{
  "mcpServers": {
    "RivalSearchMCP": {
      "url": "https://RivalSearchMCP.fastmcp.app/mcp"
    }
  }
}`,
    language: 'json',
    filename: 'cursor-settings.json',
  },
  claude: {
    code: `{
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
}`,
    language: 'json',
    filename: 'claude_desktop_config.json',
  },
  local: {
    code: `# Clone the repository
git clone https://github.com/damionrashford/RivalSearchMCP
cd RivalSearchMCP

# Install with uv
uv sync

# Run the server
uv run python server.py`,
    language: 'bash',
    filename: 'terminal',
  },
}

export default function QuickSetup() {
  const [activeTab, setActiveTab] = useState<TabId>('instant')
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    await navigator.clipboard.writeText(codeSnippets[activeTab].code)
    setCopied(true)
    setTimeout(() => setCopied(false), 2500)
  }

  return (
    <section className="relative py-32 overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-[var(--color-surface-0)]" />
      
      <div className="relative max-w-6xl mx-auto px-6 sm:px-8 lg:px-12">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <div className="flex items-center justify-center gap-4 mb-6">
            <div className="flex-1 h-px bg-gradient-to-r from-transparent to-[var(--color-rival-green)]/30" />
            <div className="flex items-center gap-2">
              <Check className="w-5 h-5 text-[var(--color-rival-green)]" />
              <span className="text-sm font-bold uppercase tracking-[0.2em] text-[var(--color-rival-green)]">
                Quick Start
              </span>
            </div>
            <div className="flex-1 h-px bg-gradient-to-l from-transparent to-[var(--color-rival-green)]/30" />
          </div>

          <h2 className="text-5xl sm:text-6xl font-black tracking-tight text-[var(--color-text-primary)] mb-6">
            Set Up in <span className="text-[var(--color-rival-red)]">60 Seconds</span>
          </h2>

          <p className="text-xl text-[var(--color-text-muted)] max-w-2xl mx-auto">
            Choose your preferred installation method and start searching.
          </p>
        </motion.div>

        {/* Setup card */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.1 }}
          viewport={{ once: true }}
          className="relative rounded-3xl overflow-hidden border border-[var(--color-border-subtle)] bg-gradient-to-br from-[var(--color-surface-2)] to-[var(--color-surface-3)]"
        >
          {/* Tab navigation - card style */}
          <div className="p-6 sm:p-8 border-b border-[var(--color-border-subtle)]/50">
            <div className="grid grid-cols-3 gap-3">
              {setupMethods.map((method) => {
                const Icon = method.icon
                const isActive = activeTab === method.id
                
                return (
                  <button
                    key={method.id}
                    onClick={() => setActiveTab(method.id)}
                    className={`
                      relative p-4 sm:p-5 rounded-xl transition-all duration-300
                      ${isActive 
                        ? 'bg-[var(--color-surface-3)] border-2 border-[var(--color-rival-red)]/40 shadow-[0_0_20px_rgba(220,38,38,0.15)]' 
                        : 'bg-[var(--color-surface-2)]/50 border border-[var(--color-border-subtle)] hover:border-[var(--color-border-default)] hover:bg-[var(--color-surface-3)]/50'
                      }
                    `}
                  >
                    <div className="flex flex-col items-center gap-2 text-center">
                      <Icon className={`w-6 h-6 ${isActive ? 'text-[var(--color-rival-red)]' : 'text-[var(--color-text-muted)]'} transition-colors duration-300`} />
                      <span className={`text-sm sm:text-base font-bold ${isActive ? 'text-[var(--color-text-primary)]' : 'text-[var(--color-text-muted)]'} transition-colors duration-300`}>
                        {method.name}
                      </span>
                      {method.badge && (
                        <span 
                          className="text-[10px] font-black uppercase tracking-wider px-2 py-0.5 rounded-full"
                          style={{ 
                            backgroundColor: `${method.badgeColor}15`,
                            color: method.badgeColor 
                          }}
                        >
                          {method.badge}
                        </span>
                      )}
                    </div>

                    {/* Active indicator */}
                    {isActive && (
                      <motion.div
                        layoutId="active-tab-indicator"
                        className="absolute inset-0 rounded-xl border-2 border-[var(--color-rival-red)]/60"
                        transition={{ type: 'spring', bounce: 0.2, duration: 0.5 }}
                      />
                    )}
                  </button>
                )
              })}
            </div>
          </div>

          {/* Content area */}
          <div className="p-6 sm:p-8">
            <AnimatePresence mode="wait">
              <motion.div
                key={activeTab}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
              >
                {/* Instant setup - special treatment */}
                {activeTab === 'instant' && (
                  <div className="space-y-6">
                    <div className="p-6 rounded-2xl bg-gradient-to-br from-[var(--color-rival-red)]/10 to-[var(--color-rival-amber)]/5 border border-[var(--color-rival-red)]/20">
                      <div className="flex items-start gap-4 mb-4">
                        <div className="w-12 h-12 rounded-xl bg-[var(--color-rival-red)]/20 flex items-center justify-center shrink-0">
                          <Zap className="w-6 h-6 text-[var(--color-rival-red)]" />
                        </div>
                        <div>
                          <h4 className="text-lg font-bold text-[var(--color-text-primary)] mb-1">
                            One-Click Installation
                          </h4>
                          <p className="text-sm text-[var(--color-text-muted)]">
                            Instantly add RivalSearchMCP to Cursor. No manual configuration needed.
                          </p>
                        </div>
                      </div>
                      
                      <a
                        href="cursor://anysphere.cursor-deeplink/mcp/install?name=RivalSearchMCP&config=eyJ1cmwiOiJodHRwczovL1JpdmFsU2VhcmNoTUNQLmZhc3RtY3AuYXBwL21jcCJ9"
                        className="w-full inline-flex items-center justify-center gap-3 px-6 py-4 text-base font-bold text-white bg-gradient-to-r from-[var(--color-rival-red)] to-[var(--color-rival-red-dark)] rounded-xl transition-all duration-300 hover:shadow-[0_0_40px_rgba(220,38,38,0.4)] hover:scale-[1.01]"
                      >
                        <Zap className="w-5 h-5" />
                        Open in Cursor
                      </a>
                    </div>

                    <div className="relative">
                      <div className="absolute inset-0 flex items-center">
                        <div className="w-full border-t border-[var(--color-border-subtle)]" />
                      </div>
                      <div className="relative flex justify-center text-sm">
                        <span className="px-4 bg-[var(--color-surface-2)] text-[var(--color-text-dim)] uppercase tracking-wider text-xs font-bold">
                          Or add manually
                        </span>
                      </div>
                    </div>
                  </div>
                )}

                {/* Code block */}
                <div className="mt-6">
                  <CodeBlock
                    code={codeSnippets[activeTab].code}
                    language={codeSnippets[activeTab].language}
                    filename={codeSnippets[activeTab].filename}
                  />
                </div>

                {/* Instructions */}
                {activeTab === 'local' && (
                  <div className="mt-6 p-5 rounded-xl bg-[var(--color-surface-3)] border border-[var(--color-border-subtle)]">
                    <div className="flex items-start gap-3">
                      <Terminal className="w-5 h-5 text-[var(--color-rival-amber)] shrink-0 mt-0.5" />
                      <div>
                        <p className="text-sm text-[var(--color-text-secondary)] leading-relaxed">
                          <strong className="text-[var(--color-rival-amber)]">Requirements:</strong>{' '}
                          Python 3.10+ and{' '}
                          <a
                            href="https://docs.astral.sh/uv/"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-[var(--color-rival-red)] hover:underline font-medium"
                          >
                            uv package manager
                          </a>
                          . The server runs in stdio mode by default for MCP compatibility.
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              </motion.div>
            </AnimatePresence>
          </div>

          {/* Footer bar */}
          <div className="px-6 sm:px-8 py-5 bg-[var(--color-surface-3)]/50 border-t border-[var(--color-border-subtle)]/50 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-green-500/10">
                <Check className="w-5 h-5 text-[var(--color-rival-green)]" />
              </div>
              <span className="text-sm font-semibold text-[var(--color-text-secondary)]">
                No API keys required • Works immediately
              </span>
            </div>
            
            <button
              onClick={handleCopy}
              className="inline-flex items-center gap-2 px-4 py-2 text-sm font-semibold bg-[var(--color-surface-2)] hover:bg-[var(--color-surface-4)] border border-[var(--color-border-subtle)] hover:border-[var(--color-border-default)] rounded-lg transition-all duration-200"
            >
              {copied ? (
                <>
                  <Check className="w-4 h-4 text-[var(--color-rival-green)]" />
                  <span className="text-[var(--color-rival-green)]">Copied!</span>
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4 text-[var(--color-text-muted)]" />
                  <span className="text-[var(--color-text-secondary)]">Copy Code</span>
                </>
              )}
            </button>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
