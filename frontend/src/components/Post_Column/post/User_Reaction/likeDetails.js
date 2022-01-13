import React from "react";

export default function LikeDetails(props) {
  const liked = props.Liked;
  const likedList = props.UserLiked;

  return (
    <div className="text-sm ml-2">
      <p>
        {liked ? "You " : null}
        {likedList.length === 2 && liked ? "and " : null}
        {likedList.length > 2 && liked ? ", " : null}
        {likedList.length > 1 && liked ? likedList[0].username + " " : null}
        {likedList.length === 1 && !liked ? likedList[0].username + " " : null}
        {likedList.length > 2
          ? " and " + likedList.length - 1 + " other "
          : null}
        {likedList.length > 0 ? "liked the post." : null}
      </p>
    </div>
  );
}
