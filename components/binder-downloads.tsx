import { Download, FileText } from 'lucide-react'
import { BINDERS } from '@/lib/case-data'

export function BinderDownloads() {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      {BINDERS.map((b) => (
        <article key={b.id} className="flex flex-col gap-4 rounded-sm border border-border bg-card p-5">
          <header className="flex flex-col gap-1">
            <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-muted-foreground">{b.court}</p>
            <h3 className="font-serif text-xl font-bold leading-tight text-balance">{b.title}</h3>
            <p className="text-sm text-muted-foreground">
              {b.caseNo} · {b.pages} pages · final build
            </p>
          </header>
          <ol className="flex flex-col gap-1 text-sm">
            {b.tabs.map(([letter, label]) => (
              <li key={letter} className="flex gap-3">
                <span className="w-5 shrink-0 font-mono text-xs text-primary">{letter}</span>
                <span className="text-pretty text-muted-foreground">{label}</span>
              </li>
            ))}
          </ol>
          <a
            href={b.href}
            download={b.file}
            className="mt-auto inline-flex items-center justify-center gap-2 rounded-sm bg-primary px-4 py-2.5 text-sm font-semibold text-primary-foreground transition-colors hover:bg-primary/90 focus-visible:outline-2 focus-visible:outline-ring"
          >
            <Download className="size-4" aria-hidden />
            Download the {b.id === 'sf' ? 'San Francisco' : 'Solano County'} binder (PDF)
          </a>
        </article>
      ))}
      <p className="flex items-start gap-2 text-xs leading-relaxed text-muted-foreground md:col-span-2">
        <FileText className="mt-0.5 size-4 shrink-0" aria-hidden />
        Each binder is one bookmarked, Bates-numbered PDF with a tabbed table of contents. Tab J (San Francisco) and Tab B (Solano) contain a medical exhibit that is
        confidential under Cal. Rules of Court, rule 1.100(c)(4). Share these links only with the court, counsel, and your advocates.
      </p>
    </div>
  )
}
