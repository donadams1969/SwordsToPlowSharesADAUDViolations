'use client'

import { useEffect, useState } from 'react'
import { TRIAL_CALL } from '@/lib/case-data'

function format(ms: number) {
  if (ms <= 0) return 'Trial call has begun'
  const h = Math.floor(ms / 3_600_000)
  const d = Math.floor(h / 24)
  const m = Math.floor((ms % 3_600_000) / 60_000)
  return d > 0 ? `${d}d ${h % 24}h ${m}m to trial call` : `${h}h ${m}m to trial call`
}

export function TrialCountdown() {
  const [label, setLabel] = useState<string | null>(null)
  useEffect(() => {
    const tick = () => setLabel(format(TRIAL_CALL.getTime() - Date.now()))
    tick()
    const id = setInterval(tick, 30_000)
    return () => clearInterval(id)
  }, [])
  return (
    <p className="rounded-sm border border-primary/40 px-3 py-1.5 font-mono text-xs text-primary" aria-live="polite">
      Nov. 2, 2026 · 9:00 a.m. · Dept. 606{label ? ` · ${label}` : ''}
    </p>
  )
}
