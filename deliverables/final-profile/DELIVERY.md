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

All three local repositories are clean and use the `main` branch.

## Publishing status

GitHub publication was not executed because `gh` is not installed/authenticated in this environment and the connected GitHub tools cannot create repositories. No credentials were requested or stored.

After GitHub CLI authentication, create and push these four repositories:

```powershell
gh repo create retail-demand-decision-engine --public --source projects/retail-demand-decision-engine --remote origin --push
gh repo create last-mile-route-control-tower --public --source projects/last-mile-route-control-tower --remote origin --push
gh repo create agent-reliability-lab --public --source projects/agent-reliability-lab --remote origin --push
gh repo create rida-melkaoui-decision-portfolio --public --source . --remote origin --push
```

Then enable GitHub Pages for the portfolio repository using GitHub Actions or deploy `dist/` to Vercel/Cloudflare Pages. Update the portfolio/resume URL only after the final public address is known.

## Claim boundary

- Demand policy outcomes are M5 holdout simulations, not realized savings.
- Route outcomes are retrospective public-benchmark simulations, not a production deployment.
- Agent results describe pinned historical official trajectories, not current model or production performance.
- No confidential supplier, customer, part or project name is included.
