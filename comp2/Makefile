VERSION ?= $(shell git describe --tags --always --dirty)

REPOSITORY ?= 129231402580.dkr.ecr.ap-northeast-1.amazonaws.com
IMG ?= serving
COMPONENT_NAME ?= comp2
TAG ?= ${COMPONENT_NAME}-${VERSION}

SERVICE_FILENAME ?= inferenceService.yaml
NAMESPACE ?= kserve-test

docker-build:
	aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin ${REPOSITORY} && \
	docker build -t ${IMG}:${TAG} .

local-test: docker-build
	docker run -p 8080:8080 -t ${IMG}:${TAG}

docker-push: docker-build
	docker tag ${IMG}:${TAG} ${REPOSITORY}/${IMG}:${TAG}
	docker push ${REPOSITORY}/${IMG}:${TAG}
	docker rmi ${REPOSITORY}/${IMG}:${TAG}
	docker rmi ${IMG}:${TAG}

deploy-k8s:
	export REPOSITORY=${REPOSITORY}; \
	export IMG=${IMG}; \
	export TAG=${TAG}; \
	export COMPONENT=${COMPONENT_NAME}; \
	export NAMESPACE=${NAMESPACE}; \
	envsubst < ${SERVICE_FILENAME}.template > ${SERVICE_FILENAME}
	ISVC=$(kubectl get isvc -n ${NAMESPACE} | grep ${COMPONENT}); \
	if [ -z ${ISVC} ]; then \
		echo Not Exist; \
	else \
		kubectl delete isvc ${COMPONENT}; \
	fi;
	kubectl apply -f ${SERVICE_FILENAME}