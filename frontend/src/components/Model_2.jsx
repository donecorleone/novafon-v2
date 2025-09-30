import { useGLTF, MeshTransmissionMaterial, useScroll } from '@react-three/drei'
import { useThree, useFrame } from '@react-three/fiber';
import { useRef, useState, useEffect, useLayoutEffect } from 'react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';


export function Model(props) {
  const { nodes, materials } = useGLTF('./models/model_2-transformed.glb')
  const model = useRef()
  const scroll = useScroll()
  const tl = useRef()

  useFrame((state, delta)=>{
    tl.current.seek(scroll.offset * tl.current.duration())
  })

  useLayoutEffect(()=> {
    tl.current = gsap.timeline({defaults: {duration: 2, ease: 'power1.inOut'}})

    tl.current
    .to(model.current.rotation, {y: 0.6}, 2)
    .to(model.current.position, {x: 1}, 2)

    .to(model.current.rotation, {y: 2}, 6)   
    .to(model.current.position, {x: -1}, 6)

    .to(model.current.rotation, {y: 0}, 11)
    .to(model.current.rotation, {x: 0}, 11)
    .to(model.current.position, {x: 0}, 11)

    .to(model.current.rotation, {y: 0}, 13)
    .to(model.current.rotation, {x: 0}, 13)    
    .to(model.current.position, {x: 0}, 13)

    .to(model.current.rotation, {y: 0}, 16)   
    .to(model.current.rotation, {x: 0}, 16) 
    .to(model.current.position, {x: 0}, 16)    

    .to(model.current.rotation, {y: 0}, 20)    
    .to(model.current.rotation, {x: 0}, 20) 
    .to(model.current.position, {x: 0}, 20)   

  },[])

  return (
    <group ref={model} {...props}>
      <mesh geometry={nodes.Circle.geometry} material={nodes.Circle.material} position={[0.002, 1.426, 0.186]} rotation={[1.276, 0, 0]} scale={0.256} />
      <group position={[0, -0.386, -0.21]}>
        <mesh geometry={nodes.Cube001.geometry} material={materials.Plastik_soft} />
        <mesh geometry={nodes.Cube001_1.geometry} material={materials.Gummi} />
      </group>
      <mesh geometry={nodes.Cube004.geometry} material={materials.Glas} position={[0, 0.995, 0.171]} />
    </group>
  )
}

useGLTF.preload('/models/model_2-transformed.glb')
