import random
# Function for child processes to generate a random integer number between 0-19 and sending that to parent.
def child_process(pipe_end, process_name):
    random_priority = random.randint(0, 19)
    print(f"{process_name}: Generated priority {random_priority}")
    pipe_end.send(random_priority)  # Send the priority to the parent through the pipe
    pipe_end.close()  # Close the pipe after sending