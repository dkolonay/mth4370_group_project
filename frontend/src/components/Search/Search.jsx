import {useState, useRef, useCallback, useEffect} from "react";

const Search = ({setSearchQuery})=>{
    const [query, setQuery] = useState("")
    const timeoutRef = useRef(null);

    const handleSubmit = (e)=>{
        e.preventDefault()

        setSearchQuery(query)
    }

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
        <form onSubmit={handleSubmit}>
            <label htmlFor="search">Search</label>
            <input type="text" default={"Search for movies"} value={query} onChange={updateQuery}/>
            <button>Submit</button>
        </form>
    )
}

export default Search