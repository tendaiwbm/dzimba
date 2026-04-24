import logging

logger = logging.getLogger("Verra")

import requests as rq

from .model import VerraModel as model
from .config import verraConfig as source
from ..utils import *

def request(url):
    return rq.get(url).json()

def pipeline():
    pipelineSetup = {
                      "request": {"function": request, "args": [create_path([source["domain"],source["endpoint"]])]},
                      "parser": None,
                      "directory": source["path"],
                      "file": source["localFileName"],
                      "model": model,
                      "source": source["name"],
                      "hostUrl": source["domain"],
                      "listingUrlColumn": model.itemUrl,
                      "filter": source["filters"],
                      "logger": logger
                    }

    worker = Pipeline(pipelineSetup)
    return worker.execute()
