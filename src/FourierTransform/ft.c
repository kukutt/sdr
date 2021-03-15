#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <sys/time.h> 
#include <time.h>
#include <string.h>

typedef float MyFloat;

typedef struct {
    MyFloat r;  /* 实部 */
    MyFloat i;  /* 虚部 */
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
void Reverse(int N, CPX *x, int log2N)
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

void fft(int dir, int framelen, CPX *x, int log2N){
    unsigned int i,j,k,l; 
    int N = framelen;    
    CPX top,bottom,xW;
    Reverse(N, x, log2N); //码位倒序
    
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


void dft(int dir, int framelen, CPX *signal){
    int i,k;
    double arg;
    double cosarg,sinarg;
    CPX *dft_s;

    dft_s = (CPX *)calloc(framelen, sizeof(CPX));

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


    memcpy(signal, dft_s, framelen*sizeof(CPX)); 
    free(dft_s);
}

int printcpx(int samplerate, int time, CPX *signal, int start, int end){
    int i;
    int framelen = samplerate * time;
    MyFloat t;
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
    MyFloat t;
    for (i = 0; i < framelen; i++){
        t = (MyFloat)time * ((MyFloat)i/framelen);
        signal[i].r = cos(2*M_PI*t*fk);
        signal[i].i = 0;
    }
    return 0;
}

int make_rand(int len, CPX *signal){
    int i = 0;
    srand((unsigned)time(NULL));
    for (i = 0; i < len; i++){
        signal[i].r = ((MyFloat)(rand()%100000))/1000.0;
        signal[i].i = ((MyFloat)(rand()%100000))/1000.0;
    }
}

int cmpcpx(int len, CPX *a, CPX *b){
    int ret = 0;
    int i = 0;
    MyFloat diffr,diffi;
    MyFloat jdr=0,jdi=0;

    for (i = 0; i < len; i++){
        diffr = fabs(a[i].r - b[i].r);
        if (fabs(a[i].r) < 1){
            jdr = 0.001;
        }else if (fabs(a[i].r) < 100){
            jdr = 0.1;
        }else {
            jdr = 1;
        }

        if (diffr > jdr){
            printf("r [%d] %f,%f [%f]\r\n", i, a[i].r, b[i].r, jdr);
            ret = -1;
            //break;
        }

        diffi = fabs(a[i].i - b[i].i);
        if (fabs(a[i].i) < 1){
            jdi = 0.001;
        }else if (fabs(a[i].i) < 100){
            jdi = 0.1;
        }else {
            jdi = 1;
        }

        if (diffi > jdi){
            printf("i [%d] %f,%f [%f]\r\n", i, a[i].i, b[i].i, jdi);
            ret = -1;
            //break;
        }
    }
#if 0
    if (ret != 0){
        printf("i = %d\r\n", i);
        printcpx(len, 1, a, 0, 0);
        printcpx(len, 1, b, 0, 0);
    }
#endif

    return ret;
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

int load_signal(int framelen, CPX *signal, const char *filename){
    FILE *fp;
    if( (fp=fopen(filename, "r")) == NULL ){  //以二进制方式打开
        printf("Fail to open file!");
        exit(0);
    }
    fread(signal, sizeof(CPX), framelen, fp);
    fclose(fp);
}
#if 0
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
    
    dft(1,framelen, signal);  //求原始信号 傅里叶变换
    for(i=0;i<framelen;i++){              //求出希尔伯特变换信号的傅里叶变换
        if(i<=framelen/2){
            hdft_s[i].r=signal[i].i;
            hdft_s[i].i=-signal[i].r;
        }else{
            hdft_s[i].r=-signal[i].i;
            hdft_s[i].i=signal[i].r;
        }
    }                                  

    dft(-1,framelen, hdft_s);    //利用反傅里叶变换求出希尔伯特变换信号
    save_signal(framelen, signal, "aaa.iq");
    save_signal(framelen, hsignal, "haa.iq");
    free(signal);
    free(dft_s);
    free(hdft_s);
    free(hsignal);
}
#endif

int dfttest(int ss){
    CPX *signal, *dft_s;
    int i;
    signal = (CPX *)calloc(ss,sizeof(CPX));
    dft_s = (CPX *)calloc(ss,sizeof(CPX));
    make_cos(ss, 1, 100, signal);
    save_signal(ss, signal, "aaa.iq");
    timeuseset("dft", 0);
    dft(1, ss, signal);
    printf("ss=%d\r\n", ss);
    timeuseset("dft", 1);
    printcpx(ss, 1, dft_s, 99, 101);

    return 0;
}
    
CPX x[]={{1,0},{3,0},{2,0},{5,0},{8,0},{4,0},{1,0},{3,0},\
         {2,0},{5,0},{8,0},{4,0},{1,0},{3,0},{2,0},{5,0},};

int dfttest2(void){
    int i;
    CPX dft_s[8];
    CPX src[8];
    memcpy(src, x, sizeof(src));
    printcpx(8, 1, src, 0, 0);
    timeuseset("dft", 0);
    dft(1, 8, src);
    timeuseset("dft", 1);
    printcpx(8, 1, src, 0, 0);
    return 0;
}

int autotest(void){
    int i;
    CPX *src;
    CPX *dstfft;
    CPX *midfft;
    CPX *dstdft;
    CPX *middft;
    int dl = 4096;
    //dl = 8;
    int ret = -1, ret1 = -1, ret2 = -1, ret3 = 0;

    src = (CPX *)calloc(dl,sizeof(CPX));
    dstfft = (CPX *)calloc(dl,sizeof(CPX));
    midfft = (CPX *)calloc(dl,sizeof(CPX));
    dstdft = (CPX *)calloc(dl,sizeof(CPX));
    middft = (CPX *)calloc(dl,sizeof(CPX));
    //make_rand(dl, src);
    load_signal(dl, src, "src.bin");
    memcpy(dstfft, src, dl*sizeof(CPX));
    memcpy(dstdft, src, dl*sizeof(CPX));

    /* test ft */
    timeuseset("fft", 0);
    fft(1, dl, dstfft, (int)(log(dl)/log(2)));
    timeuseset("fft", 1);
    
    timeuseset("dft", 0);
    dft(1, dl, dstdft);
    timeuseset("dft", 1);
    
    memcpy(midfft, dstfft, dl*sizeof(CPX));
    memcpy(middft, dstdft, dl*sizeof(CPX));

    /* test ift */
    timeuseset("ifft", 0);
    fft(-1, dl, dstfft, (int)(log(dl)/log(2)));
    timeuseset("ifft", 1);
    
    timeuseset("idft", 0);
    dft(-1, dl, dstdft);
    timeuseset("idft", 1);

    //dstfft[0].r = dstfft[0].r + 10;
    printf("[src-dstfft] = %d\r\n", ret1 = cmpcpx(dl, src, dstfft));
    //dstdft[0].i = dstdft[0].i + 0.01;
    printf("[src-dstdft] = %d\r\n", ret2 = cmpcpx(dl, src, dstdft));
    //midfft[0].i = midfft[0].i + 0.01;
    printf("[dft-fft] = %d\r\n", cmpcpx(dl, midfft, middft));
   
    if ((ret1 != 0) || (ret2 != 0) || (ret3 != 0)){
        printf("error\r\n");
        ret = -1;
    }else{
        printf("ok\r\n");
        save_signal(dl, midfft, "dst_fft.bin"); 
        save_signal(dl, middft, "dst_dft.bin"); 
        ret = 0;
    }
    free(src);
    free(dstdft);
    free(middft);
    free(dstfft);
    free(midfft);
}

int main(int argc, char **argv){
    printf("dsp start\r\n");
    autotest();
    return 0;
}
