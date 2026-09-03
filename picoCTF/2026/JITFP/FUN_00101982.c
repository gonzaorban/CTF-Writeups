
undefined8 FUN_00101982(int param_1,undefined8 *param_2)

{
  int iVar1;
  undefined8 uVar2;
  int local_10;
  int local_c;
  
  prctl(0x59616d61,0xffffffffffffffff,0,0,0);
  if (param_1 == 2) {
    for (local_10 = 0; local_10 < 0x20; local_10 = local_10 + 1) {
      putchar(0x3d);
      fflush((FILE *)0x0);
    }
    puts("v");
    for (local_c = 0; local_c < 0x21; local_c = local_c + 1) {
      sleep(1);
      iVar1 = (**(code **)(&DAT_00104120 + (long)*(int *)(&DAT_00104020 + (long)local_c * 4) * 8))
                        ((int)*(char *)((long)local_c + param_2[1]));
      if (iVar1 == 0) {
        FUN_00101932(0x21 - local_c);
        puts("Incorrect");
        return 1;
      }
      putchar(0x2a);
      fflush((FILE *)0x0);
    }
    sleep(1);
    if (*(char *)(param_2[1] + 0x21) == '\0') {
      puts("\nCorrect");
      uVar2 = 0;
    }
    else {
      puts("\nIncorrect");
      uVar2 = 1;
    }
  }
  else {
    printf("Usage: %s <flag>\n",*param_2);
    uVar2 = 1;
  }
  return uVar2;
}

