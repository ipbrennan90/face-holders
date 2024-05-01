---
title: Face Holders
emoji: 🏃
colorFrom: pink
colorTo: green
sdk: docker
pinned: false
license: mit
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference


## Getting Started

install dependencies

```
pip install -r requirements.txt
```

Add openai api key to .env

```
OPENAI_API_KEY=<your key here>
```

Run the chat bot locally

```
chainlit run app.py -w
```

## Stop... it's Docker time.

In order to ensure a successful deploy to HuggingFace it's good to double check docker is working

Run the build

```
docker build -t faceholders .
```

Spin it up locally

```
docker run -p 7860:7860 faceholders
```

Check out your amazing running dockerized app at http://localhost:7860