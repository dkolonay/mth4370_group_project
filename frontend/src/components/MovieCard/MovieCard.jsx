import "./MovieCard.css";

import defaultSrc from "../../assets/img/default_poster.jpg";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import likeIcon from "../../assets/img/like.png"
import dislikeIcon from "../../assets/img/dislike.png"
import {likeMovie, dislikeMovie, removeLikeMovie, removeDislikeMovie} from "../../hooks/useUserActions"

import { motion } from "motion/react";

const BASE_URL = "https://image.tmdb.org/t/p/original/";

const MovieCard = ({
  movie_data,
  cardType,
  addToSelection,
  removeFromSelection,
  selected
}) => {
  const [imgSrc, setImgSrc] = useState(`${BASE_URL}${movie_data.poster_path}`);
  const navigate = useNavigate();
  const [movieData, setMovieData] = useState(movie_data)

  const handleError = (e) => {
    e.preventDefault();
    setImgSrc(defaultSrc);
  };

  useEffect(() => {
    setImgSrc(`https://image.tmdb.org/t/p/original/${movieData.poster_path}`);
  }, [movieData.poster_link]);

  const handleCardClick = () => {
      navigate(`/movie-details/${movieData.id}`);
  };

  const handleSelection = (e)=>{
        e.preventDefault();
        e.stopPropagation();
        if (selected){
            removeFromSelection(movieData.id)
        } else {
            addToSelection(movieData.id)
        }

  }
  const toggleLiked = (e)=>{
    e.stopPropagation(); 
    if (movieData.liked){
      removeLikeMovie(movieData.id)
     

    } else {
      likeMovie(movieData.id)
    }
     setMovieData((prevData)=>{
      return {...prevData, liked: !prevData.liked}
    })
  }

  const toggleDisliked = (e)=>{
    e.stopPropagation(); 
    if (movieData.disliked){
      removeDislikeMovie(movieData.id)
      
    } else {
      dislikeMovie(movieData.id)
    }
         setMovieData((prevData)=>{
      return {...prevData, disliked: !prevData.disliked}
    })
  }

  return (
    <motion.div
            initial={{ opacity: 0 }} 
            animate={{ opacity: 1 }}
            transition={{ duration: 0.3}}
      className={"movie-card"}
      onClick={handleCardClick}
    >
      <div className={"movie-card-image-container"}>
        <img
          className={"movie-card-image"}
          src={imgSrc}
          alt={`${movieData.title}`}
          onError={handleError}
        />
      </div>
      <div className={"movie-card-details"}>
        <h3 className={"movie-card-title"}>{movieData.title}</h3>
        <p>{movieData.vote_average.toFixed(1)} &#9733;</p>
        </div>
        <div className={"card-actions"}>
            <img onClick={toggleLiked} className={`card-icon card-like ${movieData.liked ? "card-action-active" : ""}`} src={likeIcon} alt="like" />
            <img onClick={toggleDisliked} className={`card-icon card-dislike ${movieData.disliked ? "card-action-active": ""}`}src={dislikeIcon} alt="dislike" />
        {cardType === "selector" && <button className={`add-to-search ${selected? 'cut-from-search' : ''}`} onClick={handleSelection}>{selected ? 'Cut from search -' : 'Add to search +'}</button>}
        
      </div>
    </motion.div>
  );
};

export default MovieCard;
