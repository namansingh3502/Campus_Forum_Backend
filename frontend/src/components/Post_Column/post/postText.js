import React from "react";

export default function PostText(data) {
    return (
    <div className="p-2">
      <p
        className="text-md py-1"
        style={{whiteSpace: "pre-line"}}
      >{data.text}</p>
    </div>
  );
}
