from multiprocessing import shared_memory
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