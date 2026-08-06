import { useEffect, useRef, useState, type Ref } from 'react'
import Card from './Card'

function Section({title, url}: {title: string, url:string}) {

  const [movies, setMovies] = useState([])

  const cardsElement: Ref<HTMLElement> = useRef(null);

  const actionTriggered = () => {
    cardsElement.current?.scrollBy({
      left: cardsElement.current?.clientWidth * 0.8,
      behavior: "smooth"
    })
    console.log("dupa")
  }

  useEffect(() => {
    // 'http://127.0.0.1:8000/api/movies/netflix/'
      fetch('http://127.0.0.1:8000' + url)
        .then((response) => response.json())
        .then((movies) => setMovies(movies.results))
  }, [url])

  const pageNumber = useRef(1);
  const isLoading = useRef(false);

  const loadMoreMovies = async () => {
    isLoading.current = true
    const nextPage = pageNumber.current + 1;
    const fullUrl = 'http://127.0.0.1:8000' + url + `?page=${nextPage}`
    const response = await fetch(fullUrl)
    const data = await response.json()
    const newMovies = data.results;
   setMovies( (prevMovies) => [...prevMovies, ...newMovies])
   pageNumber.current = nextPage


    isLoading.current = false
  }
  


  const scrollTriggerElement: Ref<HTMLElement> = useRef(null)

  useEffect(() => {

    if (!cardsElement || !scrollTriggerElement) return;

    const observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting && !isLoading.current)
      {
        loadMoreMovies()
      }
    }, {
      root: cardsElement.current,
      threshold: 0.1
    })

    observer.observe(scrollTriggerElement.current!)

    return () => observer.disconnect()
  
  }, [url])

  // <div>{movie?.title} - {movie?.poster_url} - {movie?.rating} - {movie?.vote_count}</div>

  return (
    <div className='parent select-none'>
        <h1 className='mt-20 ml-20 mb-5 font-extrabold text-2xl'>
            {title}
        </h1>
      <div className='h-[250px] z-50 absolute right-20' onClick={actionTriggered}>
        <div className='arrow child opacity-60 w-0 h-full grid items-center z-50'>
        <svg className='h-20 w-20 relative right-2 lucide lucide-chevron-right-icon lucide-chevron-right' xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round"><path d="m9 18 6-6-6-6"/></svg>
      </div>
      </div>
      <div ref={cardsElement} className='flex overflow-x-scroll gap-5 ml-20 mr-20'>
        {movies.map(movie => (<Card key={movie?.tmdb_id} rating={movie?.rating} vote_count={movie?.vote_count} poster_url={movie?.poster_url}></Card>))}
        <div ref={scrollTriggerElement} id="scroll-sentinel" className="w-10 h-full flex-shrink-0" />
      </div>
    </div>
  )
}

export default Section