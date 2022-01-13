import React, { Component } from "react";
import CreatePost from "./post/Create_Post/createPost";
import Posts from "./posts";
import PostCreateModal from "./post/Create_Post/postCreateModal";

export default class PostColumn extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <div className="mx-3 w-5/12 ">
        <CreatePost />
        <Posts />
        <PostCreateModal />
      </div>
    );
  }
}
