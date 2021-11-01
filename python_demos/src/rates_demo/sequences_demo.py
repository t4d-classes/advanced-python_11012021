""" sequences demo """

def run_demo() -> None:
    """ run demo """

    colors = ['red', 'green', 'blue']

    points = (1,2, 'home')


    for color in colors:
        print(color)


    counter = 0
    while counter < len(colors):
        print(colors[counter])
        counter = counter + 1


    print("red" in colors)
    print("orange" not in colors)