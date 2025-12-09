import "./SelectedMovieItem.css"
import {motion} from "motion/react"

const SelectedMovieItem = ({movieData, removeFromSelection})=>{
    return(
        <motion.li 
        layout
        initial={{ opacity: 0 }} 
        animate={{ opacity: 1 }}
        transition={{duration: 0.3}}
        className={"selected-movie-item"} 
        onClick={()=>{removeFromSelection(movieData.id)}}>
            <img className={"selected-image"} src={`https://image.tmdb.org/t/p/original/${movieData.poster_path}`} alt={movieData.title} />
            <p className={"selected-title"}>{movieData.title}</p>
            <p className={'selected-list-remove'}>X</p>
        </motion.li>
    )
}

export default SelectedMovieItem;