import { useState, useEffect } from "react";
import api from "../../api";
// import Note from "../components/Note";
import MovieList from "../../components/MovieList/MovieList";
import PageContainer from "../../components/PageContainer/PageContainer";
import Controls from "../../components/Controls/Controls";

import "./Home.css";

const Home = () => {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    getMovies();
  }, []);

  const getMovies = (queryString = "") => {
    api
      .get(`/api/movies/${queryString}`)
      .then((res) => res.data)
      .then((data) => {
        setMovies(data);
      })
      .catch((err) => console.error(err));
  };

  return (
    <PageContainer>
      <Controls getMovies={getMovies}/>
      <MovieList movies={movies} cardType={"link"}/>
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
