## Background

The folder weather-plugin contains a COSMOS V5 plugin directory that includes telemetry definition for demonstration goddard weather.
The data included is long/lat, temperature, and timestamp.
goddard_weather_instrument.py script creates a thread to generate simulated telemetry to an interface defined in the plugin.txt. 
Additionally, it creates a thread to listen for the TO_ENABLE command and responds with the validity of that command.

### PLUGIN
When uploading the plugin you will need to provide the machine's IP address that both COSMOS and the script are running on. 

### Python Script
When starting the python script it will ask for the machine's IP address that both COSMOS and the script are running on.