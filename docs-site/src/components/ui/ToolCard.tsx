import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ArrowRight } from 'lucide-react'
import type { Tool } from '../../data/tools'
import Badge from './Badge'

interface ToolCardProps {
  tool: Tool
  index?: number
  variant?: 'default' | 'compact'
}

export default function ToolCard({ tool, index = 0, variant = 'default' }: ToolCardProps) {
  const Icon = tool.icon

  if (variant === 'compact') {
    return (
      <Link to={`/tools/${tool.id}`}>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: index * 0.05 }}
          viewport={{ once: true }}
          whileHover={{ scale: 1.02 }}
          className="group relative p-4 rounded-xl bg-[var(--color-surface-2)] border border-[var(--color-border-subtle)] hover:border-[var(--color-rival-red)]/40 transition-all duration-300"
        >
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-[var(--color-surface-3)] flex items-center justify-center group-hover:bg-[var(--color-rival-red)]/10 transition-colors duration-300">
              <Icon className="w-5 h-5 text-[var(--color-rival-red)]" />
            </div>
            <div className="flex-1 min-w-0">
              <h4 className="font-mono text-sm font-semibold text-[var(--color-text-primary)] group-hover:text-[var(--color-rival-red)] transition-colors truncate">
                {tool.name}
              </h4>
              <p className="text-xs text-[var(--color-text-muted)]">
                {tool.sources.length} source{tool.sources.length > 1 ? 's' : ''}
              </p>
            </div>
            <ArrowRight className="w-4 h-4 text-[var(--color-text-dim)] opacity-0 group-hover:opacity-100 group-hover:translate-x-1 transition-all duration-300" />
          </div>
        </motion.div>
      </Link>
    )
  }

  // Default variant - premium card design
  return (
    <Link to={`/tools/${tool.id}`}>
      <motion.article
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: index * 0.08 }}
        viewport={{ once: true, margin: "-50px" }}
        whileHover={{ y: -6 }}
        className="group relative h-full flex flex-col overflow-hidden rounded-2xl bg-[var(--color-surface-2)]/80 backdrop-blur-sm border border-[var(--color-border-subtle)] hover:border-[var(--color-rival-red)]/50 transition-all duration-500 hover:shadow-[0_20px_60px_-15px_rgba(0,0,0,0.5),0_0_40px_rgba(220,38,38,0.1)]"
      >
        {/* Top accent bar */}
        <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-[var(--color-rival-red)] to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
        
        {/* Card content */}
        <div className="relative p-7 flex-1 flex flex-col">
          {/* Icon container with glow */}
          <div className="relative mb-6 w-fit">
            <div className="relative z-10 w-14 h-14 rounded-2xl bg-gradient-to-br from-[var(--color-surface-3)] to-[var(--color-surface-4)] border border-[var(--color-border-subtle)] flex items-center justify-center group-hover:border-[var(--color-rival-red)]/30 transition-all duration-500">
              <Icon className="w-7 h-7 text-[var(--color-rival-red)] transition-all duration-500 group-hover:scale-110 group-hover:rotate-3" />
            </div>
            {/* Icon glow */}
            <div className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 blur-xl"
                 style={{ background: 'radial-gradient(circle, var(--color-rival-red) 0%, transparent 70%)' }} />
          </div>

          {/* Header with hover arrow */}
          <div className="flex items-start justify-between gap-3 mb-4">
            <h3 className="font-mono text-lg font-bold text-[var(--color-text-primary)] group-hover:text-[var(--color-rival-red)] transition-colors duration-300">
              {tool.name}
            </h3>
            <ArrowRight className="w-5 h-5 text-[var(--color-text-dim)] opacity-0 group-hover:opacity-100 group-hover:text-[var(--color-rival-red)] transform translate-x-0 group-hover:translate-x-2 transition-all duration-500 shrink-0 mt-1" />
          </div>

          {/* Description */}
          <p className="text-sm text-[var(--color-text-muted)] leading-relaxed mb-6 flex-1">
            {tool.shortDescription}
          </p>

          {/* Tags */}
          <div className="flex flex-wrap gap-2 pt-4 border-t border-[var(--color-border-subtle)]/30">
            {tool.rateLimited && (
              <Badge variant="warning">Rate Limited</Badge>
            )}
            {!tool.authRequired && (
              <Badge variant="success">No Auth</Badge>
            )}
            <Badge>
              {tool.sources.length} source{tool.sources.length > 1 ? 's' : ''}
            </Badge>
          </div>
        </div>

        {/* Bottom shine effect */}
        <div className="absolute bottom-0 left-0 right-0 h-px bg-gradient-to-r from-transparent via-[var(--color-rival-red)]/0 to-transparent group-hover:via-[var(--color-rival-red)]/60 transition-all duration-700" />
      </motion.article>
    </Link>
  )
}
