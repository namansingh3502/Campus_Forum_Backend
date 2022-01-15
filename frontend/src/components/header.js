import React from "react";
import "../styles.css";

export default function Header() {

  let user_name = localStorage.getItem('user_name')

  return (
    <div className="h-12 sticky top-0 z-10 bg-opacity-60 backdrop-blur-md bg-gray-800" >
      <div className={"mx-auto w-3/5 text-2xl grid p-3"}>
        <div className={"justify-self-end"}>
          <p className={"text-white"}>
            Hello {user_name}
          </p>
        </div>
        <div>
          <p>
          </p>
        </div>
      </div>
    </div>
  );
};