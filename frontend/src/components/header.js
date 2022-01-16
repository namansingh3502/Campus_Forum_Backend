import React from "react";
import "../styles.css";

export default function Header() {

  let user_name = localStorage.getItem('user_name')

  return (
    <div className="h-12 sticky top-0 z-10 bg-opacity-60 backdrop-blur-md bg-gray-800 border-b" >
      <div className={"mx-auto w-3/5 text-2xl p-2"}>
        <div className={"relative float-left text-amber-50 font-semibold"}>Campus Forum</div>
        <div className={"relative float-right"}>
          <button
            className={"text-white text-xl"}
            onClick={ ()=>{console.log("Clicked logout")}}
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  );
};