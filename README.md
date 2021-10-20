numpy-vox-io
============

*This is a fork of [py-vox-io](https://github.com/gromgull/py-vox-io). Many thanks to Gunnar Aastrand Grimnes for writing and sharing it.*

**This project is a WIP and I'm pausing development while I wait for the MagicaVoxel vox format to be a little less churny and be fully documented.**

**Current status: Updated for Magicavoxel 0.99.6.4 (Released September 5, 2021). Reading materials is still unsupported.**
For more info see https://github.com/alexhunsley/numpy-vox-io/issues/4


A Python parser and writer for the [Magica Voxel .vox
format](https://github.com/ephtracy/voxel-model/blob/master/MagicaVoxel-file-format-vox.txt)

![sample1](https://raw.githubusercontent.com/gromgull/py-vox-io/master/samples/1.png)
![sample2](https://raw.githubusercontent.com/gromgull/py-vox-io/master/samples/2.png)


The base parser/writer has no dependencies.

The VOX model class has methods to convert to/from numpy arrays, these
require numpy (duh) and pillow for image quantisation.
