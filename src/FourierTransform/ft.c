#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <sys/time.h> 
#include <string.h>

typedef double Float64;

typedef struct {
    Float64 r;  /* 实部 */
    Float64 i;  /* 虚部 */
} CPX;

int printcpx(int samplerate, int time, CPX *signal, int start, int end);

int timeuseset(char *name, int flg){
    static struct timeval tpstart;
    struct timeval tpend;
    float timeuse;
    if (flg == 0){ 
        gettimeofday(&tpstart,NULL);
    }else{ 
        gettimeofday(&tpend,NULL); 
        timeuse=1000000*(tpend.tv_sec-tpstart.tv_sec)+ 
        tpend.tv_usec-tpstart.tv_usec; 
        timeuse/=1000000; 
        printf("[%s]Used Time:%f\n", name, timeuse); 
    }
}

#define log2N 3 //log2N=6
/*复数类型*/
typedef struct
{
    float real;
    float img;
}complex;

/*复数加法*/
CPX add(CPX a, CPX b){
    CPX c;
    c.r=a.r+b.r;
    c.i=a.i+b.i;
    return c;
}

/*复数减法*/
CPX sub(CPX a, CPX b)
{
    CPX c;
    c.r=a.r-b.r;
    c.i=a.i-b.i;
    return c;
}

/*复数乘法*/
CPX mul(CPX a, CPX b)
{
    CPX c;
    c.r=a.r*b.r - a.i*b.i;
    c.i=a.r*b.i + a.i*b.r;
    return c;
}

/***码位倒序函数***/
void Reverse(int N, CPX *x)
{
    unsigned int i,j,k;
    unsigned int t;
    CPX temp;//临时交换变量
    for(i=0;i<N;i++)//从第0个序号到第N-1个序号
    {
        k=i;//当前第i个序号
        j=0;//存储倒序后的序号，先初始化为0
        for(t=0;t<log2N;t++)//共移位t次，其中log2N是事先宏定义算好的
        {
            j<<=1;
            j|=(k&1);//j左移一位然后加上k的最低位
            k>>=1;//k右移一位，次低位变为最低位
        }   
        if(j>i)//如果倒序后大于原序数，就将两个存储单元进行交换(判断j>i是为了防止重复交换)
        {
            temp=x[i];
            x[i]=x[j];
            x[j]=temp;
        }
    }
}

void fft(int dir, int framelen, CPX *x){
    unsigned int i,j,k,l; 
    int N = framelen;    
    CPX top,bottom,xW;
    Reverse(N, x); //码位倒序
    
    CPX *WN = (CPX *)calloc(N,sizeof(CPX));
    for(i=0;i<N;i++){
        WN[i].r = cos(2.0*M_PI*(double)i/(double)N);
        WN[i].i = sin(2.0*M_PI*(double)i/(double)N) * (-dir);
    }
    
    for(i=0;i<log2N;i++)   /*共log2N级*/
    { //一级蝶形运算
        l=1<<i;//l等于2的i次方
        for(j=0;j<N;j+=2*l)  /*每L个蝶形是一组，每级有N/2L组*/
        { //一组蝶形运算
            for(k=0;k<l;k++)   /*每组有L个*/
            { //一个蝶形运算
                xW=mul(x[j+k+l],WN[N/(2*l)*k]); //碟间距为l
                top=add(x[j+k],xW); //每组的第k个蝶形
                bottom=sub(x[j+k],xW);
                x[j+k]=top;
                x[j+k+l]=bottom;
                //printf("%d %d\r\n", j+k, j+k+l);
            }
        }
    }
    
    /*返回数据*/
    if(dir==-1){
        for(i=0;i<framelen;i++){
            x[i].r=x[i].r/(double)framelen;
            x[i].i=x[i].i/(double)framelen;
        }
    }
}


void dft(int dir, int framelen, CPX *signal, CPX *dft_s){
    int i,k;
    double arg;
    double cosarg,sinarg;

    for(i=0;i<framelen;i++){
        arg=-dir*2.0*M_PI*(double)i/(double)framelen;
        dft_s[i].r = 0;
        dft_s[i].i = 0;

        for(k=0;k<framelen;k++){
            cosarg=cos(k*arg);
            sinarg=sin(k*arg);
            /* (a+bi)*(c+di)=(ac-bd)+(ad+bc)i */
            dft_s[i].r += (signal[k].r*cosarg-signal[k].i*sinarg);
            dft_s[i].i += (signal[k].r*sinarg+signal[k].i*cosarg);
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

int printcpx(int samplerate, int time, CPX *signal, int start, int end){
    int i;
    int framelen = samplerate * time;
    Float64 t;
    int s = start;
    int e = end;
    if (e == 0) e = framelen;
    for (i = s; i < e; i++){
        printf("[%d]%f %f\r\n", i, signal[i].r, signal[i].i);
    }
    return 0;
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
    int framelen=10000;
    signal=calloc(framelen,sizeof(CPX));  //   原始信号
    make_cos(1000, 10, 10, signal);
    dft_s=calloc(framelen,sizeof(CPX));    //  原始信号的傅里叶变换
    hdft_s=calloc(framelen,sizeof(CPX));  //  希尔伯特变换的离散 傅里叶变换
    hsignal=calloc(framelen,sizeof(CPX)); //  希尔伯特变换后信号
    
    dft(1,framelen,signal, dft_s);  //求原始信号 傅里叶变换
    for(i=0;i<framelen;i++){              //求出希尔伯特变换信号的傅里叶变换
        if(i<=framelen/2){
            hdft_s[i].r=dft_s[i].i;
            hdft_s[i].i=-dft_s[i].r;
        }else{
            hdft_s[i].r=-dft_s[i].i;
            hdft_s[i].i=dft_s[i].r;
        }
    }                                  

    dft(-1,framelen, hdft_s,hsignal);    //利用反傅里叶变换求出希尔伯特变换信号
    save_signal(framelen, signal, "aaa.iq");
    save_signal(framelen, hsignal, "haa.iq");
    free(signal);
    free(dft_s);
    free(hdft_s);
    free(hsignal);
}

int dfttest(int ss){
    CPX *signal, *dft_s;
    int i;
    signal = (CPX *)calloc(ss,sizeof(CPX));
    dft_s = (CPX *)calloc(ss,sizeof(CPX));
    make_cos(ss, 1, 100, signal);
    save_signal(ss, signal, "aaa.iq");
    timeuseset("dft", 0);
    dft(1, ss, signal, dft_s);
    printf("ss=%d\r\n", ss);
    timeuseset("dft", 1);
    printcpx(ss, 1, dft_s, 99, 101);

    return 0;
}
    
CPX x[]={{1,0},{3,0},{2,0},{5,0},{8,0},{4,0},{1,0},{3,0},\
         {2,0},{5,0},{8,0},{4,0},{1,0},{3,0},{2,0},{5,0},};

int dfttest2(void){
    int i;
    CPX dft_s[16];
    CPX src[16];
    memcpy(src, x, sizeof(src));
    timeuseset("dft", 0);
    dft(1, 16, src, dft_s);
    timeuseset("dft", 1);
    printcpx(16, 1, dft_s, 0, 0);
    return 0;
}

int ffttest(void){
    int i;
    CPX src[8];
    memcpy(src, x, sizeof(src));
    printcpx(8, 1, src, 0, 0);
    timeuseset("fft", 0);
    fft(1, 8, src);
    timeuseset("fft", 1);
    timeuseset("ifft", 0);
    fft(-1, 8, src);
    timeuseset("ifft", 1);
    printcpx(8, 1, src, 0, 0);
    return 0;
}

int main(int argc, char **argv){
    printf("dsp start\r\n");
    ffttest();
    //dfttest2();
#if 0
    dfttest(256);
    dfttest(1024);
    dfttest(2048);
    dfttest(4096);
    dfttest(4096+4096);
#endif
    //hilbert();
    return 0;
}
