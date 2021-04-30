# PA1: Stop-and-wait (S&W) Protocol 
To differentiate the different types of packets (i.e., ACK_0, ACK_1, DATA_0, DATA_1), we are using the 2 most significant bits in the dest port of the UDP header. As such, you must keep port numbers below 16383. To run the `gnc` command with stop-and-wait enabled, use:
``` 
gnc -u -l -r <port>
gnc -u -r <host> <port>
```   

# File Changes
We enclosed the signifcant changes/additions in each file using the following marker comments:
```
/*** START: MODIFIED CODE FOR PA1 - STOP-AND-WAIT RELIABLE DATA TRANSFER PROTOCOL  ***/
                                 <code>
/*** START: MODIFIED CODE FOR PA1 - STOP-AND-WAIT RELIABLE DATA TRANSFER PROTOCOL  ***/
```
Below we present an overview of the changes made in each file.

## backend/include/udp.h
We added variables and types to store data specific to the stop-and-wait protocol. For example, we created two enums to represent the different stop-and-wait sender (READY_SEND_0, READY_SEND_1, WAITING_ACK_0, WAITING_ACK_1) and receiver states (READY_RECV_0, READY_RECV_1). Each UDP PCB is associated with a sender and receiver state. We also created an enum to represent the different stop-and-wait type flags (ACK_0, ACK_1, DATA_0, DATA_1). Lastly, we added a queue to the PCB which buffers the data coming in from the console while the PCB is in waiting state.

## backend/src/grouter/cli.c
* **Modified `gncCmd`**: we made changes to recongize the `-r` flag. If this flag is used, we initialize all of the S&W-specific variables in the UDP PCB (see above). Also, instead of directly sending data from the console, we simply add it to the PCB's buffer (more in next section).  
* **Added S&W receive callback**: we implemented a new S&W-enabled receive callback (`sw_recv_callback`) which executes specific actions based on the `type` flag of the incoming packet and the PCB's (sender or receiver) state. For example, if a receiver PCB receives a data packet with the correct sequence number (e.g., `type_flag == DATA_0 && receiver_state == READY_RECV_0`), then it will pass the data to the upper layer (i.e., print to the console), send the corresponding ACK, and update its receiver state. Otherwise, it will simply resend the previous ACK and not update it state.

## backend/src/grouter/udp.c
* **S&W Send Thread**: we implemented a `udp_send_rdt` thread which handles sending the data from the buffer by following the S&W protocol. If there is data in the buffer and the PCB is in a valid sender state (`READY_SEND_0 || READY_SEND_1`), then it creates the proper type flag and sends the data. A timer is then activated, resending the packet on timeouts (100ms) until the proper ACK is received. Once the ACK is received, the thread checks if there is any data in the buffer and repeats the process. This thread is started from `gncCmd()` in `cli.c` when the `-r` flag is used. 
* **Flags**: we slightly modified the `udp_sendto_if` and `udp_input` code to add, extract, and erase the type flag to and from the dest port in the UDP header. 
