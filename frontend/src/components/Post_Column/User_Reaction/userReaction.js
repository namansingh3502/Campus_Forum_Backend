import React, { Component } from "react";
import LikeDetails from "../likeDetails";
import axios from "axios";

export default class UserReaction extends Component{
  constructor(props) {
    super(props);
    this.state = {
      PostLiked: false,
      UserLiked: [],
      UserComments: [],
      PostLikeLoadStatus: 'NotLoaded',
      PostCommentsLoadStatus: 'NotLoaded',
      PostLikeUpdateStatus: 'NotLoaded',
      PostCommentsUpdateStatus: 'NotLoaded',
    }
    this.loadLikes = this.loadLikes.bind(this)
    this.handleLike = this.handleLike.bind(this)
    // this.loadComments = this.loadComments.bind(this)
  }

  handleLike(){
    const post_id = this.props.post;
    //const current_user = localStorage.getItem("user_id");

    axios
      .get(
        `http://localhost:8000/forum/${post_id}/like-post`,
        {
          headers: {
            'Authorization': localStorage.getItem("Token")
          }
      })
      .then( response => {
        if( response.status === 200 ){
          this.setState({
            PostLikeUpdateStatus: 'Loaded',
            PostLiked: !this.state.PostLiked
          })
        }
        else{
          this.setState({
            PostLikeUpdateStatus: 'NotLoaded'
          })
        }
      })
      .catch(error => {
        console.log("check post like update.", error);
      });
  }

  loadLikes() {

    //Gets the list of user who liked the post.
    //If current user has liked the post updates the post like status

    const post_id = this.props.post;
    const current_user = localStorage.getItem("user_id");

    axios
      .get(
        `http://localhost:8000/forum/${post_id}/likes`,
        {
          headers: {
            'Authorization': localStorage.getItem("Token")
          }
      })
      .then( response => {
        if( response.status === 200 ){
          const data = response.data;
          let liked = false

          for(let i = 0; i < data.length; i++ ){
            if(parseInt(current_user) === data[i].user_id){
              liked=true
            }
          }
          this.setState({
            PostLiked: liked,
            UserLiked: data,
            PostLikeLoadStatus: 'Loaded'
          })
        }
        else{
          this.setState({
            LoadStatus: 'NotLoaded'
          })
        }
      })
      .catch(error => {
        console.log("check like detail error", error);
      });
  }

  componentDidMount() {
    this.loadLikes()
  }

  render(){

    if( this.state.PostLikeLoadStatus !== 'Loaded' ){
      return <>hello</>
    }

    return(
      <div>
        <LikeDetails
          Liked={this.state.PostLiked}
          handleLike={()=>this.handleLike()}
          UserLiked={this.state.UserLiked}
        />                                               {/* Likes Count and liked on not */}
        <div className="mt-1 grid grid-cols-3 gap-x-3 justify-center border-t border-gray-600 pt-3 ">
          <button
            className="bg-gray-400 rounded-full bg-opacity-10 h-10"
            onClick={this.handleLike}
          >
            { this.state.PostLiked ? 'Liked' : 'Like'}
          </button>
          <button className="bg-gray-400 rounded-full bg-opacity-10 h-10">Comment</button>
          <button className="bg-gray-400 rounded-full bg-opacity-10 h-10">Share</button>
        </div>
      </div>
    )
  }
}