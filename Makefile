NAMESPACE ?= kserve-test
GRAPH_FILENAME ?= inferenceGraph.yaml
GRAPH_NAME ?= sequence-test

deploy-graph:
	export NAMESPACE=${NAMESPACE}; \
	export GRAPH_NAME=${GRAPH_NAME}; \
	envsubst < ${GRAPH_FILENAME}.template > ${GRAPH_FILENAME}
	kubectl apply -f inferenceGraph.yaml