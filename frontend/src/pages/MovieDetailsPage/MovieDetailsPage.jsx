import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import PageContainer from "../../components/PageContainer/PageContainer";
import LoadingIndicator from "../../components/LoadingIndicator/LoadingIndicator";
import api from "../../api";
import "./MovieDetailsPage.css"

const MovieDetailsPage = () => {
  const [movieData, setMovieData] = useState({});
  const [loading, setLoading] = useState(true);
  const { id } = useParams();

  useEffect(() => {
    api
      .get(`/api/movie/${id}/`)
      .then((res) => res.data)
      .then((data) => {
        setMovieData(data);
        setLoading(false);
      })
      .catch((err) => console.error(err));
  }, []);

  return (
    <PageContainer>
      {loading ? (
        <LoadingIndicator />
      ) : (
        <div>
          <img
            src={`https://image.tmdb.org/t/p/original/${movieData.backdrop_path}`}
            alt={movieData.title}
            className={"movie-banner"}
          />
          <h1>{movieData.title}</h1>
        </div>
      )}
    </PageContainer>
  );
};

export default MovieDetailsPage;
