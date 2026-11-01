import { Analytics } from '@vercel/analytics/next'
import type { Metadata, Viewport } from 'next'
import { Geist, Libre_Baskerville } from 'next/font/google'
import './globals.css'

const _geist = Geist({ subsets: ['latin'] })
const _baskerville = Libre_Baskerville({ subsets: ['latin'], weight: ['400', '700'], style: ['normal', 'italic'] })

export const metadata: Metadata = {
  title: 'Gillson v. Swords to Plowshares — The Record, CUD-26-682107',
  description:
    'Interactive trial record: Notice of Government Claims and Disqualification, Integrated Statement of the Case with the filed record embedded as fourteen figures, and the two all-in-one binders (San Francisco and Solano County).',
  generator: 'v0.app',
  icons: {
    icon: [
      { url: '/icon-light-32x32.png', media: '(prefers-color-scheme: light)' },
      { url: '/icon-dark-32x32.png', media: '(prefers-color-scheme: dark)' },
      { url: '/icon.svg', type: 'image/svg+xml' },
    ],
    apple: '/apple-icon.png',
  },
}

export const viewport: Viewport = {
  colorScheme: 'dark',
  themeColor: '#1a2130',
}

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className="bg-background">
      <body className="antialiased font-sans bg-background text-foreground">
        {children}
        {process.env.NODE_ENV === 'production' && <Analytics />}
      </body>
    </html>
  )
}
