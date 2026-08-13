# Final profile delivery

## Portfolio

- Source: repository root.
- Production build: `dist/`.
- Local preview: `pnpm preview` after `pnpm build`.
- Three static live labs: `public/labs/demand`, `public/labs/route`, `public/labs/agent`.

## Resumes

- `Rida_Melkaoui_Data_AI_Resume_ATS.pdf` — use for application portals and recruiter systems.
- `Rida_Melkaoui_Data_AI_Resume_Branded.pdf` — use for direct email, networking and portfolio download.

Both are one-page, selectable-text PDFs with the same verified evidence language.

## Project repositories

| Repository | Local commit | Verification |
|---|---|---|
| retail-demand-decision-engine | `d700373` | tests, executed notebook, Vite build, responsive browser QA |
| last-mile-route-control-tower | `853ccd1` | 5 tests, executed notebook, Vite build, responsive browser QA |
| agent-reliability-lab | `6593bb2` | 9 tests, executed notebook, Vite build, audit, responsive browser QA |
| rida-melkaoui-decision-portfolio | `ca06273` | TypeScript, production build, desktop/mobile browser QA, two one-page PDF validations |

All three local repositories are clean and use the `main` branch.

## Publishing status

Publication completed on 2026-08-13:

- Portfolio: <https://ridamelkaoui.github.io/rida-melkaoui-decision-portfolio/>
- Portfolio source: <https://github.com/RidaMelkaoui/rida-melkaoui-decision-portfolio>
- Demand / Order: <https://github.com/RidaMelkaoui/retail-demand-decision-engine>
- Route / Control: <https://github.com/RidaMelkaoui/last-mile-route-control-tower>
- Agent / Proof: <https://github.com/RidaMelkaoui/agent-reliability-lab>

GitHub Pages deploys the production `dist/` artifact from `main` through `.github/workflows/deploy-pages.yml`. The live portfolio and an embedded decision lab were verified in a browser after deployment.

## Claim boundary

- Demand policy outcomes are M5 holdout simulations, not realized savings.
- Route outcomes are retrospective public-benchmark simulations, not a production deployment.
- Agent results describe pinned historical official trajectories, not current model or production performance.
- No confidential supplier, customer, part or project name is included.
