import { useState, useEffect } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { motion, AnimatePresence, useScroll } from 'framer-motion'
import { Menu, X, Github } from 'lucide-react'
import { headerLinks } from '../../data/navigation'
import clsx from 'clsx'

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)
  const location = useLocation()
  const { scrollY } = useScroll()

  useEffect(() => {
    return scrollY.on('change', (latest) => {
      setScrolled(latest > 50)
    })
  }, [scrollY])

  return (
    <motion.header 
      className={clsx(
        "fixed top-0 left-0 right-0 z-50 transition-all duration-500",
        scrolled ? "py-3" : "py-4"
      )}
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
    >
      <nav className={clsx(
        "mx-auto max-w-7xl px-6 sm:px-8 lg:px-12 transition-all duration-500",
        scrolled 
          ? "backdrop-blur-xl bg-[var(--color-surface-0)]/90 rounded-2xl shadow-[0_8px_32px_rgba(0,0,0,0.4)] border border-[var(--color-border-subtle)]" 
          : "backdrop-blur-md bg-[var(--color-surface-0)]/70"
      )}>
        <div className="flex h-16 items-center justify-between">
          {/* Logo - enhanced */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="relative">
              {/* Icon background with glow */}
              <div className="relative z-10 w-10 h-10 rounded-xl bg-gradient-to-br from-[var(--color-surface-2)] to-[var(--color-surface-3)] border border-[var(--color-border-subtle)] flex items-center justify-center group-hover:border-[var(--color-rival-red)]/60 transition-all duration-300">
                <svg viewBox="0 0 24 24" className="w-5 h-5">
                  <circle cx="10" cy="10" r="5.5" fill="none" stroke="var(--color-rival-red)" strokeWidth="2.5"/>
                  <line x1="14" y1="14" x2="20" y2="20" stroke="var(--color-rival-red)" strokeWidth="2.5" strokeLinecap="round"/>
                  <circle cx="10" cy="10" r="2" fill="var(--color-rival-amber)"/>
                </svg>
              </div>
              {/* Animated glow */}
              <div className="absolute inset-0 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 blur-lg"
                   style={{ background: 'radial-gradient(circle, var(--color-rival-red) 0%, transparent 70%)' }} />
            </div>
            
            {/* Wordmark */}
            <div className="flex items-baseline gap-1">
              <span className="text-lg font-bold text-[var(--color-text-primary)] tracking-tight">Rival</span>
              <span className="text-lg font-bold text-[var(--color-rival-red)] tracking-tight">Search</span>
              <span className="hidden sm:inline text-[10px] font-mono uppercase text-[var(--color-text-dim)] ml-1.5 tracking-wider">MCP</span>
            </div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center gap-2">
            {headerLinks.map((link) => {
              const isActive = location.pathname === link.href || 
                (link.href !== '/' && location.pathname.startsWith(link.href))
              
              return (
                <Link
                  key={link.href}
                  to={link.href}
                  className={clsx(
                    'relative px-4 py-2 text-sm font-semibold rounded-lg transition-all duration-300',
                    isActive
                      ? 'text-[var(--color-rival-red)]'
                      : 'text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)]'
                  )}
                >
                  {link.title}
                  {isActive && (
                    <motion.div
                      layoutId="navbar-active-pill"
                      className="absolute inset-0 bg-[var(--color-rival-red)]/10 border border-[var(--color-rival-red)]/20 rounded-lg -z-10"
                      transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
                    />
                  )}
                </Link>
              )
            })}
          </div>

          {/* Right actions */}
          <div className="flex items-center gap-3">
            {/* GitHub star button */}
            <a
              href="https://github.com/damionrashford/RivalSearchMCP"
              target="_blank"
              rel="noopener noreferrer"
              className="hidden sm:flex items-center gap-2 px-3 py-2 text-sm font-semibold text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] bg-[var(--color-surface-2)] border border-[var(--color-border-subtle)] rounded-lg transition-all duration-200 hover:border-[var(--color-border-default)] hover:shadow-md"
            >
              <Github className="w-4 h-4" />
              <span className="hidden lg:inline">Star</span>
            </a>

            {/* Mobile menu toggle */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden p-2.5 text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] hover:bg-[var(--color-surface-2)] rounded-lg transition-all duration-200"
            >
              <AnimatePresence mode="wait">
                {mobileMenuOpen ? (
                  <motion.div
                    key="close"
                    initial={{ rotate: -90, opacity: 0 }}
                    animate={{ rotate: 0, opacity: 1 }}
                    exit={{ rotate: 90, opacity: 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <X className="w-5 h-5" />
                  </motion.div>
                ) : (
                  <motion.div
                    key="menu"
                    initial={{ rotate: 90, opacity: 0 }}
                    animate={{ rotate: 0, opacity: 1 }}
                    exit={{ rotate: -90, opacity: 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <Menu className="w-5 h-5" />
                  </motion.div>
                )}
              </AnimatePresence>
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        <AnimatePresence>
          {mobileMenuOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
              className="md:hidden overflow-hidden border-t border-[var(--color-border-subtle)] mt-4"
            >
              <div className="py-6 space-y-2">
                {headerLinks.map((link) => {
                  const isActive = location.pathname === link.href
                  
                  return (
                    <Link
                      key={link.href}
                      to={link.href}
                      onClick={() => setMobileMenuOpen(false)}
                      className={clsx(
                        'block px-4 py-3 text-base font-semibold rounded-xl transition-all duration-200',
                        isActive
                          ? 'text-[var(--color-rival-red)] bg-[var(--color-rival-red)]/10 border border-[var(--color-rival-red)]/20'
                          : 'text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] hover:bg-[var(--color-surface-2)]'
                      )}
                    >
                      {link.title}
                    </Link>
                  )
                })}
                
                {/* Mobile CTA */}
                <div className="pt-4 space-y-3">
                  <a
                    href="https://github.com/damionrashford/RivalSearchMCP"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center justify-center gap-2 px-4 py-3 text-sm font-semibold text-[var(--color-text-secondary)] bg-[var(--color-surface-2)] border border-[var(--color-border-subtle)] rounded-xl hover:border-[var(--color-border-default)] transition-all duration-200"
                  >
                    <Github className="w-4 h-4" />
                    <span>Star on GitHub</span>
                  </a>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </nav>
    </motion.header>
  )
}
