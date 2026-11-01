'use client'

import { useEffect, useState } from 'react'
import { TRIAL_CALL } from '@/lib/case-data'

function remaining(now: number) {
  const ms = Math.max(0, TRIAL_CALL.getTime() - now)
  const h = Math.floor(ms / 3_600_000)
  const m = Math.floor((ms % 3_600_000) / 60_000)
  return { days: Math.floor(h / 24), hours: h % 24, minutes: m, past: ms === 0 }
}

export function TrialClock() {
  const [now, setNow] = useState<number | null>(null)

  useEffect(() => {
    setNow(Date.now())
    const id = setInterval(() => setNow(Date.now()), 30_000)
    return () => clearInterval(id)
  }, [])

  const r = now === null ? null : remaining(now)

  return (
    <div className="flex flex-col gap-1 rounded border border-border bg-card p-4">
      <span className="font-mono text-[11px] uppercase tracking-widest text-muted-foreground">Trial call · Dept. 606</span>
      <span className="font-serif text-lg font-bold">Monday, November 2, 2026 · 9:00 a.m.</span>
      <span className="text-sm text-muted-foreground" aria-live="polite">
        {r === null ? 'Computing time remaining…' : r.past ? 'Trial call has passed.' : `${r.days} days, ${r.hours} hours, ${r.minutes} minutes remaining`}
      </span>
    </div>
  )
}
