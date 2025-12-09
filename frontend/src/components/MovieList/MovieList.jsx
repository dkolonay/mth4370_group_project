import "./MovieList.css";
import {AnimatePresence} from "motion/react"

import MovieCard from "../MovieCard/MovieCard";

const MovieList = ({ movies, selectedMovies, cardType, addToSelection, removeFromSelection }) => {
  return (
    <div className={"movie-list"}>
      <AnimatePresence>
      {movies.map((movie) => {
        const selected = selectedMovies.some(item => item.id === movie.id)
        return <MovieCard movie_data={movie} key={movie.id} cardType={cardType} addToSelection={addToSelection} removeFromSelection={removeFromSelection} selected={selected}/>;
      })}
      </AnimatePresence>
    </div>
  );
};

export default MovieList;
