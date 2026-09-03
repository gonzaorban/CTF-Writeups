
void FUN_140001dc0(short *param_1,longlong param_2)

{
  undefined8 *puVar1;
  ushort uVar2;
  undefined8 *puVar3;
  ushort uVar4;
  uint uVar5;
  undefined1 *puVar6;
  longlong lVar7;
  longlong lVar8;
  char *pcVar9;
  code *pcVar10;
  longlong *plVar11;
  uint *puVar12;
  uint uVar13;
  longlong *plVar15;
  longlong *plVar16;
  uint *puVar17;
  ulonglong uVar18;
  int *piVar19;
  undefined8 in_stack_ffffffffffffff58;
  ulonglong uVar14;
  
  uVar13 = (uint)((ulonglong)in_stack_ffffffffffffff58 >> 0x20);
  if ((((param_1 != (short *)0x0) && (uVar18 = 0, param_2 != 0)) && (*param_1 == 0x5a4d)) &&
     (piVar19 = (int *)((longlong)*(int *)(param_1 + 0x1e) + (longlong)param_1), *piVar19 == 0x4550)
     ) {
    if ((((piVar19 != (int *)0x0) && ((uint *)(piVar19 + 0x24) != (uint *)0x0)) &&
        ((piVar19 != (int *)0xffffffffffffff30 &&
         (((uint *)(piVar19 + 0x2c) != (uint *)0x0 && (piVar19 != (int *)0xffffffffffffff60)))))) &&
       (piVar19 != (int *)0xfffffffffffffef8)) {
      FUN_140004d60(0,*(longlong *)(piVar19 + 0xc),(undefined4 *)0x0);
      puVar6 = (undefined1 *)
               FUN_1400048d0(0,*(longlong *)(piVar19 + 0xc),(ulonglong)(uint)piVar19[0x14],0,
                             (ulonglong)uVar13 << 0x20,(undefined4 *)0x0);
      if ((puVar6 != (undefined1 *)0x0) ||
         (puVar6 = (undefined1 *)FUN_140004a00((ulonglong)(uint)piVar19[0x14],(undefined4 *)0x0),
         puVar6 != (undefined1 *)0x0)) {
        FUN_1400010d0((longlong)puVar6,(longlong)param_1,(ulonglong)(uint)piVar19[0x15]);
        if (*(short *)((longlong)piVar19 + 6) != 0) {
          puVar12 = (uint *)(piVar19 + 0x47);
          uVar14 = uVar18;
          do {
            FUN_1400010d0((longlong)(puVar6 + puVar12[-2]),(ulonglong)*puVar12 + (longlong)param_1,
                          (ulonglong)puVar12[-1]);
            puVar12 = puVar12 + 10;
            uVar13 = (int)uVar14 + 1;
            uVar14 = (ulonglong)uVar13;
          } while ((int)uVar13 < (int)(uint)*(ushort *)((longlong)piVar19 + 6));
        }
        if (piVar19[0x25] != 0) {
          do {
            lVar7 = (uint)piVar19[0x24] + uVar18;
            uVar13 = *(uint *)(puVar6 + lVar7);
            if ((uVar13 == 0) && (*(int *)(puVar6 + lVar7 + 0x10) == 0)) break;
            uVar14 = (ulonglong)*(uint *)(puVar6 + lVar7 + 0x10);
            lVar8 = FUN_140001900(puVar6 + *(uint *)(puVar6 + lVar7 + 0xc));
            if (lVar8 == 0) {
              return;
            }
            if (uVar13 == 0) {
              uVar13 = *(uint *)(puVar6 + lVar7 + 0x10);
            }
            plVar11 = (longlong *)(puVar6 + uVar13);
            if (*(longlong *)(puVar6 + uVar14) != 0) {
              plVar15 = (longlong *)(puVar6 + uVar14);
              do {
                lVar7 = *plVar11;
                if (lVar7 < 0) {
                  pcVar9 = (char *)((ulonglong)
                                    *(uint *)((ulonglong)
                                              *(uint *)((ulonglong)
                                                        *(uint *)((longlong)*(int *)(lVar8 + 0x3c) +
                                                                  0x88 + lVar8) + 0x1c + lVar8) +
                                              lVar8 + lVar7 * 4) + lVar8);
                }
                else {
                  uVar5 = FUN_1400014b0(puVar6 + lVar7 + 2);
                  pcVar9 = FUN_140001730(lVar8,uVar5);
                }
                if (pcVar9 == (char *)0x0) {
                  return;
                }
                plVar16 = plVar15 + 1;
                *plVar15 = (longlong)pcVar9;
                plVar11 = (longlong *)((uVar13 - uVar14) + (longlong)plVar16);
                plVar15 = plVar16;
              } while (*plVar16 != 0);
            }
            uVar18 = uVar18 + 0x14;
          } while (uVar18 < (uint)piVar19[0x25]);
        }
        if (puVar6 != *(undefined1 **)(piVar19 + 0xc)) {
          lVar7 = (longlong)puVar6 - (longlong)*(undefined1 **)(piVar19 + 0xc);
          uVar13 = *(uint *)(puVar6 + (uint)piVar19[0x2c]);
          puVar12 = (uint *)(puVar6 + (uint)piVar19[0x2c]);
          while (uVar13 != 0) {
            puVar17 = puVar12 + 2;
            if (puVar17 != (uint *)((ulonglong)puVar12[1] + (longlong)puVar12)) {
              do {
                uVar2 = (ushort)*puVar17;
                uVar13 = (uint)uVar2;
                uVar4 = uVar2 >> 0xc;
                if (uVar4 != 0) {
                  if (uVar4 == 1) {
                    *(short *)(puVar6 + (ulonglong)*puVar12 + (ulonglong)(uVar13 & 0xfff)) =
                         *(short *)(puVar6 + (ulonglong)*puVar12 + (ulonglong)(uVar13 & 0xfff)) +
                         (short)((ulonglong)lVar7 >> 0x10);
                  }
                  else if (uVar4 == 2) {
                    *(short *)(puVar6 + (ulonglong)*puVar12 + (ulonglong)(uVar13 & 0xfff)) =
                         *(short *)(puVar6 + (ulonglong)*puVar12 + (ulonglong)(uVar13 & 0xfff)) +
                         (short)lVar7;
                  }
                  else if (uVar4 == 3) {
                    *(int *)(puVar6 + (ulonglong)*puVar12 + (ulonglong)(uVar13 & 0xfff)) =
                         *(int *)(puVar6 + (ulonglong)*puVar12 + (ulonglong)(uVar13 & 0xfff)) +
                         (int)lVar7;
                  }
                  else {
                    if (uVar4 != 10) {
                      return;
                    }
                    *(longlong *)(puVar6 + (ulonglong)*puVar12 + (ulonglong)(uVar2 & 0xfff)) =
                         *(longlong *)(puVar6 + (ulonglong)*puVar12 + (ulonglong)(uVar2 & 0xfff)) +
                         lVar7;
                  }
                }
                puVar17 = (uint *)((longlong)puVar17 + 2);
              } while (puVar17 != (uint *)((ulonglong)puVar12[1] + (longlong)puVar12));
            }
            puVar12 = puVar17;
            uVar13 = *puVar17;
          }
        }
        if (piVar19[0x29] != 0) {
          uVar13 = piVar19[0x28];
          lVar7 = FUN_140001650("KERNEL32.DLL");
          pcVar10 = (code *)FUN_140001730(lVar7,0x9219585c);
          if (pcVar10 != (code *)0x0) {
            (*pcVar10)(puVar6 + uVar13,(uint)piVar19[0x29] / 0xc - 1,puVar6);
          }
        }
        FUN_1400019c0();
        uVar18 = 0;
        if (*(short *)((longlong)piVar19 + 6) != 0) {
          do {
            uVar13 = piVar19[uVar18 * 10 + 0x4b];
            uVar5 = (int)uVar13 >> 0x1f & 8;
            if ((uVar13 >> 0x1e & 1) != 0) {
              uVar5 = 2;
            }
            if ((uVar13 & 0xc0000000) == 0xc0000000) {
              uVar5 = 4;
            }
            if ((uVar13 >> 0x1d & 1) != 0) {
              uVar5 = 0x10;
            }
            if ((uVar13 & 0xa0000000) == 0xa0000000) {
              uVar5 = 0x80;
            }
            if ((uVar13 & 0x60000000) == 0x60000000) {
              uVar5 = 0x20;
            }
            if ((uVar13 & 0xe0000000) == 0xe0000000) {
              uVar5 = 0x40;
            }
            FUN_140004c70(0,(longlong)(puVar6 + (uint)piVar19[uVar18 * 10 + 0x45]),
                          (ulonglong)(uint)piVar19[uVar18 * 10 + 0x46],uVar5,(undefined4 *)0x0);
            uVar13 = (int)uVar18 + 1;
            uVar18 = (ulonglong)uVar13;
          } while (uVar13 < *(ushort *)((longlong)piVar19 + 6));
        }
        if (piVar19[0x35] != 0) {
          puVar3 = *(undefined8 **)(puVar6 + (ulonglong)(uint)piVar19[0x34] + 0x18);
          pcVar10 = (code *)*puVar3;
          while (pcVar10 != (code *)0x0) {
            (*pcVar10)(puVar6,1);
            puVar1 = puVar3 + 1;
            puVar3 = puVar3 + 1;
            pcVar10 = (code *)*puVar1;
          }
        }
        uVar13 = piVar19[10];
        FUN_1400015a0(puVar6,(ulonglong)(uint)piVar19[0x45]);
        (*(code *)(puVar6 + uVar13))();
      }
    }
  }
  return;
}

