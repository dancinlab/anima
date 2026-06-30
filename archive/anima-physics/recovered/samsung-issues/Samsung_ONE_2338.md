https://github.com/Samsung/ONE/issues/2338
# [onert] segmentation fault during nnfw_close_session()

For model below,
<sub> _it is a part of tiny model_ </sub>

![image](https://user-images.githubusercontent.com/12553213/84840426-7265e300-b07a-11ea-8899-a8b4ecb6881f.png)

onert got segmentation fault during `nnfw_close_session()`.

I've run on `x86_64` with c1aaf15.

```
$ Product/x86_64-linux.debug/out/bin/nnpackage_run --nnpackage d2-5/
... warmup 1 takes 0.308 ms
... run 1 takes 0.069 ms
Segmentation fault (core dumped)
```

This model has no problem with `tflite_run`.

nnpackage with golden data: [d2-5.tar.gz](https://github.com/Samsung/ONE/files/4789672/d2-5.tar.gz)

#### call stack

```
#0  __GI___libc_free (mem=0x40c63c9bc01cca5b) at malloc.c:2951
...
#5  0x00007ffff7b7befb in std::vector<int, std::allocator<int> >::~vector (this=0x6bac58, __in_chrg=<optimized out>) at /usr/include/c++/9/bits/stl_vector.h:680
#6  0x00007ffff3b522c4 in nnfw::cker::FCTempArena::~FCTempArena (this=0x6bac20, __in_chrg=<optimized out>) at /home/brian/z/ONE/compute/cker/include/cker/operation/FullyConnected.h:31
...
#18 0x00007ffff55da918 in onert::exec::FunctionSequence::~FunctionSequence (this=0x6b9480, __in_chrg=<optimized out>) at /home/brian/z/ONE/runtime/onert/core/include/exec/FunctionSequence.h:52
...
#23 0x00007ffff55449c6 in onert::compiler::CodeAndInfo::~CodeAndInfo (this=0x6b4f00, __in_chrg=<optimized out>) at /home/brian/z/ONE/runtime/onert/core/include/compiler/CodeMap.h:27
...
#52 0x00007ffff7b755c7 in nnfw_close_session (session=0x6b24e0) at /home/brian/z/ONE/runtime/onert/api/src/nnfw_api.cc:68
```

<details> <summary> full call stack </summary>

```
#0  __GI___libc_free (mem=0x40c63c9bc01cca5b) at malloc.c:2951
#1  0x00007ffff7b80364 in __gnu_cxx::new_allocator<int>::deallocate (this=0x6bac58, __p=0x40c63c9bc01cca5b) at /usr/include/c++/9/ext/new_allocator.h:128
#2  0x00007ffff7b7ee3c in std::allocator_traits<std::allocator<int> >::deallocate (__a=..., __p=0x40c63c9bc01cca5b, __n=2676019642441686) at /usr/include/c++/9/bits/alloc_traits.h:470
#3  0x00007ffff7b7d908 in std::_Vector_base<int, std::allocator<int> >::_M_deallocate (this=0x6bac58, __p=0x40c63c9bc01cca5b, __n=2676019642441686) at /usr/include/c++/9/bits/stl_vector.h:351
#4  0x00007ffff7b7d5d2 in std::_Vector_base<int, std::allocator<int> >::~_Vector_base (this=0x6bac58, __in_chrg=<optimized out>) at /usr/include/c++/9/bits/stl_vector.h:332
#5  0x00007ffff7b7befb in std::vector<int, std::allocator<int> >::~vector (this=0x6bac58, __in_chrg=<optimized out>) at /usr/include/c++/9/bits/stl_vector.h:680
#6  0x00007ffff3b522c4 in nnfw::cker::FCTempArena::~FCTempArena (this=0x6bac20, __in_chrg=<optimized out>) at /home/brian/z/ONE/compute/cker/include/cker/operation/FullyConnected.h:31
#7  0x00007ffff3b5230a in std::default_delete<nnfw::cker::FCTempArena>::operator() (this=0x6b7440, __ptr=0x6bac20) at /usr/include/c++/9/bits/unique_ptr.h:81
#8  0x00007ffff3b51ccc in std::unique_ptr<nnfw::cker::FCTempArena, std::default_delete<nnfw::cker::FCTempArena> >::~unique_ptr (this=0x6b7440, __in_chrg=<optimized out>) at /usr/include/c++/9/bits/unique_ptr.h:292
#9  0x00007ffff3b50224 in onert::backend::cpu::ops::FullyConnectedLayer::~FullyConnectedLayer (this=0x6b7410, __in_chrg=<optimized out>) at /home/brian/z/ONE/runtime/onert/backend/cpu/ops/FullyConnectedLayer.h:42
#10 0x00007ffff3b5024c in onert::backend::cpu::ops::FullyConnectedLayer::~FullyConnectedLayer (this=0x6b7410, __in_chrg=<optimized out>) at /home/brian/z/ONE/runtime/onert/backend/cpu/ops/FullyConnectedLayer.h:42
#11 0x00007ffff54e3fb4 in std::default_delete<onert::exec::IFunction>::operator() (this=0x6b6dc0, __ptr=0x6b7410) at /usr/include/c++/9/bits/unique_ptr.h:81
#12 0x00007ffff54dd1ea in std::unique_ptr<onert::exec::IFunction, std::default_delete<onert::exec::IFunction> >::~unique_ptr (this=0x6b6dc0, __in_chrg=<optimized out>) at /usr/include/c++/9/bits/unique_ptr.h:292
#13 0x00007ffff55db4ab in std::_Destroy<std::unique_ptr<onert::exec::IFunction, std::default_delete<onert::exec::IFunction> > > (__pointer=0x6b6dc0) at /usr/include/c++/9/bits/stl_construct.h:98
#14 0x00007ffff55db193 in std::_Destroy_aux<false>::__destroy<std::unique_ptr<onert::exec::IFunction, std::default_delete<onert::exec::IFunction> >*> (__first=0x6b6dc0, __last=0x6b6dc8) at /usr/include/c++/9/bits/stl_construct.h:108
#15 0x00007ffff55dad80 in std::_Destroy<std::unique_ptr<onert::exec::IFunction, std::default_delete<onert::exec::IFunction> >*> (__first=0x6b6dc0, __last=0x6b6dc8) at /usr/include/c++/9/bits/stl_construct.h:137
#16 0x00007ffff55dabf7 in std::_Destroy<std::unique_ptr<onert::exec::IFunction, std::default_delete<onert::exec::IFunction> >*, std::unique_ptr<onert::exec::IFunction, std::default_delete<onert::exec::IFunction> > > (__first=0x6b6dc0, 
    __last=0x6b6dc8) at /usr/include/c++/9/bits/stl_construct.h:206
#17 0x00007ffff55da9a5 in std::vector<std::unique_ptr<onert::exec::IFunction, std::default_delete<onert::exec::IFunction> >, std::allocator<std::unique_ptr<onert::exec::IFunction, std::default_delete<onert::exec::IFunction> > > >::~vector (this=0x6b9488, __in_chrg=<optimized out>) at /usr/include/c++/9/bits/stl_vector.h:677
#18 0x00007ffff55da918 in onert::exec::FunctionSequence::~FunctionSequence (this=0x6b9480, __in_chrg=<optimized out>) at /home/brian/z/ONE/runtime/onert/core/include/exec/FunctionSequence.h:52
#19 0x00007ffff55dbaaa in onert::exec::FunctionSequenceForDynamicBackend::~FunctionSequenceForDynamicBackend (this=0x6b9480, __in_chrg=<optimized out>) at /home/brian/z/ONE/runtime/onert/core/include/exec/FunctionSequence.h:82
#20 0x00007ffff55dbac6 in onert::exec::FunctionSequenceForDynamicBackend::~FunctionSequenceForDynamicBackend (this=0x6b9480, __in_chrg=<optimized out>) at /home/brian/z/ONE/runtime/onert/core/include/exec/FunctionSequence.h:82
#21 0x00007ffff54e4066 in std::default_delete<onert::exec::FunctionSequence>::operator() (this=0x6b4f10, __ptr=0x6b9480) at /usr/include/c++/9/bits/unique_ptr.h:81
#22 0x00007ffff54dd250 in std::unique_ptr<onert::exec::FunctionSequence, std::default_delete<onert::exec::FunctionSequence> >::~unique_ptr (this=0x6b4f10, __in_chrg=<optimized out>) at /usr/include/c++/9/bits/unique_ptr.h:292
#23 0x00007ffff55449c6 in onert::compiler::CodeAndInfo::~CodeAndInfo (this=0x6b4f00, __in_chrg=<optimized out>) at /home/brian/z/ONE/runtime/onert/core/include/compiler/CodeMap.h:27
#24 0x00007ffff554f4ef in std::_Destroy<onert::compiler::CodeAndInfo> (__pointer=0x6b4f00) at /usr/include/c++/9/bits/stl_construct.h:98
#25 0x00007ffff554cb1d in std::_Destroy_aux<false>::__destroy<onert::compiler::CodeAndInfo*> (__first=0x6b4f00, __last=0x6b4f60) at /usr/include/c++/9/bits/stl_construct.h:108
#26 0x00007ffff5549d3c in std::_Destroy<onert::compiler::CodeAndInfo*> (__first=0x6b4f00, __last=0x6b4f60) at /usr/include/c++/9/bits/stl_construct.h:137
#27 0x00007ffff5547027 in std::_Destroy<onert::compiler::CodeAndInfo*, onert::compiler::CodeAndInfo> (__first=0x6b4f00, __last=0x6b4f60) at /usr/include/c++/9/bits/stl_construct.h:206
#28 0x00007ffff5545173 in std::vector<onert::compiler::CodeAndInfo, std::allocator<onert::compiler::CodeAndInfo> >::~vector (this=0x6b8f90, __in_chrg=<optimized out>) at /usr/include/c++/9/bits/stl_vector.h:677
#29 0x00007ffff55ddb02 in onert::exec::LinearExecutor::~LinearExecutor (this=0x6b8e50, __in_chrg=<optimized out>) at /home/brian/z/ONE/runtime/onert/core/src/exec/LinearExecutor.h:40
#30 0x00007ffff55ddb2a in onert::exec::LinearExecutor::~LinearExecutor (this=0x6b8e50, __in_chrg=<optimized out>) at /home/brian/z/ONE/runtime/onert/core/src/exec/LinearExecutor.h:40
#31 0x00007ffff552f652 in std::default_delete<onert::exec::IExecutor>::operator() (this=0x6b7080, __ptr=0x6b8e50) at /usr/include/c++/9/bits/unique_ptr.h:81
#32 0x00007ffff552cd7c in std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> >::~unique_ptr (this=0x6b7080, __in_chrg=<optimized out>) at /usr/include/c++/9/bits/unique_ptr.h:292
#33 0x00007ffff5539002 in std::pair<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> const, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> > >::~pair (this=0x6b7078, 
    __in_chrg=<optimized out>) at /usr/include/c++/9/bits/stl_pair.h:208
#34 0x00007ffff5539022 in __gnu_cxx::new_allocator<std::__detail::_Hash_node<std::pair<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> const, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> > >, false> >::destroy<std::pair<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> const, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> > > > (this=0x6b6e30, __p=0x6b7078)
    at /usr/include/c++/9/ext/new_allocator.h:153
#35 0x00007ffff553703c in std::allocator_traits<std::allocator<std::__detail::_Hash_node<std::pair<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> const, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> > >, false> > >::destroy<std::pair<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> const, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> > > > (__a=..., __p=0x6b7078)
    at /usr/include/c++/9/bits/alloc_traits.h:497
#36 0x00007ffff553480d in std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> const, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> > >, false> > >::_M_deallocate_node (this=0x6b6e30, __n=0x6b7070) at /usr/include/c++/9/bits/hashtable_policy.h:2102
#37 0x00007ffff553c1d4 in std::__detail::_Hashtable_alloc<std::allocator<std::__detail::_Hash_node<std::pair<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> const, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> > >, false> > >::_M_deallocate_nodes (this=0x6b6e30, __n=0x0) at /usr/include/c++/9/bits/hashtable_policy.h:2124
#38 0x00007ffff553bea8 in std::_Hashtable<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag>, std::pair<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> const, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> > >, std::allocator<std::pair<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> const, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> > > >, std::__detail::_Select1st, std::equal_to<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> >, std::hash<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> >, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true> >::clear (this=0x6b6e30) at /usr/include/c++/9/bits/hashtable.h:2028
#39 0x00007ffff553b90e in std::_Hashtable<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag>, std::pair<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> const, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> > >, std::allocator<std::pair<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> const, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> > > >, std::__detail::_Select1st, std::equal_to<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> >, std::hash<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> >, std::__detail::_Mod_range_hashing, std::__detail::_Default_ranged_hash, std::__detail::_Prime_rehash_policy, std::__detail::_Hashtable_traits<false, false, true> >::~_Hashtable (this=0x6b6e30, __in_chrg=<optimized out>) at /usr/include/c++/9/bits/hashtable.h:1352
#40 0x00007ffff553ca46 in std::unordered_map<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag>, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> >, std::hash<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> >, std::equal_to<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> >, std::allocator<std::pair<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> const, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> > > > >::~unordered_map (this=0x6b6e30, __in_chrg=<optimized out>) at /usr/include/c++/9/bits/unordered_map.h:102
#41 0x00007ffff553ca66 in __gnu_cxx::new_allocator<std::unordered_map<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag>, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> >, std::hash<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> >, std::equal_to<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> >, std::allocator<std::pair<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> const, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> > > > > >::destroy<std::unordered_map<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag>, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> >, std::hash<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> >, std::equal_to<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> >, std::allocator<std::pair<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> const, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> > > > > > (this=0x6b6e30, __p=0x6b6e30) at /usr/include/c++/9/ext/new_allocator.h:153
#42 0x00007ffff553ca1d in std::allocator_traits<std::allocator<std::unordered_map<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag>, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> >, std::hash<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> >, std::equal_to<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> >, std::allocator<std::pair<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> con--Type <RET> for more, q to quit, c to continue without paging--
st, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> > > > > > >::destroy<std::unordered_map<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag>, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> >, std::hash<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> >, std::equal_to<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> >, std::allocator<std::pair<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> const, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> > > > > > (__a=..., __p=0x6b6e30) at /usr/include/c++/9/bits/alloc_traits.h:497
#43 0x00007ffff553c8e5 in std::_Sp_counted_ptr_inplace<std::unordered_map<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag>, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> >, std::hash<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> >, std::equal_to<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> >, std::allocator<std::pair<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> const, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> > > > >, std::allocator<std::unordered_map<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag>, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> >, std::hash<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> >, std::equal_to<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> >, std::allocator<std::pair<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> const, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> > > > > >, (__gnu_cxx::_Lock_policy)2>::_M_dispose (this=0x6b6e20)
    at /usr/include/c++/9/bits/shared_ptr_base.h:557
#44 0x00007ffff7b7305e in std::_Sp_counted_base<(__gnu_cxx::_Lock_policy)2>::_M_release (this=0x6b6e20) at /usr/include/c++/9/bits/shared_ptr_base.h:155
#45 0x00007ffff7b72bb7 in std::__shared_count<(__gnu_cxx::_Lock_policy)2>::~__shared_count (this=0x6b2858, __in_chrg=<optimized out>) at /usr/include/c++/9/bits/shared_ptr_base.h:730
#46 0x00007ffff7b7a120 in std::__shared_ptr<std::unordered_map<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag>, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> >, std::hash<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> >, std::equal_to<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> >, std::allocator<std::pair<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> const, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> > > > >, (__gnu_cxx::_Lock_policy)2>::~__shared_ptr (this=0x6b2850, __in_chrg=<optimized out>) at /usr/include/c++/9/bits/shared_ptr_base.h:1169
#47 0x00007ffff7b7a152 in std::shared_ptr<std::unordered_map<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag>, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> >, std::hash<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> >, std::equal_to<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> >, std::allocator<std::pair<onert::util::Index<unsigned int, onert::ir::SubgraphIndexTag> const, std::unique_ptr<onert::exec::IExecutor, std::default_delete<onert::exec::IExecutor> > > > > >::~shared_ptr (this=0x6b2850, __in_chrg=<optimized out>) at /usr/include/c++/9/bits/shared_ptr.h:103
#48 0x00007ffff7b7e19e in onert::compiler::Compiler::~Compiler (this=0x6b2840, __in_chrg=<optimized out>) at /home/brian/z/ONE/runtime/onert/core/include/compiler/Compiler.h:69
#49 0x00007ffff7b7e1d0 in std::default_delete<onert::compiler::Compiler>::operator() (this=0x6b24f8, __ptr=0x6b2840) at /usr/include/c++/9/bits/unique_ptr.h:81
#50 0x00007ffff7b7ca62 in std::unique_ptr<onert::compiler::Compiler, std::default_delete<onert::compiler::Compiler> >::~unique_ptr (this=0x6b24f8, __in_chrg=<optimized out>) at /usr/include/c++/9/bits/unique_ptr.h:292
#51 0x00007ffff7b75bfe in nnfw_session::~nnfw_session (this=0x6b24e0, __in_chrg=<optimized out>) at /home/brian/z/ONE/runtime/onert/api/src/nnfw_api_internal.h:52
#52 0x00007ffff7b755c7 in nnfw_close_session (session=0x6b24e0) at /home/brian/z/ONE/runtime/onert/api/src/nnfw_api.cc:68
#53 0x0000000000424360 in main (argc=3, argv=0x7fffffffdd98) at /home/brian/z/ONE/tests/tools/nnpackage_run/src/nnpackage_run.cc:237
```
<details>
