import React, { Component } from "react";
import axios from "axios";


export default class Posts extends Component{
  constructor(props) {
    super(props);
    this.state = {
      LikeLoadStatus:'NotLoaded',
      LikeData:[],
    }
  }

  loadLikes() {
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
          const data = response.data
          for(let i = 0; i < data.length; i++ ){
            if(parseInt(current_user) === data[i].user_id){
              this.props.handleLike()
            }
          }
          this.setState({
            LikeData: data,
            LikeLoadStatus: 'Loaded',
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
    const liked = this.props.Liked;
    const likedList = this.state.LikeData

    return(
      <div className="text-sm ml-2">
        <p>
          { liked ? 'You' : null }
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