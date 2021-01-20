#include <hackrf.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

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

FILE *iqfile;
int hf_tx_callback(hackrf_transfer* transfer) {
    int ret = 1;
    
    //fread(transfer->buffer, transfer->valid_length, 1, iqfile);
    int i;    
    for (i = 0; i < transfer->valid_length; i+=2){
        transfer->buffer[i] = 127;
        transfer->buffer[i+1] = 127;
    }
    if (ret == 0){
	printf("set\r\n");
	fseek(iqfile, 0L, SEEK_SET);
    }
    return 0;
}

int hf_tx(hackrf_device* device){
    iqfile = fopen("hello.iq", "rb");
    hackrf_set_txvga_gain(device, 50);
    hackrf_set_sample_rate(device, 2000000);
    hackrf_set_freq(device, 2000000);
    hackrf_start_tx(device, hf_tx_callback, NULL);
    while(1){
	sleep(1);
    }
    hackrf_stop_tx(device);
    fclose(iqfile);

    return 0;
}

int main(int argc, char **argv){
    int ret;
    hackrf_device* device;
    printf("hackrf_init:%d\r\n", hackrf_init());
    hf_open(&device);
    hf_tx(device);
    hf_close(device);
    printf("hackrf_exit:%d\r\n", hackrf_exit());

    return 0;
}

