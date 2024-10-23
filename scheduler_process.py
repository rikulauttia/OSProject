from multiprocessing import shared_memory
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