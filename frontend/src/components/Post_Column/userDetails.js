import userImage from "../../images/userimg.jpeg"
import React from "react";

const UserDetails = (data) => {
  const user = data.user

  return(
    <div className="flex">
      <img src={userImage} className="rounded-full" style={{height:50, width:50}} alt={"user"}/>
      <div className="ml-4">
        <h1 className="text-md">{user}</h1>
        <p className="text-sm">10 hrs</p>
      </div>
    </div>
  )
}

export default UserDetails