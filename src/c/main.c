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
    printf("[aa]%d %d %d\r\n", transfer->valid_length, transfer->buffer[0], transfer->buffer[1]);
    return 0;
}

int hf_rx(hackrf_device* device){
    printf("hf_rx:0\r\n");
    hackrf_set_freq(device, 20000);
    hackrf_start_rx(device, hf_rx_callback, NULL);
    printf("hf_rx:1\r\n");
    sleep(10);
    hackrf_stop_rx(device);

    return 0;
}

int main(int argc, char **argv){
    int ret;
    hackrf_device* device;
    printf("hackrf_init:%d\r\n", hackrf_init());
    hf_open(&device);
    hf_rx(device);
    hf_close(device);
    printf("hackrf_exit:%d\r\n", hackrf_exit());

    return 0;
}
