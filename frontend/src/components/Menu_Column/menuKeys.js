import React from "react";

const MenuKeys = () => {
  const Buttons = ["Home", "Video", "Tags", "FAQ", "Contacts"];
  return (
    <div className="p-4 bg-gray-400 rounded-lg bg-opacity-10 backdrop-filter backdrop-blur-lg text-lg">
      {Buttons.map((item) => (
        <h1 className="pl-14 font-medium text-white my-2 " key={item}>
          {item}
        </h1>
      ))}
    </div>
  );
};

export default MenuKeys;
