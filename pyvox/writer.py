from struct import pack

from pyvox.models import Vox


class VoxWriter(object):

    def __init__(self, filename, vox: Vox):
        self.filename = filename
        self.vox: Vox = vox

    def _chunk(self, id, content, chunks=[]):

        res = b''
        for c in chunks:
            res += self._chunk(*c)

        return pack('4sii', id, len(content), len(res)) + content + res

    def _matflags(self, props):
        flags = 0
        res = b''
        for b, field in [(0, 'plastic'),
                         (1, 'roughness'),
                         (2, 'specular'),
                         (3, 'IOR'),
                         (4, 'attenuation'),
                         (5, 'power'),
                         (6, 'glow'),
                         (7, 'isTotalPower')]:
            if field in props:
                flags |= 1 << b
                try:
                    res += pack('f', props[field])
                except Exception as exc:
                    print(f"Bad prop content: {props[field]} ({type(props[field])}) expected float.")
                    raise exc

        return pack('i', flags) + res

    def write(self):

        res = self.to_bytes()

        with open(self.filename, 'wb') as f:
            f.write(res)

    def _pack_dict(self, data: dict):
        ret = b''
        # Pack dict: store the # of keys, then for each key/value strings.
        ret += pack('i', len(data))
        for key, value in data.items():
            ret += pack('i', len(key))
            ret += b''.join(pack('s', key[c:c+1]) for c in range(len(key)))
            ret += pack('i', len(value))
            ret += b''.join(pack('s', value[c:c+1]) for c in range(len(value)))
        return ret

    def to_bytes(self):

        res = pack('4si', b'VOX ', 150)

        chunks = []

        if len(self.vox.models):
            chunks.append((b'PACK', pack('i', len(self.vox.models))))

        for m in self.vox.models:
            chunks.append((b'SIZE', pack('iii', *m.size)))
            chunks.append((b'XYZI', pack('i', len(m.voxels)) + b''.join(pack('BBBB', *v) for v in m.voxels)))

        if not self.vox.default_palette:
            # The palette needs to contain 255 items of MagicaVoxel will overflow the read.
            chunks.append((b'RGBA', b''.join(pack('BBBB', *c) for c in self.vox.palette) + b''.join(pack('BBBB', 0x00, 0x00, 0x00, 0xFF) for i in range(256 - len(self.vox.palette)))))

        for m in self.vox.materials:
            chunks.append((b'MATL', pack('i', m.id) + self._pack_dict({
                b'_type': m.type,
                b'_weight': str(m.weight).encode('ascii'),
                **{ (b'_' + key.encode('ascii')): str(value).encode('ascii') for key, value in m.props.items() },
            })))

        # TODO materials

        res += self._chunk(b'MAIN', b'', chunks)

        return res
