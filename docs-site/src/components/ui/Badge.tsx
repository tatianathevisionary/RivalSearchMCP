import clsx from 'clsx'

interface BadgeProps {
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'info'
  children: React.ReactNode
  className?: string
}

export default function Badge({ variant = 'default', children, className }: BadgeProps) {
  const variants = {
    default: 'bg-[var(--color-surface-3)] text-[var(--color-text-secondary)] border-[var(--color-border-subtle)]',
    success: 'bg-green-500/10 text-green-400 border-green-500/20',
    warning: 'bg-amber-500/10 text-amber-400 border-amber-500/20',
    danger: 'bg-red-500/10 text-red-400 border-red-500/20',
    info: 'bg-blue-500/10 text-blue-400 border-blue-500/20',
  }

  return (
    <span
      className={clsx(
        'inline-flex items-center px-2 py-0.5 text-xs font-medium rounded-md border',
        variants[variant],
        className
      )}
    >
      {children}
    </span>
  )
}
