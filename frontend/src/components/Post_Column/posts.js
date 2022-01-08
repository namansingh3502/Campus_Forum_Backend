import React, { Component } from "react";

import imageplaceholder from "../../images/image-placeholder.jpg"
import { Comment } from "@material-ui/icons";
import axios from "axios";

import UserReaction from "./User_Reaction/userReaction";
import PostText from "./postText";
import UserDetails from "./userDetails";
import ChannelTags from "./channelTags";
import PostImage from "./postImage";

export default class Posts extends Component{
  constructor(props) {
    super(props);
    this.state = {
      PostLoadStatus:'NotLoaded',
      PostData:[]
    }
  }

  loadPost() {
    const Token = localStorage.getItem("Token");

    axios
      .get('http://127.0.0.1:8000/forum/posts',{
          headers: {
            'Authorization': Token
          }
      })
      .then( response => {
        if( response.status === 200 ){
          this.setState({
            PostData: response.data,
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

  componentDidMount(){
    this.loadPost()
  }

  render(){

    const Post = this.state.PostData

    return(
      <>
        {Post.map((item, index) => {
          return(
            <div className="p-4 bg-gray-400 rounded-lg bg-opacity-10 backdrop-filter backdrop-blur-lg text-white h-auto mt-4"
                 key={Post[index].post_id}
            >
              <UserDetails user={Post[index].username} />      {/* User image and user details */}
              <ChannelTags />                                  {/* All channels in which post is shared */}
              <PostText text={Post[index].body}/>              {/* Text in post if present */}
              {/* <PostImage/>  */}                            {/* Image in post if present */}
              <UserReaction
                post={Post[index].post_id}
              />                                                {/* User reaction or like and comment*/}
            </div>
          )}
        )}
      </>
    )
  }

}
