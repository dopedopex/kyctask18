# Redbelly Access portal: the on-screen text this guide quotes

Captured on 22 October 2026 from https://access.redbelly.network/

Redbelly Access is a web app. Its screens are not separate pages you can link to, but all of its on-screen text ships inside two public JavaScript files. The quotes below were read from those files. Anyone can repeat the check.

## The two files

| File | SHA-256 on 22 October 2026 |
|---|---|
| https://access.redbelly.network/_next/static/chunks/pages/index-25986869981a8ae9.js | 4a128d38b556eeae044f703b1aba895f9ec7fa3d7872020c2d6038718d7db357 |
| https://access.redbelly.network/_next/static/chunks/pages/_app-cee7356aa3975380.js | 6699d0cdb7c326000388f1454596c95cd900a0fab7677fc0a04a283c97548e6a |

The file names change when Redbelly ships a new version. If a link above stops working, use the steps below. They search whatever version is live.

## Check a quote yourself

1. Open https://access.redbelly.network/ in Chrome or Edge on a computer.
2. Press F12, then open the **Sources** tab.
3. Press Ctrl+Shift+F (Cmd+Option+F on a Mac) to search every file the portal loaded.
4. Paste a **Search for** line from below and press Enter.
5. Click the result. Press `{}` at the bottom of the code panel to make it readable.

From a terminal:

```
curl -s https://access.redbelly.network/_next/static/chunks/pages/index-25986869981a8ae9.js | grep -o 'Account allocation exhausted'
```

## E1. Wallet limit (index file)

**Search for:** `Account allocation exhausted`

```
L.length>=Number("10")?(0,i.jsx)(d.A,{severity:"info",children:"Account allocation exhausted."}):null
```

When 10 accounts are linked to one identity, the Accounts screen shows "Account allocation exhausted." in place of the "Add another account" option. The same screen has the buttons "Add another account" and "Link another wallet".

## E2. Approval time and outcomes (_app file for the messages, index file for the titles and buttons)

**Search for:** `could take a few days`

```
PENDING = "Your identity is being verified by the accredited issuer. This could take a few minutes but in some (rare) cases it could take a few days. Please check again soon."
FAIL    = "The issuer, Averer, was not able to verify your identity. You may need to reach out to Averer directly."
RETRY   = "The issuer, Averer, is not yet able to verify your identity. You may need to resubmit some information. If you continue having trouble however, you may need to reach out to Averer directly."
```

Screen titles: "Identity verification pending", "Identity verification incomplete", "Identity verification failed".
Buttons: "Check verification status", "Retry identity verification", "CONTACT AVERER".

### The 30 second re-check (index file)

**Search for:** `(0,I.cb)(3e4)`

```
onClick:async()=>{...,await (0,I.cb)(3e4),await b(...sessionId)},children:"Check verification status"
```

`I.cb` is a delay helper (module 54994 in `https://access.redbelly.network/_next/static/chunks/9971-5aa2e37871eac7c7.js`, ending in `new Promise(e=>setTimeout(e,t))`). `3e4` is 30,000 milliseconds, so the button waits 30 seconds and then asks for the verification status again.

No other approval time limit appears in the portal's code. The two page files, the shared chunks and all 85 lazy loaded chunks were searched for hours, days, minutes and "within" on 22 October 2026. The PENDING message above is the only approval wording.

## E3. Screens and buttons from start to "Enabled" (index file)

**Search for:** `Begin identity verification`, `Continue with Averer`, `Enable account`, `haven't received the RBNT`, `must first be funded`

1. "Connect wallet". Link "ADD NETWORK MANUALLY".
2. Screen "Get access credential", button "Begin identity verification".
3. Notice that the check is managed by Averer. Checkbox "I understand", button "Continue with Averer".
4. Wallet request letting the accredited issuer access your public address.
5. Window titled "Interacting with averer.co".
6. "Account status: Not enabled", button "Enable account".
7. If the issuer's RBNT has not arrived: "It seems you haven't received the RBNT yet, which you will need to enable you account. Please wait a few minutes and try again." Button "RETRY".
8. If the account has no RBNT and none is on the way: "To pay the transaction fee required to enable this account, this account must first be funded with at least [amount] USD worth RBNT coins."
9. "Account status: Enabled" and "Next steps".

## E4. Adding wallets (index file)

**Search for:** `Link another wallet`, `attached to another account`, `accountable for all`

- "Add another account": switch your wallet's connection to the address you want to add, then sign.
- "Link another wallet": connect the other wallet with the wallet widget in the top right corner of the portal.
- "By linking another wallet, you will be accountable for all the actions taken by that wallet on the network."
- Error: "The address you're trying to add is attached to another account."

## E5. "Having trouble?" FAQ (_app file, visible on the home page before you connect)

**Search for:** `Do I need to pay for access`, `MetaMask and Coinbase Wallet`, `create a Testnet account`

- "Do I need to pay for access?" "No, the accredited issuer that verifies your identity will cover any associated fees required to grant your network access."
- "Which wallets can I use to gain access to Redbelly Network?" "MetaMask and Coinbase Wallet can be used to get access."
- "Can I get access to the Redbelly Testnet?" "Yes, once you have completed the process of identity verification and enabling your account, you will be offered the option to create a Testnet account too."
- "Can I get access to Redbelly Network for multiple accounts?" "Yes, once you have completed the process of identity verification and enabling your first account, you will be offered the option to add more accounts which will be connected to your identity."
- "Who will verify my identity?" "Your identity will be verified by an accredited issuer, Averer."
- Identity verification problems: "contact Averer" (links to https://www.averer.co/). Connection or account errors: "Redbelly Support" (links to https://vine.redbelly.network/support).
