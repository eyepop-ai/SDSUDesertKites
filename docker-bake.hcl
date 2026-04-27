variable "REGISTRY" {
  default = "ghcr.io/eyepop-ai"
}

variable "TAG" {
  default = "latest"
}

target "app" {
  context    = "."
  dockerfile = "Dockerfile"
  push       = true
  output     = ["type=registry"]
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
