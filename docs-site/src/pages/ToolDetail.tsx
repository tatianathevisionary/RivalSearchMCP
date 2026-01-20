import { useParams, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ArrowLeft, ArrowRight } from 'lucide-react'
import { getToolById, tools } from '../data/tools'
import Badge from '../components/ui/Badge'
import Table from '../components/ui/Table'
import CodeBlock from '../components/ui/CodeBlock'
import Callout from '../components/ui/Callout'

export default function ToolDetail() {
  const { toolId } = useParams<{ toolId: string }>()
  const tool = getToolById(toolId || '')
  
  if (!tool) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] text-center">
        <div className="w-20 h-20 rounded-2xl bg-[var(--color-surface-2)] border border-[var(--color-border-subtle)] flex items-center justify-center mb-6">
          <span className="text-4xl">🔍</span>
        </div>
        <h1 className="text-3xl font-black text-[var(--color-text-primary)] mb-3">Tool Not Found</h1>
        <p className="text-[var(--color-text-muted)] mb-8 max-w-md">
          The tool <code className="text-[var(--color-rival-amber)]">"{toolId}"</code> doesn't exist in our toolkit.
        </p>
        <Link
          to="/tools"
          className="inline-flex items-center gap-2 px-5 py-2.5 text-sm font-semibold text-[var(--color-rival-red)] hover:text-[var(--color-rival-red-glow)] bg-[var(--color-surface-2)] border border-[var(--color-border-subtle)] rounded-xl hover:border-[var(--color-rival-red)]/30 transition-all duration-200"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Tools
        </Link>
      </div>
    )
  }

  const Icon = tool.icon
  const currentIndex = tools.findIndex(t => t.id === tool.id)
  const prevTool = currentIndex > 0 ? tools[currentIndex - 1] : null
  const nextTool = currentIndex < tools.length - 1 ? tools[currentIndex + 1] : null

  const paramTableHeaders = ['Parameter', 'Type', 'Required', 'Default', 'Description']
  const paramTableRows = tool.parameters.map(param => [
    <code className="font-mono font-semibold text-[var(--color-rival-amber)]">{param.name}</code>,
    <code className="font-mono text-[var(--color-text-muted)] text-xs">{param.type}</code>,
    param.required 
      ? <Badge variant="danger">Required</Badge> 
      : <Badge variant="info">Optional</Badge>,
    param.default 
      ? <code className="font-mono text-xs bg-[var(--color-surface-3)] px-2 py-1 rounded">{param.default}</code> 
      : <span className="text-[var(--color-text-dim)]">—</span>,
    <span className="text-sm">{param.description}</span>,
  ])

  const exampleRequest = `{
  "${tool.parameters[0]?.name || 'query'}": "example search query"${
    tool.parameters.slice(1, 3).map(p => p.default ? `,\n  "${p.name}": ${p.default}` : '').join('')
  }
}`

  const exampleResponse = `{
  "success": true,
  "query": "example search query",
  "total_results": ${tool.sources.length * 10},
  "sources_used": ${JSON.stringify(tool.sources.slice(0, 3))},
  "results": [
    {
      "title": "Example Result",
      "url": "https://example.com",
      "snippet": "Result description and preview..."
    }
  ],
  "next_steps": ${JSON.stringify(tool.nextSteps.slice(0, 2).map(s => s.useCase))}
}`

  return (
    <div className="max-w-4xl">
      {/* Breadcrumb */}
      <motion.nav
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="flex items-center gap-2 text-sm text-[var(--color-text-muted)] mb-8"
      >
        <Link to="/tools" className="hover:text-[var(--color-text-secondary)] transition-colors">
          Tools
        </Link>
        <span className="text-[var(--color-text-dim)]">/</span>
        <span className="text-[var(--color-text-secondary)] font-medium">{tool.displayName}</span>
      </motion.nav>

      {/* Tool header - hero style */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="relative p-8 sm:p-10 rounded-3xl bg-gradient-to-br from-[var(--color-surface-2)] via-[var(--color-surface-3)] to-[var(--color-surface-2)] border border-[var(--color-border-subtle)] mb-12 overflow-hidden"
      >
        {/* Background accent */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-[var(--color-rival-red)] rounded-full blur-[150px] opacity-[0.06]" />
        
        <div className="relative">
          <div className="flex items-start gap-5 mb-6">
            {/* Icon with glow */}
            <div className="relative">
              <div className="w-16 h-16 rounded-2xl bg-[var(--color-surface-4)] border-2 border-[var(--color-rival-red)]/30 flex items-center justify-center shrink-0">
                <Icon className="w-8 h-8 text-[var(--color-rival-red)]" />
              </div>
              <div className="absolute inset-0 rounded-2xl blur-xl opacity-50" style={{ background: 'radial-gradient(circle, var(--color-rival-red) 0%, transparent 70%)' }} />
            </div>

            <div className="flex-1">
              <h1 className="text-4xl sm:text-5xl font-black tracking-tight text-[var(--color-text-primary)] mb-3 leading-tight">
                {tool.displayName}
              </h1>
              <code className="text-lg font-mono font-semibold text-[var(--color-rival-amber)] bg-[var(--color-surface-4)] px-3 py-1.5 rounded-lg">
                {tool.name}
              </code>
            </div>
          </div>

          {/* Meta tags */}
          <div className="flex flex-wrap gap-2 mb-6">
            {!tool.authRequired && <Badge variant="success">No Auth Required</Badge>}
            {tool.rateLimited && <Badge variant="warning">Rate Limited (60/hr)</Badge>}
            <Badge>{tool.sources.length} Data Source{tool.sources.length > 1 ? 's' : ''}</Badge>
            <Badge variant="info">{tool.category}</Badge>
          </div>

          {/* Description */}
          <p className="text-lg text-[var(--color-text-secondary)] leading-relaxed">
            {tool.description}
          </p>
        </div>
      </motion.div>

      {/* Data sources */}
      <motion.section
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="mb-12"
      >
        <h2 className="text-2xl font-black text-[var(--color-text-primary)] mb-6 flex items-center gap-3">
          <div className="w-1 h-8 bg-[var(--color-rival-red)] rounded-full" />
          Data Sources
        </h2>
        <div className="flex flex-wrap gap-3">
          {tool.sources.map((source) => (
            <div
              key={source}
              className="px-5 py-3 rounded-xl bg-[var(--color-surface-2)] border border-[var(--color-border-subtle)] text-sm font-semibold text-[var(--color-text-secondary)] hover:border-[var(--color-rival-red)]/30 hover:text-[var(--color-text-primary)] transition-all duration-200"
            >
              {source}
            </div>
          ))}
        </div>
      </motion.section>

      {/* Parameters table */}
      <motion.section
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="mb-12"
      >
        <h2 className="text-2xl font-black text-[var(--color-text-primary)] mb-6 flex items-center gap-3">
          <div className="w-1 h-8 bg-[var(--color-rival-red)] rounded-full" />
          Parameters
        </h2>
        <Table headers={paramTableHeaders} rows={paramTableRows} />
      </motion.section>

      {/* Example usage */}
      <motion.section
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="mb-12"
      >
        <h2 className="text-2xl font-black text-[var(--color-text-primary)] mb-6 flex items-center gap-3">
          <div className="w-1 h-8 bg-[var(--color-rival-red)] rounded-full" />
          Example Usage
        </h2>

        <div className="space-y-8">
          <div>
            <h3 className="text-lg font-bold text-[var(--color-text-primary)] mb-4">Request</h3>
            <CodeBlock code={exampleRequest} language="json" filename="request.json" />
          </div>

          <div>
            <h3 className="text-lg font-bold text-[var(--color-text-primary)] mb-4">Response</h3>
            <CodeBlock code={exampleResponse} language="json" filename="response.json" />
          </div>
        </div>
      </motion.section>

      {/* Next steps */}
      {tool.nextSteps.length > 0 && (
        <motion.section
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
          className="mb-12"
        >
          <h2 className="text-2xl font-black text-[var(--color-text-primary)] mb-6 flex items-center gap-3">
            <div className="w-1 h-8 bg-[var(--color-rival-red)] rounded-full" />
            Suggested Next Steps
          </h2>
          
          <Callout type="tip" title="Workflow Optimization">
            After using <code>{tool.name}</code>, consider these follow-up actions for comprehensive research:
          </Callout>

          <div className="grid gap-4 mt-6">
            {tool.nextSteps.map((step) => {
              const nextToolData = tools.find(t => t.name === step.tool)
              const NextIcon = nextToolData?.icon
              
              return (
                <Link
                  key={step.tool}
                  to={nextToolData ? `/tools/${nextToolData.id}` : '/tools'}
                  className="group flex items-center justify-between p-5 rounded-xl bg-[var(--color-surface-2)] border border-[var(--color-border-subtle)] hover:border-[var(--color-rival-red)]/40 transition-all duration-300 hover:shadow-lg"
                >
                  <div className="flex items-start gap-4">
                    {NextIcon && (
                      <div className="w-10 h-10 rounded-lg bg-[var(--color-surface-3)] flex items-center justify-center group-hover:bg-[var(--color-rival-red)]/10 transition-colors duration-300">
                        <NextIcon className="w-5 h-5 text-[var(--color-rival-red)]" />
                      </div>
                    )}
                    <div>
                      <code className="font-mono font-semibold text-base text-[var(--color-rival-amber)] group-hover:text-[var(--color-rival-red)] transition-colors duration-300">
                        {step.tool}
                      </code>
                      <p className="text-sm text-[var(--color-text-muted)] mt-1.5 leading-relaxed">
                        {step.useCase}
                      </p>
                    </div>
                  </div>
                  <ArrowRight className="w-5 h-5 text-[var(--color-text-dim)] group-hover:text-[var(--color-rival-red)] group-hover:translate-x-2 transition-all duration-300 shrink-0" />
                </Link>
              )
            })}
          </div>
        </motion.section>
      )}

      {/* Tips */}
      <motion.section
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.5 }}
        className="mb-16"
      >
        <h2 className="text-2xl font-black text-[var(--color-text-primary)] mb-6 flex items-center gap-3">
          <div className="w-1 h-8 bg-[var(--color-rival-red)] rounded-full" />
          Tips & Best Practices
        </h2>

        <div className="space-y-4">
          <Callout type="success" title="Optimization Tips">
            Be specific in your queries for better results. Include relevant keywords, context, and time ranges when applicable.
          </Callout>
          
          {tool.rateLimited && (
            <Callout type="warning" title="Rate Limiting">
              This tool is limited to <strong>60 requests per hour</strong> for unauthenticated access. Plan your research queries accordingly.
            </Callout>
          )}

          {tool.id === 'research-agent' && (
            <Callout type="info" title="API Key Required">
              The research agent requires an <code>OPENROUTER_API_KEY</code> environment variable to power AI orchestration. All other tools work without any API keys.
            </Callout>
          )}
        </div>
      </motion.section>

      {/* Navigation */}
      <motion.nav
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.6 }}
        className="flex items-center justify-between pt-10 mt-12 border-t-2 border-[var(--color-border-subtle)]"
      >
        {prevTool ? (
          <Link
            to={`/tools/${prevTool.id}`}
            className="group flex items-center gap-3 px-5 py-4 rounded-xl bg-[var(--color-surface-2)] border border-[var(--color-border-subtle)] hover:border-[var(--color-rival-red)]/30 transition-all duration-300 hover:shadow-lg"
          >
            <ArrowLeft className="w-5 h-5 text-[var(--color-text-muted)] group-hover:text-[var(--color-rival-red)] group-hover:-translate-x-1 transition-all duration-300" />
            <div className="text-left">
              <div className="text-xs uppercase tracking-wider text-[var(--color-text-dim)] font-bold mb-1">Previous</div>
              <div className="font-bold text-[var(--color-text-primary)] group-hover:text-[var(--color-rival-red)] transition-colors duration-300">
                {prevTool.displayName}
              </div>
            </div>
          </Link>
        ) : (
          <div />
        )}
        
        {nextTool && (
          <Link
            to={`/tools/${nextTool.id}`}
            className="group flex items-center gap-3 px-5 py-4 rounded-xl bg-[var(--color-surface-2)] border border-[var(--color-border-subtle)] hover:border-[var(--color-rival-red)]/30 transition-all duration-300 hover:shadow-lg"
          >
            <div className="text-right">
              <div className="text-xs uppercase tracking-wider text-[var(--color-text-dim)] font-bold mb-1">Next</div>
              <div className="font-bold text-[var(--color-text-primary)] group-hover:text-[var(--color-rival-red)] transition-colors duration-300">
                {nextTool.displayName}
              </div>
            </div>
            <ArrowRight className="w-5 h-5 text-[var(--color-text-muted)] group-hover:text-[var(--color-rival-red)] group-hover:translate-x-1 transition-all duration-300" />
          </Link>
        )}
      </motion.nav>
    </div>
  )
}
