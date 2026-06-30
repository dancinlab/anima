https://github.com/Samsung/ONE/issues/4309
# [onert] Incorrect result of Cast operation with bool type input

TFLite generates result of Cast operation to 1 when type of inputs is boolean and the input's value is true. But onert' acl backends generate the result to 255. We need to fix it.

- Some nnfw api testcases for this issue
```cpp
TEST_F(GenModelTest, OneOp_Cast_BoolToFloat32)
{
  CircleGen cgen;
  int in = cgen.addTensor({{1, 2, 2, 1}, circle::TensorType::TensorType_BOOL});
  int out = cgen.addTensor({{1, 2, 2, 1}, circle::TensorType::TensorType_FLOAT32});
  cgen.addOperatorCast({{in}, {out}}, circle::TensorType::TensorType_BOOL,
                       circle::TensorType::TensorType_FLOAT32);
  cgen.setInputsAndOutputs({in}, {out});

  _context = std::make_unique<GenModelTestContext>(cgen.finish());
  TestCaseData tcd;
  tcd.addInput(std::vector<bool>{true, false, true, true});
  tcd.addOutput(std::vector<float>{1, 0, 1, 1});
  _context->addTestCase(tcd);
  _context->setBackends({"acl_cl", "acl_neon", "cpu"});

  SUCCEED();
}

TEST_F(GenModelTest, OneOp_Cast_AfterEqual)
{
  CircleGen cgen;
  int lhs = cgen.addTensor({{1, 2, 2, 1}, circle::TensorType::TensorType_FLOAT32});
  int rhs = cgen.addTensor({{1, 2, 2, 1}, circle::TensorType::TensorType_FLOAT32});
  int equal_out = cgen.addTensor({{1, 2, 2, 1}, circle::TensorType::TensorType_BOOL});
  int out = cgen.addTensor({{1, 2, 2, 1}, circle::TensorType::TensorType_FLOAT32});
  cgen.addOperatorEqual({{lhs, rhs}, {equal_out}});
  cgen.addOperatorCast({{equal_out}, {out}}, circle::TensorType::TensorType_BOOL,
                       circle::TensorType::TensorType_FLOAT32);
  cgen.setInputsAndOutputs({lhs, rhs}, {out});

  _context = std::make_unique<GenModelTestContext>(cgen.finish());
  _context->addTestCase(uniformTCD<float>({{1, 3, 2, 4}, {2, 3, 1, 4}}, {{0, 1, 0, 1}}));
  _context->setBackends({"acl_cl", "acl_neon", "cpu"});

  SUCCEED();
}
```

- Failure by above tests
<details>

```bash
$ ONERT_LOG_ENABLE=1 Product/armv7l-linux.debug/out/unittest_standalone/nnfw_api_gtest --gtest_filter=GenModelTest.*OneOp_Cast_*
Note: Google Test filter = GenModelTest.*OneOp_Cast_*
[==========] Running 2 tests from 1 test case.
[----------] Global test environment set-up.
[----------] 2 tests from GenModelTest
[ RUN      ] GenModelTest.OneOp_Cast_BoolToFloat32
[EdgeConsistencyChecker] Total Number of errors : 0
[Compiler] [Compiler] ==== Compiler Options ====
[Compiler] backend_list             : acl_cl
[Compiler] trace_filepath           : 
[Compiler] graph_dump_level         : 0
[Compiler] op_seq_max_node          : 0
[Compiler] executor                 : Linear
[Compiler] manual_scheduler_options : (Too many things to print)
[Compiler] he_scheduler             : false
[Compiler] he_profiling_mode        : false
[Compiler] disable_compile          : false
[Compiler] fp16_enable              : false
[Compiler] [loadBackend] Successfully loaded 'acl_cl' - libbackend_acl_cl.so
[onert_backend_create] 'acl_cl' loaded
[acl_cl_createTensorManager] AclTensorManager as Linear
[ManualScheduler] Default backend for all ops: acl_cl
[ManualScheduler] backend for operation #0: acl_cl
[Lower] OpSequence#0 is created for NODE#0(Cast)
[OpSequences] dump before permutation insertion
[OpSequences] 0]   OpSequence IN(0) -> { 0(Cast:0:1) } -> OUT(1)
[PassRunner] Start running 'ConstantInsertionPass'
[PassRunner] Finished running 'ConstantInsertionPass'
[PassRunner] Start running 'ConstantLoweringPass'
[PassRunner] Finished running 'ConstantLoweringPass'
[Lower] Operand #0 LowerInfo
  - Shape           : { 1 2 2 1 }
  - Def ir::Operations  : N/A
  - Use ir::Operations  : { 0 }
  - Lower Info
    - Def Backends    : { controlflow(NHWC) }
    - Use Backends    : { acl_cl(NHWC) }
[Lower] Operand #1 LowerInfo
  - Shape           : { 1 2 2 1 }
  - Def ir::Operations  : 0
  - Use ir::Operations  : { }
  - Lower Info
    - Def Backends    : { acl_cl(NHWC) }
    - Use Backends    : { controlflow(NHWC) }
[PassRunner] Start running 'PermutationOperationPass'
[PassRunner] Finished running 'PermutationOperationPass'
[PassRunner] Start running 'PermutationInsertionPass'
[insertPermute] Permute Op inserted, node index : 1
[insertPermute]   - Input (original) Operand : 0
[insertPermute]   - Output(inserted) Operand : 2
[insertPermute] Permute Op inserted, node index : 2
[insertPermute]   - Input (original) Operand : 1
[insertPermute]   - Output(inserted) Operand : 3
[PassRunner] Finished running 'PermutationInsertionPass'
[PassRunner] Start running 'PermutationEliminationPass'
[PassRunner] Finished running 'PermutationEliminationPass'
[OpSequences] Dump after permutation insertion
[OpSequences] 2]   OpSequence IN(1) -> { 2(Permute:1:3) } -> OUT(3)
[OpSequences] 0]   OpSequence IN(2) -> { 0(Cast:2:1) } -> OUT(1)
[OpSequences] 1]   OpSequence IN(0) -> { 1(Permute:0:2) } -> OUT(2)
[EdgeConsistencyChecker] Total Number of errors : 0
[StaticShapeInferer] SubGraph #0
[StaticShapeInferer] Operand #3, Static, shape : {1 2 2 1}
[StaticShapeInferer] Operand #2, Static, shape : {1 2 2 1}
[StaticShapeInferer] Operand #1, Static, shape : {1 2 2 1}
[StaticShapeInferer] Operand #0, Static, shape : {1 2 2 1}
[Permute] Configure Permute operation
[Permute] Configure Permute operation
[LIR] START SUBGRAPH 0
[LIR] * Permute(Copy)
[LIR]   - Inputs : Input(1)
[LIR]   - Output : Output(3)
[LIR] * Cast
[LIR]   - Inputs : Input(2) 
[LIR]   - Output : Output(1)
[LIR] * Permute(Copy)
[LIR]   - Inputs : Input(0)
[LIR]   - Output : Output(2)
[Linear] Final OpSequence
[Linear] * OP_SEQ {controlflow}   OpSequence IN(0) -> { 1(Permute:0:2) } -> OUT(2)
[Linear] * OP_SEQ {acl_cl}   OpSequence IN(2) -> { 0(Cast:2:1) } -> OUT(1)
[Linear] * OP_SEQ {controlflow}   OpSequence IN(1) -> { 2(Permute:1:3) } -> OUT(3)
[LINEAR] TENSORS as CONSTANT
[LINEAR] TENSORS as MODEL INPUT
[LINEAR] TENSORS
[ALLOC] allocation capacity: 0
[ALLOC] base pointer: 0xebf60
[Execution] Start execution
[Execution] Execution finished
/home/jang/git/github/ragmani/ONE/tests/nnfw_api/src/GenModelTest.h:391: Failure
The difference between refval and val is 49, which exceeds 0.001, where
refval evaluates to 1.4012984643248171e-45,
val evaluates to 49, and
0.001 evaluates to 0.001.
e == 0
/home/jang/git/github/ragmani/ONE/tests/nnfw_api/src/GenModelTest.h:391: Failure
The difference between refval and val is 48, which exceeds 0.001, where
refval evaluates to 0,
val evaluates to 48, and
0.001 evaluates to 0.001.
e == 1
/home/jang/git/github/ragmani/ONE/tests/nnfw_api/src/GenModelTest.h:391: Failure
The difference between refval and val is 48, which exceeds 0.001, where
refval evaluates to 0,
val evaluates to 48, and
0.001 evaluates to 0.001.
e == 2
/home/jang/git/github/ragmani/ONE/tests/nnfw_api/src/GenModelTest.h:391: Failure
The difference between refval and val is 49, which exceeds 0.001, where
refval evaluates to 1.4012984643248171e-45,
val evaluates to 49, and
0.001 evaluates to 0.001.
e == 3
[EdgeConsistencyChecker] Total Number of errors : 0
[Compiler] [Compiler] ==== Compiler Options ====
[Compiler] backend_list             : acl_neon
[Compiler] trace_filepath           : 
[Compiler] graph_dump_level         : 0
[Compiler] op_seq_max_node          : 0
[Compiler] executor                 : Linear
[Compiler] manual_scheduler_options : (Too many things to print)
[Compiler] he_scheduler             : false
[Compiler] he_profiling_mode        : false
[Compiler] disable_compile          : false
[Compiler] fp16_enable              : false
[Compiler] [loadBackend] Successfully loaded 'acl_neon' - libbackend_acl_neon.so
[onert_backend_create] 'acl_neon' loaded
[acl_neon_createTensorManager] AclTensorManager as Linear
[ManualScheduler] Default backend for all ops: acl_neon
[ManualScheduler] backend for operation #0: acl_neon
[Lower] OpSequence#0 is created for NODE#0(Cast)
[OpSequences] dump before permutation insertion
[OpSequences] 0]   OpSequence IN(0) -> { 0(Cast:0:1) } -> OUT(1)
[PassRunner] Start running 'ConstantInsertionPass'
[PassRunner] Finished running 'ConstantInsertionPass'
[PassRunner] Start running 'ConstantLoweringPass'
[PassRunner] Finished running 'ConstantLoweringPass'
[Lower] Operand #0 LowerInfo
  - Shape           : { 1 2 2 1 }
  - Def ir::Operations  : N/A
  - Use ir::Operations  : { 0 }
  - Lower Info
    - Def Backends    : { controlflow(NHWC) }
    - Use Backends    : { acl_neon(NHWC) }
[Lower] Operand #1 LowerInfo
  - Shape           : { 1 2 2 1 }
  - Def ir::Operations  : 0
  - Use ir::Operations  : { }
  - Lower Info
    - Def Backends    : { acl_neon(NHWC) }
    - Use Backends    : { controlflow(NHWC) }
[PassRunner] Start running 'PermutationOperationPass'
[PassRunner] Finished running 'PermutationOperationPass'
[PassRunner] Start running 'PermutationInsertionPass'
[insertPermute] Permute Op inserted, node index : 1
[insertPermute]   - Input (original) Operand : 0
[insertPermute]   - Output(inserted) Operand : 2
[insertPermute] Permute Op inserted, node index : 2
[insertPermute]   - Input (original) Operand : 1
[insertPermute]   - Output(inserted) Operand : 3
[PassRunner] Finished running 'PermutationInsertionPass'
[PassRunner] Start running 'PermutationEliminationPass'
[PassRunner] Finished running 'PermutationEliminationPass'
[OpSequences] Dump after permutation insertion
[OpSequences] 2]   OpSequence IN(1) -> { 2(Permute:1:3) } -> OUT(3)
[OpSequences] 0]   OpSequence IN(2) -> { 0(Cast:2:1) } -> OUT(1)
[OpSequences] 1]   OpSequence IN(0) -> { 1(Permute:0:2) } -> OUT(2)
[EdgeConsistencyChecker] Total Number of errors : 0
[StaticShapeInferer] SubGraph #0
[StaticShapeInferer] Operand #3, Static, shape : {1 2 2 1}
[StaticShapeInferer] Operand #2, Static, shape : {1 2 2 1}
[StaticShapeInferer] Operand #1, Static, shape : {1 2 2 1}
[StaticShapeInferer] Operand #0, Static, shape : {1 2 2 1}
[Permute] Configure Permute operation
[Permute] Configure Permute operation
[LIR] START SUBGRAPH 0
[LIR] * Permute(Copy)
[LIR]   - Inputs : Input(1)
[LIR]   - Output : Output(3)
[LIR] * Cast
[LIR]   - Inputs : Input(2) 
[LIR]   - Output : Output(1)
[LIR] * Permute(Copy)
[LIR]   - Inputs : Input(0)
[LIR]   - Output : Output(2)
[Linear] Final OpSequence
[Linear] * OP_SEQ {controlflow}   OpSequence IN(0) -> { 1(Permute:0:2) } -> OUT(2)
[Linear] * OP_SEQ {acl_neon}   OpSequence IN(2) -> { 0(Cast:2:1) } -> OUT(1)
[Linear] * OP_SEQ {controlflow}   OpSequence IN(1) -> { 2(Permute:1:3) } -> OUT(3)
[LINEAR] TENSORS as CONSTANT
[LINEAR] TENSORS as MODEL INPUT
[LINEAR] TENSORS
[ALLOC] allocation capacity: 0
[ALLOC] base pointer: 0x305970
[Execution] Start execution
[Execution] Execution finished
/home/jang/git/github/ragmani/ONE/tests/nnfw_api/src/GenModelTest.h:391: Failure
The difference between refval and val is 49, which exceeds 0.001, where
refval evaluates to 1.4012984643248171e-45,
val evaluates to 49, and
0.001 evaluates to 0.001.
e == 0
/home/jang/git/github/ragmani/ONE/tests/nnfw_api/src/GenModelTest.h:391: Failure
The difference between refval and val is 48, which exceeds 0.001, where
refval evaluates to 0,
val evaluates to 48, and
0.001 evaluates to 0.001.
e == 1
/home/jang/git/github/ragmani/ONE/tests/nnfw_api/src/GenModelTest.h:391: Failure
The difference between refval and val is 48, which exceeds 0.001, where
refval evaluates to 0,
val evaluates to 48, and
0.001 evaluates to 0.001.
e == 2
/home/jang/git/github/ragmani/ONE/tests/nnfw_api/src/GenModelTest.h:391: Failure
The difference between refval and val is 49, which exceeds 0.001, where
refval evaluates to 1.4012984643248171e-45,
val evaluates to 49, and
0.001 evaluates to 0.001.
e == 3
[EdgeConsistencyChecker] Total Number of errors : 0
[Compiler] [Compiler] ==== Compiler Options ====
[Compiler] backend_list             : cpu
[Compiler] trace_filepath           : 
[Compiler] graph_dump_level         : 0
[Compiler] op_seq_max_node          : 0
[Compiler] executor                 : Linear
[Compiler] manual_scheduler_options : (Too many things to print)
[Compiler] he_scheduler             : false
[Compiler] he_profiling_mode        : false
[Compiler] disable_compile          : false
[Compiler] fp16_enable              : false
[Compiler] [loadBackend] Successfully loaded 'cpu' - libbackend_cpu.so
[onert_backend_create] 'cpu' loaded
[ManualScheduler] Default backend for all ops: cpu
[ManualScheduler] backend for operation #0: cpu
[Lower] OpSequence#0 is created for NODE#0(Cast)
[OpSequences] dump before permutation insertion
[OpSequences] 0]   OpSequence IN(0) -> { 0(Cast:0:1) } -> OUT(1)
[PassRunner] Start running 'ConstantInsertionPass'
[PassRunner] Finished running 'ConstantInsertionPass'
[PassRunner] Start running 'ConstantLoweringPass'
[PassRunner] Finished running 'ConstantLoweringPass'
[Lower] Operand #0 LowerInfo
  - Shape           : { 1 2 2 1 }
  - Def ir::Operations  : N/A
  - Use ir::Operations  : { 0 }
  - Lower Info
    - Def Backends    : { controlflow(NHWC) }
    - Use Backends    : { cpu(NHWC) }
[Lower] Operand #1 LowerInfo
  - Shape           : { 1 2 2 1 }
  - Def ir::Operations  : 0
  - Use ir::Operations  : { }
  - Lower Info
    - Def Backends    : { cpu(NHWC) }
    - Use Backends    : { controlflow(NHWC) }
[PassRunner] Start running 'PermutationOperationPass'
[PassRunner] Finished running 'PermutationOperationPass'
[PassRunner] Start running 'PermutationInsertionPass'
[insertPermute] Permute Op inserted, node index : 1
[insertPermute]   - Input (original) Operand : 0
[insertPermute]   - Output(inserted) Operand : 2
[insertPermute] Permute Op inserted, node index : 2
[insertPermute]   - Input (original) Operand : 1
[insertPermute]   - Output(inserted) Operand : 3
[PassRunner] Finished running 'PermutationInsertionPass'
[PassRunner] Start running 'PermutationEliminationPass'
[removePermute] Permute Op removed, node index : 2
[removePermute]   - Input (removed) ir::Operand : 1
[removePermute]   - Output(kept)    ir::Operand : 3
[removePermute] Permute Op removed, node index : 1
[removePermute]   - Input (kept)    ir::Operand : 0
[removePermute]   - Output(removed) ir::Operand : 2
[PassRunner] Finished running 'PermutationEliminationPass'
[OpSequences] Dump after permutation insertion
[OpSequences] 0]   OpSequence IN(0) -> { 0(Cast:0:3) } -> OUT(3)
[EdgeConsistencyChecker] Total Number of errors : 0
[StaticShapeInferer] SubGraph #0
[StaticShapeInferer] Operand #3, Static, shape : {1 2 2 1}
[StaticShapeInferer] Operand #0, Static, shape : {1 2 2 1}
[LIR] START SUBGRAPH 0
[LIR] * Cast
[LIR]   - Inputs : Input(0) 
[LIR]   - Output : Output(3)
[Linear] Final OpSequence
[Linear] * OP_SEQ {cpu}   OpSequence IN(0) -> { 0(Cast:0:3) } -> OUT(3)
[LINEAR] TENSORS as CONSTANT
[LINEAR] TENSORS as MODEL INPUT
[LINEAR] TENSORS
[ALLOC] allocation capacity: 0
[ALLOC] base pointer: 0x24af30
[ALLOC] allocation capacity: 0
[ALLOC] base pointer: 0x17ba90
[Execution] Start execution
[Execution] Execution finished
/home/jang/git/github/ragmani/ONE/tests/nnfw_api/src/GenModelTest.h:391: Failure
The difference between refval and val is 49, which exceeds 0.001, where
refval evaluates to 1.4012984643248171e-45,
val evaluates to 49, and
0.001 evaluates to 0.001.
e == 0
/home/jang/git/github/ragmani/ONE/tests/nnfw_api/src/GenModelTest.h:391: Failure
The difference between refval and val is 48, which exceeds 0.001, where
refval evaluates to 0,
val evaluates to 48, and
0.001 evaluates to 0.001.
e == 1
/home/jang/git/github/ragmani/ONE/tests/nnfw_api/src/GenModelTest.h:391: Failure
The difference between refval and val is 48, which exceeds 0.001, where
refval evaluates to 0,
val evaluates to 48, and
0.001 evaluates to 0.001.
e == 2
/home/jang/git/github/ragmani/ONE/tests/nnfw_api/src/GenModelTest.h:391: Failure
The difference between refval and val is 49, which exceeds 0.001, where
refval evaluates to 1.4012984643248171e-45,
val evaluates to 49, and
0.001 evaluates to 0.001.
e == 3
[  FAILED  ] GenModelTest.OneOp_Cast_BoolToFloat32 (9474 ms)
[ RUN      ] GenModelTest.OneOp_Cast_AfterEqual
[EdgeConsistencyChecker] Total Number of errors : 0
[Compiler] [Compiler] ==== Compiler Options ====
[Compiler] backend_list             : acl_cl
[Compiler] trace_filepath           : 
[Compiler] graph_dump_level         : 0
[Compiler] op_seq_max_node          : 0
[Compiler] executor                 : Linear
[Compiler] manual_scheduler_options : (Too many things to print)
[Compiler] he_scheduler             : false
[Compiler] he_profiling_mode        : false
[Compiler] disable_compile          : false
[Compiler] fp16_enable              : false
[Compiler] [acl_cl_createTensorManager] AclTensorManager as Linear
[ManualScheduler] Default backend for all ops: acl_cl
[ManualScheduler] backend for operation #1: acl_cl
[ManualScheduler] backend for operation #0: acl_cl
[Lower] OpSequence#0 is created for NODE#1(Cast)
[Lower] OpSequence#0 { acl_cl(NHWC) }  NODE#0 (Comparison) { acl_cl(NHWC) } 
[Lower] OpSequence#0 's NODE#1(Cast) is connected to NODE#0(Comparison)
[Lower] OpSequence#0 merges NODE#0(Comparison)
[OpSequences] dump before permutation insertion
[OpSequences] 0]   OpSequence IN(0,1) -> { 0(Comparison:0,1:2) 1(Cast:2:3) } -> OUT(3)
[PassRunner] Start running 'ConstantInsertionPass'
[PassRunner] Finished running 'ConstantInsertionPass'
[PassRunner] Start running 'ConstantLoweringPass'
[PassRunner] Finished running 'ConstantLoweringPass'
[Lower] Operand #0 LowerInfo
  - Shape           : { 1 2 2 1 }
  - Def ir::Operations  : N/A
  - Use ir::Operations  : { 0 }
  - Lower Info
    - Def Backends    : { controlflow(NHWC) }
    - Use Backends    : { acl_cl(NHWC) }
[Lower] Operand #1 LowerInfo
  - Shape           : { 1 2 2 1 }
  - Def ir::Operations  : N/A
  - Use ir::Operations  : { 0 }
  - Lower Info
    - Def Backends    : { controlflow(NHWC) }
    - Use Backends    : { acl_cl(NHWC) }
[Lower] Operand #2 LowerInfo
  - Shape           : { 1 2 2 1 }
  - Def ir::Operations  : 0
  - Use ir::Operations  : { 1 }
  - Lower Info
    - Def Backends    : { acl_cl(NHWC) }
    - Use Backends    : { acl_cl(NHWC) }
[Lower] Operand #3 LowerInfo
  - Shape           : { 1 2 2 1 }
  - Def ir::Operations  : 1
  - Use ir::Operations  : { }
  - Lower Info
    - Def Backends    : { acl_cl(NHWC) }
    - Use Backends    : { controlflow(NHWC) }
[PassRunner] Start running 'PermutationOperationPass'
[PassRunner] Finished running 'PermutationOperationPass'
[PassRunner] Start running 'PermutationInsertionPass'
[insertPermute] Permute Op inserted, node index : 2
[insertPermute]   - Input (original) Operand : 1
[insertPermute]   - Output(inserted) Operand : 4
[insertPermute] Permute Op inserted, node index : 3
[insertPermute]   - Input (original) Operand : 0
[insertPermute]   - Output(inserted) Operand : 5
[insertPermute] Permute Op inserted, node index : 4
[insertPermute]   - Input (original) Operand : 3
[insertPermute]   - Output(inserted) Operand : 6
[PassRunner] Finished running 'PermutationInsertionPass'
[PassRunner] Start running 'PermutationEliminationPass'
[PassRunner] Finished running 'PermutationEliminationPass'
[OpSequences] Dump after permutation insertion
[OpSequences] 3]   OpSequence IN(3) -> { 4(Permute:3:6) } -> OUT(6)
[OpSequences] 2]   OpSequence IN(0) -> { 3(Permute:0:5) } -> OUT(5)
[OpSequences] 0]   OpSequence IN(5,4) -> { 0(Comparison:5,4:2) 1(Cast:2:3) } -> OUT(3)
[OpSequences] 1]   OpSequence IN(1) -> { 2(Permute:1:4) } -> OUT(4)
[EdgeConsistencyChecker] Total Number of errors : 0
[StaticShapeInferer] SubGraph #0
[StaticShapeInferer] Operand #6, Static, shape : {1 2 2 1}
[StaticShapeInferer] Operand #2, Static, shape : {1 2 2 1}
[StaticShapeInferer] Operand #3, Static, shape : {1 2 2 1}
[StaticShapeInferer] Operand #0, Static, shape : {1 2 2 1}
[StaticShapeInferer] Operand #1, Static, shape : {1 2 2 1}
[StaticShapeInferer] Operand #4, Static, shape : {1 2 2 1}
[StaticShapeInferer] Operand #5, Static, shape : {1 2 2 1}
[Permute] Configure Permute operation
[Permute] Configure Permute operation
[Permute] Configure Permute operation
[LIR] START SUBGRAPH 0
[LIR] * Permute(Copy)
[LIR]   - Inputs : Input(3)
[LIR]   - Output : Output(6)
[LIR] * Permute(Copy)
[LIR]   - Inputs : Input(0)
[LIR]   - Output : Output(5)
[LIR] * Permute(Copy)
[LIR]   - Inputs : Input(1)
[LIR]   - Output : Output(4)
[LIR] * Cast
[LIR]   - Inputs : Input(2) 
[LIR]   - Output : Output(3)
[LIR] * Comparison
[LIR]   - Inputs : Input(5, 5) 
[LIR]   - Output : Output(2)
[Linear] Final OpSequence
[Linear] * OP_SEQ {controlflow}   OpSequence IN(1) -> { 2(Permute:1:4) } -> OUT(4)
[Linear] * OP_SEQ {controlflow}   OpSequence IN(0) -> { 3(Permute:0:5) } -> OUT(5)
[Linear] * OP_SEQ {acl_cl}   OpSequence IN(5,4) -> { 0(Comparison:5,4:2) 1(Cast:2:3) } -> OUT(3)
[Linear] * OP_SEQ {controlflow}   OpSequence IN(3) -> { 4(Permute:3:6) } -> OUT(6)
[LINEAR] TENSORS as CONSTANT
[LINEAR] TENSORS as MODEL INPUT
[LINEAR] TENSORS
[ALLOC] allocation capacity: 0
[ALLOC] base pointer: 0x2422c0
[Execution] Start execution
[Execution] Execution finished
/home/jang/git/github/ragmani/ONE/tests/nnfw_api/src/GenModelTest.h:391: Failure
The difference between refval and val is 254, which exceeds 0.001, where
refval evaluates to 1,
val evaluates to 255, and
0.001 evaluates to 0.001.
e == 1
/home/jang/git/github/ragmani/ONE/tests/nnfw_api/src/GenModelTest.h:391: Failure
The difference between refval and val is 254, which exceeds 0.001, where
refval evaluates to 1,
val evaluates to 255, and
0.001 evaluates to 0.001.
e == 3
[EdgeConsistencyChecker] Total Number of errors : 0
[Compiler] [Compiler] ==== Compiler Options ====
[Compiler] backend_list             : acl_neon
[Compiler] trace_filepath           : 
[Compiler] graph_dump_level         : 0
[Compiler] op_seq_max_node          : 0
[Compiler] executor                 : Linear
[Compiler] manual_scheduler_options : (Too many things to print)
[Compiler] he_scheduler             : false
[Compiler] he_profiling_mode        : false
[Compiler] disable_compile          : false
[Compiler] fp16_enable              : false
[Compiler] [acl_neon_createTensorManager] AclTensorManager as Linear
[ManualScheduler] Default backend for all ops: acl_neon
[ManualScheduler] backend for operation #1: acl_neon
[ManualScheduler] backend for operation #0: acl_neon
[Lower] OpSequence#0 is created for NODE#1(Cast)
[Lower] OpSequence#0 { acl_neon(NHWC) }  NODE#0 (Comparison) { acl_neon(NHWC) } 
[Lower] OpSequence#0 's NODE#1(Cast) is connected to NODE#0(Comparison)
[Lower] OpSequence#0 merges NODE#0(Comparison)
[OpSequences] dump before permutation insertion
[OpSequences] 0]   OpSequence IN(0,1) -> { 0(Comparison:0,1:2) 1(Cast:2:3) } -> OUT(3)
[PassRunner] Start running 'ConstantInsertionPass'
[PassRunner] Finished running 'ConstantInsertionPass'
[PassRunner] Start running 'ConstantLoweringPass'
[PassRunner] Finished running 'ConstantLoweringPass'
[Lower] Operand #0 LowerInfo
  - Shape           : { 1 2 2 1 }
  - Def ir::Operations  : N/A
  - Use ir::Operations  : { 0 }
  - Lower Info
    - Def Backends    : { controlflow(NHWC) }
    - Use Backends    : { acl_neon(NHWC) }
[Lower] Operand #1 LowerInfo
  - Shape           : { 1 2 2 1 }
  - Def ir::Operations  : N/A
  - Use ir::Operations  : { 0 }
  - Lower Info
    - Def Backends    : { controlflow(NHWC) }
    - Use Backends    : { acl_neon(NHWC) }
[Lower] Operand #2 LowerInfo
  - Shape           : { 1 2 2 1 }
  - Def ir::Operations  : 0
  - Use ir::Operations  : { 1 }
  - Lower Info
    - Def Backends    : { acl_neon(NHWC) }
    - Use Backends    : { acl_neon(NHWC) }
[Lower] Operand #3 LowerInfo
  - Shape           : { 1 2 2 1 }
  - Def ir::Operations  : 1
  - Use ir::Operations  : { }
  - Lower Info
    - Def Backends    : { acl_neon(NHWC) }
    - Use Backends    : { controlflow(NHWC) }
[PassRunner] Start running 'PermutationOperationPass'
[PassRunner] Finished running 'PermutationOperationPass'
[PassRunner] Start running 'PermutationInsertionPass'
[insertPermute] Permute Op inserted, node index : 2
[insertPermute]   - Input (original) Operand : 1
[insertPermute]   - Output(inserted) Operand : 4
[insertPermute] Permute Op inserted, node index : 3
[insertPermute]   - Input (original) Operand : 0
[insertPermute]   - Output(inserted) Operand : 5
[insertPermute] Permute Op inserted, node index : 4
[insertPermute]   - Input (original) Operand : 3
[insertPermute]   - Output(inserted) Operand : 6
[PassRunner] Finished running 'PermutationInsertionPass'
[PassRunner] Start running 'PermutationEliminationPass'
[PassRunner] Finished running 'PermutationEliminationPass'
[OpSequences] Dump after permutation insertion
[OpSequences] 3]   OpSequence IN(3) -> { 4(Permute:3:6) } -> OUT(6)
[OpSequences] 2]   OpSequence IN(0) -> { 3(Permute:0:5) } -> OUT(5)
[OpSequences] 0]   OpSequence IN(5,4) -> { 0(Comparison:5,4:2) 1(Cast:2:3) } -> OUT(3)
[OpSequences] 1]   OpSequence IN(1) -> { 2(Permute:1:4) } -> OUT(4)
[EdgeConsistencyChecker] Total Number of errors : 0
[StaticShapeInferer] SubGraph #0
[StaticShapeInferer] Operand #6, Static, shape : {1 2 2 1}
[StaticShapeInferer] Operand #2, Static, shape : {1 2 2 1}
[StaticShapeInferer] Operand #3, Static, shape : {1 2 2 1}
[StaticShapeInferer] Operand #0, Static, shape : {1 2 2 1}
[StaticShapeInferer] Operand #1, Static, shape : {1 2 2 1}
[StaticShapeInferer] Operand #4, Static, shape : {1 2 2 1}
[StaticShapeInferer] Operand #5, Static, shape : {1 2 2 1}
[Permute] Configure Permute operation
[Permute] Configure Permute operation
[Permute] Configure Permute operation
[LIR] START SUBGRAPH 0
[LIR] * Permute(Copy)
[LIR]   - Inputs : Input(3)
[LIR]   - Output : Output(6)
[LIR] * Permute(Copy)
[LIR]   - Inputs : Input(0)
[LIR]   - Output : Output(5)
[LIR] * Permute(Copy)
[LIR]   - Inputs : Input(1)
[LIR]   - Output : Output(4)
[LIR] * Cast
[LIR]   - Inputs : Input(2) 
[LIR]   - Output : Output(3)
[LIR] * Comparison
[LIR]   - Inputs : Input(5, 5) 
[LIR]   - Output : Output(2)
[Linear] Final OpSequence
[Linear] * OP_SEQ {controlflow}   OpSequence IN(1) -> { 2(Permute:1:4) } -> OUT(4)
[Linear] * OP_SEQ {controlflow}   OpSequence IN(0) -> { 3(Permute:0:5) } -> OUT(5)
[Linear] * OP_SEQ {acl_neon}   OpSequence IN(5,4) -> { 0(Comparison:5,4:2) 1(Cast:2:3) } -> OUT(3)
[Linear] * OP_SEQ {controlflow}   OpSequence IN(3) -> { 4(Permute:3:6) } -> OUT(6)
[LINEAR] TENSORS as CONSTANT
[LINEAR] TENSORS as MODEL INPUT
[LINEAR] TENSORS
[ALLOC] allocation capacity: 0
[ALLOC] base pointer: 0x307078
[Execution] Start execution
[Execution] Execution finished
/home/jang/git/github/ragmani/ONE/tests/nnfw_api/src/GenModelTest.h:391: Failure
The difference between refval and val is 254, which exceeds 0.001, where
refval evaluates to 1,
val evaluates to 255, and
0.001 evaluates to 0.001.
e == 1
/home/jang/git/github/ragmani/ONE/tests/nnfw_api/src/GenModelTest.h:391: Failure
The difference between refval and val is 254, which exceeds 0.001, where
refval evaluates to 1,
val evaluates to 255, and
0.001 evaluates to 0.001.
e == 3
[EdgeConsistencyChecker] Total Number of errors : 0
[Compiler] [Compiler] ==== Compiler Options ====
[Compiler] backend_list             : cpu
[Compiler] trace_filepath           : 
[Compiler] graph_dump_level         : 0
[Compiler] op_seq_max_node          : 0
[Compiler] executor                 : Linear
[Compiler] manual_scheduler_options : (Too many things to print)
[Compiler] he_scheduler             : false
[Compiler] he_profiling_mode        : false
[Compiler] disable_compile          : false
[Compiler] fp16_enable              : false
[Compiler] [ManualScheduler] Default backend for all ops: cpu
[ManualScheduler] backend for operation #1: cpu
[ManualScheduler] backend for operation #0: cpu
[Lower] OpSequence#0 is created for NODE#1(Cast)
[Lower] OpSequence#0 { cpu(NHWC) }  NODE#0 (Comparison) { cpu(NHWC) } 
[Lower] OpSequence#0 's NODE#1(Cast) is connected to NODE#0(Comparison)
[Lower] OpSequence#0 merges NODE#0(Comparison)
[OpSequences] dump before permutation insertion
[OpSequences] 0]   OpSequence IN(0,1) -> { 0(Comparison:0,1:2) 1(Cast:2:3) } -> OUT(3)
[PassRunner] Start running 'ConstantInsertionPass'
[PassRunner] Finished running 'ConstantInsertionPass'
[PassRunner] Start running 'ConstantLoweringPass'
[PassRunner] Finished running 'ConstantLoweringPass'
[Lower] Operand #0 LowerInfo
  - Shape           : { 1 2 2 1 }
  - Def ir::Operations  : N/A
  - Use ir::Operations  : { 0 }
  - Lower Info
    - Def Backends    : { controlflow(NHWC) }
    - Use Backends    : { cpu(NHWC) }
[Lower] Operand #1 LowerInfo
  - Shape           : { 1 2 2 1 }
  - Def ir::Operations  : N/A
  - Use ir::Operations  : { 0 }
  - Lower Info
    - Def Backends    : { controlflow(NHWC) }
    - Use Backends    : { cpu(NHWC) }
[Lower] Operand #2 LowerInfo
  - Shape           : { 1 2 2 1 }
  - Def ir::Operations  : 0
  - Use ir::Operations  : { 1 }
  - Lower Info
    - Def Backends    : { cpu(NHWC) }
    - Use Backends    : { cpu(NHWC) }
[Lower] Operand #3 LowerInfo
  - Shape           : { 1 2 2 1 }
  - Def ir::Operations  : 1
  - Use ir::Operations  : { }
  - Lower Info
    - Def Backends    : { cpu(NHWC) }
    - Use Backends    : { controlflow(NHWC) }
[PassRunner] Start running 'PermutationOperationPass'
[PassRunner] Finished running 'PermutationOperationPass'
[PassRunner] Start running 'PermutationInsertionPass'
[insertPermute] Permute Op inserted, node index : 2
[insertPermute]   - Input (original) Operand : 1
[insertPermute]   - Output(inserted) Operand : 4
[insertPermute] Permute Op inserted, node index : 3
[insertPermute]   - Input (original) Operand : 0
[insertPermute]   - Output(inserted) Operand : 5
[insertPermute] Permute Op inserted, node index : 4
[insertPermute]   - Input (original) Operand : 3
[insertPermute]   - Output(inserted) Operand : 6
[PassRunner] Finished running 'PermutationInsertionPass'
[PassRunner] Start running 'PermutationEliminationPass'
[removePermute] Permute Op removed, node index : 4
[removePermute]   - Input (removed) ir::Operand : 3
[removePermute]   - Output(kept)    ir::Operand : 6
[removePermute] Permute Op removed, node index : 3
[removePermute]   - Input (kept)    ir::Operand : 0
[removePermute]   - Output(removed) ir::Operand : 5
[removePermute] Permute Op removed, node index : 2
[removePermute]   - Input (kept)    ir::Operand : 1
[removePermute]   - Output(removed) ir::Operand : 4
[PassRunner] Finished running 'PermutationEliminationPass'
[OpSequences] Dump after permutation insertion
[OpSequences] 0]   OpSequence IN(0,1) -> { 0(Comparison:0,1:2) 1(Cast:2:6) } -> OUT(6)
[EdgeConsistencyChecker] Total Number of errors : 0
[StaticShapeInferer] SubGraph #0
[StaticShapeInferer] Operand #6, Static, shape : {1 2 2 1}
[StaticShapeInferer] Operand #2, Static, shape : {1 2 2 1}
[StaticShapeInferer] Operand #0, Static, shape : {1 2 2 1}
[StaticShapeInferer] Operand #1, Static, shape : {1 2 2 1}
[LIR] START SUBGRAPH 0
[LIR] * Cast
[LIR]   - Inputs : Input(2) 
[LIR]   - Output : Output(6)
[LIR] * Comparison
[LIR]   - Inputs : Input(0, 0) 
[LIR]   - Output : Output(2)
[Linear] Final OpSequence
[Linear] * OP_SEQ {cpu}   OpSequence IN(0,1) -> { 0(Comparison:0,1:2) 1(Cast:2:6) } -> OUT(6)
[LINEAR] TENSORS as CONSTANT
[LINEAR] TENSORS as MODEL INPUT
[LINEAR] TENSORS
[WIC_PLANNER] claim(#2): [4sz]
[WIC_PLANNER] release(#2)
[ALLOC] allocation capacity: 0
[ALLOC] base pointer: 0x431098
[WIC_PLANNER] build_plan(#2): [4sz]
[WIC_PLANNER] alloc(#2): [+0, 4sz]
[ALLOC] allocation capacity: 4
[ALLOC] base pointer: 0x305120
[CPU_StaticTensorManager] TENSOR(#2): 0x305120
[Execution] Start execution
[Execution] Execution finished
[  FAILED  ] GenModelTest.OneOp_Cast_AfterEqual (63 ms)
[----------] 2 tests from GenModelTest (9537 ms total)

[----------] Global test environment tear-down
[==========] 2 tests from 1 test case ran. (9537 ms total)
[  PASSED  ] 0 tests.
[  FAILED  ] 2 tests, listed below:
[  FAILED  ] GenModelTest.OneOp_Cast_BoolToFloat32
[  FAILED  ] GenModelTest.OneOp_Cast_AfterEqual

 2 FAILED TESTS
[onert_backend_create] 'cpu' unloaded
[onert_backend_create] 'acl_neon' unloaded
[onert_backend_create] 'acl_cl' unloaded
```

</details>
