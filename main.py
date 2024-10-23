import os
import random
import multiprocessing
from multiprocessing import shared_memory, Pipe

# Function for child processes to generate a random integer number between 0-19 and sending that to parent.
def child_process(pipe_end, process_name):
    random_priority = random.randint(0, 19)
    print(f"{process_name}: Generated priority {random_priority}")
    pipe_end.send(random_priority)  # Send the priority to the parent through the pipe
    pipe_end.close()  # Close the pipe after sending

# Parent process (init).
def parent_process(pipe_ends, shared_mem_name):
    priorities = []
    # Receiving priorities from each child through pipes
    print("Parent: Waiting to receive data from children...")
    for i, pipe_end in enumerate(pipe_ends):
        priority = pipe_end.recv()  # Receive priority from child
        print(f"Parent: Received priority {priority} from child P{i+1}")
        priorities.append(priority)
        pipe_end.close()

    # Attaching to shared memory to write priorities
    print("Parent: Writing data to shared memory...")
    shm = shared_memory.SharedMemory(name=shared_mem_name)
    # The parent process attaches to an existing shared memory segment that
    # was created in the main() function, using the provided shared_mem_name.

    # Writing the priorities to shared memory as bytes
    shm.buf[:len(priorities)] = bytearray(priorities)
    #shm.buf is a buffer interface to the shared memory, and by converting the list of
    #priorities into a bytearray, we can store the data in the memory buffer as raw bytes.
    #The [:len(priorities)] part ensures that the parent writes exactly as many bytes as there are priorities.
    print(f"Parent: Data written to shared memory: {priorities}")
    shm.close()

# Scheduler process reads shared memory, sorts priorities, and prints them
def scheduler_process(shared_mem_name):
    print("Scheduler: Attaching to shared memory...")
    shm = shared_memory.SharedMemory(name=shared_mem_name)
    # Read data from shared memory
    # shm.buf[:4]:The scheduler reads the first 4 bytes from shared memory, 
    # which represent the priorities of the child processes.
    priorities = list(shm.buf[:4]) 
    print(f"Scheduler: Priorities read from shared memory: {priorities}")
    # Sorting the priorities
    sorted_priorities = sorted(priorities)
    print(f"Scheduler: Sorted priorities: {sorted_priorities}")
    shm.close()

# Main function to set up the processes and shared memory
def main():
    print("Main: Creating shared memory segment...")
    shared_mem = shared_memory.SharedMemory(create=True, size=4)

    # Create pipes for communication between parent and child processes using multiprocessing.Pipe()
    pipes = [Pipe() for _ in range(4)]  # the code creates 4 pipes to allow communication between each child process and the parent.
    pipe_parents = [pipe[0] for pipe in pipes]  # The pipe[0] is the parent's end of the pipe (which the parent process will use to receive data)
    pipe_children = [pipe[1] for pipe in pipes]  # The pipe[1] is the child's end (which the child process will use to send data)

    # Forking child processes P1-P4
    print("Main: Forking child processes...") #parent process is about to start forking child processes...
    child_pids = [] 
    # This is an empty list that will store the process IDs (PIDs) of all the child processes.
    # Keeping track of child PIDs is necessary so that the parent can wait for them to
    # finish later using os.waitpid().
    for i in range(4): #This loop will run 4 times, because we want to create 4 child processes (P1 to P4).
        pid = os.fork()
         #This is the key system call that creates a new process.
         #fork() duplicates the current process (parent process).
         #In the parent process, os.fork() returns the child's process ID (a positive number).
         #In the child process, os.fork() returns 0.
        if pid == 0:
            # Child process
            print(f"Child P{i+1}: Forked successfully")
            pipe_parents[i].close()  # Close the parent's end in the child process
            child_process(pipe_children[i], f"P{i+1}")
            os._exit(0)  # Child exits after sending data
        else:
            # Parent process keeps track of child PIDs
            child_pids.append(pid)
            #The parent process stores the child process's PID in the
            #child_pids list. This will be used later so that the parent can wait for the child processes to
            #finish using os.waitpid().
            pipe_children[i].close() 
            # The parent process closes the child's end of the pipe because the parent only
            # needs to receive data (not send it). By closing the unused end, we ensure that
            #each process only has access to the part of the pipe it needs.


    # Parent (init) process handles communication and writes to shared memory
    parent_process(pipe_parents, shared_mem.name)

    # Fork the scheduler process
    print("Main: Forking scheduler process...")
    scheduler_pid = os.fork()
    if scheduler_pid == 0:
        # Scheduler process reads from shared memory
        print("Scheduler: Forked successfully")
        scheduler_process(shared_mem.name)
        os._exit(0)

    # Waiting for all child processes to finish
    print("Main: Waiting for child processes to finish...")
    for pid in child_pids:
        os.waitpid(pid, 0)
    print("Main: Waiting for scheduler process to finish...")
    os.waitpid(scheduler_pid, 0)

    # Cleanup: Detaching and deleting the shared memory
    print("Main: Cleaning up shared memory...")
    shared_mem.unlink()

if __name__ == "__main__":
    main()