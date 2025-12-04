import { useEffect, useState } from "react";
import api from "../../api";
import "./Recommendations.css";
import PageContainer from "../../components/PageContainer/PageContainer";
import MovieList from "../../components/MovieList/MovieList";

const Recommendations = () => {
  const [descriptionInput, setDescriptionInput] = useState("");
  const [movieRecommendations, setMovieRecommendations] = useState([]);
  const [movieChoices, setMovieChoices] = useState([]);
  const [selectedMovieIds, setSelectedMovieIds] = useState([]);

  const handleDescriptionRec = (e) => {
    e.preventDefault();
    console.log(`/api/recommendations/by-description/?description=${descriptionInput}`);
    api
      .get(`/api/recommendations/by-description/?description=${descriptionInput}`)
      .then((res) => res.data)
      .then((data) => {
        setMovieRecommendations(data);
      })
      .catch((err) => console.error(err));
  };

    const handleIdRec = (e) => {
    e.preventDefault();
    const ids_string = selectedMovieIds.join(",")
    console.log(`/api/recommendations/by-id/?movie_ids=${ids_string}`);
    api
      .get(`/api/recommendations/by-id/?movie_ids=${ids_string}`)
      .then((res) => res.data)
      .then((data) => {
        setMovieRecommendations(data);
      })
      .catch((err) => console.error(err));
  };

    const handleHybridRec = (e) => {
    e.preventDefault();
    const ids_string = selectedMovieIds.join(",")
    console.log(`/api/recommendations/hybrid/?movie_ids=${ids_string}&description=${descriptionInput}`);
    api
      .get(`/api/recommendations/hybrid/?movie_ids=${ids_string}&description=${descriptionInput}`)
      .then((res) => res.data)
      .then((data) => {
        setMovieRecommendations(data);
      })
      .catch((err) => console.error(err));
  };

  const addSelectedMovie = (clicked_movie_id)=>{
      setSelectedMovieIds((prevMovieIds)=>{
        return [...prevMovieIds, clicked_movie_id]
      })
  }

  const removeSelectedMovie = (clicked_movie_id)=>{
    setSelectedMovieIds((prevMovies)=>{
      return prevMovies.filter((movie_id)=>movie_id != clicked_movie_id)
    })
  }

console.log(selectedMovieIds)

  useEffect(() => {
    api
      .get(`/api/movies/`)
      .then((res) => res.data)
      .then((data) => {
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
          // onSubmit={handleDescriptionRec}
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
          <button onClick={handleDescriptionRec} className={"rec-btn"}>Text</button>
          <button onClick={handleIdRec} className={"rec-btn"}>Id</button>
          <button onClick={handleHybridRec} className={"rec-btn"}>Hybrid</button>
        </form>

        <br />
        <MovieList movies={movieRecommendations} cardType={"link"}/>
        <br />
        <br />
        <br />
        <h2>
          Option 2: Select 5 movies you like and we'll pick similar ones
        </h2>
        <br />
        <br />
        <MovieList movies={movieChoices} cardType={"selectable"} addToSelection={addSelectedMovie} removeFromSelection={removeSelectedMovie}/>
      </div>
    </PageContainer>
  );
};

export default Recommendations;
