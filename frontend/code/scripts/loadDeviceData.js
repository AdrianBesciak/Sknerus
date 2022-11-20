//HELPERS

console.log("Updating sensor data...");
const host = "";

let jsonString =
   '{"room.0.radiator.0": {"tags": {"room_type": "room", "room_id": "1", "device_type": "boiler", "device_id": "0"}, "fields": {"state": "on", "value": "169"}, "field_properties": {"state": ["off", "on"], "value": "float"}},"room.0.radiator.3": {"tags": {"room_type": "room", "room_id": "2", "device_type": "window", "device_id": "0"}, "fields": {"state": "open", "value": "open"}, "field_properties": {"state": ["closed", "open"], "value": "float"}}}';

const roomServerIdToUiId = {
  1: "main-room",
  2: "bathroom",
  3: "hallway-plus-kitchen",
};

const uiIdToRoomServer = {
  "main-room": 1,
  bathroom: 2,
  "hallway-plus-kitchen": 3,
};


//FETCH REQUESTS
const getDataAsJson = async () => {
  const urlToFetch = `${host}:5000/uapi/device/get_all`;
  try {
    const response = await fetch(urlToFetch);
    if (response.ok) {
      const jsonResponse = await response.json();
      console.log(jsonResponse);
      return jsonResponse;
    }
  } catch (error) {
    console.log(error);
  }
};

(async function() {
    console.log("We are demanding results");
    jsonString = await getDataAsJson();
    console.log(jsonString);
    console.log("We got the data result");
})();

while(!jsonString){

}


const sendControl = async () => {
  let location = document.getElementById(
    "device-detail-location-input"
  ).innerHTML;
  location = uiIdToRoomServer(location);
  const sensor = document.getElementById("device-detail-name-input").innerHTML;
  const desiredControl = document.getElementById(
    "device-detail-states-selector"
  ).value;
  const endpoint = `${host}:5000/uapi/room.${location}.${sensor}.0/desiredControl`;
  console.log(`Sending control to ${endpoint}`);
  try {
    const response = await fetch(endpoint, { cache: "no-cache" });
    if (response.ok) {
      const jsonResponse = await response.json();
    }
  } catch (error) {
    console.log(error);
  }
};


// UPDATING CONTROL
const sensorsControl = {};
const sensorsReading = {};
const sensorsStatus = {};
const sensorsLocation = {};

const updateSensorsInRoomAsHtmlElems = (room, roomsData) => {
  const roomData = roomsData[room];
  const roomUiId = roomServerIdToUiId[roomData.tags.room_id];
  const deviceType = roomData.tags.device_type;
  const deviceState = roomData.fields.state;
  const deviceReading = roomData.fields.value;
  const deviceControl = roomData.field_properties.state;
  const sensorHtmlId = roomUiId + "-" + deviceType;

  sensorsControl[sensorHtmlId] = deviceControl;
  sensorsReading[sensorHtmlId] = deviceReading;
  sensorsStatus[sensorHtmlId] = deviceState;
  sensorsLocation[sensorHtmlId] = roomUiId;

  console.log(sensorHtmlId);
  updateDeviceDetailInfo(sensorHtmlId);

  const sensorHtmlElement = document.getElementById(sensorHtmlId);
  const deviceStatusHtmlElement = sensorHtmlElement
    .querySelector(".device-status")
    .getElementsByTagName("span")[0];
  const deviceReadingHtmlElement = sensorHtmlElement
    .querySelector(".device-reading")
    .getElementsByTagName("span")[0];

  deviceStatusHtmlElement.innerHTML = deviceState;
  deviceReadingHtmlElement.innerHTML = deviceReading;

  if (deviceStatusHtmlElement && deviceReadingHtmlElement) {
    console.log("Data was succesfuly updated");
  } else {
    console.log("Failure duruing data update");
  }
};


//SELECTOR MANAGMENT
const clearDropDownList = (select) => {
  var i,
    L = select.options.length - 1;
  for (i = L; i >= 0; i--) {
    select.remove(i);
  }
};
const updateControlDropDownList = (controls) => {
  const select = document.getElementById("device-detail-states-selector");
  clearDropDownList(select);
  for (const control of controls) {
    let option = document.createElement("option");
    option.value = control;
    option.text = control;
    select.appendChild(option);
  }
  if (select) {
    console.log("INF >> Sensor's control dropdown list was updated");
  } else {
    console.log("ERR >> FAILURE DURING CONTROL DROPDOWN LIST UPDATE");
  }
};

const updateDeviceDetailInfo = (sensorHtmlId) => {
  console.log("Updating sensor's detail view .....");
  const sensorNameInputField = document.getElementById(
    "device-detail-name-input"
  );
  sensorNameInputField.innerHTML = sensorHtmlId.split("-").at(-1);

  const stateInputField = document.getElementById(
    "device-detail-current-state-input"
  );
  stateInputField.innerHTML = sensorsStatus[sensorHtmlId];

  const readingInputField = document.getElementById(
    "device-detail-reading-input"
  );
  readingInputField.innerHTML = sensorsReading[sensorHtmlId];

  const locationInputField = document.getElementById(
    "device-detail-location-input"
  );
  locationInputField.innerHTML = sensorsLocation[sensorHtmlId];

  updateControlDropDownList(sensorsControl[sensorHtmlId]);

  if (
    sensorNameInputField &&
    stateInputField &&
    readingInputField &&
    locationInputField
  ) {
    console.log("Updating sensor's detail view was succesfuly");
  } else {
    console.log("ERR >>> CODE FAILED TO UPDATE SENSOR'S DETAIL VIEW");
  }
};

const jsObjSensorsData = JSON.parse(jsonString);
const roomsInServer = Object.keys(jsObjSensorsData);
roomsInServer.forEach((room) =>
  updateSensorsInRoomAsHtmlElems(room, jsObjSensorsData)
);

// Listeners

const updateSensorDetailInfoCallback = (event) => {
  console.log(`INF >> ${event.currentTarget.id} sensor updates detail view`);
  updateDeviceDetailInfo(event.currentTarget.id);
};

document.querySelectorAll(".device-tile").forEach((device) => {
  device.addEventListener("click", updateSensorDetailInfoCallback);
});

const controlSendingBtn = document.getElementById("update-device-state-btn");
controlSendingBtn.onclick = sendControl;
