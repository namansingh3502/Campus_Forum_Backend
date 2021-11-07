import React from "react";

const ChannelList = () => {
  const Channels = [
      '#Channel-1', '#Channel-2', '#Channel-3', '#Channel-4', '#Channel-5', '#Channel-6',
      '#Channel-7', '#Channel-8', '#Channel-9','#Channel-10'
  ]

  return(
    <div className="p-4 bg-gray-400 rounded-lg bg-opacity-10 backdrop-filter backdrop-blur-lg text-lg mt-2" style={{height:400}} >
      <h1 className="text-center text-xl border-b-2 border-gray-500 text-white pb-2"> Channels </h1>
      <div className="text-center text-white overflow-hidden" style={{height:330}}>
        {Channels.map((item) => <h1 className="pl-4 font-medium text-white my-2" key={item}>{item}</h1> )}
      </div>
    </div>
  )
}

export default ChannelList;