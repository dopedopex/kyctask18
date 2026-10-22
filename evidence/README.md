# Evidence

Saved copies of the official text the guide relies on, captured on 22 October 2026, so a reviewer can check every claim even if a live page changes.

| File | What it holds | Live source |
|---|---|---|
| access-portal-text.md | Redbelly Access on-screen text (E1 to E5): wallet limit, approval time, button names, FAQ. File names, SHA-256 hashes and search strings. | https://access.redbelly.network/ |
| snapshot-proposal.json | The DAO vote that removed regional limits for general members: title, dates, result, and the proposal's Summary. Read from the Snapshot API. | https://snapshot.box/#/s:rbnt.eth/proposal/0xa57ccc9a6d554c9e5a1b1ca429ad2affc2e9058f12ea50bce999460f2aea4e02 |
| terms-clause-15.txt | Clause 15 of the Redbelly Network terms (restricted jurisdictions) | https://redbelly.network/terms-and-conditions |
| averer-ticket-form.json | The fields on Averer's ticket form, read from the form page | https://averer-help.freshdesk.com/support/tickets/new |
| governance-kyc-notice.md | The DAO governance site's notice that voting needs a verified, enabled wallet | https://redbelly-governance.vercel.app/ |

Refresh the Snapshot result with:

```
curl -s https://hub.snapshot.org/graphql -H 'content-type: application/json' \
  -d '{"query":"{proposal(id:\"0xa57ccc9a6d554c9e5a1b1ca429ad2affc2e9058f12ea50bce999460f2aea4e02\"){title state start end scores scores_total votes}}"}'
```
