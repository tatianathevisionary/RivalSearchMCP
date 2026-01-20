import { motion } from 'framer-motion'
import { Sparkles, Filter, Zap } from 'lucide-react'
import { tools, toolCategories, getToolsByCategory } from '../data/tools'
import ToolCard from '../components/ui/ToolCard'
import Table from '../components/ui/Table'
import Badge from '../components/ui/Badge'

export default function Tools() {
    const tableHeaders = ['Tool', 'Sources', 'Rate Limited', 'Auth', 'Best For']

    const tableRows = tools.map(tool => [
        <span className="font-mono font-semibold text-[var(--color-rival-red)]">{tool.name}</span>,
        <span className="font-medium">{tool.sources.length} source{tool.sources.length > 1 ? 's' : ''}</span>,
        tool.rateLimited ? <Badge variant="warning">60/hr</Badge> : <Badge variant="success">Unlimited</Badge>,
        tool.authRequired ? <Badge variant="danger">Required</Badge> : <Badge variant="success">None</Badge>,
        <span className="text-[var(--color-text-muted)]">{tool.bestFor}</span>,
    ])

    return (
        <div className="max-w-5xl">
            {/* Hero header */}
            <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
                className="mb-12"
            >
                <div className="flex items-center gap-4 mb-6">
                    <Sparkles className="w-6 h-6 text-[var(--color-rival-amber)]" />
                    <span className="text-sm font-bold uppercase tracking-[0.2em] text-[var(--color-rival-amber)]">
                        Complete Toolkit
                    </span>
                    <div className="flex-1 h-px bg-gradient-to-r from-[var(--color-rival-amber)]/30 to-transparent" />
                </div>

                <h1 className="text-5xl sm:text-6xl font-black tracking-tight text-[var(--color-text-primary)] mb-6 leading-tight">
                    Tools Overview
                </h1>

                <p className="text-xl text-[var(--color-text-muted)] leading-relaxed max-w-3xl">
                    RivalSearchMCP provides 10 powerful tools for web research, content discovery, and AI-powered analysis.
                    <span className="block mt-2 text-[var(--color-text-secondary)] font-semibold">All tools work without API keys.</span>
                </p>
            </motion.div>

            {/* Stats overview */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.1 }}
                className="grid grid-cols-3 gap-4 mb-16"
            >
                {[
                    { value: '10', label: 'Tools', color: '#dc2626' },
                    { value: '3', label: 'Categories', color: '#f59e0b' },
                    { value: '20+', label: 'Data Sources', color: '#22c55e' },
                ].map((stat) => (
                    <div
                        key={stat.label}
                        className="relative p-6 rounded-2xl bg-[var(--color-surface-2)] border border-[var(--color-border-subtle)] overflow-hidden group hover:border-[var(--color-border-default)] transition-all duration-300"
                    >
                        <div className="text-4xl font-black mb-2 tabular-nums" style={{ color: stat.color }}>
                            {stat.value}
                        </div>
                        <div className="text-sm font-bold text-[var(--color-text-muted)] uppercase tracking-wider">
                            {stat.label}
                        </div>
                        {/* Glow on hover */}
                        <div
                            className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 pointer-events-none"
                            style={{ background: `radial-gradient(circle at center, ${stat.color}10 0%, transparent 70%)` }}
                        />
                    </div>
                ))}
            </motion.div>

            {/* Tool categories */}
            <div className="space-y-16 mb-20">
                {toolCategories.map((category, categoryIndex) => {
                    const categoryTools = getToolsByCategory(category.id)

                    return (
                        <motion.section
                            key={category.id}
                            initial={{ opacity: 0, y: 40 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6, delay: 0.2 + categoryIndex * 0.15 }}
                        >
                            {/* Category header */}
                            <div className="mb-8">
                                <div className="flex items-baseline gap-4 mb-3">
                                    <div className="w-2 h-2 rounded-full bg-[var(--color-rival-red)]" />
                                    <h2 className="text-3xl font-black tracking-tight text-[var(--color-text-primary)]">
                                        {category.name}
                                    </h2>
                                </div>
                                <p className="text-base text-[var(--color-text-muted)] ml-6 max-w-2xl">
                                    {category.description}
                                </p>
                            </div>

                            {/* Tool cards */}
                            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
                                {categoryTools.map((tool, toolIndex) => (
                                    <ToolCard
                                        key={tool.id}
                                        tool={tool}
                                        index={toolIndex}
                                    />
                                ))}
                            </div>
                        </motion.section>
                    )
                })}
            </div>

            {/* Comparison table */}
            <motion.section
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.5 }}
                className="mb-16"
            >
                <div className="flex items-center gap-4 mb-8">
                    <Filter className="w-6 h-6 text-[var(--color-rival-red)]" />
                    <h2 className="text-3xl font-black tracking-tight text-[var(--color-text-primary)]">
                        Quick Reference
                    </h2>
                </div>

                <p className="text-base text-[var(--color-text-muted)] mb-8 max-w-2xl">
                    Compare all tools at a glance — features, limitations, and best use cases.
                </p>

                <Table headers={tableHeaders} rows={tableRows} />
            </motion.section>

            {/* Bottom CTA */}
            <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.6 }}
                className="p-8 rounded-2xl bg-gradient-to-br from-[var(--color-surface-2)] to-[var(--color-surface-3)] border border-[var(--color-border-subtle)]"
            >
                <div className="flex flex-col sm:flex-row items-center gap-6">
                    <div className="flex-1">
                        <h3 className="text-2xl font-bold text-[var(--color-text-primary)] mb-2">
                            Ready to get started?
                        </h3>
                        <p className="text-base text-[var(--color-text-muted)]">
                            Install RivalSearchMCP and unlock these capabilities for your AI.
                        </p>
                    </div>
                    <a
                        href="cursor://anysphere.cursor-deeplink/mcp/install?name=RivalSearchMCP&config=eyJ1cmwiOiJodHRwczovL1JpdmFsU2VhcmNoTUNQLmZhc3RtY3AuYXBwL21jcCJ9"
                        className="inline-flex items-center gap-2 px-6 py-3 text-base font-bold text-white bg-gradient-to-r from-[var(--color-rival-red)] to-[var(--color-rival-red-dark)] rounded-xl transition-all duration-300 hover:shadow-[0_0_30px_rgba(220,38,38,0.4)] hover:scale-[1.02] shrink-0"
                    >
                        <Zap className="w-5 h-5" />
                        Add to Cursor
                    </a>
                </div>
            </motion.div>
        </div>
    )
}
