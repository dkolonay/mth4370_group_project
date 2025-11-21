import { useState, useEffect } from "react";
import { useSearchParams } from 'react-router-dom';
import api from "../../api";
// import Note from "../components/Note";
import MovieCard from "../../components/MovieCard/MovieCard";
import PageContainer from "../../components/PageContainer/PageContainer";
import Controls from "../../components/Controls/Controls";

import "./Home.css";

/*  https://a.ltrbxd.com/resized/
    film-poster/4/6/4/4/4/0/464440-football-freaks-0-230-0-345-crop
    .jpg
*/

//https://a.ltrbxd.com/resized/film-poster/4/6/4/4/4/0/464440-football-freaks-0-230-0-345-crop.jpg

const Home = () => {
  // const [notes, setNotes] = useState([]);
  // const [content, setContent] = useState("");
  // const [title, setTitle] = useState("");
  const [movies, setMovies] = useState([]);
  const [searchParams, setSearchParams] = useSearchParams()

  useEffect(() => {
    getMovies();
  }, []);

  const getMovies = (queryString = "") => {
    // console.log(`/api/movies/?${searchParams}`)
    api
      .get(`/api/movies/${queryString}`)
      .then((res) => res.data)
      .then((data) => {
        console.log("got movies")
        setMovies(data);
      })
      .catch((err) => console.error(err));
  };

  return (
    <PageContainer>
      <Controls getMovies={getMovies}/>
      <div className={"movie-list"}>
        {movies.map((movie) => {
          return <MovieCard movie_data={movie} key={movie.id}/>;
        })}
      </div>
    </PageContainer>
  );
};

export default Home;


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
