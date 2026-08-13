import { type RefObject, useLayoutEffect } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export function usePortfolioMotion(scope: RefObject<HTMLElement>) {
  useLayoutEffect(() => {
    const root = scope.current;
    if (!root) return;
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    const context = gsap.context(() => {
      if (reducedMotion) {
        gsap.set("[data-motion], [data-hero-word]", { clearProps: "all" });
        return;
      }

      gsap
        .timeline({ defaults: { ease: "power4.out" } })
        .from(".site-header", { autoAlpha: 0, y: -18, duration: 0.8 })
        .from(
          "[data-hero-word]",
          { autoAlpha: 0, yPercent: 105, rotationX: -7, duration: 1.05, stagger: 0.1 },
          "-=0.48",
        )
        .from(".hero-support, .hero-actions, .hero-proof", { autoAlpha: 0, filter: "blur(8px)", duration: 0.9, stagger: 0.11 }, "-=0.58")
        .from(".portrait-portal", { autoAlpha: 0, scale: 0.94, rotationY: -7, duration: 1.2 }, "-=1.02")
        .from(".signal-legend li", { autoAlpha: 0, x: 14, duration: 0.62, stagger: 0.05 }, "-=0.82");

      gsap.utils.toArray<HTMLElement>("[data-motion='section']").forEach((element) => {
        gsap.fromTo(
          element,
          { autoAlpha: 0, filter: "blur(9px)", y: 22 },
          {
            autoAlpha: 1,
            filter: "blur(0px)",
            y: 0,
            duration: 1.15,
            ease: "power3.out",
            scrollTrigger: { trigger: element, start: "top 84%", once: true },
          },
        );
      });

      gsap.utils.toArray<HTMLElement>("[data-stagger]").forEach((container) => {
        const children = [...container.children];
        gsap.fromTo(
          children,
          { autoAlpha: 0, y: 16, filter: "blur(5px)" },
          {
            autoAlpha: 1,
            y: 0,
            filter: "blur(0px)",
            duration: 0.82,
            stagger: 0.09,
            ease: "power3.out",
            scrollTrigger: { trigger: container, start: "top 82%", once: true },
          },
        );
      });

      gsap.utils.toArray<HTMLElement>("[data-depth-plane]").forEach((plane) => {
        gsap.fromTo(
          plane,
          { yPercent: 4, rotationX: 2.2 },
          {
            yPercent: -3,
            rotationX: -1.2,
            ease: "none",
            scrollTrigger: { trigger: plane, start: "top bottom", end: "bottom top", scrub: 0.7 },
          },
        );
      });
    }, root);

    const refresh = () => ScrollTrigger.refresh();
    window.addEventListener("load", refresh, { once: true });
    return () => {
      window.removeEventListener("load", refresh);
      context.revert();
    };
  }, [scope]);
}
