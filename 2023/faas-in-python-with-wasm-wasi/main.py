"""FastAPI で wasm (wasi) を実行して wasi の出力を返すサンプル."""
import json
import logging
from typing import Any

from aiofiles import tempfile
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from wasmtime import Engine, Linker, Module, Store, WasiConfig, WasmtimeError

app = FastAPI()

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)


class Item(BaseModel):
    """Item."""

    name: str
    age: int
    description: str


@app.get("/{funcname}")
async def execute(funcname: str) -> Item:
    """Execute wasm function."""
    # refs: https://gist.github.com/pims/711549577759ad1341f1a90860f1f3a5

    wasm_path = f"functions/{funcname}.wasm"
    # create data
    d = {"name": "zztkm", "age": 20}

    try:
        item_dict = await invoke_wasm_module(funcname, wasm_path, d)
        return Item(**item_dict)
    except Exception:
        logger.exception("error")
        raise HTTPException(status_code=400, detail="Bad Request") from None


async def invoke_wasm_module(modname: str, wasm_path: str, input_data: dict[str, Any]) -> dict[str, Any]:
    """Invoke wasm module."""
    # refs: https://gist.github.com/pims/711549577759ad1341f1a90860f1f3a5

    engine = Engine()
    linker = Linker(engine)
    linker.define_wasi()

    # functions/funcname.wasm が存在するか確認
    try:
        module = Module.from_file(linker.engine, wasm_path)
    except Exception:
        logger.exception("module not found %s", wasm_path)
        raise

    config = WasiConfig()

    # generate tenmporary file for stdout_file
    async with tempfile.NamedTemporaryFile() as f:
        config.stdout_file = f.name
        config.env = [["DATA", json.dumps(input_data)]]

        store = Store(linker.engine)
        store.set_wasi(config)

        instance = linker.instantiate(store, module)
        start = instance.exports(store)["_start"]

        logger.info("start wasm module %s", modname)
        try:
            start(store)
            await f.seek(0)
            out = await f.read()
            return json.loads(out.decode(encoding="utf-8"))
        except WasmtimeError as e:
            logger.debug(e)
            await f.seek(0)
            out = await f.read()
            return json.loads(out.decode(encoding="utf-8"))
