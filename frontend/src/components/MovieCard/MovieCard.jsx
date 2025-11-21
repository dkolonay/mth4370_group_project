import "./MovieCard.css"

import defaultSrc from "../../assets/img/default_poster.jpg"
import { useState, useEffect } from "react"

const BASE_URL = "https://image.tmdb.org/t/p/original/"

const MovieCard = ({movie_data}) =>{
    const [imgSrc, setImgSrc] = useState(`${BASE_URL}${movie_data.poster_path}`)
    const handleError = (e)=>{
        e.preventDefault();
        setImgSrc(defaultSrc)
    }

    useEffect(()=>{
        setImgSrc(`https://image.tmdb.org/t/p/original/${movie_data.poster_path}`)
    },[movie_data.poster_link])

    return(
        <div className={"movie-card"}>
            <div className={"movie-card-image-container"}>

            <img className={"movie-card-image"} src={imgSrc} alt={`${movie_data.title}`} onError={handleError} />
            </div>
            <h3 className={"movie-card-title"}>{movie_data.title}</h3>
        </div>
    )
}

export default MovieCard