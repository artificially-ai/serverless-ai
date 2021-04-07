def greet(context, event):
    context.logger.info('Some one is knocking at the door.')

    return context.Response(body='Hello, from Nuclio :]',
                            headers={},
                            content_type='text/plain',
                            status_code=200)
