import "../styles/MovieCard.css"

const MovieCard = ({movie_data}) =>{
    return(
        <div className={"movie-card"}>
            <div className={"movie-card-image-container"}>

            <img className={"movie-card-image"} src={movie_data.poster_link} alt="" />
            </div>
            <h3 className={"movie-card-title"}>{movie_data.title}</h3>
        </div>
    )
}

export default MovieCard