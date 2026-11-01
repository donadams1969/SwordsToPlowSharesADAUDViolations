'use client'

import { useMemo, useState } from 'react'
import type { Block } from '@/lib/case-data'

type TableBlock = Extract<Block, { type: 'table' }>

export function ContradictionsTable({ blocks }: { blocks: Block[] }) {
  const table = blocks.find((b): b is TableBlock => b.type === 'table' && b.rows[0]?.some((c) => c.toLowerCase().includes('contradicted')))
  const [query, setQuery] = useState('')

  const rows = useMemo(() => {
    if (!table) return []
    const body = table.rows.slice(1)
    const q = query.trim().toLowerCase()
    return q ? body.filter((r) => r.some((c) => c.toLowerCase().includes(q))) : body
  }, [table, query])

  if (!table) return null
  const header = table.rows[0]

  return (
    <div className="flex flex-col gap-4">
      <label className="flex flex-col gap-1 text-sm">
        <span className="text-muted-foreground">Filter the table (try &ldquo;Bates&rdquo;, &ldquo;locks&rdquo;, &ldquo;1161&rdquo;)</span>
        <input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search every cell"
          className="rounded border border-input bg-card px-3 py-2 text-foreground outline-none ring-ring placeholder:text-muted-foreground focus-visible:ring-2"
        />
      </label>
      <p className="text-xs text-muted-foreground">
        {rows.length} of {table.rows.length - 1} entries shown
      </p>
      <ul className="flex flex-col gap-3">
        {rows.map((r, i) => (
          <li key={i} className="grid grid-cols-1 gap-3 rounded border border-border bg-card p-4 md:grid-cols-3">
            {r.map((cell, j) => (
              <div key={j} className="flex flex-col gap-1">
                <span className="font-mono text-[11px] uppercase tracking-widest text-primary">{header[j]}</span>
                <span className="text-sm leading-relaxed text-card-foreground">{cell}</span>
              </div>
            ))}
          </li>
        ))}
        {rows.length === 0 && <li className="text-sm text-muted-foreground">No entries match that filter.</li>}
      </ul>
    </div>
  )
}
