import type { Block, Figure, TextBlock } from '@/lib/case-data'
import { RecordFigure } from './record-figure'
import { Checkpoint } from './checkpoint'

const slug = (t: string) =>
  t
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '')
    .slice(0, 60)

export function headingsOf(blocks: Block[]) {
  return blocks.filter((b): b is TextBlock => b.type === 'h2').map((b) => ({ id: slug(b.text), text: b.text }))
}

/** Turns "Fig. 7", "Figs. 7–10", "Tab K", "R07" into links/pills. */
function RichText({ text }: { text: string }) {
  const parts = text.split(/(Figs?\. \d+(?:[–-]\d+)?(?:, \d+)*|\bR\d{2}\b|\bTab [A-M]\b)/g)
  return (
    <>
      {parts.map((part, i) => {
        if (/^Figs?\. \d+/.test(part)) {
          const first = part.match(/\d+/)?.[0]
          return (
            <a key={i} href={`#fig-${first}`} className="text-primary underline decoration-primary/40 underline-offset-4 hover:decoration-primary">
              {part}
            </a>
          )
        }
        if (/^R\d{2}$/.test(part) || /^Tab [A-M]$/.test(part)) {
          return (
            <span key={i} className="rounded-sm border border-border bg-secondary px-1 py-0.5 font-mono text-[0.8em] text-secondary-foreground">
              {part}
            </span>
          )
        }
        return <span key={i}>{part}</span>
      })}
    </>
  )
}

export function ContentBlocks({ blocks, figures, numbered = true }: { blocks: Block[]; figures: Record<string, Figure>; numbered?: boolean }) {
  let n = 0
  return (
    <div className="flex flex-col gap-4">
      {blocks.map((b, i) => {
        switch (b.type) {
          case 'phase':
            return (
              <p key={i} className="mt-8 font-mono text-xs uppercase tracking-[0.2em] text-muted-foreground">
                {b.text}
              </p>
            )
          case 'h2':
            return (
              <h2 key={i} id={slug(b.text)} className="mt-6 scroll-mt-24 font-serif text-2xl font-bold leading-tight text-balance md:text-3xl">
                {b.text}
              </h2>
            )
          case 'h3':
            return (
              <h3 key={i} className="mt-4 font-serif text-lg font-bold leading-snug text-balance md:text-xl">
                {b.text}
              </h3>
            )
          case 'n': {
            n += 1
            return (
              <p key={i} className="max-w-prose text-[15px] leading-relaxed md:text-base">
                {numbered && <span className="mr-2 font-mono text-xs text-primary">{n}.</span>}
                <RichText text={b.text} />
              </p>
            )
          }
          case 'p':
            return (
              <p key={i} className="max-w-prose text-[15px] leading-relaxed md:text-base">
                <RichText text={b.text} />
              </p>
            )
          case 'box':
            return (
              <blockquote key={i} className="max-w-prose border border-primary/50 bg-card px-5 py-4 text-sm leading-relaxed text-card-foreground">
                <RichText text={b.text} />
              </blockquote>
            )
          case 'fig':
            return figures[b.key] ? <RecordFigure key={i} id={b.key} figure={figures[b.key]} /> : null
          case 'chk':
            return <Checkpoint key={i} shows={b.shows} omits={b.omits} asked={b.asked} />
          case 'table':
            return (
              <div key={i} className="overflow-x-auto rounded-sm border border-border">
                <table className="w-full min-w-[36rem] text-sm">
                  <thead className="bg-secondary text-left text-secondary-foreground">
                    <tr>
                      {b.rows[0].map((c, j) => (
                        <th key={j} scope="col" className="px-3 py-2 font-semibold">
                          {c}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {b.rows.slice(1).map((r, k) => (
                      <tr key={k} className="border-t border-border align-top">
                        {r.map((c, j) => (
                          <td key={j} className="px-3 py-2 leading-relaxed">
                            <RichText text={c} />
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )
        }
      })}
    </div>
  )
}
