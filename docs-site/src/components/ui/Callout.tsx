import { AlertCircle, CheckCircle, Info, AlertTriangle, Lightbulb } from 'lucide-react'
import clsx from 'clsx'

interface CalloutProps {
  type?: 'info' | 'success' | 'warning' | 'danger' | 'tip'
  title?: string
  children: React.ReactNode
  className?: string
}

export default function Callout({ type = 'info', title, children, className }: CalloutProps) {
  const config = {
    info: {
      icon: Info,
      bg: 'bg-blue-500/5',
      border: 'border-blue-500/30',
      iconBg: 'bg-blue-500/10',
      iconColor: 'text-blue-400',
      titleColor: 'text-blue-300',
      accentBar: 'bg-blue-500',
    },
    success: {
      icon: CheckCircle,
      bg: 'bg-green-500/5',
      border: 'border-green-500/30',
      iconBg: 'bg-green-500/10',
      iconColor: 'text-green-400',
      titleColor: 'text-green-300',
      accentBar: 'bg-green-500',
    },
    warning: {
      icon: AlertTriangle,
      bg: 'bg-amber-500/5',
      border: 'border-amber-500/30',
      iconBg: 'bg-amber-500/10',
      iconColor: 'text-amber-400',
      titleColor: 'text-amber-300',
      accentBar: 'bg-amber-500',
    },
    danger: {
      icon: AlertCircle,
      bg: 'bg-red-500/5',
      border: 'border-red-500/30',
      iconBg: 'bg-red-500/10',
      iconColor: 'text-red-400',
      titleColor: 'text-red-300',
      accentBar: 'bg-red-500',
    },
    tip: {
      icon: Lightbulb,
      bg: 'bg-purple-500/5',
      border: 'border-purple-500/30',
      iconBg: 'bg-purple-500/10',
      iconColor: 'text-purple-400',
      titleColor: 'text-purple-300',
      accentBar: 'bg-purple-500',
    },
  }

  const { icon: Icon, bg, border, iconBg, iconColor, titleColor, accentBar } = config[type]

  return (
    <div
      className={clsx(
        'relative flex gap-4 p-5 rounded-xl border backdrop-blur-sm',
        bg,
        border,
        className
      )}
    >
      {/* Left accent bar */}
      <div className={clsx('absolute left-0 top-4 bottom-4 w-1 rounded-full', accentBar)} />
      
      {/* Icon */}
      <div className={clsx('shrink-0 w-10 h-10 rounded-xl flex items-center justify-center', iconBg)}>
        <Icon className={clsx('w-5 h-5', iconColor)} />
      </div>
      
      {/* Content */}
      <div className="flex-1 min-w-0 pt-0.5">
        {title && (
          <p className={clsx('font-bold mb-2 text-base', titleColor)}>{title}</p>
        )}
        <div className="text-sm text-[var(--color-text-secondary)] leading-relaxed [&_code]:text-xs [&_code]:bg-[var(--color-surface-4)] [&_code]:px-1.5 [&_code]:py-0.5 [&_code]:rounded [&_a]:text-[var(--color-rival-red)] [&_a]:font-semibold [&_a:hover]:underline">
          {children}
        </div>
      </div>
    </div>
  )
}
