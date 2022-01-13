import React, { Component } from "react";
import CreatePost from "./post/Create_Post/createPost";
import Posts from "./posts";

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
      </div>
    );
  }
}
