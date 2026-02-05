char gen_garbage(){
    int fd = open("/dev/urandom", 0,0);
    if(fd < 0){
        puts("Error: Could not open /dev/urandom");
        exit(-1);
    }

    char buf[1];
    read(fd, buf, 1);
    close(fd);
    return buf[0];
}


int check_flag(char *flag){
if ((flag[0] ^ 0x06) != 0x40) goto fail;
if ((flag[1] ^ 0x95) != 0xD9) goto fail;
if ((flag[2] ^ 0xED) != 0xAC) goto fail;
if ((flag[3] ^ 0x5E) != 0x19) goto fail;
if ((flag[4] ^ 0x26) != 0x5D) goto fail;
if ((flag[5] ^ 0xD7) != 0x99) goto fail;
if ((flag[6] ^ 0x85) != 0xB5) goto fail;
if ((flag[7] ^ 0x10) != 0x4F) goto fail;
if ((flag[8] ^ 0x75) != 0x38) goto fail;
if ((flag[9] ^ 0xBE) != 0xD1) goto fail;
if ((flag[10] ^ 0xF3) != 0x81) goto fail;
if ((flag[11] ^ 0xE0) != 0xD3) goto fail;
if ((flag[12] ^ 0x16) != 0x49) goto fail;
if ((flag[13] ^ 0x05) != 0x53) goto fail;
if ((flag[14] ^ 0xE7) != 0xAA) goto fail;
if ((flag[15] ^ 0x25) != 0x7A) goto fail;
if ((flag[16] ^ 0x34) != 0x57) goto fail;
if ((flag[17] ^ 0x6C) != 0x04) goto fail;
if ((flag[18] ^ 0xEC) != 0x8D) goto fail;
if ((flag[19] ^ 0xC7) != 0xF6) goto fail;
if ((flag[20] ^ 0x33) != 0x02) goto fail;
if ((flag[21] ^ 0xDA) != 0xBF) goto fail;
if ((flag[22] ^ 0x49) != 0x27) goto fail;
if ((flag[23] ^ 0xAB) != 0xCC) goto fail;
if ((flag[24] ^ 0xE9) != 0x8C) goto fail;
if ((flag[25] ^ 0xE9) != 0x9A) goto fail;
if ((flag[26] ^ 0xEA) != 0xB5) goto fail;
if ((flag[27] ^ 0x4E) != 0x3E) goto fail;
if ((flag[28] ^ 0x02) != 0x6E) goto fail;
if ((flag[29] ^ 0xF0) != 0x8A) goto fail;
if ((flag[30] ^ 0x8A) != 0xBB) goto fail;
if ((flag[31] ^ 0x6B) != 0x5A) goto fail;
if ((flag[32] ^ 0xC3) != 0xF2) goto fail;
if ((flag[33] ^ 0x67) != 0x1A) goto fail;
    puts("Correct!");
    return 0;
    fail:
    int garbage = (unsigned char)gen_garbage() + 100;
    int gay = 0;
    for(unsigned int i=0;i<garbage;i++){
        gay += 1;
    }
    puts("Nope2...");
    return 1;
}

int main(){
    char aaa[34 + 1];
    memset(aaa, 0, 34 + 1);
    printf("Flag: ");
    fgets(aaa, 34 + 1, stdin);
    if (strlen(aaa) != 34){
        puts("Nope1...");
        return 1;
    }
    return check_flag(aaa);
}
