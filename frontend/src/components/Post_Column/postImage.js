import imagePlaceHolder from "../../images/image-placeholder.jpg";
import React from "react";

const PostImage = () => {
  return(
    <div className="grid grid-cols-2 justify-center gap-x-2">
      <button className={"mx-auto p-1"}>
        <img
          src={imagePlaceHolder}
          alt="placeholder"
        />
      </button>
      <button className={"mx-auto p-1"}>
        <img
          src={imagePlaceHolder}
          alt="placeholder"
        />
      </button>
    </div>
  )
}

export default PostImage