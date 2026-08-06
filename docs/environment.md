# Research Environment

## Audited environment

The completed Bitcoin and electricity experiments were run on a CPU-only Windows workstation. No GPU is required to reproduce the completed experiments, although foundation-model inference can be computationally expensive.

| Component | Audited value |
|---|---|
| Python | 3.13.2 |
| Operating system | Windows 11, build 26100 |
| Compute | CPU-only, AMD64 |
| NumPy | 2.4.6 |
| pandas | 3.0.3 |
| Matplotlib | 3.11.0 |
| scikit-learn | 1.9.0 |
| statsmodels | 0.14.6 |
| SciPy | 1.18.0 |
| TensorFlow | 2.21.0 |
| PyTorch | 2.12.1 |
| chronos-forecasting | 2.3.1 |
| TimesFM | 2.0.2 |
| psutil | 7.2.2 |
| datasets | 2.19.2 |

The project `.venv` contains a `jupyter.exe` launcher. The audit found Jupyter and nbformat-related tooling resolving partly outside the virtual environment's package metadata. The external tooling reported nbconvert 7.16.6, nbformat 5.10.4, and ipykernel 6.29.5. A clean reproduction must install notebook tooling explicitly rather than relying on workstation-level packages. [`requirements-research.txt`](../requirements-research.txt) is the authoritative direct-dependency specification; the older `requirements.txt` is retained for historical compatibility.

## Known blockers

- **Moirai / Uni2TS:** unavailable in the completed Python 3.13 workflow because the required dependency stack was not compatible with this environment.
- **PatchTST and iTransformer:** NeuralForecast depends on packages, including Ray in the tested installation path, that were unavailable for Python 3.13. A supported Python 3.11 or 3.12 environment is recommended; see [`patchtst_itransformer_environment.md`](patchtst_itransformer_environment.md).
- These unavailable models have no authoritative forecasts and are not included in rankings.

## Reproduction boundaries

Downstream trustworthiness, significance, and cross-domain analyses operate on saved forecast vectors. They do not require model checkpoints. Reproducing model generation from scratch is a separate, substantially more expensive operation and must not overwrite the frozen artifacts without an explicit new experiment version.
