import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronRight, ExternalLink, ArrowRight } from 'lucide-react'
import { navigation } from '../../data/navigation'
import clsx from 'clsx'

export default function Sidebar() {
  const location = useLocation()
  const [expandedSections, setExpandedSections] = useState<string[]>(['Tools', 'Getting Started'])

  const toggleSection = (title: string) => {
    setExpandedSections(prev =>
      prev.includes(title)
        ? prev.filter(t => t !== title)
        : [...prev, title]
    )
  }

  const isActive = (href: string) => {
    if (href.includes('#')) {
      return location.pathname + location.hash === href
    }
    return location.pathname === href || 
      (href !== '/' && location.pathname.startsWith(href) && !location.pathname.slice(href.length).includes('/'))
  }

  return (
    <aside className="hidden lg:block w-72 shrink-0">
      <motion.div 
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5 }}
        className="sticky top-24 h-[calc(100vh-7rem)]"
      >
        <div className="h-full overflow-y-auto pr-4 pb-8 scrollbar-thin">
          <nav className="space-y-2">
            {navigation.map((section) => {
              const isExpanded = expandedSections.includes(section.title)
              const hasActiveChild = section.children?.some(child => isActive(child.href))
              
              return (
                <div key={section.title}>
                  <button
                    onClick={() => toggleSection(section.title)}
                    className={clsx(
                      'w-full flex items-center justify-between px-4 py-3 text-sm font-bold rounded-xl transition-all duration-200 group',
                      hasActiveChild || isExpanded
                        ? 'text-[var(--color-text-primary)] bg-[var(--color-surface-2)]'
                        : 'text-[var(--color-text-muted)] hover:text-[var(--color-text-primary)] hover:bg-[var(--color-surface-2)]/50'
                    )}
                  >
                    <span>{section.title}</span>
                    <motion.div
                      animate={{ rotate: isExpanded ? 90 : 0 }}
                      transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
                    >
                      <ChevronRight className={clsx(
                        'w-4 h-4 transition-colors duration-200',
                        hasActiveChild ? 'text-[var(--color-rival-red)]' : 'text-[var(--color-text-dim)]'
                      )} />
                    </motion.div>
                  </button>
                  
                  <AnimatePresence initial={false}>
                    {isExpanded && section.children && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
                        className="overflow-hidden"
                      >
                        <div className="mt-1 ml-3 pl-5 border-l-2 border-[var(--color-border-subtle)] space-y-1 py-2">
                          {section.children.map((item) => {
                            const active = isActive(item.href)
                            
                            return (
                              <Link
                                key={item.href}
                                to={item.href}
                                className={clsx(
                                  'relative block px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200',
                                  active
                                    ? 'text-[var(--color-rival-red)] bg-[var(--color-rival-red)]/10'
                                    : 'text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)] hover:bg-[var(--color-surface-2)]/50'
                                )}
                              >
                                {active && (
                                  <>
                                    <motion.div
                                      layoutId="sidebar-active"
                                      className="absolute left-0 top-1/2 -translate-y-1/2 -translate-x-[calc(100%+1.25rem+2px)] w-1 h-6 bg-[var(--color-rival-red)] rounded-full"
                                      transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
                                    />
                                    <div className="absolute inset-0 rounded-lg border border-[var(--color-rival-red)]/30" />
                                  </>
                                )}
                                {item.title}
                              </Link>
                            )
                          })}
                        </div>
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              )
            })}
          </nav>

          {/* Resources section */}
          <div className="mt-10 pt-8 border-t border-[var(--color-border-subtle)]">
            <h4 className="px-4 text-xs font-black uppercase tracking-[0.15em] text-[var(--color-text-dim)] mb-4">
              Resources
            </h4>
            <div className="space-y-1">
              {[
                { name: 'GitHub', href: 'https://github.com/damionrashford/RivalSearchMCP' },
                { name: 'FastMCP Docs', href: 'https://gofastmcp.com' },
                { name: 'MCP Protocol', href: 'https://modelcontextprotocol.io' },
              ].map((resource) => (
                <a
                  key={resource.name}
                  href={resource.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2.5 px-4 py-2.5 text-sm font-medium text-[var(--color-text-muted)] hover:text-[var(--color-text-secondary)] hover:bg-[var(--color-surface-2)]/50 rounded-lg transition-all duration-200 group"
                >
                  <ExternalLink className="w-4 h-4 text-[var(--color-text-dim)] group-hover:text-[var(--color-rival-red)] transition-colors duration-200" />
                  <span className="flex-1">{resource.name}</span>
                  <ArrowRight className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity duration-200" />
                </a>
              ))}
            </div>
          </div>

          {/* Status indicator */}
          <div className="mt-8 px-4">
            <div className="flex items-center gap-2.5 px-4 py-3 rounded-xl bg-green-500/5 border border-green-500/20">
              <span className="relative flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[var(--color-rival-green)] opacity-75" />
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-[var(--color-rival-green)]" />
              </span>
              <span className="text-xs font-semibold text-green-400">
                All systems operational
              </span>
            </div>
          </div>
        </div>
      </motion.div>
    </aside>
  )
}
