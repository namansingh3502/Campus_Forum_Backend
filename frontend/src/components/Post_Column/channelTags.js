import React from "react";

export default function ChannelTags (props){
  const Channels = props.channel_list;

  return (
    <div className="m-2 text-black flex flex-wrap text-sm">
      {Channels.map((channel) => {
        return(
          <span className="bg-gray-400 opacity-40 rounded-full px-2 m-1" key={channel.id}>{channel.name}</span>
        )}
      )}
    </div>
  )
}