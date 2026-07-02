# H_6170 (attention-capacity terminal) ckpt manifest
## base ByteGPT (frozen h1129c 303M, d1024 L24 H16 block512)
base_pt_sha256(aiden ~/g6_h6165/h1129c_chat.pt) = 4fcc2d6c9b3164f478139ffb148f484465b42fc339d630956e4ea0f90ec13f68
base_bin_sha256(serialize, byte-identical aiden==summer) = 5c303f026f134e4bc4faf516ef5298bd26269e19693696a73a5058e6ffa5319e
## injected BindAttn stacks (N=2 blocks, 25.2M trained params, 600 steps, base frozen)
inj_REGon_N2_s7.pt  sha256 = bca40ff12487329dfffb020bdf600ba751575372da16261169cf6136a7e706ba  gates=[-0.013521, 0.013131]
inj_REGoff_N2_s7.pt sha256 = 40b96253a53e00cfb3bf6ceb716957ba1be2c346efe96e15b371398f5ead8e39  gates=[-0.013286, 0.013154]
