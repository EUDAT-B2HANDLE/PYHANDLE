class BatchFileExistsException(Exception):
      """ Raises when batch files does not exists"""

      def __init__(self, **args):
         # Default message:
         self.msg = 'Batch file '
         self.file = args['file']
         self.custom_message = args['msg']

         if self.file is not None:
            self.msg = self.msg.replace('ile ', 'ile ' + self.file)

         if self.custom_message is not None:
             self.msg += ': ' + self.custom_message
         self.msg += '.'

         super(self.__class__, self).__init__(self.msg)