import uvicorn

if __name__ == '__main__':
    uvicorn.run(
        app='api:app',
        host='0.0.0.0',
        port=8200,
        reload=True,
        timeout_graceful_shutdown=0,
        log_level='debug'
    )