import { Github, Twitter, ExternalLink, ArrowUpRight } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function Footer() {
  const quickLinks = [
    { name: 'Getting Started', href: '/getting-started' },
    { name: 'Tools Reference', href: '/tools' },
    { name: 'User Guide', href: '/guide' },
    { name: 'Examples', href: '/examples' },
  ]

  const resources = [
    { name: 'GitHub', href: 'https://github.com/damionrashford/RivalSearchMCP', external: true },
    { name: 'FastMCP', href: 'https://gofastmcp.com', external: true },
    { name: 'MCP Protocol', href: 'https://modelcontextprotocol.io', external: true },
  ]

  return (
    <footer className="relative border-t border-[var(--color-border-subtle)] bg-gradient-to-b from-[var(--color-surface-1)] to-[var(--color-surface-0)] overflow-hidden">
      {/* Subtle background glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[400px] bg-[var(--color-rival-red)] rounded-full blur-[200px] opacity-[0.02]" />
      
      <div className="relative mx-auto max-w-7xl px-6 sm:px-8 lg:px-12 py-16 sm:py-20">
        {/* Top section - Brand and Newsletter */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 lg:gap-16 pb-12 border-b border-[var(--color-border-subtle)]">
          {/* Brand column */}
          <div>
            <Link to="/" className="inline-flex items-center gap-3 mb-6 group">
              <div className="relative">
                <div className="w-11 h-11 rounded-xl bg-[var(--color-surface-3)] border border-[var(--color-border-subtle)] flex items-center justify-center group-hover:border-[var(--color-rival-red)]/40 transition-all duration-300">
                  <svg viewBox="0 0 24 24" className="w-5 h-5">
                    <circle cx="10" cy="10" r="5" fill="none" stroke="var(--color-rival-red)" strokeWidth="2.5"/>
                    <line x1="13.5" y1="13.5" x2="20" y2="20" stroke="var(--color-rival-red)" strokeWidth="2.5" strokeLinecap="round"/>
                    <circle cx="10" cy="10" r="1.8" fill="var(--color-rival-amber)"/>
                  </svg>
                </div>
              </div>
              <div className="flex items-baseline gap-1">
                <span className="text-xl font-bold text-[var(--color-text-primary)]">Rival</span>
                <span className="text-xl font-bold text-[var(--color-rival-red)]">Search</span>
                <span className="text-xs font-mono uppercase text-[var(--color-text-dim)] ml-1">MCP</span>
              </div>
            </Link>
            
            <p className="text-base text-[var(--color-text-muted)] leading-relaxed mb-6 max-w-md">
              Professional multi-engine search and content discovery MCP server. 
              <strong className="text-[var(--color-text-secondary)]"> 10 powerful tools, 3 search engines, 20+ sources</strong> — zero API keys required.
            </p>

            {/* Social links */}
            <div className="flex items-center gap-3">
              <a
                href="https://github.com/damionrashford/RivalSearchMCP"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-center w-10 h-10 rounded-lg bg-[var(--color-surface-2)] border border-[var(--color-border-subtle)] text-[var(--color-text-muted)] hover:text-[var(--color-text-primary)] hover:border-[var(--color-rival-red)]/30 transition-all duration-200"
                aria-label="GitHub"
              >
                <Github className="w-5 h-5" />
              </a>
              <a
                href="https://twitter.com/damionrashford"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-center w-10 h-10 rounded-lg bg-[var(--color-surface-2)] border border-[var(--color-border-subtle)] text-[var(--color-text-muted)] hover:text-[var(--color-text-primary)] hover:border-[var(--color-rival-red)]/30 transition-all duration-200"
                aria-label="Twitter"
              >
                <Twitter className="w-5 h-5" />
              </a>
            </div>
          </div>

          {/* Quick links grid */}
          <div className="grid grid-cols-2 gap-8">
            {/* Documentation */}
            <div>
              <h4 className="text-sm font-black uppercase tracking-[0.1em] text-[var(--color-text-primary)] mb-5">
                Documentation
              </h4>
              <ul className="space-y-3">
                {quickLinks.map((link) => (
                  <li key={link.href}>
                    <Link
                      to={link.href}
                      className="group inline-flex items-center gap-2 text-sm font-medium text-[var(--color-text-muted)] hover:text-[var(--color-rival-red)] transition-colors duration-200"
                    >
                      <span>{link.name}</span>
                      <ArrowUpRight className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-all duration-200 group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
                    </Link>
                  </li>
                ))}
              </ul>
            </div>

            {/* Resources */}
            <div>
              <h4 className="text-sm font-black uppercase tracking-[0.1em] text-[var(--color-text-primary)] mb-5">
                Resources
              </h4>
              <ul className="space-y-3">
                {resources.map((resource) => (
                  <li key={resource.href}>
                    <a
                      href={resource.href}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="group inline-flex items-center gap-2 text-sm font-medium text-[var(--color-text-muted)] hover:text-[var(--color-rival-red)] transition-colors duration-200"
                    >
                      <span>{resource.name}</span>
                      <ExternalLink className="w-3 h-3 opacity-50 group-hover:opacity-100 transition-opacity duration-200" />
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="pt-10 mt-10 border-t border-[var(--color-border-subtle)] flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-sm text-[var(--color-text-dim)] font-medium">
            © {new Date().getFullYear()} RivalSearchMCP. Built with{' '}
            <a 
              href="https://gofastmcp.com" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-[var(--color-rival-red)] hover:underline"
            >
              FastMCP
            </a>
            .
          </p>
          
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-green-500/5 border border-green-500/20">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[var(--color-rival-green)] opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-[var(--color-rival-green)]" />
            </span>
            <span className="text-xs font-bold text-green-400">
              All systems operational
            </span>
          </div>
        </div>
      </div>
    </footer>
  )
}
