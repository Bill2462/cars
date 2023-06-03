from car.drive import Car

car = Car()

def main():
    # Tu wpisz kod
    pass # usuń tę linię

if __name__ == "__main__":
    try:
        main()
    except Exception as _:
        car.stop()
