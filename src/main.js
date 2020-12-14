var schema = "testlan"

const TuyAPI = require('tuyapi');
console.log(process.argv);
number = process.argv[2]
desiredState = process.argv[3]

const device = new TuyAPI({
    ip: "192.168.1.193",
//   id: '34062563a4cf12e5c9ad',
  key: '489d4795c28c17ce',
  issueGetOnConnect: false});

(async () => {
  await device.find();

  await device.connect();

  let statusObj = await device.get(options={"schema": true});
  let statusString = JSON.stringify(statusObj)
  let status = statusObj.dps[number]
  statusObj.dps[number] = (desiredState == "on")
  console.log(`Current status: ${statusString}.`);
  console.log(`Current status: ${JSON.stringify(statusObj)}.`);
  if (status != desiredState) {
  await device.set(
    {multiple: true,
    data: statusObj.dps});
    console.log(`Changed state to: ${desiredState}`);
  }
  else {
    console.log(`No need to change state to: ${desiredState}`);
  }

  status = await device.get();

  console.log(`New status: ${status}.`);

  device.disconnect();
})();