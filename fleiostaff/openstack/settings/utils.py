import re
from six.moves.urllib import parse
from kombu.connection import Connection
from amqp.exceptions import AccessRefused
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _


def parse_test_url(url):
    _url = ''
    driver = 'kombu'
    if url.hosts:
        for host in url.hosts:
            transport = url.transport.replace('kombu+', '')
            transport = transport.replace('rabbit', 'amqp')
            if transport == 'pika':
                driver = 'pika'
                transport = transport.replace('pika', 'amqp')
            _url += '%s%s://%s:%s@%s:%s/%s' % (
                ";" if _url else '',
                transport,
                parse.quote(host.username or ''),
                parse.quote(host.password or ''),
                '[%s]' % host.hostname if ':' in host.hostname else host.hostname,
                str(host.port or 5672),
                url.virtual_host)
    elif url.transport.startswith('kombu+'):
        transport = url.transport.replace('kombu+', '')
        _url = "%s://%s" % (transport, url.virtual_host)
    if url.query:
        _url = "%s?%s" % (_url, '&'.join(['{}={}'.format(key, value) for key, value in url.query.items()]))
    return _url, driver


def connection_thread(url, results, hide_password=False):
    from oslo_config import cfg
    from oslo_messaging.transport import TransportURL
    from pika import exceptions as pika_exceptions
    from pika import URLParameters as PikaUrlParameters
    from pika import BlockingConnection as PikaBlockingConnection
    try:
        parsed_url = TransportURL.parse(cfg.CONF, url)
        if hide_password:
            url = re.sub(':+[^:@]+@', ':******@', url)
    except Exception as e:
        results.append({'url': url, 'exception': e})
    else:
        test_url, driver = parse_test_url(parsed_url)
        try:
            if driver == 'kombu':
                connection = Connection(test_url)
                connection.connect()
                connection.close()
            elif driver == 'pika':
                params = PikaUrlParameters(test_url)
                params.socket_timeout = 5
                conn = PikaBlockingConnection(params)
                conn.close()
        except (OSError, pika_exceptions.ConnectionClosed):
            results.append({'url': url, 'exception': _('Url not reachable')})
        except (AccessRefused, pika_exceptions.ProbableAuthenticationError):
            results.append({'url': url, 'exception': _('Credentials incorrect')})
        except Exception as e:
            results.append({'url': url, 'exception': force_text(e)})
        else:
            results.append({'url': url})
