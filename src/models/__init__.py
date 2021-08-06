# from models.maven import ModelLibrary
# from common.application import Application, Logger

# try:
#     ModelLibrary.Index.name = Application.GetInstance().ConfigData["mvn"]["index"]
# except KeyError as e:
#     Logger.getLogger(__name__).info("Using default value for " + e)

# Logger.getLogger(__name__).debug("Using Index: {}".format(
#     ModelLibrary.Index.name
# ))
