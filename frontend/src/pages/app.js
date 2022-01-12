import { BrowserRouter } from "react-router-dom";
import React, { StrictMode, Component } from "react";
import { render } from "react-dom";

import MenuColumn from "../components/Menu_Column/menuColumn";
import PostColumn from "../components/Post_Column/postColumn";
import ActivityColumn from "../components/activityColumn";
import Header from "../components/header";
import axios from "axios";

export default class App extends Component {
  constructor(props) {
    super(props);
    this.state = {};
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
    this.loadUserData();
  }

  render() {
    return (
      <div className="min-h-screen">
        <Header />
        <div className="flex w-4/5 mx-auto mt-4 justify-center ">
          <MenuColumn />
          <PostColumn />
          <ActivityColumn />
        </div>
      </div>
    );
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
