import {useState, useRef, useCallback, useEffect} from "react";
import "./Search.css"
import searchIcon from "../../assets/img/search.png"

const Search = ({setSearchQuery})=>{
    const timeoutRef = useRef(null);

    const updateQuery = useCallback((e)=>{
        setQuery(e.target.value)
        if(timeoutRef.current){
            clearTimeout(timeoutRef.current)
        }
        timeoutRef.current = setTimeout(()=>{
            setSearchQuery(e.target.value)
        }, 500)
    }, []);

    useEffect(()=>{
        return ()=>{
            if (timeoutRef.current){
                clearTimeout(timeoutRef.current)
            }
        }
    }, [])

    return(
        <div className={"search-control"}>
            <input className={'search-bar'} type="text" default={"Search for movies"} value={query} onChange={updateQuery} placeholder={"Search Movies"}/>
            <img className={'search-icon'} src={searchIcon} alt="search" />
        </div>
    )
}

export default Search