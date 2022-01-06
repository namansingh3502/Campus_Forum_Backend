import React, { Component } from "react";
import LikeDetails from "./likeDetails";
import axios from "axios";

export default class UserReaction extends Component{
  constructor(props) {
    super(props);
    this.state = {
      Liked:false
    }
    this.handleLike = this.handleLike.bind(this);
    this.updateLike = this.updateLike.bind(this);
  }

  handleLike() {
    this.setState({
      Liked : !(this.state.Liked)
    })
  }

  updateLike() {
    axios
      .post(
        `http://127.0.0.1:8000/forum/updateLike`,
        {
            post_id : this.props.post
          },
        {
          headers: {
            'Authorization': localStorage.getItem("Token")
          }
      })
      .then( response => {
        if(response.status === 200 ){
          console.log("updated like status to ", response.data)
          this.handleLike()
        }
        else{
          console.log("Some error happened in updating like status.")
        }
      })
      .catch(error => {
        console.log("check like update error ", error)
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
            onClick={this.updateLike}
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
