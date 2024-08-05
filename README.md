# MHP30 OCR data collector

This repository is made with the intent of using a webcam to read the display data of a MHP30 heat plate. Although its 
original intent is to tune the PID controller of the heat plate, it can be used for any other purpose that requires 
reading the display data of the heat plate.

## Requirements

All the requirements are in the `environment.yml` and in the `requirements.txt` files.

## Usage

To use the program, you need to run the `main.py` file with the parameters as follows:

```bash
python main.py <P> <I> <D> <setpoint>
```
    
Where:
- `P`: Proportional gain of the PID controller.
- `I`: Integral gain of the PID controller.
- `D`: Derivative gain of the PID controller.
- `setpoint`: The desired temperature of the heat plate.

The program will record data to the `experiments` folder with the name `temperature_data_<P>_<I>_<D>_<setpoint>.csv` as
long as the program is running.

The structure of the data is as follows:
```
<P>,<I>,<D>
Timestamp,Temperature,Setpoint
...
...
...
```
where the `...` imply rows of data.