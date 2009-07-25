#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include <serdisplib/serdisp.h>

serdisp_CONN_t* conn_display;
serdisp_t* display;
long fgcolour = SD_COL_BLACK;
long bgcolour = SD_COL_WHITE;


/*
    LDC connection essentials
*/

int connect_lcd() {
    conn_display = SDCONN_open("USB:060C/04EB");
    display = serdisp_init(conn_display, "ALPHACOOL", "");
    return 0;
}

void disconnect() {
    SDCONN_close(conn_display);
}


/*
    Socket server functions
*/
int initialize() {
    int socket_fd, new_socket_fd;
    struct sockaddr_in host_addr, client_addr;
    socklen_t sin_size;
    int recv_length=1, yes=1;
    char buffer[1024];
    
    if (((socket_fd = socket(PF_INET, SOCK_STREAM, 0)) == -1) ||
        (setsockopt(socket_fd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int)) == -1)) return -1;
}

/*
    Adjuvative functions
*/
void draw_bar(serdisp_t* dd, int x, int y, int w, int h, int hor, int type, long colour) {
    int i,j;
        for (j = y; j < y + ((hor)? h : w); j += ((type) ? 2 : 1))
            for (i = x; i < x + ((hor)? w : h); i += ((type) ? 2 : 1))
                serdisp_setcolour(dd, i, j, colour);
}
void draw_digit(serdisp_t* dd, int x, int y, int digit, int segwidth, int thick, long colour) {
    if (digit < 0 || digit > 9) return;
    
    draw_bar(dd, x, y, segwidth, thick, 1, !(digit != 1 && digit != 4), colour);
    draw_bar(dd, x, y + segwidth - thick, segwidth, thick, 1, !(digit != 1 && digit != 7 && digit != 0), colour);
    draw_bar(dd, x, y + 2*(segwidth - thick), segwidth, thick, 1, !(digit != 1 && digit != 4 && digit != 7), colour);

    draw_bar(dd, x, y, segwidth, thick, 0, !(digit == 4 || digit == 5 || digit == 6 || digit == 8 || digit ==  9 || digit == 0), colour);
    draw_bar(dd, x + segwidth - thick, y,  segwidth, thick, 0, !(digit != 5 && digit != 6), colour);
    draw_bar(dd, x, y + segwidth - thick, segwidth, thick, 0, !(digit == 2 || digit == 6 || digit == 8 || digit == 0), colour);
    draw_bar(dd, x + segwidth - thick, y + segwidth - thick,  segwidth, thick, 0, !(digit != 2), colour);
}

/*
    Main function
*/

int main() {
    printf("Hello, world!\n");
    connect_lcd();
    while (1) {
        
    }
    return 0;
}