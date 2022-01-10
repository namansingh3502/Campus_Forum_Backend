import React from "react";

import image from '../../../../images/userimg.jpeg'
import PostCreateModal from "./postCreateModal";

export default function CreatePost() {
  const MediaButton = ['Photo', 'Video', 'News']

  return (
    <div className="p-4 bg-gray-400 rounded-lg bg-opacity-10 backdrop-filter backdrop-blur-lg text-white h-auto" >
      <div className="flex items-center">
        <img
          src={image}
          className="rounded-full bg-black"
          alt={"logo"}
          style={{width:60, height:60}}
        />
        <button className="bg-gray-400 rounded-full bg-opacity-20 w-full text-black ml-4 h-14 px-4 text-left text-white text-lg">
          Start a Post...
        </button>

        <PostCreateModal/>

      </div>
      <div className="grid grid-cols-3 mx-auto w-full justify-items-center mt-4" >
        {MediaButton.map( (item) => {return(
            <div key={item}><button>{item}</button></div>
          )})
        }
      </div>
    </div>
  )
}