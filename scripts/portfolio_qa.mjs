import { createRequire } from "node:module";
import { mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const { chromium } = require("C:/Users/reda/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright");
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const output = path.join(root, "qa", "decision-room");
const baseUrl = process.env.PORTFOLIO_QA_URL ?? "http://127.0.0.1:4340";
await mkdir(output, { recursive: true });

const browser = await chromium.launch({
  headless: true,
  executablePath: "C:/Program Files/Google/Chrome/Application/chrome.exe",
});
const issues = [];
const watch = (page) => page.on("console", (message) => {
  if (["error", "warning"].includes(message.type())) issues.push(`${message.type()}: ${message.text()}`);
});

const desktop = await browser.newPage({ viewport: { width: 1634, height: 965 }, deviceScaleFactor: 1 });
watch(desktop);
await desktop.goto(`${baseUrl}/`, { waitUntil: "networkidle" });
await desktop.getByRole("heading", { name: /I build decision systems/i }).waitFor();
await desktop.waitForTimeout(500);

const identity = await desktop.evaluate(() => ({
  title: document.title,
  hero: document.querySelector("h1")?.textContent?.replace(/\s+/g, " ").trim(),
  heroImage: document.querySelector(".portrait-portal img")?.getAttribute("src"),
  headerAvatar: document.querySelector(".identity-avatar img")?.getAttribute("src"),
  sections: [...document.querySelectorAll(".section-identity h2")].map((node) => node.textContent?.trim()),
  bodyOverflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
}));
if (!identity.heroImage?.includes("rida-profile-evening")) throw new Error(`Incorrect hero image: ${identity.heroImage}`);
if (!identity.headerAvatar?.includes("rida-header-cutout")) throw new Error(`Incorrect header avatar: ${identity.headerAvatar}`);
for (const heading of ["PROJECTS", "DECISION METHOD", "PROFESSIONAL EXPERIENCE", "PROFILE"]) {
  if (!identity.sections.includes(heading)) throw new Error(`Missing explicit section heading: ${heading}`);
}
if (identity.bodyOverflow !== 0) throw new Error(`Desktop overflow: ${identity.bodyOverflow}px`);
await desktop.screenshot({ path: path.join(output, "desktop-hero.png"), fullPage: false });

await desktop.getByRole("link", { name: /Projects/ }).click();
await desktop.waitForTimeout(500);
await desktop.locator(".project-row").first().click();
await desktop.waitForTimeout(350);
const collapseState = await desktop.evaluate(() => ({
  activeRows: document.querySelectorAll(".project-row.active").length,
  projectOpacities: [...document.querySelectorAll(".project-row")].map((node) => getComputedStyle(node).opacity),
  idleVisible: !!document.querySelector(".project-preview-idle"),
  previewText: document.querySelector(".project-preview")?.textContent?.replace(/\s+/g, " ").trim(),
}));
if (collapseState.activeRows !== 0 || !collapseState.idleVisible || collapseState.projectOpacities.some((value) => value !== "1") || !collapseState.previewText) {
  throw new Error(`Project collapse regression: ${JSON.stringify(collapseState)}`);
}

await desktop.locator(".project-row").nth(1).click();
await desktop.waitForTimeout(300);
const routeProof = await desktop.getByText("6,112 historical routes", { exact: true }).isVisible();
const routeImage = await desktop.locator(".project-preview img").getAttribute("src");
await desktop.screenshot({ path: path.join(output, "desktop-projects.png"), fullPage: false });

await desktop.locator(".project-row").nth(2).click();
await desktop.waitForTimeout(250);
const agentProof = await desktop.getByText("3,336 official trajectories", { exact: true }).isVisible();

await desktop.getByRole("link", { name: /Experience/ }).click();
await desktop.waitForTimeout(500);
const experienceAnchor = await desktop.evaluate(() => ({
  headerBottom: document.querySelector(".site-header")?.getBoundingClientRect().bottom,
  headingTop: document.querySelector("#experience h2")?.getBoundingClientRect().top,
}));
if ((experienceAnchor.headingTop ?? 0) < (experienceAnchor.headerBottom ?? 0)) {
  throw new Error(`Experience heading hidden by fixed header: ${JSON.stringify(experienceAnchor)}`);
}
const syntheticPreview = await desktop.getByText("SYNTHETIC PUBLIC PREVIEW / REAL INTERFACE ANATOMY", { exact: true }).isVisible();
const xreyText = await desktop.locator(".xrey-shell").innerText();
const requiredAnatomy = ["SUPPLIER QUALITY COMMAND", "COMMAND", "TIMING", "QUALITY", "AUDITS & CAPACITY", "CLAIMS", "DATA INTAKE", "SUPPLIER CONTROL BOARD", "PRIORITY ACTION CENTER"];
for (const label of requiredAnatomy) if (!xreyText.includes(label)) throw new Error(`X-Rey anatomy is missing: ${label}`);
const confidentialTokens = ["Hebang", "MMTT", "Sluzba", "Auteca", "Muelles", "VW OSM", "IRVM"].filter((token) => xreyText.toLowerCase().includes(token.toLowerCase()));
if (confidentialTokens.length) throw new Error(`Confidential token in public preview: ${confidentialTokens.join(", ")}`);

await desktop.locator(".timeline-list button").nth(1).click();
await desktop.waitForTimeout(300);
const experienceSwitch = await desktop.getByRole("heading", { name: /Converted a two-day BOM anomaly workflow/ }).isVisible();
const stellantisMetrics = await desktop.locator(".experience-metrics").innerText();
const stellantisImage = await desktop.locator(".stellantis-proof img").getAttribute("src");
if (!["2 days", "<3 min", "-98%", "100%"].every((value) => stellantisMetrics.includes(value))) {
  throw new Error(`Stellantis KPI evidence missing: ${stellantisMetrics}`);
}
if (!stellantisImage?.includes("stellantis-workstation")) throw new Error(`Incorrect Stellantis image: ${stellantisImage}`);
await desktop.screenshot({ path: path.join(output, "desktop-experience.png"), fullPage: false });

await desktop.getByRole("link", { name: /Profile/ }).click();
await desktop.waitForTimeout(1400);
const profileVisible = await desktop.getByRole("heading", { name: "PROFILE", exact: true }).isVisible();
await desktop.screenshot({ path: path.join(output, "desktop-profile.png"), fullPage: false });

const liveLab = await browser.newPage({ viewport: { width: 1200, height: 850 } });
watch(liveLab);
await liveLab.goto(`${baseUrl}/labs/agent/index.html`, { waitUntil: "networkidle" });
const labTitle = await liveLab.title();
const labVisible = await liveLab.getByRole("heading", { name: /ONE PASS IS/ }).isVisible();

const mobile = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1 });
watch(mobile);
await mobile.goto(`${baseUrl}/`, { waitUntil: "networkidle" });
await mobile.getByRole("heading", { name: /I build decision systems/i }).waitFor();
const mobileBox = await mobile.evaluate(() => ({
  clientWidth: document.documentElement.clientWidth,
  scrollWidth: document.documentElement.scrollWidth,
  scrollHeight: document.documentElement.scrollHeight,
}));
if (mobileBox.clientWidth !== mobileBox.scrollWidth) throw new Error(`Mobile overflow: ${JSON.stringify(mobileBox)}`);
await mobile.screenshot({ path: path.join(output, "mobile-hero.png"), fullPage: false });

await mobile.getByRole("button", { name: "Toggle navigation" }).click();
const menuOpen = await mobile.locator(".site-header nav.open").isVisible();
await mobile.getByRole("link", { name: /Experience/ }).click();
await mobile.waitForTimeout(350);
const mobileExperience = await mobile.evaluate(() => ({
  headingTop: document.querySelector("#experience h2")?.getBoundingClientRect().top,
  headerBottom: document.querySelector(".site-header")?.getBoundingClientRect().bottom,
  pageOverflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
  xreyClientWidth: document.querySelector(".xrey-shell")?.clientWidth,
  xreyScrollWidth: document.querySelector(".xrey-shell")?.scrollWidth,
}));
if ((mobileExperience.headingTop ?? 0) < (mobileExperience.headerBottom ?? 0) || mobileExperience.pageOverflow !== 0) {
  throw new Error(`Mobile experience layout regression: ${JSON.stringify(mobileExperience)}`);
}
if ((mobileExperience.xreyScrollWidth ?? 0) <= (mobileExperience.xreyClientWidth ?? 0)) {
  throw new Error(`X-Rey evidence frame should own its horizontal scroll: ${JSON.stringify(mobileExperience)}`);
}
await mobile.screenshot({ path: path.join(output, "mobile-experience.png"), fullPage: false });

if (!routeProof || !agentProof || !syntheticPreview || !experienceSwitch || !profileVisible || !labVisible || !menuOpen) {
  throw new Error("A required visual or interaction check failed");
}
if (issues.length) throw new Error(`Console issues: ${issues.join(" | ")}`);

console.log(JSON.stringify({
  identity,
  collapseState,
  routeProof,
  routeImage,
  agentProof,
  experienceAnchor,
  syntheticPreview,
  confidentialTokens,
  experienceSwitch,
  stellantisMetrics,
  stellantisImage,
  profileVisible,
  labTitle,
  labVisible,
  mobileBox,
  mobileExperience,
  menuOpen,
  issues,
}, null, 2));
await browser.close();
