https://github.com/Samsung/ONE/issues/11743
# [onert-micro] Fix 3 critcal and 5 major svace defects

Let's fix svace defects on the latest master. It seems to be caused by recent kernel update.

[defect list link](https://analysishub.sec.samsung.net/service/analyses/2432084#defects)

  |  N | Severity |    ID | Classification | Checker                   | File Path                                                                        |                                                                                                   
  | --| ---|    ---| ---| ---| ---| 
  |  1 | Critical | 12230 | Undecided      | BUFFER_OVERFLOW.PROC      | /tmp/source_root/ONE/onert-micro/luci-interpreter/src/kernels/Mean.cpp:101       |
  |  2 | Critical | 12231 | Undecided      | BUFFER_OVERFLOW.PROC      | /tmp/source_root/ONE/onert-micro/luci-interpreter/src/kernels/Mean.cpp:101       |
  |  3 | Critical | 12234 | Undecided      | DIVISION_BY_ZERO          | /tmp/source_root/ONE/onert-micro/luci-interpreter/pal/common/PALL2Pool2D.h:69    |
  |  4 | Major    | 12210 | Undecided      | DEREF_OF_NULL.RET.STAT    | /tmp/source_root/ONE/onert-micro/luci-interpreter/src/kernels/Slice.cpp:89       |
  |  5 | Major    | 12211 | Undecided      | DEREF_OF_NULL.RET.STAT    | /tmp/source_root/ONE/onert-micro/luci-interpreter/src/kernels/PadCommon.cpp:131  |
  |  6 | Major    | 12232 | Undecided      | DEREF_OF_NULL.RET.STAT    | /tmp/source_root/ONE/onert-micro/luci-interpreter/src/kernels/Conv2D.cpp:294     |
  |  7 | Major    | 12233 | Undecided      | DEREF_OF_NULL.RET.STAT    | /tmp/source_root/ONE/onert-micro/luci-interpreter/src/loader/GraphLoader.cpp:113 |
  |  8 | Major    | 12235 | Undecided      | SIGNED_TO_BIGGER_UNSIGNED | /tmp/source_root/ONE/onert-micro/luci-interpreter/pal/common/PALMean.h:148       |
