'use client'

import { useRef } from 'react'
import { X, ZoomIn } from 'lucide-react'
import type { Figure } from '@/lib/case-data'

export function RecordFigure({ id, figure }: { id: string; figure: Figure }) {
  const dialogRef = useRef<HTMLDialogElement>(null)
  const number = id.replace(/^F/, '')

  return (
    <figure id={`fig-${number}`} className="my-8 flex flex-col gap-3 scroll-mt-24">
      <button
        type="button"
        onClick={() => dialogRef.current?.showModal()}
        className="group relative overflow-hidden rounded-sm border border-border bg-paper p-2 text-left transition-colors hover:border-primary focus-visible:outline-2 focus-visible:outline-ring"
        aria-label={`Enlarge Figure ${number}`}
      >
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={figure.src} alt={`Figure ${number}: ${figure.caption}`} className="mx-auto max-h-[28rem] w-auto" loading="lazy" />
        <span className="absolute right-3 top-3 flex items-center gap-1 rounded-sm bg-background/85 px-2 py-1 text-xs text-foreground opacity-0 transition-opacity group-hover:opacity-100 group-focus-visible:opacity-100">
          <ZoomIn className="size-3.5" aria-hidden="true" /> Enlarge
        </span>
      </button>
      <figcaption className="flex flex-col gap-1 text-sm leading-relaxed text-muted-foreground">
        <span>
          <span className="font-mono text-xs uppercase tracking-wider text-primary">Figure {number}</span>
          <span className="ml-3 font-mono text-xs text-muted-foreground">{figure.page}</span>
        </span>
        <span>{figure.caption}</span>
      </figcaption>

      <dialog
        ref={dialogRef}
        className="m-auto max-h-[95vh] max-w-[95vw] bg-paper p-0 text-paper-foreground backdrop:bg-background/90"
        onClick={(e) => {
          if (e.target === dialogRef.current) dialogRef.current?.close()
        }}
      >
        <div className="flex flex-col gap-2 p-3">
          <div className="flex items-center justify-between gap-4">
            <p className="font-mono text-xs uppercase tracking-wider">
              Figure {number} · {figure.page}
            </p>
            <button
              type="button"
              onClick={() => dialogRef.current?.close()}
              className="rounded-sm p-1 hover:bg-paper-foreground/10 focus-visible:outline-2"
              aria-label="Close"
            >
              <X className="size-5" aria-hidden="true" />
            </button>
          </div>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={figure.src} alt={`Figure ${number}: ${figure.caption}`} className="max-h-[82vh] w-auto" />
          <p className="max-w-3xl text-sm leading-relaxed">{figure.caption}</p>
        </div>
      </dialog>
    </figure>
  )
}
