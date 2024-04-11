import datetime
import sys

from nbt import nbt

import util

version = "1.0"


def start():
    # Check if exists, otherwise notify and stop
    if not util.track_file_exists():
        print("Create track file is missing. Please put it into the 'input' folder.")
        sys.exit(0)

    print("Running Create Train Fix " + version + " by JX_Snack")

    print("Loading file...")
    # Start loading thread for loading animation
    util.start_loading_thread()
    # Load file
    trackfile = nbt.NBTFile(util.path_to_file(), 'rb')
    util.Storage.loading_finished = True  # Stop loading

    print("\nLoading dimensions...")
    dimension_palette = []
    for dimension in trackfile["data"]["DimensionPalette"]:
        dimension_palette.append(dimension["Id"].value)

    print("\nCommands:")
    print("- trains")
    print("Dumps all trains")
    print("- graphs")
    print("Dumps all graphs")
    print("- dim <dimension id>")
    print("Dumps all graphs with a specific dimension")
    print("- dimtrain <dimension id>")
    print("Dumps all trains within a specific dimension")

    while True:
        action = input("> ")
        action = action.lower()

        if action == "trains":
            print("Getting all trains...")
            trains = 0
            dt1 = datetime.datetime.now()
            for train in trackfile["data"]["Trains"]:
                print(f"Train {train['Name']}")
                trains += 1

            dt2 = datetime.datetime.now()
            print(f"\n{trains} total trains. Took {(dt2 - dt1).seconds} second(s)")

        elif action == "graphs":
            print("Getting all graphs...")
            graphs = 0
            dt1 = datetime.datetime.now()
            for graph in trackfile["data"]["RailGraphs"]:
                try:
                    n0 = graph["Nodes"][0]["Location"]
                    loc0 = f"({dimension_palette[n0['D'].value]}, {n0['X']}, {n0['Y']}, {n0['Z']})"
                except IndexError:
                    n0 = "[Unknown]"
                    loc0 = "[Unknown]"

                try:
                    n1 = graph["Nodes"][1]["Location"]
                    loc1 = f"({dimension_palette[n1['D'].value]}, {n1['X']}, {n1['Y']}, {n1['Z']})"
                except IndexError:
                    n1 = "[Unknown]"
                    loc1 = "[Unknown]"

                print(f"Found graph \n\t{loc0} \n\t{loc1}")
                graphs += 1

            dt2 = datetime.datetime.now()
            print(f"\n{graphs} total graphs. Took {(dt2 - dt1).seconds} second(s)")

        elif action.startswith("dim "):
            args = action.split()
            if len(args) != 2:
                print("Invalid arguments")
                continue

            dim = args[1]
            if dim not in dimension_palette:
                print(f"Invalid dimension! Dimensions can only be: {', '.join(dimension_palette)}")
                continue

            dim_nbr = dimension_palette.index(dim)
            print("Getting all graphs...")
            for g in get_graphs_in_dimension(dim_nbr, dimension_palette, trackfile):
                print(f"Found correct graph\n\t{g[0]}\n\t{g[1]}\n\t{g[2]}")

        elif action.startswith("dimtrain "):
            args = action.split()
            if len(args) != 2:
                print("Invalid arguments")
                continue

            dim = args[1]
            if dim not in dimension_palette:
                print(f"Invalid dimension! Dimensions can only be: {', '.join(dimension_palette)}")
                continue

            dim_nbr = dimension_palette.index(dim)
            graphs = get_graphs_in_dimension(dim_nbr, dimension_palette, trackfile)
            correct_graphs = []
            for graph in graphs:
                correct_graphs.append(graph[2])

            trains = 0
            missing_graph_trains = []
            dt1 = datetime.datetime.now()
            for train in trackfile["data"]["Trains"]:
                try:
                    train_graph = train['Graph']
                except KeyError:
                    missing_graph_trains.append(train)
                    continue

                train_graph_id = to_str_graph(train_graph)
                if train_graph_id not in correct_graphs:
                    continue

                print(f"Train {train['Name']}")
                trains += 1

            dt2 = datetime.datetime.now()

            print("\n")
            for train in missing_graph_trains:
                print(f"\033[91mTrain {train['Name']} is missing a graph.\033[0m")

            print(f"\n{trains} total trains. Took {(dt2 - dt1).seconds} second(s)")

        else:
            print("Unknown command")


def get_graphs_in_dimension(dim_nbr: int, dimension_palette: list, trackfile: nbt.NBTFile) -> list:
    graphs = 0
    dt1 = datetime.datetime.now()
    correct_graphs = []
    for graph in trackfile["data"]["RailGraphs"]:
        try:
            n0 = graph["Nodes"][0]["Location"]
            n0_dim = n0['D'].value
            loc0 = f"({dimension_palette[n0['D'].value]}, {n0['X']}, {n0['Y']}, {n0['Z']})"
        except IndexError:
            n0 = "[Unknown]"
            n0_dim = None
            loc0 = "[Unknown]"

        try:
            n1 = graph["Nodes"][1]["Location"]
            n1_dim = n1['D'].value
            loc1 = f"({dimension_palette[n1['D'].value]}, {n1['X']}, {n1['Y']}, {n1['Z']})"
        except IndexError:
            n1 = "[Unknown]"
            n1_dim = None
            loc1 = "[Unknown]"

        graph_id = to_str_graph(graph['Id'])

        c = False
        if n1_dim is not None:
            c = n1_dim == dim_nbr

        if n0_dim is not None and not c:
            c = n0_dim == dim_nbr

        if not c:
            continue

        correct_graphs.append((loc0, loc1, graph_id))

        graphs += 1

    dt2 = datetime.datetime.now()
    print(f"\n{correct_graphs} correct graphs. Took {(dt2 - dt1).seconds} second(s)")
    return correct_graphs


def to_str_graph(graph):
    return str(graph[0]) + str(graph[1]) + str(graph[2]) + str(graph[2])


if __name__ == "__main__":
    try:
        start()
    except KeyboardInterrupt:
        print("Goodbye")
