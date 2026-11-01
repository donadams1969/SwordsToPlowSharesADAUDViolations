import { caseData } from '@/lib/case-data'
import { ContentBlocks, headingsOf } from '@/components/content-blocks'
import { SiteNav, type NavSection } from '@/components/site-nav'
import { BinderDownloads } from '@/components/binder-downloads'
import { TrialCountdown } from '@/components/trial-countdown'
import { FigureStrip } from '@/components/figure-strip'

export default function Page() {
  const { statement, notice, motion, brief, figures, noticeTitle, motionTitle, briefTitle } = caseData
  const sections: NavSection[] = [
    { id: 'overview', label: 'Overview' },
    { id: 'record', label: 'The record in 14 figures' },
    { id: 'brief', label: 'Master trial brief (lead document)', children: headingsOf(brief) },
    { id: 'notice', label: 'Notice and verified statement', children: headingsOf(notice) },
    { id: 'motion', label: 'Motion in Limine No. 1', children: headingsOf(motion) },
    { id: 'statement', label: 'Integrated statement of the case', children: headingsOf(statement) },
    { id: 'downloads', label: 'Download the binders' },
  ]

  return (
    <div className="mx-auto flex w-full max-w-7xl flex-col gap-8 px-4 py-6 md:px-8 md:py-10">
      <header className="flex flex-col gap-6 border-b border-border pb-8">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-muted-foreground">
            Superior Court of California · San Francisco · CUD-26-682107 · Related CCH-26-589086
          </p>
          <TrialCountdown />
        </div>
        <div className="flex flex-col gap-4">
          <h1 className="max-w-4xl font-serif text-3xl font-bold leading-[1.1] text-balance md:text-5xl">
            Swords to Plowshares v. Gillson: the record, in the order it happened.
          </h1>
          <p className="max-w-prose text-base leading-relaxed text-muted-foreground md:text-lg">
            A disabled veteran&apos;s trial binder, published as a navigable record. Every statement below is pinned to a Bates page, a filed
            document (R01&ndash;R10), or a tab of the binder. Click any figure to read the source page at full size.
          </p>
        </div>
      </header>

      <div className="flex flex-col gap-10 lg:grid lg:grid-cols-[14rem_minmax(0,1fr)] lg:gap-12">
        <aside className="lg:sticky lg:top-6 lg:self-start">
          <SiteNav sections={sections} />
        </aside>

        <main className="flex min-w-0 flex-col gap-16">
          <section id="overview" aria-labelledby="overview-h" className="flex flex-col gap-4 scroll-mt-24">
            <h2 id="overview-h" className="font-serif text-2xl font-bold md:text-3xl">
              What this site holds
            </h2>
            <div className="grid gap-3 sm:grid-cols-3">
              {[
                ['Notice', 'Government Claims, Request for Judicial Notice, Verified Statement of Disqualification, federal rights and reservation of removal.'],
                ['Motion in Limine No. 1', 'Disqualify plaintiff\u2019s director-lawyer and firm; exclude evidence derived from confidential VA information; rule 1.100 accommodation.'],
                ['Integrated Statement', 'The chronology, the contradictions table, the check-points, and 14 figures cut from the filed record itself.'],
              ].map(([t, d]) => (
                <div key={t} className="flex flex-col gap-2 rounded-sm border border-border bg-card p-4">
                  <h3 className="font-serif text-lg font-bold leading-snug">{t}</h3>
                  <p className="text-sm leading-relaxed text-muted-foreground text-pretty">{d}</p>
                </div>
              ))}
            </div>
            <p className="max-w-prose text-sm leading-relaxed text-muted-foreground">
              The assistive-technology record system that produced these papers is this application. It is the repository of every communication,
              filing and timestamp in the case, and the Notice asks that it be treated as protected work product and assistive technology.
            </p>
          </section>

          <section id="record" aria-labelledby="record-h" className="flex flex-col gap-4 scroll-mt-24">
            <h2 id="record-h" className="font-serif text-2xl font-bold md:text-3xl">
              The record in 14 figures
            </h2>
            <FigureStrip figures={figures} />
          </section>

          <section id="brief" aria-labelledby="brief-h" className="flex flex-col gap-6 scroll-mt-24 border-t border-border pt-10">
            <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary">Exhibit A-1 · Lead document</p>
            <h2 id="brief-h" className="font-serif text-2xl font-bold leading-tight text-balance md:text-3xl">
              Master Integrated Statement of the Case and Trial Brief
            </h2>
            <p className="max-w-prose text-sm leading-relaxed text-muted-foreground">{briefTitle.join(' ')}</p>
            <ContentBlocks blocks={brief} figures={figures} />
          </section>

          <section id="notice" aria-labelledby="notice-h" className="flex flex-col gap-6 scroll-mt-24 border-t border-border pt-10">
            <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary">Exhibit A-2 · Notice</p>
            <h2 id="notice-h" className="font-serif text-2xl font-bold leading-tight text-balance md:text-3xl">
              {noticeTitle.join(' ')}
            </h2>
            <ContentBlocks blocks={notice} figures={figures} />
          </section>

          <section id="motion" aria-labelledby="motion-h" className="flex flex-col gap-6 scroll-mt-24 border-t border-border pt-10">
            <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary">Tab A · Emergency motion</p>
            <h2 id="motion-h" className="font-serif text-2xl font-bold leading-tight text-balance md:text-3xl">
              {motionTitle.slice(0, 3).join(' ')}
            </h2>
            <ContentBlocks blocks={motion} figures={figures} />
          </section>

          <section id="statement" aria-labelledby="statement-h" className="flex flex-col gap-6 scroll-mt-24 border-t border-border pt-10">
            <p className="font-mono text-[11px] uppercase tracking-[0.2em] text-primary">Tab A · Integrated statement</p>
            <h2 id="statement-h" className="font-serif text-2xl font-bold leading-tight text-balance md:text-3xl">
              Defendant&apos;s Integrated Statement of the Case
            </h2>
            <ContentBlocks blocks={statement} figures={figures} />
          </section>

          <section id="downloads" aria-labelledby="downloads-h" className="flex flex-col gap-6 scroll-mt-24 border-t border-border pt-10">
            <h2 id="downloads-h" className="font-serif text-2xl font-bold md:text-3xl">
              Download the binders
            </h2>
            <BinderDownloads />
          </section>
        </main>
      </div>

      <footer className="border-t border-border pt-6 text-xs leading-relaxed text-muted-foreground">
        Donald Ernest Gillson, Ed.D., Defendant in Pro Per · 1030 Girard Road, Unit 301A, San Francisco, CA 94129 · Prepared and signed October 31, 2026.
        Bracketed items in the motion are facts only the defendant can supply before filing.
      </footer>
    </div>
  )
}
