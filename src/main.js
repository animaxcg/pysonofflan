var schema = "testlan"

const TuyAPI = require('tuyapi');
console.log(process.argv);
ip = process.argv[2]
number = process.argv[3]
desiredState = process.argv[4]



// execute touch command synchronously
// to create three text file

console.log(`Current ip: ${ip}`);
const device = new TuyAPI({
  ip: ip,
  key: '489d4795c28c17ce',
  issueGetOnConnect: false});

(async () => {
  await device.find();

  await device.connect();
if (number != "status"){
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
}
  status = JSON.stringify(await device.get(options={"schema": true}));

  console.log(`New status: ${status}.`);

  device.disconnect();
})();