// Builds every derived file from one source so they never drift apart:
//   pin.txt                                  <- the pin block in index.html
//   decision-guide.png (1080 x 1080)         <- src/decision-guide.html
//   img/og.png (1200 x 630)                  <- src/og.html
//   KYC-and-Wallet-Activation-Explainer.pdf  <- index.html, print styles
// Usage: node scripts/build.mjs   (needs the playwright package and Chromium)
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { createRequire } from "node:module";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const html = readFileSync(join(root, "index.html"), "utf8");
const m = html.match(/<pre class="pin" id="pin-text">([\s\S]*?)<\/pre>/);
if (!m) throw new Error("pin block not found in index.html");
const pin = m[1].replace(/&quot;/g, '"').replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&");
writeFileSync(join(root, "pin.txt"), pin.trimEnd() + "\n");
console.log("pin.txt written");

const footFont = readFileSync(join(root, "fonts", "BeVietnamPro-Regular.ttf")).toString("base64");
const exe = process.env.CHROMIUM_PATH;
const browser = await chromium.launch(exe ? { executablePath: exe } : {});

async function shot(src, out, width, height) {
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(join(root, src)).href);
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: join(root, out), clip: { x: 0, y: 0, width, height } });
  await page.close();
  console.log(`${out} written`);
}

await shot("src/decision-guide.html", "decision-guide.png", 1080, 1080);
await shot("src/og.html", "img/og.png", 1200, 630);

const page = await browser.newPage();
await page.emulateMedia({ media: "print", colorScheme: "light" });
await page.goto(pathToFileURL(join(root, "index.html")).href, { waitUntil: "load" });
await page.evaluate(() => document.fonts.ready);
// Relative links would otherwise become file:// paths of the build machine inside the PDF.
await page.evaluate((site) => {
  document.querySelectorAll("a[href]").forEach((a) => {
    const h = a.getAttribute("href");
    if (!/^(https?:|mailto:|#)/.test(h)) a.setAttribute("href", new URL(h, site).href);
  });
}, "https://pykyc.vercel.app/");
await page.pdf({
  path: join(root, "KYC-and-Wallet-Activation-Explainer.pdf"),
  format: "A4",
  printBackground: true,
  margin: { top: "16mm", bottom: "16mm", left: "14mm", right: "14mm" },
  displayHeaderFooter: true,
  headerTemplate: "<span></span>",
  footerTemplate: `<style>@font-face{font-family:BVP;src:url(data:font/ttf;base64,${footFont})}</style>` + '<div style="font:9px BVP;color:#596975;width:100%;padding:0 14mm;display:flex;justify-content:space-between"><span>Redbelly KYC and Wallet Activation Explainer. Last verified 22 October 2026. pykyc.vercel.app</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
});
console.log("KYC-and-Wallet-Activation-Explainer.pdf written");
await browser.close();
