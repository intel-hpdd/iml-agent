#
# INTEL CONFIDENTIAL
#
# Copyright 2013 Intel Corporation All Rights Reserved.
#
# The source code contained or described herein and all documents related
# to the source code ("Material") are owned by Intel Corporation or its
# suppliers or licensors. Title to the Material remains with Intel Corporation
# or its suppliers and licensors. The Material contains trade secrets and
# proprietary and confidential information of Intel or its suppliers and
# licensors. The Material is protected by worldwide copyright and trade secret
# laws and treaty provisions. No part of the Material may be used, copied,
# reproduced, modified, published, uploaded, posted, transmitted, distributed,
# or disclosed in any way without Intel's prior express written permission.
#
# No license under any patent, copyright, trade secret or other intellectual
# property right is granted to or conferred upon you by disclosure or delivery
# of the Materials, either expressly, by implication, inducement, estoppel or
# otherwise. Any license under such intellectual property rights must be
# express and approved by Intel in writing.


from chroma_agent.device_plugins.audit.fscontext import FileSystemContext


class FileSystemMixin(object):
    """Mixin for Audit subclasses.  Classes that inherit from
    this mixin will get a number of methods for interacting with a
    filesystem.  The context property provides a way to override the
    default filesystem context ("/") for unit testing.
    """

    def __set_fscontext(self, ctx):
        if hasattr(ctx, "root"):
            self.__fscontext = ctx
        else:
            self.__fscontext = FileSystemContext(ctx)

    def __get_fscontext(self):
        # This bit of hackery is necessary due to the fact that mixins
        # can't have an __init__() to set things up.
        if not '_FileSystemMixin__fscontext' in self.__dict__:
            self.__fscontext = FileSystemContext()
        return self.__fscontext

    fscontext = property(__get_fscontext, __set_fscontext, doc="""
        The filesystem context (defaults to "/")""")

    def read_lines(self, filename, filter_f=None):
        """Return a generator for stripped lines read from the file.

        If the optional filter_f argument is supplied, it will be applied
        prior to stripping each line.
        """
        for line in open(self.fscontext.abs(filename)):
            if filter_f:
                if filter_f(line):
                    yield line.rstrip("\n")
            else:
                yield line.rstrip("\n")

    def read_string(self, filename):
        """Read the first line from a file and return it as a string."""
        try:
            return self.read_lines(filename).next()
        except StopIteration:
            raise RuntimeError("read_string() on empty file: %s" % filename)

    def read_int(self, filename):
        """Read one line from a file and return it as an int."""
        return int(self.read_string(filename))
