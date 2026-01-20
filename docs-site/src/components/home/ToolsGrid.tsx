import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { ArrowRight, Sparkles } from 'lucide-react'
import { tools, toolCategories } from '../../data/tools'
import ToolCard from '../ui/ToolCard'

export default function ToolsGrid() {
  return (
    <section className="relative py-32 overflow-hidden">
      {/* Background gradient accent */}
      <div className="absolute inset-0 bg-gradient-to-b from-[var(--color-surface-0)] via-[var(--color-surface-1)] to-[var(--color-surface-0)]" />
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[1000px] h-[1000px] bg-[var(--color-rival-red)] rounded-full blur-[250px] opacity-[0.02]" />

      <div className="relative max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
        {/* Section header - editorial style */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true, margin: "-100px" }}
          className="mb-20"
        >
          {/* Kicker */}
          <div className="flex items-center gap-4 mb-6">
            <Sparkles className="w-5 h-5 text-[var(--color-rival-amber)]" />
            <span className="text-sm font-bold uppercase tracking-[0.2em] text-[var(--color-rival-amber)]">
              Complete Toolkit
            </span>
            <div className="flex-1 h-px bg-gradient-to-r from-[var(--color-rival-amber)]/30 to-transparent" />
          </div>

          {/* Headline */}
          <h2 className="text-5xl sm:text-6xl font-black tracking-tight text-[var(--color-text-primary)] mb-6 leading-tight">
            10 Powerful Tools
          </h2>

          {/* Description */}
          <p className="text-xl text-[var(--color-text-muted)] max-w-3xl leading-relaxed">
            Everything you need for comprehensive web research, content discovery, and AI-powered analysis.
            <span className="block mt-2 text-[var(--color-text-secondary)]">Zero API keys. Zero authentication. Zero friction.</span>
          </p>
        </motion.div>

        {/* Tool categories */}
        <div className="space-y-20">
          {toolCategories.map((category, categoryIndex) => {
            const categoryTools = tools.filter(t => t.category === category.id)
            
            return (
              <motion.div
                key={category.id}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: categoryIndex * 0.1 }}
                viewport={{ once: true, margin: "-100px" }}
              >
                {/* Category header */}
                <div className="flex items-center gap-6 mb-10">
                  <div className="flex items-baseline gap-3">
                    <div className="w-2 h-2 rounded-full bg-[var(--color-rival-red)]" />
                    <h3 className="text-2xl sm:text-3xl font-bold text-[var(--color-text-primary)]">
                      {category.name}
                    </h3>
                  </div>
                  <div className="hidden sm:block flex-1 h-px bg-gradient-to-r from-[var(--color-border-subtle)] to-transparent" />
                  <span className="hidden sm:inline text-sm text-[var(--color-text-dim)]">
                    {categoryTools.length} tool{categoryTools.length > 1 ? 's' : ''}
                  </span>
                </div>

                <p className="text-base text-[var(--color-text-muted)] mb-8 max-w-2xl">
                  {category.description}
                </p>

                {/* Tool cards grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                  {categoryTools.map((tool, toolIndex) => (
                    <ToolCard
                      key={tool.id}
                      tool={tool}
                      index={toolIndex}
                    />
                  ))}
                </div>
              </motion.div>
            )
          })}
        </div>

        {/* CTA to full documentation */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="mt-20 text-center"
        >
          <Link
            to="/tools"
            className="group inline-flex items-center gap-3 px-6 py-3 rounded-xl bg-[var(--color-surface-2)] border border-[var(--color-border-subtle)] hover:border-[var(--color-rival-red)]/40 transition-all duration-300"
          >
            <span className="font-semibold text-[var(--color-rival-red)] group-hover:text-[var(--color-rival-red-glow)] transition-colors">
              View complete tool documentation
            </span>
            <ArrowRight className="w-4 h-4 text-[var(--color-rival-red)] group-hover:translate-x-2 transition-transform duration-300" />
          </Link>
        </motion.div>
      </div>
    </section>
  )
}
