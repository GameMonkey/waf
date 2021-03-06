#! /usr/bin/env python
# encoding: utf-8

# This file contains the methods added to the ConfigurationContext
# and BuildContext objects. This means that you can use these methods
# inside the configure(...) and build(...) functions defined in most
# wscripts.

from waflib.Configure import conf
from waflib.Errors import WafError
from waflib import Logs

from . import waf_resolve_context


@conf
def dependency_path(ctx, name):
    """
    Returns the dependency path
    """
    return waf_resolve_context.dependency_cache[name]['path']


@conf
def has_dependency_path(ctx, name):
    """
    Returns true if a path is available for the dependency
    """
    return name in waf_resolve_context.dependency_cache


@conf
def is_toplevel(self):
    """
    Returns true if the current script is the top-level wscript
    """
    return self.srcnode == self.path


@conf
def recurse_dependencies(ctx):
    """ Recurse the dependencies which have the resolve property set to True.

    :param ctx: A Waf Context instance.
    """

    # See if we have a log file, we do this here to avoid raising
    # excpetions and destroying traceback inside the excpetion
    # handler below.
    try:
        logfile = ctx.logger.handlers[0].baseFilename
    except:
        logfile = None

    # Since dependency_cache is an OrderedDict, the dependencies will be
    # enumerated in the same order as they were defined in the wscripts
    # (waf-tools should be the first if it is defined)
    for name, dependency in waf_resolve_context.dependency_cache.items():

        if not dependency['recurse']:

            Logs.debug('resolve: Skipped recurse {} cmd={}'.format(
                name, ctx.cmd))

            continue

        path = dependency['path']

        Logs.debug('resolve: recurse {} cmd={}, path={}'.format(
            name, ctx.cmd, path))

        try:
            # @todo mandatory is False here, which means that no wscript
            # is required to exist. Not sure if this is really a good idea?
            # As a minimum it should be described here why that is the
            # case. Because it opens the door to errors where e.g. the
            # user points the dependency to some empty folder. Which will
            # not fail them - but probably should?
            # There is a unit test in:
            # test/fail_recurse/test_fail_recurse.py which should fail
            # if mandatory is changed to True
            #
            # str() is needed as waf does not handle unicode in find_node
            ctx.recurse([str(path)], once=False, mandatory=False)
        except WafError as e:

            msg = 'Recurse "{}" for "{}" failed with: {}'.format(
                name, ctx.cmd, e.msg)

            if logfile:
                msg = '{}\n(complete log in {})'.format(msg, logfile)
            else:
                msg = '{}\n(run with -v for more information)'.format(msg)

            raise WafError(msg=msg, ex=e)
