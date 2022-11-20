// import React from 'react';
// import ReactDOM from 'react-dom';

const sendDesiredStateBtn = document.getElementById("update-device-state-btn");
let deviceData = {};
const updateDeviceData = async () => {
  document.getElementById("active-state-page-heroes").style.display = "grid";
  document.getElementById("loading-state-page-heroes").style.display = "none";
};

setInterval(updateDeviceData, 1000);
