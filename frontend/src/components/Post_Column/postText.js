import React from "react";

const PostText = (data) => {
  const body = data.text
  return(
    <div className="p-2">
      <p className="text-md py-1">
        {body}
      </p>
    </div>
  )
}

export default PostText