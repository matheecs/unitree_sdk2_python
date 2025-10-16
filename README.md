# 机器人可视化工具 DViz (is not RViz)

```bash
conda create -y -n dds python=3.10
conda activate dds

# [dep] pin3
conda install pinocchio -c conda-forge
# [dep] meshcat
pip install meshcat
# [dep] sdk2
pip install -e .

python dviz.py
```
