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

  const getMovies = (queryString = "") => {
    api
      .get(`/api/movies/${queryString}`)
      .then((res) => res.data)
      .then((data) => {
        setMovies(data);
      })
      .catch((err) => console.error(err));
  };

    const handleTextRec = (textQuery) => {
 
    console.log(`/api/recommendations/by-description/?description=${textQuery}`);
    api
      .get(`/api/recommendations/by-description/?description=${textQuery}`)
      .then((res) => res.data)
      .then((data) => {
        setMovies(data);
      })
      .catch((err) => console.error(err));
  };

    const handleIdRec = (movieIds) => {
  
    const ids_string = movieIds.join(",")
    console.log(`/api/recommendations/by-id/?movie_ids=${ids_string}`);
    api
      .get(`/api/recommendations/by-id/?movie_ids=${ids_string}`)
      .then((res) => res.data)
      .then((data) => {
        setMovies(data);
      })
      .catch((err) => console.error(err));
  };

    const handleHybridRec = (movieIds, textQuery) => {

    const ids_string = movieIds.join(",")
    console.log(`/api/recommendations/hybrid/?movie_ids=${ids_string}&description=${textQuery}`);
    api
      .get(`/api/recommendations/hybrid/?movie_ids=${ids_string}&description=${textQuery}`)
      .then((res) => res.data)
      .then((data) => {
        setMovies(data)
      })
      .catch((err) => console.error(err));
  };

  const getRecommendations = (movieIds, textQuery) =>{
    const isIdSearch = movieIds.length > 0;
    const isTextSearch = textQuery.length > 0;
    if (isIdSearch && isTextSearch){
      handleHybridRec(movieIds, textQuery)
    } else if(isIdSearch){
      handleIdRec(movieIds)
    } else if(isTextSearch){
      handleTextRec(textQuery)
    } else {
      alert("Invalid recommendation search")
    }
  }

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
        <MovieList movies={movies} selectedMovies={selectedMovies} cardType={"link"} addToSelection={addToSelection} removeFromSelection={removeFromSelection}/>
        <Controls getMovies={getMovies} selectedMovieData={selectedMovies} removeFromSelection={removeFromSelection} getRecommendations={getRecommendations}/>
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
