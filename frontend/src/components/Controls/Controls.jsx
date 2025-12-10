import { useState, useEffect } from "react";
import "./Controls.css";
import FilterSelectItem from "../FilterSelectItem/FilterSelectItem";
import Search from "../Search/Search";
import SelectedMovieItem from "./SelectedMovieItem/SelectedMovieItem";
import {AnimatePresence} from "motion/react"

const Controls = ({ getMovies, selectedMovieData, removeFromSelection }) => {
  const [sortType, setSortType] = useState("-popularity");
  const [searchQuery, setSearchQuery] = useState("");
  const [genres, setGenres] = useState([
    { name: "Action", selected: false },
    { name: "Adventure", selected: false },
    { name: "Animation", selected: false },
    { name: "Comedy", selected: false },
    { name: "Crime", selected: false },
    { name: "Documentary", selected: false },
    { name: "Drama", selected: false },
    { name: "Family", selected: false },
    { name: "Fantasy", selected: false },
    { name: "History", selected: false },
    { name: "Horror", selected: false },
    { name: "Music", selected: false },
    { name: "Mystery", selected: false },
    { name: "Romance", selected: false },
    { name: "Science Fiction", selected: false },
    { name: "Thriller", selected: false },
    { name: "TV Movie", selected: false },
    { name: "War", selected: false },
    { name: "Western", selected: false },
  ]);
  const [textQuery, setTextQuery] = useState("");
  const [filterFavorites, setFilterFavorites] = useState(false)

  const parseGenreList = ()=>{
    return genres
      .filter((genre) => genre.selected)
      .map((genre) => genre.name)
      .join(",");
  }
  const handleGetMovies = ()=>{
    const selectedGenres = parseGenreList()
    const movieIds = selectedMovieData.map((movie)=>movie.id).join(",")
    getMovies(selectedGenres, sortType, searchQuery, textQuery, movieIds, filterFavorites);
  }

  useEffect(() => {
    handleGetMovies()
  }, [genres, sortType, searchQuery, filterFavorites]);

  const toggleGenre = (name) => {
    setGenres((prevGenres) => {
      const changedId = prevGenres.findIndex((genre) => genre.name === name);
      const newGenres = [...prevGenres];
      newGenres[changedId] = {
        name: name,
        selected: !newGenres[changedId].selected,
      };
      return newGenres;
    });
  };

  const handleGetRecommendations = (e)=>{
    e.preventDefault()
    const movieIds = selectedMovieData.map((movie)=>movie.id)

    if (movieIds.length > 0 || textQuery.length > 0){
      handleGetMovies()
    } else{
      alert("Select movies or make a text query to get recommendations")
    }
  }

  return (
    <form className={"controls"}>
        <Search setSearchQuery={setSearchQuery} />
        <div className={"sort-control"}>
          <label htmlFor="sort">Sort by:</label>
          <select
            name="sort"
            className={"sort"}
            id="sort"
            value={sortType}
            onChange={(e) => {
              e.preventDefault();
              setSortType(e.target.value);
            }}
          >
            <option value="None">None</option>
            <option value="-popularity">Popularity (Highest first)</option>
            <option value="popularity">Popularity (Lowest first)</option>
            <option value="-vote_average">Rating (Highest first)</option>
            <option value="vote_average"> Rating (Lowest first)</option>
            <option value="-release_date">Release date (newest first)</option>
            <option value="release_date">Release date (oldest first)</option>
            <option value="title">Title (A-Z)</option>
            <option value="-title">Title (Z-A)</option>
          </select>
        </div>
        

        <br />
        <br />
        <p>Filter by genre:</p>
        <ul className={"filter-select-list genres"}>
          {genres.map((genre) => {
            return (
              <FilterSelectItem
                name={genre.name}
                key={genre.name}
                selected={genre.selected}
                toggle={toggleGenre}
              />
            );
          })}
        </ul>
        <p>show only favorites</p>
        <input type="checkbox" value={filterFavorites} onChange={()=>{setFilterFavorites((prev)=>!prev)}}/>
        <div className={"divider"}></div>
        <h3>Get Recommendations</h3>
        <textarea className={"text-query"} name="text-query" id="text-query" value={textQuery} onChange={(e)=>{setTextQuery(e.target.value)}} placeholder="Examples: &#10;I want to watch a cozy Christmas movie&#10;Light-hearted comedy set in New York City"></textarea>
        <ul className={"selected-movie-list"}>
          <AnimatePresence>
          {selectedMovieData.map((movie)=>{
            return <SelectedMovieItem key={`selected ${movie.id}`} movieData={movie} removeFromSelection={removeFromSelection}/>
          })}
          </AnimatePresence>
        </ul>
        <button onClick={handleGetRecommendations}>Get Recommendations</button>
      </form>
  );
};

export default Controls;
