# Install KNative Serving

```bash
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.8.1/serving-crds.yaml
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.8.1/serving-core.yaml
```

```bash
# No DNS
kubectl patch configmap/config-domain \
      --namespace knative-serving \
      --type merge \
      --patch '{"data":{"advanced-mlops.ai":""}}'
```

# Install Istio v1.14.6

## Install istioctl
```bash
curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.14.6  sh -
```

```bash
istioctl install -y

kubectl apply -l knative.dev/crd-install=true -f https://github.com/knative/net-istio/releases/download/knative-v1.8.1/istio.yaml
kubectl apply -f https://github.com/knative/net-istio/releases/download/knative-v1.8.1/istio.yaml
kubectl apply -f https://github.com/knative/net-istio/releases/download/knative-v1.8.1/net-istio.yaml
```

# Install Cert Manager

```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.12.0/cert-manager.yaml
```

# Test Cert Manager

```bash
kubectl apply -f test-cert-manager.yaml
```

# Install KServe

```bash
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.10.0/kserve.yaml
kubectl apply -f https://github.com/kserve/kserve/releases/download/v0.10.0/kserve-runtimes.yaml
```