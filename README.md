# garden-pi
Automated watering and gardening system using the Raspberry Pi


The design is very simple, targeting small container gardening. Planed support for the following hardware:
* 4 watering/gardening zones
* 4 MCP23017 based GPIO Relays
* 4 Vegetronix VH400 moisture sensors (using an ADS1115 I2C ADC)
* 1 TSL2561 I2C light sensor
* 5 One-wire Dallas temperature sensors
* 1 DS1307 Real Time Clock
* CSV logging of data
* Charting of data using Flask/matplotlib/pandas
* Keep infrastructure simple

Video of a zone being watered is here: https://www.youtube.com/watch?v=Rl8ZuR8gYi8


