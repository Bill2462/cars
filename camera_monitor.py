import time
import sys
import argparse
import requests
import select
import matplotlib.pyplot as plt
from PIL import Image

def check_if_enter_pressed():
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        return True
    return False

def get_image_or_panic(address):
    response = requests.get(address, stream=True)

    if response.status_code != 200:
        raise ValueError(f"Invalid response code. Got {response.status_code}!")

    return Image.open(response.raw)

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("topic", type=str,
                        help="Name of the image topic to subscribe to.")

    parser.add_argument("--ip", type=str, default="10.128.168.100",
                        help="IP of the server.")

    parser.add_argument("--port", type=int, default=8000,
                        help="Port")

    parser.add_argument("--endpoint", type=str, default="images",
                        help="Endpoint for images.")

    parser.add_argument("--refresh_rate", type=float, default=2,
                        help="How many requests per second we will make.")

    return parser.parse_args()

def main():
    args = get_args()
    api = f"http://{args.ip}:{args.port}/{args.endpoint}?name={args.topic}"
    period = 1 / args.refresh_rate

    image = get_image_or_panic(api)

    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot()
    im_plot = ax.imshow(image)

    print("Please press enter to exit")

    next_refresh = time.time() + period
    while True:
        if time.time() > next_refresh:
            image = get_image_or_panic(api)
            next_refresh = time.time() + period

        im_plot.set_data(image)
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.01) # To avoid 100% CPU utilization

        if check_if_enter_pressed():
            break

if __name__ == "__main__":
    main()
