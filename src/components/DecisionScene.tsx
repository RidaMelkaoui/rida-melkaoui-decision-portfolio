import { Canvas, useFrame } from "@react-three/fiber";
import { useMemo, useRef } from "react";
import * as THREE from "three";

type DecisionSceneProps = {
  variant?: "convergence" | "core";
  className?: string;
};

function useReducedMotion() {
  return typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

function ConvergenceField() {
  const group = useRef<THREE.Group>(null);
  const reducedMotion = useReducedMotion();

  const { curvePositions, signalPositions, signalColors } = useMemo(() => {
    const curve: number[] = [];
    const signals: number[] = [];
    const colors: number[] = [];
    const blue = new THREE.Color("#2f5bff");
    const orange = new THREE.Color("#ff5b22");

    for (let index = 0; index < 34; index += 1) {
      const start = new THREE.Vector3(
        -2.7 + (index % 4) * 0.12,
        -1.85 + (index / 33) * 3.7,
        Math.sin(index * 1.71) * 0.72,
      );
      const end = new THREE.Vector3(2.38, 0, 0);
      const path = new THREE.CatmullRomCurve3([
        start,
        new THREE.Vector3(-1.3, start.y * 0.82, start.z * 0.55),
        new THREE.Vector3(0.2, start.y * 0.46, start.z * 0.22),
        new THREE.Vector3(1.2, start.y * 0.2, 0),
        end,
      ]);
      const points = path.getPoints(20);
      for (let point = 0; point < points.length - 1; point += 1) {
        curve.push(...points[point].toArray(), ...points[point + 1].toArray());
      }
      signals.push(...start.toArray());
      const color = index % 5 === 0 ? orange : blue;
      colors.push(color.r, color.g, color.b);
    }
    signals.push(2.38, 0, 0);
    colors.push(1, 0.35, 0.12);
    return {
      curvePositions: new Float32Array(curve),
      signalPositions: new Float32Array(signals),
      signalColors: new Float32Array(colors),
    };
  }, []);

  useFrame(({ clock, pointer }, delta) => {
    if (!group.current || reducedMotion) return;
    group.current.rotation.y = THREE.MathUtils.damp(group.current.rotation.y, pointer.x * 0.11, 3, delta);
    group.current.rotation.x = THREE.MathUtils.damp(group.current.rotation.x, -pointer.y * 0.07, 3, delta);
    group.current.position.z = Math.sin(clock.elapsedTime * 0.35) * 0.08;
  });

  return (
    <group ref={group} rotation={[0.08, -0.18, -0.04]}>
      <lineSegments>
        <bufferGeometry>
          <bufferAttribute attach="attributes-position" args={[curvePositions, 3]} />
        </bufferGeometry>
        <lineBasicMaterial color="#5577ff" transparent opacity={0.32} />
      </lineSegments>
      <points>
        <bufferGeometry>
          <bufferAttribute attach="attributes-position" args={[signalPositions, 3]} />
          <bufferAttribute attach="attributes-color" args={[signalColors, 3]} />
        </bufferGeometry>
        <pointsMaterial size={0.075} vertexColors transparent opacity={0.92} sizeAttenuation />
      </points>
      <mesh position={[2.38, 0, 0]}>
        <sphereGeometry args={[0.14, 24, 24]} />
        <meshBasicMaterial color="#ff5b22" />
      </mesh>
      <mesh position={[2.38, 0, 0]} rotation={[Math.PI / 2, 0, 0]}>
        <torusGeometry args={[0.34, 0.012, 10, 96]} />
        <meshBasicMaterial color="#ffb18d" transparent opacity={0.7} />
      </mesh>
    </group>
  );
}

function DecisionCore() {
  const group = useRef<THREE.Group>(null);
  const reducedMotion = useReducedMotion();
  const points = useMemo(() => {
    const result: number[] = [];
    for (let x = -2; x <= 2; x += 1) {
      for (let y = -2; y <= 2; y += 1) {
        for (let z = -2; z <= 2; z += 1) {
          result.push(x * 0.37, y * 0.37, z * 0.37);
        }
      }
    }
    return new Float32Array(result);
  }, []);

  useFrame(({ clock, pointer }, delta) => {
    if (!group.current || reducedMotion) return;
    group.current.rotation.y += delta * 0.12;
    group.current.rotation.x = THREE.MathUtils.damp(
      group.current.rotation.x,
      pointer.y * 0.16 + Math.sin(clock.elapsedTime * 0.22) * 0.08,
      2,
      delta,
    );
  });

  return (
    <group ref={group}>
      <points>
        <bufferGeometry>
          <bufferAttribute attach="attributes-position" args={[points, 3]} />
        </bufferGeometry>
        <pointsMaterial color="#dbe3ff" size={0.042} transparent opacity={0.78} sizeAttenuation />
      </points>
      {[0.95, 1.2, 1.46].map((radius, index) => (
        <mesh key={radius} rotation={[Math.PI / 2 + index * 0.44, index * 0.35, index * 0.2]}>
          <torusGeometry args={[radius, 0.008 + index * 0.002, 8, 120]} />
          <meshBasicMaterial color={index === 2 ? "#ff5b22" : "#2f5bff"} transparent opacity={0.52} />
        </mesh>
      ))}
      <mesh>
        <icosahedronGeometry args={[0.92, 1]} />
        <meshBasicMaterial color="#2f5bff" wireframe transparent opacity={0.18} />
      </mesh>
    </group>
  );
}

export function DecisionScene({ variant = "convergence", className }: DecisionSceneProps) {
  return (
    <div className={className} aria-hidden="true">
      <Canvas
        camera={{ position: [0, 0, variant === "core" ? 4.5 : 6.8], fov: variant === "core" ? 44 : 42 }}
        dpr={[1, 1.6]}
        gl={{ antialias: true, alpha: true, powerPreference: "high-performance" }}
      >
        {variant === "core" ? <DecisionCore /> : <ConvergenceField />}
      </Canvas>
    </div>
  );
}
