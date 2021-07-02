#include <hackrf.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include <signal.h>
#include<sys/time.h>

static unsigned int g_freq = 77300000;
static int g_sample = 2000000;
static int g_txga = 48;
static char g_data = 127;
static hackrf_device* device;

int hf_show(void){
    printf("%s\r\n", hackrf_library_version());
    printf("%s\r\n", hackrf_library_release());

    return 0;
}

int hf_open(hackrf_device** device){
    char version[255 + 1];
    hackrf_device_list_t *list = hackrf_device_list();
    printf("count=%d\r\n", list->devicecount);
    hackrf_device_list_open(list, 0, device);
    hackrf_version_string_read(*device, &version[0], 255);
    hackrf_device_list_free(list);
    printf("version:%s\r\n", version);
    return 0;
}

int hf_close(hackrf_device* device){
    hackrf_close(device);
    return 0;
}

int hf_rx_callback(hackrf_transfer* transfer) {
    printf("[rx]%d %d %d\r\n", transfer->valid_length, transfer->buffer[0], transfer->buffer[1]);
    return 0;
}

int hf_rx(hackrf_device* device){
    hackrf_set_freq(device, 20000);
    hackrf_start_rx(device, hf_rx_callback, NULL);
    sleep(10);
    hackrf_stop_rx(device);

    return 0;
}

int hf_tx_callback(hackrf_transfer* transfer) {
    int i;    
    for (i = 0; i < transfer->valid_length; i+=2){
        transfer->buffer[i] = g_data;
        transfer->buffer[i+1] = g_data;
    }
    return 0;
}

int hf_tx(hackrf_device* device){
    hackrf_set_txvga_gain(device, g_txga);
    hackrf_set_sample_rate(device, g_sample);
    hackrf_set_freq(device, g_freq*1000);
    hackrf_start_tx(device, hf_tx_callback, NULL);
    while(1){
	    sleep(1);
    }
    hackrf_stop_tx(device);

    return 0;
}

void process_exit(int sig)
{
    hackrf_stop_tx(device);
    hf_close(device);
    printf("hackrf_exit:%d\r\n", hackrf_exit());
    exit(0);
}

int main(int argc, char **argv){
    int ret;
    
    signal(SIGPIPE, SIG_IGN);
    signal(SIGHUP, SIG_IGN);
    signal(SIGINT, process_exit);
    signal(SIGQUIT, SIG_IGN);

    if (argc == 3){
        g_freq = strtoul(argv[1], NULL, 10);
        g_data = strtoul(argv[2], NULL, 10);
    }
    printf("set freq = %dk, A = %d\r\n", g_freq, g_data);
    printf("hackrf_init:%d\r\n", hackrf_init());
    hf_open(&device);
    hf_tx(device);
    hf_close(device);
    printf("hackrf_exit:%d\r\n", hackrf_exit());

    return 0;
}

