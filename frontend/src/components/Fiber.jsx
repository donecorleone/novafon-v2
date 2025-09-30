import { Canvas } from "@react-three/fiber";
import { Environment } from "@react-three/drei";
import ScrollAnimation from "./ScrollAnimation";


export default function Fiber() {
  return (
    <Canvas
      camera={{
        fov: 65,
        position: [2.3, 1.5, 2.3],
      }}
    >
      <ScrollAnimation />
      <Environment preset="city" />
    </Canvas>
  );
}
