"""FastAPI で wasm (wasi) を実行して wasi の出力を返すサンプル."""
import logging
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, HTTPException
from wasmtime import Engine, Linker, Module, Store, WasiConfig, WasmtimeError

app = FastAPI()

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)


@app.get("/{funcname}")
async def execute(funcname: str) -> dict[str, str]:
    """Execute wasm function."""
    # refs: https://gist.github.com/pims/711549577759ad1341f1a90860f1f3a5

    engine = Engine()
    linker = Linker(engine)
    linker.define_wasi()

    # functions/funcname.wasm が存在するか確認
    try:
        module = Module.from_file(linker.engine, f"functions/{funcname}.wasm")
    except Exception:
        logger.exception("module not found")
        raise HTTPException(status_code=400, detail="Bad Request") from None

    config = WasiConfig()
    # generate tenmporary file for stdout
    f = NamedTemporaryFile()
    config.stdout_file = Path(f.name)
    config.env = [["NAME", "zztkm"]]

    store = Store(linker.engine)
    store.set_wasi(config)

    instance = linker.instantiate(store, module)

    start = instance.exports(store)["_start"]

    try:
        start(store)
        f.seek(0)
        out = f.read()
        return {"hello": out.decode(encoding="utf-8")}
    except WasmtimeError as e:
        logger.debug(e)
        f.seek(0)
        out = f.read()
        return {"hello": out.decode(encoding="utf-8")}
    except Exception:
        logger.exception("error")
        raise HTTPException(status_code=500, detail="Internal Server Error") from None
