# shop-backend

Demo app for Codesphere global deployments. Its landscape (`ci.prod.yml`) has two private services:
`inference`, which needs a GPU data center, and `model-store`, which `inference` calls inside the landscape.
The global config places it on a DC labelled `gpu` and lets the frontend's `api-gateway` call `inference`.
