'use client'

import { useEffect, useState } from 'react'
import { Menu, X } from 'lucide-react'

export type NavSection = { id: string; label: string; children?: { id: string; text: string }[] }

export function SiteNav({ sections }: { sections: NavSection[] }) {
  const [active, setActive] = useState(sections[0]?.id)
  const [open, setOpen] = useState(false)

  useEffect(() => {
    const ids = sections.flatMap((s) => [s.id, ...(s.children?.map((c) => c.id) ?? [])])
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries.filter((e) => e.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)
        if (visible[0]) setActive(visible[0].target.id)
      },
      { rootMargin: '-20% 0px -70% 0px' },
    )
    ids.forEach((id) => {
      const el = document.getElementById(id)
      if (el) observer.observe(el)
    })
    return () => observer.disconnect()
  }, [sections])

  const list = (
    <ol className="flex flex-col gap-1 text-sm">
      {sections.map((s) => {
        const isActive = active === s.id || s.children?.some((c) => c.id === active)
        return (
          <li key={s.id}>
            <a
              href={`#${s.id}`}
              onClick={() => setOpen(false)}
              aria-current={isActive ? 'location' : undefined}
              className={`block border-l-2 py-1.5 pl-3 transition-colors ${isActive ? 'border-primary text-foreground' : 'border-transparent text-muted-foreground hover:text-foreground'}`}
            >
              {s.label}
            </a>
            {s.children && isActive && (
              <ol className="mb-2 flex flex-col gap-0.5 pl-3">
                {s.children.map((c) => (
                  <li key={c.id}>
                    <a
                      href={`#${c.id}`}
                      onClick={() => setOpen(false)}
                      className={`block truncate border-l py-1 pl-3 text-xs ${active === c.id ? 'border-primary text-foreground' : 'border-border text-muted-foreground hover:text-foreground'}`}
                    >
                      {c.text}
                    </a>
                  </li>
                ))}
              </ol>
            )}
          </li>
        )
      })}
    </ol>
  )

  return (
    <>
      <nav aria-label="Binder contents" className="hidden lg:block">
        <p className="mb-3 font-mono text-[11px] uppercase tracking-[0.2em] text-muted-foreground">Contents</p>
        {list}
      </nav>
      <div className="lg:hidden">
        <button
          type="button"
          onClick={() => setOpen((o) => !o)}
          aria-expanded={open}
          aria-controls="mobile-contents"
          className="flex items-center gap-2 rounded-sm border border-border bg-card px-3 py-2 text-sm"
        >
          {open ? <X className="size-4" aria-hidden /> : <Menu className="size-4" aria-hidden />}
          Contents
        </button>
        {open && (
          <nav id="mobile-contents" aria-label="Binder contents" className="mt-2 rounded-sm border border-border bg-card p-3">
            {list}
          </nav>
        )}
      </div>
    </>
  )
}
