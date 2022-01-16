import React from "react";

export default function LikeDetails(props) {
  const liked = props.Liked;
  const likedList = props.UserLiked;
  const length = props.UserLiked.length
  return (
    <div className="text-sm ml-2">
      <p>
        {
          length === 1 ?
            (liked ? "You" : likedList[0].username) + " "
          :""
        }
        {
          length === 2 ?
            liked ? "You and " + likedList[0].username
            :
            likedList[0].username + " and 1 other"
          :""
        }
        {
          length > 2 ?
            liked ? "You, " + likedList[0].username + " and " + JSON.stringify(length-2) +" other"
            :
            likedList[0].username + " and " + JSON.stringify(length-1) +" other"
          :""
        }
        {
          length > 0 ? " liked the post.":
            ""
        }

      </p>
    </div>
  );
}
