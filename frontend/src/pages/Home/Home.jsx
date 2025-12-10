import { useState, useEffect } from "react";
import api from "../../api";
// import Note from "../components/Note";
import MovieList from "../../components/MovieList/MovieList";
import PageContainer from "../../components/PageContainer/PageContainer";
import Controls from "../../components/Controls/Controls";
import ContentContainer from "../../components/ContentContainer/ContentContainer";

import "./Home.css";

const Home = () => {
  const [movies, setMovies] = useState([]);
  const [selectedMovies, setSelectedMovies] = useState([]);
  
  useEffect(() => {
    getMovies();
  }, []);

  const getMovies = (genres, sort_by, search, text_query, movie_ids, favorites) => {
    console.log({genres, sort_by, search, text_query, movie_ids})
    if (sort_by === "None"){sort_by = null}
    api
      .get("/api/movies/", {
        params: {
          genres: genres ? genres : null,
          sort_by: sort_by ? sort_by : null,
          search: search ? search : null,
          text_query: text_query ? text_query : null,
          movie_ids: movie_ids ? movie_ids : null,
          favorites: favorites ? "true" : null
        }
      })
      .then((res) => res.data)
      .then((data) => {
        setMovies(data);
      })
      .catch((err) => console.error(err));
  };

  const addToSelection = (clicked_movie_id)=>{
      setSelectedMovies((prevMovies)=>{
        return [...prevMovies, movies.find((movie)=>movie.id == clicked_movie_id)]
      })
  }

  const removeFromSelection = (clicked_movie_id)=>{
    setSelectedMovies((prevMovies)=>{
      return prevMovies.filter((movie)=>movie.id != clicked_movie_id)
    })
  }
  return (
    <PageContainer>
      <ContentContainer>
        <h1 className="home-title">Browse Movies</h1>
        <div className={"home-container"}>
        <MovieList movies={movies} selectedMovies={selectedMovies} cardType={"selector"} addToSelection={addToSelection} removeFromSelection={removeFromSelection}/>
        <Controls getMovies={getMovies} selectedMovieData={selectedMovies} removeFromSelection={removeFromSelection}/>
        </div>
      </ContentContainer>
    </PageContainer>
  );
};

export default Home;

//Demo api calls from practicing Django (use as template later)
// const getNotes = () => {
//   api
//     .get("/api/notes/")
//     .then((res) => res.data)
//     .then((data) => {
//       setNotes(data);
//       console.log(data);
//     })
//     .catch((err) => alert(err));
// };

// const deleteNote = (id) => {
//   api
//     .delete(`/api/notes/delete/${id}/`)
//     .then((res) => {
//       if (res.status === 204) {
//         alert("Note deleted!");
//       } else {
//         alert("failed to delete");
//       }
//       getNotes();
//     })
//     .catch((error) => alert(error));
// };

// const createNote = (e) => {
//   e.preventDefault();
//   api
//     .post("/api/notes/", { content, title })
//     .then((res) => {
//       if (res.status === 201) {
//         alert("note created");
//       } else {
//         alert("failed to create note");
//       }
//       getNotes();
//     })
//     .catch((err) => alert(err));
// };
