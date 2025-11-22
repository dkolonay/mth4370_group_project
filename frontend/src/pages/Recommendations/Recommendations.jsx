import { useEffect, useState } from "react";
import api from "../../api";
import "./Recommendations.css";
import PageContainer from "../../components/PageContainer/PageContainer";
import MovieList from "../../components/MovieList/MovieList";

const Recommendations = () => {
  const [descriptionInput, setDescriptionInput] = useState("");
  const [movies, setMovies] = useState([]);
  const [movieChoices, setMovieChoices] = useState([]);

  const handleDescriptionRec = (e) => {
    e.preventDefault();
    console.log(`/api/recommendations/?description=${descriptionInput}`);
    api
      .get(`/api/recommendations/?description=${descriptionInput}`)
      .then((res) => res.data)
      .then((data) => {
        console.log(data);
        setMovies(data);
      })
      .catch((err) => console.error(err));
  };

  useEffect(() => {
    api
      .get(`/api/movies/`)
      .then((res) => res.data)
      .then((data) => {
        console.log(data);
        setMovieChoices(data);
      })
      .catch((err) => console.error(err));
  }, []);

  return (
    <PageContainer>
      <div className={"recommendations-container"}>
        <h1>Get Movie Recommendations</h1>
        <br />
        <br />
        <br />

        <form
          className={"description-recommendation-form"}
          id="movie-description-form"
          onSubmit={handleDescriptionRec}
        >
          <h2>Option 1: Describe a movie</h2>
          <textarea
            className={"description-input"}
            name="description-input"
            id="description-input"
            placeholder="Examples: &#10;I want to watch a cozy Christmas movie&#10;Light-hearted comedy set in New York City"
            value={descriptionInput}
            onChange={(e) => {
              setDescriptionInput(e.target.value);
            }}
          ></textarea>
          <button className={"rec-btn"}>Submit</button>
        </form>

        <br />
        <MovieList movies={movies} cardType={"link"}/>
        <br />
        <br />
        <br />
        <h2>
          Option 2: Select 5 movies you like and we'll pick similar ones
        </h2>
        <br />
        <br />
        <MovieList movies={movieChoices} cardType={"selectable"}/>
      </div>
    </PageContainer>
  );
};

export default Recommendations;
