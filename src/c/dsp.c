#include <stdio.h>
#include <stdlib.h>
#include <math.h>

typedef double Float64;

typedef struct {
    Float64 r;  /* 实部 */
    Float64 i;  /* 虚部 */
} CPX;


void DFT(int dir, int framelen, CPX *signal, CPX *dft_s){
    int i,k;
    double arg;
    double cosarg,sinarg;

    for(i=0;i<framelen;i++){
        arg=-dir*2.0*3.141592654*(double)i/(double)framelen;

        for(k=0;k<framelen;k++){
            cosarg=cos(k*arg);
            sinarg=sin(k*arg);
            dft_s[i].r+=(signal[k].r*cosarg-signal[k].i*sinarg);
            dft_s[i].i+=(signal[k].r*sinarg+signal[k].i*cosarg);
        }
    }
    /*返回数据*/
    if(dir==-1){
        for(i=0;i<framelen;i++){
            dft_s[i].r=dft_s[i].r/(double)framelen;
            dft_s[i].i=dft_s[i].i/(double)framelen;
        }
    }
}

int make_cos(int samplerate, int time, int fk, CPX *signal){
    int i;
    int framelen = samplerate * time;
    Float64 t;
    for (i = 0; i < framelen; i++){
        t = (Float64)time * ((Float64)i/framelen);
        signal[i].r = cos(2*M_PI*t*fk);
        signal[i].i = 0;
    }
    return 0;
}

int save_signal(int framelen, CPX *signal, const char *filename){
    FILE *fp;
    if( (fp=fopen(filename, "wb+")) == NULL ){  //以二进制方式打开
        printf("Fail to open file!");
        exit(0);
    }
    fwrite(signal, sizeof(CPX), framelen, fp);
    fclose(fp);
}

int hilbert(void){
    CPX *signal;
    CPX *dft_s;
    CPX *hdft_s;
    CPX *hsignal;
    int i;
    int framelen=1920000;
    signal=calloc(framelen,sizeof(CPX));  //   原始信号
    dft_s=calloc(framelen,sizeof(CPX));    //  原始信号的傅里叶变换
    hdft_s=calloc(framelen,sizeof(CPX));  //  希尔伯特变换的离散 傅里叶变换
    hsignal=calloc(framelen,sizeof(CPX)); //  希尔伯特变换后信号
    
    DFT(1,framelen,signal, dft_s);  //求原始信号 傅里叶变换
    for(i=0;i<framelen;i++){              //求出希尔伯特变换信号的傅里叶变换
        if(i<=framelen/2){
            hdft_s[i].r=dft_s[i].i;
            hdft_s[i].i=-dft_s[i].r;
        }else{
            hdft_s[i].r=-dft_s[i].i;
            hdft_s[i].i=dft_s[i].r;
        }
    }                                  

    DFT(-1,framelen, hdft_s,hsignal);    //利用反傅里叶变换求出希尔伯特变换信号
}

int main(int argc, char **argv){
    printf("dsp start\r\n");

    CPX *signal;
    signal = (CPX *)calloc(192000*10,sizeof(CPX));
    make_cos(192000, 10, 1000, signal);
    save_signal(192000*10, signal, "aaa.iq"); 
    //hilbert();
    return 0;
}
