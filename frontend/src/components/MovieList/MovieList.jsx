import "./MovieList.css";

import MovieCard from "../MovieCard/MovieCard";

const MovieList = ({ movies, cardType, addToSelection, removeFromSelection }) => {
  return (
    <div className={"movie-list"}>
      {movies.map((movie) => {
        return <MovieCard movie_data={movie} key={movie.id} cardType={cardType} addToSelection={addToSelection} removeFromSelection={removeFromSelection}/>;
      })}
    </div>
  );
};

export default MovieList;
