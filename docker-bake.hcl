variable "REGISTRY" {
  default = "ghcr.io/eyepop-ai"
}

variable "TAG" {
  default = "latest"
}

group "default" {
  targets = ["app"]
}

target "app" {
  context    = "."
  dockerfile = "Dockerfile"
  push       = true
  tags = [
    "${REGISTRY}/sdsu-desert-kites:${TAG}",
    "${REGISTRY}/sdsu-desert-kites:latest",
  ]
  platforms = ["linux/amd64"]
  cache-from = [
    "type=registry,ref=${REGISTRY}/sdsu-desert-kites:cache"
  ]
  cache-to = [
    "type=registry,ref=${REGISTRY}/sdsu-desert-kites:cache,mode=max"
  ]
}
