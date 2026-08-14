# Career OS — human-in-the-loop application system

Career OS is a semi-automated job-search workflow built around verified evidence and explicit approval gates.

## Flow

```text
Discover → Qualify → Score → Tailor → Verify → Apply → Follow up → Learn
```

| Stage | Automation level | Output | Human gate |
|---|---|---|---|
| Discover | Automated | Deduplicated shortlist | Define role families and geographies |
| Qualify | Human gate | Eligible / uncertain / reject | Work authorization, relocation, sponsorship, language, salary, seniority |
| Score | Automated | Evidence-match score and missing requirements | Reject weak matches and false positives |
| Tailor | Semi-automated | Headline, summary, bullet order, project order | Select only verified claims |
| Verify | Human gate | Final resume and application brief | Check names, dates, links, metrics, and role language |
| Apply | Human gate | Submitted application and confirmation | Use the employer's official channel; no blind auto-submit |
| Follow up | Semi-automated | Reminder and concise message | Review tone and recipient |
| Learn | Automated | Callback rate by role, geography, resume version, and project signal | Decide what to change next |

## Evidence hierarchy

1. Verified professional result: Stellantis workflow, two days to two minutes.
2. Current operating scope: supplier quality, electronics and metal, global supplier portfolio.
3. Reproducible portfolio evidence: Supplier Signal and AgentOps Pulse.
4. Public product evidence: TariffSnapshot and other GitHub projects.
5. Education and verified certifications.

## Country gate

“Remote” is not assumed to mean “work from Morocco.” Every role is screened for location scope, work authorization, sponsorship, relocation, employer-of-record, and contractor eligibility before time is spent tailoring an application.

## Safety rules

- Never invent a metric, employer claim, certification, or tool.
- Never submit without final human review.
- Never upload employer-confidential information.
- Never reuse one resume blindly; change the evidence order, not the truth.
- Track outcomes so the portfolio and evidence library improve from real market feedback.

The interactive local-first implementation is available at `#/career-os` on the deployed portfolio. Tracker data stays in the user's browser.

