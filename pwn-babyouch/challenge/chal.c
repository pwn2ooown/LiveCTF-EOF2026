#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
int challenge(){
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    puts("I'm baby :)");
    char buffer[64]={'0'};
    while(1){
        read(0,buffer,200);
        if(memcmp(buffer, "exit",4) == 0){
            break;
        }
	puts(buffer);
    }
    return 0;
}
int main(){
	challenge();
}
