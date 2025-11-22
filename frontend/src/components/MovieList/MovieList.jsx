import "./MovieList.css";

import MovieCard from "../MovieCard/MovieCard";

const MovieList = ({ movies, cardType }) => {
  return (
    <div className={"movie-list"}>
      {movies.map((movie) => {
        return <MovieCard movie_data={movie} key={movie.id} cardType={cardType}/>;
      })}
    </div>
  );
};

export default MovieList;
