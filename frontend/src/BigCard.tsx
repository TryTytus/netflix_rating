

function BigCard({title, poster_url, rating, vote_count, top, left, mouseLeaveTriggered})
{

    const getFormattedVotes = (vote_count: number): string =>  {
        if (vote_count < 1000)
        {
            return '>1k'
        }

        const numOfThounsends = Math.floor(vote_count / 1000)
        return `${numOfThounsends}k`
    }

    return (
    <>
        <div onMouseLeave={() => mouseLeaveTriggered()} style={{top, left}} className={`w-[250px] left-0 top-0 shrink-0 absolute z-50 -translate-x-1/2 -translate-y-1/2`}>
            <img className={`h-[300px] w-full object-cover`} src={poster_url} />
            <div className="absolute flex items-center gap-1 bottom-0 bg-gray-700 p-1 rounded-tr-md text-gray-400 text-xs opacity-85">
                <svg className="h-3.5 w-3.5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round"><path d="M11.525 2.295a.53.53 0 0 1 .95 0l2.31 4.679a2.123 2.123 0 0 0 1.595 1.16l5.166.756a.53.53 0 0 1 .294.904l-3.736 3.638a2.123 2.123 0 0 0-.611 1.878l.882 5.14a.53.53 0 0 1-.771.56l-4.618-2.428a2.122 2.122 0 0 0-1.973 0L6.396 21.01a.53.53 0 0 1-.77-.56l.881-5.139a2.122 2.122 0 0 0-.611-1.879L2.16 9.795a.53.53 0 0 1 .294-.906l5.165-.755a2.122 2.122 0 0 0 1.597-1.16z"/></svg>
                {Math.floor(rating * 10) / 10}
            </div>
            <div className="absolute flex items-center gap-0.6 bottom-0 right-0 bg-gray-700 p-1 rounded-tl-md text-gray-400 text-xs opacity-85">
                <svg className="h-3.5 w-3.5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round"><path d="M9 19a1 1 0 0 0 1 1h4a1 1 0 0 0 1-1v-6a1 1 0 0 1 1-1h3.293a.707.707 0 0 0 .5-1.207l-7.086-7.086a1 1 0 0 0-1.414 0l-7.086 7.086a.707.707 0 0 0 .5 1.207H8a1 1 0 0 1 1 1z"/></svg>
                {getFormattedVotes(vote_count)}
            </div>
        </div>
    </>)
}


export default BigCard;