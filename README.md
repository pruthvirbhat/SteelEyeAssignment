# SteelEyeAssignment

## Configuration 
In config.ini, below information has to be provided
- xml_source_path : xml source url path
- xml_download_path : relative xml file download path
- csv_path : relative path where csv file can be downloaded.

## Files
- Config.ini : Configuration details can be filled in this file
- LoggerModule.py : This module includes generation of logger file
- CommonModule.py : This module includes all the common module needed for the process
- test_steeleye.py : This module performs unittests
- main.py : Main module which includes complete flow.

## Execution
- command to execute : python run.py config.ini
- command to execute unittest: python -m unittest
