import sys
import os
import re
import lizard

def getAllBC(filepath):
    bcList = []
    if os.path.isdir(filepath):
        # When the path is a directory, traverse all files and directories under the directory
        for s in os.listdir(filepath):
            newPath = os.path.join(filepath, s)
            if os.path.isdir(newPath):
                bcList.append(newPath)
    return bcList

def findFunction(filename):
    fp = open(filename, encoding='gbk', errors='ignore')
    print(fp)
    lines = fp.readlines()
    temp = ""
    code = ''
    for line in lines:
        line = temp + line
        line = line.strip("\r\t ")  # Remove white space at both ends
        if line[-1] == "\\":  # Check whether there is a line continuation character at the end. If there is a line continuation character, save the current line value and prepare to splice it with the next line.
            temp += line[:-1]
            continue
        else:
            temp = ""
        code += line

    function_parten = r'\w+\s+(?P<name>\w+)((\s*)(\()(\n)?)[\w+\s*\w*]+((\s*)(\))(\n)?)\{'
    pat1 = re.compile(function_parten, re.X)

    ret1 = pat1.finditer(code)
    functionlist = []
    if ret1 != None:

        for match in ret1:
            function_name = match.group('name')
            state = 1

            functionindex = ''
            for i in range(match.end(), len(code)):
                if code[i] == "{":
                    state += 1
                elif code[i] == "}":
                    state -= 1
                if state == 0:
                    functionindex = code[match.start():i + 1]
                    break

            functionlist.append([function_name, functionindex])
    return functionlist

def generate_tokens(source_code, addition='', token_class=None):
    def create_token(match):
        return match.group(0)
    if not token_class:
        token_class = create_token

    def _generate_tokens(source_code, addition):
        # DO NOT put any sub groups in the regex. Good for performance
        _until_end = r"(?:\\\n|[^\n])*"
        combined_symbols = ["<<=", ">>=", "||", "&&", "===", "!==",
                            "==", "!=", "<=", ">=", "->", "=>",
                            "++", "--", '+=', '-=',
                            "+", "-", '*', '/',
                            '*=', '/=', '^=', '&=', '|=', "..."]
        token_pattern = re.compile(
            r"(?:" +
            r"\/\*.*?\*\/" +
            addition +
            r"|\w+" +
            r"|\"(?:\\.|[^\"\\])*\"" +
            r"|\'(?:\\.|[^\'\\])*?\'" +
            r"|\/\/" + _until_end +
            r"|\#" +
            r"|:=|::|\*\*" +
            r"|\<\s*\?\s*\>" +
            r"|" + r"|".join(re.escape(s) for s in combined_symbols) +
            r"|\\\n" +
            r"|\n" +
            r"|[^\S\n]+" +
            r"|.)", re.M | re.S)
        macro = ""
        for match in token_pattern.finditer(source_code):
            token = token_class(match)
            if macro:
                if "\\\n" in token or "\n" not in token:
                    macro += token
                else:
                    yield macro
                    yield token
                    macro = ""
            elif token == "#":
                macro = token
            else:
                yield token
        if macro:
            yield macro

    return [t for t in _generate_tokens(source_code, addition)]

rgl_exp1 = r'''
            
            ((VOID)|(void)|(char)|(short)|(int)|(float)|(long)|(double)) # Identify function return value types
            (\s*(\*)?\s*)                                                # Identify whether the return value is a pointer type and contains spaces in the middle
            (\w+)                                                        # Identify function names
            ((\s*)(\()(\n)?)                                             # Function opening parenthesis
            ((\s*)?(const)?(\s*)?                                        # Is there const before the parameter?
            ((void)|(char)|(short)|(int)|(float)|(long)|(double))        # Parameter Type
            (\s*)(\*)?(\s*)?(restrict)?(\s*)?(\w*)(\s*)?(\,)?(\n)?(.*)?)*# The * at the end indicates there are multiple parameters
            ((\s*)(\))(\n)?)                                             # Function closing parenthesis
            \{
            '''

rgl = r'\w+(\s|\n|\*)+\w+(\s|\n)*\((\s|\n|!|%|&|\(|\)|\*|\+|,|-|\/|\w|\[|\\|\]|\^|\||~|<{2}|>{2})*?\)(\n|\s)*\{'
function_parten =  r'\w+\s+(?P<name>\w+)((\s*)(\()(\n)?)[\w+\s*\w*]+((\s*)(\))(\n)?)\{'
function_return_type = r'''
                    (   
                       (const)?(volatile)?(static)?\s*(inline)?\s*(extern)?\s*
                                (
                                    (VOID)|(void)|(enum)|
                                        ((unsigned)?(signed)?(long)?\s*(int)|(char)|(float)|(short)|(long)|(double))|
                                        (bool)|(struct\s*\w+)|(union\s*\w+)|(wait_queue_t)|(wait_queue_head_t)
                                )
                                \s*(fastcall)?

                    )  
                    (\s*(\*)?\s*) 
                    (?P<name>\w+) 
                    ((\s*)(\()(\n)?) 
                    ((\s*)?(const)?(volatile)?(\s*)? 
                    (   
                       (static)?\s*(inline)?\s*(extern)?\s*
                                (
                                    (VOID)|(void)|(enum)|
                                        ((unsigned)?(signed)?(long)?\s*\s*(int)|(char)|(float)|(short)|(long)|(double))|
                                        (bool)|(struct\s*\w+)|(union\s*\w+)|(wait_queue_t)|(wait_queue_head_t)
                                )
                                \s*(fastcall)?

                    ) 
                    (\s*)(\*)?(\s*)?(restrict)?(\s*)?(\w*)(\s*)?(\,)?(\n)?(.*)?)* 
                    ((\s*)(\))(\n)?)
                    ((\s*)(\{))
'''

# 匹配函数，包含函数体


code = """
#include "exti.h"
#include "led.h"
#include "key.h"
#include "delay.h"
#include "usart.h"
#include "beep.h"

//////////////////////////////////////////////////////////////////////////////////	 
//������ֻ��ѧϰʹ�ã�δ���������ɣ��������������κ���;
//ALIENTEK��ӢSTM32������
//�ⲿ�ж� ��������	   
//����ԭ��@ALIENTEK
//������̳:www.openedv.com
//�޸�����:2012/9/3
//�汾��V1.0
//��Ȩ���У�����ؾ���
//Copyright(C) �������������ӿƼ����޹�˾ 2009-2019
//All rights reserved									  
//////////////////////////////////////////////////////////////////////////////////   
//�ⲿ�ж�0�������
void EXTIX_Init(void)
{
 
   	EXTI_InitTypeDef EXTI_InitStructure;
 	  NVIC_InitTypeDef NVIC_InitStructure;

    KEY_Init();	 //	�����˿ڳ�ʼ��

  	RCC_APB2PeriphClockCmd(RCC_APB2Periph_AFIO,ENABLE);	//ʹ�ܸ��ù���ʱ��



   //GPIOE.3	  �ж����Լ��жϳ�ʼ������ �½��ش��� //KEY1
  	GPIO_EXTILineConfig(GPIO_PortSourceGPIOE,GPIO_PinSource3);
  	EXTI_InitStructure.EXTI_Line=EXTI_Line3;
  	EXTI_InitStructure.EXTI_Mode = EXTI_Mode_Interrupt;	
  	EXTI_InitStructure.EXTI_Trigger = EXTI_Trigger_Falling;
  	EXTI_Init(&EXTI_InitStructure);	  	//����EXTI_InitStruct��ָ���Ĳ�����ʼ������EXTI�Ĵ���

   //GPIOE.4	  �ж����Լ��жϳ�ʼ������  �½��ش���	//KEY0
  	GPIO_EXTILineConfig(GPIO_PortSourceGPIOE,GPIO_PinSource4);
  	EXTI_InitStructure.EXTI_Line=EXTI_Line4;
  	EXTI_Init(&EXTI_InitStructure);	  	//����EXTI_InitStruct��ָ���Ĳ�����ʼ������EXTI�Ĵ���


   //GPIOA.0	  �ж����Լ��жϳ�ʼ������ �����ش��� PA0  WK_UP
 	  GPIO_EXTILineConfig(GPIO_PortSourceGPIOA,GPIO_PinSource0); 

  	EXTI_InitStructure.EXTI_Line=EXTI_Line0;
  	EXTI_InitStructure.EXTI_Trigger = EXTI_Trigger_Rising;
  	EXTI_Init(&EXTI_InitStructure);		//����EXTI_InitStruct��ָ���Ĳ�����ʼ������EXTI�Ĵ���


  	NVIC_InitStructure.NVIC_IRQChannel = EXTI0_IRQn;			//ʹ�ܰ���WK_UP���ڵ��ⲿ�ж�ͨ��
  	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0x02;	//��ռ���ȼ�2�� 
  	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 0x03;					//�����ȼ�3
  	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;								//ʹ���ⲿ�ж�ͨ��
  	NVIC_Init(&NVIC_InitStructure); 

  	NVIC_InitStructure.NVIC_IRQChannel = EXTI3_IRQn;			//ʹ�ܰ���KEY1���ڵ��ⲿ�ж�ͨ��
  	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0x02;	//��ռ���ȼ�2 
  	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 0x01;					//�����ȼ�1 
  	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;								//ʹ���ⲿ�ж�ͨ��
  	NVIC_Init(&NVIC_InitStructure);  	  //����NVIC_InitStruct��ָ���Ĳ�����ʼ������NVIC�Ĵ���

  	NVIC_InitStructure.NVIC_IRQChannel = EXTI4_IRQn;			//ʹ�ܰ���KEY0���ڵ��ⲿ�ж�ͨ��
  	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 0x02;	//��ռ���ȼ�2 
  	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 0x00;					//�����ȼ�0 
  	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;								//ʹ���ⲿ�ж�ͨ��
  	NVIC_Init(&NVIC_InitStructure);  	  //����NVIC_InitStruct��ָ���Ĳ�����ʼ������NVIC�Ĵ���
 
}

//�ⲿ�ж�0������� 
void EXTI0_IRQHandler(void)
{
	delay_ms(10);//����
	if(WK_UP==1)	 	 //WK_UP����
	{				 
		BEEP=!BEEP;	
	}
	EXTI_ClearITPendingBit(EXTI_Line0); //���LINE0�ϵ��жϱ�־λ  
}
 

//�ⲿ�ж�3�������
void EXTI3_IRQHandler(void)
{
	delay_ms(10);//����
	if(KEY1==0)	 //����KEY1
	{				 
		LED1=!LED1;
	}		 
	EXTI_ClearITPendingBit(EXTI_Line3);  //���LINE3�ϵ��жϱ�־λ  
}

void EXTI4_IRQHandler(void)
{
	delay_ms(10);//����
	if(KEY0==0)	 //����KEY0
	{
		LED0=!LED0;
		LED1=!LED1; 
	}		 
	EXTI_ClearITPendingBit(EXTI_Line4);  //���LINE4�ϵ��жϱ�־λ  
}
 

    """





'''pat1 = re.compile(function_parten, re.X)

ret1 = pat1.finditer(code)

for match in ret1:
    function_name = match.group('name')
    state = 1
    functionlist = []
    functionindex = ''
    for i in range(match.end(),len(code)):
        if code[i] == "{":
            state +=1
        elif code[i] == "}":
            state -=1
        if state == 0:
            functionindex = code[match.start():i+1]
            break
    print(functionindex)
    functionlist.append([function_name,functionindex])'''



'''if None == ret1:
    print('不包含C函数定义!')
else:
    print(ret1.group())
    print("包含C函数定义!")

tokens = generate_tokens(code)
print(generate_tokens(code))'''

code = """void USART1_IRQHandler(void)                	//����1�жϷ������
	{
	u8 Res;
#if SYSTEM_SUPPORT_OS 		//���SYSTEM_SUPPORT_OSΪ�棬����Ҫ֧��OS.
	OSIntEnter();    
#endif
	if(USART_GetITStatus(USART1, USART_IT_RXNE) != RESET)  //�����ж�(���յ������ݱ�����0x0d 0x0a��β)
		{
		Res =USART_ReceiveData(USART1);	//��ȡ���յ�������
		
		if((USART_RX_STA&0x8000)==0)//����δ���
			{
			if(USART_RX_STA&0x4000)//���յ���0x0d
				{
				if(Res!=0x0a)USART_RX_STA=0;//���մ���,���¿�ʼ
				else USART_RX_STA|=0x8000;	//��������� 
				}
			else //��û�յ�0X0D
				{	
				if(Res==0x0d)USART_RX_STA|=0x4000;
				else
					{
					USART_RX_BUF[USART_RX_STA&0X3FFF]=Res ;
					USART_RX_STA++;
					if(USART_RX_STA->(USART_REC_LEN-1))USART_RX_STA=0;//�������ݴ���,���¿�ʼ����	  
					}		 
				}
			}   		 
     } 
#if SYSTEM_SUPPORT_OS 	//���SYSTEM_SUPPORT_OSΪ�棬����Ҫ֧��OS.
	OSIntExit();  											 
#endif
} """
code1 = """
void uart_init(u32 bound){
  //GPIO�˿�����
   b = (a == 10) ? 20: 30;
   unsigned char a;
  GPIO_InitTypeDef GPIO_InitStructure;
	USART_InitTypeDef USART_InitStructure;
	NVIC_InitTypeDef NVIC_InitStructure;
	 
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1|RCC_APB2Periph_GPIOA, ENABLE);	//ʹ��USART1��GPIOAʱ��
  
	//USART1_TX   GPIOA.9
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9; //PA.9
  GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;	//�����������
  GPIO_Init(GPIOA, &GPIO_InitStructure);//��ʼ��GPIOA.9
   
  //USART1_RX	  GPIOA.10��ʼ��
  GPIO_InitStructure.GPIO_Pin = GPIO_Pin_10;//PA10
  GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING;//��������
  GPIO_Init(GPIOA, &GPIO_InitStructure);//��ʼ��GPIOA.10  

  //Usart1 NVIC ����
  NVIC_InitStructure.NVIC_IRQChannel = USART1_IRQn;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority=3 ;//��ռ���ȼ�3
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 3;		//�����ȼ�3
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;			//IRQͨ��ʹ��
	NVIC_Init(&NVIC_InitStructure);	//����ָ���Ĳ�����ʼ��VIC�Ĵ���
  
   //USART ��ʼ������

	USART_InitStructure.USART_BaudRate = bound;//���ڲ�����
	USART_InitStructure.USART_WordLength = USART_WordLength_8b;//�ֳ�Ϊ8λ���ݸ�ʽ
	USART_InitStructure.USART_StopBits = USART_StopBits_1;//һ��ֹͣλ
	USART_InitStructure.USART_Parity = USART_Parity_No;//����żУ��λ
	USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;//��Ӳ������������
	USART_InitStructure.USART_Mode = USART_Mode_Rx | USART_Mode_Tx;	//�շ�ģʽ

  USART_Init(USART1, &USART_InitStructure); //��ʼ������1
  USART_ITConfig(USART1, USART_IT_RXNE, ENABLE);//�������ڽ����ж�
  USART_Cmd(USART1, ENABLE);                    //ʹ�ܴ���1 

}"""
#file = lizard.analyze_file(r'C:\Users\yjl\Desktop\PostBuild.c')


