import React, { Component } from "react";
import LikeDetails from "./likeDetails";

export default class UserReaction extends Component{
  constructor(props) {
    super(props);
    this.state = {
      Liked:false
    }
    this.handleLike = this.handleLike.bind(this);
  }

  handleLike() {
    this.setState({
      Liked : !(this.state.Liked)
    })
  }


  render(){
    return(
      <>
        <LikeDetails
          Liked={this.state.Liked}
          handleLike={()=>this.handleLike()}
          post={this.props.post}
        />                                               {/* Likes Count and liked on not */}
        <div className="mt-1 grid grid-cols-3 gap-x-3 justify-center border-t border-gray-600 pt-3 ">
          <button
            className="bg-gray-400 rounded-full bg-opacity-10 h-10"
            onClick={this.handleLike}
          >
            Like
          </button>
          <button className="bg-gray-400 rounded-full bg-opacity-10 h-10">Comment</button>
          <button className="bg-gray-400 rounded-full bg-opacity-10 h-10">Share</button>
        </div>
      </>
    )
  }
}
