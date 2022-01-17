import { BrowserRouter } from "react-router-dom";
import React, { StrictMode, Component } from "react";
import { render } from "react-dom";
import Login from "./login";
import Forum from "../components/forum";
import axios from "axios";

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      UserLoggedIn: false,
    };
    this.updateLoginStatus = this.updateLoginStatus.bind(this)
  }

  updateLoginStatus(){
    this.setState({
      UserLoggedIn: !this.state.UserLoggedIn
    })
  }

  loadUserData() {
    const Token = localStorage.getItem("Token");
    axios
      .get("http://127.0.0.1:8000/auth/users/me", {
        headers: {
          Authorization: Token,
        },
      })
      .then((response) => {
        if (response.status === 200) {
          this.setState({
            UserLoggedIn: true
          })
          localStorage.setItem("user_id", response.data.id);
          localStorage.setItem("user_name", response.data.username);
        } else {
          console.log(response.status);
          console.log(response.data);
        }
      })
      .catch((error) => {
        console.log("check login error", error);
      });
  }

  componentDidMount() {
    const token = localStorage.getItem('Token')
    if(token){
      this.loadUserData()
    }
  }

  render() {

    if( this.state.UserLoggedIn ){
      return (
        <Forum
          updateLoginStatus={()=>{this.updateLoginStatus()}}
        />
      )
    } else {
      return(
        <Login
          updateLoginStatus={()=>{this.updateLoginStatus()}}
        />
      )
    }
  }
}

render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>,
  document.getElementById("root")
);
