import "./MovieCard.css";

import defaultSrc from "../../assets/img/default_poster.jpg";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

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

  const handleError = (e) => {
    e.preventDefault();
    setImgSrc(defaultSrc);
  };

  useEffect(() => {
    setImgSrc(`https://image.tmdb.org/t/p/original/${movie_data.poster_path}`);
  }, [movie_data.poster_link]);

  const handleCardClick = () => {
      navigate(`/movie-details/${movie_data.id}`);
  };

  const handleSelection = (e)=>{
        e.preventDefault();
        e.stopPropagation();
        if (selected){
            removeFromSelection(movie_data.id)
        } else {
            addToSelection(movie_data.id)
        }

  }

  return (
    <motion.div
            initial={{ opacity: 0 }}      // fade in
            animate={{ opacity: 1 }}
            transition={{ duration: 0.3}}
      className={"movie-card"}
      onClick={handleCardClick}
    >
      <div className={"movie-card-image-container"}>
        <img
          className={"movie-card-image"}
          src={imgSrc}
          alt={`${movie_data.title}`}
          onError={handleError}
        />
      </div>
      <div className={"movie-card-details"}>
        <h3 className={"movie-card-title"}>{movie_data.title}</h3>
        <p>{movie_data.vote_average.toFixed(1)} &#9733;</p>
        {cardType === "selector" && <button onClick={handleSelection}>{selected ? 'Remove from search' : 'Add to search'}</button>}
      </div>
    </motion.div>
  );
};

export default MovieCard;
