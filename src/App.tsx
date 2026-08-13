import { lazy, Suspense, useEffect, useRef, useState, type CSSProperties, type PointerEvent } from "react";
import { usePortfolioMotion } from "./hooks/usePortfolioMotion";

const DecisionScene = lazy(() =>
  import("./components/DecisionScene").then((module) => ({ default: module.DecisionScene })),
);

type ProjectKey = "demand" | "route" | "agent";

type Project = {
  key: ProjectKey;
  index: string;
  title: string;
  thesis: string;
  question: string;
  result: string;
  resultNote: string;
  narrative: string;
  proof: string[];
  evidenceChain: [string, string, string];
  stack: string;
  image: string;
  lab: string;
  source: string;
  caveat: string;
};

type ExperienceMetric = {
  value: string;
  label: string;
  note: string;
};

type ExperienceItem = {
  period: string;
  company: string;
  place: string;
  role: string;
  statement: string;
  details: string[];
  metrics: ExperienceMetric[];
  proof?: "sqe" | "stellantis";
  sourceNote?: string;
};

const projects: Project[] = [
  {
    key: "demand",
    index: "01",
    title: "DEMAND / ORDER",
    thesis: "From a forecast score to a replenishment decision.",
    question: "What should a planner review, and how much service buffer is defensible?",
    result: "1,528",
    resultNote: "fewer simulated lost units",
    narrative:
      "I built a cutoff-safe M5 forecasting pipeline, challenged the global model with a calibration-selected seasonal baseline, then converted the winning signal into policy scenarios and a planner exception queue. The interface makes the service-versus-inventory trade-off visible instead of hiding it behind one accuracy score.",
    proof: ["900 item-store series", "4.5% lower WAPE vs selected baseline", "96.7% simulated fulfilled demand"],
    evidenceChain: ["Checksum-verified M5 tables", "Leakage-safe forecast + policy simulation", "Planner exception queue"],
    stack: "Python / scikit-learn / forecasting / policy simulation / React",
    image: "./images/projects/demand-overview.png",
    lab: "./labs/demand/index.html",
    source: "https://github.com/RidaMelkaoui/retail-demand-decision-engine",
    caveat: "M5 28-day holdout; policy outcomes are simulation, not realized savings.",
  },
  {
    key: "route",
    index: "02",
    title: "ROUTE / CONTROL",
    thesis: "A route policy a dispatcher can interrogate.",
    question: "Which sequence balances drive time, timed packages and route coherence?",
    result: "85.2 min",
    resultNote: "less simulated drive time",
    narrative:
      "I learned zone-order preferences from 6,112 historical routes and combined them with directed travel time, timed-package guardrails and constrained local search. The control tower compares policies route by route, preserves service and sends the remaining exceptions to a dispatcher for review.",
    proof: ["6,112 historical routes", "100% timed-package adherence", "332 to 0 zone re-entries"],
    evidenceChain: ["Public Amazon route histories", "Driver-aware constrained sequence policy", "Dispatch intervention queue"],
    stack: "Python / sequence learning / constrained local search / React",
    image: "./images/projects/route-control.png",
    lab: "./labs/route/index.html",
    source: "https://github.com/RidaMelkaoui/last-mile-route-control-tower",
    caveat: "Separate 13-route public cohort; retrospective simulation, not a production claim.",
  },
  {
    key: "agent",
    index: "03",
    title: "AGENT / PROOF",
    thesis: "One pass is not reliability.",
    question: "Which agent is repeatable enough to release, and what fails first?",
    result: "14.9 pts",
    resultNote: "repeatability loss exposed",
    narrative:
      "I reconstructed four-trial reliability, cost, latency, tool behaviour and evaluator signals from official agent trajectories. The interface separates stable, unstable and always-failing tasks, applies a transparent release gate and points the team to the failure family that deserves intervention first.",
    proof: ["3,336 official trajectories", "4 trials per task", "99.0% missing-action diagnostic share"],
    evidenceChain: ["Pinned official trajectories", "Pass-k + deterministic diagnostics", "Release / monitor / hold gate"],
    stack: "Python / agent evaluation / statistics / failure diagnostics / React",
    image: "./images/projects/agent-proof.png",
    lab: "./labs/agent/index.html",
    source: "https://github.com/RidaMelkaoui/agent-reliability-lab",
    caveat: "Pinned historical tau2-bench cohort; no live calls or current-production claim.",
  },
];

const timeline: ExperienceItem[] = [
  {
    period: "MAR 2026 - NOW",
    company: "MAGNA INTERNATIONAL",
    place: "KENITRA, MOROCCO",
    role: "Supplier Quality Engineer / Electronics & Metal",
    statement: "Built the decision layer I needed to run supplier quality.",
    details: [
      "Designed an SQE assistant joining ownership, timing, PPAP and DVP evidence, audits, claims and controlled data intake in one operating view.",
      "Built KPI views and notification logic so missing baselines, overdue actions and readiness gaps surface before the next launch gate.",
      "Operate electronics and metal supplier quality from nomination through Safe Launch and SOP across Europe, Asia and Morocco.",
    ],
    metrics: [
      { value: "6", label: "control modules", note: "command to intake" },
      { value: "4", label: "lifecycle gates", note: "nomination to SOP" },
      { value: "6", label: "supplier countries", note: "three operating regions" },
    ],
    proof: "sqe",
    sourceNote: "System scope only. Every program, supplier and value in the public preview is synthetic.",
  },
  {
    period: "FEB - AUG 2025",
    company: "STELLANTIS R&D",
    place: "CASABLANCA, MOROCCO",
    role: "Engineering Intern / Data Analytics, Process Optimization & AI",
    statement: "Converted a two-day BOM anomaly workflow into a sub-three-minute validated process.",
    details: [
      "Mapped the E-BOM/M-BOM decision flow and its failure modes, then translated status logic into a standardized treatment process.",
      "Built a Python detector around exported configuration data for anomaly identification, prioritization and treatment traceability.",
      "Benchmarked the automated workflow against the manual process and documented limitations around live PLM/SAP integration and data quality.",
    ],
    metrics: [
      { value: "2 days", label: "manual cycle", note: "before automation" },
      { value: "<3 min", label: "automated cycle", note: "validation benchmark" },
      { value: "-98%", label: "manual handling", note: "100% to 2%" },
      { value: "100%", label: "processing reliability", note: "project test cases" },
    ],
    proof: "stellantis",
    sourceNote: "PFE validation benchmark; not presented as a plant-wide production deployment.",
  },
  {
    period: "JUL - SEP 2024",
    company: "SANY / FORGE DE BAZAS",
    place: "CASABLANCA, MOROCCO",
    role: "Engineering Intern / Process Digitalization & Maintenance",
    statement: "Made maintenance knowledge easier to retrieve and use on the shop floor.",
    details: [
      "Built a Unity/NLP assistant that structured access to maintenance and spare-parts information while preserving a traceable knowledge flow.",
    ],
    metrics: [
      { value: "1", label: "knowledge assistant", note: "Unity + NLP" },
      { value: "2", label: "data domains", note: "maintenance / spare parts" },
    ],
  },
  {
    period: "AUG - SEP 2023",
    company: "3D SMART FACTORY",
    place: "MOHAMMEDIA, MOROCCO",
    role: "Data Analyst Intern",
    statement: "Converted production records into visual operating signals.",
    details: ["Built Power BI and Excel reporting around OEE, FPY, scrap and downtime to expose bottlenecks for Lean review."],
    metrics: [
      { value: "4", label: "KPI families", note: "OEE / FPY / scrap / downtime" },
      { value: "2", label: "analytics tools", note: "Power BI + Excel" },
    ],
  },
];

function ArrowIcon({ direction = "right" }: { direction?: "right" | "down" }) {
  return (
    <svg className={`action-icon action-icon-${direction}`} viewBox="0 0 24 24" aria-hidden="true">
      {direction === "right" ? <path d="M4 12h15M13 6l6 6-6 6" /> : <path d="M12 4v15M6 13l6 6 6-6" />}
    </svg>
  );
}

function Header() {
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState("top");
  const nav = [
    ["Projects", "work", "01"],
    ["Method", "method", "02"],
    ["Experience", "experience", "03"],
    ["Profile", "profile", "04"],
    ["Contact", "contact", "05"],
  ];

  useEffect(() => {
    const sections = ["top", ...nav.map(([, id]) => id)]
      .map((id) => document.getElementById(id))
      .filter(Boolean) as HTMLElement[];
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries.filter((entry) => entry.isIntersecting).sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (visible) setActive(visible.target.id);
      },
      { rootMargin: "-24% 0px -63%", threshold: [0, 0.15, 0.35] },
    );
    sections.forEach((section) => observer.observe(section));
    const progress = () => {
      const max = document.documentElement.scrollHeight - innerHeight;
      document.documentElement.style.setProperty("--scroll-progress", `${max > 0 ? scrollY / max : 0}`);
    };
    addEventListener("scroll", progress, { passive: true });
    progress();
    return () => {
      observer.disconnect();
      removeEventListener("scroll", progress);
    };
  }, []);

  return (
    <header className="site-header">
      <a className="identity-mark" href="#top" aria-label="Rida Melkaoui, back to top">
        <span className="identity-avatar">
          <img src="./images/rida-header-cutout.png" alt="" />
          <i aria-hidden="true" />
        </span>
        <span className="identity-copy">
          <strong>RIDA MELKAOUI</strong>
          <small>DECISION ENGINEER</small>
        </span>
      </a>
      <nav className={open ? "open" : ""} aria-label="Portfolio sections">
        {nav.map(([label, id, number]) => (
          <a
            key={id}
            href={`#${id}`}
            aria-current={active === id ? "location" : undefined}
            onClick={() => setOpen(false)}
          >
            <span>[{number}]</span>
            {label}
          </a>
        ))}
      </nav>
      <a className="resume-link" href="./documents/Rida_Melkaoui_Data_AI_Resume.pdf" target="_blank" rel="noreferrer">
        RESUME <ArrowIcon direction="down" />
      </a>
      <button className="menu-toggle" aria-label="Toggle navigation" aria-expanded={open} onClick={() => setOpen((value) => !value)}>
        <span />
        <span />
      </button>
    </header>
  );
}

function Hero() {
  const portal = useRef<HTMLDivElement>(null);
  const tilt = (event: PointerEvent<HTMLDivElement>) => {
    const element = portal.current;
    if (!element) return;
    const bounds = element.getBoundingClientRect();
    const x = (event.clientX - bounds.left) / bounds.width - 0.5;
    const y = (event.clientY - bounds.top) / bounds.height - 0.5;
    element.style.setProperty("--portal-rx", `${-y * 5}deg`);
    element.style.setProperty("--portal-ry", `${x * 7}deg`);
    element.style.setProperty("--portal-x", `${x * 8}px`);
    element.style.setProperty("--portal-y", `${y * 8}px`);
  };

  return (
    <section className="hero" id="top">
      <div className="hero-grid" aria-hidden="true" />
      <div className="hero-copy">
        <span className="hero-coordinate">[00] / DECISION OBSERVATORY</span>
        <h1 aria-label="I build decision systems.">
          {[
            ["I BUILD", "solid"],
            ["DECISION", "outline"],
            ["SYSTEMS.", "solid"],
          ].map(([word, style]) => (
            <span className="hero-word-mask" key={word}>
              <span data-hero-word className={style}>{word}</span>
            </span>
          ))}
        </h1>
        <p className="hero-support">
          Forecast demand. Control operational risk. Test whether an AI agent is actually reliable. I turn complex workflows into evidence people can act on.
        </p>
        <div className="hero-actions">
          <a href="#work">ENTER THE DECISION ROOM <ArrowIcon /></a>
          <a href="mailto:ridamelkaouiofficial@gmail.com">DISCUSS A PROBLEM <ArrowIcon /></a>
        </div>
        <a className="hero-proof" href="#experience">
          <span>LIVE OPERATIONS</span>
          <strong>Supplier quality at Magna International</strong>
          <small>Industrial context / global collaboration / analytics built around action</small>
          <ArrowIcon />
        </a>
      </div>
      <div
        className="hero-visual"
        ref={portal}
        onPointerMove={tilt}
        onPointerLeave={() => {
          portal.current?.style.removeProperty("--portal-rx");
          portal.current?.style.removeProperty("--portal-ry");
          portal.current?.style.removeProperty("--portal-x");
          portal.current?.style.removeProperty("--portal-y");
        }}
      >
        <Suspense fallback={<div className="hero-scene scene-fallback" aria-hidden="true" />}>
          <DecisionScene className="hero-scene" />
        </Suspense>
        <div className="portrait-portal" data-hologram>
          <div className="projection-beam" aria-hidden="true" />
          <div className="projection-rays" aria-hidden="true">
            <span /><span /><span /><span /><span /><span /><span />
          </div>
          <div className="hologram-figure">
            <img className="hologram-image" src="./images/rida-header-cutout.png" alt="Rida Melkaoui" />
            <img className="hologram-echo echo-cyan" src="./images/rida-header-cutout.png" alt="" aria-hidden="true" />
            <img className="hologram-echo echo-orange" src="./images/rida-header-cutout.png" alt="" aria-hidden="true" />
            <span className="hologram-scan" aria-hidden="true" />
          </div>
          <div className="projection-source" aria-hidden="true"><i /><span>IDENTITY SIGNAL</span></div>
          <span className="portrait-reading reading-top">270</span>
          <span className="portrait-reading reading-left">180</span>
          <span className="portrait-reading reading-right">90</span>
        </div>
        <ul className="signal-legend" aria-label="Decision inputs">
          {[
            "DEMAND SIGNALS",
            "SUPPLIER QUALITY",
            "INVENTORY LEVELS",
            "LEAD TIMES",
            "ROUTE COHERENCE",
            "AI RELIABILITY",
          ].map((signal) => <li key={signal}>{signal}</li>)}
        </ul>
        <span className="one-decision">ONE DECISION</span>
        <div className="hero-status"><span>SYSTEM STATUS</span><strong><i /> OBSERVING</strong></div>
      </div>
      <a className="next-section" href="#work">NEXT / PROJECTS <ArrowIcon direction="down" /></a>
    </section>
  );
}

function SectionHeading({ number, name, headline, aside }: { number: string; name: string; headline: string; aside?: string }) {
  return (
    <header className="section-heading" data-motion="section">
      <div className="section-identity">
        <span>[{number}] /</span>
        <h2>{name}</h2>
      </div>
      <p>{headline}</p>
      {aside ? <small>{aside}</small> : null}
    </header>
  );
}

function ProjectPreview({ project, close }: { project: Project | null; close: () => void }) {
  const plane = useRef<HTMLDivElement>(null);
  const tilt = (event: PointerEvent<HTMLDivElement>) => {
    const element = plane.current;
    if (!element) return;
    const bounds = element.getBoundingClientRect();
    const x = (event.clientX - bounds.left) / bounds.width - 0.5;
    const y = (event.clientY - bounds.top) / bounds.height - 0.5;
    element.style.setProperty("--project-rx", `${-y * 2.5}deg`);
    element.style.setProperty("--project-ry", `${x * 3.8}deg`);
  };

  if (!project) {
    return (
      <div className="project-preview project-preview-idle">
        <span>[ SELECT A SYSTEM ]</span>
        <strong>Three operating decisions.<br />Three evidence trails.</strong>
        <p>Open a project to inspect its claim, interface and boundary.</p>
      </div>
    );
  }

  return (
    <div
      className="project-preview"
      ref={plane}
      data-depth-plane
      onPointerMove={tilt}
      onPointerLeave={() => {
        plane.current?.style.removeProperty("--project-rx");
        plane.current?.style.removeProperty("--project-ry");
      }}
    >
      <div className="project-preview-head">
        <span>{project.title}</span>
        <button onClick={close} aria-label={`Close ${project.title} case`}><i /> CLOSE CASE</button>
      </div>
      <h3>{project.thesis}</h3>
      <p className="project-narrative">{project.narrative}</p>
      <div className="project-interface">
        <img src={project.image} alt={`${project.title} evidence interface`} />
        <span>VERIFIED INTERFACE / DESKTOP</span>
      </div>
      <div className="project-proof-grid">
        <div className="evidence-chain">
          <span>EVIDENCE CHAIN</span>
          {project.evidenceChain.map((step, index) => (
            <div key={step}><small>[0{index + 1}]</small><strong>{step}</strong><ArrowIcon /></div>
          ))}
        </div>
        <div className="proof-stack">
          <span>VERIFIED OUTPUT</span>
          {project.proof.map((item) => <strong key={item}>{item}</strong>)}
          <small>{project.stack}</small>
        </div>
      </div>
      <p className="project-caveat">EVIDENCE NOTE / {project.caveat}</p>
      <div className="project-actions">
        <a href={project.lab} target="_blank" rel="noreferrer">OPEN LIVE LAB <ArrowIcon /></a>
        <a href={project.source} target="_blank" rel="noreferrer">SOURCE REPOSITORY <ArrowIcon /></a>
      </div>
    </div>
  );
}

function Projects() {
  const [active, setActive] = useState<ProjectKey | null>("demand");
  const selected = projects.find((project) => project.key === active) ?? null;
  return (
    <section className="projects section-dark" id="work">
      <SectionHeading
        number="01"
        name="PROJECTS"
        headline="Proof, not promises."
        aside="Public evidence / tested interfaces / explicit claim boundaries"
      />
      <div className="projects-room">
        <div className="projects-ghost" aria-hidden="true">PROJECTS</div>
        <div className="project-list" data-stagger>
          {projects.map((project) => {
            const isActive = active === project.key;
            return (
              <button
                key={project.key}
                className={isActive ? "project-row active" : "project-row"}
                onClick={() => setActive((current) => current === project.key ? null : project.key)}
                aria-expanded={isActive}
              >
                <span className="project-number">[{project.index}]</span>
                <span className="project-row-copy"><small>{project.title}</small><strong>{project.thesis}</strong><em>{project.question}</em></span>
                <span className="project-result"><strong>{project.result}</strong><small>{project.resultNote}</small></span>
                <span className="project-open"><i /> {isActive ? "CLOSE" : "OPEN"}</span>
              </button>
            );
          })}
        </div>
        <ProjectPreview key={selected?.key ?? "idle"} project={selected} close={() => setActive(null)} />
      </div>
    </section>
  );
}

function MethodIcon({ type }: { type: string }) {
  if (type === "FRAME") return <svg viewBox="0 0 64 64"><path d="M9 23V9h14M41 9h14v14M55 41v14H41M23 55H9V41"/><circle cx="32" cy="32" r="7"/></svg>;
  if (type === "PROVE") return <svg viewBox="0 0 64 64"><circle cx="16" cy="32" r="5"/><circle cx="44" cy="16" r="5"/><circle cx="48" cy="46" r="5"/><path d="m20 30 19-11M20 35l23 9M45 21l2 20"/></svg>;
  if (type === "MODEL") return <svg viewBox="0 0 64 64"><path d="m32 8 21 12-21 12L11 20 32 8Z"/><path d="m13 31 19 11 19-11M13 42l19 11 19-11"/></svg>;
  return <svg viewBox="0 0 64 64"><circle cx="32" cy="32" r="22"/><circle cx="32" cy="32" r="13"/><circle cx="32" cy="32" r="4"/><path d="M32 4v10M60 32H50M32 60V50M4 32h10"/></svg>;
}

function Method() {
  const steps = [
    ["01", "FRAME", "Name the decision, actor, action and cost of being wrong."],
    ["02", "PROVE", "Define the data contract, quality gates, baselines and claim boundary."],
    ["03", "MODEL", "Use the simplest defensible statistical, optimization or AI method."],
    ["04", "OPERATE", "Deliver an interface, exception queue and evidence trail—not a notebook alone."],
  ];
  return (
    <section className="method-field" id="method">
      <SectionHeading number="02" name="DECISION METHOD" headline="From ambiguity to an operating decision." />
      <div className="method-steps" data-stagger>
        {steps.map(([number, title, body]) => (
          <article key={number}>
            <span>[{number}]</span>
            <MethodIcon type={title} />
            <h3>{title}</h3>
            <p>{body}</p>
          </article>
        ))}
      </div>
      <p className="method-manifesto" data-motion="section">
        <span>OPERATING PRINCIPLE</span>
        A model earns its place only when a person can understand the decision, inspect the evidence and act on the result.
      </p>
    </section>
  );
}

const xreyRows = [
  ["Atlas Components", "Seat frame assemblies", "VECTOR-07", "B / MEDIUM", "RECEIVED", "REQUESTED", "71%", "PPAP review"],
  ["Nova Plastics", "Interior trim panels", "VECTOR-07", "A / HIGH", "RECEIVED", "REQUESTED", "48%", "OTS evidence"],
  ["Quantum Metals", "Seat rails", "ATLAS-12", "A / HIGH", "RECEIVED", "SUBMITTED", "83%", "Readiness review"],
  ["Orion Fasteners", "Bolts & clips", "ATLAS-12", "C / LOW", "RECEIVED", "REQUESTED", "64%", "Capability evidence"],
  ["Vertex Wiring", "Wiring harnesses", "NOVA-01", "C / LOW", "REQUIRED", "APPROVED", "89%", "Timing evidence"],
];

function XReyPreview() {
  const modules = ["COMMAND", "TIMING", "QUALITY", "AUDITS & CAPACITY", "CLAIMS", "DATA INTAKE"];
  const kpis = [
    ["VISIBLE SUPPLIERS", "7", "Ownership from connected trackers"],
    ["TIMING COVERAGE", "83%", "1 plan gap"],
    ["OVERDUE ACTIONS", "5", "Against actual end date"],
    ["OPEN CLAIMS", "6", "2 repeated"],
    ["CRITICAL SUPPLIERS", "2", "Part + supplier criticality"],
  ];
  return (
    <div className="xrey-shell" aria-label="Synthetic public preview of the X-Rey supplier quality assistant">
      <div className="xrey-public-label">SYNTHETIC PUBLIC PREVIEW / REAL INTERFACE ANATOMY</div>
      <div className="xrey-topbar">
        <strong className="xrey-brand"><i /> X-REY</strong>
        <span><small>SQE OWNER</small>NOVA-01</span>
        <span><small>PROGRAM</small>VECTOR-07</span>
        <span><small>SUPPLIER</small>ALL SYNTHETIC</span>
        <span className="xrey-search">SEARCH SUPPLIER, TASK… <kbd>CTRL K</kbd></span>
      </div>
      <div className="xrey-layout">
        <aside className="xrey-sidebar">
          {modules.map((module, index) => <span className={index === 0 ? "active" : ""} key={module}><i />{module}</span>)}
          <div><small>ACTIVE SQE</small><strong>NOVA-01</strong><em>TRACKER DATA</em></div>
        </aside>
        <div className="xrey-main">
          <header><span>EVIDENCE-LED OPERATING VIEW</span><h4>SUPPLIER QUALITY COMMAND</h4><small>NOVA-01 / VECTOR-07</small><button>+ ADD TASK</button></header>
          <div className="xrey-kpis">
            {kpis.map(([label, value, note], index) => <article key={label} className={`tone-${index}`}><span>{label}</span><strong>{value}</strong><small>{note}</small></article>)}
          </div>
          <div className="xrey-alert"><strong>△ &nbsp; Timing plan data required</strong><span>Synthetic reminder: dependencies cannot be trusted until baselines are received.</span><b>›</b></div>
          <section className="xrey-board">
            <header><span>OWNERSHIP-FILTERED PORTFOLIO</span><strong>SUPPLIER CONTROL BOARD</strong><button>▽ FILTER BASIS</button></header>
            <div className="xrey-table-head"><span>SUPPLIER / COMMODITY</span><span>PROGRAM</span><span>CRITICALITY</span><span>TIMING</span><span>PPAP</span><span>PROGRESS</span><span>NEXT GATE</span></div>
            {xreyRows.map((row) => (
              <div className="xrey-table-row" key={row[0]}>
                <span><strong>{row[0]}</strong><small>{row[1]}</small></span>
                <span>{row[2]}</span><span><b>{row[3]}</b></span><span><b>{row[4]}</b></span><span><b>{row[5]}</b></span>
                <span><strong>{row[6]}</strong><i style={{ "--progress": row[6] } as CSSProperties} /></span><span><strong>{row[7]}</strong><small>REVIEW QUEUE</small></span>
              </div>
            ))}
          </section>
          <section className="xrey-priority"><span>DUE HEALTH FROM TASK END DATES</span><strong>PRIORITY ACTION CENTER</strong><button>VIEW ALL</button></section>
        </div>
      </div>
    </div>
  );
}

function StellantisProof() {
  return (
    <div className="stellantis-proof">
      <div className="cycle-proof"><span>MANUAL / BEFORE</span><strong>2 DAYS</strong><ArrowIcon /><span>AUTOMATED / VALIDATED</span><strong>&lt;3 MIN</strong></div>
      <figure><img src="./images/stellantis-workstation.jpeg" alt="Rida developing the Stellantis anomaly-treatment application at a dual-screen workstation" /><figcaption>APPLICATION DEVELOPMENT / VALIDATION ENVIRONMENT</figcaption></figure>
    </div>
  );
}

function Experience() {
  const [active, setActive] = useState(0);
  const item = timeline[active];
  return (
    <section className="experience section-dark" id="experience">
      <SectionHeading
        number="03"
        name="PROFESSIONAL EXPERIENCE"
        headline="Analytics where decisions have consequences."
        aside="Supplier quality / process engineering / data products"
      />
      <div className="experience-room">
        <div className="timeline-list" data-stagger>
          {timeline.map((entry, index) => (
            <button className={active === index ? "active" : ""} key={entry.company} onClick={() => setActive(index)}>
              <span>[0{index + 1}] / {entry.period}</span><strong>{entry.company}</strong><small>{entry.role}</small>
            </button>
          ))}
        </div>
        <article className="experience-detail" key={item.company}>
          <span>{item.place}</span>
          <span className="experience-code">0{active + 1} / 04</span>
          <h3>{item.statement}</h3>
          <div className="experience-metrics">
            {item.metrics.map((metric) => <div key={metric.label}><strong>{metric.value}</strong><span>{metric.label}</span><small>{metric.note}</small></div>)}
          </div>
          <div className={item.proof ? "experience-evidence with-proof" : "experience-evidence"}>
            <ul>{item.details.map((detail) => <li key={detail}>{detail}</li>)}</ul>
            {item.proof === "sqe" ? <XReyPreview /> : null}
            {item.proof === "stellantis" ? <StellantisProof /> : null}
          </div>
          {item.sourceNote ? <p className="experience-note"><span>EVIDENCE NOTE</span>{item.sourceNote}</p> : null}
        </article>
      </div>
    </section>
  );
}

const capabilities = [
  ["OPERATIONS & QUALITY", "Supplier quality management", "Launch / SOP governance", "Corrective actions", "Process reliability"],
  ["DATA & BI", "Forecasting and KPI systems", "Power BI / DAX / SQL", "Dashboards and reporting", "Decision support"],
  ["APPLIED AI", "AI evaluation and validation", "Scenario simulation", "Optimization and routing", "Human-in-the-loop"],
];

function Profile() {
  return (
    <section className="profile section-dark" id="profile">
      <SectionHeading number="04" name="PROFILE" headline="Business context in. Decision system out." />
      <div className="profile-room">
        <div className="profile-intro" data-motion="section">
          <p>Industrial & Production Engineer with hands-on supplier-quality responsibility and a portfolio spanning forecasting, optimization, BI and AI evaluation.</p>
          <div className="credential-list">
            <span>AIAC / Industrial & Production Engineering</span>
            <a href="https://www.linkedin.com/in/rida-melkaoui-7bab50256/details/certifications/" target="_blank" rel="noreferrer">IBM / Data Analyst Professional Certificate</a>
            <span>Arabic / French / English C1</span>
          </div>
        </div>
        <div className="capability-inputs" data-stagger>
          {capabilities.map(([heading, ...items]) => <article key={heading}><h3>{heading}</h3>{items.map((item) => <span key={item}>{item}</span>)}</article>)}
        </div>
        <div className="decision-core">
          <Suspense fallback={<div className="core-scene scene-fallback" aria-hidden="true" />}>
            <DecisionScene variant="core" className="core-scene" />
          </Suspense>
          <span>CONTEXT</span><strong>DECISION<br />CORE</strong><small>TRACEABLE / TESTED / ACTIONABLE</small>
        </div>
        <div className="capability-outputs" data-stagger>
          <span>DECISION SYSTEM OUT.</span>
          <article><strong>SUPPLIER QUALITY</strong><small>Signals → actions</small></article>
          <article><strong>DEMAND FORECAST</strong><small>Forecasts → plans</small></article>
          <article><strong>ROUTING & CAPACITY</strong><small>Constraints → policies</small></article>
          <article><strong>AI RELIABILITY</strong><small>Evidence → confidence</small></article>
        </div>
      </div>
    </section>
  );
}

function Contact() {
  const email = "ridamelkaouiofficial@gmail.com";
  return (
    <footer className="contact" id="contact">
      <div className="contact-heading" data-motion="section"><span>[05] /</span><h2>CONTACT</h2></div>
      <p className="contact-statement" data-motion="section">BRING ME THE <em>MESSY PART.</em></p>
      <div className="contact-links" data-stagger>
        <a href={`mailto:${email}`}>{email}<ArrowIcon /></a>
        <a href="https://www.linkedin.com/in/rida-melkaoui-7bab50256/" target="_blank" rel="noreferrer">LINKEDIN<ArrowIcon /></a>
        <a href="https://github.com/RidaMelkaoui" target="_blank" rel="noreferrer">GITHUB<ArrowIcon /></a>
        <a href="./documents/Rida_Melkaoui_Data_AI_Resume.pdf" target="_blank" rel="noreferrer">DOWNLOAD RESUME<ArrowIcon direction="down" /></a>
      </div>
      <div className="footer-line"><span><i /> DECISION OBSERVATORY / 2026</span><span>KENITRA, MOROCCO</span><span>LET'S BUILD WHAT MATTERS.</span></div>
    </footer>
  );
}

export default function App() {
  const app = useRef<HTMLDivElement>(null);
  usePortfolioMotion(app);
  return (
    <div className="app" ref={app}>
      <Header />
      <main id="main">
        <Hero />
        <Projects />
        <Method />
        <Experience />
        <Profile />
      </main>
      <Contact />
    </div>
  );
}
