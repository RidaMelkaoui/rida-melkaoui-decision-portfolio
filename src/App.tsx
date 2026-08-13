import { useEffect, useState } from "react";

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

type Experience = {
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
      "To make forecasting useful at the planning desk, I built a cutoff-safe M5 pipeline that challenges a global count model with a calibration-selected seasonal baseline, then converts the winning signal into weekly policy scenarios and an exception queue. The result exposes the service-versus-inventory trade-off instead of hiding it behind one accuracy score.",
    proof: [
      "900 item-store series",
      "4.5% lower WAPE vs selected baseline",
      "96.7% simulated fulfilled demand",
    ],
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
      "To move routing from abstract optimization to a pre-dispatch choice, I learned zone-order preferences from 6,112 historical routes and combined them with directed travel time, timed-package guardrails and constrained local search. The control tower compares policies route by route, preserves service, and sends the remaining exceptions to a dispatcher for review.",
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
      "To replace leaderboard optimism with a release decision, I reconstructed four-trial reliability, cost, latency, tool behaviour and evaluator signals from official agent trajectories. The interface separates stable, unstable and always-failing tasks, applies a transparent release gate, and points the team to the failure family that deserves intervention first.",
    proof: ["3,336 official trajectories", "4 trials per task", "99.0% missing-action diagnostic share"],
    evidenceChain: ["Pinned official trajectories", "Pass-k + deterministic diagnostics", "Release / monitor / hold gate"],
    stack: "Python / agent evaluation / statistics / failure diagnostics / React",
    image: "./images/projects/agent-proof.png",
    lab: "./labs/agent/index.html",
    source: "https://github.com/RidaMelkaoui/agent-reliability-lab",
    caveat: "Pinned historical tau2-bench cohort; no live calls or current-production claim.",
  },
];

const timeline: Experience[] = [
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
    sourceNote: "System scope only. The interface preview below uses synthetic programs, suppliers and KPI values.",
  },
  {
    period: "FEB - AUG 2025",
    company: "STELLANTIS R&D",
    place: "CASABLANCA, MOROCCO",
    role: "Engineering Intern / Data Analytics, Process Optimization & AI",
    statement: "Converted a two-day BOM anomaly workflow into a sub-three-minute validated process.",
    details: [
      "Mapped the E-BOM/M-BOM decision flow and its failure modes, then translated the status logic into a standardized treatment process.",
      "Built a Python detector around exported configuration data for anomaly identification, prioritization and treatment traceability.",
      "Benchmarked the automated workflow against the manual process and documented limitations around live PLM/SAP integration and data quality.",
    ],
    metrics: [
      { value: "2 days", label: "manual cycle", note: "before automation" },
      { value: "<3 min", label: "automated cycle", note: "validation benchmark" },
      { value: "−98%", label: "manual handling", note: "100% to 2%" },
      { value: "100%", label: "processing reliability", note: "project test cases" },
    ],
    proof: "stellantis",
    sourceNote: "PFE validation benchmark; this is not presented as a plant-wide production deployment.",
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

function ArrowIcon({ direction = "up-right" }: { direction?: "up-right" | "right" | "down" }) {
  const paths = {
    "up-right": "M5 15 15 5M7 5h8v8",
    right: "M4 10h12M11 5l5 5-5 5",
    down: "M10 4v12M5 11l5 5 5-5",
  };
  return (
    <svg className="action-icon" viewBox="0 0 20 20" aria-hidden="true">
      <path d={paths[direction]} />
    </svg>
  );
}

function Header() {
  const [open, setOpen] = useState(false);
  const [active, setActive] = useState("top");
  const nav = [
    ["Work", "work"],
    ["Method", "method"],
    ["Experience", "experience"],
    ["Profile", "profile"],
    ["Contact", "contact"],
  ];

  useEffect(() => {
    const sections = ["top", ...nav.map(([, id]) => id)]
      .map((id) => document.getElementById(id))
      .filter((section): section is HTMLElement => Boolean(section));
    const updateHeader = () => {
      const total = document.documentElement.scrollHeight - window.innerHeight;
      const progress = total > 0 ? Math.min(1, Math.max(0, window.scrollY / total)) : 0;
      document.documentElement.style.setProperty("--scroll-progress", String(progress));

      const threshold = 120;
      const current = sections.reduce((selected, section) => {
        return section.getBoundingClientRect().top <= threshold ? section : selected;
      }, sections[0]);
      setActive(current?.id ?? "top");
    };
    updateHeader();
    window.addEventListener("scroll", updateHeader, { passive: true });
    return () => window.removeEventListener("scroll", updateHeader);
  }, []);

  useEffect(() => {
    if (!open) return;
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") setOpen(false);
    };
    window.addEventListener("keydown", closeOnEscape);
    return () => window.removeEventListener("keydown", closeOnEscape);
  }, [open]);

  return (
    <header className="site-header">
      <a className="wordmark" href="#top">
        <span>RM</span> / DECISION ENGINEER
      </a>
      <nav className={open ? "open" : ""} aria-label="Primary">
        {nav.map(([label, id]) => (
          <a
            key={id}
            href={`#${id}`}
            aria-current={active === id ? "location" : undefined}
            onClick={() => setOpen(false)}
          >
            {label}
          </a>
        ))}
      </nav>
      <a
        className="resume-link"
        href="./documents/Rida_Melkaoui_Data_AI_Resume.pdf"
        aria-label="Download Rida Melkaoui resume as PDF"
        download
      >
        RESUME <ArrowIcon direction="down" />
      </a>
      <button
        className="menu-toggle"
        aria-label="Toggle navigation"
        aria-expanded={open}
        onClick={() => setOpen((value) => !value)}
      >
        <i />
        <i />
        <i />
      </button>
    </header>
  );
}

function Hero() {
  return (
    <section className="hero" id="top">
      <div className="hero-copy">
        <div className="kicker">INDUSTRIAL ENGINEER / DATA + AI / BI</div>
        <h1>
          I BUILD
          <br />
          <em>DECISION</em>
          <br />
          SYSTEMS.
        </h1>
        <p>
          Forecast demand. Control operational risk. Test whether an AI agent is actually reliable. I turn complex
          workflows into evidence people can act on.
        </p>
        <div className="hero-actions">
          <a href="#work">
            ENTER THE DECISION ROOM <ArrowIcon direction="right" />
          </a>
          <a href="mailto:ridamelkaouiofficial@gmail.com">
            DISCUSS A PROBLEM <ArrowIcon direction="up-right" />
          </a>
        </div>
        <div className="hero-proof">
          <span>LIVE OPERATIONS</span>
          <strong>Supplier quality at Magna International</strong>
          <small>Industrial context / global collaboration / analytics built around action</small>
        </div>
      </div>
      <div
        className="portrait-stage"
        aria-label="Portrait of Rida Melkaoui"
        onPointerMove={(event) => {
          const bounds = event.currentTarget.getBoundingClientRect();
          const x = (event.clientX - bounds.left) / bounds.width - 0.5;
          const y = (event.clientY - bounds.top) / bounds.height - 0.5;
          event.currentTarget.style.setProperty("--portrait-x", `${x * -10}px`);
          event.currentTarget.style.setProperty("--portrait-y", `${y * -8}px`);
          event.currentTarget.style.setProperty("--portrait-rx", `${y * -1.8}deg`);
          event.currentTarget.style.setProperty("--portrait-ry", `${x * 2.2}deg`);
        }}
        onPointerLeave={(event) => {
          event.currentTarget.style.removeProperty("--portrait-x");
          event.currentTarget.style.removeProperty("--portrait-y");
          event.currentTarget.style.removeProperty("--portrait-rx");
          event.currentTarget.style.removeProperty("--portrait-ry");
        }}
      >
        <div className="portrait-ghost" aria-hidden="true">
          RIDA
          <br />
          MELKAOUI
        </div>
        <div className="portrait-orbit orbit-a" aria-hidden="true" />
        <div className="portrait-orbit orbit-b" aria-hidden="true" />
        <div className="portrait-axis" aria-hidden="true">
          <span>OPERATIONS</span>
          <span>DATA</span>
          <span>AI</span>
          <span>DECISIONS</span>
        </div>
        <img src="./images/rida-cutout.png" alt="Rida Melkaoui, industrial engineer and data/AI professional" />
        <span className="coordinate coordinate-a">33.9716 N</span>
        <span className="coordinate coordinate-b">06.8498 W</span>
        <div className="portrait-label">
          <span>RIDA MELKAOUI</span>
          <small>OPERATIONS - DATA - DECISION</small>
        </div>
      </div>
      <div className="hero-rail">
        <span>[ CURRENT SIGNAL ]</span>
        <b>Kenitra, Morocco / Building at the intersection of industrial operations and intelligent systems</b>
      </div>
    </section>
  );
}

function SectionIntro({ index, label, title, body }: { index: string; label: string; title: string; body?: string }) {
  return (
    <header className="section-intro" data-reveal>
      <div>
        <span>[{index}]</span>
        <small>{label}</small>
      </div>
      <h2>{title}</h2>
      {body ? <p>{body}</p> : null}
    </header>
  );
}

function ProjectCase({ project, active, onOpen }: { project: Project; active: boolean; onOpen: () => void }) {
  const bodyId = `project-${project.key}-detail`;
  return (
    <article className={`project-case ${active ? "active" : ""}`}>
      <button className="case-cover" onClick={onOpen} aria-expanded={active} aria-controls={bodyId}>
        <div className="case-index">[{project.index}]</div>
        <div className="case-title">
          <span>{project.title}</span>
          <h3>{project.thesis}</h3>
          <p>{project.question}</p>
        </div>
        <div className="case-result">
          <strong>{project.result}</strong>
          <span>{project.resultNote}</span>
        </div>
        <span className="case-toggle">
          <i aria-hidden="true" />
          {active ? "CLOSE CASE" : "OPEN CASE"}
        </span>
      </button>
      {active ? (
        <div className="case-body" id={bodyId}>
          <div className="case-visual">
            <img src={project.image} alt={`${project.title} decision dashboard`} />
            <span>VERIFIED INTERFACE / DESKTOP</span>
          </div>
          <div className="case-evidence">
            <div>
              <span className="mini-label">DECISION SUPPORTED</span>
              <h4>{project.question}</h4>
            </div>
            <p className="case-narrative">{project.narrative}</p>
            <ol>
              {project.proof.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ol>
            <div className="evidence-chain" aria-label={`${project.title} evidence chain`}>
              {project.evidenceChain.map((item, index) => (
                <div key={item}>
                  <span>0{index + 1}</span>
                  <strong>{item}</strong>
                  {index < project.evidenceChain.length - 1 ? <ArrowIcon direction="right" /> : null}
                </div>
              ))}
            </div>
            <p className="case-stack">{project.stack}</p>
            <small>{project.caveat}</small>
            <div className="case-actions">
              <a href={project.lab} target="_blank" rel="noreferrer">
                OPEN LIVE LAB <ArrowIcon direction="up-right" />
              </a>
              <a href={project.source} target="_blank" rel="noreferrer">
                OPEN SOURCE REPO <ArrowIcon direction="up-right" />
              </a>
            </div>
          </div>
        </div>
      ) : null}
    </article>
  );
}

function Work() {
  const [active, setActive] = useState<ProjectKey | null>("demand");
  return (
    <section className="work section-shell" id="work">
      <SectionIntro
        index="01"
        label="SELECTED SYSTEMS"
        title="Proof, not promises."
        body="Each build starts with an operating decision, uses public or non-confidential evidence, and ends with a tested interface a stakeholder can interrogate."
      />
      <div className="project-list">
        {projects.map((project) => (
          <ProjectCase
            key={project.key}
            project={project}
            active={project.key === active}
            onOpen={() => setActive((current) => (current === project.key ? null : project.key))}
          />
        ))}
      </div>
    </section>
  );
}

function Method() {
  const steps = [
    ["01", "FRAME", "Name the decision, actor, action and cost of being wrong."],
    ["02", "PROVE", "Build the data contract, quality gates, baselines and claim boundaries."],
    ["03", "MODEL", "Use the simplest defensible statistical, optimization or AI method."],
    ["04", "OPERATE", "Deliver an interface, exception queue and evidence trail - not a notebook alone."],
  ];
  return (
    <section className="method" id="method">
      <SectionIntro index="02" label="HOW I WORK" title="From ambiguity to an operating decision." />
      <div className="method-track" data-reveal>
        {steps.map(([number, title, body]) => (
          <article key={number}>
            <span>{number}</span>
            <i />
            <h3>{title}</h3>
            <p>{body}</p>
          </article>
        ))}
      </div>
      <div className="method-manifesto" data-reveal>
        <span>THE STANDARD</span>
        <p>Useful analytics changes the next action. Reliable AI survives repetition. Good BI keeps the owner, exception and deadline visible.</p>
      </div>
    </section>
  );
}

function SQEDemo() {
  const rows = [
    ["NOVA-01", "ELECTRONICS", "LAUNCH", "86%", "REVIEW"],
    ["VECTOR-07", "METAL", "SAFE LAUNCH", "72%", "AT RISK"],
    ["ATLAS-12", "MECHATRONICS", "SOP", "96%", "ON TRACK"],
  ];
  return (
    <div className="sqe-demo" role="img" aria-label="Synthetic preview of the supplier quality assistant">
      <div className="demo-topline">
        <div>
          <span>SQE / CONTROL</span>
          <strong>SUPPLIER QUALITY COMMAND</strong>
        </div>
        <i>SYNTHETIC DATA</i>
      </div>
      <div className="demo-kpis">
        <div><span>TIMING COVERAGE</span><strong>92%</strong></div>
        <div><span>OVERDUE ACTIONS</span><strong>04</strong></div>
        <div><span>CRITICAL SIGNALS</span><strong>02</strong></div>
      </div>
      <div className="demo-table" aria-hidden="true">
        <div className="demo-table-head"><span>PROGRAM</span><span>COMMODITY</span><span>GATE</span><span>READINESS</span><span>DECISION</span></div>
        {rows.map(([program, commodity, gate, readiness, decision]) => (
          <div className="demo-table-row" key={program}>
            <strong>{program}</strong><span>{commodity}</span><span>{gate}</span><span>{readiness}</span><i>{decision}</i>
          </div>
        ))}
      </div>
      <div className="demo-modules">
        <span>COMMAND</span><span>TIMING</span><span>QUALITY</span><span>AUDITS</span><span>CLAIMS</span><span>INTAKE</span>
      </div>
    </div>
  );
}

function StellantisProof() {
  return (
    <div className="stellantis-proof">
      <div className="cycle-comparison" role="img" aria-label="Manual cycle of two days compared with an automated cycle under three minutes">
        <div>
          <span>MANUAL / BEFORE</span>
          <strong>2 DAYS</strong>
          <i><b /></i>
        </div>
        <ArrowIcon direction="right" />
        <div>
          <span>AUTOMATED / VALIDATED</span>
          <strong>&lt;3 MIN</strong>
          <i><b /></i>
        </div>
      </div>
      <figure className="workbench-photo">
        <img src="./images/rida-workbench.jpeg" alt="Rida Melkaoui building and testing the anomaly-processing application" />
        <figcaption><span>BUILD / TEST / VALIDATE</span><b>ENGINEERING WORKBENCH / 2025</b></figcaption>
      </figure>
    </div>
  );
}

function Experience() {
  const [active, setActive] = useState(0);
  const item = timeline[active];
  return (
    <section className="experience section-shell" id="experience">
      <SectionIntro index="03" label="OPERATING CONTEXT" title="I learned analytics where decisions have consequences." />
      <div className="experience-grid" data-reveal>
        <div className="timeline-list">
          {timeline.map((item, index) => (
            <button key={item.company} className={active === index ? "active" : ""} onClick={() => setActive(index)}>
              <span>{item.period}</span>
              <strong>{item.company}</strong>
              <small>{item.role}</small>
            </button>
          ))}
        </div>
        <article className="experience-detail" aria-live="polite" key={item.company}>
          <div className="experience-code">0{active + 1} / 04</div>
          <span>{item.place}</span>
          <h3>{item.statement}</h3>
          <div className="experience-metrics" aria-label={`${item.company} quantified evidence`}>
            {item.metrics.map((metric) => (
              <div key={`${metric.value}-${metric.label}`}>
                <strong>{metric.value}</strong>
                <span>{metric.label}</span>
                <small>{metric.note}</small>
              </div>
            ))}
          </div>
          <div className={`experience-lower ${item.proof ? "with-proof" : ""}`}>
            <ul>
              {item.details.map((detail) => (
                <li key={detail}>{detail}</li>
              ))}
            </ul>
            {item.proof === "sqe" ? <SQEDemo /> : null}
            {item.proof === "stellantis" ? <StellantisProof /> : null}
          </div>
          {item.sourceNote ? (
            <p className="experience-source">
              <span>EVIDENCE NOTE</span>
              {item.sourceNote}
            </p>
          ) : null}
          {active === 0 ? (
            <div className="world-strip">
              <i>CN</i>
              <i>ES</i>
              <i>SK</i>
              <i>DE</i>
              <i>KR</i>
              <i>MA</i>
              <span>GLOBAL SUPPLIER RANGE</span>
            </div>
          ) : null}
        </article>
      </div>
    </section>
  );
}

function Profile() {
  const [copied, setCopied] = useState(false);
  const email = "ridamelkaouiofficial@gmail.com";
  const copy = async () => {
    try {
      await navigator.clipboard.writeText(email);
    } catch {
      const fallback = document.createElement("textarea");
      fallback.value = email;
      fallback.setAttribute("readonly", "");
      fallback.style.position = "fixed";
      fallback.style.opacity = "0";
      document.body.appendChild(fallback);
      fallback.select();
      document.execCommand("copy");
      fallback.remove();
    }
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1500);
  };
  return (
    <>
      <section className="profile section-shell" id="profile">
        <SectionIntro index="04" label="PROFILE" title="Business context in. Decision system out." />
        <div className="profile-grid" data-reveal>
          <p className="profile-lead">
            Industrial & Production Engineer with hands-on supplier-quality responsibility and a portfolio spanning forecasting, optimization, BI and AI evaluation.
          </p>
          <div className="capability-grid">
            <div>
              <span>ANALYZE</span>
              <p>SQL / Python / statistics / forecasting / experimentation / data quality</p>
            </div>
            <div>
              <span>BUILD</span>
              <p>Power BI / DAX / data models / React / APIs / automation / decision interfaces</p>
            </div>
            <div>
              <span>OPERATE</span>
              <p>Supplier quality / launches / 8D-CAPA / FMEA / Lean / cross-functional communication</p>
            </div>
          </div>
        </div>
        <div className="credential-rail" data-reveal>
          <div>
            <span>EDUCATION</span>
            <strong>Industrial & Production Engineering</strong>
            <small>AIAC / 2022-2025</small>
            <small>Preparatory Classes MPSI-MP / 2020-2022</small>
          </div>
          <div>
            <span>CERTIFICATIONS</span>
            <strong>IBM Data Analyst Professional Certificate</strong>
            <small>EF SET C1 / TOEIC 855</small>
          </div>
          <div>
            <span>LANGUAGES</span>
            <strong>Arabic / French / English</strong>
            <small>Native / Fluent / C1</small>
          </div>
        </div>
      </section>
      <footer id="contact" className="contact">
        <span className="contact-index">[05] CONTACT</span>
        <h2>
          BRING ME THE
          <br />
          <em>MESSY PART.</em>
        </h2>
        <p>If the problem involves operational complexity, unreliable data, repeated manual decisions or AI that needs proof, I want to hear about it.</p>
        <div className="contact-links">
          <a href={`mailto:${email}`}>
            EMAIL ME <ArrowIcon direction="up-right" />
          </a>
          <button onClick={copy}>{copied ? "EMAIL COPIED" : "COPY EMAIL"}</button>
          <a href="https://www.linkedin.com/in/rida-melkaoui-7bab50256/" target="_blank" rel="noreferrer">
            LINKEDIN <ArrowIcon direction="up-right" />
          </a>
          <a href="https://github.com/RidaMelkaoui" target="_blank" rel="noreferrer">
            GITHUB <ArrowIcon direction="up-right" />
          </a>
        </div>
        <div className="footer-line">
          <span>RIDA MELKAOUI / 2026</span>
          <span>INDUSTRIAL ENGINEER / DATA + AI / BI</span>
          <span>KENITRA, MOROCCO</span>
        </div>
      </footer>
    </>
  );
}

export default function App() {
  useEffect(() => {
    document.documentElement.classList.add("ready");
    const nodes = Array.from(document.querySelectorAll<HTMLElement>("[data-reveal]"));
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduceMotion) {
      nodes.forEach((node) => node.classList.add("is-visible"));
      return () => document.documentElement.classList.remove("ready");
    }
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      { rootMargin: "0px 0px -10%", threshold: 0.08 },
    );
    nodes.forEach((node) => observer.observe(node));
    return () => {
      observer.disconnect();
      document.documentElement.classList.remove("ready");
    };
  }, []);

  return (
    <>
      <Header />
      <main id="main">
        <Hero />
        <Work />
        <Method />
        <Experience />
        <Profile />
      </main>
    </>
  );
}
