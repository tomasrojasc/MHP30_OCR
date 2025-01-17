import cv2
import easyocr
import time
import argparse
import os

threshold = 251
parser = argparse.ArgumentParser(description='PID tunning IronOS')

# Use positional arguments for the PID constants
parser.add_argument('P', type=float, help='P constant')
parser.add_argument('I', type=float, help='I constant')
parser.add_argument('D', type=float, help='D constant')
parser.add_argument('setpoint', type=float, help='setpoint temperature')
args = parser.parse_args()


reader = easyocr.Reader(["en"], gpu=False)
# Initialize video capture
vid = cv2.VideoCapture(1)

# Initialize lists to store temperature and timestamps
temperatures = []
timestamps = []


def find_temp_meas(text_):
    for t in text_:
        bbox, text, score = t
        if (len(text) > 1) and (text != "MHP3O"):
            text = text.replace("S", "5")
            text2parse = text
            break  # Exit the loop after finding the first valid text

    for i in range(1, len(text2parse) + 1):
        try:
            out = float(text2parse[:i])
        except ValueError:
            continue  # If conversion fails, continue to the next iteration
    return out


# the filename will be temperature_data_<P>_<I>_<D>_<setpoint>.csv
folder = os.path.join('experiments', f"{args.P}_{args.I}_{args.D}".replace('.', 'DOT'))

if not os.path.exists(folder):
    os.makedirs(folder)

filename = f'{int(args.setpoint)}.csv'
filename = os.path.join(folder, filename)

# we first start the csv file with the header (we will write line by line)
# the first line has the PID parameters, then the header of the csv file
with open(filename, 'w') as f:
    f.write(f'{args.P},{args.I},{args.D}\n')
    f.write('Timestamp,Temperature,Setpoint\n')

t0 = time.time()


while True:
    ret, frame = vid.read()
    # turn the frame to grayscale if the frame is not None
    if frame is not None:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = (frame > threshold) * 251
        frame = frame.astype('uint8')
        # we need a depth of 1 channel for the OCR to work
        frame = cv2.merge((frame, frame, frame))

    if not ret:
        break

    text_ = reader.readtext(frame)
    try:
        current_temp = find_temp_meas(text_)
        # if the current temp is greater than 360 we skip the current iteration
        if current_temp > 360:
            continue
    except:
        current_temp = None

    if current_temp is not None:
        line = f"{time.time() - t0},{current_temp},{args.setpoint}"
        print("current line: ", line)

    input_ = input("Do you want to start the program? (y/n): ")
    if input_ == 'y':
        break

t0 = time.time()
previous_temp = -100

while True:
    ret, frame = vid.read()
    # turn the frame to grayscale
    if frame is not None:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = (frame > threshold) * 251
        frame = frame.astype('uint8')
        # we need a depth of 1 channel for the OCR to work
        frame = cv2.merge((frame, frame, frame))

    if not ret:
        break

    text_ = reader.readtext(frame)
    try:
        current_temp = find_temp_meas(text_)
        # if previous_temp = -100 we set the previous temp to the current temp
        if previous_temp == -100:
            previous_temp = current_temp
        # if the current temp is greater than 360 we skip the current iteration
        if current_temp > 360:
            continue
        # if the difference between the current temp and the previous temp is greater than 10 we skip the current
        # iteration
        if abs(current_temp - previous_temp) > 5:
            continue
        previous_temp = current_temp
    except:
        current_temp = None

    if current_temp is not None:
        line = f"{time.time() - t0},{current_temp},{args.setpoint}"
        print("writing line: ", line)
        with open(filename, 'a') as f:
            f.write(line + '\n')
