import { motion } from 'framer-motion'
import { ArrowRight, Sparkles, Zap, Shield } from 'lucide-react'
import { Link } from 'react-router-dom'

export default function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Layered background effects */}
      <div className="absolute inset-0 z-0">
        {/* Animated gradient orbs */}
        <div className="absolute top-[20%] left-[15%] w-[600px] h-[600px] bg-[var(--color-rival-red)] rounded-full blur-[180px] opacity-[0.08] animate-pulse" 
             style={{ animationDuration: '8s' }} />
        <div className="absolute bottom-[15%] right-[20%] w-[500px] h-[500px] bg-[var(--color-rival-amber)] rounded-full blur-[160px] opacity-[0.04]" />
        
        {/* Subtle grid pattern */}
        <div 
          className="absolute inset-0 opacity-[0.015]"
          style={{
            backgroundImage: `
              linear-gradient(var(--color-border-subtle) 1.5px, transparent 1.5px),
              linear-gradient(90deg, var(--color-border-subtle) 1.5px, transparent 1.5px)
            `,
            backgroundSize: '60px 60px',
          }}
        />
        
        {/* Radial fade at edges */}
        <div className="absolute inset-0 bg-gradient-radial from-transparent via-transparent to-[var(--color-surface-0)]" />
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-6 sm:px-8 lg:px-12 py-24 sm:py-32">
        <div className="text-center">
          {/* Status badge */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.4 }}
            className="inline-flex items-center gap-2.5 px-4 py-2 rounded-full bg-[var(--color-surface-2)]/80 backdrop-blur-md border border-[var(--color-border-subtle)] mb-12"
          >
            <span className="relative flex h-2.5 w-2.5">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-[var(--color-rival-green)] opacity-75" />
              <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-[var(--color-rival-green)]" />
            </span>
            <span className="text-sm font-medium text-[var(--color-text-secondary)]">
              Live on FastMCP Cloud
            </span>
          </motion.div>

          {/* Main headline - massive, bold, attention-grabbing */}
          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.1 }}
            className="text-6xl sm:text-7xl lg:text-8xl font-extrabold tracking-tight mb-8 leading-[1.1]"
          >
            <span className="block text-[var(--color-text-primary)] mb-2">
              Give Your AI
            </span>
            <span className="block">
              <span className="text-[var(--color-text-primary)]">The Power to </span>
              <span className="relative inline-block">
                <span className="text-[var(--color-rival-red)] text-glow-red">Search</span>
                {/* Animated underline */}
                <motion.span
                  initial={{ scaleX: 0 }}
                  animate={{ scaleX: 1 }}
                  transition={{ duration: 1, delay: 0.9, ease: [0.22, 1, 0.36, 1] }}
                  className="absolute -bottom-3 left-0 right-0 h-1.5 bg-gradient-to-r from-[var(--color-rival-red)] via-[var(--color-rival-amber)] to-[var(--color-rival-red)] rounded-full origin-left"
                />
              </span>
            </span>
          </motion.h1>

          {/* Subtitle - clear, readable */}
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="text-xl sm:text-2xl text-[var(--color-text-muted)] mx-auto mb-14 leading-relaxed max-w-3xl px-4"
          >
            Professional multi-engine search and content discovery MCP server.{' '}
            <span className="text-[var(--color-text-secondary)]">Transform "I don't know" into "Let me search that for you."</span>
          </motion.p>

          {/* CTA - singular, focused */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-20"
          >
            <Link
              to="/getting-started"
              className="group relative inline-flex items-center gap-3 px-8 py-4 text-lg font-bold text-white bg-gradient-to-r from-[var(--color-rival-red)] via-[var(--color-rival-red-dark)] to-[var(--color-rival-red)] rounded-2xl overflow-hidden transition-all duration-300 hover:shadow-[0_0_40px_rgba(220,38,38,0.5),0_20px_50px_rgba(220,38,38,0.15)] hover:scale-[1.03] hover:-translate-y-0.5"
            >
              <span className="relative z-10 flex items-center gap-3">
                <Zap className="w-6 h-6" />
                Get Started Now
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-300" />
              </span>
              {/* Animated shine effect */}
              <span className="absolute inset-0 -translate-x-full group-hover:translate-x-full transition-transform duration-1000 bg-gradient-to-r from-transparent via-white/10 to-transparent skew-x-12" />
            </Link>
            
            <a
              href="https://github.com/damionrashford/RivalSearchMCP"
              target="_blank"
              rel="noopener noreferrer"
              className="group inline-flex items-center gap-2 px-6 py-3 text-base font-semibold text-[var(--color-text-primary)] bg-[var(--color-surface-2)]/60 backdrop-blur-sm border border-[var(--color-border-subtle)] rounded-xl transition-all duration-300 hover:border-[var(--color-border-default)] hover:bg-[var(--color-surface-3)]"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path fillRule="evenodd" clipRule="evenodd" d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.17 6.839 9.49.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.604-3.369-1.34-3.369-1.34-.454-1.156-1.11-1.464-1.11-1.464-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.831.092-.646.35-1.086.636-1.336-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.836c.85.004 1.705.115 2.504.337 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.167 22 16.418 22 12c0-5.523-4.477-10-10-10z" />
              </svg>
              View on GitHub
            </a>
          </motion.div>

          {/* Stats grid - Clean, structured */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.5 }}
            className="relative"
          >
            {/* Stats container with distinctive styling */}
            <div className="inline-grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 p-2 rounded-2xl bg-gradient-to-br from-[var(--color-surface-2)]/40 via-[var(--color-surface-2)]/60 to-[var(--color-surface-2)]/40 backdrop-blur-lg border border-[var(--color-border-subtle)]/50">
              {[
                { value: '10', label: 'Tools', color: '#dc2626' },
                { value: '3', label: 'Engines', color: '#f59e0b' },
                { value: '20+', label: 'Sources', color: '#22c55e' },
                { value: '0', label: 'API Keys', color: '#3b82f6' },
              ].map((stat, index) => (
                <div
                  key={stat.label}
                  className="relative group px-6 py-5 sm:px-8 sm:py-6 rounded-xl bg-[var(--color-surface-3)]/50 border border-[var(--color-border-subtle)]/30 hover:border-[var(--color-border-default)] transition-all duration-300"
                  style={{ transitionDelay: `${index * 50}ms` }}
                >
                  {/* Stat value */}
                  <div
                    className="text-4xl sm:text-5xl font-black mb-2 tabular-nums tracking-tight"
                    style={{ color: stat.color }}
                  >
                    {stat.value}
                  </div>
                  {/* Stat label */}
                  <div className="text-sm sm:text-base font-medium text-[var(--color-text-muted)] uppercase tracking-wide">
                    {stat.label}
                  </div>
                  
                  {/* Hover glow effect */}
                  <div 
                    className="absolute inset-0 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"
                    style={{
                      background: `radial-gradient(circle at center, ${stat.color}15 0%, transparent 70%)`
                    }}
                  />
                </div>
              ))}
            </div>
          </motion.div>

          {/* Feature pills - below stats */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.7 }}
            className="flex flex-wrap items-center justify-center gap-4 sm:gap-6 mt-16 max-w-3xl mx-auto"
          >
            {[
              { icon: Zap, text: 'Concurrent multi-engine search', color: '#dc2626' },
              { icon: Shield, text: 'Zero authentication required', color: '#22c55e' },
              { icon: Sparkles, text: 'AI-powered research agent', color: '#f59e0b' },
            ].map((feature, index) => (
              <motion.div
                key={feature.text}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.4, delay: 0.8 + index * 0.1 }}
                className="group flex items-center gap-2.5 px-4 py-2.5 rounded-xl bg-[var(--color-surface-2)]/60 border border-[var(--color-border-subtle)]/50 hover:border-[var(--color-border-default)] transition-all duration-300"
              >
                <feature.icon 
                  className="w-4 h-4 sm:w-5 sm:h-5 transition-transform duration-300 group-hover:scale-110" 
                  style={{ color: feature.color }}
                />
                <span className="text-sm sm:text-base text-[var(--color-text-secondary)] group-hover:text-[var(--color-text-primary)] transition-colors duration-300">
                  {feature.text}
                </span>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </div>

      {/* Scroll indicator - more prominent */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.8 }}
        className="absolute bottom-10 left-1/2 -translate-x-1/2 z-20"
      >
        <motion.div
          animate={{ y: [0, 12, 0] }}
          transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
          className="flex flex-col items-center gap-2"
        >
          <div className="w-6 h-10 rounded-full border-2 border-[var(--color-rival-red)]/40 flex items-start justify-center p-1.5">
            <motion.div 
              className="w-1.5 h-3 rounded-full bg-[var(--color-rival-red)]"
              animate={{ y: [0, 12, 0] }}
              transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
            />
          </div>
          <span className="text-xs text-[var(--color-text-dim)] uppercase tracking-wider">Scroll</span>
        </motion.div>
      </motion.div>
    </section>
  )
}
