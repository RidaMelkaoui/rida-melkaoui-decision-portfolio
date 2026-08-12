import { createRequire } from "node:module";
import { mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const { chromium } = require("C:/Users/reda/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright");
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const output = path.join(root, "qa", "decision-room");
await mkdir(output, { recursive: true });
const browser = await chromium.launch({ headless: true, executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe" });
const issues = [];
const watch = (page) => page.on("console", message => { if (["error", "warning"].includes(message.type())) issues.push(`${message.type()}: ${message.text()}`); });

const desktop = await browser.newPage({ viewport: { width: 1536, height: 1024 }, deviceScaleFactor: 1 });
watch(desktop);
await desktop.goto("http://127.0.0.1:4329/", { waitUntil: "networkidle" });
await desktop.waitForTimeout(450);
const title = await desktop.title();
const hero = await desktop.getByRole("heading", { name: /I BUILD/ }).isVisible();
const headingOrder = await desktop.locator("h1,h2,h3").evaluateAll(nodes => nodes.map(node => node.textContent?.trim()).filter(Boolean));
await desktop.screenshot({ path: path.join(output, "desktop-hero.png"), fullPage: false });

await desktop.getByRole("button", { name: /A route policy/ }).click();
await desktop.waitForTimeout(250);
const routeProof = await desktop.getByText("6,112 historical routes", { exact: true }).isVisible();
await desktop.screenshot({ path: path.join(output, "desktop-route-case.png"), fullPage: false });
await desktop.getByRole("button", { name: /One pass is not reliability/ }).click();
const agentProof = await desktop.getByText("3,336 official trajectories", { exact: true }).isVisible();
await desktop.locator("#experience").scrollIntoViewIfNeeded();
await desktop.getByRole("button", { name: /STELLANTIS R&D/ }).click();
const experienceSwitch = await desktop.getByRole("heading", { name: /Reduced a configuration-anomaly workflow/ }).isVisible();
await desktop.screenshot({ path: path.join(output, "desktop-experience.png"), fullPage: false });

const liveLab = await browser.newPage({ viewport: { width: 1200, height: 850 } });
watch(liveLab);
await liveLab.goto("http://127.0.0.1:4329/labs/agent/index.html", { waitUntil: "networkidle" });
const labTitle = await liveLab.title();
const labVisible = await liveLab.getByRole("heading", { name: /ONE PASS IS/ }).isVisible();

const mobile = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
watch(mobile);
await mobile.goto("http://127.0.0.1:4329/", { waitUntil: "networkidle" });
await mobile.waitForTimeout(300);
const mobileBox = await mobile.evaluate(() => ({ clientWidth: document.documentElement.clientWidth, scrollWidth: document.documentElement.scrollWidth, scrollHeight: document.documentElement.scrollHeight }));
if (mobileBox.clientWidth !== mobileBox.scrollWidth) throw new Error(`Mobile overflow: ${JSON.stringify(mobileBox)}`);
await mobile.screenshot({ path: path.join(output, "mobile-hero.png"), fullPage: false });
await mobile.getByRole("button", { name: "Toggle navigation" }).click();
const menuOpen = await mobile.locator(".site-header nav.open").isVisible();
await mobile.locator("#work").scrollIntoViewIfNeeded();
await mobile.screenshot({ path: path.join(output, "mobile-work.png"), fullPage: false });

if (!hero || !routeProof || !agentProof || !experienceSwitch || !labVisible || !menuOpen) throw new Error("A required visual or interaction check failed");
if (issues.length) throw new Error(`Console issues: ${issues.join(" | ")}`);
console.log(JSON.stringify({ title, hero, headingOrder: headingOrder.slice(0, 12), routeProof, agentProof, experienceSwitch, labTitle, labVisible, mobileBox, menuOpen, issues }, null, 2));
await browser.close();
