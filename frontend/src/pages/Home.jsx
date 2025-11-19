import { useState, useEffect } from "react";
import api from "../api";
import Note from "../components/Note";
import MovieCard from "../components/MovieCard";

import "../styles/Home.css"

/*  https://a.ltrbxd.com/resized/
    film-poster/4/6/4/4/4/0/464440-football-freaks-0-230-0-345-crop
    .jpg
*/ 

//https://a.ltrbxd.com/resized/film-poster/4/6/4/4/4/0/464440-football-freaks-0-230-0-345-crop.jpg

const Home = () => {
  const [notes, setNotes] = useState([]);
  const [content, setContent] = useState("");
  const [title, setTitle] = useState("");
  const [movies, setMovies] = useState([])

  useEffect(() => {
    getNotes();
    getMovies();
  }, []);

  const getMovies = ()=>{
    api.get("/api/movies/")
    .then((res)=>res.data)
    .then((data)=>{
      console.log(data)
      setMovies(data)
    })
    .catch((err)=> console.error(err))
  }

  const getNotes = () => {
    api
      .get("/api/notes/")
      .then((res) => res.data)
      .then((data) => {
        setNotes(data);
        console.log(data);
      })
      .catch((err) => alert(err));
  };

  const deleteNote = (id) => {
    api
      .delete(`/api/notes/delete/${id}/`)
      .then((res) => {
        if (res.status === 204) {
          alert("Note deleted!");
        } else {
          alert("failed to delete");
        }
        getNotes();
      })
      .catch((error) => alert(error));
  };

  const createNote = (e) => {
    e.preventDefault();
    api
      .post("/api/notes/", { content, title })
      .then((res) => {
        if (res.status === 201) {
          alert("note created");
        } else {
          alert("failed to create note");
        }
        getNotes();
      })
      .catch((err) => alert(err));
  };

  return (
    <div>
      <div>
        <h2>Notes</h2>
        {notes.map((note) => {
          return <Note note={note} onDelete={deleteNote} key={note.id}/>;
        })}
      </div>
      <h2>Create a Note</h2>
      <form onSubmit={createNote}>
        <label htmlFor="title">Title:</label>
        <br />
        <input
          type="text"
          id="title"
          name="title"
          required
          onChange={(e) => setTitle(e.target.value)}
          value={title}
        />
        <br />
        <label htmlFor="content">Content:</label>
        <br />
        <textarea
          name="content"
          id="content"
          required
          onChange={(e) => setContent(e.target.value)}
          value={content}
        ></textarea>
        <input type={"submit"} value="Submit"></input>
      </form>
      <div className={"movie-list"}>
{movies.map((movie)=>{
        return <MovieCard movie_data={movie}/>
      })}
      </div>
      
    </div>
  );
};

export default Home;
