import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import PageContainer from "../../components/PageContainer/PageContainer";
import ContentContainer from "../../components/ContentContainer/ContentContainer";
import LoadingIndicator from "../../components/LoadingIndicator/LoadingIndicator";
import MovieList from "../../components/MovieList/MovieList";
import api from "../../api";
import "./MovieDetailsPage.css";

import defaultPoster from "../../assets/img/default_poster.jpg"
import defaultBanner from "../../assets/img/default_banner.jpg"

const MovieDetailsPage = () => {
  const [movieData, setMovieData] = useState({});
  const [movieRecommendations, setMovieRecommendations] = useState([]);
  const [loadingMovie, setLoadingMovie] = useState(true);
  const [loadingRecommendations, setLoadingRecommendations] = useState(true);
  const [liked, setLiked] = useState(false);
  const [disliked, setDisliked] = useState(false);
  const { id } = useParams();

  useEffect(() => {
    window.scrollTo(0,0);
    api
      .get(`/api/movie/${id}/`)
      .then((res) => res.data)
      .then((data) => {
        setMovieData(data.movie_data);
        setLiked(data.liked);
        setDisliked(data.disliked)
        setLoadingMovie(false);
      })
      .catch((err) => console.error(err));

    api
      .get(`/api/movies/`, {params: {movie_ids: id}})
      .then((res) => res.data)
      .then((data) => {
        setMovieRecommendations(data);
        setLoadingRecommendations(false);
      })
      .catch((err) => console.error(err));
  }, [id]);

  const likeMovie = (e)=>{
    e.preventDefault();
    const movie_id = movieData.id
     api
      .post(`/api/user-actions/like/`, {movie_id})
      .then((res) => {
        if (res.status === 201){
          setLiked(true);
        }
      })
      .catch((err) => console.error(err));

  }

  const removeLikeMovie = (e)=>{
    e.preventDefault();
    const movie_id = movieData.id
     api
      .delete(`/api/user-actions/like/remove/${movie_id}/`)
      .then((res) => {
        if (res.status === 204){
          setLiked(false);
        }
      })
      .catch((err) => console.error(err));

  }

  const dislikeMovie = (e)=>{
    e.preventDefault();
    const movie_id = movieData.id
     api
      .post(`/api/user-actions/dislike/`, {movie_id})
      .then((res) => {
        if (res.status === 201){
          setDisliked(true);
        }
      })
      .catch((err) => console.error(err));

  }

  const removeDislikeMovie = (e)=>{
    e.preventDefault();
    const movie_id = movieData.id
     api
      .delete(`/api/user-actions/dislike/remove/${movie_id}/`)
      .then((res) => {
        if (res.status === 204){
          setDisliked(false);
        }
      })
      .catch((err) => console.error(err));

  }

  return (
    <PageContainer>
      {!loadingMovie && (
        <div className={"detail-page"}>
          <div className={"details-header"}>
            <div className={"banner-container"}>
              <img
                src={movieData.backdrop_path ? `https://image.tmdb.org/t/p/original/${movieData.backdrop_path}` : defaultBanner}
                alt={movieData.title}
                className={"movie-banner"}
              />
            </div>

            <div className={"details-container"}>
              <img
                className={"details-poster"}
                src={movieData.poster_path ? `https://image.tmdb.org/t/p/original/${movieData.poster_path}` : defaultPoster}
                alt={movieData.title}
              />
              <div className={"details-content-area"}>
                <h1>{movieData.title}</h1>
                <p>{new Date(movieData.release_date).getFullYear()}</p>
                <p>{movieData.overview}</p>
                <div className={"genre-list"}>

                {movieData.genres.split(",", 6).map((genre)=>{
                  return (
                  <p key={genre} className={"genre-item"}>{genre}</p>
                )
                })}
                </div>

                <div className={`review-circle ${movieData.vote_average > 7 ? 'green-circle' : 'red-circle'}`}>
                  <p>{movieData.vote_average.toFixed(1)}</p>
                </div>
                <p>{movieData.vote_count} user ratings</p>
                <button className={`action-button like-button ${liked ? 'like-active' : ''}`} onClick={liked? removeLikeMovie : likeMovie}>Like</button>
                <button className={`action-button dislike-button ${disliked ? 'dislike-active' : ''}`} onClick={disliked ? removeDislikeMovie : dislikeMovie}>Not Interested</button>
              </div>
            </div>
          </div>

          {loadingRecommendations ? (
            <LoadingIndicator />
          ) : (
            <ContentContainer>
            <div className={"recommendations-area"}>
              <h2 className={"rec-title"}>Check out similar films</h2>
              <MovieList movies={movieRecommendations} cardType={"basic"} />
            </div>
            </ContentContainer>
          )}
        </div>
      )}
    </PageContainer>
  );
};

export default MovieDetailsPage;
