
void FUN_00101932(int param_1)

{
  undefined4 local_c;
  
  for (local_c = 0; local_c < param_1; local_c = local_c + 1) {
    putchar(0x2a);
    fflush((FILE *)0x0);
    sleep(1);
  }
  putchar(10);
  return;
}

