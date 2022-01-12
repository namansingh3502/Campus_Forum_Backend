import React from "react";

export default function ChannelTags(props) {
  const Channels = props.channel_list;

  return (
    <div className="m-2 flex flex-wrap">
      {Channels.map((channel) => {
        return (
          <p
            className="bg-gray-400 bg-opacity-40 text-sm rounded-full px-2 m-1 text-black"
            key={channel.id}
          >
            {channel.name}
          </p>
        );
      })}
    </div>
  );
}
