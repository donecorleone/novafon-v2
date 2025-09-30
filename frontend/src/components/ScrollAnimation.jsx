import { ScrollControls, Scroll, Environment } from '@react-three/drei';
import { Model } from  './Model_2.jsx'

export default function ScrollAnimation() {
    return (
       <>
            <directionalLight />
            <ambientLight intensity={6} />
            <ScrollControls pages={6} damping={0.1}>
               
                <Model />
                <Scroll html style={{width: '100%'}}>
                    <h1 className='title' style={{ color: '#cdcbca',position: 'absolute', top: `65vh`,left: '50%', fontSize: '13em', transform: `translate(-50%,-50%)` }}>NOVAFON</h1>
          
                    <div className='row' style={{ position: 'absolute', top: `132vh`}}>
                        <h2 style={{ paddingBottom: '20px'}}>novafon power 2</h2>
                        <p style={{ maxWidth: '400px', paddingBottom: '20px' }}>Das novafon power 2 macht die lokale Vibrationstherapie so smart wie nie zuvor. Das große Intensitätsspektrum mit 3 Frequenzen 100, 75 und 50 Hz und bis zu 15 Intensitätsstufen via App bietet die bisher vielfältigsten Einstellungsmöglichkeiten individuell anpassbar auf die Bedürfnisse von Mensch und Tier. Sanft zu empfindlichen und schmerzenden Körperregionen, intensiv einsetzbar bei kompakten Muskelgruppen.</p>
                        <button>Read more</button>
                    </div>

                    <div className='row' style={{ position: 'absolute', top: `230vh`}}>
                        <div className='col' style={{ position: 'absolute', right: `40px`, width: "540px"}}>
                        <h2 style={{ maxWidth: "440px", paddingBottom: '20px' }}>Stay synced</h2>
                        <p style={{ maxWidth: '440px', paddingBottom: '20px' }}>Dank Bluetooth-Konnektivität kann das novafon power 2 ganz einfach mit der novafon App verbunden werden und ermöglicht dadurch eine noch einfachere und individuellere Behandlung. Die praktische „Travel Lock-Funktion“ verhindert zudem unterwegs eine ungewollten Inbetriebnahme des Gerätes und durch die IP Schutzklasse 44 ist DAS NOVAFON power 2 auch gegen Spritzwasser bestens geschützt.</p>                
                        <button>Read more</button>
                        </div>
                    </div>
          
                    <h2 style={{ position: 'absolute', top: '350vh', left: '50%', transform: `translate(-50%,-50%)` }}>Bereit für das was wichtig ist.</h2>              
                    
                    <button style={{ position: 'absolute', top: `590vh`,left: '50%', transform: `translate(-50%,-50%)` }}>Hello there!</button>
                </Scroll>
            </ScrollControls>
            </>
    );
    }