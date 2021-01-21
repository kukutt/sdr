#include <hackrf.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <math.h>
#include<sys/time.h>

//static int g_freq = 1000000;
//static int g_freq = 77300000;
static int g_freq = 88500000;
static int g_sample = 2000000;
static int g_txga = 48;

int hf_echotime(const char *s){
    struct timeval tim;
    gettimeofday(&tim, NULL);
    long nowtim = ((long)tim.tv_sec)*1000+(long)tim.tv_usec/1000;
    printf("[%s]: %ld msn\r\n", s, nowtim);
}

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
    //hf_echotime("start");
#if 0
    int ret = 1;
    ret = fread(transfer->buffer, transfer->valid_length, 1, iqfile);
    if (ret == 0){
	    printf("set\r\n");
	    fseek(iqfile, 0L, SEEK_SET);
    }
#endif
#if 0
    int i;    
    for (i = 0; i < transfer->valid_length; i+=2){
        transfer->buffer[i] = 127;
        transfer->buffer[i+1] = 127;
    }
#endif

#if 0
    static float phase = 0;
    float deviation;
    float i,q;
    int a;
    
    deviation = (2.0f * M_PI * 75000) / (g_sample);

    for (a = 0; a < transfer->valid_length; a+=2){
        phase += deviation * 0.9f;
        i = cos(phase);
        q = sin(phase);
        transfer->buffer[a] = (uint8_t)((127.0f * i));
        transfer->buffer[a+1] = (uint8_t)((127.0f * q));
    }
    //printf("%02x %02x\r\n", transfer->buffer[0], transfer->buffer[1]);
    while (phase > (float)(2.0f * M_PI))phase -= (float)(2.0f * M_PI);
    while (phase < (float)(-2.0f * M_PI))phase += (float)(2.0f * M_PI);
#endif

#if 1
    static float phase = 0;
    static int newfileflg = 0;
    float deviation;
    float i,q;
    int a;

    if (newfileflg == 0){
	    fseek(iqfile, 138, SEEK_SET);
        newfileflg = 1;
    }
    
    short *music = (short *)malloc(transfer->valid_length * 1);
    if (fread((char *)music, transfer->valid_length, 1, iqfile) == 0){
        hf_echotime("music end");
        newfileflg = 0;
    }
    
    deviation = (2.0f * M_PI * 75000) / (g_sample);
    for (a = 0; a < transfer->valid_length; a+=2){
        phase += deviation * 0.9f * ((float)music[a/2]/32768.0);
        i = cos(phase);
        q = sin(phase);
        transfer->buffer[a] = (uint8_t)((127.0f * i));
        transfer->buffer[a+1] = (uint8_t)((127.0f * q));
    }
    //printf("%02x %02x\r\n", transfer->buffer[0], transfer->buffer[1]);
    while (phase > (float)(2.0f * M_PI))phase -= (float)(2.0f * M_PI);
    while (phase < (float)(-2.0f * M_PI))phase += (float)(2.0f * M_PI);
    free(music);
#endif
    //hf_echotime("  end");
    return 0;
}

int hf_tx(hackrf_device* device){
    iqfile = fopen("hello.iq", "rb");
    hackrf_set_txvga_gain(device, g_txga);
    hackrf_set_sample_rate(device, g_sample);
    hackrf_set_freq(device, g_freq);
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

