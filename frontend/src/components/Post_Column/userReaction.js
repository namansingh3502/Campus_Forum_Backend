import React from "react";

const UserReaction = () =>{
  const Reaction = ['Like','Comment','Share']

  return(
    <div className="mt-1 grid grid-cols-3 gap-x-3 justify-center border-t border-gray-600 pt-3 ">
      {
        Reaction.map((item) => {
          return(
            <button className="bg-gray-400 rounded-full bg-opacity-10 h-10" key={item}>{item}</button>
          )
        })
      }
    </div>
  )
}

export default UserReaction