import os
from multiprocessing import shared_memory, Pipe
from parent_process import parent_process
from scheduler_process import scheduler_process
from child_process import child_process

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
    #The parent process (init) has already forked the child processes (P1–P4) 
    #and now needs to receive the priorities from these child processes.

    # Fork the scheduler process
    print("Main: Forking scheduler process...")
    scheduler_pid = os.fork()
    if scheduler_pid == 0: #This block of code checks whether we are inside the forked process
        # Scheduler process reads from shared memory
        print("Scheduler: Forked successfully")
        scheduler_process(shared_mem.name)
        os._exit(0)

    # In this code, the parent process waits for each child (P1–P4) to finish one by one before moving forward.
    # It ensures that all child processes complete their tasks before proceeding.
    # After that, the parent waits for the Scheduler process to finish as well, ensuring that everything is
    # done before the program moves on to clean up the shared memory.
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