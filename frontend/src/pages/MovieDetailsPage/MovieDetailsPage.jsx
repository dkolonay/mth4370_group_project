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
  const { id } = useParams();

  useEffect(() => {
    window.scrollTo(0,0);
    api
      .get(`/api/movie/${id}/`)
      .then((res) => res.data)
      .then((data) => {
        setMovieData(data);
        setLoadingMovie(false);
      })
      .catch((err) => console.error(err));

    api
      .get(`/api/recommendations/by-id/?movie_ids=${id}`)
      .then((res) => res.data)
      .then((data) => {
        setMovieRecommendations(data);
        setLoadingRecommendations(false);
      })
      .catch((err) => console.error(err));
  }, [id]);

  return (
    <PageContainer>
      {loadingMovie ? (
        <LoadingIndicator />
      ) : (
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
                <p>{movieData.genres}</p>

                <div className={`review-circle ${movieData.vote_average > 7 ? 'green-circle' : 'red-circle'}`}>
                  <p>{movieData.vote_average.toFixed(1)}</p>
                </div>
                <p>{movieData.vote_count} user ratings</p>
              </div>
            </div>
          </div>

          {loadingRecommendations ? (
            <LoadingIndicator />
          ) : (
            <ContentContainer>
            <div className={"recommendations-area"}>
              <h2>Check out similar films</h2>
              <MovieList movies={movieRecommendations} cardType={"link"} />
            </div>
            </ContentContainer>
          )}
        </div>
      )}
    </PageContainer>
  );
};

export default MovieDetailsPage;
