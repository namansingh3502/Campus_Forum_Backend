import React from "react";
import { AiOutlineClose } from "react-icons/all";
import userImage from "../../../../images/userimg.jpeg";

export default function PostCreateModal() {
  const username = localStorage.getItem("user_name");
  const user_id = localStorage.getItem("user_id");

  return (
    <div
      className={"fixed inset-0 bg-gray-400 bg-opacity-60 h-full w-full"}
      id={"postCreateModal"}
    >
      <div
        className={
          "h-auto w-3/12 relative top-20 mx-auto border-0 shadow-lg rounded-lg"
        }
        style={{ backgroundColor: "#011627"}}
      >
        <div
          className={
            "bg-gray-400 rounded-lg border-0 bg-opacity-20 backdrop-filter h-full w-full text-amber-50"
          }
        >
          <div className={"divide-y divide-gray-700"}>
            <div className="border-b pl-6 pr-4 py-4 flex justify-between items-center">
              <h3 className="text-2xl font-medium">Create Post</h3>
              <button>
                <AiOutlineClose className="close-modal" />
              </button>
            </div>
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
                  className="resize-none w-full h-32 p-2 bg-transparent focus:outline-0 text-white text-xl"
                  placeholder={"What do you want to talk about?"}
                  style={{ outline: "none" }}
                />
              </div>
              <div className={"mx-auto"}>
                <button className="w-full bg-blue-400 mx-auto text-lg rounded-md p-2">
                  Post
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
