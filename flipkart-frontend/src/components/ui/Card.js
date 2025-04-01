import React from "react";

const Card = ({ title, content }) => (
  <div className="bg-white p-4 rounded shadow-md mb-4">
    <h3 className="text-xl font-semibold">{title}</h3>
    <p>{content}</p>
  </div>
);

export default Card;
