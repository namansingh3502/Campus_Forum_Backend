import React, { Component } from "react";
import axios from "axios";

export default class Login extends Component{
  constructor(props) {
    super(props);
    this.state = {
      Username: "",
      Password: "",
    }
  }

  login(){
    axios
      .post(`http://127.0.0.1:8000/auth/token/login/`,
        {
          username: this.state.Username,
          password: this.state.Password
        },
        {
          headers: {
            Authorization: localStorage.getItem("Token"),
          }
        }
      )
      .then((response) => {
        if ((response.status === 200)) {
            console.log(response.data)
            localStorage.setItem('Token','Token ' + response.data.auth_token)
          this.props.updateLoginStatus()
        } else {
          console.log(response.status, response.data.msg)
        }
      })
      .catch((error) => {
        console.log("check error at login page. \n",error)
      })
  }

  render() {
    return(
    <div className="font-sans min-h-screen antialiased bg-gray-900 pt-24 pb-5">
      <div className="flex flex-col justify-center sm:w-96 sm:m-auto mx-5 mb-5 space-y-8">
        <h1 className="font-bold text-center text-4xl text-yellow-500">
          Campus<span className="text-blue-500 ml-2">Forum</span>
        </h1>
          <form onSubmit={(e) => {
              e.preventDefault();
              this.login()
            }}
          >
            <div className="flex flex-col bg-white p-10 rounded-lg shadow space-y-10">
              <h1 className="font-bold text-xl text-center">Sign in to your account</h1>
              <div className="flex flex-col space-y-1">
                <input
                  type="text"
                  className="border-2 rounded px-3 py-2 w-full focus:outline-none focus:border-blue-400 focus:shadow"
                  placeholder="Username"
                  value={this.state.Username}
                  onChange={(e => {
                    this.setState({
                      Username: e.target.value
                    })
                  })}
                />
              <div className="flex flex-col space-y-1">
                <input
                  type="password"
                  className="border-2 rounded px-3 py-2 w-full focus:outline-none focus:border-blue-400 focus:shadow"
                  placeholder="Password"
                  value={this.state.Password}
                  onChange={(e => {
                    this.setState({
                      Password: e.target.value
                    })
                  })}
                />
              </div>
              <div className="flex flex-col-reverse sm:flex-row sm:justify-between items-center w-full">
                <button
                  type="submit"
                  className="w-full bg-blue-500 text-white font-bold text-center py-2 rounded focus:outline-none shadow hover:bg-blue-700 transition-colors">
                  Log In
                </button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
    )
  }
}