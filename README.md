# cosmos-demo

The purpose of this repository is to provide an easy to test and configure demo of a cosmos plugin in action.

## Background

The folder cosmos-bob was generated using the following command
`cosmos-control.bat cosmos generate plugin BOB`
The version provided here have diverged from that original example to provide additional telemetry examples.

This example and valuable background reading can be found in the [COSMOS 5 Tutorial](https://cosmosc2.com/docs/v5/gettingstarted).
## Installation instructions

### Build and upload your plugin to COSMOS

Take the gem file and go to the Admin page and click the Plugins tab. Clock on "Click to Select Plugin" and select the gem file then click Upload.

If you make any changes to the tlm.txt file you'll need to generate a new gem file and reload it into COSMOS. To do that run the following command

Inside the `cosmos-bob` folder run the following command
`<path>cosmos-control.bat cosmos rake build VERSION=2.0.0`
Fully qualify the path to the `cosmos-control.bat` file to run this. 

If you made any breaking changes, you'll likely need to update 
the `tlm_sender.py` script to send your new telemetry items for testing.

### Opening a port
The script `tlm_sender.py` sends telemetry packets to COSMOS on port 8081. To configure COSMOS to be able these packets you will need to open this port. With COSMOS not running, under the COSMOS folder, open the file `compose.yaml` under the section `cosmos-operator` add the following
```
ports:
 - "8081:8081/udp"
```

## Running the telemetry emulator
The script `tlm_sender.py` will send telemetry packets to COSMOS. To run it simply input the following inside any terminal
`python tlm_sender.py`
