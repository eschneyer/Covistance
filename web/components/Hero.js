import React from "react";

import logo from "../assets/logo.svg";
import covistanceLogo from "../assets/covistanceLogo.png"

const Hero = () => (
  <div className="text-center hero my-5">
    <img className="mb-3 app-logo" src={covistanceLogo} alt="React logo" width="120" />
    <h1 className="mb-4">Covistance</h1>

    <p className="lead">
    This is an application that uses the OpenCV API with cutting-edge machine learning technology, artificial intelligence, and facial recognition to maintain social distance between its users.
    </p>
  </div>
);

export default Hero;
