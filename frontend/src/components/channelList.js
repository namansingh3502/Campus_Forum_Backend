import React, { Component, useState } from "react";
import axios from "axios";

export default class ChannelList extends Component{

  constructor(props) {
    super(props);
    this.state = {
      Channels:[],
      LoadStatus:"Not_Loaded"
    }
  }

  laodChannelList(){
    //const Token = localStorage.getItem("Token");

    axios
      .get('http://127.0.0.1:8000/forum/channel-list')
      .then( response => {
        if( response.status === 200 ){
          this.setState({
              Channels: response.data,
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
    this.laodChannelList();
  }

  render() {
    const Channel = this.state.Channels

    if(this.state.LoadStatus === 'Not_Loaded'){
      return (
        <div className="p-4 bg-gray-400 rounded-lg bg-opacity-10 backdrop-filter backdrop-blur-lg text-lg mt-2"
           style={{ height: 400 }}>
        </div>
      )
    }

    return (
      <div className="p-4 bg-gray-400 rounded-lg bg-opacity-10 backdrop-filter backdrop-blur-lg text-lg mt-2"
           style={{ height: 400 }}>
        <h1 className="text-center text-xl border-b-2 border-gray-500 text-white pb-2"> Channels </h1>
        <div className="text-center text-white overflow-hidden" style={{ height: 330 }}>
          {Channel.map((item,index) => <h1 className="pl-4 font-medium text-white my-2" key={index}>{item.channel_name}</h1>)}
        </div>
      </div>
    )
  }
}