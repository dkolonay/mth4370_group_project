import { useState, useEffect } from "react";
import "./Controls.css";
import FilterSelectItem from "../FilterSelectItem/FilterSelectItem";
import Search from "../Search/Search";
import SelectedMovieItem from "./SelectedMovieItem/SelectedMovieItem";
import { AnimatePresence, motion } from "motion/react";

const Controls = ({ getMovies, selectedMovieData, removeFromSelection }) => {
  const [isOpen, setIsOpen] = useState(false);
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
  const [filterFavorites, setFilterFavorites] = useState(false);

  const clearControls = (e)=>{
    e.preventDefault()
    setSortType("None");
    setSearchQuery("")
    setTextQuery("")
    setFilterFavorites(false)
    selectedMovieData.forEach((movie)=>{
      removeFromSelection(movie.id)
    })
    setGenres((prevGenres)=>{
      return prevGenres.map((genre)=>{return {"name": genre.name, selected: false}})
    })
  }
  console.log(genres)
  const parseGenreList = () => {
    return genres
      .filter((genre) => genre.selected)
      .map((genre) => genre.name)
      .join(",");
  };
  const handleGetMovies = () => {
    const selectedGenres = parseGenreList();
    const movieIds = selectedMovieData.map((movie) => movie.id).join(",");
    getMovies(
      selectedGenres,
      sortType,
      searchQuery,
      textQuery,
      movieIds,
      filterFavorites
    );
  };

  useEffect(() => {
    handleGetMovies();
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

  const handleGetRecommendations = (e) => {
    e.preventDefault();
    const movieIds = selectedMovieData.map((movie) => movie.id);

    if (movieIds.length > 0 || textQuery.length > 0) {
      handleGetMovies();
    } else {
      alert("Select movies or make a text query to get recommendations");
    }
  };

  return (
    <motion.div className={"controls"}>
      <AnimatePresence mode="popLayout">
        <motion.div>
          <button
            className="accordion-title"
            onClick={() => setIsOpen(!isOpen)}
          >
            <span className="accordion-title-text">Filter Controls</span>
            <span className={`accordion-arrow ${isOpen ? "open" : ""}`}>▶</span>
          </button>
          <AnimatePresence initial={false}>
            {isOpen && (
              <motion.div
                key="accordian-content"
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: "auto", opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.3 }}
                style={{ overflow: "hidden" }}
              >
                <div className="accordian-content">
                  <motion.div layout className={"sort-control"} key="accordian-inner" >
                  <Search setSearchQuery={setSearchQuery} />
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
                      <option value="-popularity">
                        Popularity (Highest first)
                      </option>
                      <option value="popularity">
                        Popularity (Lowest first)
                      </option>
                      <option value="-vote_average">
                        Rating (Highest first)
                      </option>
                      <option value="vote_average">
                        {" "}
                        Rating (Lowest first)
                      </option>
                      <option value="-release_date">
                        Release date (newest first)
                      </option>
                      <option value="release_date">
                        Release date (oldest first)
                      </option>
                      <option value="title">Title (A-Z)</option>
                      <option value="-title">Title (Z-A)</option>
                    </select>
                  </motion.div>

                  <p className={"control-left-align"}>Filter by genre:</p>
                  <motion.ul className={"filter-select-list genres"}>
                    {genres.map((genre, i) => {
                      return (
                        <FilterSelectItem
                          name={genre.name}
                          key={`${i},${genre.name}`}
                          selected={genre.selected}
                          toggle={toggleGenre}
                        />
                      );
                    })}
                  </motion.ul>
                  <div className={'fav-flex'}>
                  <p className={"fav-text"} >Show only favorites</p>
                  <input
                    type="checkbox"
                    className={"fav-check"}
                    value={filterFavorites}
                    onClick={() => {
                      setFilterFavorites((prev) => !prev);
                    }}
                  />
                  </div>
                
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>

        <div className={"divider"}></div>
        <h2 className={"control-left-align rec-header"}>Get Recommendations </h2>
                <h3 className={"control-left-align"}>
          Describe the movie you want to watch
        </h3>
        <textarea
          className={"text-query"}
          name="text-query"
          id="text-query"
          value={textQuery}
          onChange={(e) => {
            setTextQuery(e.target.value);
          }}
          placeholder="Examples: &#10;I want to watch a cozy Christmas movie&#10;Light-hearted comedy set in New York City"
        ></textarea>
        <h3 className={"control-left-align"}>
          Select Movies from the list to search for similar ones
        </h3>
        <motion.div layout className={"control-end"}>
          <motion.ul className={"selected-movie-list"} layout>
            <AnimatePresence mode="popLayout">
              {selectedMovieData.map((movie) => {
                return (
                  <SelectedMovieItem
                    key={`selected ${movie.id}`}
                    movieData={movie}
                    removeFromSelection={removeFromSelection}
                  />
                );
              })}
            </AnimatePresence>
          </motion.ul>
          <button className={"rec-submit"} onClick={handleGetRecommendations}>
            Get Recommendations
          </button>
          <button className={"control-clear"} onClick={clearControls}>Start over</button>
        </motion.div>
      </AnimatePresence>
    </motion.div>
  );
};

export default Controls;
