
function Button({children})
{
    return <>
        <div>
            <button className="bg-gray-800 text-gray-400 border opacity-70 border-gray-600 overflow-hidden rounded-sm px-4 py-2 flex gap-2 items-center">{children}</button>
        </div>
    </>
}

export default Button;