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
        .from(".portrait-portal", { autoAlpha: 0, filter: "blur(5px)", duration: 1.05 }, "-=1.02")
        .from(".signal-legend li", { autoAlpha: 0, x: 14, duration: 0.62, stagger: 0.05 }, "-=0.82");

      const hologram = gsap.timeline({
        delay: 1.2,
        repeat: -1,
        repeatDelay: 1.35,
        defaults: { ease: "power3.out" },
      });
      hologram
        .set(".projection-source", { autoAlpha: 0, scale: 0.72 })
        .set(".projection-rays span", { autoAlpha: 0, scaleY: 0.08, transformOrigin: "50% 100%" })
        .set(".projection-beam", { autoAlpha: 0, scaleY: 0.1, transformOrigin: "50% 100%" })
        .set(".hologram-figure", {
          autoAlpha: 0,
          y: 22,
          scaleX: 0.96,
          scaleY: 0.04,
          transformOrigin: "50% 100%",
          clipPath: "inset(48% 0 48% 0)",
          filter: "blur(7px) brightness(1.8)",
        })
        .set(".hologram-echo, .hologram-scan", { autoAlpha: 0 })
        .to(".projection-source", { autoAlpha: 1, scale: 1, duration: 0.34 })
        .to(".projection-rays span", { autoAlpha: 0.58, scaleY: 1, duration: 0.62, stagger: { each: 0.035, from: "center" } }, "-=0.1")
        .to(".projection-beam", { autoAlpha: 0.28, scaleY: 1, duration: 0.74 }, "-=0.6")
        .to(".hologram-figure", {
          autoAlpha: 0.92,
          y: 0,
          scaleX: 1,
          scaleY: 1,
          clipPath: "inset(0% 0 0% 0)",
          filter: "blur(0px) brightness(1.16)",
          duration: 1.05,
          ease: "expo.out",
        }, "-=0.45")
        .to(".hologram-scan", { autoAlpha: 0.9, yPercent: 1180, duration: 0.78, repeat: 4, ease: "none" }, "-=0.95")
        .to(".hologram-echo", { autoAlpha: 0.25, x: (index) => index ? 7 : -7, duration: 0.07, stagger: 0.025, repeat: 3, yoyo: true }, "-=3.4")
        .to(".hologram-figure", { x: -4, skewX: 1.4, duration: 0.055, repeat: 3, yoyo: true, ease: "steps(1)" }, "-=1.95")
        .to(".hologram-figure", { x: 0, skewX: 0, duration: 0.1 })
        .to(".hologram-echo", { autoAlpha: 0.18, x: (index) => index ? -9 : 9, duration: 0.06, repeat: 2, yoyo: true }, "+=1.15")
        .to(".hologram-figure", {
          autoAlpha: 0,
          y: 18,
          scaleY: 0.045,
          clipPath: "inset(48% 0 48% 0)",
          filter: "blur(6px) brightness(1.8)",
          duration: 0.82,
          ease: "power3.in",
        }, "+=1.35")
        .to(".projection-beam, .projection-rays span", { autoAlpha: 0, scaleY: 0.08, duration: 0.42, stagger: 0.018 }, "-=0.45")
        .to(".projection-source", { autoAlpha: 0, scale: 0.72, duration: 0.25 }, "-=0.18");

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
