RouterRoot = "/"
RouterEvaluation = "/v1/evaluation/{name}"
RouterFluency = "/v1/fluency"
RouterUnderstand = "/v1/understand"
RouterDivergence = "/v1/divergence"
RouterSimilarity = "/v1/similarity"
RouterQueryStatus = "/v1/query_status"

BadRequestStatusCode = 400

OPENAI_API_KEY = "OPENAI_API_KEY"
EMBEDDING_MODEL = "text-embedding-ada-002"

StageInit = "init"
StageSimilarity = "do_similarity"
StageStyle = "do_style"
StageFluency = "do_fluency"
StageUnderstand = "do_understand"
StageDivergence = "do_divergence"
StageStatusPadding = "status_padding"
StageStatusDone = "status_done"
StageStatusFailed = "status_failed"
