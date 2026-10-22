# Redbelly KYC and Wallet Activation Explainer (TASK-18)

A plain-language guide for the Redbelly community: do you need KYC, the five questions people ask most, how to get verified through Redbelly Access and Averer, and what to do when it goes wrong. Every fact links to an official page or to the Redbelly Access portal's own text.

Live: https://pykyc.vercel.app/
Last verified: 22 October 2026.

## Deliverables

| # | Deliverable | File |
|---|---|---|
| 1 | The guide, Parts A to D | `index.html` (live site). PDF: `KYC-and-Wallet-Activation-Explainer.pdf` |
| 2 | Part A decision guide as an image | `decision-guide.png` (1080 x 1080, X square post size). Source: `src/decision-guide.html` |
| 3 | Short version for pinning in Discord or Telegram | `pin.txt`, posted with `decision-guide.png`. Same wording as questions 2, 3 and 4 |
| 4 | Source list with a link for every fact | "Sources" section of the guide (S1 to S19, E1 to E5), `sources.md`, `evidence.html` and `evidence/` |

Also: `img/og.png` (1200 x 630) is the Discord and Open Graph preview for the link.

## What changed in this version

- Pin and questions 2 and 3 use the same sentences. A script checks that they match.
- Approval time and the 10 wallet limit come from the portal's own text: "This could take a few minutes but in some (rare) cases it could take a few days." and "Account allocation exhausted." at `Number("10")`.
- Button names are the live ones: Connect wallet, Begin identity verification, I understand, Continue with Averer, Check verification status, Enable account, RETRY, Add another account, Link another wallet.
- The Averer link goes to the ticket form (`/support/tickets/new`), and the guide lists its real fields.
- The 5 July 2026 Snapshot vote is cited (S10) with its result, saved from the Snapshot API.
- The task brief and the community dev.to post are no longer sources. Every source is an official page, the portal, or the DAO vote.
- Redbelly DAO Task Board brand kit: Be Vietnam Pro and JetBrains Mono, the official colour tokens for dark and light, the official logo files with no plate, status shown as a dot plus a mono label, no em or en dashes, no emoji, and a dated "last verified" line on every graphic.

## How the facts were checked

- **Portal text (E1 to E5):** read from the two public JavaScript files of https://access.redbelly.network/, with SHA-256 hashes and search strings in `evidence/access-portal-text.md` and `evidence.html`.
- **DAO vote (S10):** Snapshot GraphQL API, saved in `evidence/snapshot-proposal.json`.
- **Terms clause 15 (S11):** saved in `evidence/terms-clause-15.txt`.
- **Averer ticket form (S18):** field list saved in `evidence/averer-ticket-form.json`.
- **DAO voting needs KYC (S15):** governance site notice, saved in `evidence/governance-kyc-notice.md`.
- All other pages: vine.redbelly.network, docs.redbelly.network, redbelly.network and averer.co, opened on 22 October 2026.

## Build and check

Everything derived is built from one source, so the page, pin, PDF and images cannot drift apart.

```
node scripts/build.mjs              # pin.txt, decision-guide.png, img/og.png, the PDF (needs playwright + Chromium)
python3 scripts/check.py            # dashes, emoji, credit, sources cited, anchors, pin matches guide (needs pdftotext)
python3 scripts/check.py --online   # also checks every external link and re-reads the portal files
```

## Files

```
index.html, style.css, evidence.html     the site
pin.txt, decision-guide.png, img/og.png  sharing assets
KYC-and-Wallet-Activation-Explainer.pdf  print version
sources.md                               source list as plain text
evidence/                                saved copies of the official text
src/                                     editable sources for the images
scripts/                                 build and check
fonts/                                   Be Vietnam Pro and JetBrains Mono (SIL Open Font License)
img/                                     official Redbelly DAO logos from the brand kit
```

Deploys as a static site. No build step is needed on Vercel.
