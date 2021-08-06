from models.sbom.cyclonedx import Parser
from common.application import Application, Logger

try:
    Parser.indexname = Application.GetInstance().ConfigData["sbom"]["index"]
except KeyError as e:
    Logger.getLogger(__name__).info("Using default value for " + e)

try:
    Parser.timeStampField = Application.GetInstance().ConfigData["sbom"]["timestamp-field"]
except KeyError as e:
    Logger.getLogger(__name__).info("Using default value for " + e)

Logger.getLogger(__name__).debug("Using Index: {}, timestamp field: {}".format(
    Parser.indexname, Parser.timeStampField
))