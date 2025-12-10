  import api from "../api"
  
  export const likeMovie = (movie_id)=>{
     api
      .post(`/api/user-actions/like/`, {movie_id})
      .then((res) => {
        if (res.status === 201){
          return res.status
        }
      })
      .catch((err) => console.error(err));
  }

  export const removeLikeMovie = (movie_id)=>{
     api
      .delete(`/api/user-actions/like/remove/${movie_id}/`)
      .then((res) => {
        if (res.status === 204){
          return res.status
        }
      })
      .catch((err) => console.error(err));
  }

  export const dislikeMovie = (movie_id)=>{
     api
      .post(`/api/user-actions/dislike/`, {movie_id})
      .then((res) => {
        if (res.status === 201){
          return res.status
        }
      })
      .catch((err) => console.error(err));

  }

  export const removeDislikeMovie = (movie_id)=>{
     api
      .delete(`/api/user-actions/dislike/remove/${movie_id}/`)
      .then((res) => {
        if (res.status === 204){
          return res.status
        }
      })
      .catch((err) => console.error(err));

  }