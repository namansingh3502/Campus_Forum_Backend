import React, { Component } from "react";

import image from "../images/userimg.jpeg"
import imageplaceholder from "../images/image-placeholder.jpg"
import { Comment } from "@material-ui/icons";
import axios from "axios";

const ChannelTags = () => {
  const Channels = ['#Channel-1','#Channel-2','#Channel-3','#Channel-4','#Channel-5','#Channel-6','#Channel-7']
  return(
    <div className="m-2 text-black flex flex-wrap text-sm">
      {Channels.map((channel) => {
        return(
          <span className="bg-gray-400 opacity-40 rounded-full px-2 m-1" key={channel}>{channel}</span>
        )})}
    </div>
  )
}

const UserDetails = (data) => {
  const user = data.user

  return(
    <div className="flex">
      <img src={image} className="rounded-full" style={{height:50, width:50}} alt={"user image"}/>
      <div className="ml-4">
        <h1 className="text-md">{user}</h1>
        <p className="text-sm">10 hrs</p>
      </div>
    </div>
  )
}

const PostText = (data) => {
  const body = data.text
  return(
    <div className="p-1">
      <p className="text-md py-1">
        {body}
      </p>
    </div>
  )
}

const PostImage = () => {
  return(
    <div className="grid grid-cols-2 justify-center gap-x-2">
      <button className={"mx-auto p-1"}>
        <img
          src={imageplaceholder}
          alt="placeholder"
        />
      </button>
      <button className={"mx-auto p-1"}>
        <img
          src={imageplaceholder}
          alt="placeholder"
        />
      </button>
    </div>
  )
}

const UserReaction = () =>{
  const Reaction = ['Like','Comment','Share']

  return(
    <div className="mt-3 grid grid-cols-3 gap-x-3 justify-center">
      {
        Reaction.map((item) => {
          return(
            <button className="bg-gray-400 rounded-full bg-opacity-10 h-10" key={item}>{item}</button>
          )
        })
      }
    </div>
  )
}

export default class Posts extends Component{
  constructor(props) {
    super(props);
    this.state = {
      PostLoadStatus:'NotLoaded',
      PostData:[],
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
    console.log(Post)

    return(
      <>
        {Post.map((item, index) => {
          console.log(Post[index])

          return(
            <div className="p-4 bg-gray-400 rounded-lg bg-opacity-10 backdrop-filter backdrop-blur-lg text-white h-auto mt-4"
                 key={index}
            >
              <UserDetails user={Post[index].username} />      {/* User image and user details */}
              {/*<ChannelTags />*/}      {/* All channels in which post is shared */}
              <PostText text={Post[index].body}/>         {/* Text in post if present */}
              {/* <PostImage/>  */}      {/* Image in post if present */}
              <UserReaction/>     {/* User reaction or like and comment*/}
            </div>
          )}
        )}
      </>
    )
  }

}
