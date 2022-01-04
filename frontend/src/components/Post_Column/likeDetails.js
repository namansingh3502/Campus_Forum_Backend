import React, { Component } from "react";
import axios from "axios";


export default class Posts extends Component{
  constructor(props) {
    super(props);
    this.state = {
      LikeLoadStatus:'NotLoaded',
      LikeData:[],
      Liked:true
    }
  }

  loadLikes() {
    const Token = localStorage.getItem("Token");
    const user_id = this.props.user;
    const post_id = this.props.post;

    axios
      .get(`http://127.0.0.1:8000/forum/${post_id}/likes`,{
        headers: {
          'Authorization': Token
        }
      })
      .then( response => {
        if( response.status === 200 ){
          console.log(response.data)
          this.setState({
            LikeData: response.data,
            LoadStatus: 'Loaded'
          })
        }
        else{
          this.setState({
            LoadStatus: 'NotLoaded'
          })
        }
      })
      .catch(error => {
        console.log("check login error", error);
      });
  }

  componentDidMount() {
    this.loadLikes()
  }

  render(){
    const liked = this.state.Liked;
    const likedList = this.state.LikeData;

    return(
      <div className="text-sm ml-2">
        <p> { liked ? 'You' : null }
          { (likedList.length === 1 && liked ) ? ' and ' : null }
          { (likedList.length > 1 && liked ) ? ', ' : null }
          { likedList.length ? likedList[0].username + ' ' : null }
          { (likedList.length > 1 ) ? ' and ' + parseInt(likedList.length-1) + ' other ' : null}
          <span>liked the post.</span>
        </p>
      </div>
    )
  }

}