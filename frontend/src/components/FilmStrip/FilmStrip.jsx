import { useEffect, useState } from "react";
import "./FilmStrip.css"


const FilmStrip = ({isBottom})=>{
    const [windowWidth, setWindowWidth] = useState(window.innerWidth);
    const filmHoles = []

    useEffect(()=>{
        const handleResize = ()=>{
            setWindowWidth(window.innerWidth);
        }

        window.addEventListener('resize', handleResize);
        return ()=>{
            window.removeEventListener('resize', handleResize);
        }
    }, [])

    const holeWidth = 20;
    const gap = 12;
    let numberOfHoles = Math.round(windowWidth / (holeWidth + gap))

    for (let i = 0; i < numberOfHoles; i++){
        filmHoles.push(
            <div key={`hole ${i}`} className={"film-strip-hole"}></div>
        )
    }

    return(
        <div className={`film-strip ${isBottom ? "bottom-strip": ""}`}>
            {filmHoles}
        </div>
    )
}

export default FilmStrip;