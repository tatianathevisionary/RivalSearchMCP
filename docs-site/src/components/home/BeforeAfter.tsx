import { motion, useMotionValue, useTransform, animate } from 'framer-motion'
import { useEffect, useState } from 'react'
import { X, Check, Minus } from 'lucide-react'

export default function BeforeAfter() {
    const [, setHoveredSide] = useState<'before' | 'after' | null>(null)
    const dividerX = useMotionValue(50)

    const leftWidth = useTransform(dividerX, [0, 100], ['0%', '100%'])
    const rightWidth = useTransform(dividerX, [0, 100], ['100%', '0%'])

    // Subtle breathing animation
    useEffect(() => {
        const controls = animate(dividerX, [48, 52, 48], {
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut"
        })
        return controls.stop
    }, [dividerX])

    const scenarios = [
        {
            question: "What's the latest AI news?",
            before: "I can't access current information or browse the web.",
            after: "Searches 3 engines, returns 27 current articles from today.",
        },
        {
            question: "What are people saying about X on Reddit?",
            before: "I don't have access to Reddit or social media platforms.",
            after: "Finds relevant discussions across Reddit, HN, Dev.to, and more.",
        },
        {
            question: "Find GitHub repos for web scraping",
            before: "I can't search GitHub repositories directly.",
            after: "Returns top repos with stars, descriptions, and README links.",
        },
        {
            question: "Analyze this PDF document",
            before: "I cannot read or process PDF files.",
            after: "Extracts text with OCR, analyzes content, returns summary.",
        },
    ]

    return (
        <section className="relative py-32 overflow-hidden">
            {/* Background */}
            <div className="absolute inset-0 bg-[var(--color-surface-1)]" />
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[1200px] h-[600px] bg-[var(--color-rival-red)] rounded-full blur-[250px] opacity-[0.025]" />

            <div className="relative max-w-7xl mx-auto px-6 sm:px-8 lg:px-12">
                {/* Section header */}
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6 }}
                    viewport={{ once: true }}
                    className="mb-16"
                >
                    <div className="flex items-center gap-4 mb-6">
                        <Minus className="w-5 h-5 text-[var(--color-rival-amber)]" />
                        <span className="text-sm font-bold uppercase tracking-[0.2em] text-[var(--color-rival-amber)]">
                            The Difference
                        </span>
                        <div className="flex-1 h-px bg-gradient-to-r from-[var(--color-rival-amber)]/30 to-transparent" />
                    </div>

                    <h2 className="text-5xl sm:text-6xl font-black tracking-tight text-[var(--color-text-primary)] mb-6 leading-tight">
                        What Your AI <span className="text-[var(--color-rival-red)]">Can Do Now</span>
                    </h2>

                    <p className="text-xl text-[var(--color-text-muted)] max-w-3xl leading-relaxed">
                        Transform your AI from knowledge-limited to web-capable in seconds.
                    </p>
                </motion.div>

                {/* Split comparison - Interactive */}
                <motion.div
                    initial={{ opacity: 0, y: 40 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.7 }}
                    viewport={{ once: true }}
                    className="relative rounded-3xl overflow-hidden border border-[var(--color-border-subtle)] bg-[var(--color-surface-2)]"
                    style={{ minHeight: '600px' }}
                >
                    {/* Before side */}
                    <motion.div
                        className="absolute inset-y-0 left-0 overflow-hidden"
                        style={{ width: leftWidth }}
                        onHoverStart={() => setHoveredSide('before')}
                        onHoverEnd={() => setHoveredSide(null)}
                    >
                        <div className="absolute inset-0 bg-gradient-to-br from-[var(--color-surface-2)] to-[var(--color-surface-3)] p-8 sm:p-12">
                            {/* Label */}
                            <div className="flex items-center gap-3 mb-8">
                                <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-red-500/10 border border-red-500/20">
                                    <X className="w-5 h-5 text-red-400" />
                                </div>
                                <div>
                                    <div className="text-sm uppercase tracking-wider text-red-400/60 font-bold">Before</div>
                                    <div className="text-lg font-bold text-red-300">RivalSearchMCP</div>
                                </div>
                            </div>

                            {/* Scenarios */}
                            <div className="space-y-5 max-w-md">
                                {scenarios.map((scenario, index) => (
                                    <motion.div
                                        key={index}
                                        initial={{ opacity: 0, x: -20 }}
                                        whileInView={{ opacity: 1, x: 0 }}
                                        transition={{ duration: 0.4, delay: index * 0.1 }}
                                        viewport={{ once: true }}
                                        className="group"
                                    >
                                        <div className="p-5 rounded-xl bg-[var(--color-surface-3)]/70 border border-[var(--color-border-subtle)]/50 hover:border-red-500/20 transition-all duration-300">
                                            <p className="text-sm font-semibold text-[var(--color-text-secondary)] mb-3">
                                                "{scenario.question}"
                                            </p>
                                            <div className="flex items-start gap-2">
                                                <X className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
                                                <p className="text-sm text-red-300/80 italic leading-relaxed">
                                                    "{scenario.before}"
                                                </p>
                                            </div>
                                        </div>
                                    </motion.div>
                                ))}
                            </div>
                        </div>
                    </motion.div>

                    {/* After side */}
                    <motion.div
                        className="absolute inset-y-0 right-0 overflow-hidden"
                        style={{ width: rightWidth }}
                        onHoverStart={() => setHoveredSide('after')}
                        onHoverEnd={() => setHoveredSide(null)}
                    >
                        <div className="absolute inset-0 bg-gradient-to-bl from-[var(--color-surface-2)] via-[var(--color-surface-3)] to-[var(--color-surface-2)] p-8 sm:p-12">
                            {/* Label */}
                            <div className="flex items-center gap-3 mb-8 justify-end">
                                <div>
                                    <div className="text-sm uppercase tracking-wider text-green-400/60 font-bold text-right">After</div>
                                    <div className="text-lg font-bold text-green-300 text-right">RivalSearchMCP</div>
                                </div>
                                <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-green-500/10 border border-green-500/20">
                                    <Check className="w-5 h-5 text-green-400" />
                                </div>
                            </div>

                            {/* Scenarios */}
                            <div className="space-y-5 max-w-md ml-auto">
                                {scenarios.map((scenario, index) => (
                                    <motion.div
                                        key={index}
                                        initial={{ opacity: 0, x: 20 }}
                                        whileInView={{ opacity: 1, x: 0 }}
                                        transition={{ duration: 0.4, delay: 0.2 + index * 0.1 }}
                                        viewport={{ once: true }}
                                        className="group"
                                    >
                                        <div className="p-5 rounded-xl bg-[var(--color-surface-3)]/70 border border-green-500/10 hover:border-green-500/30 transition-all duration-300">
                                            <p className="text-sm font-semibold text-[var(--color-text-secondary)] mb-3">
                                                "{scenario.question}"
                                            </p>
                                            <div className="flex items-start gap-2">
                                                <Check className="w-4 h-4 text-green-400 shrink-0 mt-0.5" />
                                                <p className="text-sm text-green-300 font-medium leading-relaxed">
                                                    {scenario.after}
                                                </p>
                                            </div>
                                        </div>
                                    </motion.div>
                                ))}
                            </div>
                        </div>
                    </motion.div>

                    {/* Center divider with drag handle */}
                    <motion.div
                        className="absolute inset-y-0 z-10 cursor-ew-resize"
                        style={{ left: `calc(${dividerX.get()}% - 1px)`, width: '2px' }}
                        drag="x"
                        dragConstraints={{ left: 0, right: 0 }}
                        dragElastic={0}
                        dragMomentum={false}
                        onDrag={(_, info) => {
                            const container = document.querySelector('section')
                            if (container) {
                                const rect = container.getBoundingClientRect()
                                const percentage = ((info.point.x - rect.left) / rect.width) * 100
                                dividerX.set(Math.max(20, Math.min(80, percentage)))
                            }
                        }}
                    >
                        {/* Divider line */}
                        <div className="absolute inset-0 bg-gradient-to-b from-[var(--color-rival-red)]/40 via-[var(--color-rival-red)] to-[var(--color-rival-red)]/40" />

                        {/* Drag handle */}
                        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-12 h-12 rounded-full bg-[var(--color-rival-red)] border-4 border-[var(--color-surface-0)] shadow-[0_0_30px_rgba(220,38,38,0.6)] flex items-center justify-center">
                            <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M8 9l4-4 4 4m0 6l-4 4-4-4" />
                            </svg>
                        </div>
                    </motion.div>

                    {/* VS label at bottom */}
                    <div className="absolute bottom-8 left-1/2 -translate-x-1/2 z-20 px-6 py-2 rounded-full bg-[var(--color-surface-0)]/90 backdrop-blur-md border border-[var(--color-border-subtle)]">
                        <span className="text-xs font-black uppercase tracking-[0.3em] text-[var(--color-text-muted)]">
                            VS
                        </span>
                    </div>
                </motion.div>

                {/* Feature highlights below */}
                <motion.div
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.6, delay: 0.3 }}
                    viewport={{ once: true }}
                    className="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-12"
                >
                    {[
                        { label: 'Web Search', sublabel: '3 engines, concurrent' },
                        { label: 'Social Search', sublabel: '5 platforms' },
                        { label: 'Document Analysis', sublabel: 'PDF, Word, OCR' },
                        { label: 'Research Agent', sublabel: 'AI orchestration' },
                    ].map((item) => (
                        <div
                            key={item.label}
                            className="p-5 rounded-xl bg-[var(--color-surface-2)]/60 border border-[var(--color-border-subtle)] hover:border-[var(--color-rival-red)]/30 transition-all duration-300 group"
                        >
                            <div className="font-bold text-[var(--color-text-primary)] mb-1 group-hover:text-[var(--color-rival-red)] transition-colors duration-300">
                                {item.label}
                            </div>
                            <div className="text-sm text-[var(--color-text-muted)]">
                                {item.sublabel}
                            </div>
                        </div>
                    ))}
                </motion.div>
            </div>
        </section>
    )
}
