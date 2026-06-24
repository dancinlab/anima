# Torch-FREE loader for a torch .pt zip (pickle + raw storages, handles bf16/fp16/fp32) -> {key: np.float32}. No torch import. Built 2026-06-24 for the H_1579 serialize reference-match (proves serializer byte-faithful).
# Provenance: anima H_1579 clm303 root-cause (overfit, NOT serialize defect).
#   See UNIVERSE/cards/H_1579_clm303_serialization_defect.md + CORRECTION_overfit_not_serialize.md.
#   Torch-free (no torch import) — runs on any host with numpy.

# Torch-free loader for a torch .pt zip: returns {key: np.ndarray(float32)} + shapes.
import zipfile, pickle, struct, numpy as np

class _Unpickler(pickle.Unpickler):
    def __init__(self, f, zf, root):
        super().__init__(f)
        self.zf=zf; self.root=root; self.storages={}
    def persistent_load(self, pid):
        # pid = ('storage', storage_type, key, location, numel)
        typ=pid[0]; assert typ=='storage'
        storage_type=pid[1]; key=pid[2]; numel=pid[4]
        return ('STORAGE', storage_type, key, numel)
    def find_class(self, module, name):
        # torch dtype storage classes -> sentinel strings
        if module.startswith('torch'):
            return ('TORCHCLS', module, name)
        return super().find_class(module, name)

# We don't fully reconstruct via reduce; instead parse data.pkl ourselves by
# walking the BINPERSID order which (in torch save) matches key insertion order.
import pickletools, io
def load_pt(path):
    zf=zipfile.ZipFile(path)
    names=zf.namelist()
    root=names[0].split('/')[0]
    pkl=zf.read(f'{root}/data.pkl')
    # parse: ordered (key, storage_idx, dtype) by scanning opcodes
    # also need dtype + shape: those are in REDUCE args. Simpler: emulate via
    # a minimal unpickler capturing the rebuild_tensor_v2 calls.
    captured=[]
    class U(pickle.Unpickler):
        def persistent_load(self, pid):
            return {'storage_key':pid[2],'storage_type':str(pid[1]),'numel':pid[4]}
        def find_class(self, mod, nm):
            if nm=='_rebuild_tensor_v2':
                def rebuild(storage, storage_offset, size, stride, requires_grad=False, backward_hooks=None, metadata=None):
                    return {'st':storage,'off':storage_offset,'size':tuple(size),'stride':tuple(stride)}
                return rebuild
            if nm=='OrderedDict':
                from collections import OrderedDict; return OrderedDict
            class _Stub: pass
            return _Stub
    sd=U(io.BytesIO(pkl)).load()
    # dtype map from storage_type string
    def dtype_of(stype):
        s=stype.lower()
        if 'bfloat16' in s: return ('bf16',2)
        if 'half' in s or 'float16' in s: return ('f2',2)
        if 'float' in s or 'double' not in s and 'float32' in s: return ('f4',4)
        if 'double' in s: return ('f8',8)
        return ('f4',4)
    out={}
    for k,v in sd.items():
        st=v['st']; size=v['size']
        skey=st['storage_key']; stype=st['storage_type']
        raw=zf.read(f'{root}/data/{skey}')
        dt,sz=dtype_of(stype)
        numel=int(np.prod(size)) if size else 1
        if dt=='bf16':
            u16=np.frombuffer(raw, dtype='<u2', count=numel)
            u32=(u16.astype(np.uint32)<<16)
            arr=u32.view(np.float32).astype(np.float32)
        elif dt=='f2':
            arr=np.frombuffer(raw,dtype='<f2',count=numel).astype(np.float32)
        elif dt=='f8':
            arr=np.frombuffer(raw,dtype='<f8',count=numel).astype(np.float32)
        else:
            arr=np.frombuffer(raw,dtype='<f4',count=numel).astype(np.float32)
        out[k]=arr.reshape(size)
    return out

if __name__=='__main__':
    import sys
    sd=load_pt(sys.argv[1])
    for k,v in sd.items():
        print(f"{k:38} {str(v.shape):22} dt-in absmean={np.abs(v).mean():.5f} std={v.std():.5f}")
