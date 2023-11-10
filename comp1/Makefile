VERSION ?= $(shell git describe --tags --always --dirty)

REPOSITORY ?= 129231402580.dkr.ecr.ap-northeast-1.amazonaws.com
IMG ?= serving
COMPONENT_NAME ?= comp1
TAG ?= ${COMPONENT_NAME}-${VERSION}

SERVICE_FILENAME ?= inferenceService.yaml

docker-build:
	aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin ${REPOSITORY} && \
	pack build --builder=heroku/buildpacks:20 ${IMG}:${TAG}

local-test: docker-build
	docker run -p 8080:8080 -t ${IMG}:${TAG}

docker-push: docker-build
	docker tag ${IMG}:${TAG} ${REPOSITORY}/${IMG}:${TAG}
	docker push ${REPOSITORY}/${IMG}:${TAG}
	docker rmi ${REPOSITORY}/${IMG}:${TAG}

deploy-k8s:
	export REPOSITORY=${REPOSITORY}; \
	export IMG=${IMG}; \
	export TAG=${TAG}; \
	export COMPONENT=${COMPONENT_NAME}; \
	envsubst < ${SERVICE_FILENAME}.template > ${SERVICE_FILENAME}
	kubectl apply -f ${SERVICE_FILENAME}