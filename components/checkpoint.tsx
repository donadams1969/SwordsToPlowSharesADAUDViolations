'use client'

import { useState } from 'react'
import { ChevronDown } from 'lucide-react'

export function Checkpoint({ shows, omits, asked }: { shows: string; omits: string; asked: string }) {
  const [open, setOpen] = useState(false)
  return (
    <section className="my-2 max-w-prose rounded-sm border border-border bg-card text-card-foreground" aria-label="Checkpoint">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        className="flex w-full items-center justify-between gap-4 px-4 py-3 text-left font-mono text-xs uppercase tracking-[0.18em] hover:bg-secondary/60"
      >
        <span>Checkpoint — shows · omits · asked</span>
        <ChevronDown className={`size-4 transition-transform ${open ? 'rotate-180' : ''}`} aria-hidden="true" />
      </button>
      {open && (
        <dl className="grid gap-4 border-t border-border px-4 py-4 text-sm leading-relaxed md:grid-cols-3">
          <div className="flex flex-col gap-1">
            <dt className="font-semibold text-primary">The record shows</dt>
            <dd className="text-muted-foreground">{shows}</dd>
          </div>
          <div className="flex flex-col gap-1">
            <dt className="font-semibold text-primary">The record omits</dt>
            <dd className="text-muted-foreground">{omits}</dd>
          </div>
          <div className="flex flex-col gap-1">
            <dt className="font-semibold text-primary">Asked of the Court</dt>
            <dd className="text-muted-foreground">{asked}</dd>
          </div>
        </dl>
      )}
    </section>
  )
}
