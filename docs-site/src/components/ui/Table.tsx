import clsx from 'clsx'

interface TableProps {
  headers: string[]
  rows: (string | React.ReactNode)[][]
  className?: string
}

export default function Table({ headers, rows, className }: TableProps) {
  return (
    <div className={clsx('overflow-hidden rounded-2xl border border-[var(--color-border-subtle)] bg-[var(--color-surface-2)]', className)}>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="bg-[var(--color-surface-3)]">
              {headers.map((header, i) => (
                <th
                  key={i}
                  className="px-6 py-4 text-left text-xs font-black uppercase tracking-[0.1em] text-[var(--color-text-secondary)] border-b-2 border-[var(--color-rival-red)]/20"
                >
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, rowIndex) => (
              <tr
                key={rowIndex}
                className="group border-b border-[var(--color-border-subtle)]/30 last:border-b-0 hover:bg-[var(--color-surface-3)]/50 transition-colors duration-200"
              >
                {row.map((cell, cellIndex) => (
                  <td
                    key={cellIndex}
                    className="px-6 py-4 text-sm text-[var(--color-text-secondary)]"
                  >
                    {cell}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
