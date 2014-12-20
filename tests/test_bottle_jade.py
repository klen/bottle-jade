""" Tests for `bottle-jade` module. """


def test_bottle_jade():
    from bottle import Bottle
    from bottle_jade import JadePlugin
    from os import path as op
    import webtest

    app = Bottle()
    templates = op.dirname(op.abspath(__file__))
    jade = app.install(JadePlugin(template_folder=templates))

    @app.route('/')
    def index():
        context = {'var': 'value'}
        return jade.render('index.jade', **context)

    @app.route('/simple')
    @jade.view('simple.jade')
    def simple():
        context = {}
        return context

    client = webtest.TestApp(app)
    response = client.get('/')
    assert b'Hello world' in response.body

    response = client.get('/simple')
    assert b'Simple' in response.body

# pylama:ignore=W0612
