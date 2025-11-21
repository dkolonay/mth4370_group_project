import { useState, useEffect } from "react";
import "./Controls.css";
import FilterSelectItem from "../FilterSelectItem/FilterSelectItem";

const Controls = ({ getMovies }) => {
  const [sortType, setSortType] = useState("-popularity");

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

  useEffect(() => {
    let queryString = `?sort_by=${sortType}`;
    const selectedGenreList = genres.filter((genre)=>genre.selected).map((genre)=>genre.name).join(",")

    if (selectedGenreList.length > 0){
      queryString += `&genres=${selectedGenreList}`
    }

    getMovies(queryString);
  }, [genres, sortType]);

  const toggleGenre = (name)=>{
    setGenres((prevGenres)=>{
      const changedId = prevGenres.findIndex((genre)=> genre.name === name);
      const newGenres = [...prevGenres]
      newGenres[changedId] = {name: name, selected: !newGenres[changedId].selected}
      return newGenres;
    })
  }

  return (
    <form className={"controls"}>
      <label htmlFor="sort">Sort by:</label>

      <select
        name="sort"
        id="sort"
        value={sortType}
        onChange={(e) => {
          e.preventDefault();
          setSortType(e.target.value);
        }}
      >
        <option value="-popularity">Popularity (Highest first)</option>
        <option value="popularity">Popularity (Lowest first)</option>
        <option value="-vote_average">Rating (Highest first)</option>
        <option value="vote_average"> Rating (Lowest first)</option>
        <option value="-release_date">Release date (newest first)</option>
        <option value="release_date">Release date (oldest first)</option>
        <option value="title">Title (A-Z)</option>
        <option value="-title">Title (Z-A)</option>
      </select>
      <br />
      <br />
      <p>Filter by genre:</p>
      <ul className={"filter-select-list genres"}>
        {genres.map((genre)=>{
          return <FilterSelectItem name={genre.name} key={genre.name} selected={genre.selected} toggle={toggleGenre}/>
        })}
      </ul>
    </form>
  );
};

export default Controls;
