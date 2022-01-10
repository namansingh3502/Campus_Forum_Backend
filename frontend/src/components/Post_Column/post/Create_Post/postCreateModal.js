import React from "react"
import { AiOutlineClose } from "react-icons/all";
import userImage from "../../../../images/userimg.jpeg";

export default function PostCreateModal(){
  const username = localStorage.getItem('user_name')
  const user_id = localStorage.getItem('user_id')

  return(
    <div
      className={"fixed inset-0 bg-black bg-opacity-60 h-full w-full"}
      id={'postCreateModal'}
    >
      <div
        className={"h-2/5 w-1/3 relative top-20 mx-auto border shadow-lg rounded-md  body"}
        style={{backgroundColor:'#011627'}}
      >
        <div className={"bg-gray-400 rounded-lg bg-opacity-10 backdrop-filter backdrop-blur-xl h-full w-full"}>
          <div className={"divide-y divide-gray-700"}>
            <div className="border-b px-4 py-2 flex justify-between items-center font-bold">
              <h3 className="text-2xl">Create Post</h3>
              <button><AiOutlineClose className="close-modal "/></button>
            </div>

            <div className="flex p-5">
              <img src={userImage} className="rounded-full" style={{height:50, width:50}} alt={"user"}/>
              <div className="ml-4 text-bold">
                <h1 className="text-md font-bold" id={user_id}>{username}</h1>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}