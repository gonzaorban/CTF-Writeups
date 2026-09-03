
ulonglong FUN_140001300(int param_1,undefined8 param_2,undefined8 param_3,undefined8 *param_4,
                       undefined8 *param_5)

{
  LPVOID lpMem;
  ulonglong uVar1;
  HANDLE hHeap;
  ulonglong uVar2;
  undefined1 *local_res10;
  undefined8 local_28;
  undefined8 local_20;
  LPVOID local_18;
  undefined8 local_10;
  
  local_res10 = FUN_1400022a0();
  local_18 = (LPVOID)0x0;
  local_10 = 0;
  local_28 = param_2;
  local_20 = param_3;
  uVar1 = FUN_140002320((longlong)local_res10,FUN_140001030,&local_28,FUN_140001150,&local_28,
                        param_1);
  lpMem = local_18;
  uVar2 = uVar1 & 0xffffffff;
  if ((int)uVar1 == 0) {
    FUN_1400022f0(&local_res10);
    *param_4 = local_18;
    *param_5 = local_10;
    uVar2 = 0;
  }
  else {
    if (local_18 != (LPVOID)0x0) {
      hHeap = GetProcessHeap();
      HeapFree(hHeap,0,lpMem);
    }
    FUN_1400022f0(&local_res10);
  }
  return uVar2;
}

