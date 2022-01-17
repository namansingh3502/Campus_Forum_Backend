import React, { Component } from "react";
import "../styles.css";
import axios from "axios";

export default class Header extends Component{
  constructor(props) {
    super(props);
  }

  logout(){
    axios
      .post(`http://127.0.0.1:8000/auth/token/logout/`,
        {},
        {
          headers: {
            Authorization: localStorage.getItem("Token"),
          }
        }
      )
      .then((response) => {
        if ((response.status === 204)) {
          localStorage.removeItem('Token')
          this.props.updateLoginStatus()
        } else {
          console.log(response.status, response.data.msg)
        }
      })
      .catch((error) => {
        console.log("check error at login page. \n",error)
      })
  }

  render(){
    return (
      <div className="h-12 sticky top-0 z-10 bg-opacity-60 backdrop-blur-md bg-gray-800 border-b" >
        <div className={"mx-auto w-3/5 text-2xl py-2 px-8"}>
          <div className={"relative float-left text-amber-50 font-semibold"}>
            <h1 className="font-bold text-center text-3xl text-yellow-500">
              Campus<span className="text-blue-500 ml-2">Forum</span>
            </h1>
          </div>
          <div className={"relative float-right"}>
            <button
            className={"text-white text-2xl"}
            onClick={ ()=>{this.logout()}}
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  )}
};