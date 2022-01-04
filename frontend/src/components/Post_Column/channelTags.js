import React from "react";

const ChannelTags = () => {
  const Channels = ['#Channel-1','#Channel-2','#Channel-3','#Channel-4','#Channel-5','#Channel-6','#Channel-7']
  return(
    <div className="m-2 text-black flex flex-wrap text-sm">
      {Channels.map((channel) => {
        return(
          <span className="bg-gray-400 opacity-40 rounded-full px-2 m-1" key={channel}>{channel}</span>
        )})}
    </div>
  )
}
export default ChannelTags