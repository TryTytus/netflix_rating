

import { Fragment, useEffect, useState } from 'react'
import './App.css'
import Section from './Section'

function App() {
  const [genres, setGenres] = useState([])

  useEffect(() => {
    // 'http://127.0.0.1:8000/api/movies/netflix/'
      fetch('http://127.0.0.1:8000/api/genre/')
        .then((response) => response.json())
        .then((genres) => setGenres(genres?.genres))
  }, [])

  return (
    <>
      <Section title='Top by votes' url='/api/movies/netflix_top_by_votes/' />
      <Section title='Top rated with 100k votes' url='/api/movies/netflix_top_100000_votes/' />
      <Section title='Top rated with 1k votes' url='/api/movies/netflix_top_1000_votes/' />


      {genres.map((genre, i) => (
      <Fragment key={i}>
        <Section title={`${genre?.name} top by rating`} url={`/api/movies/netflix_top_genre_by_rating/${genre?.id}/`} />
        <Section title={`${genre?.name} top by vote`} url={`/api/movies/netflix_top_genre_by_votes/${genre?.id}/`} />
      </Fragment>
    ))}

    </>
  )
}

export default App
