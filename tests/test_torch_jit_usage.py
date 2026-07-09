import ast
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SERVER_ROOT = REPO_ROOT / "server"


def _attribute_chain(node):
    parts = []
    current = node

    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value

    if isinstance(current, ast.Name):
        parts.append(current.id)
        return ".".join(reversed(parts))

    return None


def test_server_code_does_not_call_torch_jit_script():
    for path in SERVER_ROOT.rglob("*.py"):
        tree = ast.parse(path.read_text(), filename=str(path))

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = _attribute_chain(node.func)
                assert func_name != "torch.jit.script", (
                    f"{path.relative_to(REPO_ROOT)} must not call torch.jit.script() "
                    "while GHSA-rrmf-rvhw-rf47 remains unpatched upstream."
                )
