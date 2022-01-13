import React, { useCallback, useEffect, useState } from "react";
import { AiOutlineClose } from "react-icons/all";
import userImage from "../../../../images/userimg.jpeg";
import axios from "axios";

export default function PostCreateModal(props) {
  const [postText, updatePostText] = useState("")
  const [postCreated, updatePostCreated] = useState("")
  const username = localStorage.getItem("user_name");
  const user_id = localStorage.getItem("user_id");

  async function createPost() {
    await axios
      .post(`http://127.0.0.1:8000/forum/new-post`,
        {
          body : postText,
          media_count : 0
        },
        {
          headers: {
            Authorization: localStorage.getItem("Token"),
          }
        }
      )
      .then((response) => {
        if ((response.status === 200)) {
          const data = response.data;
          console.log(data.msg)
          updatePostText("")
          props.updateNewPost()
        } else {
          console.log(response.status, "some error happened while creating post.")
        }
      })
      .catch((error) => {
        console.log("check error at new post ", error)
      })
  }

  const escFunction = useCallback((event) => {
    if(event.keyCode === 27) {
      props.updateNewPost();
      updatePostText("")
    }
  }, []);
  useEffect(() => {
    document.addEventListener("keydown", escFunction, false);
    return () => {
      document.removeEventListener("keydown", escFunction, false);
    };
  }, []);

  return (
    <div
      className="fixed inset-0 bg-gray-400 bg-opacity-60 h-full w-full"
      id={"postCreateModal"}
      style={{
        display: props.ShowModal ? "block" : "none"
      }}
    >
      <div
        className="h-auto w-3/12 relative top-20 mx-auto border-0 shadow-lg rounded-lg "
        style={{ backgroundColor: "#011627"}}
      >
        <div className="bg-gray-400 rounded-lg border-0 bg-opacity-20 backdrop-filter h-full w-full text-amber-50">
          <div className="divide-y divide-gray-700">
            <div className="border-b pl-6 pr-4 py-4 flex justify-between items-center">
              <h3 className="text-2xl font-medium">Create Post</h3>
              <button
                onClick={()=>{
                  updatePostText("")
                  props.updateNewPost()
                }}
              >
                <AiOutlineClose className="close-modal" />
              </button>
            </div>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                createPost();
              }}
            >
              <div className={"p-4"}>
                <div className="flex p-2">
                  <img
                    src={userImage}
                    className="rounded-full"
                    style={{ height: 50, width: 50 }}
                    alt={"user"}
                  />
                  <div className="ml-4 text-bold">
                    <h1 className="text-md font-bold" id={user_id}>
                      {username}
                    </h1>
                  </div>
                </div>
                <div className={"px-2 py-4 text-black"}>
                  <textarea
                    className="resize-none w-full h-52 p-2 bg-transparent focus:outline-0 text-white text-xl"
                    placeholder="What do you want to talk about?"
                    value={postText}
                    onChange={(e)=>updatePostText(e.target.value)}
                  />
                </div>
                <div className={"mx-auto"}>
                  <button
                    className="w-full bg-blue-400 mx-auto text-xl font-semibold rounded-md p-2"
                  >
                    Post
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
