import "./MovieCard.css"

import defaultSrc from "../../assets/img/default_poster.jpg"
import { useState, useEffect } from "react"
import { useNavigate } from "react-router-dom"

const BASE_URL = "https://image.tmdb.org/t/p/original/"

const MovieCard = ({movie_data, cardType}) =>{
    const [imgSrc, setImgSrc] = useState(`${BASE_URL}${movie_data.poster_path}`)
    const [selected, setSelected] = useState(false)
    const navigate = useNavigate()

    const handleError = (e)=>{
        e.preventDefault();
        setImgSrc(defaultSrc)
    }

    useEffect(()=>{
        setImgSrc(`https://image.tmdb.org/t/p/original/${movie_data.poster_path}`)
    },[movie_data.poster_link])

    const handleClick = ()=>{
        if (cardType === "selectable"){
            setSelected((prevSelect)=> !prevSelect)
        } else {
            navigate(`/movie-details/${movie_data.id}`)
        }
    }

    return(
        <div className={"movie-card"} onClick={handleClick}>
            <div className={"movie-card-image-container"}>
            <div className={`movie-card-select-overlay ${selected ? 'remove-transparency' : "" }`}></div>

            <img className={"movie-card-image"} src={imgSrc} alt={`${movie_data.title}`} onError={handleError} />
            </div>
            <h3 className={"movie-card-title"}>{movie_data.title}</h3>
        </div>
    )
}

export default MovieCard