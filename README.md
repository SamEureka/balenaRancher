# <img src="logo.png" alt="rancher steer" width="60" /> balenaRancher

Use balenaRancher to easily deploy a Raspberry Pi4 based kubernetes cluster with a Rancher server and k3s worker nodes. The deployment is slightly more complex than your typical BalenaCloud deployment... but this is kubernetes, so it's never 'easy'!

## Equipment / Software needed

* 1 or more Raspberry Pi 4s (4/8 GB model for the Rancher server, 1/2/4/8 GB model for worker nodes)
* This [repo](https://github.com/SamEureka/balenaRancher.git) cloned to a directory of your choosing
* [Balena-cli](https://github.com/balena-io/balena-cli/blob/master/README.md) installed

## Install / Config / Deploy

### BalenaCloud setup
This project assumes a fairly advanced level of knowledge about BalenaCloud and the steps to create a new fleet. If this is your first time deploying a project, we recommend familiarizing yourself with BalenaCloud by following the steps in this [Getting started](https://www.balena.io/docs/learn/getting-started/raspberrypi4-64/nodejs/) tutorial and then coming back here to deploy your Rancher server and ranch-hand worker nodes.

1. Create a new fleet in balenaCloud and name it `balenaRancher`.
2. Go to [access-tokens](https://dashboard.balena-cloud.com/preferences/access-tokens) and click on the `Create API key` button to create an API key. Copy this key somewhere safe before moving to the next step. We are going to need the key and it is only displayed once. If you messed up and didn't copy it, make a new one.
3. Click on the name of your fleet (balenaRancher) in the side-bar and then click on `Variables`. We are going to create a Fleet Variable for your API Key 
4. Click the `Add variable` button and create a variable with the name `API_KEY` and paste the `api key` that you copied in step 2, to the value
5. Add a device to your new fleet.

### balenaRancher setup 
_these are the barebones instructions to get you started... better instructions are planned_

#### Rancher Server
***IMPORTANT:*** Make sure that you have your `API_KEY` fleet variable set, before provisioning your server... nothing will work correctly if you don't have the `API_KEY`.
1. Clone this repo `git clone https://github.com/SamEureka/balenaRancher.git`
2. Change to the balenaRancher directory `cd balenaRancher`
3. Push a draft release to your fleet `balena push balenaRancher --release-tag rancher-server --draft` using `--release-tag` will help you identify the correct release to 'pin' and `--draft` will prevent the releases from automatically deploying to your devices.
4. Log into your balenaCloud console and find the device that you want to use as the rancher server. Using these [steps](https://www.balena.io/docs/learn/deploy/release-strategy/release-policy/#pin-device-to-a-release) pin the server device to the release tagged with `rancher-server`
5. Once the rancher server release has deployed and your rancher server is up and running. Open the Rancher UI in a browser using the local ip address. The default login is `admin / b@13n4!`

#### Ranch-Hand worker node setup
1. [Add](https://www.balena.io/docs/learn/getting-started/raspberrypi3/nodejs/#add-your-first-device) another device to your balenaRancher fleet
2. In the balenaRancher repo, change directory to the ranch-hand directory `cd ranch-hand`
3. Use the balena-cli to push a release for your worker-nodes. In this example the fleet is called balenaRancher. `balena push balenaRancher --release-tag ranch-hand --draft` again, it is important to use the `--release-tag` and `--draft` flags to make sure that you can identify the correct release and prevent the ranch-hand release from automatically installing to your server.
4. Log into balenaCloud console and find the device you want to use for your worker node. Pin the device to the release tagged `ranch-hand` ([pinning device to release](https://www.balena.io/docs/learn/deploy/release-strategy/release-policy/#pin-device-to-a-release))
5. When the ranch-hand node is done initiallizing, you should see an additional node in the Rancher server UI.
6. You can additional nodes by provisioning a device and pinning the 'ranch-hand' release to the device. It will automatically join the rancher cluster.

### Note:
<s>When the worker nodes (ranch-hands) reboot, they don't always re-join the cluster correctly. You may have to delete duplicate nodes in the Rancher UI. This isn't a desired behavior and I'm working on fixing it.</s> [Fixed](https://github.com/SamEureka/balenaRancher/pull/5)

### Environment Variables

|Name|Value|
|---|---|
|API_KEY|Generate a key by going to [access-tokens](https://dashboard.balena-cloud.com/preferences/access-tokens) and clicking on the `Create API key` button|
|K3S_TOKEN|output of the command `cat /var/lib/rancher/k3s/server/node-token` executed on the rancher server|
|K3S_URL|Url that the worker node uses to connect to the Rancher server. `https://<rancher server ip>:6443`|
|CATTLE_BOOTSTRAP_PASSWORD|Creates the default password for the `admin` account in the Rancher UI. Default value is `b@13n4!`|
| | |
