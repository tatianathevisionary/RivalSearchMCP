import { motion } from 'framer-motion'
import clsx from 'clsx'

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  children: React.ReactNode
  className?: string
  onClick?: () => void
  disabled?: boolean
  type?: 'button' | 'submit' | 'reset'
}

export default function Button({ 
  variant = 'primary', 
  size = 'md', 
  className, 
  children, 
  onClick,
  disabled,
  type = 'button'
}: ButtonProps) {
  const baseStyles = 'inline-flex items-center justify-center font-medium rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-[var(--color-surface-0)]'
  
  const variants = {
    primary: 'bg-gradient-to-r from-[var(--color-rival-red)] to-[var(--color-rival-red-dark)] text-white hover:shadow-[0_0_20px_rgba(220,38,38,0.4)] focus:ring-[var(--color-rival-red)]',
    secondary: 'bg-[var(--color-surface-3)] text-[var(--color-text-primary)] border border-[var(--color-border-subtle)] hover:bg-[var(--color-surface-4)] hover:border-[var(--color-border-default)] focus:ring-[var(--color-border-default)]',
    ghost: 'text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] hover:bg-[var(--color-surface-2)] focus:ring-[var(--color-border-subtle)]',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
  }

  const sizes = {
    sm: 'px-3 py-1.5 text-sm gap-1.5',
    md: 'px-4 py-2 text-sm gap-2',
    lg: 'px-6 py-3 text-base gap-2.5',
  }

  return (
    <motion.button
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
      className={clsx(baseStyles, variants[variant], sizes[size], className)}
      onClick={onClick}
      disabled={disabled}
      type={type}
    >
      {children}
    </motion.button>
  )
}
