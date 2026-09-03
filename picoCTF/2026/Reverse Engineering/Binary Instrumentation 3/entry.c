
undefined8 entry(void)

{
  uint uVar1;
  longlong lVar2;
  void *pvVar3;
  DWORD DVar4;
  uint uVar5;
  int iVar6;
  HANDLE pvVar7;
  LPVOID lpMem;
  char *pcVar8;
  ulonglong uVar9;
  longlong local_res8;
  short *local_res10;
  
  pvVar3 = ProcessEnvironmentBlock;
  pvVar7 = GetProcessHeap();
  lpMem = HeapAlloc(pvVar7,8,0x400);
  DVar4 = GetLastError();
  if (DVar4 == 0x361c) {
    ReleaseSRWLockExclusive((PSRWLOCK)0x0);
    ReleaseSRWLockShared((PSRWLOCK)0x0);
    SetCriticalSectionSpinCount((LPCRITICAL_SECTION)0x0,0);
    TryAcquireSRWLockExclusive((PSRWLOCK)0x0);
    WakeAllConditionVariable((PCONDITION_VARIABLE)0x0);
    SetUnhandledExceptionFilter((LPTOP_LEVEL_EXCEPTION_FILTER)0x0);
    UnhandledExceptionFilter((_EXCEPTION_POINTERS *)0x0);
    CheckMenuItem((HMENU)0x0,0,0);
    GetMenu((HWND)0x0);
    GetSystemMenu((HWND)0x0,0);
    GetMenuItemID((HMENU)0x0,0);
    EnableMenuItem((HMENU)0x0,0,0);
    MessageBeep(0);
    GetLastError();
    MessageBoxW((HWND)0x0,(LPCWSTR)0x0,(LPCWSTR)0x0,0);
    MessageBoxA((HWND)0x0,(LPCSTR)0x0,(LPCSTR)0x0,0);
    UpdateWindow((HWND)0x0);
    GetWindowContextHelpId((HWND)0x0);
  }
  else {
    pvVar7 = GetProcessHeap();
    HeapFree(pvVar7,0,lpMem);
  }
  if ((pvVar3 != (void *)0x0) && (*(int *)((longlong)pvVar3 + 0x118) == 10)) {
    uVar9 = 0;
    local_res10 = (short *)0x0;
    local_res8 = 0;
    lVar2 = *(longlong *)((longlong)pvVar3 + 0x10);
    iVar6 = *(int *)(lVar2 + 0x3c);
    pcVar8 = (char *)(lVar2 + 0x108 + (longlong)iVar6);
    do {
      uVar5 = FUN_1400014b0(pcVar8);
      if (uVar5 == 0x9f520b2d) {
        uVar5 = *(uint *)(pcVar8 + 0xc);
        uVar1 = *(uint *)(pcVar8 + 0x10);
        if ((ulonglong)uVar5 + lVar2 == 0) {
          return 0xffffffff;
        }
        if (uVar1 == 0) {
          return 0xffffffff;
        }
        iVar6 = FUN_1400018b0();
        if (iVar6 == 0) {
          return 0xffffffff;
        }
        uVar9 = FUN_140001300(1,(ulonglong)uVar5 + lVar2,(ulonglong)uVar1,&local_res10,&local_res8);
        if ((int)uVar9 != 0) {
          return 0xffffffff;
        }
        FUN_140001dc0(local_res10,local_res8);
        return 0;
      }
      pcVar8 = pcVar8 + 0x28;
      uVar9 = uVar9 + 1;
    } while (uVar9 <= *(ushort *)((longlong)iVar6 + 6 + lVar2));
  }
  return 0xffffffff;
}

