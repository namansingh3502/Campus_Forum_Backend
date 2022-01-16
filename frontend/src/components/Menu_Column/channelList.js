import React, { Component, useState } from "react";
import axios from "axios";

export default function ChannelList(props) {
  const Channel = props.ChannelList;

  if (Channel === []) {
    return (
      <div
        className="p-4 bg-gray-400 rounded-lg bg-opacity-10 backdrop-filter backdrop-blur-lg text-lg mt-2"
        style={{ height: 400 }}
      />
    );
  } else {
    return (
      <div
        className="p-4 bg-gray-400 rounded-lg bg-opacity-10 backdrop-filter backdrop-blur-lg text-lg mt-2"
        style={{ height: 400 }}
      >
        <h1 className="text-center text-xl border-b-2 border-gray-500 text-white pb-2">
          Channels
        </h1>
        <div
          className="text-center text-white overflow-hidden"
          style={{ height: 330 }}
        >
          {Channel.map((item) => (
            <h1 className="pl-4 font-medium text-white my-2" key={item.id}>
              {item.name}
            </h1>
          ))}
        </div>
      </div>
    )
  };
}