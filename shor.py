import lib.simulation as sim

args = sim.process_command()
if __name__ == "__main__":
    from lib.myAlgo import run_test

    run_test(args)
