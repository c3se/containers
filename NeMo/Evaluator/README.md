# NeMo Evaluator

NeMo Evaluator provides a collection of specialized containers for different
evaluation frameworks and tasks. Each container is optimized and tested to work
seamlessly with NVIDIA hardware and software stack, providing consistent,
reproducible environments for AI model evaluation.

See
<https://docs.nvidia.com/nemo/evaluator/latest/libraries/nemo-evaluator/containers/index.html>
for details.

If you would like us to add another container here let us know through
<https://supr.naiss.se/support/>.

## Guide

1. Launch an LLM that you can interact with through the OpenAI API (such as
   with [vLLM](https://www.c3se.chalmers.se/documentation/software/machine_learning/vllm/)).
2. Launch the nemo-evalutor in the corresponding container:

```bash
apptainer exec <path-to-sif-container-here> nemo-evaluator run_eval --eval_type ...
```

