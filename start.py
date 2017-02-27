import os

'''
Launch separate apps depending on deployment location.
Use environment variable to determine load module.
'''

if os.environ.get('LAUNCH_CHATBOT', False):
    from chatbot import chatbot
else:
    import webapp
