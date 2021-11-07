import React, { Component} from "react";

export default class ActivityColumn extends Component{
  constructor(props) {
    super(props);
    this.state = {}
  }

  render() {
    return (
      <div className="w-1/5">
        <div
          className="bg-gray-400 rounded-lg bg-opacity-10 backdrop-filter backdrop-blur-lg text-lg p-4"
          style={{height:400}}
        >
          <h1 className="text-center text-xl border-b-2 border-gray-500 text-white pb-2"> Activity </h1>

        </div>
      </div>
    )
  }

}