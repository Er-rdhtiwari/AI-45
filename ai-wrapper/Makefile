.PHONY: all build test vet fmt check clean

VERSION ?= dev

all: check build

build:
	mkdir -p bin
	go build -trimpath -ldflags "-s -w -X main.version=$(VERSION)" -o bin/ai-status-wrapper ./cmd/ai-status-wrapper

test:
	go test ./...

vet:
	go vet ./...

fmt:
	gofmt -w $$(find . -name '*.go' -type f)

check: test vet

clean:
	rm -rf bin
