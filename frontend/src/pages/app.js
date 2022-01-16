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
    this.state = {
      LoadUserStatus: false,
      LoadChannelStatus: false,
      ChannelList: []
    };
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
              LoadUserStatus: true
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

  loadChannelList() {
    axios
      .get("http://127.0.0.1:8000/forum/channel-list", {
        headers: {
          Authorization: localStorage.getItem("Token"),
        },
      })
      .then((response) => {
        if( response.status === 200) {
          this.setState({
            ChannelList: response.data,
            LoadChannelStatus: true
          })
        } else {
          console.log("some error happened while getting channel list")
        }
      })
      .catch((error) => {
        console.log("check login error", error);
      });
  }

  componentDidMount() {
    this.loadUserData();
    this.loadChannelList();
  }

  render() {

    if( !this.state.LoadUserStatus && !this.state.LoadChannelStatus ){
      return (
        <div>
          Loading
        </div>
      )
    }
    return (
      <div className="min-h-screen">
        <Header />
        <div className="flex w-4/5 mx-auto mt-4 justify-center ">
          <MenuColumn
            ChannelList={this.state.ChannelList}
          />
          <PostColumn
            ChannelList={this.state.ChannelList}
          />
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
