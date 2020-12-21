#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <hackrf.h>
#include <math.h>

void modulation(float * input, unsigned int input_len, float * output, unsigned int mode) ;

#define WAV_CHANNEL 2
#define WAV_BITPERBYTE 2
#define WAV_SAMPLE_RATE 2000000
#define HACKRF_SAMPLE_RATE 2000000

#define IQ_DSP_GAIN 0.9f
#define IQ_DEAL_S 10
#define IQ_MUL 2

int wav2iq(char *wav_file, char *iq_file){
    unsigned int num_samples;
    float *pIQ_buf=NULL;
    unsigned char* pTX_buf=NULL;
    int i,j,ret,flg;
    char buftmp[4];
    FILE *p = NULL;
    float *pPCM;
    p=fopen(wav_file,"rb");
    
    flg = 0;
	do{
        if(flg!=0)fseek(p, -3, SEEK_CUR);
        flg = 1;
        ret = fread(buftmp, 4, 1, p);
    }while(memcmp(buftmp,"data", 4));
    fread((char*)&num_samples, 4, 1, p);
    num_samples = num_samples / (WAV_CHANNEL * WAV_BITPERBYTE);
    printf("num_samples=%d\r\n", num_samples);

    printf("len = %ld\r\n", sizeof(float));
    pPCM = (float*)malloc(num_samples*IQ_MUL*sizeof(float));
    float aaaa = (float)HACKRF_SAMPLE_RATE / (float)WAV_SAMPLE_RATE;
    printf("============%f\r\n", aaaa);
    pTX_buf = malloc(aaaa*num_samples*4); 

    short data_in_channel;
    float data_f;
    for (i = 0; i < num_samples; i++) {
        fread(buftmp, (WAV_CHANNEL * WAV_BITPERBYTE), 1, p);
        memcpy(&data_in_channel, buftmp, WAV_BITPERBYTE);
        data_f = data_in_channel/32767.0;
        memcpy((float*)pPCM+i,&data_f,sizeof(float));
    }
    fclose(p);

#if 1
    int t_offset = 0;
    pIQ_buf = (float*)malloc(HACKRF_SAMPLE_RATE*IQ_DEAL_S*sizeof(float)*4);
    for(i=0;i<num_samples;i+=(IQ_DEAL_S*WAV_SAMPLE_RATE))
    {
        printf("%d/%d\r\n", i, num_samples);
	    if(i+WAV_SAMPLE_RATE > num_samples){
            break;
        }
	    modulation(pPCM+i, WAV_SAMPLE_RATE*IQ_DEAL_S, pIQ_buf,0);
        for(j=0;j<2*(HACKRF_SAMPLE_RATE*IQ_DEAL_S);j++){
		    pTX_buf[t_offset+j] =(unsigned char)(pIQ_buf[j]*127.0);
        }
	    t_offset += 2*(HACKRF_SAMPLE_RATE*10);
    }
    //free(pIQ_buf);
#endif

    printf("t_offset=%d\r\n", t_offset);
    p=fopen(iq_file,"wb+");
    fwrite(pTX_buf, t_offset, 1, p);
    fclose(p);

    return 0;
}

void modulation(float * input, unsigned int input_len, float * output, unsigned int mode) 
{
	unsigned int i;
    double fm_deviation=0;
    static double fm_phase=0;
    if (mode == 0) {
		fm_deviation = 2.0 * M_PI * 75.0e3 / HACKRF_SAMPLE_RATE; // 75 kHz max deviation WBFM
	}
	else if (mode == 1)
	{
		fm_deviation = 2.0 * M_PI * 5.0e3 / HACKRF_SAMPLE_RATE; // 5 kHz max deviation NBFM
	}

	//AM mode
	if (mode == 2) {
		for (i = 0; i < input_len; i++) {
			double	audio_amp = input[i] * IQ_DSP_GAIN;

			if (fabs(audio_amp) > 1.0) {
				audio_amp = (audio_amp > 0.0) ? 1.0 : -1.0;
			}

			output[i * 2] = 0;
			output[i * 2 + 1] = (float)audio_amp;
		}
	}
	//FM mode
	else {

		for (i = 0; i < input_len; i++) {

			double	audio_amp = input[i] * IQ_DSP_GAIN;

			if (fabs(audio_amp) > 1.0) {
				audio_amp = (audio_amp > 0.0) ? 1.0 : -1.0;
			}
			fm_phase += fm_deviation * audio_amp;
			while (fm_phase > (float)(M_PI))
				fm_phase -= (float)(2.0 * M_PI);
			while (fm_phase < (float)(-M_PI))
				fm_phase += (float)(2.0 * M_PI);

			output[i * 2] = (float)sin(fm_phase);
			output[i * 2 + 1] = (float)cos(fm_phase);
		}
	}


}

int main(int argc, char *argv[]){
    if(argc == 3){
        printf("start  ...\n");
        wav2iq(argv[1], argv[2]);
    }else{
        printf("Usage:%s <WAV File Abs Path> <IQ File Abs Path>\n", argv[0]);
    }
    return 0;
}

