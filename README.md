# OSProject: Inter-Process Communication Simulation

This project demonstrates **inter-process communication** (IPC) using **pipes** and **shared memory** to simulate how an operating system manages multiple processes and schedules tasks based on priority.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)

## Project Overview
In this project, the `init` process forks four child processes (P1, P2, P3, P4), each of which generates a random priority between 0 and 19. The priorities are sent back to the `init` process through pipes and `init` writes them into a shared memory segment. The **Scheduler** process then reads the list of priorities from the shared memory, sorts the tasks in ascending order (lower numbers have higher priority), and prints the sorted list.

This project explores the following core operating system concepts:
- Process creation through forking.
- Inter-process communication (IPC) via pipes.
- Shared memory usage and task scheduling.
- Scheduling policy based on task priority (ascending order sorting).

## Features
- **Process Forking**: `init` forks 4 child processes (P1–P4).
- **Priority Generation**: Each child process generates a random priority number between 0 and 19.
- **Pipe Communication**: Child processes communicate their priority back to the `init` process using pipes.
- **Shared Memory**: `init` and the Scheduler communicate using shared memory for task scheduling.
- **Task Scheduling**: The Scheduler sorts the processes based on priority before printing the final sorted list.

## Technologies Used
- **Python**: This project uses Python's `os` and `multiprocessing.shared_memory` libraries to handle forking, pipes, and shared memory.
- **Operating System Concepts**: Includes process creation, inter-process communication (IPC), shared memory management, and scheduling policies.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/rikulauttia/OSProject.git
   cd OSProject

## Usage
Run the project: To see the inter-process communication in action:
```bash
    python main.py
