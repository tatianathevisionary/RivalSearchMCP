import { useState } from 'react'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { Check, Copy } from 'lucide-react'
import clsx from 'clsx'

interface CodeBlockProps {
  code: string
  language?: string
  filename?: string
  showLineNumbers?: boolean
  className?: string
}

export default function CodeBlock({
  code,
  language = 'typescript',
  filename,
  showLineNumbers = false,
  className,
}: CodeBlockProps) {
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    await navigator.clipboard.writeText(code)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  // Custom dark theme with red/amber accents
  const customTheme = {
    ...vscDarkPlus,
    'pre[class*="language-"]': {
      background: 'var(--color-surface-3)',
      margin: 0,
      padding: '1.25rem',
      fontSize: '0.875rem',
      lineHeight: '1.75',
      borderRadius: '0',
    },
    'code[class*="language-"]': {
      background: 'transparent',
      fontFamily: 'var(--font-mono)',
    },
    'token.keyword': {
      color: '#dc2626',
    },
    'token.string': {
      color: '#f59e0b',
    },
    'token.function': {
      color: '#3b82f6',
    },
    'token.number': {
      color: '#22c55e',
    },
  }

  return (
    <div className={clsx('relative group rounded-2xl overflow-hidden border border-[var(--color-border-subtle)] bg-[var(--color-surface-2)]', className)}>
      {/* Terminal header */}
      <div className="flex items-center justify-between px-5 py-3 bg-[var(--color-surface-3)] border-b border-[var(--color-border-subtle)]">
        <div className="flex items-center gap-4">
          {/* macOS window controls */}
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full bg-[#ff5f56] shadow-[0_0_8px_rgba(255,95,86,0.4)]" />
            <div className="w-3 h-3 rounded-full bg-[#ffbd2e] shadow-[0_0_8px_rgba(255,189,46,0.4)]" />
            <div className="w-3 h-3 rounded-full bg-[#27c93f] shadow-[0_0_8px_rgba(39,201,63,0.4)]" />
          </div>
          
          {filename && (
            <span className="text-sm font-mono text-[var(--color-text-muted)] font-medium">
              {filename}
            </span>
          )}
        </div>

        <div className="flex items-center gap-3">
          {language && (
            <span className="text-xs font-mono font-bold uppercase tracking-wider text-[var(--color-text-dim)] px-2 py-1 rounded bg-[var(--color-surface-2)]">
              {language}
            </span>
          )}
        </div>
      </div>

      {/* Code area */}
      <div className="relative">
        <SyntaxHighlighter
          language={language}
          style={customTheme}
          showLineNumbers={showLineNumbers}
          customStyle={{
            margin: 0,
            background: 'var(--color-surface-3)',
          }}
          lineNumberStyle={{
            color: 'var(--color-text-dim)',
            paddingRight: '1.5rem',
            minWidth: '3rem',
            userSelect: 'none',
          }}
          codeTagProps={{
            style: {
              fontFamily: 'var(--font-mono)',
              fontSize: '0.875rem',
            }
          }}
        >
          {code.trim()}
        </SyntaxHighlighter>

        {/* Copy button - enhanced */}
        <button
          onClick={handleCopy}
          className={clsx(
            'absolute top-4 right-4 p-2.5 rounded-lg transition-all duration-300',
            'bg-[var(--color-surface-2)]/90 backdrop-blur-sm border border-[var(--color-border-subtle)]',
            'opacity-0 group-hover:opacity-100',
            'hover:bg-[var(--color-surface-4)] hover:border-[var(--color-border-default)] hover:shadow-lg',
            copied && 'opacity-100 bg-green-500/10 border-green-500/30'
          )}
          aria-label={copied ? 'Copied' : 'Copy code'}
        >
          {copied ? (
            <Check className="w-4 h-4 text-green-400" />
          ) : (
            <Copy className="w-4 h-4 text-[var(--color-text-muted)]" />
          )}
        </button>
      </div>
    </div>
  )
}
