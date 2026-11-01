import Image from 'next/image'
import type { Figure } from '@/lib/case-data'

export function FigureStrip({ figures }: { figures: Record<string, Figure> }) {
  const entries = Object.entries(figures).sort(([a], [b]) => Number(a.replace(/\D/g, '')) - Number(b.replace(/\D/g, '')))
  return (
    <ol className="grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-7">
      {entries.map(([key, f]) => {
        const n = key.replace(/\D/g, '')
        return (
          <li key={key}>
            <a href={`#fig-${n}`} className="group flex flex-col gap-2 focus-visible:outline-2 focus-visible:outline-ring">
              <span className="relative block aspect-[3/4] overflow-hidden rounded-sm border border-border bg-paper transition-colors group-hover:border-primary">
                <Image src={f.src} alt={`Figure ${n}: ${f.caption}`} fill sizes="(min-width: 1024px) 12vw, 40vw" className="object-cover object-top" />
              </span>
              <span className="flex flex-col gap-0.5">
                <span className="font-mono text-[11px] text-primary">Fig. {n}</span>
                <span className="line-clamp-2 text-xs leading-snug text-muted-foreground">{f.caption.replace(/^Figure \d+\.\s*/, '')}</span>
              </span>
            </a>
          </li>
        )
      })}
    </ol>
  )
}
