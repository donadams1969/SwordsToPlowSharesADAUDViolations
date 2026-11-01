import raw from './case-data.json'

export type Block =
  | { type: 'h2' | 'h3' | 'p' | 'n' | 'phase' | 'box'; text: string }
  | { type: 'fig'; key: string }
  | { type: 'chk'; shows: string; omits: string; asked: string }
  | { type: 'table'; rows: string[][] }

export type Figure = { src: string; caption: string; page: number | string }
export type TextBlock = Extract<Block, { text: string }>

export type CaseData = {
  figures: Record<string, Figure>
  statement: Block[]
  notice: Block[]
  noticeTitle: string[]
  motion: Block[]
  motionTitle: string[]
  brief: Block[]
  briefTitle: string[]
}

export const caseData = raw as CaseData

export const TRIAL_CALL = new Date('2026-11-02T09:00:00-08:00')

export const BINDERS = [
  {
    id: 'sf',
    court: 'Superior Court of California, County of San Francisco',
    title: 'All-in-One Trial Binder — San Francisco',
    caseNo: 'CUD-26-682107 · Dept. 606',
    href: '/binders/san-francisco-final-355pp.pdf',
    file: 'Gillson_FINAL_All_In_One_Trial_Binder_SAN_FRANCISCO_CUD-26-682107.pdf',
    pages: 355,
    tabs: [
      ['A', 'Opening Papers: Notice, Master Trial Brief, Motion in Limine No. 1, Streamlined Statement of the Case'],
      ['B', 'Index of Record Irregularities and Indicia of Fraud'],
      ['C', 'Witness List'],
      ['D', 'Evidence List'],
      ['E', 'Video List'],
      ['F', 'Points and Authorities'],
      ['G', 'Closing Argument'],
      ['H', 'Record References – Chronology of the Filed Court Record (R01–R10), key pages only'],
      ['I', 'Notice to Counsel and Civil Subpoenas'],
      ['J', 'Request for Accommodations – MC-410 – Confidential in part'],
      ['K', 'Rule 1.100 Orders and Responses of this Court'],
      ['L', 'Evidence Exhibit Binder – Photographs, Notices, Agency Records, Video Links, VA Medical Excerpts'],
      ['M', 'Related Administrative Complaints'],
    ],
  },
  {
    id: 'solano',
    court: 'Superior Court of California, County of Solano',
    title: 'All-in-One Binder — Solano County',
    caseNo: 'Civil harassment petition (Code Civ. Proc., § 527.6)',
    href: '/binders/solano-final-306pp.pdf',
    file: 'Gillson_FINAL_All_In_One_Binder_SOLANO_COUNTY.pdf',
    pages: 306,
    tabs: [
      ['A', 'Ex Parte Application for Order Shortening Time; Rule 1.100 Request'],
      ['B', 'Request for Accommodations – MC-410 (Solano) – Confidential in part'],
      ['C', 'Course of Conduct – Opening Notice, Master Trial Brief and Integrated Statement (San Francisco)'],
      ['D', 'Index of Record Irregularities (San Francisco record)'],
      ['E', 'Video Evidence – Audio-Visual Exhibits'],
      ['F', 'Points and Authorities'],
      ['G', 'Record References – Chronology of the San Francisco Court Record (R01–R10), key pages only'],
      ['H', 'San Francisco Rule 1.100 Orders and Responses'],
      ['I', 'Evidence Exhibit Binder'],
      ['J', 'Related Administrative Complaints'],
    ],
  },
] as const
