import React from "react";

const Others = () => {
  const Channels = ['Code of Conduct', 'Privacy Policy', 'Terms of use', 'Some other things']

  return(
    <div className="p-4 bg-gray-400 rounded-lg bg-opacity-10 backdrop-filter backdrop-blur-lg text-lg mt-2" >
      <div className="my-2 text-center text-xl border-b-2 border-gray-500 text-white p-2">Channels</div>
      {Channels.map((item) => <h1 className="pl-4 font-medium text-white my-2 ml-6" key={item}>{item}</h1> )}
    </div>
  )
}

export default Others